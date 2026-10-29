import asyncio, json, os, uuid
import sounddevice as sd
import websockets
from dotenv import load_dotenv
from sentinel.engine import analyze_text
import sys

load_dotenv()
API_KEY = os.getenv("MODEL_API_KEY")

RATE = 24_000
FRAME_SAMPLES = RATE * 80 // 1000   # 80 ms per frame
DURATION = 45                        # seconds to listen
USER_LANGUAGE = sys.argv[1].strip().title() if len(sys.argv) > 1 else "Hindi"

history = []
current_speaker = "A"
COLORS = {"SAFE": "🟢", "SUSPICIOUS": "🟡", "SCAM": "🔴"}
seq = 0
last_shown_seq = 0
last_score = -1
last_verdict = None

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


async def analyze_live():
    global seq, last_shown_seq, last_score, last_verdict
    seq += 1
    my_seq = seq
    convo = LIVE_CONTEXT + "\nTRANSCRIPT:\n" + "\n".join(history[-12:])

    try:
        v = await asyncio.to_thread(analyze_text, convo, USER_LANGUAGE, "muse-spark-1.3")
    except Exception as e:
        print(f"\n(analysis error: {e})")
        return

    if my_seq < last_shown_seq:          # an older result arrived late, ignore it
        return

    if v.get("user_at_risk"):
        last_shown_seq = my_seq
        print("\n" + "🛑" * 10)
        print(f"🛑 {v.get('stop_message') or STOP_MESSAGES.get(USER_LANGUAGE, STOP_MESSAGES['English'])}")
        print(f"🛑 {v['action']}")
        print("🛑" * 10)
        return

    score, verdict = v["threat_score"], v["verdict"]
    if verdict != last_verdict or score >= last_score + 10:
        last_shown_seq, last_score, last_verdict = my_seq, score, verdict
        icon = COLORS.get(verdict, "⚪")
        print(f"\n{icon} {verdict} ({score}) — {v.get('scam_type') or 'no scam detected'}")
        if verdict != "SAFE":
            print(f"   ⚠️ {v['action']}")


async def live_shield():
    uri = f"wss://api.meta.ai/v1/asr/realtime?sessionId=sentinel-{uuid.uuid4()}"
    loop = asyncio.get_running_loop()
    audio_q: asyncio.Queue = asyncio.Queue()
    tasks = []

    def mic_callback(indata, frames, time, status):
        loop.call_soon_threadsafe(audio_q.put_nowait, bytes(indata))

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
        print("🛡️ Sentinel live shield active. Start the call...\n")

        async def receive_events():
            global current_speaker
            async for message in ws:
                if isinstance(message, bytes):
                    continue
                event = json.loads(message)
                etype = event.get("type")
                if etype == "error":
                    raise RuntimeError(event.get("message"))
                if etype == "speaker":
                    current_speaker = event.get("label", current_speaker)
                elif etype == "speechComplete" and event.get("transcript", "").strip():
                    line = f"Speaker {current_speaker}: {event['transcript'].strip()}"
                    history.append(line)
                    print(f"\n💬 {line}")
                    tasks.append(asyncio.create_task(analyze_live()))

        receiver = asyncio.create_task(receive_events())

        with sd.RawInputStream(samplerate=RATE, channels=1, dtype="int16",
                               blocksize=FRAME_SAMPLES, callback=mic_callback):
            end = loop.time() + DURATION
            while loop.time() < end:
                await ws.send(await audio_q.get())

        await ws.send(json.dumps({"type": "endStream"}))
        try:
            await asyncio.wait_for(receiver, timeout=10)
        except asyncio.TimeoutError:
            receiver.cancel()

    if tasks:                            # let pending analyses finish
        await asyncio.gather(*tasks, return_exceptions=True)
    print("\n⏹️ Call ended.")


asyncio.run(live_shield())

