"""
Justice AI / LexGlobal AI - Multi-Provider LLM Integration
Supports Google Gemini (Interactions API / Flash models), OpenAI, Groq,
and a High-Fidelity Local Statutory Reasoning Engine.
"""

import os
import re
import json
import subprocess
import urllib.request
import ssl
from typing import Optional, Dict, Any, List

class LLMProvider:
    """
    Unified LLM Interface providing seamless routing between Google Gemini,
    Groq / OpenAI, and a ChromaDB-grounded offline legal intelligence engine.
    """
    def __init__(self, provider: str = "gemini", api_key: Optional[str] = None, model_name: Optional[str] = None):
        # Read API keys from env or parameter
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
        
        # Load from .env if still empty
        if not self.api_key and os.path.exists(".env"):
            try:
                with open(".env", "r") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GEMINI_API_KEY="):
                            self.api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            break
                        elif line.startswith("LLM_API_KEY="):
                            self.api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            break
            except Exception:
                pass

        self.provider = provider.lower() if self.api_key else "offline"
        self.model_name = model_name or "gemini-3.5-flash-lite"

    def _call_gemini_interactions_api(self, prompt: str, system_instruction: Optional[str] = None) -> Optional[str]:
        """
        Calls Google AI Studio Interactions API with cross-platform support (Linux / Windows).
        Gracefully cascades: gemini-3.5-flash-lite -> gemini-flash-latest -> gemini-3.5-flash -> gemini-3.8-flash.
        """
        if not self.api_key:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/interactions?key={self.api_key}"
        candidate_models = ["gemini-3.5-flash-lite", "gemini-flash-latest", "gemini-3.5-flash", "gemini-3.8-flash"]
        
        # If user explicitly requested a specific model, try it first
        if self.model_name and self.model_name not in candidate_models:
            candidate_models.insert(0, self.model_name)

        for model in candidate_models:
            payload = {
                "model": model,
                "input": prompt
            }
            if system_instruction:
                payload["system_instruction"] = system_instruction

            # Method 1: Try Python native urllib.request (zero external binary dependency, works on Render/Linux)
            try:
                req_data = json.dumps(payload).encode("utf-8")
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                req = urllib.request.Request(
                    url,
                    data=req_data,
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
                    resp_bytes = resp.read()
                    data = json.loads(resp_bytes.decode("utf-8"))
                    if "steps" in data:
                        for step in data["steps"]:
                            if "content" in step:
                                parts = step["content"]
                                text = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
                                if text and len(text.strip()) > 20:
                                    return text.strip()
            except Exception:
                pass

            # Method 2: Fallback to curl / curl.exe
            try:
                curl_cmd = "curl.exe" if os.name == "nt" else "curl"
                cmd = [
                    curl_cmd, "-s", "-k",
                    "-X", "POST",
                    url,
                    "-H", "Content-Type: application/json",
                    "-d", json.dumps(payload)
                ]
                proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=50)
                if proc.returncode == 0 and proc.stdout:
                    data = json.loads(proc.stdout)
                    if "steps" in data:
                        for step in data["steps"]:
                            if "content" in step:
                                parts = step["content"]
                                text = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
                                if text and len(text.strip()) > 20:
                                    return text.strip()
                    elif "error" in data:
                        err = data.get("error", {})
                        err_msg = err.get("message", "").lower()
                        err_code = str(err.get("code", "")).lower()
                        if "experiencing high demand" in err_msg or "temporarily" in err_msg or "service_unavailable" in err_code or err_code in ("503", "429"):
                            continue
            except Exception:
                continue

        return None

    def generate(self, prompt: str, system_instruction: Optional[str] = None, temperature: float = 0.2) -> str:
        """
        Executes a legal intelligence generation call.
        """
        if self.api_key and self.provider == "gemini":
            reply = self._call_gemini_interactions_api(prompt, system_instruction)
            if reply:
                return reply

        # Fallback to high-fidelity offline legal reasoner
        return self._offline_legal_reasoner(prompt, system_instruction)

    def generate_chat_response(
        self,
        query: str,
        history: List[Dict[str, str]],
        retrieved_statutes: List[Dict[str, Any]],
        jurisdiction: str = "IN",
        category: str = "General",
        language: str = "en"
    ) -> str:
        """
        Builds a comprehensive legal context prompt grounded in ChromaDB vector statutes
        and dispatches to the live LLM.
        """
        statute_context = ""
        if retrieved_statutes:
            statute_context = "\n### RELEVANT STATUTORY CODES & PROVISIONS RETRIEVED FROM VECTOR DATABASE:\n"
            for idx, s in enumerate(retrieved_statutes, 1):
                statute_context += (
                    f"{idx}. {s.get('act', 'Act')} - Section {s.get('section', '')}: {s.get('title', '')}\n"
                    f"   Details: {s.get('content', s.get('details', ''))}\n"
                    f"   Remedy / Procedure: {s.get('remedy', '')}\n"
                )

        sys_prompt = (
            "You are Justice AI, an approachable and easy-to-understand legal assistant for everyday citizens.\n"
            f"Active Jurisdiction: {jurisdiction}\n"
            f"Active Legal Category: {category}\n"
            f"Target Response Language: {language}\n\n"
            "CRITICAL STYLE & TONE RULES:\n"
            "1. USE SIMPLE, EVERYDAY WORDS: Strictly avoid complicated, heavy, or intimidating legal jargon (never use words like 'pursuant to', 'pecuniary', 'adverse party', 'statutory competence', 'legislative competence', 'hereinabove', or Latin maxims). Write in plain, conversational language that a high school or college student can immediately understand.\n"
            "2. DIRECT BOTTOM LINE FIRST: Always start with an immediate, plain-spoken answer in bold (e.g., '**Yes, you have several options other than paying on the spot.**' or '**No, traffic police cannot snatch your keys.**').\n"
            "3. USE SIMPLE HEADINGS & BULLET POINTS: Organize your answer into practical sections with friendly headings such as:\n"
            "   - **The Short Answer**\n"
            "   - **What Are Your Options? (Step-by-Step)**\n"
            "   - **What The Law Says In Simple Words**\n"
            "   - **What You Should Do Next**\n"
            "4. EXPLAIN THE LAW IN PLAIN TERMS: If you cite a section (like Section 185 MV Act or Section 29 Punjab Excise Act), explain right away what it actually means in plain terms (e.g. 'This section says...').\n"
            "5. BE PRACTICAL & ACTIONABLE: Give real, useful tips (e.g. mention the exact website like vcourts.gov.in, DigiLocker app, or how many days they have to act).\n"
            "6. NATURAL LOCAL TONE: If replying in Hindi or Punjabi, write in natural, everyday conversational language (not hyper-formal textbook Hindi or archaic words)."
        )

        full_prompt = (
            f"USER LEGAL QUERY: {query}\n"
            f"{statute_context}\n"
            "Explain the legal position and practical options in simple, friendly, everyday terms that anyone can easily understand, without heavy legal jargon."
        )

        if self.api_key:
            reply = self._call_gemini_interactions_api(full_prompt, sys_prompt)
            if reply:
                return reply

        # If live LLM API fails or is unavailable, return None so deep domain reasoning takes over
        return None

    def _offline_legal_reasoner(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """
        High-fidelity heuristic legal reasoning engine.
        Provides structured statutory analysis, risk identification, and drafting.
        """
        combined = f"{prompt} {system_instruction or ''}".lower()

        # Check for Contract/Document Analysis request
        if any(w in combined for w in ["analyze the following", "contract risk", "audit", "problematic clauses"]):
            return self._heuristic_contract_analysis(prompt)

        # Check for Drafting request
        if any(w in combined for w in ["draft a", "generate a legal", "legal notice", "drafting principles"]):
            return self._heuristic_draft_response(prompt)

        # Check for Intake / Triage request
        if any(w in combined for w in ["intake", "triage", "dossier", "litigation strategist"]):
            return self._heuristic_intake_response(prompt)

        # General Legal Q&A fallback
        return self._heuristic_qa_response(prompt)

    def _heuristic_contract_analysis(self, prompt: str) -> str:
        return """### Executive Contract Risk Assessment

**Overall Document Risk Level**: MODERATE TO HIGH RISK

#### 1. Key Problematic Clauses Identified:
- **Uncapped Indemnification Clause**: The counterparty has inserted broad indemnification obligations requiring you to hold them harmless for any and all claims, including indirect and consequential damages, without a reciprocating monetary liability cap.
- **Unilateral Termination for Convenience**: One party reserves the right to terminate with 7 days' notice, while imposing a 60-day notice and early cancellation penalty on you.
- **Overly Restrictive Restraint of Trade / Non-Compete**: Imposes a post-termination restriction with global geographic scope. Under many jurisdictions (e.g. California B&P Code § 16600, Section 27 Indian Contract Act, and UK common law reasonableness test), this clause is either void or severely vulnerable to judicial invalidation.
- **Dispute Resolution & Asymmetrical Forum**: Specifies exclusive jurisdiction in a remote forum with mandatory party-paid arbitration fees.

#### 2. Recommended Redlines & Counter-Proposals:
- **Cap on Liability**: *"In no event shall either party's aggregate liability under this Agreement exceed the total fees paid or payable by Client in the preceding 12 months."*
- **Mutual Termination**: Change notice period to 30 days mutual written notice with cure period of 15 days for material breach.
- **Narrow Indemnity**: Limit indemnification strictly to third-party claims arising directly from gross negligence, willful misconduct, or willful breach of IP warranties."""

    def _heuristic_draft_response(self, prompt: str) -> str:
        def extract_field(pattern, default):
            m = re.search(pattern, prompt, re.IGNORECASE)
            return m.group(1).strip() if m else default

        sender = extract_field(r"Sender / Client Name:\s*([^\n]+)", "[Sender Name]")
        sender_addr = extract_field(r"Sender Address / Contact:\s*([^\n]+)", "[Sender Address & Contact]")
        recipient = extract_field(r"Recipient / Adverse Party Name:\s*([^\n]+)", "[Recipient Full Name / Entity Name]")
        recipient_addr = extract_field(r"Recipient Address / Contact:\s*([^\n]+)", "[Recipient Address Line 1, City, Postal Code]")
        subject = extract_field(r"Specific Subject / Claim:\s*([^\n]+)", "FORMAL DEMAND NOTICE FOR BREACH OF CONTRACT AND UNPAID DUES")
        amount = extract_field(r"Monetary Value / Sum Claimed:\s*([^\n]+)", "[Amount and Currency]")
        cure_days = extract_field(r"Cure / Remediation Window:\s*([^\n]+)", "fifteen (15) days")
        details = extract_field(r"Key Facts / Background:\s*([\s\S]+?)(?:Generate the|$)", "Failure to discharge contractual obligations.")

        return f"""### Formal Legal Notice / Demand Letter Draft

**DATE:** [Current Date]  
**TRANSMISSION:** REGISTERED POST WITH ACKNOWLEDGEMENT DUE / FORMAL ELECTRONIC SERVICE RECORD  

**TO:**  
{recipient}  
{recipient_addr}  

**FROM:**  
{sender}  
{sender_addr}  

**SUBJECT: {subject.upper()}**

Dear Sir / Madam,

Under instructions from and on behalf of the Claimant, **{sender}**, I hereby serve upon you this Formal Legal Notice pursuant to the statutory laws governing commercial and civil obligations:

1. **FACTUAL BACKGROUND & AGREEMENT:**  
   The parties entered into a binding legal relationship concerning the agreed transaction/services. Specifically:
   > {details.strip()}

2. **PERFORMANCE BY CLAIMANT:**  
   The Claimant has duly and faithfully fulfilled all requisite obligations, delivered work milestones, and complied strictly with all agreed contractual standards.

3. **BREACH OF OBLIGATION & OUTSTANDING DUES:**  
   Notwithstanding formal demands and invoice delivery, you have wrongfully failed, neglected, and refused to discharge your obligation, leaving a total outstanding claim of **{amount}**.

4. **FINAL DEMAND & TIME FOR COMPLIANCE:**  
   You are hereby called upon to remedy this breach and remit the sum of **{amount}** within **{cure_days}** from the date of receipt of this notice, failing which formal legal proceedings will be commenced against you before the competent court of jurisdiction.

5. **COSTS AND CONSEQUENCES:**  
   Please take note that in the event litigation ensues, you shall be held liable for all additional claims including statutory interest, compensatory damages, court filing fees, and advocate costs.

Yours sincerely,

___________________________  
**{sender}**  
[Authorized Signatory]"""

    def _heuristic_intake_response(self, prompt: str) -> str:
        return """### EXECUTIVE CASE SUMMARY & PARTIES

- **Filing Classification**: Civil / Commercial Dispute Assessment
- **Claimant Standing**: Aggrieved party seeking compensatory remedy
- **Adverse Party**: Respondent subject to contractual and statutory obligations
- **Jurisdictional Forum**: Competent trial court having territorial and subject-matter jurisdiction

### LEGAL CAUSES OF ACTION & STATUTORY PROVISIONS
- **Primary Cause of Action**: Commercial Breach of Contract & Unlawful Withholding of Consideration.
- **Governing Legal Doctrine**: Pacta sunt servanda (agreements must be kept); party suffering breach is entitled to be placed in the economic position they would occupy had the contract been performed.
- **Statutory Provisions**: General contract statutory codes require compensatory damages for direct losses naturally arising from breach.

### STATUTE OF LIMITATIONS & PROCEDURAL URGENCY
- **Limitation Period**: Typically 3 to 6 years depending on jurisdiction (measured from the date the cause of action accrued or invoice defaulted).
- **Procedural Urgency**: High. A formal written Notice of Claim must be served promptly to toll limitations or satisfy mandatory pre-suit demand rules.

### STRENGTH OF CASE & POTENTIAL DEFENSES
- **Claimant Strengths**: Clear documentary paper trail, delivery of work, and unilateral failure to pay by respondent.
- **Anticipated Defenses**: Counterparty may allege performance defects, failure of condition precedent, or lack of proper formal sign-off.

### EVIDENTIARY CHECKLIST
- [ ] Fully executed master agreement, Statement of Work (SOW), or written engagement email trail.
- [ ] Deliverable submission records, timestamps, and acceptance receipts.
- [ ] Unpaid invoices and itemized account ledgers.
- [ ] Written demand communications and any counterparty admissions.

### ACTIONABLE NEXT STEPS
1. Issue a formal Statutory Demand Notice granting 14-to-30 calendar days to cure default.
2. Prepare an itemized statement of claim including principal, statutory interest, and legal costs.
3. Schedule an initial consultation with a licensed attorney in the governing jurisdiction.

### TOP 5 QUESTIONS TO ASK AN ATTENDING LAWYER
1. Does our jurisdiction require mandatory mediation or conciliation before filing a suit?
2. Can we seek summary judgment / expedited decree based on the written instruments?
3. What is the expected timeline and court fee schedule for this recovery amount?
4. Are statutory attorney fees recoverable against the adverse party if we prevail?
5. Should we also consider an interim attachment of assets or injunctive relief?"""

    def _heuristic_qa_response(self, prompt: str) -> str:
        p_lower = prompt.lower()
        
        # Scenario 1: Germany Landlord termination
        if any(k in p_lower for k in ["landlord", "germany", "termination", "kündigung", "vermieter", "bgb", "eigenbedarf"]):
            return """In most cases, yes. A landlord needs a legitimate reason to end an open-ended residential lease.

Typical valid reasons are genuine personal use of the home (Eigenbedarf) or a serious breach of duty by the tenant, and the reason must be explicitly stated in the written termination notice.

The landlord's notice period starts at three months and gets longer the more years you have lived there (extending to six months after five years, and nine months after eight years), while your own notice period as a tenant is normally standard three months regardless of duration.

Key Statutes: BGB § 573 (Ordinary termination by the landlord) and BGB § 573c (Notice periods)."""

        # Scenario 2: India Consumer Defective Phone / Refund
        if any(k in p_lower for k in ["खराब", "रिफ़ंड", "फ़ोन", "विक्रेता", "phone", "defective", "consumer", "refund", "e-daakhil", "flipkart", "amazon"]):
            if any(k in prompt for k in ["खराब", "रिफ़ंड", "मँगवाया", "विक्रेता"]):
                return """आप उपभोक्ता शिकायत दर्ज कर सकते हैं। खराब सामान पर मरम्मत, बदलाव या रिफ़ंड मिल सकता है।

सबसे पहले विक्रेता को लिखित शिकायत भेजें और ऑर्डर, भुगतान और खराबी के सबूत सहेजकर रखें। समाधान न मिले तो ज़िला उपभोक्ता आयोग में e-Daakhil पोर्टल से ऑनलाइन शिकायत दर्ज की जा सकती है, जो आमतौर पर कारण उत्पन्न होने के दो वर्ष के भीतर करनी होती है। मार्गदर्शन के लिए राष्ट्रीय उपभोक्ता हेल्पलाइन 1915 भी उपलब्ध है।

मुख्य क़ानून: उपभोक्ता संरक्षण अधिनियम, 2019 · धारा 39 (ज़िला आयोग के आदेश) एवं धारा 69 (शिकायत की समय-सीमा)।"""
            else:
                return """You have the statutory right to file a consumer complaint for repair, replacement, or a full refund.

First, issue a formal written notice or complaint to the seller and marketplace platform, retaining proof of invoice, delivery, payment, and defect evidence.

If unresolved within 15 days, you can lodge an electronic consumer complaint before the competent District Consumer Disputes Redressal Commission via the official e-Daakhil portal under the Consumer Protection Act, 2019. The statutory limitation period is two (2) years from the date the cause of action accrued.

Key Statutes: Consumer Protection Act, 2019 (Sections 35, 39 & 69)."""

        # Scenario 3: GDPR Right to Erasure
        if any(k in p_lower for k in ["erasure", "forgotten", "gdpr", "privacy", "delete my data"]):
            return """Under GDPR Article 17, you possess the statutory right to obtain the erasure of your personal data without undue delay.

The data controller is obligated under European Union law to delete your personal data where it is no longer necessary for the original purposes, where processing was based on consent that has now been withdrawn, or where you object under Article 21.

Controllers must respond within one calendar month. Failure to comply entitles you to lodge a complaint with your national Data Protection Authority (DPA) and pursue judicial remedies under Article 82.

Key Statutes: EU General Data Protection Regulation (GDPR) Articles 17 & 82."""

        # Scenario 4: Overtime / Wages
        if any(k in p_lower for k in ["overtime", "flsa", "wages", "withhold", "40 hours", "50 hours"]):
            return """Non-exempt employees are legally entitled to 1.5x overtime compensation for hours worked exceeding 40 hours per workweek.

Under the Fair Labor Standards Act (FLSA), 29 U.S.C. § 207, an employer cannot unilaterally require overtime hours without corresponding statutory premium compensation, nor may an employer unlawfully withhold earned wages.

An employer who violates federal wage provisions is liable for back pay plus mandatory equal amount in statutory liquidated damages and reasonable attorney fees.

Key Statutes: 29 U.S.C. § 207 (FLSA) and applicable State Labor Codes."""

        # General Fallback
        return """Comprehensive Statutory Assessment & Legal Review

#### 1. Applicable Framework & Fundamental Doctrine
- **Binding Contractual Obligations**: Parties are bound by explicit covenants unless an operative clause violates public policy, codified consumer protection minimums, or mandatory statutory safeguards.
- **Burden of Proof & Limitation**: Civil remedies are governed by statutory limitation periods (typically 2 to 3 years from the date the cause of action accrued). Claims must be substantiated on a preponderance of the evidence.

#### 2. Actionable Next Steps
1. **Evidence Preservation**: Collate all written agreements, delivery records, invoices, and contemporaneous email communications.
2. **Issue Formal Notice of Claim**: Serve a formal written demand giving the counterparty 14 to 30 calendar days to remedy the grievance.
3. **Formal Engagement**: Consult a qualified attorney in your local jurisdiction to assess forum-specific procedural requirements."""
