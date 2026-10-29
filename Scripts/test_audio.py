import os, json, requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("MODEL_API_KEY")

settings = {
    "model": "muse-voice-transcribe-1.0",
    "audioEncoding": "WAV",
    "mode": "DIARIZATION",
}

with open("samples/scam_call.wav", "rb") as f:
    r = requests.post(
        "https://api.meta.ai/v1/asr/transcribe",
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
        data={"request": json.dumps(settings)},
        files={"audio": ("scam_call.wav", f, "audio/wav")},
        timeout=120,
    )

print("HTTP:", r.status_code)
print(json.dumps(r.json(), indent=2, ensure_ascii=False)[:3000])