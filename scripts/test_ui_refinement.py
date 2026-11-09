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

            # Check that tab pill buttons have clean styling and strictly 3 operational tabs
            tab_pills = page.locator(".dev-tab-pill")
            print("  Common Space Tab pills count:", tab_pills.count(), "(Expected: 3)")
            assert tab_pills.count() == 3, f"Expected 3 tab pills in Common Space, got {tab_pills.count()}"

            # Verify Deliverables & Partner tabs are removed
            assert page.locator("#devTabBtnEvals").count() == 0, "Deliverables tab must be removed!"
            assert page.locator("#devTabBtnPartner").count() == 0, "Partner tab must be removed from Common Space!"

            # Click through Outbound Call Desk tab
            print("  Switching to Outbound Call Desk tab in Common Space...")
            page.locator("#devTabBtnOutbound").click()
            page.wait_for_timeout(1000)
            outbound_view = page.locator("#devViewOutbound")
            assert outbound_view.is_visible(), "Outbound Call Desk view must be visible in Common Space!"
            page.screenshot(path="artifacts/mobile_common_space_outbound.png")
            print("  ✓ Captured outbound call desk tab in common space: artifacts/mobile_common_space_outbound.png")

            # Close Common Space
            page.locator(".dev-modal-close-btn").click()
            page.wait_for_timeout(500)

            # ========================================================
            # 2. Desktop Laptop Screen (1280 x 800) & Smart KYC JSON Inspector
            # ========================================================
            print("\n[Test 2] Testing Desktop Laptop Screen & Smart KYC Structured JSON...")
            desk_context = browser.new_context(viewport={"width": 1280, "height": 800})
            page_desk = desk_context.new_page()
            page_desk.goto(f"http://127.0.0.1:{port}", wait_until="networkidle")
            page_desk.wait_for_timeout(1500)

            # Switch to Smart KYC tab
            page_desk.locator("#deskTabKyc").click()
            page_desk.wait_for_timeout(1200)

            # Check Structured JSON output toggle in Smart KYC
            json_btn = page_desk.locator("#kycInspectBtnJson")
            assert json_btn.is_visible(), "Structured JSON toggle button must be visible in Smart KYC workbench!"
            json_btn.click()
            page_desk.wait_for_timeout(500)
            json_output = page_desk.locator("#kycJsonOutput")
            assert json_output.is_visible(), "Structured JSON output pre element must be visible!"
            json_text = json_output.inner_text()
            assert '"applicant_id": "K02"' in json_text, "Structured JSON must contain valid applicant data!"
            print("  ✓ Verified Smart KYC Structured JSON output format!")

            page_desk.screenshot(path="artifacts/desktop_smart_kyc_structured_json.png")
            print("  ✓ Captured desktop smart kyc with structured json: artifacts/desktop_smart_kyc_structured_json.png")

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
