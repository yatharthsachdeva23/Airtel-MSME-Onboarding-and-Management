import uvicorn
import os
import sys

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"================================================================")
    print(f"   PROJECT UDYAM DIGITAL - AIRTEL ENTERPRISE HACKATHON 2026")
    print(f"   Server running at: http://127.0.0.1:{port}")
    print(f"   API Documentation: http://127.0.0.1:{port}/docs")
    print(f"================================================================")
    uvicorn.run("backend.app:app", host="0.0.0.0", port=port, reload=False)
