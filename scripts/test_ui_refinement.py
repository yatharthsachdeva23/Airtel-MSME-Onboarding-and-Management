import os
import sys
import time
import subprocess
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

def main():
    port = 8096
    print(f"Starting server on port {port}...")
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.app:app", "--host", "127.0.0.1", "--port", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(3.5)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            # ========================================================
            # 1. Real Mobile Phone Screen (390 x 844 - iPhone / Android)
            # ========================================================
            print("\n[Test 1] Testing Mobile Screen (390 x 844)...")
            context = browser.new_context(viewport={"width": 390, "height": 844})
            page = context.new_page()
            page.goto(f"http://127.0.0.1:{port}", wait_until="networkidle")
            page.wait_for_timeout(1500)

            os.makedirs("artifacts", exist_ok=True)
            page.screenshot(path="artifacts/mobile_main_screen_refined.png")
            print("  ✓ Captured mobile main screen: artifacts/mobile_main_screen_refined.png")

            # Verify that only ONE Common Space button exists in header and no green headset button
            headset_btns = page.locator(".header-actions i.fa-headset").count()
            print("  Headset buttons in mobile header:", headset_btns, "(Expected: 0)")
            assert headset_btns == 0, "No separate backend headset button should exist in mobile header!"

            dev_ops_btn = page.locator("#headerDevOpsBtn")
            assert dev_ops_btn.is_visible(), "Unified Common Space button must be visible in mobile header!"

            # Open Common Space on Mobile
            print("  Opening Common Space Modal on Mobile...")
            dev_ops_btn.click()
            page.wait_for_timeout(1000)

            page.screenshot(path="artifacts/mobile_common_space_health.png")
            print("  ✓ Captured mobile common space: artifacts/mobile_common_space_health.png")

            # Check that tab pill buttons have clean styling and no squished wrapping
            tab_pills = page.locator(".dev-tab-pill")
            print("  Common Space Tab pills count:", tab_pills.count(), "(Expected: 5)")
            assert tab_pills.count() == 5, f"Expected 5 tab pills in Common Space, got {tab_pills.count()}"

            # Click through tabs
            print("  Switching to Partner & Back-Office tab in Common Space...")
            page.locator("#devTabBtnPartner").click()
            page.wait_for_timeout(1000)
            partner_view = page.locator("#devViewPartner")
            assert partner_view.is_visible(), "Partner & Back-Office view must be visible in Common Space!"
            page.screenshot(path="artifacts/mobile_common_space_partner.png")
            print("  ✓ Captured partner back-office tab in common space: artifacts/mobile_common_space_partner.png")

            # Close Common Space
            page.locator(".dev-modal-close-btn").click()
            page.wait_for_timeout(500)

            # ========================================================
            # 2. Desktop Laptop Screen (1280 x 800)
            # ========================================================
            print("\n[Test 2] Testing Desktop Laptop Screen (1280 x 800)...")
            desk_context = browser.new_context(viewport={"width": 1280, "height": 800})
            page_desk = desk_context.new_page()
            page_desk.goto(f"http://127.0.0.1:{port}", wait_until="networkidle")
            page_desk.wait_for_timeout(1500)

            page_desk.screenshot(path="artifacts/desktop_main_screen_refined.png")
            print("  ✓ Captured desktop main screen: artifacts/desktop_main_screen_refined.png")

            # Open Common Space on Desktop
            print("  Opening Common Space Modal on Desktop...")
            page_desk.locator("#headerDevOpsBtn").click()
            page_desk.wait_for_timeout(1000)
            page_desk.screenshot(path="artifacts/desktop_common_space_refined.png")
            print("  ✓ Captured desktop common space modal: artifacts/desktop_common_space_refined.png")

            browser.close()
            print("\nALL UI REFINEMENT TESTS COMPLETED SUCCESSFULLY!")

    finally:
        server_proc.terminate()
        server_proc.wait()

if __name__ == "__main__":
    main()
