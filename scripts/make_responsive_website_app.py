import os
import re

def update_html():
    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update CSS styles for Laptop Website vs Mobile App
    css_insert = """
    /* ==========================================================================
       RESPONSIVE MULTI-DEVICE ARCHITECTURE (LAPTOP WEBSITE VS MOBILE APP)
       ========================================================================== */
    
    /* Device Mode Switcher (Visible on Laptop / Desktop Screen) */
    .device-mode-switcher {
      display: none;
      align-items: center;
      background: #F1F5F9;
      border: 1px solid var(--border-color);
      border-radius: 20px;
      padding: 2px;
      gap: 2px;
    }
    .view-mode-pill {
      background: transparent;
      border: none;
      padding: 4px 10px;
      border-radius: 16px;
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s ease;
    }
    .view-mode-pill.active {
      background: white;
      color: var(--airtel-red);
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Main Dual Layout Container */
    .app-dual-layout {
      display: flex;
      flex: 1;
      min-height: 0;
      width: 100%;
      position: relative;
      overflow: hidden;
    }

    /* Left Column (Chat Stream) */
    .app-chat-column {
      height: 100%;
      min-height: 0;
      display: flex;
      flex-direction: column;
      position: relative;
      background: white;
      overflow: hidden;
    }

    /* Right Column (Enterprise Workspace) */
    .app-workspace-column {
      height: 100%;
      min-height: 0;
      display: flex;
      flex-direction: column;
      background: var(--bg-mobile);
      overflow: hidden;
    }

    .desktop-workspace-nav {
      display: none;
      background: white;
      border-bottom: 1px solid var(--border-color);
      padding: 10px 18px;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      gap: 12px;
    }
    .workspace-nav-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13.5px;
      font-weight: 800;
      color: var(--airtel-dark);
      white-space: nowrap;
    }
    .desktop-workspace-tabs {
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }
    .desk-tab-btn {
      background: #F8FAFC;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 6px 12px;
      font-size: 11.5px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
      white-space: nowrap;
    }
    .desk-tab-btn:hover {
      background: #F1F5F9;
      color: var(--airtel-dark);
    }
    .desk-tab-btn.active {
      background: var(--airtel-red-soft);
      border-color: #FECDD3;
      color: var(--airtel-red);
      font-weight: 800;
    }
    .desk-tab-btn.active i {
      color: var(--airtel-red);
    }

    .desktop-workspace-content {
      flex: 1;
      min-height: 0;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      overflow-x: hidden;
      width: 100%;
    }

    /* ==========================================================================
       MEDIA QUERY 1: LAPTOP & DESKTOP SCREEN (min-width: 900px) -> WEBSITE MODE
       ========================================================================== */
    @media (min-width: 900px) {
      body {
        background: #0F172A;
        background-image: radial-gradient(circle at 10% 20%, rgba(228, 0, 0, 0.08) 0%, transparent 40%),
                          radial-gradient(circle at 90% 80%, rgba(37, 99, 235, 0.08) 0%, transparent 40%);
        padding: 24px;
        align-items: center;
        justify-content: center;
      }

      .mobile-app-shell:not(.force-mobile-view) {
        max-width: 1380px;
        width: 100%;
        height: 94vh;
        max-height: 94vh;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.35);
        background: var(--bg-mobile);
      }

      .mobile-app-shell:not(.force-mobile-view) .device-mode-switcher {
        display: flex;
      }

      .mobile-app-shell:not(.force-mobile-view) .mobile-header {
        padding: 12px 20px;
      }
      .mobile-app-shell:not(.force-mobile-view) .mobile-title {
        font-size: 15px;
      }

      /* Desktop Dual Pane */
      .mobile-app-shell:not(.force-mobile-view) .app-dual-layout {
        display: flex;
        flex-direction: row;
      }

      .mobile-app-shell:not(.force-mobile-view) .app-chat-column {
        width: 440px;
        min-width: 400px;
        max-width: 480px;
        height: 100%;
        display: flex !important;
        flex-direction: column;
        border-right: 1px solid var(--border-color);
      }

      .mobile-app-shell:not(.force-mobile-view) .app-workspace-column {
        flex: 1;
        min-width: 0;
        height: 100%;
        display: flex !important;
        flex-direction: column;
      }

      .mobile-app-shell:not(.force-mobile-view) .desktop-workspace-nav {
        display: flex;
      }

      /* Hide Mobile Bottom Nav in Desktop Website View */
      .mobile-app-shell:not(.force-mobile-view) .mobile-bottom-nav {
        display: none !important;
      }
    }

    /* ==========================================================================
       MEDIA QUERY 2: PHONE / MOBILE SCREEN (max-width: 899px) -> NATIVE APP MODE
       ========================================================================== */
    @media (max-width: 899px) {
      body {
        background: var(--bg-mobile);
        padding: 0;
      }
      .mobile-app-shell {
        max-width: 100%;
        width: 100%;
        height: var(--app-height, 100dvh);
        max-height: var(--app-height, 100dvh);
        border-radius: 0;
        border: none;
        box-shadow: none;
      }

      .device-mode-switcher {
        display: none !important;
      }

      .app-dual-layout {
        display: flex;
        flex-direction: column;
        flex: 1;
        min-height: 0;
        overflow: hidden;
      }

      /* Mobile App: Only show active panel */
      .app-chat-column {
        display: none;
        width: 100%;
        flex: 1;
      }
      .app-chat-column.mobile-active {
        display: flex !important;
      }

      .app-workspace-column {
        display: none;
        width: 100%;
        flex: 1;
      }
      .app-workspace-column.mobile-active {
        display: flex !important;
      }

      .desktop-workspace-nav {
        display: none !important;
      }

      .mobile-bottom-nav {
        display: flex !important;
      }
    }

    /* When Force Mobile View is Active on Desktop (Simulating phone) */
    .mobile-app-shell.force-mobile-view {
      max-width: 440px !important;
      width: 440px !important;
      height: 90vh !important;
      max-height: 90vh !important;
      border-radius: 28px !important;
      box-shadow: 0 0 0 10px #1E293B, 0 25px 60px rgba(0,0,0,0.4) !important;
    }
    .mobile-app-shell.force-mobile-view .desktop-workspace-nav {
      display: none !important;
    }
    .mobile-app-shell.force-mobile-view .app-dual-layout {
      display: flex;
      flex-direction: column;
    }
    .mobile-app-shell.force-mobile-view .app-chat-column {
      display: none;
      width: 100%;
    }
    .mobile-app-shell.force-mobile-view .app-chat-column.mobile-active {
      display: flex !important;
    }
    .mobile-app-shell.force-mobile-view .app-workspace-column {
      display: none;
      width: 100%;
    }
    .mobile-app-shell.force-mobile-view .app-workspace-column.mobile-active {
      display: flex !important;
    }
    .mobile-app-shell.force-mobile-view .mobile-bottom-nav {
      display: flex !important;
    }
    """

    # Insert CSS into <style> before </style>
    if "/* ==========================================================================\n       RESPONSIVE MULTI-DEVICE ARCHITECTURE" not in html:
        html = html.replace("</style>", css_insert + "\n  </style>")

    # 2. Add Device Mode Switcher in Header
    mode_switcher_html = """
        <!-- Device Mode Switcher (Visible on Laptop / Desktop) -->
        <div class="device-mode-switcher">
          <button id="btnViewWebsite" class="view-mode-pill active" onclick="setDeviceViewMode('website')" title="Laptop / Enterprise Website View">
            <i class="fa-solid fa-laptop"></i> Website
          </button>
          <button id="btnViewApp" class="view-mode-pill" onclick="setDeviceViewMode('app')" title="Mobile Phone App View">
            <i class="fa-solid fa-mobile-screen"></i> Mobile App
          </button>
        </div>
"""
    if 'id="btnViewWebsite"' not in html:
        html = html.replace('<div class="header-actions">', '<div class="header-actions">\n' + mode_switcher_html)

    # 3. Restructure Main Content into Dual Layout
    # Find start of tabChat and end of tabTrack
    chat_start = html.find('<!-- ---------------- TAB 1: CONVERSATIONAL STREAM ---------------- -->')
    track_end = html.find('<!-- Fixed Bottom App Navigation Bar')

    if chat_start != -1 and track_end != -1 and 'class="app-dual-layout"' not in html:
        # Extract tabChat
        quote_start = html.find('<!-- ---------------- TAB 2: CART & DETERMINISTIC QUOTE')
        tab_chat_content = html[chat_start:quote_start].strip()

        # Extract workspace content (tabQuote + tabTrack)
        workspace_content = html[quote_start:track_end].strip()

        # New Dual-Layout HTML
        dual_layout_html = f"""
    <!-- Main Dual Layout Container: On Laptop displays Side-by-Side (Website); On Phone displays Tab-by-Tab (App) -->
    <div class="app-dual-layout">
      
      <!-- Left Column: Conversational AI Advisor (Always visible on Desktop; Toggled on Mobile) -->
      <div class="app-chat-column mobile-active" id="appChatColumn">
        {tab_chat_content}
      </div>

      <!-- Right Column: Enterprise Workspace Dashboard (Visible on Desktop; Toggled on Mobile) -->
      <div class="app-workspace-column" id="appWorkspaceColumn">
        
        <!-- Desktop Workspace Navigation Bar (Visible on Laptop / Desktop Screen) -->
        <div class="desktop-workspace-nav">
          <div class="workspace-nav-title">
            <i class="fa-solid fa-layer-group" style="color: var(--airtel-red);"></i>
            <span>Enterprise Workspace</span>
          </div>
          <div class="desktop-workspace-tabs">
            <button class="desk-tab-btn active" id="deskTabPlan" onclick="switchDesktopWorkspace('plan', this)">
              <i class="fa-solid fa-cart-shopping"></i> Plan &amp; Price
            </button>
            <button class="desk-tab-btn" id="deskTabKyc" onclick="switchDesktopWorkspace('kyc', this)">
              <i class="fa-solid fa-file-shield"></i> Smart KYC
            </button>
            <button class="desk-tab-btn" id="deskTabFeas" onclick="switchDesktopWorkspace('feas', this)">
              <i class="fa-solid fa-tower-broadcast"></i> GIS Network
            </button>
            <button class="desk-tab-btn" id="deskTabTrack" onclick="switchDesktopWorkspace('track', this)">
              <i class="fa-solid fa-truck-fast"></i> SLA Tracker
            </button>
            <button class="desk-tab-btn" id="deskTabPartner" onclick="openPartnerModal()">
              <i class="fa-solid fa-headset" style="color: #059669;"></i> Partner Desk
            </button>
          </div>
        </div>

        <!-- Desktop Workspace Content Area -->
        <div class="desktop-workspace-content">
          {workspace_content}
        </div>

      </div>

    </div>
"""
        html = html[:chat_start] + dual_layout_html + "\n    " + html[track_end:]

    # 4. Update switchMobileTab and add responsive helper functions in JS
    js_update = """
    /* ---------------- RESPONSIVE MULTI-DEVICE CONTROLLER (LAPTOP VS PHONE) ---------------- */
    function setDeviceViewMode(mode) {
      const shell = document.querySelector('.mobile-app-shell');
      const btnWeb = document.getElementById('btnViewWebsite');
      const btnApp = document.getElementById('btnViewApp');
      if (mode === 'app') {
        shell.classList.add('force-mobile-view');
        btnApp?.classList.add('active');
        btnWeb?.classList.remove('active');
      } else {
        shell.classList.remove('force-mobile-view');
        btnWeb?.classList.add('active');
        btnApp?.classList.remove('active');
      }
    }

    function switchDesktopWorkspace(target, btn) {
      document.querySelectorAll('.desk-tab-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');

      if (target === 'plan') {
        showWorkspaceTab('tabQuote');
        switchBundleSubTab('plan', document.getElementById('subtab_plan'));
      } else if (target === 'kyc') {
        showWorkspaceTab('tabQuote');
        switchBundleSubTab('kyc', document.getElementById('subtab_kyc'));
      } else if (target === 'feas') {
        showWorkspaceTab('tabQuote');
        switchBundleSubTab('feas', document.getElementById('subtab_feas'));
      } else if (target === 'track') {
        showWorkspaceTab('tabTrack');
      }
    }

    function showWorkspaceTab(tabId) {
      document.getElementById('tabQuote')?.classList.remove('active');
      document.getElementById('tabTrack')?.classList.remove('active');
      const target = document.getElementById(tabId);
      if (target) target.classList.add('active');
    }

    function switchMobileTab(tabId, el) {
      const chatCol = document.getElementById('appChatColumn');
      const workCol = document.getElementById('appWorkspaceColumn');
      
      document.querySelectorAll('.nav-tab-item').forEach(btn => btn.classList.remove('active'));
      if (el) {
        el.classList.add('active');
      } else {
        if (tabId === 'tabQuote') document.getElementById('navTabQuote')?.classList.add('active');
        if (tabId === 'tabChat') document.getElementById('navTabChat')?.classList.add('active');
        if (tabId === 'tabTrack') document.getElementById('navTabTrack')?.classList.add('active');
      }

      if (tabId === 'tabChat') {
        chatCol?.classList.add('mobile-active');
        workCol?.classList.remove('mobile-active');
      } else {
        chatCol?.classList.remove('mobile-active');
        workCol?.classList.add('mobile-active');
        showWorkspaceTab(tabId);
      }
    }
"""

    # Replace existing switchMobileTab implementation
    old_switch_pattern = re.compile(r'function switchMobileTab\(tabId, el\)\s*\{[^}]*\}', re.DOTALL)
    if 'setDeviceViewMode' not in html:
        html = old_switch_pattern.sub(js_update, html)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully upgraded frontend/index.html to responsive Laptop Website + Phone App architecture!")

if __name__ == "__main__":
    update_html()
