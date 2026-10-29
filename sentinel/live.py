import asyncio, json, os, uuid
import websockets
from dotenv import load_dotenv
from sentinel.engine import analyze_text

load_dotenv()
API_KEY = os.getenv("MODEL_API_KEY")
ASR_URL = "wss://api.meta.ai/v1/asr/realtime"

STOP_MESSAGES = {
    "Hindi": "रुकिए! पैसे न भेजें और कोई OTP या जानकारी न दें — यह धोखा है। अभी फ़ोन काट दें।",
    "Hinglish": "Rukiye! Paise mat bhejiye, koi OTP ya detail mat dijiye — yeh scam hai. Abhi phone kaatiye.",
    "English": "STOP! Don't send money or share any OTP or details — this is a scam. Hang up now.",
}

LIVE_CONTEXT = """This is a LIVE phone call transcript between Speaker A and Speaker B.
One may be a scammer and the other the user being protected.
In addition to the standard fields, include:
  "scammer_speaker": "A" or "B" or null,
  "user_at_risk": true if the protected user is agreeing to pay, sharing an OTP,
                  password, bank or ID details, or installing an app, else false,
  "stop_message": an urgent warning in the USER LANGUAGE, following these rules:
      - Start with the word for "STOP" in that language
      - Name the exact thing the scammer wants (e.g. "Do not send the ₹50,000",
        "Do not share the OTP"), using details from the transcript
      - Give one short reason the request is fake (e.g. "Real police never ask
        for money on a call")
      - End with one clear action: hang up now
      - Max 2 short sentences, under 30 words, everyday words a grandparent
        understands, respectful tone, no technical terms
      - Use the user's natural script (Devanagari for Hindi, Roman for Hinglish)
"""


class LiveSession:
    """Relays call audio to Muse Voice Transcribe and pushes events through `send`."""

    def __init__(self, language: str, send):
        self.language = language
        self.send = send                     # async function that delivers a dict to the browser
        self.history, self.tasks = [], []
        self.speaker = "A"
        self.seq = self.last_shown = 0
        self.last_score, self.last_verdict = -1, None

    async def _analyze(self):
        self.seq += 1
        my_seq = self.seq
        convo = LIVE_CONTEXT + "\nTRANSCRIPT:\n" + "\n".join(self.history[-12:])
        try:
            v = await asyncio.to_thread(analyze_text, convo, self.language, "muse-spark-1.3")
        except Exception:
            await self.send({"type": "error", "message": "One line couldn't be checked. Still listening."})
            return
        if my_seq < self.last_shown:          # an older result arrived late
            return

        if v.get("user_at_risk"):
            self.last_shown = my_seq
            await self.send({"type": "stop",
                             "message": v.get("stop_message")
                                        or STOP_MESSAGES.get(self.language, STOP_MESSAGES["English"]),
                             "action": v.get("action")})
            return

        score, verdict = v.get("threat_score", 0), v.get("verdict", "SAFE")
        if verdict != self.last_verdict or score >= self.last_score + 10:
            self.last_shown, self.last_score, self.last_verdict = my_seq, score, verdict
            await self.send({"type": "verdict", "verdict": verdict, "score": score,
                             "scam_type": v.get("scam_type"), "explanation": v.get("explanation"),
                             "action": v.get("action"), "scammer_speaker": v.get("scammer_speaker")})

    async def run(self, audio_source):
        """audio_source: async iterator of 24 kHz 16-bit mono PCM chunks; ends when the call ends."""
        uri = f"{ASR_URL}?sessionId=sentinel-{uuid.uuid4()}"
        async with websockets.connect(uri, open_timeout=30) as ws:
            await ws.send(json.dumps({
                "authorization": {"accessToken": f"Bearer {API_KEY}"},
                "audioEncoding": "PCM_24KHZ",
                "model": "muse-voice-transcribe-1.0",
                "mode": "DIARIZATION",
            }))
            handshake = json.loads(await ws.recv())
            if "sessionId" not in handshake:
                raise RuntimeError(f"Handshake failed: {handshake}")
            await self.send({"type": "ready"})

            async def receive():
                async for message in ws:
                    if isinstance(message, bytes):
                        continue
                    e = json.loads(message)
                    etype = e.get("type")
                    if etype == "speaker":
                        self.speaker = e.get("label", self.speaker)
                    elif etype == "transcript" and not e.get("final"):
                        await self.send({"type": "partial", "text": e.get("transcript", "")})
                    elif etype == "speechComplete" and e.get("transcript", "").strip():
                        text = e["transcript"].strip()
                        self.history.append(f"Speaker {self.speaker}: {text}")
                        await self.send({"type": "line", "speaker": self.speaker, "text": text})
                        self.tasks.append(asyncio.create_task(self._analyze()))

            receiver = asyncio.create_task(receive())
            async for chunk in audio_source:
                await ws.send(chunk)
            await ws.send(json.dumps({"type": "endStream"}))
            try:
                await asyncio.wait_for(receiver, timeout=10)
            except asyncio.TimeoutError:
                receiver.cancel()

        if self.tasks:
            await asyncio.gather(*self.tasks, return_exceptions=True)
        await self.send({"type": "ended"})