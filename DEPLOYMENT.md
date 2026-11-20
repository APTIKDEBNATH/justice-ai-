# 🚀 Justice AI: Production Deployment & Operation Guide

**Project:** Justice AI – Universal Multi-Jurisdictional Legal Intelligence Suite  
**Architecture:** Decoupled Micro-Architecture (Frontend Client + Backend REST API)  
**Status:** Validated, Hardened & Deployment Ready  

---

## 📌 Architecture Overview

Justice AI operates as a decoupled two-tier system:

| Service | Port | Protocol | Purpose | Key File |
|---|---|---|---|---|
| **Frontend Web Client** | `3000` | HTTP / Static | Serves HTML5/CSS3 client interface with dynamic theme and language managers | [frontend_server.py](file:///c:/Users/akdeb/Desktop/experiments/LEGAL%20CHATBOT/frontend_server.py) |
| **Backend REST API** | `5000` | HTTP / JSON | Handles NLP statutory retrieval, supervised ML classification, and RAG | [backend_server.py](file:///c:/Users/akdeb/Desktop/experiments/LEGAL%20CHATBOT/backend_server.py) |
| **Streamlit Dashboard** | `8501` | HTTP / WS | Internal analytics and research dashboard | [app.py](file:///c:/Users/akdeb/Desktop/experiments/LEGAL%20CHATBOT/app.py) |

---

## 🛠️ Deployment Methods

### Option 1: 1-Click Local Production Startup

Run the unified process orchestrator:
```bash
python run_all.py
```
This automatically launches both the Backend API on port `5000` and the Frontend Web App on port `3000` with automated process monitoring and graceful shutdown (`Ctrl+C`).

---

### Option 2: Docker & Docker Compose (Recommended for Cloud)

Deploy anywhere (AWS EC2, Google Cloud, DigitalOcean, Azure):
```bash
# Build and start all services in the background
docker compose up -d --build

# View real-time logs
docker compose logs -f

# Stop services
docker compose down
```

---

### Option 3: Cloud PaaS Deployment (Render / Railway / Heroku)

1. Connect your repository to **Railway** or **Render**.
2. The included [`Procfile`](file:///c:/Users/akdeb/Desktop/experiments/LEGAL%20CHATBOT/Procfile) tells the platform to start `python run_all.py`.
3. Set environment variables (optional for external LLMs):
   - `GEMINI_API_KEY`: *(Optional) For Google Gemini live inference*
   - `OPENAI_API_KEY`: *(Optional) For OpenAI GPT-4 live inference*
4. Justice AI includes built-in offline heuristics and local statutory knowledge bases, ensuring 100% functionality even without any API keys configured!

---

### Option 4: Production Nginx Reverse Proxy Configuration

For hosting behind standard web proxies:
```nginx
server {
    listen 80;
    server_name justice-ai.yourdomain.com;

    # Frontend Client
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API Routing
    location /api/ {
        proxy_pass http://127.0.0.1:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 🔍 API Endpoints Reference

### 1. `GET /api/health`
Checks server health and active modules:
```json
{
  "status": "online",
  "service": "Justice AI Dedicated Backend API",
  "port": 5000,
  "version": "2.1.0",
  "endpoints": ["/api/chat", "/api/health", "/api/taxonomy"]
}
```

### 2. `POST /api/chat`
Processes statutory inquiries with ML intent classification and verified citations:
```json
// Request Body
{
  "query": "Does a landlord need a reason to evict in Germany?",
  "jurisdiction": "DE",
  "category": "Tenancy: Eviction & Termination Notice",
  "language": "en"
}

// Response Body
{
  "status": "success",
  "jurisdiction": "DE",
  "category": "Tenancy: Eviction & Termination Notice",
  "language": "en",
  "card": {
    "headline": "In most cases, yes. A landlord needs a legitimate reason to end an open-ended residential lease.",
    "body_text": "...",
    "tag_label": "Germany · Tenancy: Eviction & Termination Notice",
    "sources": [
      {
        "title": "BGB § 573 · Ordinary termination by the landlord",
        "domain": "gesetze-im-internet.de",
        "url": "https://www.gesetze-im-internet.de/bgb/__573.html"
      }
    ],
    "confidence_level": "High",
    "confidence_percentage": 85,
    "chips": ["What if I have lived here over 8 years?", "Can I object to the termination?"]
  }
}
```

---

## ✅ Quality Assurance & Verification Checklist

- [x] **No White Elements in Dark Mode:** Verified sleek graphite/charcoal `#000000` / `#27272A` theme without stark `#FFFFFF` backgrounds or buttons.
- [x] **Borderless Sun/Moon Theme Toggle:** Smooth icon-only circular button without square/pill borders.
- [x] **Full Multilingual & Regional Taxonomy:** Dynamic region-aware languages across 10+ jurisdictions.
- [x] **Boundary Safe Sidebar:** Long recent inquiry titles constrained with clean text-overflow ellipsis.
- [x] **Clean New Question Reset:** Empties consultation and displays starter prompt pills.
- [x] **Unit & Integration Test Suite:** 100% passing rate on [test_suite.py](file:///c:/Users/akdeb/Desktop/experiments/LEGAL%20CHATBOT/test_suite.py).
