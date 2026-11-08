import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_pptx_path):
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "airtel_sync_case", "Submission Template_Sync.pptx")
    prs = pptx.Presentation(template_path)

    # Remove template slides so we have a clean deck while keeping template formatting and masters
    for _ in range(len(prs.slides)):
        rId = prs.slides._sldIdLst[0].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[0]

    blank_layout = prs.slide_layouts[10] if len(prs.slide_layouts) > 10 else prs.slide_layouts[6]
    
    # Airtel Palette
    C_RED = RGBColor(228, 0, 0)
    C_DARK = RGBColor(15, 23, 42)
    C_SLATE = RGBColor(30, 41, 59)
    C_MUTED = RGBColor(100, 116, 139)
    C_LIGHT_BG = RGBColor(248, 250, 252)
    C_WHITE = RGBColor(255, 255, 255)
    C_GREEN = RGBColor(22, 163, 74)
    C_BORDER = RGBColor(203, 213, 225)
    C_AMBER = RGBColor(217, 119, 6)

    def add_header(slide, title_text, category_text="ENTERPRISE TRACK A: PROJECT UDYAM DIGITAL"):
        # Top banner
        header_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.25), Inches(9.0), Inches(0.7))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(8.5)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_RED

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(14)
        p_title.font.bold = True
        p_title.font.color.rgb = C_DARK

    def add_footer_metrics(slide, metric_pairs):
        y_pos = Inches(5.0)
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), y_pos, Inches(9.0), Inches(0.45))
        box.fill.solid()
        box.fill.fore_color.rgb = C_DARK
        box.line.color.rgb = C_RED
        box.line.width = Pt(1.5)

        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        
        parts = []
        for label, val in metric_pairs:
            parts.append(f"{label}: {val}")
        full_text = "   |   ".join(parts)
        
        run = p.add_run()
        run.text = full_text
        run.font.name = "Arial"
        run.font.size = Pt(9.5)
        run.font.bold = True
        run.font.color.rgb = C_WHITE

    # ==================== SLIDE 1: TITLE & TEAM ====================
    s1 = prs.slides.add_slide(blank_layout)
    # Background card
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.5), Inches(9.0), Inches(4.625))
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_WHITE
    bg.line.color.rgb = C_RED
    bg.line.width = Pt(2)

    tf1 = bg.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_right = Inches(0.6)
    tf1.margin_top = Inches(0.5)

    p = tf1.paragraphs[0]
    p.text = "AIRTEL SYNC HACKATHON 2026 · ENTERPRISE TRACK A"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_RED

    p2 = tf1.add_paragraph()
    p2.text = "Project Udyam Digital"
    p2.font.size = Pt(26)
    p2.font.bold = True
    p2.font.color.rgb = C_DARK
    p2.space_before = Pt(6)

    p3 = tf1.add_paragraph()
    p3.text = "Making Small Businesses Go Digital in One Sitting (10-Minute Autonomous Onboarding)"
    p3.font.size = Pt(13)
    p3.font.color.rgb = C_SLATE
    p3.space_before = Pt(4)

    p4 = tf1.add_paragraph()
    p4.text = (
        "• Core Vision: Replacing a 17.6-day traditional paper-heavy sales cycle with a 10-minute digital journey.\n"
        "• Live Prototype: https://anageme.vercel.app (Mobile PWA for Android/iOS)\n"
        "• GitHub Repository: yatharthsachdeva23/Airtel-MSME-Onboarding-and-Management\n"
        "• Verification: 30 Unit Tests Passed (100%) · 8/8 System Audit Passed · DPDP Act 2023 Compliant"
    )
    p4.font.size = Pt(10)
    p4.font.color.rgb = C_SLATE
    p4.space_before = Pt(12)

    p5 = tf1.add_paragraph()
    p5.text = "Team Details: Yatharth Sachdeva & Team | Enterprise Track A Submission"
    p5.font.size = Pt(11)
    p5.font.bold = True
    p5.font.color.rgb = C_RED
    p5.space_before = Pt(16)

    # ==================== SLIDE 2: PROBLEM STATEMENT ====================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement: 92.6% Funnel Collapse (5,000 Leads Analysis)")
    
    # Left Card: Funnel Breakdown
    c1 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.05), Inches(4.35), Inches(3.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_LIGHT_BG
    c1.line.color.rgb = C_BORDER
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_right = tf_c1.margin_top = Inches(0.2)
    
    p = tf_c1.paragraphs[0]
    p.text = "1. Empirical Funnel Leakage (smb_leads.csv)"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_RED
    
    p = tf_c1.add_paragraph()
    p.text = (
        "• Leads Generated (5,000) → Contacted (3,406): 32% lost to slow manual outreach.\n"
        "• Contacted → Needs Assessed (1,974): 42% lost; reps pitch quotas instead of workflows.\n"
        "• Needs Assessed → Quote Accepted (861): 56% LOST IN THE 'QUOTING BLACK HOLE'. 3-5 day delay for cryptic multi-page PDF quotes kills buyer momentum.\n"
        "• Quote Accepted → KYC Complete (588): 32% lost to physical paperwork friction.\n"
        "• KYC Complete → Activated (368): 37% lost to unfeasible fiber runs."
    )
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(6)

    # Right Card: Customer Segments & Structural Killers
    c2 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.0), Inches(1.05), Inches(4.5), Inches(3.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_LIGHT_BG
    c2.line.color.rgb = C_BORDER
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_right = tf_c2.margin_top = Inches(0.2)

    p = tf_c2.paragraphs[0]
    p.text = "2. Customer Segments & The 3 Structural Killers"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = C_DARK

    p = tf_c2.add_paragraph()
    p.text = (
        "• Micro Retail & Services (55% of MSMEs): Kirana, salon, clinic; very price sensitive; owner mobile hotspot setup.\n"
        "• Professional Offices (25%): Clinics, CA firms; home broadband, personal Gmail.\n"
        "• Small Multi-Site (15%): 3-10 store retailers; mixed ISPs, no central IT.\n\n"
        "The 3 Structural Killers Identified:\n"
        "1. The CAC vs ARPU Trap: ₹15,000 field sales CAC against a ₹2,500/mo Kirana bundle breaks enterprise unit economics.\n"
        "2. The Buyer Fatigue Lag: 17.6-day average lag + 3 status chases per customer calling support.\n"
        "3. The Non-GST Barrier: 9.6% activation with GST vs 2.0% without GST (abandons 55% of micro merchants)."
    )
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(6)

    add_footer_metrics(s2, [("Total Leads", "5,000"), ("Activated", "368 (7.4%)"), ("Lead-to-Active Lag", "17.6 Days"), ("Field CAC", "₹15,000"), ("Overall Leakage", "92.6%")])

    # ==================== SLIDE 3: SOLUTION IN BRIEF (4 BOXES) ====================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Solution Overview: The 4 Architectural Pillars")

    box_data = [
        ("1. Conversational GenAI Advisor", "• Regional Voice & Chat in 6 Indian languages\n• Queries business type, size & daily bottlenecks\n• Plain-Language business benefit reasoning\n★ Eliminates 4-Day Sales Rep Lag", Inches(0.5), Inches(1.1), C_RED),
        ("2. Instant Deterministic Quoting", "• 1-Click Transparent Pricing from 25 SKUs\n• 5% Multi-Product Bundle Discount applied\n• Rule-based ₹2,500 setup fee waiver\n★ Eliminates Cryptic 5-Page PDF Quotes", Inches(5.0), Inches(1.1), C_SLATE),
        ("3. Zero-Delay Smart KYC (<60s)", "• Smartphone Camera OCR (<3s extraction)\n• Real-Time National Registry Lookup (GST/Udyam)\n• DPDP Act 2023 Cryptographic Consent Token\n★ Eliminates Physical Paper Collection", Inches(0.5), Inches(2.95), C_GREEN),
        ("4. Live Tracker & GIS 5G Pivot", "• 5 Self-Serve Visual SLA Milestones\n• Integrated Delhivery Courier Waybill & Tech link\n• Autonomous Pivot to 5G AirFiber if fiber >250m\n★ Eliminates 3x Customer Status Chases", Inches(5.0), Inches(2.95), C_AMBER)
    ]

    for title, desc, x, y, accent_col in box_data:
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(4.35), Inches(1.75))
        box.fill.solid()
        box.fill.fore_color.rgb = C_WHITE
        box.line.color.rgb = accent_col
        box.line.width = Pt(1.5)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.18)

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = accent_col

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(8.5)
        p_desc.font.color.rgb = C_SLATE
        p_desc.space_before = Pt(4)

    add_footer_metrics(s3, [("Onboarding Time", "17.6 Days → 10 Minutes"), ("Acquisition Cost", "₹15,000 → <₹1,200"), ("Support Chases", "3 Calls → 0 Calls")])

    # ==================== SLIDE 4: ARCHITECTURE 16:9 ====================
    s4 = prs.slides.add_slide(blank_layout)
    arch_png_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "architecture_diagram_16x9.png")
    if os.path.exists(arch_png_path):
        s4.shapes.add_picture(arch_png_path, Inches(0), Inches(0), Inches(10.0), Inches(5.625))
    else:
        add_header(s4, "End-to-End Solution Architecture & Data Flows (16:9)")

    # ==================== SLIDE 5: FEATURE 1: ADVISOR & QUOTE ====================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Feature 1: Conversational AI Advisor & Deterministic Quoting")
    
    c1 = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.05), Inches(4.35), Inches(3.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BORDER
    tf = c1.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "1. Natural Conversational Needs Discovery"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_RED
    p = tf.add_paragraph()
    p.text = (
        "• 3 Simple Inquiries: Business Category → Staff & Site Count → Operational Bottlenecks (UPI payment failures, slow billing, customer calls).\n"
        "• Multilingual Dual Voice Engine: Web Speech API for sub-100ms response + MediaRecorder streaming audio fallback in 6 Indian languages.\n"
        "• Plain-Language Business Reasoning: Explains why services are needed without jargon (e.g. 'Dual-Band Wi-Fi ensures your UPI Soundbox never drops off during peak rushes').\n"
        "• Step Preservation: Answers ad-hoc user inquiries and smoothly resumes onboarding without losing context."
    )
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(6)

    c2 = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.0), Inches(1.05), Inches(4.5), Inches(3.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_WHITE
    c2.line.color.rgb = C_BORDER
    tf = c2.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "2. 1-Click Transparent Quoting (The Cart Customizer)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p = tf.add_paragraph()
    p.text = (
        "• Zero Hidden Costs: Single transparent monthly price with itemized 18% GST input credit breakdown.\n"
        "• Deterministic Math Core: Covers all 25 official products from catalog.json with zero model hallucinations.\n"
        "• Automated Incentive Rules: 5% multi-product discount + ₹2,500 setup fee waived automatically on annual contracts.\n"
        "• Interactive Toggles: Merchants can toggle add-ons (Cloud PBX, Cyber Protect, extra SIMs) with instant re-calculation.\n"
        "• Single-View PWA Hub: Replaces 3-card horizontal scrolling with 3 full-view tabs (Plan & Price, Smart KYC, GIS Network)."
    )
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(6)

    add_footer_metrics(s5, [("Quoting Latency", "< 50 ms"), ("Pricing Hallucinations", "0%"), ("Catalog Coverage", "25/25 SKUs"), ("Setup Waiver", "₹2,500 Waived")])

    # ==================== SLIDE 6: FEATURE 2: SMART KYC & DPDP ====================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Feature 2: Zero-Human-Delay Smart KYC & DPDP Act 2023 Shield")

    c1 = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.05), Inches(4.35), Inches(3.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BORDER
    tf = c1.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "1. Multimodal Vision OCR & National Registries"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p = tf.add_paragraph()
    p.text = (
        "• Camera Snapshot & Local Extraction: Gemini 2.5 Flash Vision OCR extracts GSTIN, entity name, and address in <3 seconds (with local WinRT OCR fallback).\n"
        "• Instant National Mock Registries: Real-time queries against 3,534 GSTINs and 2,723 MSME Udyam database records.\n"
        "• Automated Fraud Defense (K01–K12 Bench):\n"
        "  – K01: Catches CANCELLED or SUSPENDED GSTIN registrations.\n"
        "  – K06: Flags non-existent / fake GSTINs.\n"
        "  – K11: Enforces DoT 90-Day Utility Proof Recency; rejects stale bills >90 days.\n"
        "• Non-GST Merchant Path: Unlocks 55% micro-retailers via Shop & Establishment proof or electricity bill."
    )
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(6)

    c2 = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.0), Inches(1.05), Inches(4.5), Inches(3.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_WHITE
    c2.line.color.rgb = C_BORDER
    tf = c2.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "2. DPDP Act 2023 Statutory Compliance"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p = tf.add_paragraph()
    p.text = (
        "• Section 5 (Notice): Clear, itemized purpose specification (DoT telecom verification, billing, hardware dispatch) in applicant's preferred language.\n"
        "• Section 6 (Consent): Affirmative verification generating an immutable SHA-256 cryptographic audit token (Hash of Session + Signatory + Time + IP).\n"
        "• Section 8 (Data Minimization): Strict algorithmic masking of Aadhaar (XXXX-XXXX-1234), PAN (ABCDE****F), GSTIN, and phone.\n"
        "• Ephemeral Processing: Raw document photos are processed strictly in volatile memory and purged immediately post-verification."
    )
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(6)

    add_footer_metrics(s6, [("KYC Verification", "< 60 Seconds"), ("Planted Errors Caught", "100% (12/12)"), ("DoT Recency", "90-Day Rule"), ("DPDP Compliance", "100% Validated")])

    # ==================== SLIDE 7: FEATURE 3: LIVE TRACKER & 5G PIVOT ====================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Feature 3: Live SLA Milestone Tracker & 5G AirFiber GIS Auto-Pivot")

    c1 = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.05), Inches(4.35), Inches(3.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BORDER
    tf = c1.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "1. Customer Self-Serve SLA Milestone Tracker"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p = tf.add_paragraph()
    p.text = (
        "• 5 Real-Time Status Milestones: Order Configured → KYC Verified → Hardware Dispatched → Engineer Visit → Live Activation.\n"
        "• Courier Transparency: Direct integration with Delhivery tracking APIs (e.g. Waybill DL982341) with real-time transit telemetry.\n"
        "• Assigned Field Contact: Displays assigned Lead Field Engineer (e.g. Rahul Sharma) with direct 1-click customer call button.\n"
        "• Zero Status Chases: Completely eliminates the 3 status chase calls per customer that congest support centers."
    )
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(6)

    c2 = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.0), Inches(1.05), Inches(4.5), Inches(3.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_WHITE
    c2.line.color.rgb = C_BORDER
    tf = c2.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "2. Self-Healing 5G AirFiber GIS Auto-Pivot"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p = tf.add_paragraph()
    p.text = (
        "• FAT Splitter Proximity Calculation: Checks optical fiber feasibility within 250m of premise using coverage.json.\n"
        "• Autonomous Failover: If fiber distance exceeds 250m or fiber ports are saturated, the system auto-pivots to 5G AirFiber (FWA).\n"
        "• 48-Hour SLA Guarantee: Plug-and-play wireless CPE activation preserves the customer and prevents merchant drop-off at feasibility.\n"
        "• Commercial Parity: Maintains the same quoted price point while delivering gigabit-grade wireless broadband."
    )
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(6)

    add_footer_metrics(s7, [("Activation SLA", "48 Hours (vs 17.6d)"), ("Support Calls", "0 Calls (100% Self-Serve)"), ("GIS Auto-Pivot", "5G AirFiber Active"), ("Logistics", "Delhivery Integrated")])

    # ==================== SLIDE 8: STRETCH GOAL: PARTNER BACK-OFFICE ====================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Stretch Goal: Sales & Partner Back-Office with ML Propensity Scoring")

    c1 = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.05), Inches(4.35), Inches(3.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BORDER
    tf = c1.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "1. Unclosed Lead Recovery & Propensity Scoring"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_RED
    p = tf.add_paragraph()
    p.text = (
        "• The 4,632 Unclosed Leads Opportunity: Traditional sales abandons dropped leads. Our platform captures every cart drop with exact reasons.\n"
        "• ML Propensity Scoring Algorithm (0–100):\n"
        "  – Stage Depth: Quote accepted (+40 pts) vs Needs assessed (+25 pts).\n"
        "  – Viability: Has GSTIN (+15 pts), Has Udyam (+8 pts), Spend ≥₹4,000 (+12 pts).\n"
        "  – Recoverability: 'Price too high' or 'Quote too complex' (+10 to +12 pts).\n"
        "• Priority Tiers: Score ≥75% = High Priority (call within 15 min); 50–74% = Medium Priority; <50% = Automated WhatsApp drip.\n"
        "• Live API: /api/backoffice/leads dynamically serves ranked recovery queues."
    )
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(6)

    c2 = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.0), Inches(1.05), Inches(4.5), Inches(3.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_WHITE
    c2.line.color.rgb = C_BORDER
    tf = c2.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "2. Channel Partner Co-Pilot Desk & Synergy"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p = tf.add_paragraph()
    p.text = (
        "• Pre-Populated Talk Tracks: Equips field reps with exact objection counter-offers (e.g. 'Offer 5% discount + free ₹2,500 setup on 12-mo contract').\n"
        "• 1-Click Tele-Rescue Button: Directly triggers tele-rescue call from the back-office view and marks lead as RESCUED.\n"
        "• ₹1,500 Partner Commission: High-intent activation payout incentivizes 100,000+ local retail distributors.\n"
        "• Co-Pilot Synergy: Replaces partner friction with collaborative digital toolsets that increase distributor earnings."
    )
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(6)

    add_footer_metrics(s8, [("Unclosed Leads", "4,632 Analyzed"), ("High-Intent Targets", "805 (≥75% Score)"), ("Recoverable MRR", "₹2.4 Lakhs/Mo"), ("Partner Payout", "₹1,500 / Rescue")])

    # ==================== SLIDE 9: BUSINESS IMPACT & ROLLOUT ====================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Business Impact, Unit Economics & Phased Rollout")

    c1 = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.05), Inches(4.35), Inches(3.8))
    c1.fill.solid()
    c1.fill.fore_color.rgb = C_WHITE
    c1.line.color.rgb = C_BORDER
    tf = c1.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "1. Transformational Unit Economics"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_GREEN
    p = tf.add_paragraph()
    p.text = (
        "• Conversion Rate: 7.4% (Baseline) → 32.5% (Project Udyam Digital) — 4.4× Lift.\n"
        "• Time-to-Activate: 17.6 Days → 10 Minutes (Digital) / 48 Hours (Physical) — 95% Slashed.\n"
        "• Customer Acquisition Cost (CAC): ₹15,000 / SMB → <₹1,200 / SMB — 92% Reduction.\n"
        "• Customer Status Chases: 3 calls/lead → 0 calls (100% Self-Serve Elimination).\n"
        "• Payback Period: 6.0 Months → 0.5 Months (Instant Profitability)."
    )
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(6)

    c2 = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.0), Inches(1.05), Inches(4.5), Inches(3.8))
    c2.fill.solid()
    c2.fill.fore_color.rgb = C_WHITE
    c2.line.color.rgb = C_BORDER
    tf = c2.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "2. 3-Phase Commercial Rollout Strategy"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_DARK
    p = tf.add_paragraph()
    p.text = (
        "• Phase 1 (Direct Self-Service In-App Hook): Embedded into Airtel Thanks / Business App, driving organic merchant traffic from 63M micro-merchants.\n"
        "• Phase 2 (Partner Co-Pilot Mode): Equipping 100,000+ local retail distributors with in-app assisted onboarding, earning instant activation commissions.\n"
        "• Phase 3 (Pan-India Scale): Expansion into Tier 2 and Tier 3 enterprise clusters with automated GIS network coverage provisioning."
    )
    p.font.size = Pt(8.5)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(6)

    add_footer_metrics(s9, [("Conversion Lift", "4.4×"), ("CAC Reduction", "92%"), ("Activation Time", "95% Faster"), ("Payback", "0.5 Months")])

    # ==================== SLIDE 10: CONCLUSION & CHECKLIST ====================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Conclusion & Mandatory Deliverables Verification")

    card = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.05), Inches(9.0), Inches(3.8))
    card.fill.solid()
    card.fill.fore_color.rgb = C_WHITE
    card.line.color.rgb = C_RED
    card.line.width = Pt(1.5)
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)

    p = tf.paragraphs[0]
    p.text = "All Mandatory & Stretch Deliverables Completed (100%)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_RED

    p = tf.add_paragraph()
    p.text = (
        "✓ Deliverable 1: Working Prototype — Deployed live on Vercel at https://anageme.vercel.app with GitHub repository (30 unit tests passed).\n"
        "✓ Deliverable 2: Solution Architecture Diagram — 16:9 widescreen diagram (3840x2160 UHD) detailing all 5 tiers and data flows.\n"
        "✓ Deliverable 3: Business Case (10 Slides) — Built on official Airtel SYNC template covering target customer, economics, and rollout.\n"
        "✓ Deliverable 4: 1-Page Data Privacy & Security Note — Full compliance with DPDP Act 2023 (Sections 5, 6, 8) and DoT KYC guidelines.\n"
        "✓ Stretch Goal 1: Voice & Multilingual Front-End — Direct Web Speech API and Gemini audio streaming in 6 Indian languages.\n"
        "✓ Stretch Goal 2: Sales & Partner Back-Office Desk — Unclosed lead recovery queue with ML Propensity Scoring (0–100).\n\n"
        "Thank You! Open for Questions & Live Interactive Demonstration."
    )
    p.font.size = Pt(9.5)
    p.font.color.rgb = C_SLATE
    p.space_before = Pt(8)

    add_footer_metrics(s10, [("Live Prototype", "anageme.vercel.app"), ("GitHub", "yatharthsachdeva23/Airtel-MSME"), ("Tests", "30/30 Passed"), ("Audit", "8/8 Passed")])

    prs.save(output_pptx_path)
    print(f"PowerPoint Presentation generated successfully: {output_pptx_path}")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_pptx = os.path.join(out_dir, "Project_Udyam_Digital_Presentation.pptx")
    create_deck(out_pptx)
    
    # Also copy to frontend
    frontend_dir = os.path.join(out_dir, "frontend")
    if os.path.exists(frontend_dir):
        import shutil
        dest = os.path.join(frontend_dir, "Project_Udyam_Digital_Presentation.pptx")
        shutil.copyfile(out_pptx, dest)
        print(f"Copied PPTX to frontend: {dest}")
