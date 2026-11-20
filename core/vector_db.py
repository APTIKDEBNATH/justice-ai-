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
    
    where_filter = None
    if jurisdiction not in ("AUTO", "GLOBAL") and category not in ("AUTO", "General"):
        where_filter = {"$and": [{"jurisdiction": jurisdiction}, {"category": category}]}
    elif jurisdiction not in ("AUTO", "GLOBAL"):
        where_filter = {"jurisdiction": jurisdiction}
    elif category not in ("AUTO", "General"):
        where_filter = {"category": category}

    try:
        results = col.query(
            query_texts=[query],
            n_results=top_k,
            where=where_filter
        )
    except Exception as e:
        # If strict filter returned 0, retry without where filter
        results = col.query(
            query_texts=[query],
            n_results=top_k
        )

    matched_statutes = []
    if results and "metadatas" in results and results["metadatas"]:
        for meta_list in results["metadatas"]:
            for m in meta_list:
                matched_statutes.append(dict(m))

    return matched_statutes

# Initialize on import
try:
    get_vector_db()
except Exception as e:
    print(f"[VectorDB] Warning on auto-init: {e}")
