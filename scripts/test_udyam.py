import json
import re
import pandas as pd

cache = json.load(open("data/kyc_ocr_cache.json", encoding="utf-8"))
udyam_df = pd.read_csv("udyam_digital_data/mock_udyam_registry.csv")

for i in range(1, 13):
    app_id = f"K{i:02d}"
    txt = cache.get(f"{app_id}_udyam_certificate.png", "")
    print(f"=== {app_id} Udyam ===")
    lines = [l.strip() for l in txt.split("\n") if l.strip()]
    for l in lines:
        if "UDYAM" in l.upper() or any(st in l for st in ["Enterprise", "Registration", "activity"]):
            print("  ", l)
