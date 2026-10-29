import json
from sentinel.asr import transcribe
from sentinel.engine import investigate

for f in ["samples/scam_call.wav", "samples/ai_voice.wav"]:
    t = transcribe(f)
    v = investigate(t["transcript"], user_language="English", audio_path=f)
    print(f"\n🎧 {f} → {v['verdict']} ({v['threat_score']})")
    print("   voice:", json.dumps(v.get("voice_analysis"), ensure_ascii=False))