"""Gate DAST : fait échouer le pipeline si ZAP trouve des alertes
de risque >= MIN_RISK (3 = High, 2 = Medium). Défaut : 2."""
import json
import os
import sys

MIN_RISK = int(os.environ.get("MIN_RISK", "2"))
path = sys.argv[1] if len(sys.argv) > 1 else "zap-out/zap-report.json"

with open(path, encoding="utf-8") as f:
    report = json.load(f)

sites = report.get("site") or report.get("sites") or []
blocking = []
for site in sites:
    for alert in site.get("alerts", []):
        risk = int(alert.get("riskcode", 0))
        print(f"[risque {risk}] {alert.get('name')}")
        if risk >= MIN_RISK:
            blocking.append(alert.get("name"))

if blocking:
    print(f"\nECHEC : {len(blocking)} alerte(s) de risque >= {MIN_RISK} :")
    for name in blocking:
        print(f" - {name}")
    sys.exit(1)
print("\nOK : aucune alerte bloquante.")
