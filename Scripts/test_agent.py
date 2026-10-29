import json
from sentinel.engine import investigate

msg = ("Dear Customer, your SBI YONO account will be BLOCKED today. "
       "Update PAN/KYC immediately: http://sbi-kyc-verify.top/update "
       "or call our helpline 9876543210 - SBI Team")

v = investigate(msg, user_language="English")
with open("samples/output_agent.json", "w", encoding="utf-8") as f:
    json.dump(v, f, indent=2, ensure_ascii=False)
print("\n", v["verdict"], v["threat_score"])
print(json.dumps(v.get("tool_findings"), indent=2, ensure_ascii=False))