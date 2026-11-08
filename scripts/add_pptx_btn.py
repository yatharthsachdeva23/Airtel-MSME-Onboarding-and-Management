import os

def add_pptx_button():
    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    old_btns = '''          <!-- 1-Click Deliverable Downloads: Brief, Slide Blueprint, DPDP 1-Page Note -->
          <div style="display: flex; gap: 6px; margin-bottom: 10px;">
            <button onclick="downloadExecutivePDF()" class="mobile-cta-btn" style="flex: 1; background: #1E293B; height: 38px; font-size: 10.5px; padding: 0 4px;">
              <i class="fa-solid fa-file-pdf" style="color: #EF4444;"></i> Exec Brief
            </button>
            <button onclick="downloadSlideDeckPDF()" class="mobile-cta-btn" style="flex: 1; background: var(--airtel-red); height: 38px; font-size: 10.5px; padding: 0 4px;">
              <i class="fa-solid fa-file-powerpoint" style="color: white;"></i> Blueprint
            </button>
            <button onclick="downloadSecurityPDF()" class="mobile-cta-btn" style="flex: 1; background: #059669; height: 38px; font-size: 10.5px; padding: 0 4px;">
              <i class="fa-solid fa-shield-halved" style="color: white;"></i> DPDP Note
            </button>
          </div>'''

    new_btns = '''          <!-- 1-Click Deliverable Downloads: Brief, PPTX, Slide Blueprint, DPDP 1-Page Note -->
          <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin-bottom: 10px;">
            <button onclick="downloadExecutivePDF()" class="mobile-cta-btn" style="background: #1E293B; height: 36px; font-size: 10.5px; padding: 0 4px;">
              <i class="fa-solid fa-file-pdf" style="color: #EF4444;"></i> Executive Brief
            </button>
            <button onclick="downloadPPTX()" class="mobile-cta-btn" style="background: var(--airtel-red); height: 36px; font-size: 10.5px; padding: 0 4px;">
              <i class="fa-solid fa-file-powerpoint" style="color: white;"></i> Official PPTX (10 Slides)
            </button>
            <button onclick="downloadSlideDeckPDF()" class="mobile-cta-btn" style="background: #334155; height: 36px; font-size: 10.5px; padding: 0 4px;">
              <i class="fa-solid fa-file-lines" style="color: #93C5FD;"></i> Slide Blueprint PDF
            </button>
            <button onclick="downloadSecurityPDF()" class="mobile-cta-btn" style="background: #059669; height: 36px; font-size: 10.5px; padding: 0 4px;">
              <i class="fa-solid fa-shield-halved" style="color: white;"></i> DPDP Note (1-Page)
            </button>
          </div>'''

    if 'downloadPPTX()' not in content:
        content = content.replace(old_btns, new_btns)
        js_pptx = '''
    function downloadPPTX() {
      window.open("/static/Project_Udyam_Digital_Presentation.pptx", "_blank");
    }
'''
        content = content.replace('function downloadSlideDeckPDF() {', js_pptx + '    function downloadSlideDeckPDF() {')

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated deliverable buttons in frontend/index.html")

if __name__ == "__main__":
    add_pptx_button()
