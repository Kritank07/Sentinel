import json
from sentinel.engine import analyze_image

v = analyze_image("samples/fake_kyc_sms.png", user_language="English")
with open("samples/output_image.json", "w", encoding="utf-8") as f:
    json.dump(v, f, indent=2, ensure_ascii=False)
print(v["verdict"], v["threat_score"], v["scam_type"])