import os, json, base64, requests
from dotenv import load_dotenv
from sentinel.engine import upload_file

load_dotenv()
KEY = os.getenv("MODEL_API_KEY")

PROMPT = """Listen ONLY to the voice, not the meaning of the words.
Judge whether this voice is a real human or AI-generated / voice-cloned.
Listen for: robotic or overly smooth tone, unnatural pauses or rhythm, missing breaths,
flat or mismatched emotion, metallic artifacts, perfectly even volume.
Be calibrated: real phone or laptop recordings can sound flat or noisy and still be human.
Return ONLY JSON: {"synthetic_likelihood": 0-100, "verdict": "REAL" | "UNCERTAIN" | "AI_GENERATED",
"confidence": "low" | "medium" | "high", "signals": ["what you heard"]}"""


def audio_parts(path):
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    parts = {"input_audio (base64)": {"type": "input_audio",
                                      "input_audio": {"data": b64, "format": "wav"}}}
    try:
        fid = upload_file(path)
        parts["input_audio (file_id)"] = {"type": "input_audio", "file_id": fid}
        parts["input_file (file_id)"] = {"type": "input_file", "file_id": fid}
    except requests.HTTPError as e:
        print(f"  ✗ file upload rejected: {e.response.text[:300]}")
    return parts


def judge_voice(path):
    for name, part in audio_parts(path).items():
        r = requests.post(
            "https://api.meta.ai/v1/responses",
            headers={"Authorization": f"Bearer {KEY}"},
            json={
                "model": "muse-wonder-1.0",
                "input": [{"role": "user", "content": [{"type": "input_text", "text": PROMPT}, part]}],
                "max_output_tokens": 1500,
                "reasoning": {"effort": "medium"},
            },
            timeout=180,
        )
        if r.status_code != 200:
            print(f"  ✗ {name}: {r.status_code} {r.text[:200]}")
            continue
        print(f"  ✓ format that works: {name}")
        out = "".join(c.get("text", "") for i in r.json().get("output", [])
                      if i.get("type") == "message" for c in i.get("content", []))
        return json.loads(out.strip().removeprefix("```json").removesuffix("```").strip())


for f in ["samples/scam_call.wav", "samples/ai_voice.wav"]:
    print(f"\n🎧 {f}")
    print(json.dumps(judge_voice(f), indent=2))