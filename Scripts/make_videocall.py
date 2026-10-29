import os, base64, requests
from dotenv import load_dotenv

load_dotenv()
PROMPT = ("A smartphone video call screenshot. A fictional middle-aged man in a dark blue "
          "uniform with a badge sits at a desk in an office with a flag behind him. "
          "Video call app interface with end-call button. Realistic, photographic.")

r = requests.post(
    "https://api.meta.ai/v1/responses",
    headers={"Authorization": f"Bearer {os.getenv('MODEL_API_KEY')}"},
    json={
        "model": "muse-image-1.0",
        "input": [{"type": "message", "role": "user",
                   "content": [{"type": "input_text", "text": PROMPT}]}],
        "max_output_tokens": 2048, "store": True, "stream": False,
        "temperature": 0.6, "top_p": 0.9,
        "tools": [{"type": "image_generation", "output_format": "png",
                   "reasoning_strength": "high", "enable_image_search": False,
                   "enable_shell": False, "enable_web_search": False}],
    },
    timeout=300,
)
if r.status_code != 200:
    print(r.status_code, r.text[:500])
    raise SystemExit
for item in r.json().get("output", []):
    if item.get("type") == "image_generation_call" and item.get("result"):
        open("samples/videocall.png", "wb").write(base64.b64decode(item["result"]))
        print("Saved samples/videocall.png")