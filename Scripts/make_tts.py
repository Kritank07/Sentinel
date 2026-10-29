import asyncio, edge_tts, soundfile as sf

TEXT = ("Hello, main CBI officer bol raha hoon. Aapka Aadhaar money laundering case mein "
        "link hai. Verification ke liye pachaas hazaar rupaye transfer kariye, warna arrest hoga.")

async def main():
    await edge_tts.Communicate(TEXT, "hi-IN-MadhurNeural").save("samples/ai_voice.mp3")
    audio, rate = sf.read("samples/ai_voice.mp3")
    sf.write("samples/ai_voice.wav", audio, rate, subtype="PCM_16")
    print("Saved samples/ai_voice.wav")

asyncio.run(main())