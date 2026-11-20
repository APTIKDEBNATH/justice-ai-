"""
LexGlobal AI - Configuration and Global Settings
"""

import os
from typing import Dict, Any

APP_TITLE = "LexGlobal AI"
APP_SUBTITLE = "Universal AI-Assisted Legal Intelligence & Case Management Suite"
APP_VERSION = "2.0.0"

# Supported Global Jurisdictions
JURISDICTIONS: Dict[str, Dict[str, Any]] = {
    "GLOBAL": {
        "name": "Global / International Law",
        "flag": "🌐",
        "family": "Transnational / International",
        "key_frameworks": [
            "UN CISG (Contracts for International Sale of Goods)",
            "UNCITRAL Model Law on International Commercial Arbitration",
            "New York Convention (1958) on Foreign Arbitral Awards",
            "WIPO Intellectual Property Treaties",
            "Universal Declaration of Human Rights (UDHR)"
        ],
        "currency": "USD / EUR",
        "primary_courts": "International Court of Justice (ICJ), Permanent Court of Arbitration (PCA), ICC Court of Arbitration"
    },
    "US": {
        "name": "United States",
        "flag": "🇺🇸",
        "family": "Common Law (Federal + 50 State Systems)",
        "key_frameworks": [
            "Uniform Commercial Code (UCC Article 2 - Sales)",
            "Title 18 United States Code (Federal Crimes)",
            "Fair Labor Standards Act (FLSA - Wage & Hour)",
            "Americans with Disabilities Act (ADA)",
            "Digital Millennium Copyright Act (DMCA)",
            "California Consumer Privacy Act (CCPA/CPRA)",
            "Federal Rules of Civil Procedure (FRCP)"
        ],
        "currency": "USD ($)",
        "primary_courts": "Supreme Court of the US, Federal District Courts, State Supreme/Superior Courts"
    },
    "UK": {
        "name": "United Kingdom",
        "flag": "🇬🇧",
        "family": "Common Law (England & Wales, Scotland, Northern Ireland)",
        "key_frameworks": [
            "Employment Rights Act 1996",
            "Consumer Rights Act 2015",
            "Data Protection Act 2018 (UK GDPR)",
            "Sale of Goods Act 1979",
            "Equality Act 2010",
            "Companies Act 2006",
            "Civil Procedure Rules (CPR)"
        ],
        "currency": "GBP (£)",
        "primary_courts": "Supreme Court of the UK, Court of Appeal, High Court of Justice, Crown Court, County Court"
    },
    "IN": {
        "name": "India",
        "flag": "🇮🇳",
        "family": "Common Law / Statutory Codes",
        "key_frameworks": [
            "Bharatiya Nyaya Sanhita, 2023 (BNS - Penal Code)",
            "Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS - Criminal Procedure)",
            "Bharatiya Sakshya Adhiniyam, 2023 (BSA - Evidence)",
            "Indian Contract Act, 1872",
            "Consumer Protection Act, 2019",
            "Digital Personal Data Protection Act, 2023 (DPDP)",
            "Information Technology Act, 2000 (Section 66, 43A)",
            "Specific Relief Act, 1963",
            "Negotiable Instruments Act, 1881 (Section 138 Cheque Bounce)"
        ],
        "currency": "INR (₹)",
        "primary_courts": "Supreme Court of India, State High Courts, District & Sessions Courts, Consumer Disputes Commissions (NCDRC)"
    },
    "EU": {
        "name": "European Union",
        "flag": "🇪🇺",
        "family": "Civil Law / Supranational EU Law",
        "key_frameworks": [
            "General Data Protection Regulation (EU GDPR 2016/679)",
            "EU Artificial Intelligence Act (2024)",
            "Rome I Regulation (Law Applicable to Contractual Obligations)",
            "Brussels I Regulation (Recast - Jurisdiction & Enforcement)",
            "Digital Services Act (DSA) & Digital Markets Act (DMA)",
            "EU Consumer Rights Directive (2011/83/EU)"
        ],
        "currency": "EUR (€)",
        "primary_courts": "Court of Justice of the European Union (CJEU), General Court, National Member State Courts"
    },
    "CA": {
        "name": "Canada",
        "flag": "🇨🇦",
        "family": "Common Law (Civil Law in Quebec)",
        "key_frameworks": [
            "Criminal Code (RSC 1985, c C-46)",
            "Canada Labour Code (RSC 1985, c L-2)",
            "Personal Information Protection and Electronic Documents Act (PIPEDA)",
            "Civil Code of Quebec (CCQ - for Quebec)",
            "Competition Act (RSC 1985, c C-34)"
        ],
        "currency": "CAD (C$)",
        "primary_courts": "Supreme Court of Canada, Federal Court of Appeal, Provincial Courts of Appeal"
    },
    "AU": {
        "name": "Australia",
        "flag": "🇦🇺",
        "family": "Common Law (Commonwealth + States/Territories)",
        "key_frameworks": [
            "Competition and Consumer Act 2010 (Australian Consumer Law - ACL)",
            "Fair Work Act 2009 (Workplace Relations)",
            "Privacy Act 1988 (Australian Privacy Principles - APPs)",
            "Corporations Act 2001",
            "Criminal Code Act 1995"
        ],
        "currency": "AUD (A$)",
        "primary_courts": "High Court of Australia, Federal Court of Australia, State Supreme Courts"
    },
    "SG": {
        "name": "Singapore",
        "flag": "🇸🇬",
        "family": "Common Law (Statutory Codes & English Precedents)",
        "key_frameworks": [
            "Penal Code 1871 (Rev. Ed. 2020)",
            "Personal Data Protection Act 2012 (PDPA)",
            "Employment Act 1968",
            "Consumer Protection (Fair Trading) Act 2003",
            "International Arbitration Act 1994 (SIAC Rules)"
        ],
        "currency": "SGD (S$)",
        "primary_courts": "Supreme Court of Singapore (Court of Appeal & High Court), State Courts, Singapore International Commercial Court (SICC)"
    },
    "DE": {
        "name": "Germany",
        "flag": "🇩🇪",
        "family": "Civil Law (Germanic / Roman Tradition)",
        "key_frameworks": [
            "Bürgerliches Gesetzbuch (BGB - Civil Code)",
            "Strafgesetzbuch (StGB - Criminal Code)",
            "Handelsgesetzbuch (HGB - Commercial Code)",
            "Bundesdatenschutzgesetz (BDSG - Data Protection)",
            "Zivilprozessordnung (ZPO - Civil Procedure)"
        ],
        "currency": "EUR (€)",
        "primary_courts": "Bundesverfassungsgericht (BVerfG), Bundesgerichtshof (BGH), Bundesarbeitsgericht (BAG)"
    },
    "FR": {
        "name": "France",
        "flag": "🇫🇷",
        "family": "Civil Law (Napoleonic Code Tradition)",
        "key_frameworks": [
            "Code Civil (Civil Code - Contracts, Torts, Property)",
            "Code Pénal (Penal Code)",
            "Code du Travail (Labor Code)",
            "Code de Commerce (Commercial Code)",
            "Code de la Consommation (Consumer Code)"
        ],
        "currency": "EUR (€)",
        "primary_courts": "Cour de Cassation, Conseil d'État, Cours d'Appel, Tribunaux Judiciaires"
    },
    "AE": {
        "name": "United Arab Emirates",
        "flag": "🇦🇪",
        "family": "Civil Law / Islamic Sharia / Common Law Free Zones (DIFC, ADGM)",
        "key_frameworks": [
            "Federal Decree-Law No. 33 of 2021 (Labour Relations)",
            "Federal Decree-Law No. 42 of 2022 (Civil Procedures)",
            "Federal Law No. 5 of 1985 (Civil Transactions Code)",
            "DIFC Contract Law & Employment Law (Common Law in DIFC)",
            "Federal Decree-Law No. 45 of 2021 (Personal Data Protection)"
        ],
        "currency": "AED (د.إ)",
        "primary_courts": "Federal Supreme Court, Dubai/Abu Dhabi Courts, DIFC Courts, ADGM Courts"
    },
    "ZA": {
        "name": "South Africa",
        "flag": "🇿🇦",
        "family": "Hybrid (Roman-Dutch Civil Law & English Common Law)",
        "key_frameworks": [
            "Constitution of the Republic of South Africa, 1996",
            "Protection of Personal Information Act (POPIA 2013)",
            "Labour Relations Act 66 of 1995",
            "Consumer Protection Act 68 of 2008",
            "Companies Act 71 of 2008"
        ],
        "currency": "ZAR (R)",
        "primary_courts": "Constitutional Court of South Africa, Supreme Court of Appeal, High Courts"
    }
}

# Legal Specialization Domains
LEGAL_DOMAINS = [
    "General Legal Counsel & Triage",
    "Contracts & Commercial Transactions",
    "Employment & Labor Rights",
    "Tenancy & Real Estate",
    "Consumer Protection & Fair Trade",
    "Data Privacy & Cybersecurity (GDPR, CCPA, DPDP)",
    "Intellectual Property (Copyright, Trademark, Patent)",
    "Corporate & Company Compliance",
    "Criminal Law & Statutory Offences",
    "Civil Litigation & Dispute Resolution"
]

# Emergency Contact Hotlines by Jurisdiction
EMERGENCY_HOTLINES = {
    "GLOBAL": "Please contact your national emergency response service or local police department.",
    "US": "Emergency: 911 | National Domestic Violence Hotline: 1-800-799-SAFE (7233) | Suicide & Crisis: 988",
    "UK": "Emergency: 999 or 112 | Non-Emergency Police: 101 | National Domestic Abuse: 0808 2000 247",
    "IN": "National Emergency: 112 | Police: 100 | Women Helpline: 1091 | Cyber Crime: 1930",
    "EU": "Pan-European Emergency: 112 | Medical: 112 | Police: 112",
    "CA": "Emergency: 911 | Crisis Services Canada: 1-833-456-4566",
    "AU": "Emergency: 000 | 1800RESPECT: 1800 737 732 | Lifeline: 13 11 14",
    "SG": "Police: 999 | Ambulance/Fire: 995 | National Anti-Violence: 1800-777-0000",
    "DE": "Police: 110 | Emergency/Fire: 112 | Violence Against Women: 116 016",
    "FR": "Emergency: 112 | Police (Police Secours): 17 | SAMU: 15",
    "AE": "Police: 999 | Ambulance: 998 | Civil Defence: 997",
    "ZA": "Police: 10111 | Ambulance: 10177 | National Emergency: 112"
}
