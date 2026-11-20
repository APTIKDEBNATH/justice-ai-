"""
Justice AI - Legal Dataset Generator & Curator
Constructs a curated, multi-class legal NLP dataset compiled from official government statutes:
India Code, German Gesetze-im-Internet, UK Legislation, EUR-Lex, and US Code.
"""

import os
import json
import pandas as pd
from typing import List, Dict

# Raw statutory training samples (Queries mapped to Jurisdiction and Legal Intent Domain)
RAW_DATA: List[Dict[str, str]] = [
    # --- GERMANY (DE) - TENANCY & LEASE ---
    {"text": "My landlord in Germany sent me a termination letter. Does he need a reason?", "jurisdiction": "DE", "domain": "Tenancy", "statute": "BGB § 573"},
    {"text": "What is the statutory notice period for a landlord under German BGB?", "jurisdiction": "DE", "domain": "Tenancy", "statute": "BGB § 573c"},
    {"text": "Can my landlord evict me without stating Eigenbedarf personal need?", "jurisdiction": "DE", "domain": "Tenancy", "statute": "BGB § 573"},
    {"text": "How much can a landlord increase rent under the Mietspiegel in Berlin?", "jurisdiction": "DE", "domain": "Tenancy", "statute": "BGB § 558"},
    {"text": "Can I object to lease termination on social hardship grounds under BGB 574?", "jurisdiction": "DE", "domain": "Tenancy", "statute": "BGB § 574"},
    {"text": "What if I have lived in my rented apartment in Germany for over 8 years?", "jurisdiction": "DE", "domain": "Tenancy", "statute": "BGB § 573c"},
    {"text": "Is the landlord responsible for heating and mold repairs under German law?", "jurisdiction": "DE", "domain": "Tenancy", "statute": "BGB § 535"},
    {"text": "Mein Vermieter in Deutschland hat mir gekündigt. Braucht er einen Grund?", "jurisdiction": "DE", "domain": "Tenancy", "statute": "BGB § 573"},
    {"text": "Kündigungsfrist für Vermieter nach 5 Jahren Mietzeit nach BGB.", "jurisdiction": "DE", "domain": "Tenancy", "statute": "BGB § 573c"},
    {"text": "Widerspruch gegen Kündigung wegen sozialer Härte BGB 574.", "jurisdiction": "DE", "domain": "Tenancy", "statute": "BGB § 574"},
    {"text": "Mieterhöhung bis zur ortsüblichen Vergleichsmiete Mietpreisbremse.", "jurisdiction": "DE", "domain": "Tenancy", "statute": "BGB § 556d"},
    {"text": "Kaution Rückzahlung Frist nach Beendigung des Mietvertrags.", "jurisdiction": "DE", "domain": "Tenancy", "statute": "BGB § 551"},

    # --- INDIA (IN) - CONSUMER PROTECTION & CONTRACT ---
    {"text": "I ordered a phone online that arrived defective and the seller refuses refund.", "jurisdiction": "IN", "domain": "Consumer", "statute": "Consumer Protection Act, 2019 Section 39"},
    {"text": "How do I file an online complaint on e-Daakhil consumer portal in India?", "jurisdiction": "IN", "domain": "Consumer", "statute": "Consumer Protection Act, 2019 Section 35"},
    {"text": "What is the limitation period for filing consumer complaint in District Commission?", "jurisdiction": "IN", "domain": "Consumer", "statute": "Consumer Protection Act, 2019 Section 69"},
    {"text": "Deficiency of service by airline for cancelling flight without compensation.", "jurisdiction": "IN", "domain": "Consumer", "statute": "Consumer Protection Act, 2019 Section 2(11)"},
    {"text": "Unfair trade practice by e-commerce platform giving misleading discounts.", "jurisdiction": "IN", "domain": "Consumer", "statute": "Consumer Protection Act, 2019 Section 2(47)"},
    {"text": "मैंने ऑनलाइन एक फ़ोन मँगवाया था जो खराब निकला। विक्रेता रिफ़ंड देने से मना कर रहा है।", "jurisdiction": "IN", "domain": "Consumer", "statute": "Consumer Protection Act, 2019 Section 39"},
    {"text": "उपभोक्ता आयोग में ई-दाखिल पोर्टल पर शिकायत दर्ज करने की समय-सीमा क्या है?", "jurisdiction": "IN", "domain": "Consumer", "statute": "Consumer Protection Act, 2019 Section 69"},
    {"text": "विक्रेता ने वारंटी के बावजूद ख़राब लैपटॉप बदलने से इनकार कर दिया।", "jurisdiction": "IN", "domain": "Consumer", "statute": "Consumer Protection Act, 2019 Section 39"},
    {"text": "Is a 2-year non-compete clause enforceable against an employee in India?", "jurisdiction": "IN", "domain": "Commercial", "statute": "Indian Contract Act, 1872 Section 27"},
    {"text": "Agreement in restraint of trade is void under Indian Contract Act Section 27.", "jurisdiction": "IN", "domain": "Commercial", "statute": "Indian Contract Act, 1872 Section 27"},
    {"text": "Can a company impose heavy liquidated damages penalty for leaving job before bond?", "jurisdiction": "IN", "domain": "Commercial", "statute": "Indian Contract Act, 1872 Section 74"},
    {"text": "Cheque bounce case under Section 138 Negotiable Instruments Act statutory notice period.", "jurisdiction": "IN", "domain": "Commercial", "statute": "NI Act Section 138"},
    {"text": "Punishment for cheating and dishonestly inducing delivery of property under BNS 318.", "jurisdiction": "IN", "domain": "Criminal", "statute": "Bharatiya Nyaya Sanhita, 2023 Section 318"},
    {"text": "How does Bharatiya Sakshya Adhiniyam treat electronic records and digital certificates?", "jurisdiction": "IN", "domain": "Criminal", "statute": "BSA 2023 Section 61"},
    {"text": "Mandatory consent and notice obligations under Digital Personal Data Protection Act 2023.", "jurisdiction": "IN", "domain": "Privacy", "statute": "DPDP Act, 2023 Section 6"},

    # --- EUROPEAN UNION (EU) - DATA PRIVACY (GDPR) ---
    {"text": "How do I enforce my right to erasure under GDPR Article 17 if a website refuses deletion?", "jurisdiction": "EU", "domain": "Privacy", "statute": "GDPR Article 17"},
    {"text": "Can a company refuse right to be forgotten claiming legitimate interest under GDPR?", "jurisdiction": "EU", "domain": "Privacy", "statute": "GDPR Article 17(3)"},
    {"text": "What is the statutory deadline for a data controller to respond to a GDPR subject access request?", "jurisdiction": "EU", "domain": "Privacy", "statute": "GDPR Article 12(3)"},
    {"text": "Compensation for non-material distress from data breach under GDPR Article 82.", "jurisdiction": "EU", "domain": "Privacy", "statute": "GDPR Article 82"},
    {"text": "Cross-border consumer contract choice of law under Rome I Regulation Article 6.", "jurisdiction": "EU", "domain": "Commercial", "statute": "Rome I Regulation Article 6"},
    {"text": "Is transferring EU personal data to foreign servers compliant with Chapter V GDPR?", "jurisdiction": "EU", "domain": "Privacy", "statute": "GDPR Article 44"},
    {"text": "Filing a complaint with national Data Protection Supervisory Authority under GDPR Art 77.", "jurisdiction": "EU", "domain": "Privacy", "statute": "GDPR Article 77"},
    {"text": "High-risk AI systems transparency and compliance obligations under EU AI Act 2024.", "jurisdiction": "EU", "domain": "Privacy", "statute": "EU AI Act 2024"},

    # --- UNITED STATES (US) - EMPLOYMENT, REAL ESTATE & COMMERCIAL ---
    {"text": "My employer requires 50 hours of work per week without overtime pay under FLSA.", "jurisdiction": "US", "domain": "Employment", "statute": "29 U.S.C. § 207 FLSA"},
    {"text": "Does California enforce post-employment non-compete agreements under Section 16600?", "jurisdiction": "US", "domain": "Employment", "statute": "Cal. Bus. & Prof. Code § 16600"},
    {"text": "What is the minimum notice to vacate before filing eviction in Texas Property Code?", "jurisdiction": "US", "domain": "Tenancy", "statute": "Texas Property Code § 24.005"},
    {"text": "Battle of the forms conflicting standard purchase order terms under UCC Section 2-207.", "jurisdiction": "US", "domain": "Commercial", "statute": "UCC § 2-207"},
    {"text": "Statute of limitations for breach of written contract in New York and Delaware.", "jurisdiction": "US", "domain": "Commercial", "statute": "NY CPLR § 213"},
    {"text": "DMCA safe harbor takedown notice requirements for online hosting service providers.", "jurisdiction": "US", "domain": "Commercial", "statute": "17 U.S.C. § 512(c)"},
    {"text": "Exempt vs non-exempt employee salary threshold test under federal wage and hour rules.", "jurisdiction": "US", "domain": "Employment", "statute": "29 C.F.R. Part 541"},
    {"text": "Can an employer retaliate against worker for reporting OSHA workplace safety violations?", "jurisdiction": "US", "domain": "Employment", "statute": "29 U.S.C. § 660(c)"},

    # --- UNITED KINGDOM (UK) - CONSUMER, EMPLOYMENT & HOUSING ---
    {"text": "What is the statutory redundancy notice period under Employment Rights Act 1996?", "jurisdiction": "UK", "domain": "Employment", "statute": "Employment Rights Act 1996 Section 86"},
    {"text": "Qualifying period for unfair dismissal claim before an employment tribunal in UK.", "jurisdiction": "UK", "domain": "Employment", "statute": "Employment Rights Act 1996 Section 94"},
    {"text": "Short-term right to reject faulty goods and get full refund under Consumer Rights Act 2015.", "jurisdiction": "UK", "domain": "Consumer", "statute": "Consumer Rights Act 2015 Section 20"},
    {"text": "Can a landlord serve a Section 21 no-fault eviction notice without protecting tenant deposit?", "jurisdiction": "UK", "domain": "Tenancy", "statute": "Housing Act 1988 Section 21"},
    {"text": "Grounds for possession under Section 8 of Housing Act 1988 for rent arrears in England.", "jurisdiction": "UK", "domain": "Tenancy", "statute": "Housing Act 1988 Section 8"},
    {"text": "Data subject access request time limit under UK Data Protection Act 2018 UK GDPR.", "jurisdiction": "UK", "domain": "Privacy", "statute": "Data Protection Act 2018 Section 54"},

    # --- GLOBAL & TRANSNATIONAL LAW ---
    {"text": "Fundamental breach of international sales contract and right to avoid under CISG Article 25.", "jurisdiction": "GLOBAL", "domain": "Commercial", "statute": "CISG Article 25 & 49"},
    {"text": "Grounds for refusal of foreign arbitral award recognition under New York Convention Article V.", "jurisdiction": "GLOBAL", "domain": "Commercial", "statute": "New York Convention 1958 Article V"},
    {"text": "UNCITRAL Model Law on International Commercial Arbitration competence of arbitral tribunal.", "jurisdiction": "GLOBAL", "domain": "Commercial", "statute": "UNCITRAL Model Law Article 16"},
    {"text": "Incoterms 2020 transfer of risk and carriage obligations between CIF and FOB buyers.", "jurisdiction": "GLOBAL", "domain": "Commercial", "statute": "ICC Incoterms 2020"},

    # --- EMERGENCY / CRISIS (GUARDRAIL CLASS) ---
    {"text": "Help, my partner is physically beating me right now and I am locked in the room.", "jurisdiction": "GLOBAL", "domain": "Emergency", "statute": "Domestic Violence Emergency Protocol"},
    {"text": "Someone is trying to break into my house with a weapon right now please help.", "jurisdiction": "GLOBAL", "domain": "Emergency", "statute": "Immediate Police Assistance Protocol"},
    {"text": "I am being held hostage against my will and need emergency police rescue.", "jurisdiction": "GLOBAL", "domain": "Emergency", "statute": "Emergency Crisis Response"}
]

def generate_and_save_dataset():
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)

    # Augment data with realistic paraphrases to expand sample count for training
    augmented_records = []
    
    # Paraphrase templates for data augmentation
    templates = [
        "Legal advice needed: {query}",
        "What are my rights regarding: {query}",
        "Under local statutes, {query}",
        "Can someone explain the legal provisions: {query}",
        "According to governing law, {query}"
    ]

    for item in RAW_DATA:
        # Original
        augmented_records.append(item)
        # Paraphrases
        for t in templates:
            paraphrased = t.format(query=item["text"])
            augmented_records.append({
                "text": paraphrased,
                "jurisdiction": item["jurisdiction"],
                "domain": item["domain"],
                "statute": item["statute"]
            })

    df = pd.DataFrame(augmented_records)
    
    csv_path = os.path.join(data_dir, "legal_nlp_training_dataset.csv")
    json_path = os.path.join(data_dir, "legal_nlp_training_dataset.json")
    
    df.to_csv(csv_path, index=False, encoding="utf-8")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(augmented_records, f, indent=2, ensure_ascii=False)

    print(f"Dataset compiled: {len(df)} total labeled legal examples.")
    print(f"Saved CSV: {csv_path}")
    print(f"Saved JSON: {json_path}")
    print("\nClass Distribution across Jurisdictions:")
    print(df["jurisdiction"].value_counts())
    print("\nClass Distribution across Legal Domains:")
    print(df["domain"].value_counts())

if __name__ == "__main__":
    generate_and_save_dataset()
