"""
Jurisdiction Engine for LexGlobal AI
Provides dynamic multi-jurisdictional detection, cross-border analysis, and statutory context mapping.
"""

import re
from typing import Dict, Any, List, Tuple
from core.config import JURISDICTIONS, EMERGENCY_HOTLINES

# Keyword mappings for dynamic jurisdiction detection
JURISDICTION_INDICATORS: Dict[str, List[str]] = {
    "IN": [
        "india", "indian", "bns", "ipc", "bnss", "crpc", "bsa", "delhi", "mumbai", "bengaluru",
        "high court", "supreme court of india", "section 420", "section 138", "ni act",
        "cheque bounce", "labour court", "fir", "vakalatnama", "advocate", "rs.", "inr",
        "rupees", "lakh", "crore", "aadhaar", "pan card", "rbi", "sebi", "consumer forum",
        "ncdrc", "rera", "dpdp", "arbitration and conciliation act"
    ],
    "US": [
        "united states", "usa", "u.s.", "america", "california", "new york", "delaware",
        "texas", "florida", "irs", "401k", "w-2", "1099", "title vii", "eeoc", "flsa",
        "ada", "ccpa", "cpra", "llc", "c-corp", "delaware c-corp", "at-will", "non-compete",
        "dmca", "sec", "doj", "supreme court of the united states", "scotus", "circuit court",
        "miranda", "ucc", "subpoena", "attorney-client privilege", "dollars", "$"
    ],
    "UK": [
        "united kingdom", "uk", "britain", "england", "wales", "scotland", "northern ireland",
        "london", "hmrc", "companies house", "crown court", "magistrates", "county court",
        "barrister", "solicitor", "tribunal", "employment rights act", "tupe", "statutory redundancy",
        "pounds", "£", "gbp", "cpr", "high court of justice", "king's bench", "chancery",
        "consumer rights act", "sra", "acas"
    ],
    "EU": [
        "european union", "eu", "gdpr", "brussels", "cjeu", "directive", "regulation (eu)",
        "cross-border data transfer", "standard contractual clauses", "sccs", "data protection officer",
        "dpo", "edpb", "digital services act", "dsa", "dma", "ai act", "euro", "€"
    ],
    "CA": [
        "canada", "canadian", "ontario", "quebec", "british columbia", "alberta", "toronto",
        "vancouver", "pipeda", "canada labour code", "charter of rights and freedoms",
        "supreme court of canada", "cra", "gst/hst", "provincial court", "c$"
    ],
    "AU": [
        "australia", "australian", "sydney", "melbourne", "new south wales", "queensland",
        "victoria", "fair work ombudsman", "fair work act", "accc", "asic", "ato", "high court of australia",
        "australian consumer law", "acl", "superannuation", "a$"
    ],
    "SG": [
        "singapore", "singaporean", "pdpa", "mom", "ministry of manpower", "siac",
        "singapore international arbitration centre", "employment act", "cpib", "mas",
        "monetary authority of singapore", "subordinate courts", "state courts", "s$"
    ],
    "DE": [
        "germany", "deutschland", "german", "berlin", "munich", "frankfurt", "bgb", "stgb",
        "hgb", "bundesgerichtshof", "bgh", "bundesverfassungsgericht", "arbeitsgericht",
        "gmbh", "ag", "abmahnung", "kuendigung", "betriebsrat"
    ],
    "FR": [
        "france", "french", "paris", "code civil", "code penal", "code du travail",
        "cour de cassation", "prud'hommes", "prudhommes", "sarl", "sas", "urssaf"
    ],
    "AE": [
        "united arab emirates", "uae", "dubai", "abu dhabi", "difc", "adgm", "free zone",
        "labour law", "mohre", "civil transactions", "dirham", "aed", "sharia"
    ],
    "ZA": [
        "south africa", "south african", "johannesburg", "cape town", "pretoria",
        "popia", "ccma", "labour court", "constitutional court", "rand", "zar"
    ]
}


def detect_jurisdiction(text: str) -> Tuple[str, float]:
    """
    Analyzes text to infer the most likely jurisdiction.
    Uses the trained Machine Learning Jurisdiction Classifier (TF-IDF + Calibrated L-BFGS),
    with fallback to symbolic indicator scoring.
    Returns (jurisdiction_code, confidence_score 0.0-1.0).
    """
    if not text:
        return ("GLOBAL", 0.0)

    # 1. First, attempt inference using our trained Machine Learning Model
    try:
        import os
        import joblib
        import numpy as np
        model_path = os.path.join(os.path.dirname(__file__), "..", "models", "jurisdiction_classifier.joblib")
        if os.path.exists(model_path):
            ml_model = joblib.load(model_path)
            probs = ml_model.predict_proba([text])[0]
            classes = ml_model.classes_
            top_idx = int(np.argmax(probs))
            ml_jur = str(classes[top_idx])
            ml_conf = float(probs[top_idx])
            if ml_conf >= 0.45:
                return (ml_jur, round(ml_conf, 2))
    except Exception:
        pass

    # 2. Fallback to symbolic indicator scoring
    clean_text = text.lower()
    scores: Dict[str, int] = {k: 0 for k in JURISDICTION_INDICATORS.keys()}
    
    for jur_code, keywords in JURISDICTION_INDICATORS.items():
        for kw in keywords:
            # Word boundary regex for short terms, substring for phrases
            if len(kw) <= 4:
                matches = re.findall(rf"\b{re.escape(kw)}\b", clean_text)
                scores[jur_code] += len(matches) * 2
            else:
                if kw in clean_text:
                    scores[jur_code] += 3
                    
    # Currency symbols special weighting
    if "₹" in text or "rs." in clean_text:
        scores["IN"] += 4
    if "£" in text:
        scores["UK"] += 4
    if "€" in text:
        scores["EU"] += 3
        scores["DE"] += 1
        scores["FR"] += 1
    if "c$" in clean_text:
        scores["CA"] += 4
    if "a$" in clean_text:
        scores["AU"] += 4
    if "s$" in clean_text:
        scores["SG"] += 4
    if "aed" in clean_text:
        scores["AE"] += 4

    top_jur = max(scores, key=scores.get)
    max_score = scores[top_jur]
    
    if max_score == 0:
        return ("GLOBAL", 0.0)
        
    confidence = min(1.0, max_score / 8.0)
    return (top_jur, round(confidence, 2))


def get_jurisdiction_details(jur_code: str) -> Dict[str, Any]:
    """Retrieves metadata and statutory frameworks for a given jurisdiction."""
    return JURISDICTIONS.get(jur_code, JURISDICTIONS["GLOBAL"])


def get_jurisdiction_prompt_context(jur_code: str) -> str:
    """Generates structured legal system guidelines to inject into LLM prompts."""
    jur = get_jurisdiction_details(jur_code)
    frameworks = "\n- ".join(jur.get("key_frameworks", []))
    
    context = f"""
JURISDICTION CONTEXT:
Target Country / Legal Forum: {jur['name']} {jur['flag']}
Legal Family & System: {jur['family']}
Currency & Standard Denomination: {jur.get('currency', 'USD')}
Primary Court Hierarchy: {jur.get('primary_courts', 'National Appellate and Trial Courts')}

Key Statutory Codes & Regulations to Cite:
- {frameworks}

STRICT JURISDICTION INSTRUCTIONS:
1. Ground all legal analysis strictly within the legal doctrine, statutes, and precedent of {jur['name']}.
2. Always cite specific acts, sections, articles, or statutory rules where applicable (e.g. section number or regulatory framework).
3. If the user's issue touches another jurisdiction (cross-border or foreign counterparty), analyze Private International Law, choice of law provisions, and forum non conveniens.
4. Highlight procedural requirements (e.g. mandatory statutory notice periods, mediation/conciliation steps, and limitation periods).
"""
    return context.strip()
