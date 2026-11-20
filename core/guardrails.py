"""
Safety Guardrails, Ethics, and Emergency Handling for LexGlobal AI
"""

import re
from typing import Tuple, Optional
from core.config import EMERGENCY_HOTLINES

STANDARD_LEGAL_DISCLAIMER = (
    "⚖️ **Legal Information & Ethical Notice**: "
    "LexGlobal AI provides automated legal information, document review, and research assistance based on statutory doctrines. "
    "This does NOT constitute formal legal advice, legal counsel, or attorney-client representation. "
    "Laws vary by jurisdiction and evolve frequently. Always consult a licensed attorney or legal practitioner in your jurisdiction "
    "before taking formal legal action, signing agreements, or relying on statutory interpretation."
)

DOCUMENT_REVIEW_DISCLAIMER = (
    "📑 **Document Analysis Notice**: "
    "This automated contract review highlights potential commercial hazards, standard risk clauses, and common negotiation points. "
    "It is not an exhaustive legal audit. Ambiguous terms or unstated commercial facts may alter enforceability."
)

DRAFTING_DISCLAIMER = (
    "✍️ **Drafting Disclaimer**: "
    "Generated documents and notices are preliminary drafts. Review each clause, dates, party names, and statutory citations "
    "with local legal counsel to verify compliance with local civil procedure rules before serving or executing."
)

EMERGENCY_KEYWORDS = [
    "domestic violence", "being beaten", "beating me", "physically beating", "physically abused",
    "hitting me", "kill myself", "suicide", "threatened to shoot", "active shooter", "kidnapped",
    "hostage", "rape", "sexual assault", "stalking me right now", "break into my house",
    "assault in progress", "imminent danger", "help me they are attacking"
]


def check_emergency(text: str, jurisdiction: str = "GLOBAL") -> Tuple[bool, Optional[str]]:
    """
    Scans text for immediate safety or life-threatening emergencies.
    If detected, returns (True, emergency_hotline_message).
    """
    if not text:
        return False, None
        
    lower_text = text.lower()
    for kw in EMERGENCY_KEYWORDS:
        if kw in lower_text:
            hotline_info = EMERGENCY_HOTLINES.get(jurisdiction, EMERGENCY_HOTLINES["GLOBAL"])
            warning = (
                f"🚨 **IMMEDIATE SAFETY ALERT**:\n\n"
                f"It appears you may be describing an active emergency, physical danger, or crisis situation.\n"
                f"**Please contact emergency services immediately:**\n\n"
                f"> **{hotline_info}**\n\n"
                f"Antigravity/LexGlobal AI cannot dispatch emergency response services. "
                f"Please prioritize your immediate physical safety first."
            )
            return True, warning
            
    return False, None


def inject_disclaimer(content: str, disclaimer_type: str = "standard") -> str:
    """Appends appropriate legal ethical notice to AI responses."""
    if disclaimer_type == "document":
        disclaimer = DOCUMENT_REVIEW_DISCLAIMER
    elif disclaimer_type == "drafting":
        disclaimer = DRAFTING_DISCLAIMER
    else:
        disclaimer = STANDARD_LEGAL_DISCLAIMER
        
    return f"{content}\n\n---\n{disclaimer}"
