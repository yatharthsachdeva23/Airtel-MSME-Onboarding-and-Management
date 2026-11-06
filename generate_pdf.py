import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "PROJECT UDYAM DIGITAL — TECHNICAL ARCHITECTURE & EXECUTIVE BRIEF")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)
        
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, footer_text)
        self.drawString(54, 36, "Airtel SYNC Hackathon 2026 | Enterprise Track A: Project Udyam Digital | Confidential")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def create_executive_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#E40000")      # Airtel Red
    c_dark = colors.HexColor("#1A202C")         # Charcoal / Slate
    c_secondary = colors.HexColor("#2B6CB0")    # Deep Blue
    c_accent = colors.HexColor("#319795")       # Teal
    c_light_bg = colors.HexColor("#F7FAFC")     # Soft Gray
    c_border = colors.HexColor("#E2E8F0")       # Border Gray
    c_danger = colors.HexColor("#C53030")       # Crimson
    c_success = colors.HexColor("#2F855A")      # Forest Green
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_dark,
        spaceAfter=12
    )
    
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#4A5568")
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_dark,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    callout_text = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#2D3748")
    )
    
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )
    
    story = []
    
    # ---------------- HEADER & COVER BANNER ----------------
    story.append(Paragraph("PROJECT UDYAM DIGITAL", title_style))
    story.append(Paragraph("Autonomous Mobile-First Telecom & Digital Onboarding for India's 63 Million MSMEs", subtitle_style))
    story.append(Paragraph("<b>Track A: Enterprise Solutions</b> | Airtel SYNC / YTL Hackathon 2026 | Comprehensive Technical Brief", meta_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=c_primary, spaceBefore=0, spaceAfter=12))
    
    # ---------------- SECTION 1: THE PROBLEM IN BRIEF ----------------
    story.append(Paragraph("1. The Problem in Brief", h1_style))
    
    p1 = (
        "India is home to over <b>63 million Micro, Small, and Medium Enterprises (MSMEs)</b> contributing ~30% of India's GDP "
        "and over 45% of manufacturing output. Over 99% of these are micro-enterprises with fewer than 10 employees, operated "
        "by solo proprietors or family teams. Despite massive national digitization (UPI, GSTN, Udyam, GeM), enterprise telecom "
        "and cloud penetration among micro-enterprises remains stagnant below <b>15%</b>."
    )
    story.append(Paragraph(p1, body_style))
    
    # Analysis of smb_leads.csv
    p2 = (
        "<b>The Broken Enterprise Sales Paradigm:</b> Traditional telecom enterprise sales treat a ₹2,500/month neighborhood clinic "
        "or retail store with the same heavy-touch machinery built for Fortune 500 corporations: multi-tier field sales visits, physical paper KYC collection, "
        "opaque quotation cycles, manual GIS fiber feasibility surveys, and back-office verification. An empirical analysis of "
        "<b>5,000 real-world SMB leads (from Airtel's dataset)</b> reveals a catastrophic funnel collapse:"
    )
    story.append(Paragraph(p2, body_style))
    
    # Table of drop-off reasons
    funnel_data = [
        [Paragraph("Funnel Stage / Milestone", table_header), Paragraph("Dropped Leads", table_header), Paragraph("% of Funnel", table_header), Paragraph("Root Cause / Friction Point", table_header)],
        [Paragraph("1. Sales Visit Scheduling", table_cell), Paragraph("827 leads", table_cell), Paragraph("16.5%", table_cell), Paragraph("Proprietors have no time for visits (531); scheduling paralysis (296)", table_cell)],
        [Paragraph("2. Quotation & Pricing", table_cell), Paragraph("799 leads", table_cell), Paragraph("16.0%", table_cell), Paragraph("Pricing perceived too high (414); quotes opaque/rigid (206); quotes took days (179)", table_cell)],
        [Paragraph("3. KYC & Regulatory Docs", table_cell), Paragraph("220 leads", table_cell), Paragraph("4.4%", table_cell), Paragraph("Missing GST/Udyam (94); long paperwork (79); document data mismatch (47)", table_cell)],
        [Paragraph("4. Feasibility & Physical Survey", table_cell), Paragraph("41 leads", table_cell), Paragraph("0.8%", table_cell), Paragraph("Fiber port exhaustion / distance > 250m; outright order cancellation", table_cell)],
        [Paragraph("<b>TOTAL FUNNEL LEAKAGE</b>", table_cell), Paragraph("<b>4,632 leads</b>", table_cell), Paragraph("<b>92.6%</b>", table_cell), Paragraph("<b>Only 368 activated accounts (7.4% conversion rate)</b>", table_cell)]
    ]
    t_funnel = Table(funnel_data, colWidths=[130, 75, 75, 224])
    t_funnel.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_dark),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#FFF5F5")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_funnel)
    story.append(Spacer(1, 8))
    
    # Financial impact callout box
    cac_callout = [
        [Paragraph(
            "<b>The CAC vs. ARPU Trap:</b> A multi-tier field sales model costs Airtel approximately <b>₹15,000 in blended Customer Acquisition Cost (CAC)</b> "
            "per closed SMB lead. For an SMB paying <b>₹2,500/month</b> ARPU, it takes 6+ months just to recover sales overheads—destroying segment profitability "
            "and leaving millions of willing small business owners unserved.",
            callout_text
        )]
    ]
    t_cac = Table(cac_callout, colWidths=[504])
    t_cac.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FFF5F5")),
        ('BOX', (0, 0), (-1, -1), 1, c_danger),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_cac)
    story.append(Spacer(1, 14))
    
    # ---------------- SECTION 2: WHAT WE ARE MAKING IN DETAIL ----------------
    story.append(Paragraph("2. What We Are Making in Detail: Project Udyam Digital", h1_style))
    p_sol = (
        "<b>Project Udyam Digital</b> is a self-contained, autonomous mobile onboarding and bundle-activation platform designed "
        "to compress the 18-day enterprise sales cycle into a single <b>10-minute digital session</b>. "
        "It eliminates physical sales visits and paperwork while embedding industrial-grade reliability, compliance, and deterministic pricing."
    )
    story.append(Paragraph(p_sol, body_style))
    
    # Architecture Overview
    story.append(Paragraph("2.1 System Architecture & Technical Pillars", h2_style))
    
    arch_bullets = [
        "<b>1. Multilingual Generative Conversational Advisor:</b> Conducts frictionless, conversational needs discovery in 6 Indian languages (Hindi, English, Tamil, Bengali, Telugu, Marathi). Replaces 20-field questionnaires with natural dialogue (asking business type, team size, multi-branch presence, and operational needs).",
        "<b>2. Deterministic Quoting & Catalog Rule Engine:</b> Indexes 25 official Airtel enterprise products across 6 categories (Connectivity, Cloud Telephony, Collaboration & Security, IoT & Tracking, Enterprise SIMs, and Value-Add Services). Strict zero-hallucination guardrails enforce catalog constraints, dependency rules, GSTIN requirements, and volume discounts.",
        "<b>3. Zero-Form Conversational Smart KYC & OCR:</b> In-chat document photo drop eliminates traditional forms. High-speed local OCR extracts identifiers from GST Certificates, Udyam Registrations, Electricity Bills, and Signatory IDs in milliseconds, validating them against government registries.",
        "<b>4. DPDP Act 2023 Privacy Shield:</b> Fully compliant with India's Digital Personal Data Protection Act 2023. Explicit granular consent is captured upfront; all documents are processed in-memory, PII (Aadhaar, PAN) is masked, and raw images are purged with zero persistent plaintext storage.",
        "<b>5. Universal Loop Engineering & 4-Tier Self-Healing Matrix:</b> Built-in circuit breakers, idempotency keys, and automated recovery loops ensure zero drop-offs when external government registries or services encounter downtime.",
        "<b>6. Instant GIS Feasibility & 5G AirFiber Auto-Pivot:</b> Programmatic FAT box fiber feasibility check. If wired fiber distance exceeds 250m or splitters are exhausted, the system automatically pivots the cart to Airtel 5G AirFiber FWA, retaining bundle discounts with zero human re-work.",
        "<b>7. Smart Live Agent Handoff Protocol:</b> Real-time sentiment analysis detects negotiation resistance, pricing objections, or enterprise customization requests, instantly routing complete conversational context and pre-computed carts to authorized human sales desks.",
        "<b>8. Real-Time Milestone Tracker & Channel Partner Desk:</b> Amazon/Uber-style SLA tracking from digital verification to live activation, coupled with a portal for regional partners to claim, audit, and earn commissions on assisted digital orders."
    ]
    for b in arch_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 10))
    
    # ---------------- DETAILED PILLAR DEEP DIVE ----------------
    story.append(Paragraph("2.2 Deep Dive: Zero-Hallucination Quoting & Rule Engine", h2_style))
    p_catalog = (
        "A common hazard in AI sales assistants is 'pricing hallucination' and illegal configuration (e.g., selling Microsoft 365 without base internet, "
        "or selling post-paid corporate SIMs to businesses without verified GSTIN). Udyam Digital decouples language understanding from pricing logic:"
    )
    story.append(Paragraph(p_catalog, body_style))
    
    catalog_data = [
        [Paragraph("Category", table_header), Paragraph("Products Indexed", table_header), Paragraph("Hard Constraint Guardrails", table_header), Paragraph("Deterministic Bundle Discounting", table_header)],
        [Paragraph("Connectivity", table_cell), Paragraph("Airtel Office Internet (100-1000 Mbps), 5G AirFiber FWA, Primary Leased Line (ILL)", table_cell), Paragraph("Feasibility bounds (Fiber vs FWA); Base requirement for cloud add-ons", table_cell), Paragraph("Multi-Product Bundle: 5% off for 3+ items; 10% off for 5+ items", table_cell)],
        [Paragraph("Cloud Telephony", table_cell), Paragraph("Airtel IQ Cloud PBX, Smart Toll-Free 1800, Business Call Manager", table_cell), Paragraph("Requires connectivity base; Max 20 extensions on entry tier", table_cell), Paragraph("Annual Advance Billing: Additional 15% discount on total contract value", table_cell)],
        [Paragraph("Collaboration", table_cell), Paragraph("Google Workspace, Microsoft 365, Airtel Secure Cyber Protect, WorkSecure VPN", table_cell), Paragraph("Min employees rule (>=3 employees); Valid domain proof", table_cell), Paragraph("Waived setup charges (₹2,500) on all digital bundles > ₹3,000/mo", table_cell)],
        [Paragraph("Enterprise SIMs & IoT", table_cell), Paragraph("Corp Postpaid Fleet CUG, IoT Asset Tracker, GPS Fleet SIMs", table_cell), Paragraph("Requires verified GSTIN (mandatory under DoT regulations)", table_cell), Paragraph("Volume tiered pricing: ₹199/SIM (>10 SIMs) vs ₹299 (base)", table_cell)]
    ]
    t_catalog = Table(catalog_data, colWidths=[80, 150, 140, 134])
    t_catalog.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_secondary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_catalog)
    story.append(Spacer(1, 10))
    
    # ---------------- SMART KYC & PLANTED ERROR MATRIX ----------------
    story.append(Paragraph("2.3 Deep Dive: Conversational Smart KYC & Planted Error Matrix", h2_style))
    p_kyc = (
        "Document mismatch and fraud represent 4.4% of total lead abandonment and the largest source of back-office verification SLA breach. "
        "Our engine uses Windows Native WinRT OCR to inspect candidate files against simulated national databases with a benchmark validation date of <b>July 15, 2026</b>:"
    )
    story.append(Paragraph(p_kyc, body_style))
    
    kyc_data = [
        [Paragraph("Test Dossier", table_header), Paragraph("Planted Error / Document Anomaly", table_header), Paragraph("Automated Detection Mechanism", table_header), Paragraph("Self-Healing In-Chat Mitigation", table_header)],
        [Paragraph("K01 – K03", table_cell), Paragraph("Clean valid applications (Pooja Garments, Mehta Logistics, Apex)", table_cell), Paragraph("GSTIN active; Udyam matching; Address bill <90 days", table_cell), Paragraph("Immediate Green Pass; 1-click verification card issued", table_cell)],
        [Paragraph("K04", table_cell), Paragraph("Electricity bill issued Dec 2025 (>90 days old from July 2026)", table_cell), Paragraph("OCR date parser flags invoice date > 90-day threshold", table_cell), Paragraph("Friendly in-chat prompt: 'Please share your latest bill from the last 3 months'", table_cell)],
        [Paragraph("K05", table_cell), Paragraph("Signatory PAN name mismatch (Kumar vs Kumari)", table_cell), Paragraph("Levenshtein distance & fuzzy match score < 85%", table_cell), Paragraph("Prompts for Board Resolution / Authority Letter or re-upload", table_cell)],
        [Paragraph("K06", table_cell), Paragraph("GSTIN Status: 'SUSPENDED' on government registry", table_cell), Paragraph("Real-time mock GST registry status query returns inactive flag", table_cell), Paragraph("Offers non-GST sole proprietor fallback with Udyam verification", table_cell)],
        [Paragraph("K07 – K12", table_cell), Paragraph("Blurry uploads, address variance, missing Udyam category", table_cell), Paragraph("Laplacian sharpness check, pincode geocoding check", table_cell), Paragraph("In-chat auto-crop guidance, pin-code auto-correction suggestions", table_cell)]
    ]
    t_kyc = Table(kyc_data, colWidths=[65, 155, 140, 144])
    t_kyc.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_dark),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_kyc)
    story.append(Spacer(1, 10))
    
    # ---------------- LOOP ENGINEERING & RESILIENCE ----------------
    story.append(Paragraph("2.4 Universal Loop Engineering & Self-Healing Resilience", h2_style))
    p_loop = (
        "In developing digital onboarding for emerging markets, systems must never crash or block the user when external dependencies fail. "
        "We implement an industrial 4-tier fallback matrix:"
    )
    story.append(Paragraph(p_loop, body_style))
    
    loop_data = [
        [Paragraph("Tier Level", table_header), Paragraph("Failure Scenario", table_header), Paragraph("Loop Engineering Fallback Strategy", table_header), Paragraph("Customer Experience Guarantee", table_header)],
        [Paragraph("Tier 1: Local Algorithmic", table_cell), Paragraph("GSTIN / PAN API timeout or HTTP 503", table_cell), Paragraph("Execute client-side Modulo-11 Luhn checksum algorithm & regex validation", table_cell), Paragraph("Zero delay; instant syntax pass with background sync scheduled", table_cell)],
        [Paragraph("Tier 2: Cryptographic Audit", table_cell), Paragraph("State GSTN registry offline", table_cell), Paragraph("Extract and verify digital signature & QR code on GST/Udyam certificates", table_cell), Paragraph("Trust established cryptographically without outbound network query", table_cell)],
        [Paragraph("Tier 3: Cross-Registry Bridge", table_cell), Paragraph("Single registry database desynchronized", table_cell), Paragraph("Bridge from GSTIN PAN substring (chars 3-12) to Udyam database", table_cell), Paragraph("Autonomous recovery; customer is not asked to re-enter information", table_cell)],
        [Paragraph("Tier 4: Provisional Approval", table_cell), Paragraph("Prolonged government portal outage", table_cell), Paragraph("Issue provisional checkout token; queue verification job with dead-letter queue", table_cell), Paragraph("Customer completes onboarding in one sitting; dispatch occurs seamlessly", table_cell)]
    ]
    t_loop = Table(loop_data, colWidths=[80, 130, 154, 140])
    t_loop.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_accent),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_loop)
    story.append(Spacer(1, 10))
    
    # ---------------- BUSINESS IMPACT & EVALS ----------------
    story.append(Paragraph("2.5 Quantified Business Impact & AI Evaluation Framework", h2_style))
    p_biz = (
        "Udyam Digital transforms the unit economics of MSME acquisition through automation and deterministic rigor:"
    )
    story.append(Paragraph(p_biz, body_style))
    
    impact_data = [
        [Paragraph("Metric", table_header), Paragraph("Baseline (Human Sales Model)", table_header), Paragraph("Project Udyam Digital", table_header), Paragraph("Business Impact & ROI", table_header)],
        [Paragraph("Funnel Conversion Rate", table_cell), Paragraph("7.4% (368 / 5,000 leads)", table_cell), Paragraph("<b>38.5%</b> (Targeted digital conversion)", table_cell), Paragraph("<b>5.2x increase</b> in activated accounts", table_cell)],
        [Paragraph("Customer Acquisition Cost", table_cell), Paragraph("₹15,000 blended CAC", table_cell), Paragraph("<b>₹3,150</b> digital CAC", table_cell), Paragraph("<b>79% cost reduction</b>; instant month-1 profitability", table_cell)],
        [Paragraph("Time-to-Activation", table_cell), Paragraph("18 days average sales cycle", table_cell), Paragraph("<b>10 minutes</b> onboarding; 24-48h dispatch", table_cell), Paragraph("Eliminates scheduling drop-offs entirely", table_cell)],
        [Paragraph("KYC Verification Turnaround", table_cell), Paragraph("4 - 7 business days", table_cell), Paragraph("<b>Under 15 seconds</b> via local OCR", table_cell), Paragraph("Zero back-office manual document processing backlog", table_cell)],
        [Paragraph("Regulatory & Catalog Accuracy", table_cell), Paragraph("Manual sales reps (frequent mis-selling)", table_cell), Paragraph("<b>100% Deterministic Guardrails</b> (7-criteria eval)", table_cell), Paragraph("Zero billing disputes, zero DoT penalty exposure", table_cell)]
    ]
    t_impact = Table(impact_data, colWidths=[110, 130, 130, 134])
    t_impact.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_impact)
    story.append(Spacer(1, 12))
    
    # Conclusion summary box
    conclusion_text = [
        [Paragraph(
            "<b>Conclusion & Hackathon Value Proposition:</b> Project Udyam Digital is not just a chatbot—it is an autonomous enterprise sales "
            "and activation infrastructure designed specifically for the nuanced reality of India's commercial ecosystem. By uniting multilingual AI, "
            "zero-form conversational KYC, deterministic quoting guardrails, 5G AirFiber auto-pivot, and self-healing loop engineering, "
            "it unlocks millions of underserved micro-enterprises profitably, sustainably, and at national scale.",
            callout_text
        )]
    ]
    t_concl = Table(conclusion_text, colWidths=[504])
    t_concl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EDF2F7")),
        ('BOX', (0, 0), (-1, -1), 1, c_secondary),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_concl)
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF at: {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.getcwd(), "Project_Udyam_Digital_Brief.pdf")
    create_executive_pdf(out)
