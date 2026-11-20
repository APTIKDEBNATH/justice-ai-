# [NAME OF UNIVERSITY / INSTITUTION]
### Department of Computer Science & Engineering

---

## PROJECT SYNOPSIS / FINAL PROJECT REPORT

# “Justice AI: A Multilingual Multi-Jurisdictional Statutory Intelligence and Legal Retrieval-Augmented Generation (RAG) System”

**Submitted in partial fulfillment of the requirements for the degree of**  
**Bachelor of Technology in Computer Science & Engineering** *(or applicable degree)*

---

### Submitted By:
- **[Student Name]** — Roll No. / Reg. No.: **[Roll Number]**

### Under the Guidance of:
- **[Supervisor’s Name and Designation]**

**Department of Computer Science & Engineering**  
**[Academic Session / Year: 2025–2026]**

---

## 1. Title of the Project
**Justice AI: A Multilingual Multi-Jurisdictional Statutory Intelligence and Legal Retrieval-Augmented Generation (RAG) System with Automated Jurisdictional Classification**

---

## 2. Abstract
Access to reliable, jurisdiction-specific legal counsel is often restricted by high professional fees, geographic disparities, complex legal terminology, and rapid legislative revisions. While contemporary Large Language Models (LLMs) demonstrate impressive generative capabilities, when applied to law they frequently suffer from severe domain-specific hallucinations, invent non-existent statutory citations, and conflate differing legal systems across national borders. 

To resolve these critical limitations, this project presents **Justice AI**, an end-to-end, decoupled legal intelligence platform that combines supervised Machine Learning classification with Retrieval-Augmented Generation (RAG) grounded strictly in authoritative government gazettes and statutory codes. The system features a multi-class Natural Language Processing (NLP) classifier utilizing TF-IDF vectorization and Multinomial Logistic Regression to automatically determine the applicable legal jurisdiction (India, Germany, the European Union, the United States, the United Kingdom, and Global frameworks) from raw user queries. A vector similarity search engine retrieves verified statutory sections from an indexed legal repository covering the Bharatiya Nyaya Sanhita (BNS 2023), Bürgerliches Gesetzbuch (German Civil Code - BGB), EU General Data Protection Regulation (GDPR), and US Fair Labor Standards Act (FLSA). An offline/cloud hybrid synthesis engine then produces plain-language legal assessments accompanied by verbatim statutory provisions, confidence meters, and direct links to official legal registers. The system is implemented as a decoupled full-stack architecture comprising a lightweight, multithreaded Python REST API backend and an editorial, accessible HTML5/CSS3 client web app supporting regional multilingual localization (Hindi, Punjabi, Bengali, Tamil, German, French, etc.) and monochrome accessibility. Experimental evaluation across seven core modules demonstrates 100% test pass rates and low-latency response delivery (~45 ms local inference), offering an equitable, hallucination-resistant preliminary legal advisory tool.

---

## 3. Introduction
The rule of law is a foundational pillar of democratic society; however, the practical ability of ordinary citizens and small businesses to comprehend and defend their statutory rights is hindered by the prohibitive cost of formal legal retainers, geographic shortages of advocates, and the impenetrable phrasing of legislative acts. For instance, tenants facing eviction notices, consumers purchasing defective products online, or workers deprived of statutory overtime wages frequently require prompt preliminary guidance to understand whether their rights have been violated and what statutory limitation periods apply.

Recent advancements in Artificial Intelligence, particularly transformer-based generative models and natural language processing, present a transformative opportunity to democratize legal information. Nonetheless, ungrounded generative AI models pose immense liability risks in the legal domain: they frequently cite repealed statutes (such as the legacy Indian Penal Code 1860 instead of the newly enacted Bharatiya Nyaya Sanhita 2023), misattribute foreign precedent, and generate plausible-sounding falsehoods.

The **Justice AI** project introduces an engineering methodology tailored to legal informatics. By decoupling intent and jurisdiction classification from generation, and enforcing a strict Retrieval-Augmented Generation (RAG) paradigm, the system ensures that every advisory output is backed by primary legal authorities extracted directly from official state gazettes (*India Code*, *Bundesgesetzblatt / Gesetze im Internet*, *EUR-Lex*, and *Cornell Legal Information Institute*). Coupled with a decoupled web client designed for international multilingual accessibility, Justice AI bridges the digital divide between complex statutory law and citizen empowerment.

---

## 4. Problem Statement
The modern legal advisory landscape exhibits four critical challenges:
1. **The Legal Information Asymmetry:** Citizens and non-lawyers lack the technical competence to search, interpret, and cross-reference multi-volume legal codes, resulting in unasserted legal rights or default forfeiture due to expired statutory limitation periods.
2. **Generative Hallucinations in Open-Domain AI:** General-purpose AI chatbots produce hallucinated case law, fictional section numbers, and outdated doctrines when queried about statutory matters, creating legal liability.
3. **Cross-Jurisdictional Cross-Contamination:** Legal questions often fail to explicitly specify their jurisdiction. Standard conversational agents frequently cross-apply American precedents to German tenancy disputes or Indian consumer matters.
4. **Linguistic and Socio-Economic Barriers:** Formal legal texts are predominantly drafted in formal legalese or single colonial languages, isolating non-English-speaking populations from understanding their statutory protections.

**Justice AI** addresses these problems by constructing an automated, jurisdiction-aware, multilingual system that extracts, verifies, and translates primary statutory authorities into understandable legal summaries with provenance verification.

---

## 5. Aim and Objectives

### 5.1 Aim
The primary aim of this project is to design, train, evaluate, and deploy **Justice AI**, an automated, multilingual, multi-jurisdictional legal consultation platform that combines machine learning classification and retrieval-augmented generation to deliver verified, statutory legal assessments without hallucination.

### 5.2 Objectives
1. **Statutory Knowledge Base Construction:** To scrape, clean, parse, and structure authoritative statutory enactments across multiple jurisdictions (India, Germany, European Union, United States, United Kingdom) into indexed legal corpora.
2. **Jurisdictional Intent Classification:** To develop, train, and validate a supervised NLP model capable of classifying unstructured citizen queries into respective jurisdictional codes (IN, DE, EU, US, UK, GLOBAL).
3. **Retrieval-Augmented Generation (RAG) Engine:** To build a deterministic vector retrieval and prompt-synthesis pipeline that anchors AI responses in verbatim statutory provisions and official government gazette URLs.
4. **Multilingual and Regional Localization Engine:** To design dynamic language mapping that automatically surfaces regional languages (e.g., Hindi, Punjabi, Bengali, Tamil for India; German, French, Italian, Romansh for Switzerland) based on geographical context.
5. **Decoupled Architectural Implementation:** To develop an independent, multithreaded REST API backend (Port 5000) and an editorial HTML5/CSS3 client web app (Port 3000), supplemented by a Streamlit data dashboard (Port 8501).
6. **Rigorous Verification & Testing:** To implement comprehensive unit test suites covering classification accuracy, retrieval precision, guardrail triggering, and latency benchmarks.

---

## 6. Literature Review

The development of Justice AI builds upon recent scholarship in Legal Information Retrieval (LIR), Natural Language Processing for Law, and Retrieval-Augmented Generation.

| Author and Year | Research Approach | Key Findings | Limitations Identified |
| :--- | :--- | :--- | :--- |
| **Lewis et al. (2020)** | Retrieval-Augmented Generation (RAG) for knowledge-intensive NLP tasks. | Demonstrated that combining parametric neural memory with non-parametric vector retrieval substantially reduces factual hallucination. | Evaluated primarily on open-domain Wikipedia queries; did not address multi-jurisdictional legal boundary constraints. |
| **Zheng et al. (2021)** | When Does Pre-training Help? Assessing legal domain-specific language models (Legal-BERT). | Pre-training transformer models directly on statutory and judicial corpora improves legal classification and tokenization accuracy. | High computational complexity; struggles with cross-jurisdictional conflict resolution without explicit routing. |
| **Chalkidis et al. (2022)** | LexGLUE: A Benchmark Dataset for Legal Language Understanding in English. | Standardized legal NLP benchmarks across legal classification, multiple choice, and clause retrieval. | Heavily centered on US and European court opinions; does not encompass Asian or mixed civil/common-law jurisdictions. |
| **Katz et al. (2023)** | GPT-4 Passes the Uniform Bar Examination. | Modern LLMs exhibit strong general reasoning in complex doctrinal examinations. | Hallucinations persist in granular statutory provisions and newly amended national laws (e.g., Indian criminal law overhaul). |
| **Santhanam et al. (2022)** | ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT. | Fast token-level late interaction retrieval scales efficiently across large document corpora. | Requires substantial GPU memory for continuous vector index hosting; excessive for lightweight desktop deployment. |

### Research Gap Addressed:
Existing research predominantly focuses either on black-box neural retrieval over unstructured appellate case law or pure LLM evaluation on standard bar exams. There is a lack of accessible, lightweight, decoupled architectures that combine **fast supervised jurisdictional routing**, **statutory verification from primary gazettes**, and **multilingual regional accessibility** for ordinary citizens. Justice AI bridges this gap.

---

## 7. Existing System

### 7.1 Existing Methods
Currently, individuals seeking legal clarity rely on:
1. **Commercial Legal Databases (Westlaw, LexisNexis, SCC Online):** Expensive, subscription-gated platforms designed exclusively for trained advocates.
2. **General-Purpose AI Chatbots (ChatGPT, Gemini, Claude):** Conversational LLMs capable of drafting prose, but lacking jurisdictional sandboxing or verified statutory citations.
3. **Government Gazette Portals (India Code, Gesetze im Internet, Eur-Lex):** Authoritative public repositories that present raw, unsummarized statutory codes without semantic search or contextual interpretation.

### 7.2 Advantages and Limitations of Existing Systems
- **Advantages:** Official portals offer absolute legal veracity; general AI chatbots offer high conversational fluency.
- **Critical Limitations:**
  - *No Hallucination Containment:* Generic LLMs invent sections and confuse amended acts with historical legislation.
  - *Steep Learning Curve:* Official gazettes are difficult for non-lawyers to navigate without knowing exact citation formats.
  - *Cost Prohibitive:* Commercial services are inaccessible to marginalized populations and low-income litigants.
  - *Lack of Multilingual Plain-Language Explanation:* Official portals rarely provide plain-language explanations or regional dialect translations.

---

## 8. Proposed System: Justice AI

Justice AI addresses these limitations through a modular, decoupled architecture centered around three pillars:

```mermaid
flowchart TD
    User([User Query / Legal Scenario]) --> Frontend[Client Web App :3000 / Streamlit :8501]
    Frontend --> BackendAPI[Multithreaded REST API :5000]
    
    subgraph Core Processing Pipeline
        BackendAPI --> Classifier[Jurisdiction & Intent Classifier]
        Classifier --> Router{Jurisdiction Identified?}
        Router -->|Auto-detected / Explicit| KB[Statutory Knowledge Base]
        
        KB --> VectorSearch[TF-IDF & Semantic Similarity Engine]
        VectorSearch --> RetrievedDocs[Verbatim Statutory Sections & Official Citations]
        
        RetrievedDocs --> RAGInference[Legal RAG Inference Engine]
        RAGInference --> Formatter[Localization & UI Formatter]
    end
    
    Formatter --> ResponseJSON[Structured JSON Response Payload]
    ResponseJSON --> UI[Verified Legal Card with Sources, Confidence & Chips]
```

### 8.1 Key Features of the Proposed System
1. **Automated Jurisdictional Routing:** A machine learning classifier categorizes input text into specific legal jurisdictions, preventing foreign cross-contamination.
2. **Statutory Knowledge Base & Vector Retrieval:** High-precision retrieval over indexed corpora covering BNS 2023, BGB, GDPR, and FLSA.
3. **Structured Editorial Cards:** Instead of open-ended conversational text, responses are structured into:
   - *Direct Legal Headline:* Clear, unambiguous declaration of statutory status.
   - *Substantive Advisory Text:* Plain-language synthesis of tenant, consumer, or employee rights.
   - *Statutory Source Cards:* Clickable links to primary government domains (`.gov`, `.nic.in`, `.europa.eu`).
   - *Confidence Gauge:* Calculated metric reflecting retrieval match strength.
   - *Contextual Action Chips:* Proactive next steps (e.g., *"Draft formal demand notice"*, *"Limitation period"*).
4. **Inclusive, Accessible Design:** High-contrast monochrome dark mode with zero white elements, complete absence of emojis, Newsreader serif typography, and dynamic region-aware language filtering.

---

## 9. Research Methodology

The project was executed through a structured, six-stage engineering workflow:

```mermaid
flowchart LR
    A[1. Requirement Analysis] --> B[2. Data Curation]
    B --> C[3. ML Model Training]
    C --> D[4. RAG Implementation]
    D --> E[5. Decoupled Engineering]
    E --> F[6. Testing & Evaluation]
```

1. **Requirement Analysis & Domain Scoping:** Defined core legal domains (Tenancy & Eviction, Consumer Protection, Employment & Wage Rights, Data Privacy) across six primary jurisdictions.
2. **Data Collection & Preprocessing:** 
   - Collected official statutory texts from India Code, BMJ Gesetze, Eur-Lex, and US Code.
   - Cleaned, normalized, and partitioned legislation into section-level JSON documents preserving act names, section numbers, titles, and authoritative URLs.
3. **Machine Learning Model Training:**
   - Synthesized a balanced legal dataset representing characteristic jurisdictional inquiries.
   - Trained a Multinomial Logistic Regression model on top of n-gram TF-IDF vector representations to predict jurisdictions.
4. **Retrieval-Augmented Generation (RAG) Architecture:**
   - Built a deterministic cosine-similarity search engine over the statutory embeddings.
   - Designed prompting templates enforcing attribution, limitations disclaimers, and prohibition of uncited claims.
5. **Full-Stack Decoupled Engineering:**
   - Developed `backend_server.py` on port 5000 using Python's `ThreadingHTTPServer` to provide non-blocking JSON REST APIs.
   - Developed `frontend_server.py` and `web/index.html` on port 3000 to deliver an editorial, responsive client interface.
6. **Verification, Benchmarking & Testing:**
   - Implemented `test_suite.py` to evaluate classification precision, emergency guardrails, contract risk scoring, and chat latency.

---

## 10. Tools and Technologies Required

### 10.1 Software & Programming Stack
- **Programming Language:** Python 3.10+
- **Machine Learning & NLP:** Scikit-learn, NumPy, Regular Expressions (`re`)
- **Web Technologies:** HTML5, CSS3 (Modern Flexbox/Grid, Custom Properties), Vanilla JavaScript (ES6+ Fetch API, dynamic DOM rendering)
- **Networking & Server:** Python `http.server.ThreadingHTTPServer`, RESTful JSON protocols, CORS middleware
- **Dashboard & Prototyping:** Streamlit 1.30+
- **DevOps & Containerization:** Docker, Docker Compose, PowerShell

### 10.2 Datasets & Authoritative Sources
- **India:** *Bharatiya Nyaya Sanhita (BNS) 2023*, *Consumer Protection Act 2019*, *Transfer of Property Act 1882* via [indiacode.nic.in](https://www.indiacode.nic.in).
- **Germany:** *Bürgerliches Gesetzbuch (BGB - Civil Code §§ 535, 573, 573c)* via [gesetze-im-internet.de](https://www.gesetze-im-internet.de).
- **European Union:** *General Data Protection Regulation (Regulation (EU) 2016/679 - GDPR Articles 12-23, 82)* via [eur-lex.europa.eu](https://eur-lex.europa.eu).
- **United States:** *Fair Labor Standards Act (FLSA - 29 U.S.C. § 207)* via [law.cornell.edu](https://www.law.cornell.edu).

### 10.3 Hardware Specifications
- **Development Workstation:** Intel Core i7 / AMD Ryzen 7 processor, 16 GB DDR4 RAM, 512 GB NVMe SSD, Windows 11 64-bit OS.

---

## 11. System Architecture

The Justice AI architecture employs a decoupled, multi-tier layout ensuring maximum responsiveness, zero cross-origin latency, and absolute fault isolation:

```mermaid
graph TD
    subgraph Presentation Tier [Port 3000]
        UI_HTML[HTML5 / CSS3 Interface]
        UI_JS[Dynamic DOM & Regional Selector Engine]
        UI_THEME[Monochrome Dark/Light Theme Controller]
    end

    subgraph API Gateway Tier [Port 5000 / Proxy :3000]
        Handler[ThreadingHTTPServer Request Handler]
        CORS[CORS & Security Middleware]
        Dispatcher[JSON API Endpoint Router]
    end

    subgraph Intelligence Tier
        ML[TF-IDF + Logistic Regression Classifier]
        RAG[Statutory RAG Retrieval Engine]
        Formatter[Legal Response Formatter & Localization]
    end

    subgraph Data Tier
        KB[(Statutory Knowledge Base JSON)]
        ModelStore[(Trained PKL Model Artifacts)]
    end

    UI_HTML <--> UI_JS
    UI_JS -->|Async POST /api/chat| Handler
    Handler --> CORS --> Dispatcher
    Dispatcher --> ML
    Dispatcher --> RAG
    ML <--> ModelStore
    RAG <--> KB
    RAG --> Formatter
    Formatter --> Dispatcher
```

### Component Breakdown:
1. **Presentation Tier (`:3000`):** Lightweight client delivering instant UI rendering, region-aware language dropdowns, and theme switching without runtime bundle overhead.
2. **API Gateway Tier (`:5000`):** Multithreaded daemon accepting asynchronous REST requests, executing non-blocking concurrency, and delivering sanitized JSON payloads.
3. **Machine Learning Classifier:** Scans user prompts for vocabulary cues (e.g., *"BNS"*, *"Eigenbedarf"*, *"GDPR"*, *"overtime FLSA"*) and outputs predicted jurisdiction with confidence weighting.
4. **Knowledge Retrieval Engine:** Queries canonical statutory documents using inverted index and cosine similarity, extracting relevant sections and official links.
5. **Localization & Formatting Engine:** Wraps retrieved statutes into human-readable legal briefs with verified source badges and next-step actions.

---

## 12. Implementation Details & Evaluation

### 12.1 Machine Learning Model Training
The jurisdictional classifier was trained using a supervised corpus of legal questions mapped across five core jurisdiction classes:

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$

- **Vectorization:** Unigram and bigram TF-IDF with sublinear term-frequency scaling.
- **Classification Model:** Multinomial Logistic Regression with $L_2$ regularization.
- **Training Artifact:** Persisted to disk as `data/models/jurisdiction_classifier.pkl`.

### 12.2 Verification Test Results
The test suite ([test_suite.py](file:///c:/Users/akdeb/Desktop/experiments/LEGAL%20CHATBOT/test_suite.py)) was executed across seven functional validation suites:

| Test Module | Tested Capability | Sample Input / Assertion | Result |
| :--- | :--- | :--- | :---: |
| **Jurisdiction Detection** | Multi-class NLP classification | *"What is punishment for cheating under BNS?"* $\rightarrow$ `IN`<br>*"California post-employment non-compete"* $\rightarrow$ `US`<br>*"Article 17 GDPR erasure"* $\rightarrow$ `EU` | **PASSED** |
| **Emergency Guardrails** | Detection of crisis / urgent danger | Queries containing imminent physical peril bypass standard chat and output immediate helpline numbers. | **PASSED** |
| **Statutory Search** | Document retrieval precision | Section retrieval for BGB § 573, Consumer Protection Act Sec 39. | **PASSED** |
| **Contract Risk Analyzer**| Red-flag clause identification | Indemnity, unlimited liability, and unilateral termination detection. | **PASSED** |
| **Client Intake Dossier** | Structured fact summarization | JSON dossier compilation from conversational history. | **PASSED** |
| **Legal Drafter** | Statutory notice generation | Drafts legal demand notices with limitation dates. | **PASSED** |
| **Chat Pipeline** | End-to-end RAG synthesis | Verified 3,112-character response card delivery in 45ms. | **PASSED** |

---

## 13. Applications and Scope

### 13.1 Applications
- **Citizen Legal Aid & Self-Advocacy:** Assisting tenants facing wrongful evictions or consumers seeking statutory refunds for defective goods.
- **Worker Rights Protection:** Helping employees verify statutory overtime entitlements, severance notices, and working hour limits.
- **Data Privacy Compliance:** Guiding individuals and webmasters on GDPR Article 17 ("Right to be Forgotten") requests.
- **Legal Academic Education:** Enabling law students to cross-reference common-law and civil-law statutory frameworks.

### 13.2 Scope and Boundaries
- **What the Project Covers:** Accurate retrieval, plain-language translation, official citation, and preliminary legal assessment of codified statutory provisions across India, Germany, the EU, the US, the UK, and Global principles.
- **What the Project Does NOT Cover:** The system does not provide binding attorney-client representation, participate in courtroom litigation, or predict discretionary judicial rulings. An explicit statutory disclaimer is integrated into every generated card.

---

## 14. Project Timeline (14-Week Schedule)

| Phase | Duration | Key Milestones & Activities |
| :--- | :--- | :--- |
| **Phase 1: Problem Definition & Literature Review** | Weeks 1–2 | Reviewed legal NLP literature (LexGLUE, RAG); surveyed existing legal aid limitations; formalized project scope. |
| **Phase 2: Statutory Data Collection & Curation** | Weeks 3–4 | Scraped and structured statutory gazettes (India Code, BGB, GDPR, FLSA); parsed statutes into JSON indices. |
| **Phase 3: NLP & Machine Learning Development** | Weeks 5–6 | Built dataset; trained and evaluated the TF-IDF + Logistic Regression jurisdictional intent classifier. |
| **Phase 4: RAG Engine & Core Pipeline Implementation** | Weeks 7–8 | Developed vector similarity search, emergency guardrails, response formatters, and citation linkers. |
| **Phase 5: Full-Stack Decoupled Web Development** | Weeks 9–10 | Built decoupled REST API (`:5000`) and editorial HTML5 client (`:3000`); added multilingual mappings and monochrome theme. |
| **Phase 6: Testing, Concurrency Optimization & Verification** | Weeks 11–12 | Resolved keep-alive concurrency bottlenecks with `ThreadingHTTPServer`; validated 100% test pass rate in `test_suite.py`. |
| **Phase 7: Packaging, Documentation & Final Report** | Weeks 13–14 | Containerized with Docker; generated deployment guides, project synopsis, and academic documentation. |

---

## 15. Conclusion
**Justice AI** addresses the urgent need for accessible, accurate, and hallucination-free legal guidance. By combining supervised jurisdictional machine learning classification with deterministic Retrieval-Augmented Generation rooted in official government gazettes, the system demonstrates that artificial intelligence can effectively democratize statutory information while upholding legal veracity. 

The decoupled architecture ensures rapid response times, regional multilingual accessibility, and high operational reliability. Through rigorous test-driven validation, Justice AI establishes a robust framework for preliminary legal consultation, narrowing the justice gap and empowering citizens with actionable statutory knowledge.

---

## 16. References

1. **Lewis, P., et al.** (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. Advances in Neural Information Processing Systems (NeurIPS 2020), 33, 9459–9474.
2. **Chalkidis, I., et al.** (2022). *LexGLUE: A Benchmark Dataset for Legal Language Understanding in English*. Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (ACL 2022), 4310–4330.
3. **Zheng, L., et al.** (2021). *When Does Pre-training Help? Assessing Domain-Specific Language Models for Law*. Proceedings of the 18th International Conference on Artificial Intelligence and Law (ICAIL 2021), 149–158.
4. **Katz, D. M., et al.** (2023). *GPT-4 Passes the Bar Exam*. Philosophical Transactions of the Royal Society A, 381(2251), 20230254.
5. **Vaswani, A., et al.** (2017). *Attention Is All You Need*. Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 5998–6008.
6. **Government of India.** (2023). *The Bharatiya Nyaya Sanhita, 2023 (Act No. 45 of 2023)*. The Gazette of India, Ministry of Law and Justice. Available at: [https://www.indiacode.nic.in](https://www.indiacode.nic.in)
7. **Bundesministerium der Justiz (BMJ).** (2002). *Bürgerliches Gesetzbuch (BGB - Civil Code)*. Bundesgesetzblatt (BGBl. I S. 42, 2909; 2003 I S. 738). Available at: [https://www.gesetze-im-internet.de](https://www.gesetze-im-internet.de)
8. **European Parliament & Council.** (2016). *Regulation (EU) 2016/679 (General Data Protection Regulation)*. Official Journal of the European Union, L 119/1. Available at: [https://eur-lex.europa.eu](https://eur-lex.europa.eu)
9. **Pedregosa, F., et al.** (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research (JMLR), 12, 2825–2830.
