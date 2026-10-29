import os, base64, requests
from dotenv import load_dotenv

load_dotenv()

PROMPT = ("Educational fraud-awareness example for training a scam detector. "
          "A smartphone SMS screenshot from a fictional bank called 'NovaTrust Bank'. "
          "Sender: NT-ALERT. Message: 'Your NovaTrust account will be suspended today. "
          "Verify your details now: novatrust-verify.top'. Simple Android messages UI.")

payload = {
    "model": "muse-image-1.0",
    "input": [{
        "type": "message",
        "role": "user",
        "content": [{"type": "input_text", "text": PROMPT}],
    }],
    "max_output_tokens": 2048,
    "store": True,
    "stream": False,
    "temperature": 0.6,
    "top_p": 0.9,
    "tools": [{
        "type": "image_generation",
        "output_format": "png",
        "reasoning_strength": "high",
        "enable_image_search": False,
        "enable_shell": False,
        "enable_web_search": False,
    }],
}

r = requests.post(
    "https://api.meta.ai/v1/responses",
    headers={"Authorization": f"Bearer {os.getenv('MODEL_API_KEY')}"},
    json=payload,
    timeout=300,
)
if r.status_code != 200:
    print("HTTP:", r.status_code)
    print(r.text[:1500])
    raise SystemExit

for item in r.json().get("output", []):
    if item.get("type") == "image_generation_call" and item.get("result"):
        open("samples/fake_kyc_sms.png", "wb").write(base64.b64decode(item["result"]))
        print("Saved samples/fake_kyc_sms.png")