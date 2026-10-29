import os, requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("MODEL_API_KEY")
print("Key loaded:", bool(key))

r = requests.post(
    "https://api.meta.ai/v1/responses",
    headers={"Authorization": f"Bearer {key}"},
    json={
        "model": "muse-spark-1.3",
        "input": [{"role": "user", "content": "Reply with exactly: Sentinel online"}],
        "max_output_tokens": 500,
        "reasoning": {"effort": "low"},
    },
    timeout=60,
)
data = r.json()
print("HTTP:", r.status_code)
if data.get("error"): print("Error:", data["error"])
print("Status:", data.get("status"))
for item in data.get("output", []):
    if item.get("type") == "message":
        for c in item.get("content", []):
            print("Reply:", c.get("text"))