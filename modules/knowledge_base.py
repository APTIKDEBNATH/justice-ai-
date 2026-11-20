"""
Global Statutory & Precedent Knowledge Base
Pre-indexed statutes, doctrine benchmarks, and legal search engine for LexGlobal AI.
"""

from typing import List, Dict, Any
import re

# Comprehensive global statutory database with official source portal links
STATUTORY_DATABASE: List[Dict[str, Any]] = [
    # --- GERMANY (DE) ---
    {
        "jurisdiction": "DE",
        "act": "BGB § 573",
        "section": "§ 573",
        "title": "Ordinary termination by the landlord",
        "title_de": "Ordentliche Kündigung des Vermieters",
        "summary": "In residential leases, the landlord may terminate only if they have a justified interest (legitimate reason) in ending the tenancy. Justified interest includes substantial breach of duty by tenant, legitimate personal need (Eigenbedarf) for the landlord or family, or inability to economically exploit the property.",
        "source_domain": "gesetze-im-internet.de",
        "source_url": "https://www.gesetze-im-internet.de/bgb/__573.html",
        "tags": ["germany", "tenancy", "landlord", "termination", "bgb", "eigenbedarf", "lease", "eviction"]
    },
    {
        "jurisdiction": "DE",
        "act": "BGB § 573c",
        "section": "§ 573c",
        "title": "Notice periods for termination",
        "title_de": "Fristen der ordentlichen Kündigung",
        "summary": "Termination notice by the landlord is permitted no later than the third working day of a calendar month to expire at the end of the second month following. The landlord's notice period extends by 3 months after 5 and 8 years of tenancy (up to 9 months). The tenant's notice period is standard 3 months regardless of duration.",
        "source_domain": "gesetze-im-internet.de",
        "source_url": "https://www.gesetze-im-internet.de/bgb/__573c.html",
        "tags": ["germany", "tenancy", "notice period", "bgb", "kündigungsfrist", "lease", "landlord"]
    },
    {
        "jurisdiction": "DE",
        "act": "BGB § 535",
        "section": "§ 535",
        "title": "Contents and main duties of the lease agreement",
        "title_de": "Inhalt und Hauptpflichten des Mietvertrags",
        "summary": "The landlord is required to grant the tenant the use of the leased property during the lease term and maintain it in a suitable condition. The tenant is obligated to pay the agreed rent.",
        "source_domain": "gesetze-im-internet.de",
        "source_url": "https://www.gesetze-im-internet.de/bgb/__535.html",
        "tags": ["germany", "tenancy", "lease", "maintenance", "rent", "bgb"]
    },

    # --- INDIA (IN) ---
    {
        "jurisdiction": "IN",
        "act": "Consumer Protection Act, 2019",
        "section": "Section 39",
        "title": "Findings and Orders of District Commission",
        "title_hi": "उपभोक्ता संरक्षण अधिनियम, 2019 · धारा 39 · ज़िला आयोग के आदेश",
        "summary": "Where the District Commission is satisfied that goods complain of suffer from defect or deficiency of service, it may direct removal of defect, replacement with new goods, refund of price paid along with interest, and award punitive compensation.",
        "source_domain": "indiacode.nic.in",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/15256",
        "tags": ["india", "consumer", "refund", "defective goods", "district commission", "e-daakhil", "replacement", "खराब", "रिफ़ंड", "उपभोक्ता"]
    },
    {
        "jurisdiction": "IN",
        "act": "Consumer Protection Act, 2019",
        "section": "Section 69",
        "title": "Limitation Period for Filing Complaints",
        "title_hi": "उपभोक्ता संरक्षण अधिनियम, 2019 · धारा 69 · शिकायत की समय-सीमा",
        "summary": "District, State, or National Commission shall not admit a complaint unless it is filed within two years from the date on which the cause of action has arisen, unless sufficient cause for delay is shown.",
        "source_domain": "indiacode.nic.in",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/15256",
        "tags": ["india", "consumer", "limitation", "time limit", "two years", "complaint", "समय-सीमा"]
    },
    {
        "jurisdiction": "IN",
        "act": "Bharatiya Nyaya Sanhita, 2023 (BNS)",
        "section": "Section 318",
        "title": "Cheating and Dishonestly Inducing Delivery of Property",
        "title_hi": "भारतीय न्याय संहिता, 2023 · धारा 318 · धोखाधड़ी",
        "summary": "Replaces Section 420 IPC. Defines cheating as deceiving any person and fraudulently or dishonestly inducing delivery of property. Imprisonment up to 7 years and fine.",
        "source_domain": "indiacode.nic.in",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/20340",
        "tags": ["criminal", "fraud", "cheating", "property", "bns", "ipc 420", "धोखाधड़ी"]
    },
    {
        "jurisdiction": "IN",
        "act": "Indian Contract Act, 1872",
        "section": "Section 27",
        "title": "Agreement in Restraint of Trade Void",
        "title_hi": "भारतीय अनुबंध अधिनियम, 1872 · धारा 27 · व्यापार पर रोक अमान्य",
        "summary": "Every agreement by which anyone is restrained from exercising a lawful profession, trade or business of any kind, is to that extent void, subject to the single exception of sale of goodwill.",
        "source_domain": "indiacode.nic.in",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2187",
        "tags": ["contract", "non-compete", "restraint of trade", "employment", "void agreement", "गैर-प्रतिस्पर्धा"]
    },
    {
        "jurisdiction": "IN",
        "act": "Indian Contract Act, 1872",
        "section": "Section 73 & 74",
        "title": "Compensation for Loss or Damage Caused by Breach & Liquidated Damages",
        "title_hi": "भारतीय अनुबंध अधिनियम, 1872 · धारा 73-74 · हर्जाना एवं क्षतिपूर्ति",
        "summary": "Party suffering from breach is entitled to receive compensation for any naturally arising loss. Liquidated damages clauses represent reasonable upper ceilings, not enforceable punitive penalties.",
        "source_domain": "indiacode.nic.in",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2187",
        "tags": ["contract", "damages", "breach", "liquidated damages", "penalty", "हर्जाना"]
    },
    {
        "jurisdiction": "IN",
        "act": "Negotiable Instruments Act, 1881",
        "section": "Section 138",
        "title": "Dishonour of Cheque for Insufficiency of Funds",
        "title_hi": "परक्राम्य लिखत अधिनियम, 1881 · धारा 138 · चेक बाउंस",
        "summary": "Where a cheque drawn for discharge of debt is returned unpaid, punishable with up to 2 years imprisonment or fine up to twice the cheque amount. Requires statutory demand notice within 30 days and 15 days cure window.",
        "source_domain": "indiacode.nic.in",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2190",
        "tags": ["cheque bounce", "debt", "banking", "criminal complaint", "statutory notice", "चेक बाउंस"]
    },
    {
        "jurisdiction": "IN",
        "act": "Digital Personal Data Protection Act, 2023 (DPDP)",
        "section": "Section 6 & 8",
        "title": "Consent and Obligations of Data Fiduciary",
        "title_hi": "डिजिटल व्यक्तिगत डेटा संरक्षण अधिनियम, 2023 · धारा 6-8 · सहमति और दायित्व",
        "summary": "Requires notice and verifiable consent before processing personal data. Imposes strict obligations on Data Fiduciaries to maintain security safeguards and erase data upon withdrawal of consent.",
        "source_domain": "indiacode.nic.in",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/19448",
        "tags": ["privacy", "data protection", "dpdp", "consent", "penalty", "डेटा संरक्षण"]
    },

    # --- EUROPEAN UNION (EU) ---
    {
        "jurisdiction": "EU",
        "act": "General Data Protection Regulation (EU 2016/679)",
        "section": "Article 17",
        "title": "Right to Erasure ('Right to be Forgotten')",
        "summary": "Grants data subjects the fundamental right to obtain from the controller the erasure of personal data without undue delay where data is no longer necessary in relation to original processing purposes, or consent has been withdrawn.",
        "source_domain": "eur-lex.europa.eu",
        "source_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679",
        "tags": ["gdpr", "privacy", "right to be forgotten", "erasure", "data protection", "european union", "delete data"]
    },
    {
        "jurisdiction": "EU",
        "act": "General Data Protection Regulation (EU 2016/679)",
        "section": "Article 82",
        "title": "Right to Compensation and Liability",
        "summary": "Any person who has suffered material or non-material damage as a result of an infringement of this Regulation shall have the right to receive compensation from the controller or processor for the damage suffered.",
        "source_domain": "eur-lex.europa.eu",
        "source_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679",
        "tags": ["gdpr", "damages", "compensation", "non-material damage", "liability", "privacy"]
    },
    {
        "jurisdiction": "EU",
        "act": "Rome I Regulation (EC No 593/2008)",
        "section": "Article 3 & Article 6",
        "title": "Freedom of Choice of Law & Consumer Contracts Protection",
        "summary": "Parties may choose governing law of contract, but in consumer contracts, choice cannot deprive consumer of mandatory protective provisions of their country of habitual residence.",
        "source_domain": "eur-lex.europa.eu",
        "source_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32008R0593",
        "tags": ["conflict of laws", "governing law", "cross-border", "consumer protection", "rome i"]
    },

    # --- UNITED STATES (US / TEXAS) ---
    {
        "jurisdiction": "US",
        "act": "Texas Property Code",
        "section": "§ 24.005",
        "title": "Notice to Vacate Prior to Filing Eviction Suit",
        "summary": "If the occupant is a tenant under a written lease or oral agreement, the landlord must give a tenant who defaults or holds over at least three days' written notice to vacate before filing a forcible detainer suit, unless contract specifies other period.",
        "source_domain": "statutes.capitol.texas.gov",
        "source_url": "https://statutes.capitol.texas.gov/Docs/PR/htm/PR.24.htm",
        "tags": ["texas", "property", "eviction", "notice to vacate", "tenancy", "forcible detainer", "rent"]
    },
    {
        "jurisdiction": "US",
        "act": "Fair Labor Standards Act (FLSA)",
        "section": "29 U.S.C. § 207",
        "title": "Maximum Hours & Overtime Compensation",
        "summary": "Requires non-exempt employees to receive overtime pay at not less than 1.5 times regular rate for hours worked exceeding 40 hours per workweek.",
        "source_domain": "law.cornell.edu",
        "source_url": "https://www.law.cornell.edu/uscode/text/29/207",
        "tags": ["employment", "labor", "overtime", "wages", "flsa", "hours"]
    },
    {
        "jurisdiction": "US",
        "act": "Uniform Commercial Code (UCC)",
        "section": "UCC § 2-207",
        "title": "Additional Terms in Acceptance or Confirmation (Battle of the Forms)",
        "summary": "Governs sales contracts where buyer and seller exchange standard form purchase orders and acknowledgments with conflicting terms. Replaces common law mirror image rule.",
        "source_domain": "law.cornell.edu",
        "source_url": "https://www.law.cornell.edu/ucc/2/2-207",
        "tags": ["contract", "commercial", "sales", "battle of the forms", "ucc"]
    },
    {
        "jurisdiction": "US",
        "act": "California Business & Professions Code",
        "section": "Cal. Bus. & Prof. Code § 16600",
        "title": "Invalidity of Restraint of Business or Employment (Non-Competes)",
        "summary": "Every contract by which anyone is restrained from engaging in a lawful profession, trade, or business of any kind is void. Strongly reinforced by SB 699 and AB 1076 making enforcement actionable.",
        "source_domain": "leginfo.legislature.ca.gov",
        "source_url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=16600.&lawCode=BPC",
        "tags": ["california", "non-compete", "employment", "restraint of trade", "void"]
    },

    # --- UNITED KINGDOM (UK) ---
    {
        "jurisdiction": "UK",
        "act": "Consumer Rights Act 2015",
        "section": "Section 9, 10 & 20",
        "title": "Goods to be of Satisfactory Quality & Right to Reject",
        "summary": "Implies statutory terms that goods must be of satisfactory quality, fit for particular purpose, and as described. Provides short-term right to reject and full refund within 30 days of delivery.",
        "source_domain": "legislation.gov.uk",
        "source_url": "https://www.legislation.gov.uk/ukpga/2015/15/contents",
        "tags": ["consumer", "sale of goods", "refund", "faulty product", "cra 2015", "uk consumer"]
    },
    {
        "jurisdiction": "UK",
        "act": "Housing Act 1988",
        "section": "Section 21 & Section 8",
        "title": "Recovery of Possession on Assured Shorthold Tenancies",
        "summary": "Section 21 allows no-fault recovery of possession giving at least two months notice. Section 8 allows eviction on fault grounds (rent arrears, breach of obligation).",
        "source_domain": "legislation.gov.uk",
        "source_url": "https://www.legislation.gov.uk/ukpga/1988/50/contents",
        "tags": ["tenancy", "housing act", "section 21", "section 8", "eviction", "landlord", "uk tenancy"]
    },
    {
        "jurisdiction": "UK",
        "act": "Employment Rights Act 1996",
        "section": "Section 86 & Section 94",
        "title": "Statutory Minimum Notice Periods & Unfair Dismissal",
        "summary": "Mandates statutory minimum notice of at least 1 week per year of continuous employment (up to 12 weeks). Section 94 guarantees right not to be unfairly dismissed after qualifying 2-year service period.",
        "source_domain": "legislation.gov.uk",
        "source_url": "https://www.legislation.gov.uk/ukpga/1996/18/contents",
        "tags": ["employment", "dismissal", "notice period", "redundancy", "unfair dismissal", "uk employment"]
    },

    # --- INTERNATIONAL / GLOBAL ---
    {
        "jurisdiction": "GLOBAL",
        "act": "UN Convention on Contracts for International Sale of Goods (CISG)",
        "section": "Article 25 & Article 49",
        "title": "Fundamental Breach & Right to Avoid Contract",
        "summary": "A breach of contract is fundamental if it results in such detriment to the other party as substantially to deprive them of what they were entitled to expect under the contract. Entitles buyer to avoid contract.",
        "source_domain": "uncitral.un.org",
        "source_url": "https://uncitral.un.org/en/texts/salegoods/conventions/sale_of_goods/cisg",
        "tags": ["international", "sales", "cisg", "cross-border", "fundamental breach"]
    },
    {
        "jurisdiction": "GLOBAL",
        "act": "New York Convention (1958)",
        "section": "Article V",
        "title": "Grounds for Refusal of Enforcement of Foreign Arbitral Awards",
        "summary": "Lists exhaustive grounds under which recognition and enforcement of an international arbitral award may be refused, including invalid arbitration agreement, lack of notice, or violation of public policy.",
        "source_domain": "uncitral.un.org",
        "source_url": "https://uncitral.un.org/en/texts/arbitration/conventions/foreign_arbitral_awards",
        "tags": ["arbitration", "new york convention", "foreign award", "dispute resolution", "enforcement"]
    }
]


def search_statutes(query: str, jurisdiction: str = "GLOBAL", top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Finds relevant statutory references for a query matching jurisdiction and keywords.
    """
    clean_query = query.lower()
    results = []

    for item in STATUTORY_DATABASE:
        score = 0
        
        # Jurisdiction match weighting
        if jurisdiction != "GLOBAL" and jurisdiction != "AUTO":
            if item["jurisdiction"] == jurisdiction:
                score += 8
            elif item["jurisdiction"] == "GLOBAL":
                score += 2
            else:
                score -= 3
        else:
            score += 2

        # Check tag matches
        for tag in item.get("tags", []):
            if tag in clean_query:
                score += 5

        # Check act or title or summary words
        query_words = re.findall(r"\b\w{3,}\b", clean_query)
        target_text = f"{item['act']} {item['section']} {item.get('title','')} {item.get('title_hi','')} {item['summary']}".lower()
        for word in query_words:
            if word in target_text:
                score += 2

        if score > 0:
            results.append((score, item))

    results.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in results[:top_k]]


def format_statutes_for_prompt(statutes: List[Dict[str, Any]]) -> str:
    """Formats retrieved statutes into prompt context."""
    if not statutes:
        return ""
    
    formatted = ["RELEVANT STATUTORY REFERENCES & LEGAL CODES:"]
    for s in statutes:
        formatted.append(f"- **{s['act']} - {s['section']} ({s['title']})** [{s.get('source_domain', 'official')}]: {s['summary']}")
    return "\n".join(formatted)
