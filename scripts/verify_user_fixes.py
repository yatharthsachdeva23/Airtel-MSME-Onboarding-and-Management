import os
import sys
import time
import subprocess
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("Starting background server on port 8098...")
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.app:app", "--host", "127.0.0.1", "--port", "8098"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3.5)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            # 1. Desktop / Laptop View (1280x800)
            context = browser.new_context(viewport={"width": 1280, "height": 800})
            page = context.new_page()
            page.goto("http://127.0.0.1:8098", wait_until="networkidle")
            page.wait_for_timeout(2000)

            # Ensure website view
            page.click("#btnViewWebsite")
            page.wait_for_timeout(500)

            # Check 1: Chat greeting
            greeting_text = page.inner_text("#mobileChatMessages")
            print("Chat greeting contains 'quick 2-minute chat':", "quick 2-minute chat" in greeting_text)

            # Check 2: Plan & Price initial state
            page.click("#deskTabPlan")
            page.wait_for_timeout(500)
            empty_state_visible = page.is_visible("#planEmptyState")
            print("Plan Empty State Visible at start:", empty_state_visible)
            page.screenshot(path="artifacts/desktop_starting_quote_state.png")

            # Check 3: Smart KYC Dual Buttons on Desktop (Upload should be primary red, Camera secondary)
            page.click("#deskTabKyc")
            page.wait_for_timeout(1000)
            upload_btn = page.query_selector(".kyc-toolbar-actions .btn-style-upload")
            camera_btn = page.query_selector(".kyc-toolbar-actions .btn-style-camera")
            print("Smart KYC Dual Buttons on Desktop present:", upload_btn is not None and camera_btn is not None)
            page.screenshot(path="artifacts/desktop_smart_kyc_dual_buttons.png")

            # Check 4: Mobile App View Dual Buttons (Camera should be primary red, Upload secondary)
            page.click("#btnViewApp")
            page.wait_for_timeout(1000)
            page.evaluate("() => { switchMobileTab('tabQuote'); switchBundleSubTab('kyc'); }")
            page.wait_for_timeout(1000)
            page.screenshot(path="artifacts/mobile_smart_kyc_dual_buttons.png")

            # Switch back to Website mode to test conversational flow & cart sync
            page.evaluate("() => setDeviceViewMode('website')")
            page.wait_for_timeout(1000)
            page.evaluate("() => switchDesktopWorkspace('plan')")

            # Conversational step 1: Send Logistics & Fleet
            page.fill("#mobileChatInput", "Logistics & Fleet")
            page.click(".mobile-send-btn")
            page.wait_for_timeout(3500)

            # Step 2: Send size
            page.fill("#mobileChatInput", "12 fleet staff, 3 hubs")
            page.click(".mobile-send-btn")
            page.wait_for_timeout(3500)

            # Test Question: What about cloud cctv?
            print("Asking query: 'what about cloud cctv?'...")
            current_bubble_count = page.evaluate("() => document.querySelectorAll('.chat-bubble.advisor').length")
            page.fill("#mobileChatInput", "what about cloud cctv?")
            page.click(".mobile-send-btn")
            page.wait_for_function(f"() => document.querySelectorAll('.chat-bubble.advisor').length > {current_bubble_count}", timeout=15000)
            page.wait_for_timeout(1000)

            last_chat_msg = page.evaluate("() => { const bubbles = document.querySelectorAll('.chat-bubble.advisor'); return bubbles[bubbles.length - 1].innerText; }")
            print("Last chat msg preview:\n", last_chat_msg[-300:])
            no_rep = ("Understood. What is your current internet setup" not in last_chat_msg)
            print("Query answer doesn't have repeated 'Understood. What is your current internet setup':", no_rep)
            page.screenshot(path="artifacts/chat_query_no_repeated_question.png")

            # Step 3: Send needs
            page.fill("#mobileChatInput", "Dedicated Fiber with 99.5% SLA guarantee")
            page.click(".mobile-send-btn")
            page.wait_for_timeout(3500)

            # Step 4: GST
            page.fill("#mobileChatInput", "Yes, I have an active GST number")
            page.click(".mobile-send-btn")
            page.wait_for_timeout(4500)

            # Verify bundle appears in Plan & Price zone
            page.evaluate("() => switchDesktopWorkspace('plan')")
            page.wait_for_timeout(1000)
            subtotal_before = page.inner_text("#mobileSubtotal")
            net_before = page.inner_text("#mobileNetTotal")
            print(f"Configured Bundle Initial: Subtotal = {subtotal_before}, Net = {net_before}")
            page.screenshot(path="artifacts/cart_initial_configured.png")

            # Now test customization: Can i add more things in it like upi?
            print("Sending customization query: 'can i add more things in it like upi'...")
            curr_count = page.evaluate("() => document.querySelectorAll('.chat-bubble.advisor').length")
            page.fill("#mobileChatInput", "can i add more things in it like upi")
            page.click(".mobile-send-btn")
            page.wait_for_function(f"() => document.querySelectorAll('.chat-bubble.advisor').length > {curr_count}", timeout=15000)
            page.wait_for_timeout(1500)

            page.evaluate("() => switchDesktopWorkspace('plan')")
            page.wait_for_timeout(1000)
            subtotal_after = page.inner_text("#mobileSubtotal")
            net_after = page.inner_text("#mobileNetTotal")
            print(f"Configured Bundle Updated: Subtotal = {subtotal_after}, Net = {net_after}")
            page.screenshot(path="artifacts/cart_updated_with_upi.png")

            browser.close()

            # Copy screenshots to brain directory
            brain_dir = r"C:\Users\DELL\.gemini\antigravity\brain\189eb77b-9b1f-4f68-b2ff-1682279e819c"
            import shutil
            for name in [
                "desktop_starting_quote_state.png",
                "desktop_smart_kyc_dual_buttons.png",
                "mobile_smart_kyc_dual_buttons.png",
                "chat_query_no_repeated_question.png",
                "cart_initial_configured.png",
                "cart_updated_with_upi.png"
            ]:
                src = os.path.join("artifacts", name)
                if os.path.exists(src):
                    shutil.copyfile(src, os.path.join(brain_dir, name))
                    print(f"Copied {name} to brain dir.")
    finally:
        server_proc.terminate()
        print("Server stopped.")

if __name__ == "__main__":
    main()
