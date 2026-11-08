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
        # 1. Desktop 1440x900 viewport
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto("http://127.0.0.1:8099", wait_until="networkidle")
        page.wait_for_timeout(1000)

        # Verify right column is not blank: check #bundleItemsContainer or #subview_plan
        plan_visible = page.locator("#subview_plan").is_visible()
        quote_visible = page.locator("#tabQuote").is_visible()
        print(f"Desktop: plan_visible={plan_visible}, quote_visible={quote_visible}")

        # Capture Desktop Fullscreen Website screenshot
        screenshot_path = "artifacts/desktop_fullscreen_verified.png"
        os.makedirs("artifacts", exist_ok=True)
        page.screenshot(path=screenshot_path)
        print("Screenshot saved to", screenshot_path)

        brain_path = r"C:\Users\DELL\.gemini\antigravity\brain\189eb77b-9b1f-4f68-b2ff-1682279e819c\desktop_fullscreen_verified.png"
        shutil.copyfile(screenshot_path, brain_path)
        print("Copied to", brain_path)

        # Test clicking Smart KYC tab in workspace
        page.click("#deskTabKyc")
        page.wait_for_timeout(500)
        kyc_visible = page.locator("#subview_kyc").is_visible()
        print(f"After clicking KYC tab: kyc_visible={kyc_visible}")

        # Test clicking GIS Network tab in workspace
        page.click("#deskTabFeas")
        page.wait_for_timeout(500)
        feas_visible = page.locator("#subview_feas").is_visible()
        print(f"After clicking Feas tab: feas_visible={feas_visible}")

        # Test clicking SLA Tracker tab in workspace
        page.click("#deskTabTrack")
        page.wait_for_timeout(500)
        track_visible = page.locator("#tabTrack").is_visible()
        print(f"After clicking Track tab: track_visible={track_visible}")

        # Test switching back to Plan
        page.click("#deskTabPlan")
        page.wait_for_timeout(500)

        # Test clicking Mobile App toggle
        page.click("#btnViewApp")
        page.wait_for_timeout(800)
        mobile_preview_path = "artifacts/mobile_simulated_verified.png"
        page.screenshot(path=mobile_preview_path)
        brain_mobile_path = r"C:\Users\DELL\.gemini\antigravity\brain\189eb77b-9b1f-4f68-b2ff-1682279e819c\mobile_simulated_verified.png"
        shutil.copyfile(mobile_preview_path, brain_mobile_path)
        print("Mobile simulated view screenshot saved.")

        browser.close()
finally:
    proc.terminate()
    proc.wait()
    print("Server stopped.")
