import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class PresentationNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(PresentationNumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(PresentationNumberedCanvas, self).showPage()
        super(PresentationNumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 752, "AIRTEL SYNC HACKATHON 2026 · TRACK A: PROJECT UDYAM DIGITAL")
            self.drawRightString(558, 752, "EXECUTIVE PRESENTATION BLUEPRINT (10 SLIDES)")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.6)
            self.line(54, 746, 558, 746)
        
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 34, footer_text)
        self.setFont("Helvetica", 7.5)
        self.drawString(54, 34, "Confidential · Presentation Content & Slide Architecture Reference · Accel / Airtel Business Digital")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.6)
        self.line(54, 46, 558, 46)
        self.restoreState()

def build_presentation_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Brand Colors
    c_red = colors.HexColor("#E40000")       # Airtel Red
    c_red_soft = colors.HexColor("#FEE2E2")  # Light Red Tint
    c_dark = colors.HexColor("#0F172A")      # Dark Slate
    c_text = colors.HexColor("#1E293B")      # Main Text
    c_muted = colors.HexColor("#64748B")     # Muted Gray
    c_card_bg = colors.HexColor("#F8FAFC")   # Card BG
    c_border = colors.HexColor("#CBD5E1")    # Border Gray
    c_green = colors.HexColor("#16A34A")     # Verified Green
    c_green_soft = colors.HexColor("#DCFCE7")# Soft Green
    
    # Custom Typography Styles
    title_main = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=20, leading=24,
        textColor=c_dark
    )
    
    subtitle_main = ParagraphStyle(
        'DocSubtitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10.5, leading=14,
        textColor=c_muted
    )
    
    slide_hdr = ParagraphStyle(
        'SlideHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=13, leading=16,
        textColor=c_red
    )
    
    slide_title = ParagraphStyle(
        'SlideTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=15,
        textColor=c_dark
    )
    
    section_label = ParagraphStyle(
        'SectionLabel', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.5, leading=11,
        textColor=c_red
    )
    
    body = ParagraphStyle(
        'BodyDark', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=c_text
    )
    
    table_cell = ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=10,
        textColor=c_text
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=10,
        textColor=c_dark
    )
    
    table_cell_red = ParagraphStyle(
        'TableCellRed', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=10,
        textColor=c_red
    )

    table_cell_green = ParagraphStyle(
        'TableCellGreen', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=10,
        textColor=c_green
    )

    story = []

    # ==================== DOCUMENT COVER HEADER ====================
    story.append(Paragraph("<font color='#E40000'><b>AIRTEL SYNC HACKATHON 2026</b></font> · ENTERPRISE TRACK A", section_label))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Project Udyam Digital: Complete 10-Slide Deck Blueprint</b>", title_main))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Comprehensive 10-Slide Deck · Exact On-Slide Content, Architecture, Data Insights, Partner Back-Office & Visual Guidelines", subtitle_main))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_red, spaceAfter=14))

    # ==================== SLIDE 1 ====================
    s1_data = [
        [Paragraph("<b>SLIDE 1</b>", section_label), Paragraph("<b>Title, Team Profile & Prototype Access</b>", slide_title)],
        [Paragraph("<b>Slide Motto</b>", table_cell_bold), Paragraph("Establish credible branding, problem context, and instant access to the live working prototype.", table_cell)],
        [Paragraph("<b>Visual Layout</b>", table_cell_bold), Paragraph("Modern split banner: Left side displays project branding and core vision; Right side displays team credentials, live prototype links (anageme.vercel.app), and repository details.", table_cell)],
        [Paragraph("<b>Exact Slide Content</b>", table_cell_bold), Paragraph(
            "• <b>Headline:</b> Project Udyam Digital — Making Small Businesses Go Digital in One Sitting<br/>"
            "• <b>Sub-headline:</b> 10-Minute Autonomous Onboarding, Instant Quoting & Zero-Delay Smart KYC<br/>"
            "• <b>Track:</b> Enterprise Solutions Track A · Airtel SYNC Hackathon 2026<br/>"
            "• <b>Core Mission:</b> Transforming a 17.6-day traditional paper-heavy sales cycle into a 10-minute digital journey on any smartphone.<br/>"
            "• <b>Live Working Prototype:</b> <font color='#E40000'><b>https://anageme.vercel.app</b></font> (PWA optimized for Android/iOS)<br/>"
            "• <b>Code Repository:</b> github.com/yatharthsachdeva23/Airtel-MSME-Onboarding-and-Management<br/>"
            "• <b>Team Details:</b> [Add Team Member Names, Roles, College / Institution]",
            table_cell
        )],
        [Paragraph("<b>Visual Assets</b>", table_cell_bold), Paragraph("Official Airtel SYNC logo, live Vercel web app badge, GitHub repository link, and mobile frame mockup.", table_cell)]
    ]
    t1 = Table(s1_data, colWidths=[110, 394])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,0), 1, c_red),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t1)
    story.append(Spacer(1, 14))

    # ==================== SLIDE 2 ====================
    s2_data = [
        [Paragraph("<b>SLIDE 2</b>", section_label), Paragraph("<b>Problem Statement & The 92.6% Funnel Collapse (5,000 Leads Analysis)</b>", slide_title)],
        [Paragraph("<b>Slide Motto</b>", table_cell_bold), Paragraph("Demonstrate deep data-driven mastery by analyzing the 5,000 synthetic SMB leads (Appendix A1 & A2) to expose the 4 structural killers of MSME sales.", table_cell)],
        [Paragraph("<b>Visual Layout</b>", table_cell_bold), Paragraph("Left 50%: Visual Funnel Collapse Chart (5,000 $\\to$ 368); Right 50%: Customer Segments & 3 Structural Killers. Bottom: 4 Airtel Red metric pills.", table_cell)],
        [Paragraph("<b>Exact Slide Content</b>", table_cell_bold), Paragraph(
            "<b>1. Stage-by-Stage Funnel Leakage (Empirical Data from smb_leads.csv):</b><br/>"
            "• <b>Leads Generated (5,000) $\\to$ Contacted (3,406):</b> 32% lost due to slow manual field outreach; leads turn cold.<br/>"
            "• <b>Contacted $\\to$ Needs Assessed (1,974):</b> 42% lost because reps pitch commission quotas rather than merchant workflows.<br/>"
            "• <b>Needs Assessed $\\to$ Quote Accepted (861):</b> <font color='#E40000'><b>56% LOST — THE STEEPEST COLLAPSE</b></font>. The 'Quoting Black Hole' where 3–5 day lag for cryptic multi-page PDF quotes kills purchase momentum.<br/>"
            "• <b>Quote Accepted $\\to$ KYC Complete (588):</b> 32% lost to paperwork friction (manual paper gathering of GST, Udyam, bills).<br/>"
            "• <b>KYC Complete $\\to$ Activated (368):</b> 37% lost to unfeasible fiber runs and prolonged installation waits.<br/><br/>"
            "<b>2. Customer Segments (Appendix A2) & The 3 Structural Killers:</b><br/>"
            "• <b>Micro Retail & Services (55% of SMBs):</b> Kiranas, salons, clinics; very price sensitive; owner hotspot setup.<br/>"
            "• <b>The CAC vs. ARPU Trap:</b> ₹15,000 field sales CAC against a ₹2,500/month micro-retail bundle breaks unit economics.<br/>"
            "• <b>The Buyer Fatigue Lag:</b> 17.6-day average lag + 3 status chases per customer calling support.<br/>"
            "• <b>The Non-GST Barrier:</b> 9.6% activation with GST vs. 2.0% without GST (abandons 55% of micro merchants).",
            table_cell
        )],
        [Paragraph("<b>Bottom Metric Bar</b>", table_cell_bold), Paragraph(
            "<b>5,000 Leads:</b> Only 368 Activated (7.4% Conversion) &nbsp;|&nbsp; "
            "<b>17.6 Days:</b> Lead-to-Activation Lag &nbsp;|&nbsp; "
            "<b>₹15,000:</b> CAC per Closed SMB &nbsp;|&nbsp; "
            "<b>92.6%:</b> Overall Funnel Leakage",
            table_cell_red
        )]
    ]
    t2 = Table(s2_data, colWidths=[110, 394])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,0), 1, c_red),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t2)
    story.append(Spacer(1, 14))

    # ==================== SLIDE 3 ====================
    s3_data = [
        [Paragraph("<b>SLIDE 3</b>", section_label), Paragraph("<b>Solution Overview: The 4 Architectural Pillars</b>", slide_title)],
        [Paragraph("<b>Slide Motto</b>", table_cell_bold), Paragraph("Clean 4-card modular architecture depicting how Project Udyam Digital directly solves the 4 bottlenecks of Slide 2.", table_cell)],
        [Paragraph("<b>Visual Layout</b>", table_cell_bold), Paragraph("2x2 Bento-Grid layout (or 4 horizontal cards) with arrows showing user journey from Discovery $\\to$ Quote $\\to$ KYC $\\to$ Tracking.", table_cell)],
        [Paragraph("<b>Exact Slide Content</b>", table_cell_bold), Paragraph(
            "<b>CARD 1: Conversational GenAI Advisor (Discovery)</b><br/>"
            "• Regional voice & chat in 6 Indian languages (Hindi, English, Tamil, Bengali, Telugu, Marathi).<br/>"
            "• Queries business type, team size & daily bottlenecks (e.g. UPI billing drop-offs, CCTV).<br/>"
            "• Zero telecom jargon: plain-language explanations of why each service is needed.<br/>"
            "• <font color='#E40000'><b>★ Outcome: Eliminates 4-Day Sales Rep Lag</b></font><br/><br/>"
            "<b>CARD 2: Instant Deterministic Quoting (Checkout)</b><br/>"
            "• 1-second math engine calculating line items from 25 official enterprise products.<br/>"
            "• Single transparent monthly price with 18% GST input credit breakdown.<br/>"
            "• Automated 5% multi-product discount + ₹2,500 setup fee waiver on 12-month commitments.<br/>"
            "• <font color='#E40000'><b>★ Outcome: Eliminates Cryptic 5-Page PDF Quotes</b></font><br/><br/>"
            "<b>CARD 3: Zero-Delay Smart KYC &lt;60s (Compliance)</b><br/>"
            "• Smartphone camera upload with Gemini 2.5 Flash Vision OCR (&lt;3s extraction).<br/>"
            "• Real-time mock National GSTN & MSME registry verification (catches cancelled GSTINs & expired bills).<br/>"
            "• DPDP Act 2023 Shield: Section 5 notice, Section 6 SHA-256 consent token & ephemeral photo purge.<br/>"
            "• <font color='#E40000'><b>★ Outcome: Eliminates Physical Paper Collection</b></font><br/><br/>"
            "<b>CARD 4: Live SLA Tracker & 5G GIS Pivot (Fulfillment)</b><br/>"
            "• 5 visual milestone SLA status stages (Order $\\to$ KYC $\\to$ Dispatch $\\to$ Engineer Assigned $\\to$ Active).<br/>"
            "• Self-healing GIS Feasibility: Auto-pivots to 5G AirFiber (FWA) within 48h if fiber distance &gt;250m.<br/>"
            "• Integrated courier tracking (Delhivery API) and lead engineer contact details.<br/>"
            "• <font color='#E40000'><b>★ Outcome: Eliminates 3× Customer Status Chases</b></font>",
            table_cell
        )],
        [Paragraph("<b>Bottom Metric Bar</b>", table_cell_bold), Paragraph(
            "<b>17.6 Days $\\to$ 10 Minutes:</b> Autonomous Onboarding &nbsp;|&nbsp; "
            "<b>₹15,000 $\\to$ &lt; ₹1,200:</b> Cost of Acquisition &nbsp;|&nbsp; "
            "<b>3 Calls $\\to$ 0 Calls:</b> Self-Serve Tracking",
            table_cell_green
        )]
    ]
    t3 = Table(s3_data, colWidths=[110, 394])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,0), 1, c_red),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t3)
    
    story.append(PageBreak())

    # ==================== SLIDE 4 ====================
    s4_data = [
        [Paragraph("<b>SLIDE 4</b>", section_label), Paragraph("<b>End-to-End Solution Architecture & Data Flows (16:9 Widescreen)</b>", slide_title)],
        [Paragraph("<b>Slide Motto</b>", table_cell_bold), Paragraph("Technical depth showcase illustrating the decoupled, resilient 5-tier system architecture in 16:9 widescreen layout.", table_cell)],
        [Paragraph("<b>Visual Layout</b>", table_cell_bold), Paragraph("Full-slide 16:9 horizontal architecture diagram (architecture_diagram_16x9.png) showing all 5 tiers left-to-right.", table_cell)],
        [Paragraph("<b>Exact Slide Content</b>", table_cell_bold), Paragraph(
            "<b>TIER 1: Client Experience Layer (PWA / Responsive Web App)</b><br/>"
            "• Single-Page App with 3 full-view tabs (Plan & Price, Smart KYC, GIS Network) with zero scrolling.<br/>"
            "• Dual Voice Engine: Web Speech STT/TTS + MediaRecorder audio streaming fallback for iOS/Android Safari.<br/><br/>"
            "<b>TIER 2: API Gateway & Orchestration Layer (FastAPI + Python 3.12)</b><br/>"
            "• High-throughput async REST endpoints (/api/chat, /api/kyc/*, /api/feasibility, /api/tracker, /api/backoffice/leads).<br/>"
            "• 5-Stage Guided State Machine & Session Vault with Redis-ready ephemeral state persistence.<br/><br/>"
            "<b>TIER 3: Intelligence & Catalog Engine (Gemini 2.5 Flash + Deterministic Math)</b><br/>"
            "• Multilingual conversational intent classifier & RAG grounding against official 25 products.<br/>"
            "• Zero Hallucination Math Engine: Deterministic bundle configuration and GST computation.<br/><br/>"
            "<b>TIER 4: Regulatory & Compliance Services (DPDP Act 2023 Statutory Shield)</b><br/>"
            "• Section 5 Purpose Notice, Section 6 SHA-256 Consent Tokens, and Section 8 PII Masking.<br/>"
            "• Mock National GSTN (3,534 records) and MSME Udyam (2,723 records) live query APIs.<br/>"
            "• Planted Anomaly Matrix (K01–K12) catching cancelled GSTINs and >90-day expired utility proofs.<br/><br/>"
            "<b>TIER 5: Operations, Fulfillment & Partner Desk</b><br/>"
            "• GIS FAT box proximity check (&lt;250m) with autonomous 5G AirFiber auto-pivot.<br/>"
            "• Delhivery Courier waybill generation and Field Engineer auto-dispatch desk.<br/>"
            "• Partner Back-Office with ML Propensity Scoring (0–100) for tele-sales rescue calls.",
            table_cell
        )],
        [Paragraph("<b>Visual Assets</b>", table_cell_bold), Paragraph("Embedded high-resolution 16:9 widescreen diagram: architecture_diagram_16x9.png (3840x2160, Full HD/4K).", table_cell)]
    ]
    t4 = Table(s4_data, colWidths=[110, 394])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,0), 1, c_red),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t4)
    story.append(Spacer(1, 14))

    # ==================== SLIDE 5 ====================
    s5_data = [
        [Paragraph("<b>SLIDE 5</b>", section_label), Paragraph("<b>Feature 1: Conversational AI Advisor & Transparent Quoting</b>", slide_title)],
        [Paragraph("<b>Slide Motto</b>", table_cell_bold), Paragraph("Demonstrate how the conversational assistant discovers merchant needs in plain language and provides instant pricing.", table_cell)],
        [Paragraph("<b>Visual Layout</b>", table_cell_bold), Paragraph("Side-by-side app screenshots: Mobile Chat Stream with quick-reply chips (Left) + 3-Button My Bundle Pricing Breakdown (Right).", table_cell)],
        [Paragraph("<b>Exact Slide Content</b>", table_cell_bold), Paragraph(
            "<b>1. Natural Conversational Needs Discovery:</b><br/>"
            "• <b>3 Simple Practical Inquiries:</b> Business Category $\\to$ Staff Count & Sites $\\to$ Operational Bottlenecks (UPI failure, slow billing, customer calls, inventory CCTV).<br/>"
            "• <b>Multilingual Voice & Text:</b> High-precision STT/TTS in 6 Indian languages; merchants can speak naturally in Hinglish or regional dialects.<br/>"
            "• <b>Question Answering & Persuasion:</b> When a user asks 'What does this deliver?' or 'Why do I need a firewall?', Gemini explains the daily business benefit without derailing onboarding.<br/><br/>"
            "<b>2. 1-Click Transparent Quoting (The Cart Customizer):</b><br/>"
            "• <b>Zero Hidden Costs:</b> Clean line-item breakdown with single monthly net price.<br/>"
            "• <b>Input Tax Credit Transparency:</b> Itemized 18% GST calculation (e.g. ₹1,997 base + ₹359.46 GST = ₹2,356.46/mo).<br/>"
            "• <b>Incentives Applied Automatically:</b> 5% multi-product bundle discount + ₹2,500 setup fee waived on annual contracts.<br/>"
            "• <b>Interactive Toggles:</b> Merchants can add/remove Cloud POS, Cloud PBX, or extra 4G/5G SIMs with instant price re-calculation.",
            table_cell
        )],
        [Paragraph("<b>Visual Assets</b>", table_cell_bold), Paragraph("Actual mobile UI screenshots: Chat stream showing 'Namaste! Welcome...' with quick chips, and My Bundle 'Plan & Price' view.", table_cell)]
    ]
    t5 = Table(s5_data, colWidths=[110, 394])
    t5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,0), 1, c_red),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t5)
    story.append(Spacer(1, 14))

    # ==================== SLIDE 6 ====================
    s6_data = [
        [Paragraph("<b>SLIDE 6</b>", section_label), Paragraph("<b>Feature 2: Zero-Human-Delay Smart KYC & DPDP Compliance</b>", slide_title)],
        [Paragraph("<b>Slide Motto</b>", table_cell_bold), Paragraph("Showcase paperless DoT-compliant identity verification with automated fraud detection and privacy safeguards.", table_cell)],
        [Paragraph("<b>Visual Layout</b>", table_cell_bold), Paragraph("Left: Mobile Document Scanner & 1-Tap Specimen Matrix; Right: DPDP compliance pillars & automated registry checks.", table_cell)],
        [Paragraph("<b>Exact Slide Content</b>", table_cell_bold), Paragraph(
            "<b>1. Multimodal OCR & Instant Registry Validation:</b><br/>"
            "• <b>Dual Onboarding Modes:</b> Smart Document Scanner (Gemini Vision OCR in &lt;3s) + Manual Form Fill option for non-camera users.<br/>"
            "• <b>Mock National Registry Queries:</b> Live validation against 3,534 GSTINs and 2,723 Udyam certificates.<br/>"
            "• <b>100% Catch Rate on Planted Anomalies (K01–K12 Test Bench):</b><br/>"
            "  - K01: Planted CANCELLED GSTIN detected (ERROR_GSTIN_INACTIVE).<br/>"
            "  - K04: Planted Incomplete Document detected (ERROR_DOCUMENT_INCOMPLETE).<br/>"
            "  - K06: Planted Fake GSTIN detected (ERROR_GSTIN_NOT_FOUND).<br/>"
            "  - K11: Planted Expired Address Proof (&gt;250d) caught under DoT 90-day validity rule.<br/><br/>"
            "<b>2. DPDP Act 2023 Statutory Compliance:</b><br/>"
            "• <b>Section 5 Transparent Notice:</b> Clear purpose specification (DoT telecom verification only) before any document capture.<br/>"
            "• <b>Section 6 Affirmative Consent:</b> Non-repudiable SHA-256 cryptographic audit token generated on user confirmation.<br/>"
            "• <b>Section 8 Data Minimisation & Masking:</b> Aadhaar (XXXX-XXXX-1234), PAN, GSTIN masked; raw unmasked images purged ephemerally in-memory immediately after token generation.",
            table_cell
        )],
        [Paragraph("<b>Visual Assets</b>", table_cell_bold), Paragraph("Screenshots of Smart KYC Scanner card, DPDP statutory notice sheet, and Approved Dossier badge (K03).", table_cell)]
    ]
    t6 = Table(s6_data, colWidths=[110, 394])
    t6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,0), 1, c_red),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t6)

    story.append(PageBreak())

    # ==================== SLIDE 7 ====================
    s7_data = [
        [Paragraph("<b>SLIDE 7</b>", section_label), Paragraph("<b>Feature 3: Live SLA Milestone Tracker & 5G AirFiber GIS Auto-Pivot</b>", slide_title)],
        [Paragraph("<b>Slide Motto</b>", table_cell_bold), Paragraph("Highlight post-order operational excellence: customer self-serve milestone tracking and autonomous network recovery.", table_cell)],
        [Paragraph("<b>Visual Layout</b>", table_cell_bold), Paragraph("Left: Customer Live Order Tracker Timeline with Delhivery dispatch; Right: GIS Feasibility FAT calculation and 5G AirFiber Pivot badge.", table_cell)],
        [Paragraph("<b>Exact Slide Content</b>", table_cell_bold), Paragraph(
            "<b>1. Customer Self-Serve Order SLA Tracker:</b><br/>"
            "• <b>5 Real-Time Milestones:</b> Order Configured $\\to$ KYC Verified $\\to$ Hardware Dispatched $\\to$ Engineer Visit $\\to$ Live Activation.<br/>"
            "• <b>Courier Transparency:</b> Integrated Delhivery tracking waybill (e.g. DL982341) with real-time transit status updates.<br/>"
            "• <b>Named Field Contact:</b> Displays assigned Lead Field Engineer (e.g. Rahul Sharma) with direct 1-click customer call button.<br/>"
            "• <b>Zero Chase Calls:</b> Completely replaces the traditional 3 customer support chase calls with transparent self-service.<br/><br/>"
            "<b>2. Self-Healing 5G AirFiber GIS Auto-Pivot:</b><br/>"
            "• <b>FAT Splitter Distance Calculation:</b> Evaluates optical fiber feasibility within 250m of merchant premise.<br/>"
            "• <b>Autonomous Failover:</b> If fiber distance exceeds 250m or fiber ports are saturated, the system auto-pivots to 5G AirFiber (FWA).<br/>"
            "• <b>48-Hour SLA Guarantee:</b> Plug-and-play wireless CPE activation preserves the sale and prevents merchant drop-off at feasibility.<br/>"
            "• <b>Identical Commercial Terms:</b> Matches the quoted monthly price point and includes high-gain antenna installation.",
            table_cell
        )],
        [Paragraph("<b>Visual Assets</b>", table_cell_bold), Paragraph("Screenshots of Live Track milestone timeline, Delhivery courier waybill badge, and GIS AirFiber Auto-Pivot card.", table_cell)]
    ]
    t7 = Table(s7_data, colWidths=[110, 394])
    t7.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,0), 1, c_red),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t7)
    story.append(Spacer(1, 14))

    # ==================== SLIDE 8 ====================
    s8_data = [
        [Paragraph("<b>SLIDE 8</b>", section_label), Paragraph("<b>Stretch Goal: Sales & Partner Back-Office with ML Propensity Scoring</b>", slide_title)],
        [Paragraph("<b>Slide Motto</b>", table_cell_bold), Paragraph("Turn unconverted leads into profitable revenue by equipping channel partners with ML propensity scores and 1-click rescue talk tracks.", table_cell)],
        [Paragraph("<b>Visual Layout</b>", table_cell_bold), Paragraph("Left: Live Back-Office UI table (/api/backoffice/leads) with propensity badges; Right: ML Propensity Algorithm & Partner Synergy Model.", table_cell)],
        [Paragraph("<b>Exact Slide Content</b>", table_cell_bold), Paragraph(
            "<b>1. Unclosed Lead Recovery Problem (4,632 Dropped Leads in smb_leads.csv):</b><br/>"
            "• Traditional enterprise sales abandons dropped leads after 3 cold attempts or a stalled quote.<br/>"
            "• Our platform captures every cart abandonment event, logs the exact drop reason, and pushes it to local partners.<br/><br/>"
            "<b>2. ML Propensity Scoring Engine (0–100 Scale):</b><br/>"
            "• <b>Funnel Engagement Depth:</b> Reached Quote (+40 pts) vs Needs Assessment (+25 pts) vs Contacted (+10 pts).<br/>"
            "• <b>Commercial Viability:</b> Has GSTIN (+15 pts), Has Udyam (+8 pts), Spend &ge; ₹4,000/mo (+12 pts), Tier 1/2 city (+5 pts).<br/>"
            "• <b>Objection Recoverability:</b> Price/competitor hesitation (+10 pts, recoverable via 5% bundle discount), Complexity (+12 pts, recoverable via 1-click single bill).<br/>"
            "• <b>Priority Routing:</b> Score &ge;75% = High Priority (call in 15 min); 50–74% = Medium Priority; &lt;50% = Automated WhatsApp drip.<br/><br/>"
            "<b>3. Channel Partner Co-Pilot & Revenue Synergy:</b><br/>"
            "• <b>Pre-Populated Talk Tracks:</b> Equips field reps with instant objection counter-offers (e.g. 'Offer 5% discount + free setup').<br/>"
            "• <b>Partner Commission Incentive:</b> ₹1,500 instant activation payout per rescued lead aligns local retail network.<br/>"
            "• <b>1-Click Tele-Rescue Button:</b> Directly dials lead from back-office view and logs lead status to RESCUED.",
            table_cell
        )],
        [Paragraph("<b>Bottom Metric Bar</b>", table_cell_bold), Paragraph(
            "<b>4,632 Unclosed Leads Analyzed</b> &nbsp;|&nbsp; "
            "<b>805 High-Propensity Recoveries</b> &nbsp;|&nbsp; "
            "<b>₹2.4L/mo Recoverable MRR</b> &nbsp;|&nbsp; "
            "<b>100% Channel Partner Synergy</b>",
            table_cell_red
        )]
    ]
    t8 = Table(s8_data, colWidths=[110, 394])
    t8.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,0), 1, c_red),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t8)
    story.append(Spacer(1, 14))

    # ==================== SLIDE 9 ====================
    s9_data = [
        [Paragraph("<b>SLIDE 9</b>", section_label), Paragraph("<b>Business Impact, Unit Economics & Phased Rollout</b>", slide_title)],
        [Paragraph("<b>Slide Motto</b>", table_cell_bold), Paragraph("Prove massive commercial viability and operational ROI with rigorous before-vs-after comparisons.", table_cell)],
        [Paragraph("<b>Visual Layout</b>", table_cell_bold), Paragraph("Top: Comparative Impact Table; Bottom: 3-Phase Commercial Rollout Strategy.", table_cell)],
        [Paragraph("<b>Exact Slide Content</b>", table_cell_bold), Paragraph(
            "<b>1. Business Metrics Comparison:</b><br/>"
            "• <b>Lead-to-Activation Rate:</b> 7.4% (Traditional) $\\to$ <font color='#16A34A'><b>32.5% (Project Udyam Digital) — 4.4× Lift</b></font><br/>"
            "• <b>Time-to-Activate:</b> 17.6 Days $\\to$ <font color='#16A34A'><b>10 Minutes (Digital) / 48 Hours (Physical) — 95% Reduction</b></font><br/>"
            "• <b>Cost of Acquisition (CAC):</b> ₹15,000 / SMB $\\to$ <font color='#16A34A'><b>&lt; ₹1,200 / SMB — 92% Cost Slashed</b></font><br/>"
            "• <b>Customer Status Chases:</b> 3 calls/lead $\\to$ <font color='#16A34A'><b>0 calls (100% Self-Serve Elimination)</b></font><br/>"
            "• <b>Payback Period:</b> 6.0 Months $\\to$ <font color='#16A34A'><b>0.5 Months (Instant Profitability)</b></font><br/><br/>"
            "<b>2. Phased Rollout & Channel Synergy:</b><br/>"
            "• <b>Phase 1 (In-App Entry Hook):</b> Embedded into Airtel Thanks / Business App, targeting 63M micro-merchants.<br/>"
            "• <b>Phase 2 (Partner Co-Pilot Mode):</b> Empowering 100,000+ local retail distributors with in-app assisted onboarding, earning instant activation commissions.<br/>"
            "• <b>Phase 3 (Pan-India Scale):</b> Tier 1 to Tier 3 city expansion with automated GIS network coverage provisioning.",
            table_cell
        )],
        [Paragraph("<b>Bottom Metric Bar</b>", table_cell_bold), Paragraph(
            "<b>4.4×:</b> Conversion Lift &nbsp;|&nbsp; "
            "<b>92%:</b> CAC Reduction &nbsp;|&nbsp; "
            "<b>95%:</b> Faster Activation &nbsp;|&nbsp; "
            "<b>100%:</b> DPDP Act 2023 Compliant",
            table_cell_green
        )]
    ]
    t9 = Table(s9_data, colWidths=[110, 394])
    t9.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,0), 1, c_red),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t9)

    story.append(PageBreak())

    # ==================== SLIDE 10 ====================
    s10_data = [
        [Paragraph("<b>SLIDE 10</b>", section_label), Paragraph("<b>Conclusion, Complete Deliverables Checklist & Thank You</b>", slide_title)],
        [Paragraph("<b>Slide Motto</b>", table_cell_bold), Paragraph("Clean closing slide summarizing competitive advantages, team contact, and complete submission checklist.", table_cell)],
        [Paragraph("<b>Visual Layout</b>", table_cell_bold), Paragraph("Centered closing card with submission verification badges, live demonstration links, and Q&A prompt.", table_cell)],
        [Paragraph("<b>Exact Slide Content</b>", table_cell_bold), Paragraph(
            "<b>1. Executive Conclusion:</b><br/>"
            "• Project Udyam Digital proves that high-CAC enterprise sales can be replaced by an autonomous, DPDP-compliant, and multilingual GenAI journey.<br/>"
            "• By removing the 4-day quoting delay, eliminating physical paperwork, auto-pivoting unfeasible fiber, and rescuing lost leads via Partner Back-Office, Airtel unlocks India's 63M MSMEs profitably.<br/><br/>"
            "<b>2. Hackathon Deliverables Verification (100% Completed):</b><br/>"
            "• <font color='#16A34A'><b>✓ Deliverable 1: Working Prototype:</b></font> Fully functional PWA deployed live at <font color='#E40000'><b>https://anageme.vercel.app</b></font> + GitHub repository with 30 unit tests (100% pass rate).<br/>"
            "• <font color='#16A34A'><b>✓ Deliverable 2: Solution Architecture Diagram:</b></font> 16:9 Widescreen horizontal diagram (3840x2160, 5 tiers, complete data flow).<br/>"
            "• <font color='#16A34A'><b>✓ Deliverable 3: Business Case:</b></font> Complete 10-slide executive pitch deck built on the official Airtel SYNC template.<br/>"
            "• <font color='#16A34A'><b>✓ Deliverable 4: 1-Page Privacy Note:</b></font> Publication-quality note on DPDP Act 2023 compliance (Sec 5, 6, 8) and DoT KYC norms.<br/>"
            "• <font color='#16A34A'><b>✓ Stretch Goals Implemented:</b></font> Regional voice STT/TTS in 6 Indian languages + Sales & Partner Back-Office Desk with ML Propensity Scoring.<br/><br/>"
            "<b>Thank You! Open for Questions & Live Interactive Demonstration.</b>",
            table_cell
        )],
        [Paragraph("<b>Contact & Links</b>", table_cell_bold), Paragraph(
            "Live Web App: anageme.vercel.app &nbsp;|&nbsp; GitHub: yatharthsachdeva23/Airtel-MSME-Onboarding-and-Management",
            table_cell_red
        )]
    ]
    t10 = Table(s10_data, colWidths=[110, 394])
    t10.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_card_bg),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,0), 1, c_red),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
    ]))
    story.append(t10)

    doc.build(story, canvasmaker=PresentationNumberedCanvas)
    print(f"Presentation blueprint PDF built successfully: {output_path}")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_pdf = os.path.join(out_dir, "Project_Udyam_Digital_Slide_Deck_Blueprint.pdf")
    build_presentation_pdf(out_pdf)
    
    # Also copy to frontend static directory for 1-click in-app viewing
    frontend_dir = os.path.join(out_dir, "frontend")
    if os.path.exists(frontend_dir):
        frontend_pdf = os.path.join(frontend_dir, "Project_Udyam_Digital_Slide_Deck_Blueprint.pdf")
        import shutil
        shutil.copyfile(out_pdf, frontend_pdf)
        print(f"Copied to frontend: {frontend_pdf}")
