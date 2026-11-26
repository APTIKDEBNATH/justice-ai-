"""
Justice AI - Persistent ChromaDB Vector Database & Semantic Retrieval Engine
Embeds and indexes multi-jurisdictional statutory provisions, state excise codes,
motor vehicle regulations, and consumer statutes using ChromaDB with cosine similarity.
"""

import os
import chromadb
from typing import List, Dict, Any, Optional

CHROMA_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "chroma_db")
COLLECTION_NAME = "statutory_knowledge_base"

# Canonical Statutory & Regulatory Corpus for Vector Database
VECTOR_STATUTES = [
    # ---------------- INDIA: TRAFFIC & MOTOR VEHICLES ----------------
    {
        "id": "in_mv_200",
        "jurisdiction": "IN",
        "category": "Traffic & Motor Vehicles Law",
        "act": "Motor Vehicles Act, 1988",
        "section": "Section 200 & Virtual Courts",
        "title": "Compounding of Traffic Offenses and Contesting via Virtual Court",
        "summary": "Under Section 200 of the Motor Vehicles Act 1988, specified traffic offenses can be compounded by paying the statutory fee to authorized officers. If a citizen disputes the violation or penalty, they are not obligated to pay on the spot. Instead, the challan is transmitted to the Virtual Court (vcourts.gov.in) where the citizen can plead not guilty, present evidence, or contest before a Judicial Magistrate. Pending challans can also be settled with significant fee waivers at the National Lok Adalat.",
        "source_domain": "vcourts.gov.in",
        "source_url": "https://vcourts.gov.in",
        "tags": "traffic fine challan options contest virtual court lok adalat section 200 police dispute"
    },
    {
        "id": "in_mv_139",
        "jurisdiction": "IN",
        "category": "Traffic & Motor Vehicles Law",
        "act": "Central Motor Vehicles Rules, 1989",
        "section": "Rule 139 & Section 130",
        "title": "Production of Driving Licence & Documents on Demand",
        "summary": "Under Rule 139 of CMVR and Section 130 of the Motor Vehicles Act, a driver who does not have physical or digital copies (via DigiLocker or mParivahan) of their Driving Licence, Registration Certificate, or Insurance on demand has a statutory right to produce these documents within 15 days at the relevant police station or authority, reducing the non-production fine to a nominal administrative fee of ₹100 instead of thousands.",
        "source_domain": "echallan.parivahan.gov.in",
        "source_url": "https://echallan.parivahan.gov.in",
        "tags": "challan documents 15 days digilocker driving licence rc insurance rule 139 traffic police"
    },
    {
        "id": "in_mv_speed_jalandhar",
        "jurisdiction": "IN",
        "category": "Traffic & Motor Vehicles Law",
        "act": "Motor Vehicles Act, 1988 & Punjab Transport Department",
        "section": "Section 112 & Section 183",
        "title": "Speed Limits in Jalandhar, Punjab (NH-44 vs Municipal Limits)",
        "summary": "Under Section 112 of the Motor Vehicles Act 1988 and Punjab State Transport Department notifications: On National Highway 44 (GT Road passing Jalandhar, PAP Chowk to Rama Mandi), the speed limit for Light Motor Vehicles (Cars) is 90 km/h (up to 100 km/h on express stretches) and 80 km/h for heavy vehicles. Inside Jalandhar Municipal limits (city roads, Model Town, Cantt Road, BMC Chowk), the speed limit is 50 km/h for cars, 45 km/h for two-wheelers, and 25-30 km/h in school/residential zones. Section 183 imposes fines of ₹1,000-₹2,000 for LMVs for first over-speeding offense.",
        "source_domain": "punjabtransport.org",
        "source_url": "https://punjabtransport.org",
        "tags": "speed limit jalandhar punjab driving car nh 44 gt road section 112 section 183 overspeeding"
    },

    # ---------------- INDIA: EXCISE & DRINKING AGE ----------------
    {
        "id": "in_excise_drinking_age",
        "jurisdiction": "IN",
        "category": "State Excise & Regulatory Law",
        "act": "State Excise Acts & Constitution of India",
        "section": "Seventh Schedule List II & State Specific Acts",
        "title": "Legal Drinking Age in India (State-by-State Variation)",
        "summary": "In India, alcohol regulation is exclusively a State subject under Entry 8, List II (State List) of the Seventh Schedule to the Constitution. Consequently, there is no uniform national drinking age: In Punjab, Haryana, Chandigarh, and Delhi (under the Punjab Excise Act 1914 Section 29 and Delhi Excise Act 2009), the legal drinking and purchasing age is 25 years. In Maharashtra, it is 21 for beer/wine and 25 for hard liquor. In Uttar Pradesh, Karnataka, West Bengal, and Tamil Nadu, it is 21 years. In Goa, Himachal Pradesh, Rajasthan, and Sikkim, it is 18 years. In Dry States (Gujarat, Bihar, Nagaland, Mizoram), sale and consumption are totally prohibited.",
        "source_domain": "indiacode.nic.in",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2264",
        "tags": "legal drinking age india alcohol punjab haryana delhi 25 years goa 18 maharashtra 21 dry state bihar gujarat"
    },

    # ---------------- INDIA: CONSUMER PROTECTION ----------------
    {
        "id": "in_consumer_39",
        "jurisdiction": "IN",
        "category": "Consumer Protection & Defective Goods",
        "act": "Consumer Protection Act, 2019",
        "section": "Section 39",
        "title": "Remedies and Orders of District Consumer Commission",
        "summary": "Where goods or online orders suffer from defects, deficiencies, or unfair trade practices, the District Consumer Disputes Redressal Commission may order removal of defect, replacement with new goods, full refund with interest, and punitive compensation for mental agony under Section 39. Complaints can be filed electronically via e-Daakhil.",
        "source_domain": "indiacode.nic.in",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/15256",
        "tags": "consumer defective goods refund replacement e-daakhil section 39 online shopping complaint"
    },
    {
        "id": "in_consumer_69",
        "jurisdiction": "IN",
        "category": "Consumer Protection & Defective Goods",
        "act": "Consumer Protection Act, 2019",
        "section": "Section 69",
        "title": "Limitation Period for Consumer Complaints (2 Years)",
        "summary": "Under Section 69, the District, State, or National Commission shall not admit a complaint unless it is filed within two years from the date on which the cause of action has arisen.",
        "source_domain": "indiacode.nic.in",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/15256",
        "tags": "consumer limitation period 2 years time limit filing deadline section 69"
    },

    # ---------------- INDIA: BNS CRIMINAL LAW ----------------
    {
        "id": "in_bns_318",
        "jurisdiction": "IN",
        "category": "Criminal & Penal Law",
        "act": "Bharatiya Nyaya Sanhita, 2023 (BNS)",
        "section": "Section 318",
        "title": "Cheating and Fraudulent Inducement (Replaces IPC 420)",
        "summary": "Section 318 of BNS 2023 replaces legacy IPC Section 420. Whoever cheats and dishonestly induces the person deceived to deliver any property shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.",
        "source_domain": "indiacode.nic.in",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/20340",
        "tags": "bns section 318 cheating fraud ipc 420 criminal criminal code 7 years"
    },
    {
        "id": "in_bns_theft_housebreak",
        "jurisdiction": "IN",
        "category": "Criminal & Penal Law",
        "act": "Bharatiya Nyaya Sanhita, 2023 (BNS)",
        "section": "Section 305 & Section 331",
        "title": "Theft in Dwelling House & House-breaking (Burglary / Intruders)",
        "summary": "Under Section 305 of the Bharatiya Nyaya Sanhita (BNS 2023), whoever commits theft in any building, tent, or vessel used as a human dwelling or for custody of property shall be punished with imprisonment up to 7 years and fine. Under Section 331 BNS, lurking house-trespass or house-breaking by night is punishable with rigorous imprisonment up to 10 years and fine. Stolen property recovery is mandated under Section 317 BNS.",
        "source_domain": "indiacode.nic.in",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/20340",
        "tags": "intruder theft burglary house breaking stole items stolen house trespass bns 305 bns 331 chennai tamil nadu"
    },
    {
        "id": "in_bnss_173_fir",
        "jurisdiction": "IN",
        "category": "Criminal & Penal Law",
        "act": "Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)",
        "section": "Section 173",
        "title": "Mandatory Registration of First Information Report (FIR / Zero FIR)",
        "summary": "Under Section 173 of the BNSS 2023, police officers are legally obligated to register an FIR upon receiving information relating to the commission of a cognizable offense (such as housebreaking or theft). If the station is outside local jurisdiction, they must register a Zero FIR and transfer it. The complainant has the statutory right to receive a free signed copy of the registered FIR immediately.",
        "source_domain": "indiacode.nic.in",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/20341",
        "tags": "fir zero fir police complaint register fir section 173 bnss police station free copy"
    },
    {
        "id": "in_bsa_63_evidence",
        "jurisdiction": "IN",
        "category": "Criminal & Penal Law",
        "act": "Bharatiya Sakshya Adhiniyam, 2023 (BSA)",
        "section": "Section 63",
        "title": "Admissibility of Electronic Records & CCTV Video Evidence",
        "summary": "Under Section 63 of the BSA 2023 (replaces Section 65B of Indian Evidence Act), electronic records including CCTV surveillance footage, mobile phone photos, and digital recordings are fully admissible as primary documentary evidence in court when accompanied by an electronic certificate identifying the recording device.",
        "source_domain": "indiacode.nic.in",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/20342",
        "tags": "cctv evidence proof electronic record video footage photo certificate section 63 bsa"
    },

    # ---------------- GERMANY: TENANCY & BGB ----------------
    {
        "id": "de_bgb_573",
        "jurisdiction": "DE",
        "category": "Tenancy: Eviction & Termination Notice",
        "act": "BGB (Bürgerliches Gesetzbuch)",
        "section": "§ 573",
        "title": "Ordinary Termination by the Landlord (Justified Interest / Eigenbedarf)",
        "summary": "Under German Civil Code (BGB) § 573, a landlord can only terminate an open-ended residential lease if they have a justified legitimate interest (berechtigtes Interesse). Valid reasons include genuine personal use (Eigenbedarf) for the landlord or immediate family, or substantial culpable breach of contract by the tenant. The termination notice must state the specific reasons.",
        "source_domain": "gesetze-im-internet.de",
        "source_url": "https://www.gesetze-im-internet.de/bgb/__573.html",
        "tags": "germany bgb 573 landlord eviction termination reason eigenbedarf lease"
    },
    {
        "id": "de_bgb_573c",
        "jurisdiction": "DE",
        "category": "Tenancy: Eviction & Termination Notice",
        "act": "BGB (Bürgerliches Gesetzbuch)",
        "section": "§ 573c",
        "title": "Notice Periods for Lease Termination",
        "summary": "Under BGB § 573c(1), the landlord's notice period is 3 months for tenancies up to 5 years, extends to 6 months after 5 years, and reaches 9 months after 8 years of tenancy. The tenant's statutory notice period is standard 3 months.",
        "source_domain": "gesetze-im-internet.de",
        "source_url": "https://www.gesetze-im-internet.de/bgb/__573c.html",
        "tags": "germany bgb 573c notice period 3 months 6 months 9 months 8 years tenancy"
    },

    # ---------------- EUROPEAN UNION: GDPR ----------------
    {
        "id": "eu_gdpr_17",
        "jurisdiction": "EU",
        "category": "Data Privacy & GDPR",
        "act": "General Data Protection Regulation (Regulation EU 2016/679)",
        "section": "Article 17",
        "title": "Right to Erasure ('Right to be Forgotten')",
        "summary": "Article 17 of GDPR gives individuals the statutory right to mandate that data controllers erase their personal data without undue delay when data is no longer necessary for its original purpose, consent has been withdrawn, or processing is unlawful.",
        "source_domain": "eur-lex.europa.eu",
        "source_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679",
        "tags": "gdpr article 17 right to erasure right to be forgotten privacy delete profile tech platform"
    },

    # ---------------- UNITED STATES: EMPLOYMENT ----------------
    {
        "id": "us_flsa_207",
        "jurisdiction": "US",
        "category": "Employment & Wage Rights",
        "act": "Fair Labor Standards Act (FLSA)",
        "section": "29 U.S.C. § 207",
        "title": "Maximum Hours & Overtime Compensation (1.5x Regular Rate)",
        "summary": "Under 29 U.S.C. § 207 of FLSA, non-exempt employees who work over 40 hours in a workweek must receive overtime compensation at a rate not less than one and one-half times their regular rate of pay. Employers withholding overtime pay face statutory liability for back wages and liquidated damages.",
        "source_domain": "law.cornell.edu",
        "source_url": "https://www.law.cornell.edu/uscode/text/29/207",
        "tags": "flsa 29 usc 207 overtime 1.5x 40 hours wage theft unpaid compensation employment"
    },

    # ---------------- SWITZERLAND: CODE OF OBLIGATIONS (TENANCY & EMPLOYMENT) ----------------
    {
        "id": "ch_co_266c_tenancy",
        "jurisdiction": "CH",
        "category": "Tenancy: Eviction & Termination Notice",
        "act": "Swiss Code of Obligations (SR 220)",
        "section": "Art. 266c, 266d & 266l",
        "title": "Residential & Commercial Lease Notice Periods and Official Form Requirement",
        "summary": "Under Art. 266c of the Swiss Code of Obligations (OR/CO), residential tenancies require at least 3 months' notice (Art. 266d sets 6 months for commercial premises). Under Art. 266l, notice of termination by the landlord must be given in writing using an official form approved by the canton; for family homes, separate notices must be served on both spouses (Art. 266n), otherwise the termination is void (Art. 266o).",
        "source_domain": "fedlex.admin.ch",
        "source_url": "https://www.fedlex.admin.ch/eli/cc/27/317_321_377/en#art_266c",
        "tags": "switzerland swiss eviction notice landlord termination lease 3 months official cantonal form art 266c 266l"
    },
    {
        "id": "ch_co_271_challenge",
        "jurisdiction": "CH",
        "category": "Tenancy: Eviction & Termination Notice",
        "act": "Swiss Code of Obligations (SR 220)",
        "section": "Art. 271 & Art. 273",
        "title": "Challenging Unfair Lease Termination before the Conciliation Authority (30 Days)",
        "summary": "Under Art. 271 and Art. 273 CO, a tenant may challenge a notice of termination that contravenes good faith—or request a lease extension under Art. 272—by filing with the local conciliation authority (Schlichtungsbehörde / autorité de conciliation) within 30 days of receiving the notice.",
        "source_domain": "fedlex.admin.ch",
        "source_url": "https://www.fedlex.admin.ch/eli/cc/27/317_321_377/en#art_271",
        "tags": "switzerland swiss contest challenge termination 30 days conciliation authority schlichtungsbehoerde art 271 273"
    },
    {
        "id": "ch_co_335c_employment",
        "jurisdiction": "CH",
        "category": "Employment & Wage Rights",
        "act": "Swiss Code of Obligations (SR 220)",
        "section": "Art. 335c",
        "title": "Notice Periods for Termination of Employment Contracts",
        "summary": "Under Art. 335c CO, an employment relationship may be terminated at the end of a month by giving 1 month's notice in the first year of service, 2 months from the second to ninth year, and 3 months thereafter.",
        "source_domain": "fedlex.admin.ch",
        "source_url": "https://www.fedlex.admin.ch/eli/cc/27/317_321_377/en#art_335c",
        "tags": "switzerland swiss employment termination notice period salary art 335c"
    },

    # ---------------- UNITED KINGDOM: TENANCY, CONSUMER, EMPLOYMENT, PRIVACY ----------------
    {
        "id": "gb_housing_1988",
        "jurisdiction": "GB",
        "category": "Tenancy: Eviction & Termination Notice",
        "act": "Housing Act 1988",
        "section": "Section 8 & Part I",
        "title": "Statutory Grounds & Notice Requirements for Residential Possession",
        "summary": "Under the Housing Act 1988 (as amended), residential landlords must serve valid statutory written notice specifying recognized legal grounds and notice periods and obtain a court possession order before eviction.",
        "source_domain": "legislation.gov.uk",
        "source_url": "https://www.legislation.gov.uk/ukpga/1988/50/contents",
        "tags": "uk united kingdom england landlord eviction notice housing act 1988 possession"
    },
    {
        "id": "gb_cra_2015",
        "jurisdiction": "GB",
        "category": "Consumer Protection & Defective Goods",
        "act": "Consumer Rights Act 2015",
        "section": "Sections 9, 19–24",
        "title": "Goods of Satisfactory Quality, 30-Day Right to Reject & Refund Remedies",
        "summary": "Under the Consumer Rights Act 2015, goods must be of satisfactory quality, fit for purpose, and as described. Consumers have a 30-day short-term right to reject faulty goods for a full refund, or demand repair/replacement.",
        "source_domain": "legislation.gov.uk",
        "source_url": "https://www.legislation.gov.uk/ukpga/2015/15/contents",
        "tags": "uk united kingdom consumer rights act 2015 defective goods refund repair replacement"
    },
    {
        "id": "gb_era_1996",
        "jurisdiction": "GB",
        "category": "Employment & Wage Rights",
        "act": "Employment Rights Act 1996",
        "section": "Sections 86 & 94",
        "title": "Minimum Notice Periods and Right Not to Be Unfairly Dismissed",
        "summary": "The Employment Rights Act 1996 establishes statutory minimum notice periods for termination, protection against unfair dismissal, itemized pay statements, and unlawful deduction remedies.",
        "source_domain": "legislation.gov.uk",
        "source_url": "https://www.legislation.gov.uk/ukpga/1996/18/contents",
        "tags": "uk united kingdom employment unfair dismissal wages notice period"
    },
    {
        "id": "gb_dpa_2018",
        "jurisdiction": "GB",
        "category": "Data Privacy & GDPR",
        "act": "Data Protection Act 2018 (UK GDPR)",
        "section": "Part 2 & Chapter 3",
        "title": "Data Subject Access, Rectification & Erasure Rights",
        "summary": "The UK Data Protection Act 2018 alongside UK GDPR provides enforceable rights to access personal data, demand erasure, and complain to the Information Commissioner's Office (ICO).",
        "source_domain": "legislation.gov.uk",
        "source_url": "https://www.legislation.gov.uk/ukpga/2018/12/contents",
        "tags": "uk united kingdom privacy gdpr data protection erasure ico"
    },

    # ---------------- CANADA: LABOUR & PRIVACY ----------------
    {
        "id": "ca_clc_employment",
        "jurisdiction": "CA",
        "category": "Employment & Wage Rights",
        "act": "Canada Labour Code (R.S.C., 1985, c. L-2)",
        "section": "Part III (Divisions IX–XI)",
        "title": "Termination Notice, Severance Pay & Unjust Dismissal Protections",
        "summary": "Part III of the Canada Labour Code sets statutory standards for minimum notice of termination, severance pay, hours of work, overtime, and unjust dismissal complaints in federally regulated workplaces.",
        "source_domain": "laws-lois.justice.gc.ca",
        "source_url": "https://laws-lois.justice.gc.ca/eng/acts/L-2/",
        "tags": "canada labour code employment overtime wages termination severance"
    },
    {
        "id": "ca_pipeda_privacy",
        "jurisdiction": "CA",
        "category": "Data Privacy & GDPR",
        "act": "Personal Information Protection and Electronic Documents Act (PIPEDA)",
        "section": "Schedule 1 (Fair Information Principles)",
        "title": "Consent, Access, and Commercial Data Privacy Protections",
        "summary": "PIPEDA requires private-sector organizations in Canada to obtain meaningful consent, protect personal information with safeguards, report security breaches, and honor consumer access/correction requests.",
        "source_domain": "laws-lois.justice.gc.ca",
        "source_url": "https://laws-lois.justice.gc.ca/eng/acts/P-8.6/",
        "tags": "canada privacy personal information pipeda data breach delete access"
    },

    # ---------------- AUSTRALIA: CONSUMER & WORKPLACE ----------------
    {
        "id": "au_acl_2010",
        "jurisdiction": "AU",
        "category": "Consumer Protection & Defective Goods",
        "act": "Competition and Consumer Act 2010 (Australian Consumer Law)",
        "section": "Schedule 2 · Consumer Guarantees",
        "title": "Acceptable Quality Guarantees & Remedies for Major Failures",
        "summary": "Under Schedule 2 (Australian Consumer Law), consumers are entitled to automatic statutory guarantees that goods are of acceptable quality; for major failures, consumers may choose a full refund or replacement.",
        "source_domain": "legislation.gov.au",
        "source_url": "https://www.legislation.gov.au/C2004A00109/latest/text",
        "tags": "australia acl consumer guarantee refund defective product replacement"
    },
    {
        "id": "au_fwa_2009",
        "jurisdiction": "AU",
        "category": "Employment & Wage Rights",
        "act": "Fair Work Act 2009",
        "section": "Part 2-2 (National Employment Standards)",
        "title": "Minimum Notice, Maximum Weekly Hours & Unfair Dismissal Remedies",
        "summary": "The Fair Work Act 2009 establishes the National Employment Standards (NES), minimum termination notice periods, overtime/award protections, and unfair dismissal applications via the Fair Work Commission.",
        "source_domain": "legislation.gov.au",
        "source_url": "https://www.legislation.gov.au/C2009A00028/latest/text",
        "tags": "australia fair work act employment wages dismissal notice"
    },

    # ---------------- SINGAPORE: EMPLOYMENT, CONSUMER & HARASSMENT ----------------
    {
        "id": "sg_ea_1968",
        "jurisdiction": "SG",
        "category": "Employment & Wage Rights",
        "act": "Employment Act 1968 (Singapore)",
        "section": "Parts II–IV",
        "title": "Statutory Salary Payment, Notice of Termination & Overtime Rights",
        "summary": "Singapore's Employment Act 1968 governs basic terms of employment, timely salary payment, termination notice requirements, leave entitlements, and rest/overtime rules.",
        "source_domain": "sso.agc.gov.sg",
        "source_url": "https://sso.agc.gov.sg/Act/EmA1968",
        "tags": "singapore employment act salary wages termination notice overtime"
    },
    {
        "id": "sg_cpfta_2003",
        "jurisdiction": "SG",
        "category": "Consumer Protection & Defective Goods",
        "act": "Consumer Protection (Fair Trading) Act 2003",
        "section": "Part 2 & Part 3 (Lemon Law)",
        "title": "Protection Against Unfair Practices & Defective Goods Remedies",
        "summary": "Singapore's CPFTA protects consumers against unfair trading practices and misleading claims, and provides statutory 'Lemon Law' remedies (repair, replacement, price reduction, or refund) for defective goods.",
        "source_domain": "sso.agc.gov.sg",
        "source_url": "https://sso.agc.gov.sg/Act/CPFTA2003",
        "tags": "singapore consumer protection defective goods refund lemon law cpfta"
    },
    {
        "id": "sg_poha_2014",
        "jurisdiction": "SG",
        "category": "Criminal & Penal Law",
        "act": "Protection from Harassment Act 2014",
        "section": "Sections 3–13",
        "title": "Protection Orders and Civil/Criminal Remedies Against Harassment & Stalking",
        "summary": "The Protection from Harassment Act 2014 prohibits threatening, abusive, or insulting communication (including online) and enables expedited protection orders and damages.",
        "source_domain": "sso.agc.gov.sg",
        "source_url": "https://sso.agc.gov.sg/Act/PHA2014",
        "tags": "singapore harassment stalking online abuse protection order"
    }
]

_vector_client: Optional[chromadb.ClientAPI] = None
_vector_collection = None

def get_vector_db():
    global _vector_client, _vector_collection
    if _vector_collection is None:
        os.makedirs(CHROMA_DATA_DIR, exist_ok=True)
        # Initialize persistent ChromaDB client
        _vector_client = chromadb.PersistentClient(path=CHROMA_DATA_DIR)
        _vector_collection = _vector_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "Justice AI Official Statutory Embeddings"}
        )
        
        # Populate if empty or outdated
        existing_count = _vector_collection.count()
        if existing_count < len(VECTOR_STATUTES):
            ids = [s["id"] for s in VECTOR_STATUTES]
            documents = [f"{s['act']} {s['section']} {s['title']} {s['summary']} {s['tags']}" for s in VECTOR_STATUTES]
            metadatas = [
                {
                    "act": s["act"],
                    "section": s["section"],
                    "title": s["title"],
                    "jurisdiction": s["jurisdiction"],
                    "category": s["category"],
                    "summary": s["summary"],
                    "source_domain": s["source_domain"],
                    "source_url": s["source_url"]
                }
                for s in VECTOR_STATUTES
            ]
            _vector_collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
            print(f"[VectorDB] ChromaDB initialized with {_vector_collection.count()} statutory vectors.")
    return _vector_collection

def query_vector_db(query: str, jurisdiction: str = "AUTO", category: str = "AUTO", top_k: int = 2) -> List[Dict[str, Any]]:
    """
    Executes semantic vector search using cosine distance over statutory embeddings.
    """
    col = get_vector_db()
    jur_norm = "GB" if jurisdiction == "UK" else jurisdiction

    where_filter = None
    if jur_norm not in ("AUTO", "GLOBAL") and category not in ("AUTO", "General"):
        where_filter = {"$and": [{"jurisdiction": jur_norm}, {"category": category}]}
    elif jur_norm not in ("AUTO", "GLOBAL"):
        where_filter = {"jurisdiction": jur_norm}
    elif category not in ("AUTO", "General"):
        where_filter = {"category": category}

    def _run_query(wf):
        res = col.query(query_texts=[query], n_results=top_k, where=wf)
        out = []
        if res and "metadatas" in res and res["metadatas"]:
            for meta_list in res["metadatas"]:
                for m in meta_list:
                    out.append(dict(m))
        return out

    try:
        matched_statutes = _run_query(where_filter)
    except Exception:
        matched_statutes = []

    # If strict (jurisdiction + category) yielded nothing, broaden within the same jurisdiction first
    if not matched_statutes and jur_norm not in ("AUTO", "GLOBAL"):
        try:
            matched_statutes = _run_query({"jurisdiction": jur_norm})
        except Exception:
            matched_statutes = []

    # Only fall back to global semantic search when jurisdiction is AUTO or GLOBAL
    if not matched_statutes and jur_norm in ("AUTO", "GLOBAL"):
        try:
            matched_statutes = _run_query(None)
        except Exception:
            matched_statutes = []

    return matched_statutes

# Initialize on import
try:
    get_vector_db()
except Exception as e:
    print(f"[VectorDB] Warning on auto-init: {e}")
