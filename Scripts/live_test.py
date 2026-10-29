import asyncio, json, os, uuid
import numpy as np
import sounddevice as sd
import websockets
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("MODEL_API_KEY")

RATE = 24_000
FRAME_SAMPLES = RATE * 80 // 1000   # 80 ms per frame
DURATION = 20                        # seconds to listen
seen_types = set()
max_level = 0

async def live_transcribe():
    global max_level
    uri = f"wss://api.meta.ai/v1/asr/realtime?sessionId=sentinel-{uuid.uuid4()}"
    loop = asyncio.get_running_loop()
    audio_q: asyncio.Queue = asyncio.Queue()

    def mic_callback(indata, frames, time, status):
        global max_level
        level = int(np.abs(np.frombuffer(indata, dtype=np.int16)).mean())
        max_level = max(max_level, level)
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
        print("✅ Connected. Speak now...\n")

        async def receive_events():
            async for message in ws:
                if isinstance(message, bytes):
                    continue
                event = json.loads(message)
                etype = event.get("type")
                if etype == "error":
                    raise RuntimeError(event.get("message"))
                # Print each new event type once, plus every non-empty final transcript
                if etype not in seen_types:
                    seen_types.add(etype)
                    print("NEW EVENT TYPE:", json.dumps(event, ensure_ascii=False))
                elif event.get("final") and event.get("transcript"):
                    print("FINAL:", json.dumps(event, ensure_ascii=False))

        receiver = asyncio.create_task(receive_events())

        with sd.RawInputStream(samplerate=RATE, channels=1, dtype="int16",
                               blocksize=FRAME_SAMPLES, callback=mic_callback):
            end = loop.time() + DURATION
            while loop.time() < end:
                chunk = await audio_q.get()
                await ws.send(chunk)

        await ws.send(json.dumps({"type": "endStream"}))
        try:
            await asyncio.wait_for(receiver, timeout=10)
        except asyncio.TimeoutError:
            receiver.cancel()
            print("\n(server didn't close, stopped after 10s)")

    print(f"\n⏹️ Done. Max mic level: {max_level}")
    print("Event types seen:", seen_types)

asyncio.run(live_transcribe())