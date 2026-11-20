"""
Client Intake & Legal Triage Engine
Transforms raw client narratives into structured Legal Case Dossiers and Litigation Strategy Briefs.
"""

from typing import Dict, Any, List
from core.llm import LLMProvider
from core.guardrails import inject_disclaimer
from core.jurisdiction import get_jurisdiction_prompt_context

def generate_intake_dossier(
    intake_data: Dict[str, Any],
    jurisdiction: str = "GLOBAL",
    llm: LLMProvider = None
) -> str:
    """
    Synthesizes intake facts into a professional Case Dossier for client reference
    and consultation with counsel.
    """
    if not llm:
        llm = LLMProvider()

    jur_context = get_jurisdiction_prompt_context(jurisdiction)
    
    system_prompt = f"""
You are a Senior Legal Intake Specialist and Litigation Strategist.
{jur_context}

Your objective: Synthesize the client's submitted facts into a comprehensive, professional
"Legal Intake & Case Assessment Dossier" formatted with clarity and authority.

STRUCTURE YOUR OUTPUT WITH THESE EXACT HEADINGS:
1. 🏛️ EXECUTIVE CASE SUMMARY & PARTIES
2. ⚖️ LEGAL CAUSES OF ACTION & STATUTORY PROVISIONS (Cite specific relevant sections of local law)
3. ⚠️ STATUTE OF LIMITATIONS & PROCEDURAL URGENCY (Flag any strict filing deadlines or notice requirements)
4. 📊 STRENGTH OF CASE & POTENTIAL DEFENSES COUNTERPARTY WILL RAISE
5. 📂 EVIDENTIARY CHECKLIST (Documents, communications, and proofs the client must gather)
6. 🎯 ACTIONABLE NEXT STEPS (Pre-litigation demand, alternative dispute resolution, formal filing)
7. ❓ TOP 5 QUESTIONS TO ASK AN ATTENDING LAWYER
"""

    facts_summary = f"""
CLIENT INTAKE PARTICULARS:
- Jurisdiction / Forum: {jurisdiction}
- Client Legal Standing: {intake_data.get('client_role', 'Individual')}
- Adverse Party / Counterparty: {intake_data.get('adverse_party', 'Unspecified')}
- Dispute Category: {intake_data.get('dispute_category', 'General Dispute')}
- Date / Timeline of Occurrence: {intake_data.get('incident_date', 'Recent')}
- Quantifiable Damages / Amount in Dispute: {intake_data.get('damages', 'Not quantified')}
- Primary Desired Outcome: {intake_data.get('desired_outcome', 'Full restitution / Resolution')}
- Factual Background / Narrative:
{intake_data.get('narrative', 'No narrative provided')}

- Evidence Currently Held: {intake_data.get('evidence_list', 'None specified')}
- Prior Communications / Demands Sent: {intake_data.get('prior_notice', 'None')}
"""

    response = llm.generate(prompt=facts_summary, system_instruction=system_prompt, temperature=0.2)
    return inject_disclaimer(response, disclaimer_type="standard")
