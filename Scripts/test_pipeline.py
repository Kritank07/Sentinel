import json
from sentinel.asr import transcribe
from sentinel.engine import analyze_text

t = transcribe("samples/scam_call.wav")
print("Transcript:", t["transcript"])
verdict = analyze_text(t["transcript"], user_language = "tamil")
print(verdict["explanation"])
print(verdict["action"])
# print(json.dumps(verdict, indent=2, ensure_ascii=False))
with open("samples/output_tamil.json", "w", encoding="utf-8") as f:
    json.dump(verdict, f, indent=2, ensure_ascii=False)