import os

def update_frontend():
    html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add headset button in header
    headset_btn = '''        <!-- Partner & Sales Back-Office Desk: ICON BUTTON (Stretch Goal) -->
        <button onclick="openPartnerModal()" class="header-icon-btn" title="Partner & Sales Back-Office Desk (ML Propensity)" style="color: #059669;">
          <i class="fa-solid fa-headset"></i>
        </button>
'''
    if 'openPartnerModal()' not in content:
        content = content.replace('<!-- Dev Mode: ICON ONLY as requested -->', headset_btn + '        <!-- Dev Mode: ICON ONLY as requested -->')

    # 2. Add partnerModal HTML
    partner_modal_html = '''
    <!-- Partner & Sales Back-Office Modal (Stretch Goal) -->
    <div class="bottom-sheet-overlay" id="partnerModal" style="display: none; z-index: 1000;">
      <div class="bottom-sheet-card" style="max-height: 90dvh; display: flex; flex-direction: column;">
        <div class="sheet-handle"></div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-shrink: 0;">
          <div>
            <b style="font-size: 14px; color: var(--airtel-dark);"><i class="fa-solid fa-headset" style="color: #059669;"></i> Partner &amp; Sales Back-Office Desk</b>
            <div style="font-size: 10px; color: var(--text-muted);">Unclosed Lead Recovery with ML Propensity Scoring (0–100)</div>
          </div>
          <i class="fa-solid fa-xmark" style="cursor: pointer; color: var(--text-muted); font-size: 18px; padding: 4px;" onclick="closePartnerModal()"></i>
        </div>

        <!-- Top KPI Strip -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-bottom: 10px; flex-shrink: 0;">
          <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 6px; text-align: center;">
            <div style="font-size: 9px; color: #64748B; font-weight: 700;">UNCLOSED POOL</div>
            <div style="font-size: 14px; font-weight: 900; color: #E40000;">4,632</div>
            <div style="font-size: 8.5px; color: #94A3B8;">smb_leads.csv</div>
          </div>
          <div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 8px; padding: 6px; text-align: center;">
            <div style="font-size: 9px; color: #047857; font-weight: 700;">HIGH INTENT</div>
            <div style="font-size: 14px; font-weight: 900; color: #059669;">805</div>
            <div style="font-size: 8.5px; color: #047857;">Propensity &ge;75%</div>
          </div>
          <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 6px; text-align: center;">
            <div style="font-size: 9px; color: #1E40AF; font-weight: 700;">COMMISSION</div>
            <div style="font-size: 14px; font-weight: 900; color: #2563EB;">₹1,500</div>
            <div style="font-size: 8.5px; color: #3B82F6;">Per Rescued Lead</div>
          </div>
        </div>

        <div style="font-size: 11px; font-weight: 700; color: #334155; margin-bottom: 6px;">Priority Unclosed Leads to Call:</div>
        
        <div id="partnerLeadsList" style="overflow-y: auto; padding-right: 4px; flex: 1; display: flex; flex-direction: column; gap: 8px;">
          <div style="text-align: center; color: #64748B; font-size: 12px; padding: 20px;">Loading unclosed leads...</div>
        </div>
      </div>
    </div>
'''
    if 'id="partnerModal"' not in content:
        content = content.replace('<!-- DPDP Act 2023 Mobile Bottom Sheet -->', partner_modal_html + '\n    <!-- DPDP Act 2023 Mobile Bottom Sheet -->')

    # 3. Add Javascript functions
    js_funcs = '''
    /* ---------------- PARTNER & SALES BACK-OFFICE DESK (STRETCH GOAL) ---------------- */
    function openPartnerModal() {
      const modal = document.getElementById("partnerModal");
      if (modal) {
        modal.style.display = "flex";
        loadPartnerLeads();
      }
    }

    function closePartnerModal() {
      const modal = document.getElementById("partnerModal");
      if (modal) modal.style.display = "none";
    }

    async function loadPartnerLeads() {
      const container = document.getElementById("partnerLeadsList");
      if (!container) return;
      try {
        const res = await fetch("/api/backoffice/leads?limit=15");
        const data = await res.json();
        if (data.leads && data.leads.length > 0) {
          container.innerHTML = data.leads.map(l => {
            const badgeColor = l.priority === 'HIGH' ? '#DC2626' : (l.priority === 'MEDIUM' ? '#D97706' : '#64748B');
            const badgeBg = l.priority === 'HIGH' ? '#FEE2E2' : (l.priority === 'MEDIUM' ? '#FEF3C7' : '#F1F5F9');
            const isRescued = l.status === 'RESCUED';
            return `
              <div style="background: white; border: 1px solid #E2E8F0; border-radius: 10px; padding: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px;">
                  <div>
                    <b style="font-size: 12.5px; color: #0F172A;">${l.business_name}</b>
                    <div style="font-size: 10px; color: #64748B;">${l.business_type} • ${l.city} (Tier ${l.city_tier})</div>
                  </div>
                  <span style="background: ${badgeBg}; color: ${badgeColor}; font-size: 10px; font-weight: 800; padding: 2px 7px; border-radius: 4px;">
                    ${l.priority === 'HIGH' ? '🔥' : '⚡'} ${l.propensity_score}% PROPENSITY
                  </span>
                </div>
                <div style="font-size: 10.5px; color: #DC2626; margin-bottom: 4px;">
                  <i class="fa-solid fa-triangle-exclamation"></i> <b>Drop Reason:</b> ${l.drop_reason}
                </div>
                <div style="background: #F8FAFC; border-left: 3px solid #3B82F6; padding: 6px 8px; font-size: 10px; color: #334155; margin-bottom: 8px; border-radius: 0 4px 4px 0;">
                  <b>Recommended Talk Track:</b> ${l.recommended_talk_track}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                  <span style="font-size: 11px; font-weight: 700; color: #16A34A;">MRR: ₹${Number(l.estimated_mrr).toLocaleString()}</span>
                  ${isRescued ? 
                    `<span style="background: #DCFCE7; color: #15803D; font-size: 10.5px; font-weight: 800; padding: 4px 10px; border-radius: 6px;"><i class="fa-solid fa-check"></i> Rescued &amp; Commission Logged</span>` :
                    `<button onclick="rescueLeadAction('${l.lead_id}', this)" style="background: #059669; color: white; border: none; border-radius: 6px; padding: 5px 12px; font-size: 11px; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 4px;">
                      <i class="fa-solid fa-phone"></i> Call Lead &amp; Rescue
                    </button>`
                  }
                </div>
              </div>
            `;
          }).join("");
        } else {
          container.innerHTML = `<div style="text-align: center; color: #64748B; font-size: 12px; padding: 20px;">No unclosed leads found.</div>`;
        }
      } catch (e) {
        container.innerHTML = `<div style="color: #991B1B; font-size: 12px; padding: 10px;">Failed to load leads.</div>`;
      }
    }

    async function rescueLeadAction(leadId, btn) {
      btn.disabled = true;
      btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Rescuing...`;
      try {
        const res = await fetch("/api/backoffice/rescue", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ lead_id: leadId, agent_name: "Airtel Partner Desk #412", notes: "Applied 5% multi-product discount" })
        });
        const d = await res.json();
        if (d.success) {
          btn.parentElement.innerHTML = `<span style="background: #DCFCE7; color: #15803D; font-size: 10.5px; font-weight: 800; padding: 4px 10px; border-radius: 6px;"><i class="fa-solid fa-check"></i> Rescued &amp; Commission Logged</span>`;
        }
      } catch(e) {
        btn.disabled = false;
        btn.innerHTML = `<i class="fa-solid fa-phone"></i> Retry`;
      }
    }
'''

    if 'function openPartnerModal()' not in content:
        content = content.replace('function openDevModal() {', js_funcs + '\n    function openDevModal() {')

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Successfully integrated Partner Back-Office in frontend/index.html")

if __name__ == "__main__":
    update_frontend()
