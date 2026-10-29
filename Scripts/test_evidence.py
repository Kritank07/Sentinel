import json
from sentinel.engine import analyze_image
from sentinel.segment import evidence_boxes, highlight

for img in ["samples/fake_kyc_sms.png", "samples/videocall.png"]:
    v = analyze_image(img, user_language="English")
    print(f"\n🖼️ {img} → {v['verdict']} ({v['threat_score']})")
    print(json.dumps(v.get("suspicious_regions"), indent=2))
    boxes = evidence_boxes(img, v.get("suspicious_regions", []))
    out = img.replace(".png", "_evidence.png")
    highlight(img, boxes, out)
    print("Saved", out)