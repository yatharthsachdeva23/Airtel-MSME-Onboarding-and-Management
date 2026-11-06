import os
import re
from typing import Dict, Any, List, Optional
from backend.catalog_service import CatalogService
from backend.loop_engine import LoopEngine
from backend.gemini_service import GeminiSalesService, get_gemini_api_key

# Multilingual greeting & explanation templates for Pan-India support
TRANSLATIONS = {
    "en": {
        "greeting": "Namaste! Welcome to Airtel Udyam Digital. What kind of business do you run? (e.g., Kirana store, Dental clinic, Restaurant, CA office)",
        "ask_size": "Great! How many staff members work with you, and how many shop/office locations do you have?",
        "ask_needs": "Understood. What are your main daily requirements? (e.g., Fast Wi-Fi for UPI/billing, WhatsApp marketing, Security cameras, Cloud email)",
        "ask_gstin": "Do you have an active GST number or Udyam registration for your business?",
        "bundle_ready": "Here is your tailored **Digital Business Bundle**. We picked these tools specifically for your daily workflow with zero hidden charges:",
        "handoff_prompt": "I noticed you have some questions or concerns. Would you like to connect directly with our local business advisor in your area?"
    },
    "hi": {
        "greeting": "नमस्ते! एयरटेल उद्यम डिजिटल में आपका स्वागत है। आप किस तरह का व्यवसाय चलाते हैं? (जैसे किराना दुकान, क्लिनिक, रेस्टोरेंट, सीए ऑफिस)",
        "ask_size": "बहुत बढ़िया! आपके साथ कितने कर्मचारी काम करते हैं, और आपकी कितनी दुकानें या शाखाएं हैं?",
        "ask_needs": "समझ गया। आपकी मुख्य जरूरतें क्या हैं? (जैसे UPI/बिलिंग के लिए तेज वाई-फाई, व्हाट्सएप मार्केटिंग, सीसीटीवी कैमरा, क्लाउड ईमेल)",
        "ask_gstin": "क्या आपके पास अपने व्यवसाय का सक्रिय GST नंबर या उद्यम रजिस्ट्रेशन है?",
        "bundle_ready": "यह रहा आपके व्यवसाय के लिए तैयार **डिजिटल बिज़नेस बंडल**। हमने इसे आपकी जरूरतों के अनुसार तैयार किया है, बिना किसी छिपे शुल्क के:",
        "handoff_prompt": "लगता है आपके कुछ सवाल या बजट संबंधी शंकाएं हैं। क्या आप अपने नजदीकी एयरटेल लोकल बिजनेस पार्टनर से बात करना चाहेंगे?"
    },
    "ta": {
        "greeting": "வணக்கம்! ஏர்டெல் உத்யம் டிஜிட்டலுக்கு வரவேற்கிறோம். நீங்கள் என்ன தொழில் செய்கிறீர்கள்? (எ.கா. மளிகைக் கடை, கிளினிக், உணவகம்)",
        "ask_size": "உங்கள் கடையில் எத்தனை ஊழியர்கள் பணிபுரிகிறார்கள், எத்தனை கிளைகள் உள்ளன?",
        "ask_needs": "உங்கள் முக்கிய தேவைகள் என்ன? (UPI கட்டணங்களுக்கான அதிவேக Wi-Fi, வாட்ஸ்அப் விளம்பரம், CCTV கேமரா)",
        "ask_gstin": "உங்களிடம் GST எண் அல்லது உத்யம் பதிவு உள்ளதா?",
        "bundle_ready": "உங்கள் வணிகத்திற்கான பிரத்யேக **டிஜிட்டல் வணிக தொகுப்பு** தயார்:",
        "handoff_prompt": "உங்களுக்கு ஏதேனும் சந்தேகங்கள் இருந்தால் எங்கள் உள்ளூர் ஏர்டெல் ஆலோசகரிடம் பேச விரும்புகிறீர்களா?"
    },
    "bn": {
        "greeting": "নমস্কার! এয়ারটেল উদ্যম ডিজিটালে আপনাকে স্বাগতম। আপনি কী ধরণের ব্যবসা করেন? (যেমন মুদি দোকান, ক্লিনিক, রেস্তোরাঁ)",
        "ask_size": "আপনার প্রতিষ্ঠানে কতজন কর্মচারী কাজ করেন এবং কতগুলি শাখা রয়েছে?",
        "ask_needs": "আপনার মূল প্রয়োজন কী? (UPI/বিলিংয়ের জন্য দ্রুত ওয়াই-ফাই, হোয়াটসঅ্যাপ প্রচার, সিসিটিভি ক্যামেরা)",
        "ask_gstin": "আপনার কি কোনো জিএসটি (GST) বা উদ্যম রেজিস্ট্রেশন নম্বর আছে?",
        "bundle_ready": "আপনার ব্যবসার জন্য বিশেষভাবে তৈরি **ডিজিটাল বিজনেস বান্ডিল**:",
        "handoff_prompt": "আপনার কি কোনো প্রশ্ন রয়েছে? আপনি কি আমাদের স্থানীয় পরামর্শদাতার সাথে সরাসরি কথা বলতে চান?"
    },
    "te": {
        "greeting": "నమస్కారం! ఎయిర్‌టెల్ ఉద్యమ్ డిజిటల్‌కి స్వాగతం. మీ వ్యాపారం ఏమిటి? (ఉదా. కిరాణా షాప్, క్లినిక్, రెస్టారెంట్)",
        "ask_size": "మీ వద్ద ఎంతమంది సిబ్బంది పనిచేస్తున్నారు మరియు ఎన్ని బ్రాంచీలు ఉన్నాయి?",
        "ask_needs": "మీ ముఖ్యమైన అవసరాలు ఏమిటి? (UPI కోసం వేగవంతమైన Wi-Fi, వాట్సాప్ ప్రచారం, CCTV కెమెరాలు)",
        "ask_gstin": "మీకు GST లేదా ఉద్యమ్ రిజిస్ట్రేషన్ ఉందా?",
        "bundle_ready": "మీ వ్యాపారం కోసం ప్రత్యేకంగా రూపొందించిన **డిజిటల్ బిజినెస్ బండిల్** సిద్ధంగా ఉంది:",
        "handoff_prompt": "మీకు ఏమైనా సందేహాలు ఉంటే మా స్థానిక నిపుణుడితో మాట్లాడాలనుకుంటున్నారా?"
    },
    "mr": {
        "greeting": "नमस्कार! एअरटेल उद्यम डिजिटलमध्ये आपले स्वागत आहे. आपला कोणता व्यवसाय आहे? (उदा. किराणा दुकान, क्लिनिक, हॉटेल)",
        "ask_size": "आपल्याकडे किती कर्मचारी काम करतात आणि किती दुकाने किंवा शाखा आहेत?",
        "ask_needs": "आपल्या मुख्य गरजा काय आहेत? (UPI/बिलिंगसाठी फास्ट वाय-फाय, व्हॉट्सॲप मार्केटिंग, सीसीटीव्ही)",
        "ask_gstin": "आपल्याकडे GST नंबर किंवा उद्यम नोंदणी आहे का?",
        "bundle_ready": "आपल्या व्यवसायासाठी तयार **डिजिटल बिझनेस बंडल**:",
        "handoff_prompt": "आपल्याला काही प्रश्न किंवा शंका असल्यास आमच्या स्थानिक सल्लागाराशी बोलायचे आहे का?"
    }
}

class AdvisorEngine:
    def __init__(self, catalog_service: Optional[CatalogService] = None, loop_engine: Optional[LoopEngine] = None):
        self.catalog = catalog_service or CatalogService()
        self.loop_engine = loop_engine or LoopEngine()

    def process_message(self, session_id: str, message: str, language: str = "en") -> Dict[str, Any]:
        """
        Processes user turn conversationally, checks for objections,
        extracts profile parameters, and returns verified bundle recommendation.
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
            return {
                "response_text": handoff_response,
                "step": step,
                "objection_detected": True,
                "objection_details": objection,
                "handoff_ready": True,
                "profile": profile,
                "bundle": session.get('bundle')
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
            return {
                "response_text": response_text,
                "action": "START_ONBOARDING",
                "step": 5,
                "profile": profile,
                "bundle": bundle_data,
                "language": lang,
                "onboarding_active": True
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
            return {
                "response_text": response_text,
                "action": "PAUSE_ONBOARDING",
                "step": step,
                "profile": profile,
                "bundle": bundle_data,
                "language": lang,
                "onboarding_active": False
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

            history.append({"role": "assistant", "content": response_text})
            session['profile'] = profile
            self.loop_engine.session_manager.save_session(session_id, session)
            return {
                "response_text": response_text,
                "action": action,
                "step": 5,
                "profile": profile,
                "bundle": bundle_data,
                "language": lang
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
            elif any(w in lower for w in ['chain', 'restaurant', 'branches', 'multi', 'outlets']):
                profile['segment'] = 'Small multi-site businesses'
            elif any(w in lower for w in ['factory', 'manufacturing', 'textile', 'plant', 'workshop', 'industrial']):
                profile['segment'] = 'Small manufacturers'
            else:
                profile['segment'] = 'Micro retail & services'

            response_text = t['ask_size']
            session['step'] = 2

        elif step == 2:
            # Capturing size & sites
            numbers = [int(n) for n in re.findall(r'\b\d+\b', msg_clean)]
            if numbers:
                profile['employee_count'] = numbers[0]
                profile['num_sites'] = numbers[1] if len(numbers) > 1 else 1
            else:
                profile['employee_count'] = 2
                profile['num_sites'] = 1

            response_text = t['ask_needs']
            session['step'] = 3

        elif step == 3:
            # Capturing stated needs
            profile['stated_needs'] = [w.strip() for w in msg_clean.split(',')]
            response_text = t['ask_gstin']
            session['step'] = 4

        elif step == 4:
            # Capturing GSTIN / Registration status & generating bundle
            has_gst = 'Y' if any(w in msg_clean.lower() for w in ['yes', 'haan', 'ha', 'active', 'gst', 'udyam', 'aam']) else 'N'
            profile['has_gstin'] = has_gst

            # Use LoopEngine to safely execute bundle recommendation with circuit breaker
            def recommend_task():
                return self.catalog.recommend_bundle(profile)

            rec_result, was_fallback, status = self.loop_engine.execute_with_resilience(
                service_name="llm_advisor",
                primary_fn=recommend_task,
                fallback_fn=lambda: self.catalog.recommend_bundle({"segment": "Micro retail & services", "has_gstin": "N"})
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

        return {
            "response_text": response_text,
            "action": action,
            "step": session.get('step', 1),
            "profile": profile,
            "bundle": bundle_data,
            "language": lang
        }
