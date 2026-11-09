import subprocess, time, sys, os
from playwright.sync_api import sync_playwright

proc = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'backend.app:app', '--host', '127.0.0.1', '--port', '8096'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(3)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True)
        page = context.new_page()
        page.goto('http://127.0.0.1:8096', wait_until='networkidle')
        page.wait_for_timeout(1000)
        
        # Screenshot initial phone
        page.screenshot(path='artifacts/mobile_initial.png')
        
        # Click My Bundle tab on bottom nav
        page.click('#navTabQuote')
        page.wait_for_timeout(1000)
        
        # Check computed styles of appChatColumn and appWorkspaceColumn
        chat_col_display = page.evaluate("() => window.getComputedStyle(document.getElementById('appChatColumn')).display")
        work_col_display = page.evaluate("() => window.getComputedStyle(document.getElementById('appWorkspaceColumn')).display")
        quote_tab_display = page.evaluate("() => window.getComputedStyle(document.getElementById('tabQuote')).display")
        
        print(f"After clicking My Bundle:")
        print(f"appChatColumn display: {chat_col_display}")
        print(f"appWorkspaceColumn display: {work_col_display}")
        print(f"tabQuote display: {quote_tab_display}")
        
        page.screenshot(path='artifacts/mobile_my_bundle_current.png')
        browser.close()
finally:
    proc.terminate()
