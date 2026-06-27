#!/usr/bin/env python3
from pathlib import Path
import json
ADDR = "0xA61a3B3a130a9c20768EEBF97E21515A6046a1fA"
required = ["public/agialpha-token-boundary.html","public/investment-token-boundary.html","docs/legal/AGIALPHA_TOKEN_PUBLIC_MARKET_BOUNDARY.md","docs/legal/NO_TOKEN_SALE_NO_USER_FUNDS.md","content/goalos/agialpha-token-boundary.json",".github/ISSUE_TEMPLATE/token_or_market_boundary.yml"]
errors=[]
for p in required:
    if not Path(p).exists(): errors.append(f"missing: {p}")
texts = "\n".join(Path(p).read_text(encoding="utf-8", errors="ignore") for p in required if Path(p).exists())
checks = {"address_present": ADDR in texts,"not_available_from_us": "not available from us" in texts.lower(),"no_token_sale": "no sale" in texts.lower() or "no token sale" in texts.lower(),"no_user_funds": "no user-fund authorization" in texts.lower() or "no user funds" in texts.lower(),"no_wallet_support": "wallet support" in texts.lower(),"third_party_responsibility": "third part" in texts.lower(),"no_investment_advice": "investment advice" in texts.lower()}
for k,v in checks.items():
    if not v: errors.append(f"failed check: {k}")
for forbidden in ["guaranteed profit", "risk-free", "price target", "buy now", "send funds to us"]:
    if forbidden in texts.lower(): errors.append(f"forbidden phrase: {forbidden}")
report={"status":"failed" if errors else "passed","generated_at":"2026-06-27T16:40:03Z","token_address":ADDR,"not_available_from_goalos":True,"no_token_sale":True,"no_user_funds":True,"no_wallet_support":True,"third_party_responsibility":True,"errors":errors,"checks":checks}
Path("reports").mkdir(exist_ok=True)
Path("reports/agialpha-token-boundary-qa.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
print(json.dumps(report, indent=2))
raise SystemExit(1 if errors else 0)
