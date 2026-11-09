# -*- coding: utf-8 -*-
import os
import re
from typing import Dict, Any, List, Optional, Tuple
from backend.catalog_service import CatalogService
from backend.loop_engine import LoopEngine
from backend.gemini_service import GeminiSalesService, get_gemini_api_key

# 40-Column Categorization from smb_leads.csv
SMB_LEAD_METRIC_CATEGORIES = {
    "category_1_basic": {
        "title": "Category 1: Basic Details (Always Asked)",
        "description": "Essential identity parameters asked upfront for conversational personalization.",
        "columns": ["business_name", "business_type", "preferred_language", "contact_name"]
    },
    "category_2_required": {
        "title": "Category 2: Required Operational Sizing (Always Asked)",
        "description": "Core operational and compliance dimensions needed to deterministically size bandwidth, user seats, and GST credit.",
        "columns": ["employee_count", "num_sites", "current_internet", "monthly_telecom_spend_inr", "has_gstin", "has_udyam", "gstin", "udyam_number"]
    },
    "category_3_contextual": {
        "title": "Category 3: Contextual Operational Needs (Asked Case-by-Case)",
        "description": "Domain-specific pain points asked contextually to tailor specialized add-ons (Soundbox, POS, Cloud PBX, IoT, Leased Line).",
        "columns": ["annual_turnover_band", "products_of_interest", "current_provider", "city", "city_tier", "state"]
    },
    "category_4_telemetry": {
        "title": "Category 4: Internal Telemetry & Lifecycle Metrics (Never Asked to User)",
        "description": "Telemetry and CRM drop-off tracking used strictly by backend analytics and developer diagnostics.",
        "columns": [
            "lead_id", "created_date", "lead_source", "contact_role", "stage_reached",
            "outcome", "drop_reason", "contacted_date", "needs_assessed_date",
            "quote_accepted_date", "kyc_complete_date", "activated_date",
            "days_lead_to_activation", "customer_follow_up_calls", "bundle_products",
            "monthly_bundle_value_inr", "one_time_setup_inr", "contract_months",
            "churned_within_6_months", "nps_score", "acquisition_cost_inr"
        ]
    }
}

# Multilingual greeting & explanation templates for Pan-India support
TRANSLATIONS = {
    "en": {
        "greeting": "Namaste! Welcome to Accel Business Digital. Start a quick 2-minute chat with me to get your tailored business quote and instant pricing with zero human delays! What kind of business do you run? (e.g., Kirana store, Clinic, Restaurant, Logistics, Manufacturing)",
        "ask_size": "Great! How many staff members work with you, and how many shop/office locations do you have?",
        "ask_needs": "Understood. What is your current internet setup (Mobile hotspot, broadband, or none), and what are your main daily bottlenecks? (e.g., UPI drop-offs, billing speed, customer calls, CCTV)",
        "ask_gstin": "Do you have an active GST number or Udyam registration for your business? (This unlocks 18% input tax credit and free installation)",
        "bundle_ready": "Here is your tailored **Digital Business Bundle**. We picked these tools specifically for your daily workflow with zero hidden charges:",
        "handoff_prompt": "I noticed you have some questions or concerns. Would you like to connect directly with our local business advisor in your area?",
        "switch_ack": "Got it! Switched your business profile to **{business}**.\n\n{ask}"
    },
    "hi": {
        "greeting": "नमस्ते! एक्सेल बिज़नेस डिजिटल में आपका स्वागत है। तुरंत अपने बिज़नेस का कोटेशन और सही कीमत जानने के लिए मेरे साथ 2 मिनट की त्वरित चैट करें! आप किस प्रकार का बिज़नेस चलाते हैं? (जैसे किराना दुकान, क्लिनिक, रेस्टोरेंट, लॉजिस्टिक्स, मैन्युफैक्चरिंग)",
        "ask_size": "बहुत बढ़िया! आपके साथ कितने कर्मचारी काम करते हैं, और आपकी कितनी दुकानें या शाखाएं हैं?",
        "ask_needs": "समझ गया। वर्तमान में इंटरनेट की क्या व्यवस्था है, और मुख्य चुनौतियां क्या हैं? (जैसे UPI फेल होना, बिलिंग, कस्टमर कॉल, सीसीटीवी)",
        "ask_gstin": "क्या आपके पास अपने व्यवसाय का सक्रिय GST नंबर या उद्यम रजिस्ट्रेशन है? (इससे 18% इनपुट क्रेडिट और मुफ्त इंस्टॉलेशन मिलता है)",
        "bundle_ready": "यह रहा आपके व्यवसाय के लिए तैयार **डिजिटल बिज़नेस बंडल**। हमने इसे आपकी प्राथमिकताओं के अनुसार तैयार किया है:",
        "handoff_prompt": "लगता है आपके कुछ सवाल या बजट संबंधी शंकाएं हैं। क्या आप अपने नजदीकी एक्सेल लोकल बिजनेस पार्टनर से बात करना चाहेंगे?",
        "switch_ack": "समझ गया! आपका बिजनेस प्रोफाइल बदलकर **{business}** कर दिया गया है।\n\n{ask}"
    },
    "ta": {
        "greeting": "வணக்கம்! Accel Business Digital-க்கு வரவேற்கிறோம். உடனடி விலை மதிப்பீடு பெற என்னுடன் 2 நிமிட விரைவு அரட்டையைத் தொடங்குங்கள்! நீங்கள் என்ன தொழில் செய்கிறீர்கள்? (எ.கா. மளிகைக் கடை, கிளினிக், உணவகம், போக்குவரத்து)",
        "ask_size": "உங்கள் கடையில் எத்தனை ஊழியர்கள் பணிபுரிகிறார்கள், எத்தனை கிளைகள் உள்ளன?",
        "ask_needs": "உங்கள் முக்கிய தேவைகள் என்ன? (UPI கட்டணங்களுக்கான அதிவேக Wi-Fi, வாட்ஸ்அப் விளம்பரம், CCTV கேமரா)",
        "ask_gstin": "உங்களிடம் GST எண் அல்லது உத்யம் பதிவு உள்ளதா?",
        "bundle_ready": "உங்கள் வணிகத்திற்கான பிரத்யேக **டிஜிட்டல் வணிக தொகுப்பு** தயார்:",
        "handoff_prompt": "உங்களுக்கு ஏதேனும் சந்தேகங்கள் இருந்தால் எங்கள் உள்ளூர் Accel ஆலோசகரிடம் பேச விரும்புகிறீர்களா?",
        "switch_ack": "புரிந்து கொண்டது! உங்கள் வணிக சுயவிவரம் **{business}** என மாற்றப்பட்டது.\n\n{ask}"
    },
    "bn": {
        "greeting": "নমস্কার! Accel Business Digital-এ আপনাকে স্বাগতম। তাৎক্ষণিক ব্যবসায়িক কোটেশন পেতে আমার সাথে ২ মিনিটের দ্রুত চ্যাট করুন! আপনি কী ধরণের ব্যবসা করেন? (যেমন মুদি দোকান, ক্লিনিক, রেস্তোরাঁ, পরিবহন)",
        "ask_size": "আপনার প্রতিষ্ঠানে কতজন কর্মচারী কাজ করেন এবং কতগুলি শাখা রয়েছে?",
        "ask_needs": "আপনার মূল প্রয়োজন কী? (UPI/বিলিংয়ের জন্য দ্রুত ওয়াই-ফাই, হোয়াটসঅ্যাপ প্রচার, সিসিটিভি ক্যামেরা)",
        "ask_gstin": "আপনার কি কোনো জিএসটি (GST) বা উদ্যম রেজিস্ট্রেশন নম্বর আছে?",
        "bundle_ready": "আপনার ব্যবসার জন্য বিশেষভাবে তৈরি **ডিজিটাল বিজনেস বান্ডিল**:",
        "handoff_prompt": "আপনার কি কোনো প্রশ্ন রয়েছে? আপনি কি আমাদের স্থানীয় পরামর্শদাতার সাথে সরাসরি কথা বলতে চান?",
        "switch_ack": "বুঝেছি! আপনার ব্যবসার প্রোফাইল পরিবর্তন করে **{business}** করা হলো।\n\n{ask}"
    },
    "te": {
        "greeting": "నమస్కారం! Accel Business Digital-కి స్వాగతం. మీ వ్యాపారానికి తక్షణ కొటేషన్ మరియు ధర పొందడానికి నాతో 2 నిమిషాల శీఘ్ర చాట్ చేయండి! మీ వ్యాపారం ఏమిటి? (ఉదా. కిరాణా షాప్, క్లినిక్, రెస్టారెంట్, రవాణా)",
        "ask_size": "మీ వద్ద ఎంతమంది సిబ్బంది పనిచేస్తున్నారు మరియు ఎన్ని బ్రాంచీలు ఉన్నాయి?",
        "ask_needs": "మీ ముఖ్యమైన అవసరాలు ఏమిటి? (UPI కోసం వేగవంతమైన Wi-Fi, వాట్సాప్ ప్రచారం, CCTV కెమెరాలు)",
        "ask_gstin": "మీకు GST లేదా ఉద్యమ్ రిజిస్ట్రేషన్ ఉందా?",
        "bundle_ready": "మీ వ్యాపారం కోసం ప్రత్యేకంగా రూపొందించిన **డిజిటల్ బిజినెస్ బండిల్** సిద్ధంగా ఉంది:",
        "handoff_prompt": "మీకు ఏమైనా సందేహాలు ఉంటే మా స్థానిక నిపుణుడితో మాట్లాడాలనుకుంటున్నారా?",
        "switch_ack": "అర్థమైంది! మీ వ్యాపార ప్రొఫైల్ **{business}**గా మార్చబడింది.\n\n{ask}"
    },
    "mr": {
        "greeting": "नमस्कार! Accel Business Digital मध्ये आपले स्वागत आहे. आपला कोणता व्यवसाय आहे? (उदा. किराना दुकान, क्लिनिक, हॉटेल)",
        "ask_size": "आपल्याकडे किती कर्मचारी काम करतात आणि किती दुकाने किंवा शाखा आहेत?",
        "ask_needs": "आपल्या मुख्य गरजा काय आहेत? (UPI/बिलिंगसाठी फास्ट वाय-फाय, व्हॉट्सॲप मार्केटिंग, सीसीटीव्ही)",
        "ask_gstin": "आपल्याकडे GST नंबर किंवा उद्यम नोंदणी आहे का?",
        "bundle_ready": "आपल्या व्यवसायासाठी तयार **डिजिटल बिझनेस बंडल**:",
        "handoff_prompt": "आपल्याला काही प्रश्न किंवा शंका असल्यास आमच्या स्थानिक सल्लागाराशी बोलायचे आहे का?",
        "switch_ack": "समजले! आपले बिझनेस प्रोफाइल बदलून **{business}** केले आहे.\n\n{ask}"
    }
}

# Dynamic, Context-Aware Quick Replies for Every Step and Industry Segment
QUICK_REPLIES = {
    "en": {
        1: [
            {"label": "🏪 Kirana & Retail Store", "value": "Kirana & Retail Store"},
            {"label": "🏥 Clinic & Pharmacy", "value": "Clinic & Pharmacy"},
            {"label": "🚚 Logistics & Fleet", "value": "Logistics & Fleet"},
            {"label": "🏭 Manufacturing Unit", "value": "Manufacturing Unit"},
            {"label": "☕ Cafe & Restaurant", "value": "Cafe & Restaurant"},
            {"label": "💼 Professional Office", "value": "Professional Office"}
        ],
        2: {
            "Professional offices": [
                {"label": "👤 1-3 Staff / Doctors (1 Clinic)", "value": "1-3 staff, 1 clinic"},
                {"label": "👥 4-10 Staff (1-2 Branches)", "value": "4-10 staff, 2 clinics"},
                {"label": "🏢 10+ Staff (Multi-Specialty)", "value": "12 staff, 3 locations"},
                {"label": "🩺 Solo Doctor / Clinic", "value": "Solo doctor, 1 clinic"}
            ],
            "Small multi-site businesses": [
                {"label": "🚚 1-3 Staff (1 Hub)", "value": "1-3 staff, 1 hub"},
                {"label": "👥 4-10 Staff (1-2 Hubs)", "value": "4-10 staff, 2 hubs"},
                {"label": "🏢 10+ Fleet Staff (Multi-City)", "value": "12 staff, 3 hubs"},
                {"label": "🚛 Solo Fleet Operator", "value": "Solo operator, 1 office"}
            ],
            "Small manufacturers": [
                {"label": "🏭 5-10 Workers (1 Shed)", "value": "6 workers, 1 unit"},
                {"label": "🏗️ 10-25 Workers (1 Plant)", "value": "15 workers, 1 plant"},
                {"label": "🏢 25+ Workers (Multi-Unit)", "value": "30 workers, 2 units"},
                {"label": "⚙️ Small Workshop (1-4 Staff)", "value": "3 workers, 1 workshop"}
            ],
            "default": [
                {"label": "👤 1-3 Staff (1 Shop)", "value": "1-3 staff, 1 shop"},
                {"label": "👥 4-10 Staff (1-2 Branches)", "value": "4-10 staff, 2 branches"},
                {"label": "🏢 10+ Staff (Multi-Site)", "value": "12 staff, 3 sites"},
                {"label": "🏪 Just me (Solo Owner)", "value": "Just me, 1 shop"}
            ]
        },
        3: {
            "Professional offices": [
                {"label": "📱 Hotspot (Appointment Drops)", "value": "Mobile Hotspot with appointment drops"},
                {"label": "🌐 Broadband (Need 100% SLA)", "value": "Broadband with 99.5% SLA guarantee"},
                {"label": "📹 CCTV & Patient Wi-Fi", "value": "Need CCTV security and patient Wi-Fi"},
                {"label": "☁️ Cloud Clinic Records", "value": "Cloud records backup and billing"}
            ],
            "Small multi-site businesses": [
                {"label": "🚚 Hotspot (Dispatch Drops)", "value": "Mobile Hotspot with dispatch drops"},
                {"label": "🌐 Dedicated Fiber (99.5% SLA)", "value": "Dedicated Fiber with 99.5% SLA guarantee"},
                {"label": "📹 Security CCTV & Wi-Fi", "value": "Security CCTV and high-speed Wi-Fi"},
                {"label": "🏢 Multi-Branch VPN & Cloud", "value": "Multi-branch VPN and cloud tracking"}
            ],
            "default": [
                {"label": "📱 Mobile Hotspot (UPI Drops)", "value": "Mobile Hotspot with frequent UPI billing drops"},
                {"label": "🌐 Broadband (Need 100% SLA)", "value": "Broadband with 99.5% uptime SLA guarantee"},
                {"label": "📹 CCTV & Customer Wi-Fi", "value": "Need fast Wi-Fi for billing, CCTV and guests"},
                {"label": "🏢 Multi-Branch VPN & Cloud", "value": "Multi-office connectivity and cloud tools"}
            ]
        },
        4: [
            {"label": "✅ Yes, Active GSTIN", "value": "Yes, I have an active GST number"},
            {"label": "📄 Yes, Udyam Registered", "value": "Yes, I have Udyam registration"},
            {"label": "❌ No GST / Unregistered", "value": "No GST number yet"}
        ],
        5: [
            {"label": "⚡ Start Smart KYC (Paperless)", "value": "Proceed to Smart KYC onboarding"},
            {"label": "💰 View Transparent Pricing", "value": "Show me the pricing breakdown"},
            {"label": "📡 Check 5G AirFiber Coverage", "value": "Check fiber and 5G AirFiber feasibility"},
            {"label": "📞 Talk to Business Advisor", "value": "Connect me with a local business advisor"}
        ]
    },
    "hi": {
        1: [
            {"label": "🏪 किराना और रिटेल", "value": "किराना और रिटेल स्टोर"},
            {"label": "🏥 क्लिनिक व मेडिकल", "value": "क्लिनिक और मेडिकल"},
            {"label": "🚚 ट्रांसपोर्ट व फ्लीट", "value": "ट्रांसपोर्ट और फ्लीट"},
            {"label": "🏭 फ़ैक्टरी / कारखाना", "value": "फ़ैक्टरी और मैन्युफैक्चरिंग"},
            {"label": "☕ रेस्टोरेंट / कैफ़े", "value": "रेस्टोरेंट और कैफ़े"}
        ],
        2: {
            "default": [
                {"label": "👤 1-3 कर्मचारी (1 दुकान)", "value": "2 कर्मचारी, 1 दुकान"},
                {"label": "👥 4-10 कर्मचारी (2 शाखाएं)", "value": "5 कर्मचारी, 2 शाखाएं"},
                {"label": "🏢 10+ कर्मचारी (कई शाखाएं)", "value": "12 कर्मचारी, 3 शाखाएं"},
                {"label": "🏪 सिर्फ मैं खुद (अकेला मालिक)", "value": "1 कर्मचारी, 1 दुकान"}
            ]
        },
        3: {
            "default": [
                {"label": "📱 मोबाइल हॉटस्पॉट (UPI फेल)", "value": "मोबाइल हॉटस्पॉट, UPI बार-बार फेल होता है"},
                {"label": "🌐 ब्रॉडबैंड (100% अपटाइम)", "value": "ब्रॉडबैंड चाहिए 99.5% गारंटी के साथ"},
                {"label": "📹 बिलिंग + सीसीटीवी", "value": "बिलिंग, सीसीटीवी और कस्टमर वाई-फाई"},
                {"label": "🏢 मल्टी-ब्रांच कनेक्टिविटी", "value": "कई शाखाओं के लिए इंटरनेट और बैकअप"}
            ]
        },
        4: [
            {"label": "✅ हां, एक्टिव GSTIN है", "value": "हाँ, मेरे पास एक्टिव GST नंबर है"},
            {"label": "📄 हां, उद्यम रजिस्ट्रेशन है", "value": "हाँ, उद्यम रजिस्ट्रेशन है"},
            {"label": "❌ कोई GST नहीं है", "value": "कोई GST नंबर नहीं है"}
        ],
        5: [
            {"label": "⚡ डिजिटल KYC शुरू करें", "value": "डिजिटल KYC शुरू करें"},
            {"label": "💰 प्लान की कीमत देखें", "value": "प्लान की कीमत देखें"},
            {"label": "📡 5G एयरफ़ाइबर चेक करें", "value": "5G एयरफ़ाइबर चेक करें"},
            {"label": "📞 बिजनेस एडवाइजर से बात करें", "value": "बिजनेस एडवाइजर से बात करें"}
        ]
    }
}

class AdvisorEngine:
    def __init__(self, catalog_service: Optional[CatalogService] = None, loop_engine: Optional[LoopEngine] = None):
        self.catalog = catalog_service or CatalogService()
        self.loop_engine = loop_engine or LoopEngine()

    @staticmethod
    def get_quick_replies(step: int, lang: str = "en", segment: Optional[str] = None) -> List[Dict[str, str]]:
        lang_dict = QUICK_REPLIES.get(lang, QUICK_REPLIES["en"])
        step_chips = lang_dict.get(step) or QUICK_REPLIES["en"].get(step, [])
        if isinstance(step_chips, dict):
            return step_chips.get(segment) or step_chips.get("default", [])
        return step_chips

    @staticmethod
    def detect_business_category(message: str) -> Optional[Dict[str, str]]:
        """
        Detects if user message is selecting or switching their business category/industry.
        Returns a dict with 'segment', 'business_title', 'tailored_ask', or None.
        Guards strictly against misinterpreting sizing numbers, internet setups, or GST statements.
        """
        clean = message.strip()
        lower = clean.lower()

        # Guard 1: Sizing responses (Step 2 answers)
        sizing_words = ['staff', 'employee', 'worker', 'people', 'person', 'solo', 'just me', 'only me', 'myself', 'alone', 'single owner', 'team of', 'doctors and', 'headcount', 'counters']
        if any(w in lower for w in sizing_words):
            return None
        # If message starts with digit-only or sizing pattern like "2", "5", "1-3", "4-10" without explicit business words:
        if re.search(r'^\s*\d+[\s\-\+to]*\d*\s*$', lower):
            return None

        # Guard 2: Internet / Bottleneck responses (Step 3 answers)
        internet_words = ['hotspot', 'wifi', 'wi-fi', 'broadband', 'cctv', 'upi', 'billing', 'fiber', 'fibre', 'sla', 'internet', 'backup', 'router', 'dongle', 'drops', 'speed', 'bandwidth']
        if any(w in lower for w in internet_words):
            return None

        # Guard 3: GST / Tax responses (Step 4 answers)
        gst_words = ['gstin', 'gst number', 'udyam', 'tax credit', 'unregistered', 'have gst', 'no gst', 'without gst']
        if any(w in lower for w in gst_words):
            return None

        # Guard 4: Explicit system commands / intents
        system_intents = ['onboard', 'proceed', 'continue', 'start kyc', 'pause', 'wait', 'stop', 'help', 'pricing', 'quote', 'backoffice']
        if any(w in lower for w in system_intents):
            return None

        # Business Category Matching (Checked in priority order)
        # 1. Professional offices & healthcare (clinics, doctors, pathology, accounting, coaching)
        office_keywords = [
            'clinic', 'dental', 'doctor', 'hospital', 'dispensary', 'pathology', 'diagnostic', 'lab',
            'ca firm', 'chartered accountant', 'accounting firm', 'lawyer', 'advocate', 'legal office',
            'consultant', 'consultancy', 'coaching', 'tuition', 'academy', 'institute',
            'architect', 'real estate office', 'software office', 'agency'
        ]
        if any(w in lower for w in office_keywords):
            return {
                "segment": "Professional offices",
                "business_title": clean,
                "tailored_ask": "Understood! How many staff members, doctors, or associates work with you, and how many clinic/office locations do you have?"
            }

        # 2. Small multi-site businesses & logistics (fleet, transport, courier, restaurants, chains)
        multi_keywords = [
            'logistics', 'fleet', 'transport', 'trucking', 'courier', 'delivery', 'cargo',
            'warehouse', 'depot', 'supply chain', 'fleet operator',
            'restaurant', 'hotel', 'cafe', 'dhaba', 'food chain', 'bakery chain', 'food court',
            'multi-site', 'branches', 'multi branch', 'outlets'
        ]
        if any(w in lower for w in multi_keywords):
            return {
                "segment": "Small multi-site businesses",
                "business_title": clean,
                "tailored_ask": "Excellent! How many dispatch/operations staff work with you, and how many fleet hubs, branches, or locations do you manage?"
            }

        # 3. Small manufacturers (factories, plants, workshops)
        mfg_keywords = [
            'manufacturing', 'factory', 'plant', 'workshop', 'industrial', 'fabrication',
            'textile mill', 'auto-parts', 'foundry', 'plastics', 'packaging unit', 'processing unit'
        ]
        if any(w in lower for w in mfg_keywords):
            return {
                "segment": "Small manufacturers",
                "business_title": clean,
                "tailored_ask": "Understood! How many floor workers and supervisors work with you, and how many manufacturing sheds or plants do you operate?"
            }

        # 4. Micro retail & services (kirana, grocery, salon, pharmacy, hardware)
        retail_keywords = [
            'kirana', 'retail', 'grocery', 'general store', 'supermarket', 'provision',
            'salon', 'parlour', 'parlor', 'beauty', 'spa', 'barber',
            'bakery', 'confectionery', 'pharmacy', 'chemist', 'medical store', 'medicine shop',
            'hardware', 'woodcraft', 'textile shop', 'apparel', 'boutique', 'bookstore',
            'stationery', 'electronics shop', 'mobile store', 'sweet shop'
        ]
        if any(w in lower for w in retail_keywords):
            return {
                "segment": "Micro retail & services",
                "business_title": clean,
                "tailored_ask": "Great! How many shop staff work with you, and how many retail counters or locations do you have?"
            }

        return None

    def sync_bundle_customization(
        self,
        user_message: str,
        reply_text: str,
        gem_res: Dict[str, Any],
        profile: Dict[str, Any],
        current_bundle: Optional[Dict[str, Any]]
    ) -> Tuple[Optional[Dict[str, Any]], bool]:
        """
        Synchronizes the live bundle cart with conversational changes.
        Detects product additions, removals, and upgrades from user messages and advisor replies,
        recalculates deterministic pricing via CatalogService, and returns (updated_bundle, changed).
        """
        if not current_bundle or 'recommended_bundle' not in current_bundle:
            return current_bundle, False

        lower_user = user_message.lower()
        lower_reply = (reply_text or "").lower()

        # Product alias dictionary for natural language mapping to P01-P25
        product_alias_map = {
            "P01": ["p01", "biz fibre 100", "fibre 100", "fiber 100", "100 mbps", "100mbps"],
            "P02": ["p02", "biz fibre 300", "fibre 300", "fiber 300", "300 mbps", "300mbps"],
            "P03": ["p03", "biz fibre 1g", "fibre 1g", "fiber 1g", "1 gbps", "1gbps"],
            "P04": ["p04", "airfiber", "air fiber", "5g airfiber"],
            "P05": ["p05", "leased line 20", "ill 20"],
            "P06": ["p06", "leased line 100", "ill 100"],
            "P07": ["p07", "postpaid 299", "sim 299", "mobile sim"],
            "P08": ["p08", "postpaid 599", "sim 599"],
            "P09": ["p09", "4g failover", "5g failover", "backup failover", "failover", "wireless failover"],
            "P10": ["p10", "sd-wan", "sdwan", "managed sd-wan"],
            "P11": ["p11", "static ip", "fixed ip"],
            "P12": ["p12", "cloud telephony", "sip", "ivr", "business phone"],
            "P13": ["p13", "toll-free", "toll free", "1800", "tollfree"],
            "P14": ["p14", "business sms", "sms 10k", "bulk sms"],
            "P15": ["p15", "whatsapp", "whatsapp api", "whatsapp business"],
            "P16": ["p16", "cloud email", "office suite", "business email", "google workspace"],
            "P17": ["p17", "cloud backup", "tally backup", "1 tb backup", "data backup"],
            "P18": ["p18", "website", "domain starter", "custom domain"],
            "P19": ["p19", "cloud pos", "billing", "upi", "pos machine", "pos device", "card machine"],
            "P20": ["p20", "endpoint security", "antivirus", "anti-virus", "ransomware shield"],
            "P21": ["p21", "firewall", "managed firewall"],
            "P22": ["p22", "guest wifi", "secure wifi", "customer wifi"],
            "P23": ["p23", "cloud cctv", "cctv", "camera", "cameras", "surveillance"],
            "P24": ["p24", "machine monitoring", "iot sensor"],
            "P25": ["p25", "fleet tracker", "gps tracker", "vehicle tracker"]
        }

        # Check intent: Removal vs Addition
        remove_keywords = ["remove", "delete", "drop", "don't need", "dont need", "exclude", "hatao", "nahi chahiye", "cancel", "cut out"]
        is_removal = any(w in lower_user for w in remove_keywords)

        add_keywords = ["add", "include", "more", "want", "need", "aur", "chahiye", "dedo", "plus", "can i add", "can i get", "put in", "upgrade"]
        is_addition = any(w in lower_user for w in add_keywords) or (
            "adding" in lower_reply or "bringing your updated" in lower_reply or "your new all-in-one" in lower_reply
        )

        detected_pids = set()

        # 1. PIDs in gem_res recommended_pids
        for pid in gem_res.get("recommended_pids", []):
            if pid in self.catalog.products:
                detected_pids.add(pid)

        # 2. Explicit PID regex like P19, P23 in user message or reply
        explicit_user_pids = re.findall(r'\b(P\d{2})\b', user_message, re.IGNORECASE)
        for p in explicit_user_pids:
            p_upper = p.upper()
            if p_upper in self.catalog.products:
                detected_pids.add(p_upper)

        # 3. Product keyword matching in user message
        for pid, aliases in product_alias_map.items():
            if any(alias in lower_user for alias in aliases):
                detected_pids.add(pid)

        # Also check reply text for explicit product mentions like "(P19)" or "Cloud POS & Billing (P19)"
        explicit_reply_pids = re.findall(r'\b(P\d{2})\b', reply_text, re.IGNORECASE)
        for p in explicit_reply_pids:
            p_upper = p.upper()
            if p_upper in self.catalog.products and ("add" in lower_reply or "includ" in lower_reply or "bringing your updated" in lower_reply):
                detected_pids.add(p_upper)

        if not detected_pids:
            return current_bundle, False

        items = [dict(i) for i in current_bundle.get("recommended_bundle", [])]
        changed = False

        sites = int(profile.get("num_sites", 1))
        employees = int(profile.get("employee_count", 2))

        for pid in detected_pids:
            prod_meta = self.catalog.get_product(pid)
            if not prod_meta:
                continue

            existing_item = next((i for i in items if i["product_id"] == pid), None)

            if is_removal:
                if existing_item:
                    items = [i for i in items if i["product_id"] != pid]
                    changed = True
            elif is_addition or not existing_item:
                # Handle broadband tier switches (e.g. switching between P01, P02, P03, P04)
                if pid in ["P01", "P02", "P03", "P04"]:
                    items = [i for i in items if i["product_id"] not in ["P01", "P02", "P03", "P04"]]
                    items.insert(0, {"product_id": pid, "quantity": sites if pid in ["P01", "P02", "P03"] else 1, "unit_price": prod_meta.price_min})
                    changed = True
                    continue

                # Determine sizing / quantity
                if pid == "P23":  # CCTV
                    cam_match = re.search(r'(\d+)\s*(?:camera|cctv)', lower_user)
                    qty = int(cam_match.group(1)) if cam_match else max(2, sites * 2)
                elif pid in ["P09", "P10", "P19", "P22"]:  # Per site items
                    qty = sites
                elif pid in ["P07", "P08", "P16", "P20"]:  # Per employee/user
                    qty = max(1, employees)
                elif pid == "P25":  # Fleet tracker per vehicle
                    qty = max(1, sites * 2)
                elif pid == "P24":  # IoT machine sensors
                    qty = 5
                else:
                    qty = 1

                if existing_item:
                    if existing_item.get("quantity") != qty:
                        existing_item["quantity"] = qty
                        changed = True
                else:
                    items.append({
                        "product_id": pid,
                        "quantity": qty,
                        "unit_price": prod_meta.price_min
                    })
                    changed = True

        if changed:
            new_quote = self.catalog.calculate_quote(items)
            updated_bundle = dict(current_bundle)
            updated_bundle["recommended_bundle"] = items
            updated_bundle["quote"] = new_quote
            return updated_bundle, True

        return current_bundle, False

    def process_message(self, session_id: str, message: str, language: str = "en") -> Dict[str, Any]:
        """
        Processes user turn conversationally, checks for objections,
        extracts profile parameters, detects business industry selections/switches,
        and returns verified bundle recommendation with dynamic quick replies.
        """
        lang = language if language in TRANSLATIONS else "en"
        t = TRANSLATIONS[lang]

        # 1. Retrieve session state
        session = self.loop_engine.session_manager.get_session(session_id)
        step = session.get('step', 1)
        profile = session.get('profile', {})

        # 2. Check for objections / hesitation (Loop Engineering)
        objection = self.loop_engine.detect_objections(message)
        if objection and objection.get('detected'):
            handoff_response = (
                f"{t['handoff_prompt']}\n\n"
                f"*(Detected concern: {objection['objections'][0]['detail']}. Routing to nearest partner desk...)*"
            )
            quick_replies = self.get_quick_replies(5, lang, profile.get('segment'))
            return {
                "response_text": handoff_response,
                "step": step,
                "objection_detected": True,
                "objection_details": objection,
                "handoff_ready": True,
                "profile": profile,
                "bundle": session.get('bundle'),
                "quick_replies": quick_replies
            }

        # 3. Conversational State Machine with Gemini Sales Assistant
        msg_clean = message.strip()
        lower_msg = msg_clean.lower()
        response_text = ""
        bundle_data = session.get('bundle')
        action = "NONE"

        history = session.setdefault('history', [])
        history.append({"role": "user", "content": msg_clean})

        # Check explicit intent overrides at any stage
        onboard_keywords = ["onboard", "proceed", "continue", "start kyc", "ready to buy", "buy this", "activate", "haan shuru", "shuru karo", "kar do", "sign me up"]
        pause_keywords = ["wait", "pause", "stop", "hold on", "not now", "ruk jao", "ruko", "change plan", "cancel"]

        if any(w in lower_msg for w in onboard_keywords):
            action = "START_ONBOARDING"
            session['onboarding_active'] = True
            session['step'] = 5
            
            gem_res = GeminiSalesService.process_sales_conversation(
                session_id=session_id,
                user_message=msg_clean,
                history=history,
                current_bundle=bundle_data,
                profile=profile,
                language=lang
            )
            response_text = gem_res.get("reply_text") or (
                "Fantastic! Let's get your business digitally activated.\n\n"
                "**Smart KYC (Paperless DoT Verification)** is starting now. "
                "Please review the DPDP Act consent and upload your business document or test with our 1-tap specimen dossiers below."
            )
            history.append({"role": "assistant", "content": response_text})

            session['profile'] = profile
            self.loop_engine.session_manager.save_session(session_id, session)
            quick_replies = self.get_quick_replies(5, lang, profile.get('segment'))
            return {
                "response_text": response_text,
                "action": "START_ONBOARDING",
                "step": 5,
                "profile": profile,
                "bundle": bundle_data,
                "language": lang,
                "onboarding_active": True,
                "quick_replies": quick_replies
            }

        elif any(w in lower_msg for w in pause_keywords):
            action = "PAUSE_ONBOARDING"
            session['onboarding_active'] = False
            
            gem_res = GeminiSalesService.process_sales_conversation(
                session_id=session_id,
                user_message=msg_clean,
                history=history,
                current_bundle=bundle_data,
                profile=profile,
                language=lang
            )
            response_text = gem_res.get("reply_text") or (
                "Understood! We have paused the onboarding process.\n\n"
                "Take your time to review. What questions do you have about the products, installation, or pricing?"
            )
            history.append({"role": "assistant", "content": response_text})

            session['profile'] = profile
            self.loop_engine.session_manager.save_session(session_id, session)
            quick_replies = self.get_quick_replies(5, lang, profile.get('segment'))
            return {
                "response_text": response_text,
                "action": "PAUSE_ONBOARDING",
                "step": step,
                "profile": profile,
                "bundle": bundle_data,
                "language": lang,
                "onboarding_active": False,
                "quick_replies": quick_replies
            }

        # Check if user is specifying or switching business category (at ANY stage)
        biz_info = self.detect_business_category(msg_clean)
        if biz_info:
            profile['business_input'] = msg_clean
            profile['segment'] = biz_info['segment']
            session['step'] = 2
            session['onboarding_active'] = False
            
            # If switching from an advanced step (step >= 2), give friendly acknowledgment
            if step >= 2:
                ack_template = t.get("switch_ack", "Got it! Switched your business profile to **{business}**.\n\n{ask}")
                response_text = ack_template.format(business=biz_info['business_title'], ask=biz_info['tailored_ask'])
            else:
                response_text = biz_info['tailored_ask'] or t['ask_size']

            history.append({"role": "assistant", "content": response_text})
            session['profile'] = profile
            self.loop_engine.session_manager.save_session(session_id, session)

            quick_replies = self.get_quick_replies(2, lang, profile.get('segment'))
            return {
                "response_text": response_text,
                "action": "SELECT_BUSINESS_TYPE",
                "step": 2,
                "profile": profile,
                "bundle": session.get('bundle'),
                "language": lang,
                "quick_replies": quick_replies
            }

        # If bundle has already been presented (step >= 5), handle as sales assistant Q&A / persuasion
        if step >= 5:
            gem_res = GeminiSalesService.process_sales_conversation(
                session_id=session_id,
                user_message=msg_clean,
                history=history,
                current_bundle=bundle_data,
                profile=profile,
                language=lang
            )
            response_text = gem_res.get("reply_text")
            action = gem_res.get("action", "ANSWER_QUERY")

            if not response_text:
                response_text = (
                    "This tailored bundle provides high-speed enterprise broadband with 99.5% uptime SLA, "
                    "protecting your daily UPI payments and billing. 18% GST input credit is applicable with zero hidden fees.\n\n"
                    "Would you like to customize these options or continue with digital onboarding?"
                )

            # Synchronize any plan customizations (e.g. adding UPI, POS, CCTV, WhatsApp, etc.)
            updated_bundle, changed = self.sync_bundle_customization(msg_clean, response_text, gem_res, profile, bundle_data)
            if changed and updated_bundle:
                bundle_data = updated_bundle
                session['bundle'] = bundle_data

            history.append({"role": "assistant", "content": response_text})
            session['profile'] = profile
            self.loop_engine.session_manager.save_session(session_id, session)
            quick_replies = self.get_quick_replies(5, lang, profile.get('segment'))
            return {
                "response_text": response_text,
                "action": action,
                "step": 5,
                "profile": profile,
                "bundle": bundle_data,
                "language": lang,
                "quick_replies": quick_replies
            }

        # Check if user is asking a question or requesting explanation rather than answering the step question
        question_phrases = [
            "what is", "what are", "why is", "why do", "how does", "how can", "who is",
            "when will", "which one", "where is", "can i", "can you", "could you",
            "tell me", "explain", "details on", "tell about", "kya hai", "kaise",
            "kyu", "batao", "matlab kya", "meaning of", "difference between",
            "who are you", "what can you do"
        ]
        is_user_query = ("?" in msg_clean) or any(p in lower_msg for p in question_phrases)

        if is_user_query:
            gem_res = GeminiSalesService.process_sales_conversation(
                session_id=session_id,
                user_message=msg_clean,
                history=history,
                current_bundle=bundle_data,
                profile=profile,
                language=lang
            )
            ans = gem_res.get("reply_text")
            if not ans:
                if "deliver" in lower_msg:
                    ans = (
                        "Accel Business Digital delivers high-speed business fiber connectivity (100 Mbps to 1 Gbps) "
                        "with 99.5% uptime SLA, automatic 4G/5G failover for zero UPI/POS payment drops, "
                        "and essential business cloud tools (custom email, cloud backup, WhatsApp API) with 10-minute autonomous digital activation."
                    )
                else:
                    ans = (
                        "Accel Business Digital provides complete enterprise connectivity, automated 4G/5G failover, "
                        "cloud business tools, and 100% autonomous digital onboarding with zero paperwork or sales visits."
                    )

            # Check if user query also specifies needs for step 3
            if step == 3:
                profile.setdefault('stated_needs', [])
                for kw in ['cctv', 'camera', 'upi', 'pos', 'hotspot', 'broadband', 'fiber', 'sd-wan', 'cloud', 'backup']:
                    if kw in lower_msg and kw not in [str(n).lower() for n in profile['stated_needs']]:
                        profile['stated_needs'].append(kw.capitalize())

            # Synchronize any plan customizations (e.g. adding UPI, CCTV, etc.)
            updated_bundle, changed = self.sync_bundle_customization(msg_clean, ans, gem_res, profile, bundle_data)
            if changed and updated_bundle:
                bundle_data = updated_bundle
                session['bundle'] = bundle_data

            # DO NOT blindly repeat the generic step question if Gemini's answer already guides the user
            has_question_in_ans = ("?" in ans[-250:]) or any(w in ans[-200:].lower() for w in ["how many", "would you like", "what do you think", "shall we", "ready to"])
            if not has_question_in_ans and step <= 4:
                step_hints = {
                    1: f"\n\n*(Whenever you're ready, let me know your business type to configure your plan)*",
                    2: f"\n\n*(When you're ready, let me know your staff count and site locations)*",
                    3: f"\n\n*(Whenever you're ready, let me know your current internet setup to calculate pricing)*",
                    4: f"\n\n*(Let me know if you have GSTIN or Udyam registration to unlock your quote)*"
                }
                response_text = f"{ans}{step_hints.get(step, '')}"
            else:
                response_text = ans

            history.append({"role": "assistant", "content": response_text})
            session['profile'] = profile
            # DO NOT ADVANCE STEP
            self.loop_engine.session_manager.save_session(session_id, session)
            quick_replies = self.get_quick_replies(step, lang, profile.get('segment'))
            return {
                "response_text": response_text,
                "action": "ANSWER_QUERY",
                "step": step,
                "profile": profile,
                "bundle": bundle_data,
                "language": lang,
                "quick_replies": quick_replies
            }

        if step == 1:
            # Capturing business type / segment
            profile['business_input'] = msg_clean
            # Infer segment
            lower = msg_clean.lower()
            if any(w in lower for w in ['kirana', 'retail', 'shop', 'store', 'salon', 'parlour', 'bakery', 'pharmacy', 'chemist']):
                profile['segment'] = 'Micro retail & services'
            elif any(w in lower for w in ['clinic', 'doctor', 'hospital', 'ca', 'lawyer', 'consultant', 'coaching', 'office']):
                profile['segment'] = 'Professional offices'
            elif any(w in lower for w in ['chain', 'restaurant', 'branches', 'multi', 'outlets', 'logistics', 'fleet', 'transport']):
                profile['segment'] = 'Small multi-site businesses'
            elif any(w in lower for w in ['factory', 'manufacturing', 'textile', 'plant', 'workshop', 'industrial']):
                profile['segment'] = 'Small manufacturers'
            else:
                profile['segment'] = 'Micro retail & services'

            response_text = t['ask_size']
            session['step'] = 2

        elif step == 2:
            # Capturing size & sites
            lower = msg_clean.lower()
            if any(w in lower for w in ['solo', 'just me', 'only me', 'myself', 'alone', 'single owner']):
                profile['employee_count'] = 1
                profile['num_sites'] = 1
            elif '1-3' in lower or '1 to 3' in lower:
                profile['employee_count'] = 2
                profile['num_sites'] = 1
            elif '4-10' in lower or '4 to 10' in lower:
                profile['employee_count'] = 6
                profile['num_sites'] = 2 if any(w in lower for w in ['branch', 'hub', 'site', 'location', 'clinic']) else 1
            elif '10+' in lower or '10 plus' in lower or 'multi' in lower:
                profile['employee_count'] = 12
                profile['num_sites'] = 3
            else:
                numbers = [int(n) for n in re.findall(r'\b\d+\b', msg_clean)]
                if len(numbers) >= 2:
                    profile['employee_count'] = numbers[0]
                    profile['num_sites'] = numbers[1]
                elif len(numbers) == 1:
                    if any(w in lower for w in ['branch', 'site', 'shop', 'office', 'hub', 'location', 'clinic']):
                        profile['employee_count'] = 4
                        profile['num_sites'] = numbers[0]
                    else:
                        profile['employee_count'] = numbers[0]
                        profile['num_sites'] = 1
                else:
                    profile['employee_count'] = 2
                    profile['num_sites'] = 1

            response_text = t['ask_needs']
            session['step'] = 3

        elif step == 3:
            # Capturing stated needs & current setup
            profile['stated_needs'] = [w.strip() for w in msg_clean.split(',')]
            lower = msg_clean.lower()
            if 'hotspot' in lower:
                profile['current_internet'] = 'Mobile Hotspot'
            elif 'broadband' in lower or 'fiber' in lower or 'fibre' in lower:
                profile['current_internet'] = 'Broadband'
            elif 'cctv' in lower:
                profile['current_internet'] = 'Broadband'
                profile['stated_needs'].append('CCTV Surveillance')
            elif 'vpn' in lower or 'cloud' in lower:
                profile['current_internet'] = 'Enterprise Leased Line'

            response_text = t['ask_gstin']
            session['step'] = 4

        elif step == 4:
            # Capturing GSTIN / Registration status & generating bundle
            has_gst = 'Y' if any(w in msg_clean.lower() for w in ['yes', 'haan', 'ha', 'active', 'gst', 'udyam', 'aam', 'registered', 'have']) else 'N'
            profile['has_gstin'] = has_gst
            if 'udyam' in msg_clean.lower():
                profile['has_udyam'] = 'Y'

            # Use LoopEngine to safely execute bundle recommendation with circuit breaker
            def recommend_task():
                return self.catalog.recommend_bundle(profile)

            rec_result, was_fallback, status = self.loop_engine.execute_with_resilience(
                service_name="llm_advisor",
                primary_fn=recommend_task,
                fallback_fn=lambda: self.catalog.recommend_bundle({"segment": profile.get("segment", "Micro retail & services"), "has_gstin": has_gst})
            )

            bundle_data = rec_result
            session['bundle'] = bundle_data
            session['step'] = 5

            # Construct structured plain-language explanation
            items_desc = []
            for item in bundle_data['recommended_bundle']:
                p = self.catalog.get_product(item['product_id'])
                if p:
                    items_desc.append(f"• **{p.product_name}** ({p.category}): ₹{item['unit_price']}/{p.unit} — *{p.description}*")

            q = bundle_data['quote']
            response_text = (
                f"{t['bundle_ready']}\n\n"
                + "\n\n".join(items_desc) + "\n\n"
                + f"**All-in-One Monthly Cost:** ₹{q['monthly_subtotal']} + 18% GST (₹{q['gst_18_pct']}) = **₹{q['grand_monthly_total']}/month**\n\n"
                + f"**One-Time Setup Fee:** ₹{q['one_time_setup_fee']} *(Waived with 12m contract)*\n"
                + f"**Guaranteed Installation:** {q['estimated_install_days']} business days with dedicated engineer support."
            )
            action = "RECOMMEND_BUNDLE"

        history.append({"role": "assistant", "content": response_text})
        # 4. Persist updated session
        session['profile'] = profile
        self.loop_engine.session_manager.save_session(session_id, session)

        quick_replies = self.get_quick_replies(session.get('step', 1), lang, profile.get('segment'))
        return {
            "response_text": response_text,
            "action": action,
            "step": session.get('step', 1),
            "profile": profile,
            "bundle": bundle_data,
            "language": lang,
            "quick_replies": quick_replies
        }
