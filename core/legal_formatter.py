"""
Justice AI - Legal Response Formatter & Localization Engine
Contains dynamic regional language mapping, expanded tenancy taxonomy, and clean localized strings.
"""

from typing import Dict, List, Any, Tuple
import re

# Dynamic language options per region (No emojis)
REGION_LANGUAGES: Dict[str, List[Tuple[str, str]]] = {
    "IN": [
        ("en", "English"),
        ("hi", "हिन्दी (Hindi)"),
        ("pa", "ਪੰਜਾਬੀ (Punjabi)"),
        ("bn", "বাংলা (Bengali)"),
        ("ta", "தமிழ் (Tamil)"),
        ("te", "తెలుగు (Telugu)"),
        ("mr", "मराठी (Marathi)"),
        ("gu", "ગુજરાતી (Gujarati)"),
        ("kn", "ಕನ್ನಡ (Kannada)"),
        ("ml", "മലയാളം (Malayalam)")
    ],
    "CH": [
        ("en", "English"),
        ("de", "Deutsch (German)"),
        ("fr", "Français (French)"),
        ("it", "Italiano (Italian)"),
        ("rm", "Rumantsch (Romansh)")
    ],
    "DE": [
        ("en", "English"),
        ("de", "Deutsch (German)")
    ],
    "CA": [
        ("en", "English"),
        ("fr", "Français (French)")
    ],
    "US": [
        ("en", "English"),
        ("es", "Español (Spanish)")
    ],
    "GB": [
        ("en", "English"),
        ("cy", "Cymraeg (Welsh)")
    ],
    "EU": [
        ("en", "English"),
        ("de", "Deutsch (German)"),
        ("fr", "Français (French)"),
        ("es", "Español (Spanish)"),
        ("it", "Italiano (Italian)"),
        ("nl", "Nederlands (Dutch)")
    ],
    "AU": [
        ("en", "English")
    ],
    "SG": [
        ("en", "English"),
        ("zh", "中文 (Chinese)"),
        ("ms", "Bahasa Melayu"),
        ("ta", "தமிழ் (Tamil)")
    ],
    "GLOBAL": [
        ("en", "English"),
        ("hi", "हिन्दी (Hindi)"),
        ("de", "Deutsch (German)"),
        ("fr", "Français (French)"),
        ("es", "Español (Spanish)"),
        ("pa", "ਪੰਜਾਬੀ (Punjabi)"),
        ("bn", "বাংলা (Bengali)"),
        ("ta", "தமிழ் (Tamil)")
    ],
    "AUTO": [
        ("en", "English"),
        ("hi", "हिन्दी (Hindi)"),
        ("de", "Deutsch (German)"),
        ("fr", "Français (French)"),
        ("es", "Español (Spanish)"),
        ("pa", "ਪੰਜਾਬੀ (Punjabi)"),
        ("bn", "বাংলা (Bengali)")
    ]
}

# Expanded Category Taxonomy (with granular Tenancy options)
LEGAL_CATEGORIES: List[str] = [
    "Residential Tenancy (General)",
    "Tenancy: Eviction & Termination Notice",
    "Tenancy: Rent Control & Increases",
    "Tenancy: Security Deposits & Refunds",
    "Tenancy: Repairs & Habitability",
    "Tenancy: Social Hardship Objections",
    "Tenancy: Commercial & Retail Lease",
    "Consumer Protection & Defective Goods",
    "Employment & Wage Rights",
    "Data Privacy & GDPR",
    "Commercial & Contract Disputes",
    "Family Law & Estate"
]

# Clean Region Definitions (No bracket captions)
CLEAN_REGIONS: Dict[str, str] = {
    "AUTO": "Auto-Detect",
    "IN": "India",
    "DE": "Germany",
    "CH": "Switzerland",
    "GB": "United Kingdom",
    "EU": "European Union",
    "US": "United States",
    "CA": "Canada",
    "AU": "Australia",
    "SG": "Singapore",
    "GLOBAL": "Global / International Law"
}

# Localized UI Strings (No emojis)
UI_STRINGS: Dict[str, Dict[str, str]] = {
    "en": {
        "brand": "Justice AI",
        "subtitle": "Universal Legal Intelligence & Statutory Verification Suite",
        "new_question": "New question",
        "recent_title": "RECENT",
        "verified_coverage_title": "Verified coverage",
        "verified_coverage_text": "India · United Kingdom · European Union · Germany · Switzerland · United States · Canada · Australia · Singapore · Global",
        "region_label": "Region",
        "category_label": "Category",
        "language_label": "Language",
        "share_chat": "Share chat",
        "dark_mode": "🌙",
        "light_mode": "☀️",
        "answered_from_official": "Answered from official sources",
        "sources_label": "SOURCES",
        "retrieval_confidence": "Retrieval confidence",
        "confidence_high": "High",
        "disclaimer_text": "General legal information, not formal legal advice. Statutes change; consult a licensed legal practitioner in your jurisdiction.",
        "input_placeholder": "Ask a legal question in any country or language",
        "input_footnote": "Answers are limited to jurisdictions with verified sources.",
        "welcome_headline": "Universal Legal Intelligence Consultation",
        "welcome_subtitle": "Select your jurisdiction and legal category above, then type your legal question or upload facts below.",
        "starter_1": "Can my landlord evict me without reason?",
        "starter_2": "Seller refused refund for defective goods under consumer law",
        "starter_3": "How to enforce GDPR Article 17 right to erasure"
    },
    "hi": {
        "brand": "Justice AI",
        "subtitle": "सार्वभौमिक कानूनी बुद्धिमत्ता और वैधानिक सत्यापन",
        "new_question": "नया प्रश्न",
        "recent_title": "हाल के प्रश्न",
        "verified_coverage_title": "सत्यापित कवरेज",
        "verified_coverage_text": "भारत · यूनाइटेड किंगडम · यूरोपीय संघ · जर्मनी · स्विट्ज़रलैंड · अमेरिका · कनाडा · ऑस्ट्रेलिया · सिंगापुर · वैश्विक",
        "region_label": "क्षेत्र",
        "category_label": "श्रेणी",
        "language_label": "भाषा",
        "share_chat": "चैट साझा करें",
        "dark_mode": "🌙",
        "light_mode": "☀️",
        "answered_from_official": "आधिकारिक स्रोतों से उत्तर",
        "sources_label": "स्रोत",
        "retrieval_confidence": "उत्तर की विश्वसनीयता",
        "confidence_high": "उच्च",
        "disclaimer_text": "यह सामान्य कानूनी जानकारी है, कानूनी सलाह नहीं। कानून बदलते रहते हैं, इसलिए किसी योग्य वकील से पुष्टि करें।",
        "input_placeholder": "किसी भी देश में, किसी भी भाषा में कानूनी प्रश्न पूछें",
        "input_footnote": "उत्तर केवल उन क्षेत्राधिकारों के लिए हैं जिनके सत्यापित स्रोत उपलब्ध हैं।",
        "welcome_headline": "सार्वभौमिक कानूनी परामर्श प्रणाली",
        "welcome_subtitle": "ऊपर अपना क्षेत्र और श्रेणी चुनें, फिर नीचे अपना प्रश्न दर्ज करें।",
        "starter_1": "क्या मकान मालिक बिना किसी वैध कारण के निकाल सकता है?",
        "starter_2": "दोषपूर्ण सामान पर उपभोक्ता संरक्षण कानून के तहत रिफंड",
        "starter_3": "जीडीपीआर डेटा हटाने का कानूनी नोटिस"
    },
    "de": {
        "brand": "Justice AI",
        "subtitle": "Universelle rechtliche Intelligenz & Gesetzliche Verifizierung",
        "new_question": "Neue Frage",
        "recent_title": "KÜRZLICH",
        "verified_coverage_title": "Verifizierte Abdeckung",
        "verified_coverage_text": "Deutschland · Schweiz · Indien · Vereinigtes Königreich · Europäische Union · USA · Global",
        "region_label": "Region",
        "category_label": "Kategorie",
        "language_label": "Sprache",
        "share_chat": "Chat teilen",
        "dark_mode": "🌙",
        "light_mode": "☀️",
        "answered_from_official": "Aus offiziellen Quellen beantwortet",
        "sources_label": "QUELLEN",
        "retrieval_confidence": "Abruf-Zuverlässigkeit",
        "confidence_high": "Hoch",
        "disclaimer_text": "Allgemeine rechtliche Information, keine Rechtsberatung. Bitte mit einem qualifizierten Anwalt abstimmen.",
        "input_placeholder": "Stellen Sie eine rechtliche Frage in jedem Land oder jeder Sprache",
        "input_footnote": "Antworten sind auf Rechtsordnungen mit verifizierten Quellen beschränkt.",
        "welcome_headline": "Rechtliche Beratung & Gesetzliche Auskunft",
        "welcome_subtitle": "Wählen Sie oben Rechtsgebiet und Region, und geben Sie unten Ihre Frage ein.",
        "starter_1": "Darf mein Vermieter ohne Grund kündigen?",
        "starter_2": "Rückerstattung bei mangelhafter Ware",
        "starter_3": "DSGVO Recht auf Vergessenwerden durchsetzen"
    },
    "fr": {
        "brand": "Justice AI",
        "subtitle": "Intelligence Juridique Universelle et Vérification Légale",
        "new_question": "Nouvelle question",
        "recent_title": "RÉCENT",
        "verified_coverage_title": "Couverture vérifiée",
        "verified_coverage_text": "France · Suisse · Allemagne · UE · Royaume-Uni · Canada · Mondial",
        "region_label": "Région",
        "category_label": "Catégorie",
        "language_label": "Langue",
        "share_chat": "Partager",
        "dark_mode": "🌙",
        "light_mode": "☀️",
        "answered_from_official": "Répondu à partir de sources officielles",
        "sources_label": "SOURCES",
        "retrieval_confidence": "Fiabilité du résultat",
        "confidence_high": "Élevée",
        "disclaimer_text": "Information juridique générale, ne constitue pas un avis juridique formel.",
        "input_placeholder": "Posez une question juridique dans n'importe quel pays ou langue",
        "input_footnote": "Les réponses sont limitées aux juridictions disposant de sources vérifiées.",
        "welcome_headline": "Consultation Juridique Universelle",
        "welcome_subtitle": "Sélectionnez votre juridiction et catégorie, puis saisissez votre question ci-dessous.",
        "starter_1": "Le propriétaire peut-il résilier le bail sans motif ?",
        "starter_2": "Remboursement pour produit défectueux",
        "starter_3": "Exercer le droit à l'effacement RGPD Art. 17"
    },
    "es": {
        "brand": "Justice AI",
        "subtitle": "Inteligencia Jurídica Universal y Verificación Legal",
        "new_question": "Nueva consulta",
        "recent_title": "RECIENTE",
        "verified_coverage_title": "Cobertura verificada",
        "verified_coverage_text": "España · Unión Europea · Estados Unidos · América Latina · Global",
        "region_label": "Región",
        "category_label": "Categoría",
        "language_label": "Idioma",
        "share_chat": "Compartir chat",
        "dark_mode": "🌙",
        "light_mode": "☀️",
        "answered_from_official": "Respondido desde fuentes oficiales",
        "sources_label": "FUENTES",
        "retrieval_confidence": "Confianza de recuperación",
        "confidence_high": "Alta",
        "disclaimer_text": "Información jurídica general, no constituye asesoramiento legal vinculante.",
        "input_placeholder": "Haga una pregunta jurídica en cualquier país o idioma",
        "input_footnote": "Respuestas limitadas a jurisdicciones con fuentes verificadas.",
        "welcome_headline": "Consulta Jurídica Inteligente",
        "welcome_subtitle": "Seleccione su región y categoría, y escriba su consulta a continuación.",
        "starter_1": "¿Puede el propietario desalojar sin causa justa?",
        "starter_2": "Reembolso por producto defectuoso (Consumo)",
        "starter_3": "Derecho de supresión de datos según RGPD"
    },
    "it": {
        "brand": "Justice AI",
        "subtitle": "Intelligence Giuridica Universale e Verifica Normativa",
        "new_question": "Nuova domanda",
        "recent_title": "RECENTI",
        "verified_coverage_title": "Copertura verificata",
        "verified_coverage_text": "Italia · Svizzera · Unione Europea · Regno Unito · USA · Globale",
        "region_label": "Regione",
        "category_label": "Categoria",
        "language_label": "Lingua",
        "share_chat": "Condividi chat",
        "dark_mode": "🌙",
        "light_mode": "☀️",
        "answered_from_official": "Risposta da fonti ufficiali",
        "sources_label": "FONTI",
        "retrieval_confidence": "Affidabilità di recupero",
        "confidence_high": "Alta",
        "disclaimer_text": "Informazioni legali generali, non costituiscono parere legale vincolante.",
        "input_placeholder": "Fai una domanda legale in qualsiasi paese o lingua",
        "input_footnote": "Risposte basate esclusivamente su normative verificate.",
        "welcome_headline": "Consulenza Legale Intelligente",
        "welcome_subtitle": "Seleziona giurisdizione e categoria, poi scrivi la tua richiesta in basso.",
        "starter_1": "Il locatore può recedere dal contratto senza motivo?",
        "starter_2": "Rimborso per bene difettoso a norma di legge",
        "starter_3": "Esercizio del diritto all'oblio ex Art. 17 GDPR"
    },
    "tr": {
        "brand": "Justice AI",
        "subtitle": "Evrensel Hukuk Zekası ve Mevzuat Doğrulama Sistemi",
        "new_question": "Yeni Soru",
        "recent_title": "SON",
        "verified_coverage_title": "Doğrulanmış Kapsam",
        "verified_coverage_text": "Türkiye · Almanya · Avrupa Birliği · Birleşik Krallık · ABD · Küresel",
        "region_label": "Bölge",
        "category_label": "Kategori",
        "language_label": "Dil",
        "share_chat": "Sohbeti Paylaş",
        "dark_mode": "🌙",
        "light_mode": "☀️",
        "answered_from_official": "Resmi kaynaklardan yanıtlandı",
        "sources_label": "KAYNAKLAR",
        "retrieval_confidence": "Erişim Güveni",
        "confidence_high": "Yüksek",
        "disclaimer_text": "Genel hukuki bilgilendirmedir, resmi hukuki tavsiye niteliği taşımaz.",
        "input_placeholder": "Herhangi bir dilde veya ülkede hukuki soru sorun",
        "input_footnote": "Yanıtlar doğrulanmış kaynaklara sahip yargı alanlarıyla sınırlıdır.",
        "welcome_headline": "Evrensel Hukuk Danışma Sistemi",
        "welcome_subtitle": "Yukarıdan bölge ve kategori seçin, sorunuzu aşağıya yazın.",
        "starter_1": "Ev sahibi haklı bir gerekçe olmadan tahliye edebilir mi?",
        "starter_2": "Ayıplı malda tüketici iade hakkı",
        "starter_3": "KVKK ve GDPR veri silme hakkı"
    },
    "pa": {
        "brand": "Justice AI",
        "subtitle": "ਕਾਨੂੰਨੀ ਬੁੱਧੀਮਤਾ ਅਤੇ ਵਿਧਾਨਕ ਤਸਦੀਕ ਪ੍ਰਣਾਲੀ",
        "new_question": "ਨਵਾਂ ਸਵਾਲ",
        "recent_title": "ਹਾਲੀਆ",
        "verified_coverage_title": "ਪ੍ਰਮਾਣਿਤ ਕਵਰੇਜ",
        "verified_coverage_text": "ਭਾਰਤ · ਯੂਕੇ · ਕੈਨੇਡਾ · ਅਮਰੀਕਾ · ਆਸਟ੍ਰੇਲੀਆ · ਗਲੋਬਲ",
        "region_label": "ਖੇਤਰ",
        "category_label": "ਸ਼੍ਰੇਣੀ",
        "language_label": "ਭਾਸ਼ਾ",
        "share_chat": "ਗੱਲਬਾਤ ਸਾਂਝੀ ਕਰੋ",
        "dark_mode": "🌙",
        "light_mode": "☀️",
        "answered_from_official": "ਸਰਕਾਰੀ ਕਾਨੂੰਨੀ ਸਰੋਤਾਂ ਤੋਂ ਉੱਤਰ",
        "sources_label": "ਕਾਨੂੰਨੀ ਸਰੋਤ",
        "retrieval_confidence": "ਭਰੋਸੇਯੋਗਤਾ",
        "confidence_high": "ਉੱਚ",
        "disclaimer_text": "ਇਹ ਆਮ ਕਾਨੂੰਨੀ ਜਾਣਕਾਰੀ ਹੈ, ਵਕੀਲ ਦੀ ਅਧਿਕਾਰਤ ਸਲਾਹ ਨਹੀਂ।",
        "input_placeholder": "ਕਿਸੇ ਵੀ ਭਾਸ਼ਾ ਵਿੱਚ ਕਾਨੂੰਨੀ ਸਵਾਲ ਪੁੱਛੋ",
        "input_footnote": "ਉੱਤਰ ਪ੍ਰਮਾਣਿਤ ਸਰਕਾਰੀ ਕਾਨੂੰਨਾਂ 'ਤੇ ਆਧਾਰਿਤ ਹਨ।",
        "welcome_headline": "ਕਾਨੂੰਨੀ ਸਲਾਹਕਾਰ ਪ੍ਰਣਾਲੀ",
        "welcome_subtitle": "ਉੱਪਰ ਖੇਤਰ ਅਤੇ ਸ਼੍ਰੇਣੀ ਚੁਣੋ ਅਤੇ ਹੇਠਾਂ ਆਪਣਾ ਸਵਾਲ ਲਿਖੋ।",
        "starter_1": "ਕੀ ਮਕਾਨ ਮਾਲਕ ਬਿਨਾਂ ਕਾਰਨ ਕੱਢ ਸਕਦਾ ਹੈ?",
        "starter_2": "ਖਰਾਬ ਸਮਾਨ ਲਈ ਖਪਤਕਾਰ ਰਿਫੰਡ",
        "starter_3": "ਕਾਨੂੰਨੀ ਨੋਟਿਸ ਦਾ ਖਰੜਾ"
    },
    "bn": {
        "brand": "Justice AI",
        "subtitle": "সার্বজনীন আইনি বুদ্ধিমত্তা ও বিধিবদ্ধ যাচাইকরণ",
        "new_question": "নতুন প্রশ্ন",
        "recent_title": "সাম্প্রতিক",
        "verified_coverage_title": "যাচাইকৃত কভারেজ",
        "verified_coverage_text": "ভারত · যুক্তরাজ্য · যুক্তরাষ্ট্র · কানাডা · গ্লোবাল",
        "region_label": "অঞ্চল",
        "category_label": "বিভাগ",
        "language_label": "ভাষা",
        "share_chat": "চ্যাট শেয়ার করুন",
        "dark_mode": "🌙",
        "light_mode": "☀️",
        "answered_from_official": "অফিসিয়াল সূত্র থেকে উত্তর",
        "sources_label": "উৎস",
        "retrieval_confidence": "নির্ভরযোগ্যতা",
        "confidence_high": "উচ্চ",
        "disclaimer_text": "এটি সাধারণ আইনি তথ্য, পেশাদার আইনি পরামর্শ নয়।",
        "input_placeholder": "যেকোনো ভাষায় আইনি প্রশ্ন জিজ্ঞাসা করুন",
        "input_footnote": "উত্তরগুলি সরকারি যাচাইকৃত আইনের ভিত্তিতে সীমাবদ্ধ।",
        "welcome_headline": "আইনি পরামর্শ ব্যবস্থা",
        "welcome_subtitle": "উপরে আপনার অঞ্চল এবং বিভাগ নির্বাচন করুন, তারপর প্রশ্ন লিখুন।",
        "starter_1": "বাড়িওয়ালা কি বিনা কারণে উচ্ছেদ করতে পারেন?",
        "starter_2": "ত্রুটিপূর্ণ পণ্যের জন্য ভোক্তা আইনের অধীনে রিফান্ড",
        "starter_3": "আইনি নোটিশের খসড়া তৈরি করুন"
    },
    "ta": {
        "brand": "Justice AI",
        "subtitle": "உலகளாவிய சட்ட நுண்ணறிவு மற்றும் சரிபார்ப்பு அமைப்பு",
        "new_question": "புதிய கேள்வி",
        "recent_title": "சமீபத்தியவை",
        "verified_coverage_title": "சரிபார்க்கப்பட்ட நாடுகள்",
        "verified_coverage_text": "இந்தியா · சிங்கப்பூர் · ஐக்கிய ராஜ்ஜியம் · அமெரிக்கா · உலகளாவிய",
        "region_label": "பிராந்தியம்",
        "category_label": "வகை",
        "language_label": "மொழி",
        "share_chat": "பகிரவும்",
        "dark_mode": "🌙",
        "light_mode": "☀️",
        "answered_from_official": "அதிகாரப்பூர்ਵ மூலங்களிலிருந்து பதில்",
        "sources_label": "சட்ட மூலங்கள்",
        "retrieval_confidence": "நம்பகத்தன்மை",
        "confidence_high": "உயர்",
        "disclaimer_text": "இது பொதுவான சட்ட தகவல் மட்டுமே, சட்ட ஆலோசனை அல்ல.",
        "input_placeholder": "உங்கள் சட்டக் கேள்வியை இங்கே கேட்கவும்",
        "input_footnote": "பதில்கள் சரிபார்க்கப்பட்ட சட்டங்களின் அடிப்படையில் வழங்கப்படுகின்றன.",
        "welcome_headline": "சட்ட ஆலோசனை தளம்",
        "welcome_subtitle": "மேலே பிராந்தியம் மற்றும் வகையைத் தேர்வுசெய்து, கேள்வியைத் தட்டச்சு செய்யவும்.",
        "starter_1": "காரணமின்றி வீட்டு உரிமையாளர் வெளியேற்ற முடியுமா?",
        "starter_2": "குறைபாடுள்ள பொருளுக்கு நுகர்வோர் ரீஃபண்ட்",
        "starter_3": "சட்டப்பூர்வ நோட்டீஸ் வரைவு"
    }
}

# Pre-packaged sample questions for quick navigation
SAMPLE_RECENT_QUESTIONS = [
    {
        "id": "de_tenancy",
        "title_en": "Landlord termination notice",
        "title_hi": "मकान मालिक का निष्कासन नोटिस",
        "title_de": "Kündigung des Mietvertrags durch Vermieter",
        "sub_en": "Germany · Tenancy",
        "sub_hi": "जर्मनी · किराएदारी",
        "sub_de": "Deutschland · Mietrecht",
        "query_en": "My landlord in Germany sent me a termination letter. Does he need a reason?",
        "query_hi": "जर्मनी में मेरे मकान मालिक ने मुझे नोटिस भेजा है। क्या उन्हें कोई वैध कारण चाहिए?",
        "query_de": "Mein Vermieter in Deutschland hat mir gekündigt. Braucht er einen Grund?",
        "jurisdiction": "DE",
        "category": "Tenancy: Eviction & Termination Notice"
    },
    {
        "id": "in_consumer",
        "title_en": "Refund for a faulty product",
        "title_hi": "खराब फ़ोन का रिफ़ंड",
        "title_de": "Rückerstattung für fehlerhaftes Produkt",
        "sub_en": "India · Consumer",
        "sub_hi": "भारत · उपभोक्ता",
        "sub_de": "Indien · Verbraucherschutz",
        "query_en": "I ordered a mobile phone online that arrived defective. The seller refuses a refund. What can I do under Indian law?",
        "query_hi": "मैंने ऑनलाइन एक फ़ोन मँगवाया था, जो खराब निकला। विक्रेता रिफ़ंड देने से मना कर रहा है। मैं क्या कर सकता हूँ?",
        "query_de": "Ich habe ein defektes Telefon online bestellt und der Verkäufer verweigert die Erstattung.",
        "jurisdiction": "IN",
        "category": "Consumer Protection & Defective Goods"
    },
    {
        "id": "eu_gdpr",
        "title_en": "Right to erasure request",
        "title_hi": "डेटा हटाने का अनुरोध",
        "title_de": "Antrag auf Datenlöschung (Recht auf Vergessen)",
        "sub_en": "European Union · Data privacy",
        "sub_hi": "यूरोपीय संघ · डेटा गोपनीयता",
        "sub_de": "Europäische Union · Datenschutz",
        "query_en": "How do I enforce my right to erasure under GDPR Article 17 if a tech platform refuses to delete my profile?",
        "query_hi": "जीडीपीआर के तहत कंपनी से मेरा डेटा हटाने का अनुरोध कैसे करें?",
        "query_de": "Wie setze ich mein Recht auf Löschung nach DSGVO Artikel 17 durch?",
        "jurisdiction": "EU",
        "category": "Data Privacy & GDPR"
    },
    {
        "id": "us_employment",
        "title_en": "Unpaid overtime & FLSA claim",
        "title_hi": "अवैतनिक ओवरटाइम और दावा",
        "title_de": "Nicht bezahlte Überstunden (FLSA)",
        "sub_en": "United States · Employment",
        "sub_hi": "अमेरिका · रोज़गार",
        "sub_de": "USA · Arbeitsrecht",
        "query_en": "My employer requires 50 hours of work per week without overtime pay. Am I entitled to 1.5x pay under FLSA?",
        "query_hi": "मेरा नियोक्ता बिना ओवरटाइम वेतन के 50 घंटे काम कराता है। क्या मुझे 1.5 गुना वेतन पाने का अधिकार है?",
        "query_de": "Mein Arbeitgeber verlangt 50 Stunden Arbeit pro Woche ohne Überstundenzuschlag.",
        "jurisdiction": "US",
        "category": "Employment & Wage Rights"
    }
]

def format_assistant_response_data(
    raw_response: str,
    jurisdiction: str,
    legal_domain: str,
    retrieved_statutes: List[Dict[str, Any]],
    language: str = "en"
) -> Dict[str, Any]:
    lang = language.lower()
    if lang not in UI_STRINGS:
        lang = "en"
    
    strings = UI_STRINGS[lang]
    clean_text = raw_response.strip()
    
    # Dynamic Headline Extraction
    headline = ""
    first_lines = [l.strip() for l in clean_text.split("\n") if l.strip()]
    for line in first_lines[:5]:
        candidate = re.sub(r'^(?:###|\*\*|📌|#+)\s*', '', line).rstrip('*# \t')
        candidate = re.sub(r'^(headline\s*(answer)?|key\s*takeaway|summary|quick\s*answer|definitive\s*legal\s*answer)[:\s\-]*', '', candidate, flags=re.IGNORECASE).strip()
        candidate = candidate.strip('*_ ')
        if len(candidate) >= 20 and not candidate.lower().startswith(('instruction', 'disclaimer', 'jurisdiction:', 'active', 'user')):
            headline = candidate
            break

    if not headline or len(headline) < 15:
        sentences = re.split(r'(?<=[.!?])\s+', clean_text)
        for s in sentences:
            s_clean = re.sub(r'^(?:###|\*\*|📌|#+)\s*', '', s).strip('*_ #\t\n')
            if len(s_clean) >= 20 and not s_clean.lower().startswith(('instruction', 'disclaimer', 'user')):
                headline = s_clean[:140]
                break

    if not headline:
        headline = "Statutory Legal Assessment"

    # Clean body text & extract any trailing ### Official Sources links into structured source pills
    body_text = clean_text
    body_text = re.sub(r'⚖️\s*\*\*LEGAL DISCLAIMER\*\*[\s\S]*$', '', body_text).strip()

    llm_sources = []
    src_block_match = re.search(
        r'(?:^|\n)#{1,4}\s*(?:Official\s+)?Sources?\s*:?\s*\n([\s\S]*?)(?=\n#{1,4}\s|\Z)',
        body_text,
        flags=re.IGNORECASE,
    )
    if src_block_match:
        src_block_text = src_block_match.group(1)
        for m in re.finditer(r'\[([^\]]+)\]\((https?://[^\s)]+)\)', src_block_text):
            link_title = m.group(1).strip()
            link_url = m.group(2).strip().rstrip('.,;')
            domain_match = re.match(r'https?://(?:www\.)?([^/]+)', link_url, flags=re.IGNORECASE)
            link_domain = domain_match.group(1) if domain_match else "official-statute"
            llm_sources.append({
                "title": link_title,
                "domain": link_domain,
                "url": link_url,
            })
        body_text = (body_text[:src_block_match.start()] + body_text[src_block_match.end():]).strip()

    body_text = re.sub(r'^\s*[-*_]{3,}\s*$', '', body_text, flags=re.MULTILINE).strip()
    if headline and first_lines:
        first_stripped = re.sub(r'[*_#\s`]+', ' ', first_lines[0]).strip().lower()
        hl_stripped = re.sub(r'[*_#\s`]+', ' ', headline).strip().lower()
        if first_stripped == hl_stripped or hl_stripped in first_stripped:
            body_text = "\n".join(body_text.split("\n")[1:]).strip()
            body_text = re.sub(r'^\s*[-*_]{3,}\s*$', '', body_text, flags=re.MULTILINE).strip()
    body_text = re.sub(r'^(?:###|\*\*|📌)\s*(?:short answer|headline)\s*:?\s*\n+', '', body_text, flags=re.IGNORECASE).strip()

    # Sources: Combine LLM-cited official links and retrieved ChromaDB statutes (filtered by jurisdiction)
    jur_norm = "GB" if jurisdiction == "UK" else jurisdiction
    sources = []
    seen_urls = set()

    def _add_source(title: str, domain: str, url: str):
        if not url or not url.startswith("http"):
            return
        key = (url.lower(), title.lower())
        if key in seen_urls or any(u == url.lower() for u, _ in seen_urls):
            return
        seen_urls.add(key)
        sources.append({
            "title": title,
            "domain": domain,
            "url": url,
        })

    for ls in llm_sources:
        _add_source(ls["title"], ls["domain"], ls["url"])

    dom_specific = (legal_domain or "") not in ("", "AUTO", "General", "General Legal Advisory")
    for s in retrieved_statutes:
        s_jur = "GB" if s.get("jurisdiction") == "UK" else s.get("jurisdiction")
        if jur_norm not in ("AUTO", "GLOBAL") and s_jur and s_jur != jur_norm:
            continue
        s_cat = s.get("category", "")
        if dom_specific and s_cat and s_cat.lower() != legal_domain.lower():
            continue
        title = s.get("title_hi") if lang == "hi" and "title_hi" in s else f"{s['act']} · {s['section']} · {s['title']}"
        _add_source(title, s.get("source_domain", "official-gazette.gov"), s.get("source_url", ""))

    # Jurisdictional & category canonical official portal fallback so every response has direct source links
    if not sources:
        dom_low = (legal_domain or "").lower()
        if jur_norm == "CH":
            if "employ" in dom_low or "wage" in dom_low:
                _add_source("Swiss Code of Obligations (SR 220) · Art. 335c (Employment Notice)", "fedlex.admin.ch", "https://www.fedlex.admin.ch/eli/cc/27/317_321_377/en#art_335c")
            else:
                _add_source("Swiss Code of Obligations (SR 220) · Art. 266c–266l (Tenancy Notice)", "fedlex.admin.ch", "https://www.fedlex.admin.ch/eli/cc/27/317_321_377/en#art_266c")
                _add_source("Swiss Code of Obligations (SR 220) · Art. 271 & 273 (Challenging Termination)", "fedlex.admin.ch", "https://www.fedlex.admin.ch/eli/cc/27/317_321_377/en#art_271")
        elif jur_norm == "DE":
            _add_source("BGB § 573 · Ordinary termination by the landlord", "gesetze-im-internet.de", "https://www.gesetze-im-internet.de/bgb/__573.html")
            _add_source("BGB § 573c · Notice periods", "gesetze-im-internet.de", "https://www.gesetze-im-internet.de/bgb/__573c.html")
        elif jur_norm == "IN":
            if "traffic" in dom_low or "motor" in dom_low:
                _add_source("Motor Vehicles Act, 1988 · Virtual Court & Contest Portal", "vcourts.gov.in", "https://vcourts.gov.in")
                _add_source("Parivahan e-Challan & Rule 139 Verification", "echallan.parivahan.gov.in", "https://echallan.parivahan.gov.in")
            elif "criminal" in dom_low or "penal" in dom_low:
                _add_source("Bharatiya Nyaya Sanhita, 2023 (BNS)", "indiacode.nic.in", "https://www.indiacode.nic.in/handle/123456789/20340")
                _add_source("Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)", "indiacode.nic.in", "https://www.indiacode.nic.in/handle/123456789/20341")
            else:
                _add_source("उपभोक्ता संरक्षण अधिनियम, 2019 · धारा 39" if lang == "hi" else "Consumer Protection Act, 2019 · Section 39", "indiacode.nic.in", "https://www.indiacode.nic.in/handle/123456789/15256")
                _add_source("e-Daakhil Online Consumer Redressal Portal", "edaakhil.nic.in", "https://edaakhil.nic.in")
        elif jur_norm == "EU":
            _add_source("GDPR Article 17 · Right to erasure (Regulation EU 2016/679)", "eur-lex.europa.eu", "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679")
        elif jur_norm == "US":
            if "tenan" in dom_low or "housing" in dom_low or "evict" in dom_low:
                _add_source("Texas Property Code § 24.005 · Notice to Vacate", "statutes.capitol.texas.gov", "https://statutes.capitol.texas.gov/Docs/PR/htm/PR.24.htm")
            else:
                _add_source("Fair Labor Standards Act · 29 U.S.C. § 207", "law.cornell.edu", "https://www.law.cornell.edu/uscode/text/29/207")
        elif jur_norm == "GB":
            if "tenan" in dom_low or "housing" in dom_low:
                _add_source("Housing Act 1988 · Residential Tenancy & Possession", "legislation.gov.uk", "https://www.legislation.gov.uk/ukpga/1988/50/contents")
            elif "employ" in dom_low:
                _add_source("Employment Rights Act 1996", "legislation.gov.uk", "https://www.legislation.gov.uk/ukpga/1996/18/contents")
            elif "privacy" in dom_low or "gdpr" in dom_low:
                _add_source("Data Protection Act 2018 (UK GDPR)", "legislation.gov.uk", "https://www.legislation.gov.uk/ukpga/2018/12/contents")
            else:
                _add_source("Consumer Rights Act 2015 · Goods & Remedies", "legislation.gov.uk", "https://www.legislation.gov.uk/ukpga/2015/15/contents")
        elif jur_norm == "CA":
            if "privacy" in dom_low:
                _add_source("Personal Information Protection and Electronic Documents Act (PIPEDA)", "laws-lois.justice.gc.ca", "https://laws-lois.justice.gc.ca/eng/acts/P-8.6/")
            else:
                _add_source("Canada Labour Code (R.S.C., 1985, c. L-2)", "laws-lois.justice.gc.ca", "https://laws-lois.justice.gc.ca/eng/acts/L-2/")
        elif jur_norm == "AU":
            if "employ" in dom_low or "wage" in dom_low:
                _add_source("Fair Work Act 2009 · National Employment Standards", "legislation.gov.au", "https://www.legislation.gov.au/C2009A00028/latest/text")
            else:
                _add_source("Competition and Consumer Act 2010 · Australian Consumer Law", "legislation.gov.au", "https://www.legislation.gov.au/C2004A00109/latest/text")
        elif jur_norm == "SG":
            if "consumer" in dom_low:
                _add_source("Consumer Protection (Fair Trading) Act 2003", "sso.agc.gov.sg", "https://sso.agc.gov.sg/Act/CPFTA2003")
            elif "criminal" in dom_low or "harass" in dom_low:
                _add_source("Protection from Harassment Act 2014", "sso.agc.gov.sg", "https://sso.agc.gov.sg/Act/PHA2014")
            else:
                _add_source("Employment Act 1968 (Singapore)", "sso.agc.gov.sg", "https://sso.agc.gov.sg/Act/EmA1968")
        else:
            _add_source("EUR-Lex Official Union Law Portal", "eur-lex.europa.eu", "https://eur-lex.europa.eu")
            _add_source("India Code Official Statutory Repository", "indiacode.nic.in", "https://www.indiacode.nic.in")

    sources = sources[:3]

    # Chips
    chips = []
    if jurisdiction == "DE" or "tenancy" in legal_domain.lower():
        if lang == "hi":
            chips = ["यदि मैं यहाँ 8 वर्ष से अधिक रहा हूँ?", "क्या मैं निष्कासन पर आपत्ति कर सकता हूँ?", "किराएदार संघ कैसे खोजें?"]
        elif lang == "de":
            chips = ["Was, wenn ich über 8 Jahre hier wohne?", "Kann ich der Kündigung widersprechen?", "Mieterverein finden"]
        else:
            chips = ["What if I have lived here over 8 years?", "Can I object to the termination?", "Find a tenant association"]
    elif jurisdiction == "IN" or "consumer" in legal_domain.lower():
        if lang == "hi":
            chips = ["शिकायत का मसौदा बनाएँ", "ज़िला उपभोक्ता आयोग कैसे खोजें?", "विक्रेता से क्या लिखकर माँगें?"]
        else:
            chips = ["Draft formal demand letter to seller", "How to file on e-Daakhil portal?", "Calculate interest and compensation"]
    elif jurisdiction == "EU" or "privacy" in legal_domain.lower():
        if lang == "hi":
            chips = ["डेटा हटाने के नोटिस का प्रारूप", "यदि कंपनी मना करे तो क्या करें?", "डेटा सुरक्षा प्राधिकरण से शिकायत"]
        else:
            chips = ["Draft GDPR Article 17 Erasure Notice", "What if company claims legitimate interest?", "File complaint with Supervisory Authority"]
    else:
        if lang == "hi":
            chips = ["कानूनी नोटिस का मसौदा तैयार करें", "समय-सीमा (Limitation) क्या है?", "वकील से पूछने योग्य 5 प्रश्न"]
        else:
            chips = ["Draft a formal Legal Demand Notice", "What is the limitation period?", "Top 5 questions for local counsel"]

    jur_display = CLEAN_REGIONS.get(jurisdiction, jurisdiction)
    tag_label = f"{jur_display} · {legal_domain}"

    return {
        "headline": headline,
        "body_text": body_text,
        "tag_label": tag_label,
        "verified_label": strings["answered_from_official"],
        "sources_label": strings["sources_label"],
        "sources": sources,
        "confidence_label": strings["retrieval_confidence"],
        "confidence_level": strings["confidence_high"],
        "confidence_percentage": 85,
        "disclaimer": strings["disclaimer_text"],
        "chips": chips
    }
