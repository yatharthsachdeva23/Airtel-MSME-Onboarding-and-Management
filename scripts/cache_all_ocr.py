import os
import subprocess
import json
import glob

def run_ocr(image_path):
    ps_script = os.path.join(os.getcwd(), "backend", "run_ocr.ps1")
    cmd = [
        "powershell",
        "-ExecutionPolicy", "Bypass",
        "-File", ps_script,
        "-ImagePath", image_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return res.stdout.strip()

def main():
    docs_dir = os.path.join(os.getcwd(), "udyam_digital_data", "kyc_documents")
    cache_file = os.path.join(os.getcwd(), "data", "kyc_ocr_cache.json")
    os.makedirs(os.path.join(os.getcwd(), "data"), exist_ok=True)
    
    cache = {}
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except Exception:
            cache = {}
            
    png_files = sorted(glob.glob(os.path.join(docs_dir, "*.png")))
    print(f"Found {len(png_files)} KYC document images.")
    
    for i, p in enumerate(png_files):
        fname = os.path.basename(p)
        if fname in cache and cache[fname]:
            continue
        print(f"[{i+1}/{len(png_files)}] Running OCR on {fname}...")
        txt = run_ocr(p)
        cache[fname] = txt
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
            
    print(f"Finished caching OCR for {len(cache)} files.")

if __name__ == "__main__":
    main()
