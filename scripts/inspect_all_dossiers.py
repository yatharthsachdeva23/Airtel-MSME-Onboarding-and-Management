import os
import json
import re
import difflib
import pandas as pd

def main():
    cache_file = "data/kyc_ocr_cache.json"
    cache = json.load(open(cache_file, encoding="utf-8"))
    
    gst_df = pd.read_csv("udyam_digital_data/mock_gstin_registry.csv")
    udyam_df = pd.read_csv("udyam_digital_data/mock_udyam_registry.csv")
    
    gst_list = gst_df.to_dict('records')
    udyam_list = udyam_df.to_dict('records')
    
    for i in range(1, 13):
        app_id = f"K{i:02d}"
        print(f"\n=================== DOSSIER {app_id} ===================")
        gst_txt = cache.get(f"{app_id}_gst_certificate.png", "")
        udyam_txt = cache.get(f"{app_id}_udyam_certificate.png", "")
        addr_txt = cache.get(f"{app_id}_address_proof.png", "")
        sig_txt = cache.get(f"{app_id}_signatory_id.png", "")
        
        # Find business name mentioned
        trade_name = None
        m = re.search(r'Trade name\s*(?:onstitution\s*)?(.*?)(?:\s+(?:Proprietorship|Partnership|Limited|Private|LLP))', gst_txt, re.IGNORECASE)
        if m:
            trade_name = m.group(1).strip()
        else:
            m2 = re.search(r'Billed to\s*(.*?)(?:\s+Supply address)', addr_txt, re.IGNORECASE)
            if m2:
                trade_name = m2.group(1).strip()
        
        print(f"Extracted Trade Name: {trade_name}")
        
        # Match in GST registry
        matching_gst = []
        if trade_name:
            matching_gst = [r for r in gst_list if trade_name.lower() in str(r.get('trade_name', '')).lower() or trade_name.lower() in str(r.get('legal_name', '')).lower()]
        print(f"Matching GST records count: {len(matching_gst)}")
        if matching_gst:
            g = matching_gst[0]
            print(f"  GSTIN: {g['gstin']} | Legal: {g['legal_name']} | Status: {g['status']} | State: {g['state']}")
            
        # Match in Udyam registry
        matching_udyam = []
        if trade_name:
            matching_udyam = [r for r in udyam_list if trade_name.lower() in str(r.get('enterprise_name', '')).lower()]
        print(f"Matching Udyam records count: {len(matching_udyam)}")
        if matching_udyam:
            u = matching_udyam[0]
            print(f"  Udyam: {u['udyam_number']} | Name: {u['enterprise_name']} | Type: {u['enterprise_type']} | Date: {u['date_of_registration']}")
            
        # Address proof date
        dates = re.findall(r'\b(20[2-9][0-9]-[0-9]{2}-[0-9]{2})\b', addr_txt)
        print(f"  Address proof dates found: {dates}")
        
        # Signatory name in sig_txt
        m_sig = re.search(r'Name\s+([A-Za-z\s]+?)\s+Designation', sig_txt)
        sig_name = m_sig.group(1).strip() if m_sig else "Unknown"
        print(f"  Signatory ID Name: {sig_name}")

if __name__ == "__main__":
    main()
