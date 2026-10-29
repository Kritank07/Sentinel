import os, json, requests
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("MODEL_API_KEY")

def transcribe(path: str, mode: str = "DIARIZATION") -> dict:
    settings = {"model": "muse-voice-transcribe-1.0", "audioEncoding": "WAV", "mode": mode}
    with open(path, "rb") as f:
        r = requests.post(
            "https://api.meta.ai/v1/asr/transcribe",
            headers={"Authorization": f"Bearer {KEY}", "Accept": "application/json"},
            data={"request": json.dumps(settings)},
            files={"audio": (os.path.basename(path), f, "audio/wav")},
            timeout=120,
        )
    r.raise_for_status()
    return r.json()