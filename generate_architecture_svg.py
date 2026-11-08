import os

def generate_architecture_svg(output_path):
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="100%" height="100%" style="background:#F8FAFC; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <defs>
    <filter id="cardShadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feGaussianBlur in="SourceAlpha" stdDeviation="4"/>
      <feOffset dx="0" dy="3"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.08"/></feComponentTransfer>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="gradRed" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#E40000"/>
      <stop offset="100%" stop-color="#B91C1C"/>
    </linearGradient>
    <linearGradient id="gradDark" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
    <linearGradient id="gradGreen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10B981"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
    <linearGradient id="gradBlue" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#1D4ED8"/>
    </linearGradient>
    <linearGradient id="gradPurple" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7C3AED"/>
      <stop offset="100%" stop-color="#6D28D9"/>
    </linearGradient>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#E40000"/>
    </marker>
    <marker id="arrowDark" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#64748B"/>
    </marker>
  </defs>

  <!-- ==================== HEADER BANNER ==================== -->
  <rect x="0" y="0" width="1200" height="70" fill="url(#gradDark)"/>
  <rect x="0" y="67" width="1200" height="3" fill="url(#gradRed)"/>
  
  <text x="40" y="42" font-size="22" font-weight="900" fill="#FFFFFF" letter-spacing="-0.5">PROJECT UDYAM DIGITAL</text>
  <text x="340" y="42" font-size="14" font-weight="600" fill="#94A3B8">|</text>
  <text x="360" y="42" font-size="13" font-weight="700" fill="#FCA5A5">END-TO-END SYSTEM ARCHITECTURE &amp; DATA FLOWS</text>
  <rect x="1020" y="20" width="140" height="30" rx="15" fill="#E40000"/>
  <text x="1090" y="40" font-size="11" font-weight="800" fill="#FFFFFF" text-anchor="middle">AIRTEL SYNC 2026</text>

  <!-- ==================== TIER 1: CLIENT EXPERIENCE LAYER ==================== -->
  <g transform="translate(40, 90)">
    <rect x="0" y="0" width="1120" height="130" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#cardShadow)"/>
    <path d="M 0 10 Q 0 0 10 0 L 1110 0 Q 1120 0 1120 10 L 1120 28 L 0 28 Z" fill="#F1F5F9"/>
    <text x="16" y="19" font-size="11" font-weight="800" fill="#0F172A">TIER 1: CLIENT EXPERIENCE LAYER (MOBILE PWA / ZERO-APP-INSTALL)</text>
    <text x="1104" y="19" font-size="10" font-weight="700" fill="#E40000" text-anchor="end">ANAGEME.VERCEL.APP</text>

    <!-- Sub-boxes -->
    <rect x="16" y="38" width="255" height="76" rx="8" fill="#FFF1F2" stroke="#FECDD3" stroke-width="1"/>
    <text x="28" y="58" font-size="12" font-weight="800" fill="#E40000">1. Conversational Chat Advisor</text>
    <text x="28" y="75" font-size="10" fill="#475569">• Dynamic Quick-Reply Chips</text>
    <text x="28" y="90" font-size="10" fill="#475569">• Plain-Language Benefit Reasoning</text>
    <text x="28" y="104" font-size="10" fill="#475569">• Step Preservation on Inquiry</text>

    <rect x="290" y="38" width="255" height="76" rx="8" fill="#FFF1F2" stroke="#FECDD3" stroke-width="1"/>
    <text x="302" y="58" font-size="12" font-weight="800" fill="#E40000">2. Dual-Engine Voice STT/TTS</text>
    <text x="302" y="75" font-size="10" fill="#475569">• Direct Web Speech API (Zero Lag)</text>
    <text x="302" y="90" font-size="10" fill="#475569">• MediaRecorder Fallback (iOS/Safari)</text>
    <text x="302" y="104" font-size="10" fill="#475569">• Auto-Voice Flipping Pill Switch</text>

    <rect x="565" y="38" width="265" height="76" rx="8" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1"/>
    <text x="577" y="58" font-size="12" font-weight="800" fill="#1D4ED8">3. My Bundle (3 Full-View Subtabs)</text>
    <text x="577" y="75" font-size="10" fill="#475569">• [Plan &amp; Price] Zero-Scroll Line Items</text>
    <text x="577" y="90" font-size="10" fill="#475569">• [Smart KYC] Camera OCR + Form</text>
    <text x="577" y="104" font-size="10" fill="#475569">• [GIS Network] 5G AirFiber Benchmark</text>

    <rect x="850" y="38" width="254" height="76" rx="8" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1"/>
    <text x="862" y="58" font-size="12" font-weight="800" fill="#047857">4. Self-Serve SLA Milestone Tracker</text>
    <text x="862" y="75" font-size="10" fill="#475569">• 5 Real-Time Status Milestones</text>
    <text x="862" y="90" font-size="10" fill="#475569">• Live Delhivery Courier Tracking</text>
    <text x="862" y="104" font-size="10" fill="#475569">• Assigned Lead Engineer Contact</text>
  </g>

  <!-- Connectors T1 -> T2 -->
  <line x1="600" y1="220" x2="600" y2="245" stroke="#E40000" stroke-width="2.5" marker-end="url(#arrowRed)" stroke-dasharray="4,3"/>

  <!-- ==================== TIER 2: API GATEWAY & ORCHESTRATION LAYER ==================== -->
  <g transform="translate(40, 245)">
    <rect x="0" y="0" width="1120" height="115" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#cardShadow)"/>
    <path d="M 0 10 Q 0 0 10 0 L 1110 0 Q 1120 0 1120 10 L 1120 28 L 0 28 Z" fill="#F1F5F9"/>
    <text x="16" y="19" font-size="11" font-weight="800" fill="#0F172A">TIER 2: API GATEWAY &amp; SESSION STATE ORCHESTRATOR (FASTAPI + PYTHON 3.12)</text>
    <text x="1104" y="19" font-size="10" font-weight="700" fill="#2563EB" text-anchor="end">ASYNC HIGH-THROUGHPUT</text>

    <!-- Sub-boxes -->
    <rect x="16" y="38" width="345" height="63" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
    <text x="28" y="56" font-size="11.5" font-weight="800" fill="#0F172A">REST API Endpoints</text>
    <text x="28" y="72" font-size="10" fill="#475569">• /api/chat · /api/quote · /api/kyc/*</text>
    <text x="28" y="87" font-size="10" fill="#475569">• /api/feasibility · /api/tracker · /api/evals</text>

    <rect x="380" y="38" width="355" height="63" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
    <text x="392" y="56" font-size="11.5" font-weight="800" fill="#0F172A">Session State Machine &amp; Vault</text>
    <text x="392" y="72" font-size="10" fill="#475569">• Persistent Session Context &amp; Cart State</text>
    <text x="392" y="87" font-size="10" fill="#475569">• 5-Stage Guided Acquisition Flow</text>

    <rect x="755" y="38" width="349" height="63" rx="8" fill="#FFFBEB" stroke="#FDE68A" stroke-width="1"/>
    <text x="767" y="56" font-size="11.5" font-weight="800" fill="#B45309">Loop Engine &amp; Circuit Breakers</text>
    <text x="767" y="72" font-size="10" fill="#475569">• Automatic Fallback on LLM 429 Rate Limits</text>
    <text x="767" y="87" font-size="10" fill="#475569">• Objection Detection &amp; Warm Handoff Queue</text>
  </g>

  <!-- Connectors T2 -> T3 & T4 -->
  <line x1="310" y1="360" x2="310" y2="385" stroke="#E40000" stroke-width="2.5" marker-end="url(#arrowRed)"/>
  <line x1="890" y1="360" x2="890" y2="385" stroke="#E40000" stroke-width="2.5" marker-end="url(#arrowRed)"/>

  <!-- ==================== TIER 3 & 4 (SPLIT COLUMNS) ==================== -->
  
  <!-- LEFT COLUMN: TIER 3: AI & INTELLIGENCE ENGINE -->
  <g transform="translate(40, 385)">
    <rect x="0" y="0" width="545" height="325" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#cardShadow)"/>
    <path d="M 0 10 Q 0 0 10 0 L 535 0 Q 545 0 545 10 L 545 28 L 0 28 Z" fill="#FEE2E2"/>
    <text x="16" y="19" font-size="11" font-weight="800" fill="#E40000">TIER 3: AI &amp; CATALOG INTELLIGENCE LAYER</text>

    <rect x="16" y="38" width="513" height="85" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="28" y="58" font-size="12" font-weight="800" fill="#0F172A">Gemini 2.5 Flash Conversational NLU</text>
    <text x="28" y="75" font-size="10" fill="#475569">• Multilingual reasoning in 6 Indian languages (HI, EN, TA, BN, TE, MR)</text>
    <text x="28" y="90" font-size="10" fill="#475569">• RAG grounding on official catalog features &amp; constraints</text>
    <text x="28" y="105" font-size="10" fill="#475569">• Conversational sales assistant answering ad-hoc queries</text>

    <rect x="16" y="132" width="513" height="85" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="28" y="152" font-size="12" font-weight="800" fill="#0F172A">Deterministic Catalog &amp; Quoting Engine</text>
    <text x="28" y="169" font-size="10" fill="#475569">• 25 official products across Connectivity, Comm, Cloud &amp; Security</text>
    <text x="28" y="184" font-size="10" fill="#475569">• Zero-hallucination math: 5% bundle discount + setup waiver</text>
    <text x="28" y="199" font-size="10" fill="#475569">• Automated product dependency checks (e.g. Failover requiring base Fiber)</text>

    <rect x="16" y="226" width="513" height="85" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="28" y="246" font-size="12" font-weight="800" fill="#0F172A">Vision Multimodal OCR + WinRT Engine</text>
    <text x="28" y="263" font-size="10" fill="#475569">• Gemini 2.5 Flash Vision OCR extracting GSTIN, Udyam, bills &amp; IDs</text>
    <text x="28" y="278" font-size="10" fill="#475569">• Local WinRT OCR on-device fallback for offline resilience</text>
    <text x="28" y="293" font-size="10" fill="#475569">• Audio transcription API supporting native audio bytes streaming</text>
  </g>

  <!-- RIGHT COLUMN: TIER 4: REGULATORY & REGISTRY VERIFICATION LAYER -->
  <g transform="translate(615, 385)">
    <rect x="0" y="0" width="545" height="325" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#cardShadow)"/>
    <path d="M 0 10 Q 0 0 10 0 L 535 0 Q 545 0 545 10 L 545 28 L 0 28 Z" fill="#DCFCE7"/>
    <text x="16" y="19" font-size="11" font-weight="800" fill="#047857">TIER 4: REGULATORY, IDENTITY &amp; COMPLIANCE LAYER</text>

    <rect x="16" y="38" width="513" height="85" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="28" y="58" font-size="12" font-weight="800" fill="#0F172A">DPDP Act 2023 Statutory Compliance Shield</text>
    <text x="28" y="75" font-size="10" fill="#475569">• Section 5: Transparent lawful notice of purpose (DoT KYC only)</text>
    <text x="28" y="90" font-size="10" fill="#475569">• Section 6: Affirmative consent SHA-256 cryptographic audit token</text>
    <text x="28" y="105" font-size="10" fill="#475569">• Section 8: PII Masking (Aadhaar, PAN, GSTIN) + ephemeral photo purge</text>

    <rect x="16" y="132" width="513" height="85" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="28" y="152" font-size="12" font-weight="800" fill="#0F172A">National Mock Registry Verification APIs</text>
    <text x="28" y="169" font-size="10" fill="#475569">• GSTIN Registry: 3,534 records checked for ACTIVE / CANCELLED status</text>
    <text x="28" y="184" font-size="10" fill="#475569">• Udyam Registry: 2,723 MSME records verified for business classification</text>
    <text x="28" y="199" font-size="10" fill="#475569">• Instant pass/fail for non-GST merchants via alternative ID proof</text>

    <rect x="16" y="226" width="513" height="85" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="28" y="246" font-size="12" font-weight="800" fill="#0F172A">Automated Fraud &amp; Anomaly Detection (K01–K12)</text>
    <text x="28" y="263" font-size="10" fill="#475569">• Catches CANCELLED GSTINs (K01) &amp; Unregistered Fake GSTINs (K06)</text>
    <text x="28" y="278" font-size="10" fill="#475569">• DoT 90-Day Utility Proof Enforcer: Catches bills older than 90d (K11)</text>
    <text x="28" y="293" font-size="10" fill="#475569">• Signatory PAN name matching entity authorization</text>
  </g>

  <!-- Connector T3/T4 -> T5 -->
  <line x1="600" y1="710" x2="600" y2="735" stroke="#E40000" stroke-width="2.5" marker-end="url(#arrowRed)"/>

  <!-- ==================== TIER 5: FULFILLMENT, OPERATIONS & PARTNER DESK ==================== -->
  <g transform="translate(40, 735)">
    <rect x="0" y="0" width="1120" height="135" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#cardShadow)"/>
    <path d="M 0 10 Q 0 0 10 0 L 1110 0 Q 1120 0 1120 10 L 1120 28 L 0 28 Z" fill="#EFF6FF"/>
    <text x="16" y="19" font-size="11" font-weight="800" fill="#1D4ED8">TIER 5: FULFILLMENT, OPERATIONS &amp; CHANNEL PARTNER DESK</text>
    <text x="1104" y="19" font-size="10" font-weight="700" fill="#059669" text-anchor="end">SLA GUARANTEED &amp; ZERO-DROP</text>

    <rect x="16" y="38" width="345" height="82" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
    <text x="28" y="58" font-size="12" font-weight="800" fill="#0F172A">GIS Feasibility &amp; 5G Auto-Pivot</text>
    <text x="28" y="75" font-size="10" fill="#475569">• FAT Splitter Proximity Calculation (&lt;250m)</text>
    <text x="28" y="90" font-size="10" fill="#475569">• Self-Healing: Auto-pivot to 5G AirFiber (FWA)</text>
    <text x="28" y="105" font-size="10" fill="#475569">• 48-Hour Plug-and-Play Installation SLA</text>

    <rect x="380" y="38" width="355" height="82" rx="8" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="1"/>
    <text x="392" y="58" font-size="12" font-weight="800" fill="#0F172A">Logistics &amp; Field Dispatch (Delhivery)</text>
    <text x="392" y="75" font-size="10" fill="#475569">• Automated Courier Waybill Generation</text>
    <text x="392" y="90" font-size="10" fill="#475569">• Lead Field Engineer Auto-Assignment</text>
    <text x="392" y="105" font-size="10" fill="#475569">• SMS/WhatsApp Status Notification Dispatch</text>

    <rect x="755" y="38" width="349" height="82" rx="8" fill="#FDF2F8" stroke="#FBCFE8" stroke-width="1"/>
    <text x="767" y="58" font-size="12" font-weight="800" fill="#9D174D">Partner Back-Office &amp; ML Propensity</text>
    <text x="767" y="75" font-size="10" fill="#475569">• Unclosed Cart Recovery Queue with Reasons</text>
    <text x="767" y="90" font-size="10" fill="#475569">• ML Propensity Score (0–100) Prioritizing Calls</text>
    <text x="767" y="105" font-size="10" fill="#475569">• Partner Co-Pilot Mode with Commission Split</text>
  </g>

</svg>"""
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Architecture SVG generated: {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "architecture_diagram.svg")
    generate_architecture_svg(out)
    
    # Also copy to frontend
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
    if os.path.exists(frontend_dir):
        frontend_svg = os.path.join(frontend_dir, "architecture_diagram.svg")
        import shutil
        shutil.copyfile(out, frontend_svg)
        print(f"Copied to frontend: {frontend_svg}")
