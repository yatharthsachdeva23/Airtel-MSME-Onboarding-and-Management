import uvicorn
import os
import sys

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", 8080))
    print(f"================================================================")
    print(f"   PROJECT UDYAM DIGITAL - AIRTEL ENTERPRISE HACKATHON 2026")
    print(f"   Local PC URL:   http://127.0.0.1:{port}")
    print(f"   Phone URL:      http://192.168.1.7:{port}")
    print(f"   API Docs:       http://127.0.0.1:{port}/docs")
    print(f"================================================================")
    uvicorn.run("backend.app:app", host="0.0.0.0", port=port, reload=False)
