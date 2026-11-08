import os
import fitz
import shutil

def generate_16x9_architecture_svg(output_path):
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080" style="background:#F8FAFC; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <defs>
    <filter id="shadowCard" x="-4%" y="-3%" width="108%" height="110%" filterUnits="userSpaceOnUse">
      <feGaussianBlur in="SourceAlpha" stdDeviation="5"/>
      <feOffset dx="0" dy="4"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.07"/></feComponentTransfer>
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
    <linearGradient id="gradBlue" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2563EB"/>
      <stop offset="100%" stop-color="#1D4ED8"/>
    </linearGradient>
    <linearGradient id="gradPurple" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#7C3AED"/>
      <stop offset="100%" stop-color="#6D28D9"/>
    </linearGradient>
    <linearGradient id="gradGreen" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10B981"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
    <linearGradient id="gradAmber" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#D97706"/>
    </linearGradient>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#E40000"/>
    </marker>
    <marker id="arrowSlate" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#94A3B8"/>
    </marker>
  </defs>

  <!-- ==================== TOP NAVIGATION / HEADER (y: 0 to 76) ==================== -->
  <rect x="0" y="0" width="1920" height="74" fill="url(#gradDark)"/>
  <rect x="0" y="72" width="1920" height="4" fill="url(#gradRed)"/>

  <!-- Logo Mark -->
  <rect x="50" y="18" width="38" height="38" rx="8" fill="#E40000"/>
  <circle cx="69" cy="37" r="10" fill="#FFFFFF"/>
  <circle cx="69" cy="37" r="5" fill="#E40000"/>

  <text x="100" y="44" font-size="24" font-weight="900" fill="#FFFFFF" letter-spacing="-0.5">PROJECT UDYAM DIGITAL</text>
  <text x="445" y="44" font-size="16" font-weight="400" fill="#64748B">|</text>
  <text x="465" y="44" font-size="15" font-weight="700" fill="#FCA5A5" letter-spacing="0.5">END-TO-END 5-TIER SOLUTION ARCHITECTURE &amp; DATA FLOW</text>
  <text x="1230" y="44" font-size="13" font-weight="600" fill="#94A3B8">ENTERPRISE TRACK A: 10-MIN ZERO-DROP MSME ONBOARDING</text>

  <!-- Badges -->
  <rect x="1710" y="20" width="160" height="34" rx="17" fill="#E40000"/>
  <text x="1790" y="42" font-size="13" font-weight="800" fill="#FFFFFF" text-anchor="middle">AIRTEL SYNC 2026</text>

  <!-- ==================== TOP HORIZONTAL PIPELINE FLOW INDICATOR (y: 88 to 118) ==================== -->
  <g transform="translate(50, 86)">
    <rect x="0" y="0" width="1820" height="34" rx="6" fill="#F1F5F9" stroke="#E2E8F0" stroke-width="1"/>
    
    <text x="172" y="22" font-size="12" font-weight="800" fill="#E40000" text-anchor="middle">1. Client Interaction (Voice / PWA)</text>
    <path d="M 344 17 L 366 17" stroke="#CBD5E1" stroke-width="2" marker-end="url(#arrowSlate)"/>

    <text x="541" y="22" font-size="12" font-weight="800" fill="#2563EB" text-anchor="middle">2. API Gateway &amp; State Machine</text>
    <path d="M 713 17 L 735 17" stroke="#CBD5E1" stroke-width="2" marker-end="url(#arrowSlate)"/>

    <text x="910" y="22" font-size="12" font-weight="800" fill="#7C3AED" text-anchor="middle">3. AI Intelligence &amp; Quoting Core</text>
    <path d="M 1082 17 L 1104 17" stroke="#CBD5E1" stroke-width="2" marker-end="url(#arrowSlate)"/>

    <text x="1279" y="22" font-size="12" font-weight="800" fill="#059669" text-anchor="middle">4. DPDP Statutory Shield &amp; KYC</text>
    <path d="M 1451 17 L 1473 17" stroke="#CBD5E1" stroke-width="2" marker-end="url(#arrowSlate)"/>

    <text x="1648" y="22" font-size="12" font-weight="800" fill="#D97706" text-anchor="middle">5. 48h SLA &amp; Partner Desk</text>
  </g>

  <!-- ==================== TIER 1: CLIENT EXPERIENCE LAYER (x: 50, w: 344) ==================== -->
  <g transform="translate(50, 130)">
    <rect x="0" y="0" width="344" height="825" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#shadowCard)"/>
    <path d="M 0 12 Q 0 0 12 0 L 332 0 Q 344 0 344 12 L 344 46 L 0 46 Z" fill="url(#gradRed)"/>
    <text x="18" y="28" font-size="13" font-weight="900" fill="#FFFFFF" letter-spacing="0.5">TIER 1: CLIENT EXPERIENCE</text>
    <rect x="238" y="12" width="94" height="22" rx="11" fill="#FFFFFF" fill-opacity="0.2"/>
    <text x="285" y="27" font-size="10" font-weight="800" fill="#FFFFFF" text-anchor="middle">MOBILE PWA</text>

    <!-- Card 1A: Conversational Voice & Chat -->
    <rect x="14" y="58" width="316" height="175" rx="8" fill="#FFF1F2" stroke="#FECDD3" stroke-width="1"/>
    <rect x="24" y="68" width="24" height="24" rx="6" fill="#E40000"/>
    <text x="36" y="84" font-size="12" font-weight="900" fill="#FFFFFF" text-anchor="middle">1</text>
    <text x="56" y="84" font-size="13" font-weight="800" fill="#991B1B">Voice &amp; Chat Advisor</text>
    <text x="24" y="112" font-size="11.5" font-weight="600" fill="#1E293B">• Direct Web Speech API (Zero-Lag STT)</text>
    <text x="24" y="132" font-size="11" fill="#475569">• MediaRecorder Fallback (iOS / Safari)</text>
    <text x="24" y="152" font-size="11" fill="#475569">• Contextual Quick-Reply Chips</text>
    <text x="24" y="172" font-size="11" fill="#475569">• Plain-Language Business Reasoning</text>
    <text x="24" y="192" font-size="11" fill="#475569">• Step Memory on Ad-Hoc Inquiries</text>
    <rect x="24" y="204" width="296" height="20" rx="4" fill="#FFE4E6"/>
    <text x="172" y="218" font-size="10" font-weight="700" fill="#BE123C" text-anchor="middle">SLA: Sub-800ms End-to-End Voice Turn</text>

    <!-- Card 1B: My Bundle Single-View Hub -->
    <rect x="14" y="243" width="316" height="175" rx="8" fill="#EFF6FF" stroke="#BFDBFE" stroke-width="1"/>
    <rect x="24" y="253" width="24" height="24" rx="6" fill="#2563EB"/>
    <text x="36" y="269" font-size="12" font-weight="900" fill="#FFFFFF" text-anchor="middle">2</text>
    <text x="56" y="269" font-size="13" font-weight="800" fill="#1E40AF">My Bundle Single-View Hub</text>
    <text x="24" y="297" font-size="11.5" font-weight="600" fill="#1E293B">• 3 Full-View Subtabs (Zero Scroll):</text>
    <text x="36" y="316" font-size="11" fill="#3B82F6">🛒 Plan &amp; Price | 🛡️ KYC | 📡 GIS Net</text>
    <text x="24" y="336" font-size="11" fill="#475569">• Transparent Monthly Breakdown</text>
    <text x="24" y="356" font-size="11" fill="#475569">• 5% Multi-Product Bundle Discount</text>
    <text x="24" y="376" font-size="11" fill="#475569">• ₹2,500 Installation Waiver Applied</text>
    <rect x="24" y="388" width="296" height="20" rx="4" fill="#DBEAFE"/>
    <text x="172" y="402" font-size="10" font-weight="700" fill="#1D4ED8" text-anchor="middle">Solved: 56% Drop at Quoting Stage</text>

    <!-- Card 1C: Smart KYC Camera Scanner -->
    <rect x="14" y="428" width="316" height="180" rx="8" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1"/>
    <rect x="24" y="438" width="24" height="24" rx="6" fill="#059669"/>
    <text x="36" y="454" font-size="12" font-weight="900" fill="#FFFFFF" text-anchor="middle">3</text>
    <text x="56" y="454" font-size="13" font-weight="800" fill="#065F46">Smart KYC Camera OCR</text>
    <text x="24" y="482" font-size="11.5" font-weight="600" fill="#1E293B">• Instant Camera Snapshot &amp; Drag-Drop</text>
    <text x="24" y="502" font-size="11" fill="#475569">• Auto Edge Framing &amp; Lighting Check</text>
    <text x="24" y="522" font-size="11" fill="#475569">• Pre-Fills 100% of Entity Details</text>
    <text x="24" y="542" font-size="11" fill="#475569">• Frictionless Non-GST Trade Flow</text>
    <text x="24" y="562" font-size="11" fill="#475569">• DPDP One-Click Affirmative Consent</text>
    <rect x="24" y="578" width="296" height="20" rx="4" fill="#D1FAE5"/>
    <text x="172" y="592" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">KYC Completed in &lt;60 Seconds</text>

    <!-- Card 1D: Self-Serve SLA Milestone Tracker -->
    <rect x="14" y="618" width="316" height="192" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <rect x="24" y="628" width="24" height="24" rx="6" fill="#475569"/>
    <text x="36" y="644" font-size="12" font-weight="900" fill="#FFFFFF" text-anchor="middle">4</text>
    <text x="56" y="644" font-size="13" font-weight="800" fill="#1E293B">SLA Milestone Live Tracker</text>
    <text x="24" y="672" font-size="11.5" font-weight="600" fill="#1E293B">• 5 Live Fulfillment Milestones:</text>
    <text x="36" y="692" font-size="10.5" fill="#64748B">KYC → GIS → SIM/ONT → Dispatch → Active</text>
    <text x="24" y="712" font-size="11" fill="#475569">• Live Delhivery Courier Waybill Sync</text>
    <text x="24" y="732" font-size="11" fill="#475569">• Assigned Lead Engineer Call Button</text>
    <text x="24" y="752" font-size="11" fill="#475569">• Push Status Alerts via SMS / WhatsApp</text>
    <rect x="24" y="776" width="296" height="22" rx="4" fill="#E2E8F0"/>
    <text x="172" y="791" font-size="10" font-weight="700" fill="#334155" text-anchor="middle">Eliminates 3x Status Chases / Customer</text>
  </g>

  <!-- Flow Connector 1 -> 2 -->
  <g transform="translate(394, 480)">
    <line x1="0" y1="0" x2="25" y2="0" stroke="#E40000" stroke-width="2.5" marker-end="url(#arrowRed)"/>
    <rect x="-10" y="-30" width="45" height="18" rx="4" fill="#0F172A"/>
    <text x="12" y="-17" font-size="9" font-weight="800" fill="#FFFFFF" text-anchor="middle">JSON/WSS</text>
  </g>

  <!-- ==================== TIER 2: API GATEWAY & ORCHESTRATION (x: 419, w: 344) ==================== -->
  <g transform="translate(419, 130)">
    <rect x="0" y="0" width="344" height="825" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#shadowCard)"/>
    <path d="M 0 12 Q 0 0 12 0 L 332 0 Q 344 0 344 12 L 344 46 L 0 46 Z" fill="url(#gradBlue)"/>
    <text x="18" y="28" font-size="13" font-weight="900" fill="#FFFFFF" letter-spacing="0.5">TIER 2: API GATEWAY &amp; STATE</text>
    <rect x="210" y="12" width="122" height="22" rx="11" fill="#FFFFFF" fill-opacity="0.2"/>
    <text x="271" y="27" font-size="10" font-weight="800" fill="#FFFFFF" text-anchor="middle">FASTAPI + PY 3.12</text>

    <!-- Card 2A: REST API Gateway -->
    <rect x="14" y="58" width="316" height="240" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="24" y="85" font-size="13" font-weight="800" fill="#0F172A">High-Throughput REST Gateway</text>
    <text x="24" y="112" font-size="11" font-weight="700" fill="#2563EB">• /api/chat</text>
    <text x="36" y="128" font-size="10.5" fill="#475569">Async turns with context memory</text>
    <text x="24" y="148" font-size="11" font-weight="700" fill="#2563EB">• /api/quote</text>
    <text x="36" y="164" font-size="10.5" fill="#475569">Real-time dynamic pricing engine</text>
    <text x="24" y="184" font-size="11" font-weight="700" fill="#2563EB">• /api/kyc/* &amp; /api/voice/transcribe</text>
    <text x="36" y="200" font-size="10.5" fill="#475569">Gemini Flash audio &amp; OCR ingestion</text>
    <text x="24" y="220" font-size="11" font-weight="700" fill="#2563EB">• /api/feasibility &amp; /api/tracker</text>
    <text x="36" y="236" font-size="10.5" fill="#475569">GIS network + Delhivery waybills</text>
    <rect x="24" y="256" width="296" height="26" rx="4" fill="#EFF6FF"/>
    <text x="172" y="273" font-size="10" font-weight="700" fill="#1D4ED8" text-anchor="middle">Non-blocking ASGI Async Loop</text>

    <!-- Card 2B: State Machine & Vault -->
    <rect x="14" y="310" width="316" height="250" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="24" y="337" font-size="13" font-weight="800" fill="#0F172A">State Machine &amp; Session Vault</text>
    <text x="24" y="364" font-size="11.5" font-weight="600" fill="#1E293B">• 5-Stage Guided Acquisition Lifecycle:</text>
    <rect x="24" y="376" width="296" height="28" rx="4" fill="#F1F5F9" stroke="#CBD5E1"/>
    <text x="172" y="394" font-size="9.5" font-weight="700" fill="#0F172A" text-anchor="middle">GREET → NEEDS → QUOTE → KYC → ORDER</text>
    <text x="24" y="426" font-size="11" fill="#475569">• Cart &amp; Configuration Synchronization</text>
    <text x="24" y="446" font-size="11" fill="#475569">• Ephemeral Tokenized Session Vault</text>
    <text x="24" y="466" font-size="11" fill="#475569">• Zero Data Leakage Across Sessions</text>
    <text x="24" y="486" font-size="11" fill="#475569">• Real-Time Interaction Telemetry Log</text>
    <rect x="24" y="515" width="296" height="28" rx="4" fill="#EFF6FF"/>
    <text x="172" y="533" font-size="10" font-weight="700" fill="#1D4ED8" text-anchor="middle">Guarantees Deterministic Flow Traversal</text>

    <!-- Card 2C: Resilience & Circuit Breakers -->
    <rect x="14" y="572" width="316" height="238" rx="8" fill="#FFFBEB" stroke="#FDE68A" stroke-width="1"/>
    <text x="24" y="599" font-size="13" font-weight="800" fill="#92400E">Resilience &amp; Circuit Breakers</text>
    <text x="24" y="626" font-size="11.5" font-weight="600" fill="#1E293B">• Automated LLM 429 Rate-Limit Shield</text>
    <text x="24" y="646" font-size="11" fill="#475569">• Instant Rule-Based Fallback Engine</text>
    <text x="24" y="666" font-size="11" fill="#475569">• Drop-Off &amp; Abandonment Detector</text>
    <text x="24" y="686" font-size="11" fill="#475569">• Objection Escalation Classifier</text>
    <text x="24" y="706" font-size="11" fill="#475569">• Instant Push to Tele-Sales Rescue</text>
    <rect x="24" y="750" width="296" height="42" rx="4" fill="#FEF3C7"/>
    <text x="172" y="768" font-size="10" font-weight="800" fill="#B45309" text-anchor="middle">Zero Dead-Ends: If AI Fails or User Hesitates,</text>
    <text x="172" y="784" font-size="10" font-weight="800" fill="#B45309" text-anchor="middle">System Auto-Routes to Partner Rescue</text>
  </g>

  <!-- Flow Connector 2 -> 3 -->
  <g transform="translate(763, 300)">
    <line x1="0" y1="0" x2="25" y2="0" stroke="#7C3AED" stroke-width="2.5" marker-end="url(#arrowSlate)"/>
    <rect x="-10" y="-22" width="45" height="18" rx="4" fill="#0F172A"/>
    <text x="12" y="-9" font-size="9" font-weight="800" fill="#FFFFFF" text-anchor="middle">PROMPT</text>
  </g>
  <g transform="translate(763, 680)">
    <line x1="25" y1="0" x2="0" y2="0" stroke="#7C3AED" stroke-width="2.5" marker-end="url(#arrowSlate)"/>
    <rect x="-10" y="-22" width="45" height="18" rx="4" fill="#0F172A"/>
    <text x="12" y="-9" font-size="9" font-weight="800" fill="#FFFFFF" text-anchor="middle">QUOTES</text>
  </g>

  <!-- ==================== TIER 3: AI & CATALOG INTELLIGENCE (x: 788, w: 344) ==================== -->
  <g transform="translate(788, 130)">
    <rect x="0" y="0" width="344" height="825" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#shadowCard)"/>
    <path d="M 0 12 Q 0 0 12 0 L 332 0 Q 344 0 344 12 L 344 46 L 0 46 Z" fill="url(#gradPurple)"/>
    <text x="18" y="28" font-size="13" font-weight="900" fill="#FFFFFF" letter-spacing="0.5">TIER 3: AI &amp; CATALOG ENGINE</text>
    <rect x="230" y="12" width="102" height="22" rx="11" fill="#FFFFFF" fill-opacity="0.2"/>
    <text x="281" y="27" font-size="10" font-weight="800" fill="#FFFFFF" text-anchor="middle">GEMINI 2.5</text>

    <!-- Card 3A: Multilingual Conversational NLU -->
    <rect x="14" y="58" width="316" height="240" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="24" y="85" font-size="13" font-weight="800" fill="#581C87">Gemini 2.5 Flash Multilingual</text>
    <text x="24" y="112" font-size="11.5" font-weight="600" fill="#1E293B">• 6 Native Indian Languages:</text>
    <text x="36" y="132" font-size="11" fill="#7C3AED">Hindi, English, Tamil, Bengali, Telugu, Marathi</text>
    <text x="24" y="152" font-size="11" fill="#475569">• RAG Grounding on Official Airtel SKUs</text>
    <text x="24" y="172" font-size="11" fill="#475569">• Converts Specs to Business Value</text>
    <text x="36" y="190" font-size="10.5" fill="#64748B">(e.g., dual-band = zero POS payment fails)</text>
    <text x="24" y="212" font-size="11" fill="#475569">• Strict Safety Filters &amp; Boundary Guardrails</text>
    <rect x="24" y="248" width="296" height="34" rx="4" fill="#F3E8FF"/>
    <text x="172" y="269" font-size="10" font-weight="700" fill="#6D28D9" text-anchor="middle">100% Conversational RAG Grounding</text>

    <!-- Card 3B: Deterministic Quoting Core -->
    <rect x="14" y="310" width="316" height="250" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="24" y="337" font-size="13" font-weight="800" fill="#0F172A">Deterministic Quoting Engine</text>
    <text x="24" y="364" font-size="11.5" font-weight="600" fill="#1E293B">• 25 Official Products Indexed:</text>
    <text x="36" y="384" font-size="10.5" fill="#475569">Connectivity, Voice PBX, Cloud, Security, IoT</text>
    <text x="24" y="406" font-size="11" fill="#475569">• Zero LLM Hallucinations on Pricing</text>
    <text x="24" y="426" font-size="11" fill="#475569">• Automated 5% Multi-Product Discount</text>
    <text x="24" y="446" font-size="11" fill="#475569">• Rule-Based ₹2,500 Installation Waiver</text>
    <text x="24" y="466" font-size="11" fill="#475569">• Dependency Validator (e.g. Failover / Fiber)</text>
    <rect x="24" y="500" width="296" height="42" rx="4" fill="#F5F3FF"/>
    <text x="172" y="518" font-size="10" font-weight="800" fill="#5B21B6" text-anchor="middle">Math Rule: subtotal * 0.95</text>
    <text x="172" y="534" font-size="10" font-weight="600" fill="#6D28D9" text-anchor="middle">Guarantees 100% Billing Reconciliation</text>

    <!-- Card 3C: Vision OCR & Audio Ingestion -->
    <rect x="14" y="572" width="316" height="238" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="24" y="599" font-size="13" font-weight="800" fill="#0F172A">Multimodal Vision &amp; Audio OCR</text>
    <text x="24" y="626" font-size="11.5" font-weight="600" fill="#1E293B">• Gemini 2.5 Flash Vision Document Parser</text>
    <text x="24" y="646" font-size="11" fill="#475569">• Local WinRT OCR Fallback Engine</text>
    <text x="24" y="666" font-size="11" fill="#475569">• Sub-2s Extraction of Legal Dossiers:</text>
    <text x="36" y="686" font-size="10.5" fill="#64748B">GSTIN, Trade Name, Address, Udyam, Bills</text>
    <text x="24" y="708" font-size="11" fill="#475569">• Server-side Gemini Audio Transcription</text>
    <rect x="24" y="750" width="296" height="42" rx="4" fill="#EDE9FE"/>
    <text x="172" y="768" font-size="10" font-weight="800" fill="#4C1D95" text-anchor="middle">Paperless Onboarding:</text>
    <text x="172" y="784" font-size="10" font-weight="600" fill="#5B21B6" text-anchor="middle">Zero Typing Required on Mobile Keyboards</text>
  </g>

  <!-- Flow Connector 3 -> 4 -->
  <g transform="translate(1132, 480)">
    <line x1="0" y1="0" x2="25" y2="0" stroke="#059669" stroke-width="2.5" marker-end="url(#arrowSlate)"/>
    <rect x="-10" y="-30" width="45" height="18" rx="4" fill="#0F172A"/>
    <text x="12" y="-17" font-size="9" font-weight="800" fill="#FFFFFF" text-anchor="middle">VERIFY</text>
  </g>

  <!-- ==================== TIER 4: REGULATORY & REGISTRIES (x: 1157, w: 344) ==================== -->
  <g transform="translate(1157, 130)">
    <rect x="0" y="0" width="344" height="825" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#shadowCard)"/>
    <path d="M 0 12 Q 0 0 12 0 L 332 0 Q 344 0 344 12 L 344 46 L 0 46 Z" fill="url(#gradGreen)"/>
    <text x="18" y="28" font-size="13" font-weight="900" fill="#FFFFFF" letter-spacing="0.5">TIER 4: REGULATORY &amp; DPDP</text>
    <rect x="210" y="12" width="122" height="22" rx="11" fill="#FFFFFF" fill-opacity="0.2"/>
    <text x="271" y="27" font-size="10" font-weight="800" fill="#FFFFFF" text-anchor="middle">DPDP ACT 2023</text>

    <!-- Card 4A: DPDP Act 2023 Statutory Compliance -->
    <rect x="14" y="58" width="316" height="240" rx="8" fill="#ECFDF5" stroke="#A7F3D0" stroke-width="1"/>
    <text x="24" y="85" font-size="13" font-weight="800" fill="#065F46">DPDP Act 2023 Statutory Shield</text>
    <text x="24" y="112" font-size="11" font-weight="700" fill="#047857">• Section 5 (Notice):</text>
    <text x="36" y="128" font-size="10.5" fill="#475569">Itemized notice: DoT KYC purpose only</text>
    <text x="24" y="148" font-size="11" font-weight="700" fill="#047857">• Section 6 (Consent):</text>
    <text x="36" y="164" font-size="10.5" fill="#475569">SHA-256 cryptographic audit token stored</text>
    <text x="24" y="184" font-size="11" font-weight="700" fill="#047857">• Section 8 (Data Minimization):</text>
    <text x="36" y="200" font-size="10.5" fill="#475569">Immediate PII masking (Aadhaar, PAN)</text>
    <text x="24" y="220" font-size="11" font-weight="700" fill="#047857">• Ephemeral Storage:</text>
    <text x="36" y="236" font-size="10.5" fill="#475569">Raw document images purged post-OCR</text>
    <rect x="24" y="256" width="296" height="26" rx="4" fill="#D1FAE5"/>
    <text x="172" y="273" font-size="10" font-weight="800" fill="#065F46" text-anchor="middle">Auditable Tamper-Proof Consent Trail</text>

    <!-- Card 4B: National Mock Registry Engine -->
    <rect x="14" y="310" width="316" height="250" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="24" y="337" font-size="13" font-weight="800" fill="#0F172A">National Mock Registries</text>
    <text x="24" y="364" font-size="11.5" font-weight="600" fill="#1E293B">• GSTIN Registry Engine:</text>
    <text x="36" y="384" font-size="10.5" fill="#475569">3,534 live merchant records indexed</text>
    <text x="36" y="400" font-size="10.5" fill="#475569">Real-time status check: ACTIVE vs CANCELLED</text>
    <text x="24" y="424" font-size="11.5" font-weight="600" fill="#1E293B">• MSME Udyam Registry:</text>
    <text x="36" y="444" font-size="10.5" fill="#475569">2,723 verified enterprise profiles</text>
    <text x="24" y="468" font-size="11.5" font-weight="600" fill="#1E293B">• Non-GST Alternative Proof Path:</text>
    <text x="36" y="488" font-size="10.5" fill="#475569">Validates Shop &amp; Est. Act / Electricity Bill</text>
    <rect x="24" y="515" width="296" height="28" rx="4" fill="#ECFDF5"/>
    <text x="172" y="533" font-size="10" font-weight="700" fill="#047857" text-anchor="middle">Unlocks 55% Non-GST Micro MSME Segment</text>

    <!-- Card 4C: Automated Fraud & Anomaly Rules -->
    <rect x="14" y="572" width="316" height="238" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="24" y="599" font-size="13" font-weight="800" fill="#0F172A">Risk &amp; Fraud Matrix (K01–K12)</text>
    <text x="24" y="626" font-size="11.5" font-weight="600" fill="#1E293B">• 12 Planted Field Anomaly Rules:</text>
    <text x="24" y="648" font-size="11" fill="#DC2626">• K01: Detects CANCELLED GSTIN status</text>
    <text x="24" y="668" font-size="11" fill="#DC2626">• K06: Detects Fake / Unregistered GSTIN</text>
    <text x="24" y="688" font-size="11" fill="#DC2626">• K11: DoT 90-Day Utility Recency Enforcer</text>
    <text x="36" y="706" font-size="10.5" fill="#64748B">(Flags electricity bills older than 90 days)</text>
    <text x="24" y="726" font-size="11" fill="#475569">• Signatory PAN vs Trade Name matching</text>
    <rect x="24" y="750" width="296" height="42" rx="4" fill="#FEF2F2"/>
    <text x="172" y="768" font-size="10" font-weight="800" fill="#B91C1C" text-anchor="middle">100% Planted Dossier Audits Caught</text>
    <text x="172" y="784" font-size="10" font-weight="600" fill="#DC2626" text-anchor="middle">Zero Telecom Regulatory Non-Compliance</text>
  </g>

  <!-- Flow Connector 4 -> 5 -->
  <g transform="translate(1501, 480)">
    <line x1="0" y1="0" x2="25" y2="0" stroke="#D97706" stroke-width="2.5" marker-end="url(#arrowSlate)"/>
    <rect x="-10" y="-30" width="45" height="18" rx="4" fill="#0F172A"/>
    <text x="12" y="-17" font-size="9" font-weight="800" fill="#FFFFFF" text-anchor="middle">DISPATCH</text>
  </g>

  <!-- ==================== TIER 5: FULFILLMENT & PARTNER DESK (x: 1526, w: 344) ==================== -->
  <g transform="translate(1526, 130)">
    <rect x="0" y="0" width="344" height="825" rx="12" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1.5" filter="url(#shadowCard)"/>
    <path d="M 0 12 Q 0 0 12 0 L 332 0 Q 344 0 344 12 L 344 46 L 0 46 Z" fill="url(#gradAmber)"/>
    <text x="18" y="28" font-size="13" font-weight="900" fill="#FFFFFF" letter-spacing="0.5">TIER 5: FULFILLMENT &amp; RESCUE</text>
    <rect x="210" y="12" width="122" height="22" rx="11" fill="#FFFFFF" fill-opacity="0.2"/>
    <text x="271" y="27" font-size="10" font-weight="800" fill="#FFFFFF" text-anchor="middle">48H SLA &amp; DESK</text>

    <!-- Card 5A: GIS Feasibility & 5G AirFiber Pivot -->
    <rect x="14" y="58" width="316" height="240" rx="8" fill="#FFFBEB" stroke="#FDE68A" stroke-width="1"/>
    <text x="24" y="85" font-size="13" font-weight="800" fill="#B45309">GIS Feasibility &amp; 5G Auto-Pivot</text>
    <text x="24" y="112" font-size="11.5" font-weight="600" fill="#1E293B">• FAT Splitter Proximity Calculation:</text>
    <text x="36" y="132" font-size="11" fill="#059669">Within 250m: Dedicated Optical Fiber</text>
    <text x="24" y="154" font-size="11.5" font-weight="600" fill="#1E293B">• Autonomous Self-Healing Pivot:</text>
    <text x="36" y="174" font-size="11" fill="#D97706">&gt;250m: Auto-pivot to 5G AirFiber FWA</text>
    <text x="24" y="196" font-size="11" fill="#475569">• Prevents Customer Drop at Feasibility</text>
    <text x="24" y="216" font-size="11" fill="#475569">• 48-Hour Plug-and-Play Setup SLA</text>
    <rect x="24" y="256" width="296" height="26" rx="4" fill="#FEF3C7"/>
    <text x="172" y="273" font-size="10" font-weight="800" fill="#92400E" text-anchor="middle">Turns Feasibility Rejection to 5G Win</text>

    <!-- Card 5B: Logistics Dispatch & Engineer Assignment -->
    <rect x="14" y="310" width="316" height="250" rx="8" fill="#F8FAFC" stroke="#E2E8F0" stroke-width="1"/>
    <text x="24" y="337" font-size="13" font-weight="800" fill="#0F172A">Logistics &amp; Field Dispatch</text>
    <text x="24" y="364" font-size="11.5" font-weight="600" fill="#1E293B">• Delhivery Courier API Integration:</text>
    <text x="36" y="384" font-size="10.5" fill="#475569">Instant Waybill Generation (e.g. DL982341)</text>
    <text x="24" y="408" font-size="11.5" font-weight="600" fill="#1E293B">• Field Engineer Auto-Assignment:</text>
    <text x="36" y="428" font-size="10.5" fill="#475569">Assigned Lead Tech (e.g. Rahul Sharma)</text>
    <text x="36" y="446" font-size="10.5" fill="#475569">Direct 1-click customer call link</text>
    <text x="24" y="470" font-size="11" fill="#475569">• Automated SMS / WhatsApp Milestone Push</text>
    <rect x="24" y="500" width="296" height="42" rx="4" fill="#F1F5F9"/>
    <text x="172" y="518" font-size="10" font-weight="800" fill="#334155" text-anchor="middle">Guaranteed 48-Hour Activation</text>
    <text x="172" y="534" font-size="10" font-weight="600" fill="#64748B" text-anchor="middle">Down from 17.6-Day Industry Baseline</text>

    <!-- Card 5C: Partner Back-Office & ML Propensity Recovery -->
    <rect x="14" y="572" width="316" height="238" rx="8" fill="#FDF2F8" stroke="#FBCFE8" stroke-width="1"/>
    <text x="24" y="599" font-size="13" font-weight="800" fill="#9D174D">Partner Back-Office &amp; ML Rescue</text>
    <text x="24" y="626" font-size="11.5" font-weight="600" fill="#1E293B">• Unclosed Cart Recovery Queue:</text>
    <text x="36" y="646" font-size="10.5" fill="#475569">Tracks leads stalled at quote / KYC</text>
    <text x="24" y="670" font-size="11.5" font-weight="600" fill="#1E293B">• ML Propensity Score (0–100):</text>
    <text x="36" y="690" font-size="10.5" fill="#BE185D">Prioritizes high-intent leads to call first</text>
    <text x="24" y="712" font-size="11" fill="#475569">• Partner Co-Pilot Mode with Commission Split</text>
    <rect x="24" y="750" width="296" height="42" rx="4" fill="#FCE7F3"/>
    <text x="172" y="768" font-size="10" font-weight="800" fill="#9D174D" text-anchor="middle">Stretch Goal Implemented:</text>
    <text x="172" y="784" font-size="10" font-weight="600" fill="#BE185D" text-anchor="middle">Zero Lost Leads via Partner Tele-Rescue</text>
  </g>

  <!-- ==================== BOTTOM HORIZONTAL SLA & METRICS BANNER (y: 975 to 1055) ==================== -->
  <g transform="translate(50, 975)">
    <rect x="0" y="0" width="1820" height="80" rx="10" fill="#0F172A" filter="url(#shadowCard)"/>
    <rect x="0" y="0" width="6" height="80" rx="3" fill="#E40000"/>

    <!-- 5 Summary Metric Pills -->
    <g transform="translate(25, 16)">
      <text x="0" y="16" font-size="11" font-weight="700" fill="#94A3B8">VOICE LATENCY</text>
      <text x="0" y="38" font-size="18" font-weight="900" fill="#F87171">&lt; 800 ms</text>
      <text x="0" y="52" font-size="10" fill="#CBD5E1">Web Speech + Gemini STT</text>
    </g>
    <line x1="230" y1="15" x2="230" y2="65" stroke="#334155" stroke-width="1"/>

    <g transform="translate(255, 16)">
      <text x="0" y="16" font-size="11" font-weight="700" fill="#94A3B8">PRICING MATH</text>
      <text x="0" y="38" font-size="18" font-weight="900" fill="#60A5FA">0% Hallucination</text>
      <text x="0" y="52" font-size="10" fill="#CBD5E1">25 SKUs + 5% Rule Math</text>
    </g>
    <line x1="490" y1="15" x2="490" y2="65" stroke="#334155" stroke-width="1"/>

    <g transform="translate(515, 16)">
      <text x="0" y="16" font-size="11" font-weight="700" fill="#94A3B8">SMART KYC DURATION</text>
      <text x="0" y="38" font-size="18" font-weight="900" fill="#34D399">&lt; 60 Seconds</text>
      <text x="0" y="52" font-size="10" fill="#CBD5E1">Camera OCR + Auto Registry</text>
    </g>
    <line x1="775" y1="15" x2="775" y2="65" stroke="#334155" stroke-width="1"/>

    <g transform="translate(800, 16)">
      <text x="0" y="16" font-size="11" font-weight="700" fill="#94A3B8">LEAD TO ACTIVATION</text>
      <text x="0" y="38" font-size="18" font-weight="900" fill="#FBBF24">48 Hours</text>
      <text x="0" y="52" font-size="10" fill="#CBD5E1">Down from 17.6 Day Baseline</text>
    </g>
    <line x1="1060" y1="15" x2="1060" y2="65" stroke="#334155" stroke-width="1"/>

    <g transform="translate(1085, 16)">
      <text x="0" y="16" font-size="11" font-weight="700" fill="#94A3B8">ACQUISITION COST (CAC)</text>
      <text x="0" y="38" font-size="18" font-weight="900" fill="#F472B6">₹850 / SMB</text>
      <text x="0" y="52" font-size="10" fill="#CBD5E1">Down from ₹15,000 Field CAC</text>
    </g>
    <line x1="1340" y1="15" x2="1340" y2="65" stroke="#334155" stroke-width="1"/>

    <g transform="translate(1365, 16)">
      <text x="0" y="16" font-size="11" font-weight="700" fill="#94A3B8">STATUTORY COMPLIANCE</text>
      <text x="0" y="38" font-size="18" font-weight="900" fill="#A78BFA">100% DPDP Act</text>
      <text x="0" y="52" font-size="10" fill="#CBD5E1">SHA-256 Cryptographic Tokens</text>
    </g>
    <line x1="1620" y1="15" x2="1620" y2="65" stroke="#334155" stroke-width="1"/>

    <g transform="translate(1645, 16)">
      <text x="0" y="16" font-size="11" font-weight="700" fill="#94A3B8">PARTNER RESCUE</text>
      <text x="0" y="38" font-size="18" font-weight="900" fill="#FB7185">ML Propensity</text>
      <text x="0" y="52" font-size="10" fill="#CBD5E1">Zero Abandoned Cart Drops</text>
    </g>

  </g>

</svg>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"16:9 Architecture SVG generated: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_svg = os.path.join(base_dir, "architecture_diagram_16x9.svg")
    generate_16x9_architecture_svg(out_svg)

    # Convert to 300 DPI high-res PNG (exact 16:9 widescreen: 1920x1080 * 2 = 3840x2160)
    out_png = os.path.join(base_dir, "architecture_diagram_16x9.png")
    doc = fitz.open(out_svg)
    page = doc[0]
    # DPI 144 gives 3840x2160 4K ultra crisp 16:9
    pix = page.get_pixmap(dpi=144)
    pix.save(out_png)
    print(f"Rendered 16:9 PNG ({pix.width}x{pix.height}) at: {out_png}")

    # Also copy to frontend
    frontend_dir = os.path.join(base_dir, "frontend")
    if os.path.exists(frontend_dir):
        shutil.copyfile(out_svg, os.path.join(frontend_dir, "architecture_diagram_16x9.svg"))
        shutil.copyfile(out_png, os.path.join(frontend_dir, "architecture_diagram_16x9.png"))
        print("Copied 16:9 assets to frontend directory.")

    # Also copy to brain artifact directory for preview
    brain_dir = r"C:\Users\DELL\.gemini\antigravity\brain\189eb77b-9b1f-4f68-b2ff-1682279e819c"
    if os.path.exists(brain_dir):
        shutil.copyfile(out_png, os.path.join(brain_dir, "architecture_diagram_16x9.png"))
        print("Copied 16:9 PNG to brain artifact directory.")
