"""
Justice AI - Smart India Hackathon (SIH) Official Presentation Deck Generator
Generates a 16:9 widescreen, professionally formatted PowerPoint deck (.pptx)
following the official SIH evaluation rubric and presentation format.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path="Justice_AI_SIH_Presentation.pptx"):
    prs = Presentation()
    # 16:9 Widescreen standard
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette (Corporate Legal / Tech)
    DARK_BG = RGBColor(15, 23, 42)       # Slate 900
    LIGHT_BG = RGBColor(248, 250, 252)   # Slate 50
    CARD_BG = RGBColor(255, 255, 255)    # White
    CARD_BORDER = RGBColor(226, 232, 240)# Slate 200
    TEXT_DARK = RGBColor(30, 41, 59)     # Slate 800
    TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500
    ACCENT_GOLD = RGBColor(217, 119, 6)  # Amber 600
    ACCENT_BLUE = RGBColor(37, 99, 235)  # Blue 600
    ACCENT_EMERALD = RGBColor(5, 150, 105) # Emerald 600

    def add_header(slide, title_text, category_tag="SMART INDIA HACKATHON 2024 / 2025"):
        # Header category badge
        badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.4))
        tf_b = badge_box.text_frame
        tf_b.word_wrap = True
        p_b = tf_b.paragraphs[0]
        p_b.text = category_tag.upper()
        p_b.font.size = Pt(11)
        p_b.font.bold = True
        p_b.font.color.rgb = ACCENT_BLUE

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK

    def add_card(slide, left, top, width, height, title, items, badge="", border_color=CARD_BORDER):
        # Card container
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        shape.fill.solid()
        shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)

        tb = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(width - 0.5), Inches(height - 0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_title = tf.paragraphs[0]
        if badge:
            p_title.text = f"{badge}  {title}"
        else:
            p_title.text = title
        p_title.font.size = Pt(16)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_DARK

        for item in items:
            p = tf.add_paragraph()
            p.space_before = Pt(8)
            p.level = 0
            
            if isinstance(item, tuple):
                bold_prefix, text_content = item
                run1 = p.add_run()
                run1.text = f"• {bold_prefix}: "
                run1.font.bold = True
                run1.font.size = Pt(12)
                run1.font.color.rgb = TEXT_DARK
                
                run2 = p.add_run()
                run2.text = text_content
                run2.font.bold = False
                run2.font.size = Pt(12)
                run2.font.color.rgb = TEXT_MUTED
            else:
                run = p.add_run()
                run.text = f"• {item}"
                run.font.size = Pt(12)
                run.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Hero Cover)
    # -------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_BG
    bg1.line.fill.background()

    # Title box
    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(4.5))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "SMART INDIA HACKATHON — INNOVATION PROPOSAL"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD

    p2 = tf1.add_paragraph()
    p2.text = "Justice AI: Multilingual Multi-Jurisdictional Legal RAG & Intelligence Platform"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(255, 255, 255)
    p2.space_before = Pt(12)

    p3 = tf1.add_paragraph()
    p3.text = "An accessible, hallucination-resistant statutory advisory engine grounded in official government gazettes."
    p3.font.size = Pt(16)
    p3.font.color.rgb = RGBColor(203, 213, 225)
    p3.space_before = Pt(10)

    # Details Box (Bottom)
    det_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.5), Inches(11.3), Inches(2.2))
    det_box.fill.solid()
    det_box.fill.fore_color.rgb = RGBColor(30, 41, 59)
    det_box.line.color.rgb = RGBColor(51, 65, 85)

    dtb = s1.shapes.add_textbox(Inches(1.3), Inches(4.7), Inches(10.7), Inches(1.8))
    dtf = dtb.text_frame
    
    dp1 = dtf.paragraphs[0]
    dp1.text = "PROBLEM STATEMENT DETAILS & TEAM CREDENTIALS"
    dp1.font.size = Pt(12)
    dp1.font.bold = True
    dp1.font.color.rgb = ACCENT_GOLD

    dp2 = dtf.add_paragraph()
    dp2.space_before = Pt(6)
    r = dp2.add_run()
    r.text = "PS Code & Category: "
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(255, 255, 255)
    r2 = dp2.add_run()
    r2.text = "Open Innovation / Smart Legal Tech (Software Edition)"
    r2.font.size = Pt(13)
    r2.font.color.rgb = RGBColor(226, 232, 240)

    dp3 = dtf.add_paragraph()
    dp3.space_before = Pt(4)
    r = dp3.add_run()
    r.text = "Team Name: "
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = RGBColor(255, 255, 255)
    r2 = dp3.add_run()
    r2.text = "[Team Name]  |  Team Leader: [Leader Name]  |  Institute: [College / University Name]"
    r2.font.size = Pt(13)
    r2.font.color.rgb = RGBColor(226, 232, 240)

    # -------------------------------------------------------------------------
    # SLIDE 2: Proposed Solution & Core Innovation
    # -------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Proposed Solution: What Makes Justice AI Novel?", "SIH 2024 / 2025 · Core Solution")

    add_card(s2, 0.8, 1.6, 5.6, 5.2, "The Real-World Problem", [
        ("Information Asymmetry", "Citizens lack the ability to navigate complex multi-volume legal gazettes, missing statutory limitation dates."),
        ("Generative AI Hallucinations", "Open-domain LLMs invent non-existent sections, cite repealed acts, and cross-contaminate national laws."),
        ("Language & Cost Barrier", "Formal legal consultations cost thousands of rupees, and laws are rarely accessible in local regional vernaculars.")
    ], badge="[X]")

    add_card(s2, 6.8, 1.6, 5.7, 5.2, "Our Innovative Solution", [
        ("Supervised Intent & Jur Routing", "Trained ML model predicts applicable jurisdiction from raw citizen queries with 100% boundary isolation."),
        ("Strict Gazette Grounding (RAG)", "Vector-indexed search across official government portals (India Code, BMJ Germany, EUR-Lex, US Code)."),
        ("Editorial Citizen UI", "Delivers crisp headline answers, official statutory badges, confidence scores, and limitation period alerts."),
        ("Multilingual Localization", "Auto-filters regional languages (Hindi, Punjabi, Bengali, Tamil, German, French) based on context.")
    ], badge="[OK]", border_color=ACCENT_BLUE)

    # -------------------------------------------------------------------------
    # SLIDE 3: Technical Architecture & Methodology
    # -------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Technical Architecture & System Workflow", "System Design & Methodology")

    add_card(s3, 0.8, 1.6, 3.6, 5.2, "Presentation Tier (:3000)", [
        ("Decoupled Web Client", "Lightweight HTML5/CSS3/ES6 web app with zero client framework bloat."),
        ("Editorial Typography", "Newsreader serif & Inter fonts for high readability."),
        ("Strict Accessibility", "Monochrome dark mode (zero white elements) and crisp SVG icons instead of emojis.")
    ], badge="[Client]")

    add_card(s3, 4.8, 1.6, 3.7, 5.2, "Intelligence Tier (:5000)", [
        ("Multithreaded REST API", "High-throughput ThreadingHTTPServer eliminating keep-alive deadlocks."),
        ("ML Classifier", "TF-IDF + Logistic Regression model for real-time jurisdictional prediction."),
        ("Deterministic RAG Engine", "Cosine similarity retrieval over section-chunked legislative provisions.")
    ], badge="[Engine]", border_color=ACCENT_BLUE)

    add_card(s3, 8.9, 1.6, 3.6, 5.2, "Data & Knowledge Tier", [
        ("Statutory Knowledge Base", "Curated JSON indices covering BNS 2023, BGB, GDPR, FLSA."),
        ("Provenance Attribution", "Every advisory response pairs with direct HTTPS links to official government registers."),
        ("Safety & Guardrails", "Emergency crisis detector intercepts high-danger queries and routes to official helplines.")
    ], badge="[Data]")

    # -------------------------------------------------------------------------
    # SLIDE 4: Feasibility & Operational Viability
    # -------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Feasibility, Implementation & Risk Mitigation", "Feasibility & Viability")

    add_card(s4, 0.8, 1.6, 5.6, 5.2, "Technical & Operational Feasibility", [
        ("Zero Dependency on GPU Clusters", "Utilizes optimized scikit-learn models and lightweight vector search, allowing deployment on modest CPU cloud droplets or local edge machines."),
        ("Offline-Capable Hybrid Design", "Can operate in restricted environments with local fallback heuristics when external internet connectivity is unavailable."),
        ("Instant Deployment", "Pre-configured Docker Compose, single supervisor (run_all.py), and cross-platform compatibility (Linux, Windows, macOS).")
    ], badge="[Feasibility]")

    add_card(s4, 6.8, 1.6, 5.7, 5.2, "Potential Risks & Mitigation Strategy", [
        ("Risk: Inadvertent Legal Liability", "Mitigation: Every response includes an explicit statutory disclaimer and classifies output as general legal information, not formal counsel."),
        ("Risk: Legislative Amendments", "Mitigation: Modular knowledge base design allows dropping updated JSON act chunks without model retraining."),
        ("Risk: Malicious Prompt Injection", "Mitigation: System-level input sanitation, jurisdictional boundary enforcement, and hardcoded emergency guardrails.")
    ], badge="[Mitigation]", border_color=ACCENT_EMERALD)

    # -------------------------------------------------------------------------
    # SLIDE 5: Social Impact & Target Beneficiaries
    # -------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Social Impact & Target Beneficiaries", "Value Proposition & National Reach")

    add_card(s5, 0.8, 1.6, 3.6, 5.2, "Everyday Citizens", [
        ("Tenancy Rights", "Protects tenants from illegal lockouts and arbitrary eviction notices."),
        ("Consumer Justice", "Empowers buyers to draft formal complaints under the Consumer Protection Act."),
        ("Wage Earners", "Enables workers to identify unpaid statutory overtime and minimum wage breaches.")
    ], badge="[Citizens]")

    add_card(s5, 4.8, 1.6, 3.7, 5.2, "Legal Aid Clinics & CSCs", [
        ("Common Service Centres (CSCs)", "Can be deployed at 300,000+ rural CSCs to power preliminary intake for rural citizens."),
        ("Paralegal Triage", "Accelerates initial client intake, fact summaries, and preliminary dossier compilation for legal aid lawyers.")
    ], badge="[Access]", border_color=ACCENT_GOLD)

    add_card(s5, 8.9, 1.6, 3.6, 5.2, "Judicial System Benefits", [
        ("Reduced Frivolous Litigation", "Clarifies threshold statutory conditions before filing, preventing misfiled suits."),
        ("Preserved Limitation Dates", "Alerts citizens to mandatory statutory deadlines (e.g. 2-year consumer limit) before rights lapse.")
    ], badge="[Judiciary]")

    # -------------------------------------------------------------------------
    # SLIDE 6: Comparative Analysis & Competitive Edge
    # -------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Competitive Edge & Comparison with Existing Systems", "Comparative Analysis")

    add_card(s6, 0.8, 1.6, 5.6, 5.2, "Comparison Matrix", [
        ("General LLMs (ChatGPT / Claude)", "Prone to severe statutory hallucinations; frequently cite repealed acts; no direct links to official gazettes."),
        ("Commercial Legal Databases (SCC Online)", "Expensive ($500+/yr); designed for advocates; zero plain-language summaries for non-lawyers."),
        ("Raw Government Portals (India Code)", "High legal veracity, but lacks semantic natural language query processing or multilingual synthesis.")
    ], badge="[Competitors]")

    add_card(s6, 6.8, 1.6, 5.7, 5.2, "Justice AI Unique Selling Points (USPs)", [
        ("100% Provenance Verification", "Every claim is pinned to official government domains (.nic.in, .gov, .europa.eu)."),
        ("Multi-Jurisdictional ML Firewall", "Zero cross-contamination between Indian, German, EU, and US statutory frameworks."),
        ("Ultra-Low Latency (~45 ms)", "Multithreaded decoupled architecture delivers instantaneous response generation."),
        ("Inclusive Accessibility", "Monochrome dark mode, no distracting emojis, and regional language filtering.")
    ], badge="[Our USP]", border_color=ACCENT_BLUE)

    # -------------------------------------------------------------------------
    # SLIDE 7: Scalability, Government Integration & Roadmap
    # -------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Future Scope & Government Integration Roadmap", "National Scaling Strategy")

    add_card(s7, 0.8, 1.6, 3.6, 5.2, "Phase 1: Present (Delivered)", [
        ("Full-Stack Decoupled Core", "REST API, HTML5 client, and Streamlit dashboard active."),
        ("Multi-Jurisdictional Classifier", "Trained ML model + BNS/BGB/GDPR/FLSA RAG."),
        ("100% Unit Test Pass Rate", "Comprehensive automated verification.")
    ], badge="[Phase 1]", border_color=ACCENT_EMERALD)

    add_card(s7, 4.8, 1.6, 3.7, 5.2, "Phase 2: National e-Governance", [
        ("Digital India Bhashini Integration", "Integrate voice-to-text and voice-to-voice in 22 scheduled Indian languages for illiterate citizens."),
        ("e-Daakhil & e-Courts Connect", "Direct 1-click filing of generated consumer dossiers into the official e-Daakhil consumer portal.")
    ], badge="[Phase 2]", border_color=ACCENT_BLUE)

    add_card(s7, 8.9, 1.6, 3.6, 5.2, "Phase 3: Nationwide Scale", [
        ("Tele-Law Integration", "Embedding Justice AI inside the Ministry of Law & Justice's Tele-Law scheme."),
        ("State Acts Expansion", "Ingestion of state-level Rent Control Acts, Land Revenue Codes, and Municipal Bylaws.")
    ], badge="[Phase 3]")

    # -------------------------------------------------------------------------
    # SLIDE 8: Team Structure & Project Deliverables
    # -------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Team Credentials, Deliverables & Conclusion", "Team & Summary")

    add_card(s8, 0.8, 1.6, 5.6, 5.2, "Team Roles & Responsibilities", [
        ("[Student / Leader Name]", "Full Stack Architecture, Multithreaded REST APIs, Docker Containerization."),
        ("[Team Member 2]", "Machine Learning & NLP Engineering, TF-IDF Classifier Training & Hyperparameter Tuning."),
        ("[Team Member 3]", "Statutory Knowledge Curation, RAG Inverted Indexing, Gazette Verification."),
        ("[Team Member 4 / UI Designer]", "Front-End UX/UI Engineering, Monochrome Accessibility, Dynamic Localization.")
    ], badge="[Team]")

    add_card(s8, 6.8, 1.6, 5.7, 5.2, "Verified Deliverables Ready Today", [
        ("Working Live Prototype", "Client Web App on :3000, REST API on :5000, Streamlit Dashboard on :8501."),
        ("Single-Command Startup", "python run_all.py or docker compose up -d."),
        ("Trained ML Artifacts", "Serialized classifier in data/models/jurisdiction_classifier.pkl."),
        ("Comprehensive Documentation", "Full Academic Project Report, Deployment Manual, and Automated Test Suite.")
    ], badge="[Ready]", border_color=ACCENT_GOLD)

    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    create_deck()
