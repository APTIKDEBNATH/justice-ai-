"""
Legal Drafting & Instrument Generator
Generates jurisdiction-compliant demand letters, cease & desist notices, NDAs, and agreements.
"""

from typing import Dict, Any
from core.llm import LLMProvider
from core.guardrails import inject_disclaimer
from core.jurisdiction import get_jurisdiction_prompt_context

DOCUMENT_TEMPLATES = {
    "demand_letter": {
        "title": "Formal Demand Letter / Notice of Breach",
        "description": "Pre-litigation demand for unpaid fees, outstanding debt, or contractual non-performance."
    },
    "cease_and_desist": {
        "title": "Cease and Desist Notice",
        "description": "Formal directive to stop copyright infringement, trademark misuse, defamation, or unauthorized conduct."
    },
    "nda": {
        "title": "Mutual Non-Disclosure Agreement (NDA)",
        "description": "Comprehensive bilateral confidentiality agreement with trade secret protections."
    },
    "tenancy_notice": {
        "title": "Tenancy Notice to Remedy / Notice to Vacate",
        "description": "Formal notice regarding lease violation, non-payment of rent, or end of tenancy."
    },
    "consumer_notice": {
        "title": "Consumer Grievance & Defective Product Notice",
        "description": "Formal pre-action notice demanding replacement, repair, or full refund for deficient goods/services."
    }
}


def draft_legal_document(
    doc_type: str,
    params: Dict[str, Any],
    jurisdiction: str = "GLOBAL",
    llm: LLMProvider = None
) -> str:
    """
    Drafts a high-precision legal instrument tailored to the specified jurisdiction.
    """
    if not llm:
        llm = LLMProvider()

    jur_context = get_jurisdiction_prompt_context(jurisdiction)
    doc_info = DOCUMENT_TEMPLATES.get(doc_type, DOCUMENT_TEMPLATES["demand_letter"])

    system_prompt = f"""
You are a master legal draftsman and corporate attorney.
{jur_context}

Your task: Draft an ironclad, professional, and jurisdiction-appropriate {doc_info['title']}.

DRAFTING PRINCIPLES:
1. Use exact formal legal terminology appropriate for {jurisdiction}.
2. Cite applicable statutory provisions, notice periods, and dispute resolution rules.
3. Ensure all placeholders like [DATE], [SENDER NAME], [RECIPIENT NAME], [AMOUNT] are cleanly formatted.
4. Include standard legal safeguards: reservation of rights without prejudice, limitation of liability, and notice of intention to claim legal costs and statutory interest.
5. Provide a complete, ready-to-execute document.
"""

    user_prompt = f"""
DOCUMENT TYPE: {doc_info['title']}
JURISDICTION: {jurisdiction}

PARTICULARS PROVIDED:
- Sender / Client Name: {params.get('sender_name', '[Sender Name]')}
- Sender Address / Contact: {params.get('sender_address', '[Sender Address]')}
- Recipient / Counterparty Name: {params.get('recipient_name', '[Recipient Name]')}
- Recipient Address / Contact: {params.get('recipient_address', '[Recipient Address]')}
- Specific Subject / Claim: {params.get('subject_matter', '[Subject Matter]')}
- Monetary Value / Sum Claimed: {params.get('claim_amount', '[Amount and Currency]')}
- Cure / Remediation Window: {params.get('cure_days', '15')} calendar days
- Key Facts / Background:
{params.get('details', '[Details of the matter]')}

Generate the complete, formal legal document draft.
"""

    response = llm.generate(prompt=user_prompt, system_instruction=system_prompt, temperature=0.1)
    return inject_disclaimer(response, disclaimer_type="drafting")
