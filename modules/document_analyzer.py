"""
Legal Document & Contract Risk Analyzer
Performs deep clause audits, risk scoring (Low/Med/High), redline suggestions, and enforceability checks.
"""

from typing import Dict, Any, List
import re
from core.llm import LLMProvider
from core.guardrails import inject_disclaimer
from core.jurisdiction import get_jurisdiction_prompt_context

# High-risk clause detection patterns
RISK_PATTERNS = [
    {
        "category": "Liability & Indemnification",
        "severity": "🔴 Critical",
        "pattern": r"(?:indemnif\w+.*(?:hold harmless|against any)|hold harmless|unlimited liability|without (?:cap|limitation)|waive.*consequential damages)",
        "hazard": "Uncapped or unilateral indemnity obligating you to cover third-party claims without reciprocation or liability ceiling.",
        "fair_solution": "Cap total aggregate liability to the fees paid in the preceding 12 months; exclude indirect/consequential damages mutually."
    },
    {
        "category": "Termination for Convenience",
        "severity": "🟡 Moderate",
        "pattern": r"(?:terminate.*without cause|immediate.*termination|unilateral right to terminate|sole discretion.*cancel)",
        "hazard": "Allows the other party to terminate abruptly without giving you sufficient cure or ramp-down time.",
        "fair_solution": "Require at least 30 days' advance written notice for termination without cause, and a 15-day cure period for material breach."
    },
    {
        "category": "Restrictive Covenants & Non-Compete",
        "severity": "🔴 Critical",
        "pattern": r"(?:(?:shall not|not to|agrees? not to).*compete|non-compete|period of \d+ years?|worldwide.*restrict|restraint of trade)",
        "hazard": "May unreasonably restrict your right to earn a livelihood. In many jurisdictions (e.g. California, India), post-employment non-competes are void as a matter of public policy.",
        "fair_solution": "Delete post-employment non-compete; limit restriction strictly to non-solicitation of active proprietary clients for a maximum of 6 months."
    },
    {
        "category": "Governing Law & Dispute Resolution",
        "severity": "🟡 Moderate",
        "pattern": r"(?:exclusive jurisdiction of the courts of|binding arbitration|waive.*jury|venue shall lie exclusively in)",
        "hazard": "May force litigation in a distant foreign court or subject you to cost-prohibitive private arbitration.",
        "fair_solution": "Specify mutual negotiation first (30 days), then mediation, and set venue in a mutually convenient neutral jurisdiction."
    },
    {
        "category": "Intellectual Property Overreach",
        "severity": "🔴 Critical",
        "pattern": r"(?:assigns? all rights.*in perpetuity|moral rights.*waived|all inventions.*conceived|work made for hire)",
        "hazard": "Overbroad assignment claiming ownership over pre-existing background IP, personal side projects, or future unrelated inventions.",
        "fair_solution": "Exclude 'Background Technology & Pre-existing IP'; restrict assignment only to custom deliverables created solely under this agreement."
    },
    {
        "category": "Liquidated Damages & Penalties",
        "severity": "🟡 Moderate",
        "pattern": r"(?:liquidated damages|forfeit.*all (?:payments|wages)|interest.*(?:\d{2,}%|per month))",
        "hazard": "Exorbitant liquidated damages or interest clauses that courts may strike down as unenforceable penalties.",
        "fair_solution": "Interest capped at statutory rate (e.g. 1% per month); liquidated damages strictly limited to genuine pre-estimated direct losses."
    }
]


def rule_based_audit(contract_text: str) -> List[Dict[str, Any]]:
    """Fast regex scanner across known contractual hazard patterns."""
    findings = []
    for rule in RISK_PATTERNS:
        match = re.search(rule["pattern"], contract_text, re.IGNORECASE | re.DOTALL)
        if match:
            # Extract surrounding context
            start = max(0, match.start() - 60)
            end = min(len(contract_text), match.end() + 100)
            snippet = contract_text[start:end].replace("\n", " ").strip()
            
            findings.append({
                "category": rule["category"],
                "severity": rule["severity"],
                "flagged_snippet": f"...{snippet}...",
                "hazard": rule["hazard"],
                "fair_solution": rule["fair_solution"]
            })
    return findings


def analyze_contract(
    contract_text: str,
    jurisdiction: str = "GLOBAL",
    llm: LLMProvider = None
) -> Dict[str, Any]:
    """
    Executes a comprehensive contract analysis combining rule-based hazard detection
    with LLM contextual evaluation.
    """
    if not llm:
        llm = LLMProvider()

    rule_findings = rule_based_audit(contract_text)
    
    # Calculate baseline risk score
    crit_count = sum(1 for f in rule_findings if "Critical" in f["severity"])
    mod_count = sum(1 for f in rule_findings if "Moderate" in f["severity"])
    raw_score = min(95, max(15, (crit_count * 25) + (mod_count * 12)))
    
    if raw_score >= 65:
        risk_tier = "🔴 HIGH RISK"
        risk_summary = "Multiple one-sided, aggressive, or potentially unenforceable clauses detected."
    elif raw_score >= 35:
        risk_tier = "🟡 MODERATE RISK"
        risk_summary = "Standard commercial agreement with notable clauses requiring negotiation and capping."
    else:
        risk_tier = "🟢 LOW RISK"
        risk_summary = "Relatively balanced agreement with standard mutual commitments."

    # Generate LLM in-depth review
    jur_context = get_jurisdiction_prompt_context(jurisdiction)
    system_prompt = f"""
You are an expert international contract attorney and commercial counsel.
{jur_context}

Analyze the provided legal agreement with rigorous precision. Provide:
1. Executive Risk Summary (Strengths, Weaknesses, Asymmetry).
2. Key Problematic Clauses (Quote excerpt, explain legal hazard under the governing law).
3. Redlined Alternative Clauses (Exact drafting language to suggest during negotiation).
4. Missing Protective Clauses (e.g. Force Majeure, Mutual NDA, Liability Cap, Severability).
5. Enforceability Verdict under {jurisdiction}.
"""

    user_prompt = f"""
Please analyze the following legal contract text:

```
{contract_text[:8000]}
```

Provide your full structured audit.
"""

    llm_analysis = llm.generate(prompt=user_prompt, system_instruction=system_prompt, temperature=0.2)
    safe_analysis = inject_disclaimer(llm_analysis, disclaimer_type="document")

    return {
        "risk_score": raw_score,
        "risk_tier": risk_tier,
        "risk_summary": risk_summary,
        "rule_findings": rule_findings,
        "detailed_analysis": safe_analysis
    }
