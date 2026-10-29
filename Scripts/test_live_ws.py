import asyncio, json
import sounddevice as sd
import websockets

RATE, DURATION = 24_000, 40
FRAME = RATE * 80 // 1000

async def main():
    async with websockets.connect("ws://127.0.0.1:8000/ws/live?language=English") as ws:
        loop = asyncio.get_running_loop()
        q: asyncio.Queue = asyncio.Queue()

        def mic(indata, frames, time, status):
            loop.call_soon_threadsafe(q.put_nowait, bytes(indata))

        async def receive():
            async for m in ws:
                e = json.loads(m)
                if e["type"] != "partial":
                    print(e)

        r = asyncio.create_task(receive())
        with sd.RawInputStream(samplerate=RATE, channels=1, dtype="int16",
                               blocksize=FRAME, callback=mic):
            end = loop.time() + DURATION
            while loop.time() < end:
                await ws.send(await q.get())
        await ws.send(json.dumps({"type": "end"}))
        await asyncio.wait_for(r, timeout=60)

asyncio.run(main())