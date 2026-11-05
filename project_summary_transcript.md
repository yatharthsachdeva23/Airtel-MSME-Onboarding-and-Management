# Project Udyam Digital — Master Reference & Blueprint

---

## 1. User's Vision (Exact Transcript)

> *"Starting from that, we have a telecom company that provides multiple services, and there are tons of customers. And we have to develop a system or like whole software, whatever we can say, in which we have to start from marketing to telling people—it's basically, what I understood, a part of their main app that we have to develop.*
> 
> *Just like they have for the SIM—the SIM part is just a small version of this thing. We have to make the big version of the already existing thing: first market to them in notifications or in the app with benefits and packages. When they click, it means they are interested MSMEs.*
> 
> *When they click and we know they are interested, we start the onboarding process without any human—automating it completely with AI and an automation pipeline:*
> 
> * *We start with an AI assistant in their local native language that they preferred, acting like a consultant or advisor.*
> * *The AI advisor in the app knows everything about our telecom network, like a RAG pipeline. It understands the whole system and what we can provide.*
> * *It asks the user their specifications, suggests a proper plan, allows proper modifications quickly, with no delays because it's an automated pipeline.*
> * *Because we have to do onboarding as well, we don't just stop at the advisor—we start the onboarding process where AI actively helps by asking the user to submit documents.*
> * *We must follow the DPDP Act and all legal requirements.*
> * *It requires KYC verification done by our system only, with AI assisting on top of it at every stage."*

---

## 2. Summary of What We Have to Make (Quick Reference Points)

### Pillar 1: In-App Discovery & Entry Hook
* **Feature:** Digital entry point inside the telco app / SMS / WhatsApp banner targeted at MSME owners.
* **Goal:** Zero friction transition from lead generation directly into the digital onboarding journey.

### Pillar 2: Multilingual Conversational AI Advisor (RAG-Powered)
* **Feature:** Voice/Text assistant speaking native Indian languages (Hindi, English, etc.).
* **Knowledge Engine (RAG):** Full catalog intelligence (25 products, tier availability, minimum sites/employees, required dependencies).
* **Consultative Flow:** Asks 3–4 practical business questions (business type, staff size, daily needs like billing, POS, CCTV) and recommends the optimal bundle.
* **Plain-Language Explanation:** Explains *why* each service is recommended without technical telecom jargon.

### Pillar 3: Transparent Instant Quote & Customizer
* **Feature:** One-click transparent pricing screen with single monthly total + one-time installation breakdown.
* **Interactive Toggles:** Let the owner easily adjust add-ons (extra SIMs, speed upgrades, additional CCTV cameras) with live price updates.
* **Eliminates Delay:** Removes the 3–5 day wait for cryptic PDF quotes.

### Pillar 4: Smart Instant KYC & Verification
* **Feature:** Automated document capture and verification right on the smartphone.
* **OCR & Registry Validation:** Reads uploaded GST certificate, Udyam certificate, address proof, or signatory ID and validates against mock registries (`mock_gstin_registry.csv`, `mock_udyam_registry.csv`).
* **Error Detection:** Automatically catches planted issues (expired documents >90 days, cancelled/suspended GSTINs, mismatched company/signatory names).
* **DPDP Act 2023 Compliance:** Explicit consent flow, data minimization, and PII masking (masking Aadhaar/PAN).

### Pillar 5: Self-Serve Live Order Tracker
* **Feature:** Visual timeline (Order Placed $\to$ KYC Approved $\to$ Engineer Dispatched $\to$ Hardware Installed $\to$ Active).
* **Goal:** Dynamic ETA based on product install lead times (2 days for 5G AirFiber vs 5 days for Fiber), eliminating customer chase calls.

### Pillar 6: Submission Deliverables Required
1. **Working Prototype:** Full code repository + 3-minute video walkthrough.
2. **Solution Architecture Diagram:** Data flows between app, GenAI/RAG advisor, OCR engine, and backend registries.
3. **10-Slide Pitch Deck:** Using `Submission Template_Sync.pptx` (customer segments, value prop, unit economics, rollout plan, risks).
4. **1-Page Data Privacy Note:** Documenting compliance with the Digital Personal Data Protection Act, 2023.
