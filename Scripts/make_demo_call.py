# pip install google-genai python-dotenv   (local only, not in requirements.txt)
import mimetypes
import os
import struct

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = "gemini-3.8-flash-tts"
OUTPUT = "web/samples/demo_call.wav"
CALLER_VOICE = "Bodi"      # Speaker 1: Rahul, the fake bank officer
VICTIM_VOICE = "Enya"      # Speaker 2: Mrs Sharma, an older woman

CALLER, VICTIM = "Speaker 1", "Speaker 2"

# (speaker, narration style, line)
LINES = [
    (CALLER, "Warm, polite and professional, like a trained call-centre officer. Confident and helpful. Steady, measured pace.",
     "हैलो, नमस्ते मैडम। मैं राहुल बोल रहा हूँ... आपके बैंक की फ्रॉड प्रिवेंशन टीम से। क्या मेरी बात श्रीमती शर्मा जी से हो रही है?"),
    (VICTIM, "An older woman around 65, cautious and slightly surprised by the call. Mild worry. Slow and hesitant.",
     "<cough> हाँ जी, हाँ... मैं ही बोल रही हूँ। क्या हुआ?"),
    (CALLER, "Calm and reassuring, completely in control, as if this happens every day. Smooth, unhurried pace.",
     "मैडम, घबराइए मत, सब ठीक है। बस... आपके कार्ड से अभी थोड़ी देर पहले एक ट्रांज़ैक्शन ट्राई हुआ है, करीब अड़तालीस हज़ार का, किसी ऑनलाइन वेबसाइट पर। क्या वो आपने किया था?"),
    (VICTIM, "Shocked, with rising anxiety. Slightly breathless, speaking faster than before.",
     "<breath> अड़तालीस हज़ार? अरे बाप रे... नहीं नहीं, मैंने तो कुछ भी नहीं किया!"),
    (CALLER, "Soothing and matter-of-fact, like reading details off a screen. Confident. Steady pace.",
     "जी जी, समझ सकता हूँ। इसीलिए तो हमने उसे होल्ड पर रखा है। उम्म... आपका कार्ड, जिसके आख़िर में दो दो आठ एक है, वही ना?"),
    (VICTIM, "Hesitant at first, then relieved and trusting. Slow, then a little quicker.",
     "हाँ... रुको, हाँ हाँ, वही है।"),
    (CALLER, "Helpful but slightly urgent, sounding genuinely concerned for her money. A little faster.",
     "ठीक है मैडम। देखिए, अगर अभी इसे कैंसल नहीं किया ना, तो दस-पंद्रह मिनट में ये अपने आप पास हो जाएगा। मैं अभी कैंसलेशन रिक्वेस्ट डाल रहा हूँ... आपके फ़ोन पर बैंक का एक कोड आएगा।"),
    (VICTIM, "Flustered and confused, searching for her glasses and phone. Uneven pace with natural pauses.",
     "अच्छा... एक सेकंड बेटा... चश्मा कहाँ रखा... <sigh> हाँ, हाँ, कुछ नंबर आए हैं।"),
    (CALLER, "Friendly and persuasive, patient and gentle. Calm, deliberate pace.",
     "बस, वही कोड मुझे बता दीजिए, ताकि मैं सिस्टम में कन्फ़र्म कर सकूँ कि ये आप ही हैं। फिर आपके पैसे नहीं कटेंगे।"),
    (VICTIM, "Unsure and doubtful, speaking quietly. Slow, trailing off at the end.",
     "पर बेटा... मैसेज में तो लिखा है कि... किसी को मत बताना..."),
    (CALLER, "Smooth and trustworthy with a soft, relaxed laugh, brushing off her doubt. Relaxed at first, then gently pressing and rushed at the end.",
     "<laugh> जी जी, बिल्कुल सही पढ़ा आपने मैडम, वो बाहर वालों के लिए लिखा होता है। मैं तो बैंक से ही बोल रहा हूँ, आपका पैसा बचाने के लिए ही कॉल किया है। बस... जल्दी बता दीजिए, टाइम कम है।"),
    (VICTIM, "Resigned and nervous, giving in. Very slow, reading the digits one by one.",
     "<sigh> अच्छा ठीक है... चार... सात... एक..."),
]


def to_wav(pcm: bytes, mime_type: str) -> bytes:
    """Wrap raw PCM (e.g. audio/L16;rate=24000) in a WAV header."""
    bits, rate = 16, 24000
    for p in mime_type.split(";"):
        p = p.strip()
        if p.lower().startswith("rate="):
            rate = int(p.split("=", 1)[1])
        elif p.startswith("audio/L"):
            bits = int(p.split("L", 1)[1])
    block = bits // 8
    header = struct.pack("<4sI4s4sIHHIIHH4sI", b"RIFF", 36 + len(pcm), b"WAVE", b"fmt ", 16, 1, 1,
                         rate, rate * block, block, bits, b"data", len(pcm))
    return header + pcm


def main():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    if hasattr(types, "SpeechMetadata"):
        # Newer SDK: a separate style for every line
        parts = [
            types.Part(text=text, speech_metadata=types.SpeechMetadata(speaker=spk, style=f"Style: {style}"))
            for spk, style, text in LINES
        ]
    else:
        # Older SDK: put all directions in one prompt, then the transcript
        directions = "\n".join(f"Line {i}, {spk}: {style}" for i, (spk, style, _) in enumerate(LINES, 1))
        transcript = "\n".join(f"{spk}: {text}" for spk, _, text in LINES)
        prompt = (
            "Generate a realistic, unscripted-sounding Hindi phone call recorded in a living room. "
            f"{CALLER} is Rahul, a young man posing as a bank fraud officer. "
            f"{VICTIM} is Mrs Sharma, an older woman around 65.\n"
            "Follow these directions for each line (do not read them aloud):\n"
            f"{directions}\n\nTranscript:\n{transcript}"
        )
        parts = [types.Part(text=prompt)]

    def voice(speaker, name):
        return types.SpeakerVoiceConfig(
            speaker=speaker,
            voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=name)),
        )

    config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[voice(CALLER, CALLER_VOICE), voice(VICTIM, VICTIM_VOICE)],
            ),
        ),
    )

    audio, mime = bytearray(), ""
    for chunk in client.models.generate_content_stream(
        model=MODEL, contents=[types.Content(role="user", parts=parts)], config=config
    ):
        if chunk.parts and chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
            audio.extend(chunk.parts[0].inline_data.data)
            mime = chunk.parts[0].inline_data.mime_type

    if not audio:
        raise SystemExit("No audio returned. Check the model name and your GEMINI_API_KEY.")

    data = bytes(audio)
    if mimetypes.guess_extension(mime) != ".wav":
        data = to_wav(data, mime)
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "wb") as f:
        f.write(data)
    print(f"Saved {OUTPUT} ({mime})")

if __name__ == "__main__":
    main()