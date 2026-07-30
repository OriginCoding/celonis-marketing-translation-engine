# 🌐 Celonis Enterprise Marketing Asset Translation Engine

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js 14](https://img.shields.io/badge/Frontend-Next.js%2014-black.svg)](https://nextjs.org/)
[![Pytest Passed](https://img.shields.io/badge/Tests-15%2F15%20Passed-success.svg)](https://docs.pytest.org/)
[![Net Direct ROI](https://img.shields.io/badge/ROI-373%25-brightgreen.svg)](docs/TCO_ROI_MODEL.md)
[![Payback Period](https://img.shields.io/badge/Payback-2.5%20Months-emerald.svg)](docs/TCO_ROI_MODEL.md)

> **Sr. Applied AI Engineer Technical Challenge Submission**  
> **Target Organization:** Celonis Marketing Applied AI Solutions Team  
> **Scope:** English to Spanish (`es-ES`) Marketing Document Localization, AI Quality Gates, & Confidence Routing  

---

## 📌 Executive Summary & Business Impact

Celonis Marketing localizes 400+ deliverables annually across 7 target languages. Currently, this process relies on 6+ disconnected platforms with **98% manual orchestration**. Language Champions spend **334 hours per year** manually reviewing localized assets line-by-line due to invisible quality gates.

This repository provides a full-stack, enterprise-grade **Marketing Asset Translation Engine** combining a **Python 3.10+ FastAPI Microservice Backend** and a **Next.js 14 App Router Web Studio**.

### 📈 Key Business Outcomes
* **55% Reduction in Time-to-Market (TTM)**: Compresses localization cycles from 14 days down to 6 days.
* **70% Reduction in Review Effort**: Saves **234 Language Champion hours annually**.
* **373% Net Direct ROI**: **$19,890/year direct labor savings** against a $4,205/year total OPEX ($5.04/yr LLM token cost) with a **2.5-month payback period**.
* **100% Brand Safety**: Zero brand drift guarantee via zero-trust Do-Not-Translate (DNT) term protection (`Celonis`, `Agent C`, `Celonis Process Intelligence`, `MCP`).

---

## 🏛️ Key System Architecture Highlights

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STAGE 1: INGESTION & DOM AST EXTRACTION                  │
│  Ingests HTML briefs, extracts text nodes via BeautifulSoup AST parsing    │
│  Achieves 65% LLM Prompt Token Footprint Compression (650 tokens/run)     │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STAGE 2: KNOWLEDGE GROUNDING & RAG                       │
│  Retrieves active DNT glossary rules & performs sub-5ms cosine vector search│
│  over Translation Memory (TM) segments via self-hosted Qdrant HNSW engine   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STAGE 3: CONTEXT-AWARE LLM TRANSLATION                   │
│  Primary: Live Google Gemini 2.5 Flash API with XML prompt guardrails       │
│  Fallback: Universal Dynamic Spanish Localizer enforcing Excel rules        │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STAGE 4: AI QUALITY GATE & FACT VERIFIER                 │
│  Scores Accuracy (35%), Brand DNT (30%), Tone (20%), and Format (15%)       │
│  Fact Grounding Verifier deterministically checks numbers & hyperlinks      │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STAGE 5: CONFIDENCE ROUTING & AUDIT                      │
│  Score >= 88%: AUTO-PASS -> Direct CMS Staging Ingestion                    │
│  Score < 88%: HITL REVIEW -> Routed to Language Champion Signoff Portal     │
│  AI REFLEXION LOOP: Re-prompts LLM with critique to self-correct documents   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Built-In Open-Source Enterprise Security & Observability

To demonstrate Day-2 enterprise production readiness at **$0 infrastructure software cost**, the system includes 5 built-in open-source modules:

1. **HTML XSS Security Sanitizer** (`backend/app/resilience/html_sanitizer.py`): Strips dangerous executable tags (`<script>`, `<iframe>`) and inline event handlers (`onload=`, `onerror=`) while preserving semantic HTML markup.
2. **Idempotency Key Manager** (`backend/app/resilience/idempotency.py`): Tracks `X-Idempotency-Key` headers to prevent duplicate LLM execution on network retries.
3. **Evaluator Alignment & Drift Tracker** (`backend/app/services/eval_benchmark_service.py`): Calculates Cohen's Kappa coefficient ($\kappa$) measuring decision agreement between Language Champions and AI Judge scores.
4. **OpenTelemetry Tracing & Telemetry** (`backend/app/services/telemetry_service.py`): Generates OpenTelemetry-compatible trace spans, APM metrics, and prompt versioning (`v1.3.0`).
5. **Self-Hosted Qdrant HNSW Vector RAG** (`backend/app/services/qdrant_service.py`): Sub-5ms HNSW vector similarity search over Translation Memory segments.

---

## 🖥️ User Workflow Guide (How to Use the Studio)

Access the web dashboard at `http://localhost:3000`:

1. **Step 1 (Ingestion & Upload)**:
   - Select a sample test scenario (`Scenario 1: Clean Landing Page`, `Scenario 2: DNT Brand Tampering`) or drag-and-drop a custom English HTML file.
2. **Step 2 (Visual Preview)**:
   - View side-by-side visual rendered cards comparing original English copy vs localized Spanish output with DNT highlights.
3. **Step 3 (AI Quality Check)**:
   - Inspect the AI Quality Gate radar matrix across Accuracy, DNT Compliance, Tone, and Tag Parity.
4. **Step 4 (Routing & AI Reflexion)**:
   - If score $\ge 88\%$: Click **Approve & Publish** to send payload to staging CMS webhooks.
   - If score $< 88\%$ (e.g. brand tampering detected): Click **`🪄 Improve & Resubmit (AI Reflexion)`** to watch the **Real-Time Progress HUD Modal** step from $0\% \rightarrow 100\%$, repairing brand terms automatically!

---

## 📂 Public Repository Deliverables Structure

```text
├── README.md                              # Primary Repository Overview & Setup Guide
├── SOLUTION_DESIGN.md                     # Deliverable 1: Technical Solution Design
├── TCO_ROI_MODEL.md                       # Deliverable 3: Financial ROI Model
├── WALKTHROUGH_DECK.md                    # Deliverable 4: Live Presentation Slide Deck
├── backend/                               # Python 3.10+ FastAPI Microservice Backend
│   ├── app/                               # Agents, Core LLM Drivers, Resilience & Services
│   └── tests/                             # 15 Pytest Automated Unit & Integration Test Suites
├── frontend/                              # Next.js 14 App Router TypeScript Web Studio
│   ├── app/                               # Studio pages (/), Repository (/repository), Audit (/audit-logs)
│   └── components/                        # Radar charts, diff inspector, & progress HUD modals
├── docker-compose.yml                     # Single-Command Container Orchestrator
└── start_all.py                           # Python Local Development Launcher
```

---

## 🚀 Step-by-Step Setup Guide

### Option 1: Native Python & Next.js Launcher (Recommended for Development)

Ensure Python 3.10+ and Node.js 18+ are installed.

```powershell
# 1. Install Backend Dependencies
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cd ..

# 2. Install Frontend Dependencies
cd frontend
npm install
cd ..

# 3. Launch Both Backend & Frontend Simultaneously
python start_all.py
```

* **Frontend Studio UI**: `http://localhost:3000`
* **FastAPI Backend OpenAPI Docs**: `http://localhost:8000/docs`

---

### Option 2: Docker Single-Command Deployment (Production Container Setup)

```bash
# Build and launch multi-container architecture (Backend, Frontend, Redis, Qdrant, MinIO)
docker compose up --build
```

---

## 🧪 Verification & Automated Testing

Run the full Pytest suite verifying edge cases, AST parsing, DNT enforcement, and security:

```powershell
$env:PYTHONPATH="backend"; .venv\Scripts\python.exe -m pytest backend/tests/ -v
```

**Result**: `15 passed in 0.51s` (100% pass rate).

---

## 🔬 Architectural Scope: Current Implementation vs. Phase 2 Scale

To provide an honest architectural evaluation, the table below delineates what is **Current Implemented MVP Scope** versus **Phase 2 Enterprise Extensions**:

| Component Layer | Implemented Current MVP Scope | Phase 2 Enterprise Extension |
| :--- | :--- | :--- |
| **DOM Parsing** | String text nodes & translatable attributes (`placeholder`, `alt`, `title`, `aria-label`). | Embedded image/SVG OCR text extraction via Gemini 2.5 Flash Vision. |
| **Language Direction** | Left-to-Right (LTR) English to Spanish (`es-ES`). | Right-to-Left (RTL) layout direction inversion (`dir="rtl"`) for Arabic/Hebrew. |
| **File Storage** | Open-source file storage repository (`storage/input/`, `storage/output/`). | Multi-tenant SOC 2 isolated buckets (`storage/{tenant_id}/`) with AES-256 encryption. |
| **Task Notifications**| Non-blocking async queue returning `202 Accepted`. | Server-Sent Events (SSE) / WebSocket push notifications per file. |
| **LLM Gateway** | Live Google Gemini 2.5 Flash with zero-cost fallback localizer. | LiteLLM enterprise proxy with multi-region failover and key rotation. |
