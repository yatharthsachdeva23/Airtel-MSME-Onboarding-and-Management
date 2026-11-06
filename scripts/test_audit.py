import os
import sys
sys.path.insert(0, os.getcwd())
from backend.kyc_service import KYCService
import json

def test():
    svc = KYCService()
    for i in range(1, 13):
        app_id = f"K{i:02d}"
        res = svc.audit_applicant_dossier(app_id)
        status = res["overall_status"]
        flags = [f.get("error_code") for f in res["flags"]]
        print(f"=== {app_id}: {status} ===")
        if flags:
            for flag in res["flags"]:
                print(f"  [FLAG] {flag.get('error_code')}: {flag.get('message')}")
                print(f"         Mitigation: {flag.get('mitigation')}")
        else:
            print("  [OK] All uploaded documents passed verification against registries.")

if __name__ == "__main__":
    test()
