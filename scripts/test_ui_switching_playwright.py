import subprocess
import time
import sys
import os
import shutil

sys.stdout.reconfigure(encoding='utf-8')

proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "backend.app:app", "--host", "127.0.0.1", "--port", "8099"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

time.sleep(2.5)

try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 412, "height": 915})
        page.goto("http://127.0.0.1:8099", wait_until="networkidle")

        # 1. Click Kirana Shop
        page.locator("#initialQuickChips .quick-chip").first.click()
        page.wait_for_timeout(1500)

        # 2. Send Clinic & Pharmacy
        page.evaluate("""() => {
            document.getElementById('mobileChatInput').value = 'Clinic & Pharmacy';
            sendMobileMessage();
        }""")
        page.wait_for_timeout(2000)

        # 3. Send Logistics & Fleet
        page.evaluate("""() => {
            document.getElementById('mobileChatInput').value = 'Logistics & Fleet';
            sendMobileMessage();
        }""")
        page.wait_for_timeout(2000)

        # Scroll to bottom
        page.evaluate("() => { const el = document.getElementById('mobileChatMessages'); if(el) el.scrollTop = el.scrollHeight; }")
        page.wait_for_timeout(600)

        screenshot_path = "artifacts/chat_switching_verified.png"
        os.makedirs("artifacts", exist_ok=True)
        page.screenshot(path=screenshot_path)
        print("Screenshot saved to", screenshot_path)

        brain_path = r"C:\Users\DELL\.gemini\antigravity\brain\189eb77b-9b1f-4f68-b2ff-1682279e819c\chat_switching_verified.png"
        shutil.copyfile(screenshot_path, brain_path)
        print("Copied to", brain_path)

        browser.close()
finally:
    proc.terminate()
    proc.wait()
    print("Server stopped.")
