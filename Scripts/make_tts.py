import asyncio
import edge_tts

# A "family emergency" voice-clone scam: urgent, emotional, asks for money and secrecy.
TEXT = (
    "मम्मी, मैं रोहित बोल रहा हूँ... मेरा एक्सीडेंट हो गया है, मैं अभी पुलिस स्टेशन में हूँ। "
    "प्लीज़ घबराना मत। यहाँ इंस्पेक्टर कह रहे हैं कि अभी बीस हज़ार रुपये जमा करने पड़ेंगे, "
    "नहीं तो केस बन जाएगा। मैं आपको एक नंबर भेज रहा हूँ, उस पर तुरंत गूगल पे कर दो। "
    "और प्लीज़... पापा को अभी मत बताना, मैं बाद में सब समझा दूँगा।"
)

async def main():
    voice = edge_tts.Communicate(TEXT, "hi-IN-MadhurNeural", rate="+6%")
    await voice.save("web/samples/ai_voice.mp3")
    print("Saved web/samples/ai_voice.mp3")

asyncio.run(main())