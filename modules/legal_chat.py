"""
Conversational Legal Intelligence & Consultation Module
Orchestrates multi-turn legal advisory conversations with automated jurisdiction detection and citation retrieval.
"""

from typing import List, Dict, Any, Tuple
from core.llm import LLMProvider
from core.guardrails import check_emergency, inject_disclaimer
from core.jurisdiction import detect_jurisdiction, get_jurisdiction_prompt_context, get_jurisdiction_details
from modules.knowledge_base import search_statutes, format_statutes_for_prompt

def process_chat_message(
    user_query: str,
    chat_history: List[Dict[str, str]],
    selected_jurisdiction: str = "GLOBAL",
    legal_domain: str = "General Legal Counsel & Triage",
    llm: LLMProvider = None
) -> Tuple[str, str, List[Dict[str, Any]]]:
    """
    Processes a user legal message:
    1. Scans for emergency/crisis conditions.
    2. Determines or confirms jurisdiction.
    3. Searches knowledge base for relevant statutory citations.
    4. Injects legal system doctrine and executes query with LLM.
    Returns (assistant_response, effective_jurisdiction, retrieved_statutes).
    """
    if not llm:
        llm = LLMProvider()

    # 1. Emergency safety check
    is_emergency, emergency_msg = check_emergency(user_query, selected_jurisdiction)
    if is_emergency:
        return (emergency_msg, selected_jurisdiction, [])

    # 2. Jurisdiction resolution
    effective_jurisdiction = selected_jurisdiction
    if selected_jurisdiction == "AUTO":
        detected_jur, conf = detect_jurisdiction(user_query)
        effective_jurisdiction = detected_jur if conf > 0.25 else "GLOBAL"

    # 3. Retrieve relevant statutes
    retrieved_statutes = search_statutes(user_query, jurisdiction=effective_jurisdiction, top_k=3)
    statutes_prompt_context = format_statutes_for_prompt(retrieved_statutes)

    # 4. Construct prompt
    jur_context = get_jurisdiction_prompt_context(effective_jurisdiction)
    jur_meta = get_jurisdiction_details(effective_jurisdiction)

    system_prompt = f"""
You are LexGlobal AI, an elite universal legal intelligence system.
You serve clients and attorneys globally with rigorous statutory precision.

LEGAL JURISDICTION CONFIGURATION:
{jur_context}

LEGAL SPECIALIZATION FOCUS: {legal_domain}

{statutes_prompt_context}

RESPONSE METHODOLOGY:
1. Provide a direct, authoritative, and structured legal answer.
2. CITATION REQUIREMENT: You MUST explicitly cite the specific Acts, Codes, Articles, and Sections that govern the issue in {jur_meta['name']}. If cross-border elements exist, address private international law/conflict of laws.
3. STRUCTURE:
   - 📌 **Legal Assessment**: Direct answer to the client's scenario.
   - ⚖️ **Governing Statutes & Precedent**: Explicit statutory articles, definitions, and legal standards.
   - ⚠️ **Key Risks & Procedural Traps**: Limitation periods, mandatory pre-suit notices, or burden of proof.
   - 🎯 **Actionable Next Steps**: Step-by-step checklist of what the client should do immediately.
4. Maintain a formal, reassuring, and highly competent tone.
"""

    # Build conversation context from previous turns
    conversation_str = ""
    for msg in chat_history[-4:]:
        role_label = "User" if msg["role"] == "user" else "LexGlobal AI"
        conversation_str += f"{role_label}: {msg['content']}\n\n"

    final_prompt = f"""
{conversation_str}User: {user_query}

Provide your structured legal analysis:
"""

    response_text = llm.generate(prompt=final_prompt, system_instruction=system_prompt, temperature=0.2)
    safe_response = inject_disclaimer(response_text, disclaimer_type="standard")

    return (safe_response, effective_jurisdiction, retrieved_statutes)
