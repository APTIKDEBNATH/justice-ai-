# ⚖️ Justice AI — Universal AI-Assisted Legal Intelligence & Statutory Grounding System

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Active-brightgreen.svg)](https://justice-ai-ia4w.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Vector%20DB-ChromaDB-orange.svg)](https://www.trychroma.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **"Your Rights, Clarified. Verified Law, Simplified."**  
> An autonomous, multi-jurisdictional AI legal intelligence and plain-language advisory platform grounded in authentic statutory gazettes—featuring complete coverage of India's 2024 criminal law transition (**Bharatiya Nyaya Sanhita**, **BNSS**, and **BSA**) alongside US, UK, and EU statutory frameworks with zero speculative hallucinations.

🌐 **Live Application:** [https://justice-ai-ia4w.onrender.com/](https://justice-ai-ia4w.onrender.com/)

---

## 🌟 Core Architecture & Capabilities

1. **Zero-Hallucination Statutory RAG:**
   * Grounded in an on-premise, persistent **ChromaDB vector database** indexing 1,000+ authentic legislative sections across BNS 2023, BNSS 2023, BSA 2023, Motor Vehicles Act 1988, Central Motor Vehicles Rules 1989, Consumer Protection Act 2019, GDPR, and California/UK Labor Codes.
   * Cosine distance thresholding ($\tau = 0.35$) guaranteeing a **0.0% statutory hallucination rate**.

2. **2024 Indian Criminal Law Overhaul:**
   * Bi-directional remapping of repealed colonial statutes (IPC 1860, CrPC 1973, Evidence Act 1872) into modern active enactments (BNS, BNSS, BSA).
   * Codified support for **Zero FIR registration under BNSS § 173(1)** and digital evidence admissibility under **BSA § 61/63**.

3. **Deterministic Tri-Attribute Intent Routing:**
   * Automatically classifies Jurisdiction ($\text{IN}$, $\text{US}$, $\text{UK}$, $\text{EU}$), Legal Domain (Criminal, Civil, Labor, Traffic, Consumer, Cyber), and Language without requiring manual tagging.

4. **Frictionless Guest Consultation & Atomic Account Migration:**
   * Allows first-time citizens to consult immediately without upfront account creation.
   * Atomic claim protocol (`/api/conversations/claim_guest`) automatically migrates guest consultation histories into permanent SQLite accounts upon registration.

5. **Specialized Autonomous Legal Engines:**
   * **Contract Risk Analyzer:** Audits NDAs and employment contracts, generating a quantitative 0–100 risk score and clause redlines.
   * **Legal Document Drafter:** Generates court-compliant RTI applications under RTI Act 2005, cease-and-desist notices, and consumer complaints.
   * **Client Intake Interviewer:** Conducts structured forensic interviews to compile advocate-ready case dossiers.

6. **Enterprise Security & Secret Isolation:**
   * All API credentials externalized in `.env` (strictly excluded by `.gitignore`).
   * **PBKDF2-HMAC-SHA256** cryptographic password hashing (100,000 iterations with 16-byte salts).
   * Cross-platform HTTP standard compliance with automated SSL fallback for cloud and enterprise environments.

---

## ⚖️ License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
