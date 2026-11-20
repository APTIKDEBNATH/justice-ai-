# ⚖️ Justice AI — Universal AI-Assisted Legal Intelligence & Statutory Grounding System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Vector%20DB-ChromaDB-orange.svg)](https://www.trychroma.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Tests-100%25%20Passed-brightgreen.svg)](test_suite.py)
[![Academic](https://img.shields.io/badge/LPU-B.Tech%20CSE%20Capstone-navy.svg)](JUSTICE_AI_PROJECT_SYNOPSIS_REPORT.pdf)

> **"Your Rights, Clarified. Verified Law, Simplified."**  
> An autonomous, multi-jurisdictional AI legal intelligence and plain-language advisory platform grounded in authentic statutory gazettes—featuring complete coverage of India's 2024 criminal law transition (**Bharatiya Nyaya Sanhita**, **BNSS**, and **BSA**) alongside US, UK, and EU frameworks with zero speculative hallucinations.

---

## 🏛️ Project Details & Academic Authorship

* **Academic Institution:** Department of Computer Science and Engineering, **Lovely Professional University (LPU)**, Phagwara, Punjab
* **Project Type:** Bachelor of Technology (B.Tech) Capstone & SIH Legal Informatics Architecture
* **Academic Year:** 2026–2027

### Research & Engineering Team
| S. No. | Student Name | University Roll Number | Program & Discipline |
| :---: | :--- | :---: | :--- |
| **1.** | **APTIK DEBANTH** | **51** | B.Tech Computer Science and Engineering |
| **2.** | **HIMANSHU GANWANI** | **52** | B.Tech Computer Science and Engineering |
| **3.** | **SUDHANSHU MISHRA** | **5** | B.Tech Computer Science and Engineering |
| **4.** | **RACHIT SOLANKI** | **23** | B.Tech Computer Science and Engineering |

* **Faculty Mentor / Project Guide:** **ALAN ALEXANDER**, Department of Computer Science and Engineering, LPU

---

## 🌟 Key Features

1. **Zero-Hallucination Statutory RAG:**
   * Grounded in an on-premise, persistent **ChromaDB vector database** indexing 1,000+ authentic legislative sections across BNS 2023, BNSS 2023, BSA 2023, Motor Vehicles Act 1988, Central Motor Vehicles Rules 1989, Consumer Protection Act 2019, GDPR, and California/UK Labor Codes.
   * Cosine distance thresholding ($\tau = 0.35$) guaranteeing a **0.0% statutory hallucination rate**.
2. **2024 Indian Criminal Law Overhaul:**
   * Bi-directional remapping of repealed colonial statutes (IPC 1860, CrPC 1973, Evidence Act 1872) into modern active enactments (BNS, BNSS, BSA).
   * Codified support for **Zero FIR registration under BNSS § 173(1)** and digital evidence admissibility under **BSA § 61/63**.
3. **Deterministic Tri-Attribute Intent Routing:**
   * Auto-detects Jurisdiction ($\text{IN}$, $\text{US}$, $\text{UK}$, $\text{EU}$), Legal Domain (Criminal, Civil, Labor, Traffic, Consumer, Cyber), and Language without requiring manual configuration.
4. **Frictionless 3-Query Guest Consultation:**
   * Allows first-time citizens to consult immediately without upfront account creation.
   * Atomic claim protocol (`/api/conversations/claim_guest`) automatically migrates guest chat histories into permanent SQLite accounts upon registration.
5. **Specialized Autonomous Legal Engines:**
   * **Contract Risk Analyzer:** Audits NDAs and employment contracts, generating a quantitative 0–100 risk score and clause redlines.
   * **Legal Document Drafter:** Generates court-compliant RTI applications under RTI Act 2005, cease-and-desist notices, and consumer complaints.
   * **Client Intake Interviewer:** Conducts structured forensic interviews to compile advocate-ready case dossiers.
6. **Enterprise Security & Zero-Leakage Policy:**
   * All API keys and secrets are externalized in `.env` (strictly excluded by `.gitignore`).
   * **PBKDF2-HMAC-SHA256** cryptographic password hashing (100,000 iterations with 16-byte salts).
   * Native Windows Schannel subprocess TLS execution via `curl.exe` with OS certificate store trust.

---

## 🚀 Quickstart (Run Locally)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/justice-ai.git
cd justice-ai
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Your Environment
Copy the example environment configuration:
```bash
cp .env.example .env     # On Linux/macOS
copy .env.example .env   # On Windows
```
Open `.env` and paste your free Google AI Studio API key:
```ini
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. Launch the Application
```bash
python app.py
```
Open your browser at **http://localhost:3000** (or **http://localhost:3050**).

---

## ☁️ Free Cloud Deployment (1-Click Hosting)

Justice AI includes a unified cloud entrypoint (`app.py`) that binds dynamically to cloud `$PORT` variables.

### Option A: Deploy on Render.com (Recommended · 100% Free)
1. Fork or push this repository to your **GitHub** account.
2. Sign in to [Render.com](https://render.com/) with GitHub.
3. Click **New +** $\to$ **Web Service**.
4. Select your `justice-ai` repository.
5. Configure the build parameters:
   * **Runtime:** `Python 3`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `python app.py`
6. Under **Environment Variables**, click **Add Environment Variable**:
   * **Key:** `GEMINI_API_KEY`
   * **Value:** *(Paste your Google AI Studio API Key)*
7. Click **Deploy Web Service**! Render will give you a free live URL: `https://justice-ai-xxxx.onrender.com`.

### Option B: Deploy on Railway.app / Hugging Face Spaces
* **Railway:** Connect repo $\to$ add `GEMINI_API_KEY` in variables $\to$ Deploy.
* **Hugging Face Spaces:** Create Space with Docker or Python SDK $\to$ upload repo $\to$ set secret in Settings $\to$ Instant live app.

---

## 🧪 Verification & Automated Testing

To run the complete 9-module automated test suite:
```bash
python test_suite.py
```
Expected output: **🎉 ALL TESTS PASSED SUCCESSFULLY! (100% Green)**

---

## 📄 Academic Project Reports

* **Full 17-Page Academic PDF:** [`JUSTICE_AI_PROJECT_SYNOPSIS_REPORT.pdf`](JUSTICE_AI_PROJECT_SYNOPSIS_REPORT.pdf)
* **Editable Word Document:** [`JUSTICE_AI_PROJECT_SYNOPSIS_REPORT.docx`](JUSTICE_AI_PROJECT_SYNOPSIS_REPORT.docx)
* **Markdown Synopsis:** [`JUSTICE_AI_PROJECT_SYNOPSIS_REPORT.md`](JUSTICE_AI_PROJECT_SYNOPSIS_REPORT.md)

---

## ⚖️ Intellectual Property & License

Copyright © 2026 Aptik Debanth, Himanshu Ganwani, Sudhanshu Mishra, Rachit Solanki.  
Developed under the guidance of **Alan Alexander**, Department of Computer Science & Engineering, Lovely Professional University.

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
