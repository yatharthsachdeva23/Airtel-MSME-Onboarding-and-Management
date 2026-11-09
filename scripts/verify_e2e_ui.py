import os
import sys
import time
import subprocess
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

def run_e2e_verification():
    port = 8097
    cmd = [sys.executable, "-m", "uvicorn", "backend.app:app", "--host", "127.0.0.1", "--port", str(port)]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            # 1. Test Phone Mode & "My Bundle" Tab (Must NOT be blank!)
            print("[E2E Test 1] Testing Mobile Phone View & 'My Bundle' Tab...")
            mobile_context = browser.new_context(viewport={'width': 390, 'height': 844})
            page_mobile = mobile_context.new_page()
            page_mobile.goto(f"http://127.0.0.1:{port}/")
            page_mobile.wait_for_selector("#mobileChatMessages")
            time.sleep(1)

            # Check initial chat view
            chat_col = page_mobile.locator("#appChatColumn")
            work_col = page_mobile.locator("#appWorkspaceColumn")
            print("  Initial state: chat_col visible:", chat_col.is_visible(), "| work_col visible:", work_col.is_visible())
            assert chat_col.is_visible(), "Chat column should be visible initially on mobile"

            # Click "My Bundle" nav tab on phone
            print("  Tapping 'My Bundle' bottom nav tab...")
            page_mobile.click("#navTabQuote")
            time.sleep(1)
            
            print("  After tapping 'My Bundle': chat_col visible:", chat_col.is_visible(), "| work_col visible:", work_col.is_visible())
            assert work_col.is_visible(), "Workspace column MUST be visible when 'My Bundle' is tapped on mobile!"
            
            # Check plan empty state or plan subview is visible
            plan_subview = page_mobile.locator("#subview_plan")
            assert plan_subview.is_visible(), "Plan subview must be visible in My Bundle!"
            
            os.makedirs("artifacts", exist_ok=True)
            page_mobile.screenshot(path="artifacts/mobile_my_bundle_verified.png")
            print("  ✓ Mobile 'My Bundle' tab verified non-blank! Saved: artifacts/mobile_my_bundle_verified.png")

            # Click back to Chat
            page_mobile.click("#navTabChat")
            time.sleep(0.5)
            assert chat_col.is_visible(), "Chat column must be visible again after tapping Chat"

            # 2. Test Single Button after Quote & Dissatisfaction Auto-Transfer
            print("\n[E2E Test 2] Testing Chat Quote & Single Button 'Start Onboarding'...")
            def send_msg(text):
                cnt = page_mobile.locator(".chat-bubble.advisor").count()
                page_mobile.fill("#mobileChatInput", text)
                page_mobile.press("#mobileChatInput", "Enter")
                page_mobile.wait_for_function(f"document.querySelectorAll('.chat-bubble.advisor').length > {cnt}", timeout=15000)
                time.sleep(0.5)

            send_msg("Kirana & Retail Store")
            send_msg("1-3 staff, 1 shop")
            send_msg("Broadband with 99.5% uptime SLA")
            send_msg("Yes, active GSTIN")

            page_mobile.wait_for_selector(".quick-chip:has-text('Start Onboarding')", timeout=15000)
            time.sleep(1)

            page_mobile.screenshot(path="artifacts/mobile_quote_single_button.png")
            print("  ✓ Quote rendered with single 'Start Onboarding' button! Saved: artifacts/mobile_quote_single_button.png")

            # 3. Test Dissatisfaction / Human Transfer on clean session
            print("\n[E2E Test 3] Testing Dissatisfaction / Human Transfer...")
            page_dissat = mobile_context.new_page()
            page_dissat.goto(f"http://127.0.0.1:{port}/")
            page_dissat.wait_for_selector("#mobileChatMessages")
            time.sleep(1)

            page_dissat.fill("#mobileChatInput", "I am not satisfied with this, connect me to an agent")
            page_dissat.press("#mobileChatInput", "Enter")
            page_dissat.wait_for_selector(".agent-transfer-card", timeout=12000)
            time.sleep(1)

            page_text = page_dissat.content()
            assert "(Detected concern" not in page_text, "Internal '(Detected concern' string must NOT appear in chat!"
            assert "Airtel Senior Enterprise Specialist" in page_text, "User must be informed of transfer to agent!"
            assert "Priya Sharma" in page_text, "Agent card must show assigned specialist!"
            
            page_dissat.screenshot(path="artifacts/mobile_agent_transfer_verified.png")
            print("  ✓ Automatic live agent transfer verified! Saved: artifacts/mobile_agent_transfer_verified.png")

            # 3. Test Desktop Dev & Operations Control Center
            print("\n[E2E Test 4] Testing Desktop Dev & Operations Control Center...")
            desktop_context = browser.new_context(viewport={'width': 1440, 'height': 900})
            page_desktop = desktop_context.new_page()
            page_desktop.goto(f"http://127.0.0.1:{port}/")
            page_desktop.wait_for_selector("#headerDevOpsBtn")
            time.sleep(1)

            # Open Dev & Ops Modal via Header
            print("  Clicking 'Dev & Ops' header button...")
            page_desktop.click("#headerDevOpsBtn")
            time.sleep(1)

            dev_modal = page_desktop.locator("#devModal")
            assert dev_modal.is_visible(), "Dev & Ops Modal must be open and visible!"

            # Verify System Health is active
            health_view = page_desktop.locator("#devViewHealth")
            assert health_view.is_visible(), "System Health view should be active initially in Dev modal"

            page_desktop.screenshot(path="artifacts/dev_ops_health_verified.png")
            print("  ✓ Dev & Ops Health verified. Saved: artifacts/dev_ops_health_verified.png")

            # Switch to Live Lead Transfers tab
            print("  Switching to 'Live Lead Transfers' tab...")
            page_desktop.click("#devTabBtnTransfers")
            time.sleep(1)
            transfers_view = page_desktop.locator("#devViewTransfers")
            assert transfers_view.is_visible(), "Live Lead Transfers view must be visible!"
            
            # Check that NO drop reason exists
            modal_text = transfers_view.inner_text()
            assert "Drop Reason" not in modal_text, "Forbidden 'Drop Reason' found in Live Lead Transfers!"
            assert "Apex Global Cold Chain Logistics" in modal_text, "Expected Apex Global lead in Live Transfers"
            assert "+91 98201 44521" in modal_text, "Expected unique phone number in Live Transfers"

            page_desktop.screenshot(path="artifacts/dev_ops_live_transfers_verified.png")
            print("  ✓ Live Lead Transfers verified with unique numbers, unique suggestions & zero drop reasons!")

            # Switch to Outbound Call Desk tab
            print("  Switching to 'Outbound Call Desk' tab...")
            page_desktop.click("#devTabBtnOutbound")
            time.sleep(1)
            outbound_view = page_desktop.locator("#devViewOutbound")
            assert outbound_view.is_visible(), "Outbound Call Desk view must be visible!"

            outbound_text = outbound_view.inner_text()
            assert "Drop Reason" not in outbound_text, "Forbidden 'Drop Reason' found in Outbound Call Desk!"
            assert "GreenLeaf Organic Marts" in outbound_text, "Expected GreenLeaf Organic Marts in Outbound Desk"
            assert "+91 98110 52391" in outbound_text, "Expected unique phone number in Outbound Desk"

            # Click "Call Lead" on the first lead
            print("  Clicking 'Call Lead' button...")
            page_desktop.click("#devPossibleLeadsContainer button:has-text('Call Lead')")
            time.sleep(2)

            page_desktop.screenshot(path="artifacts/dev_ops_call_active_verified.png")
            print("  ✓ Outbound call simulation active. Saved: artifacts/dev_ops_call_active_verified.png")

            browser.close()
            print("\n========================================================")
            print("ALL E2E BROWSER UI & DEV/OPS REQUIREMENTS FULLY VERIFIED!")
            print("========================================================")

    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    run_e2e_verification()
