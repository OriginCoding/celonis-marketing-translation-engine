# Celonis Marketing Asset Translation Engine

**Applied AI Technical Challenge Submission**  
**Role:** Sr. Applied AI Engineer, Marketing Applied AI Solutions Team  
**Scope:** English to Spanish (`es-ES`) Marketing Document Localization & AI Quality Gate  

---

## 📌 Executive Overview

Celonis Marketing localizes 400+ deliverables annually across 7 target languages. Currently, this process relies on 6+ disconnected platforms with **98% manual orchestration**. Language Champions spend **334 hours per year** manually reviewing localized assets line-by-line due to invisible and inconsistent quality gates.

This project delivers a full-stack, enterprise-grade **Marketing Asset Translation Engine** featuring:
1. **4-Step Guided Visual Stepper Workflow** (Select File $\rightarrow$ Translate $\rightarrow$ AI Quality Check $\rightarrow$ Approve & Publish).
2. **Zero-Trust Do-Not-Translate (DNT) Guardrails** with a **-25 point penalty per term** (dropping DNT score to **30/100** on brand term corruption).
3. **AI Quality Gate & Confidence Router**: Auto-Pass ($\ge 88\%$), HITL Review ($70\% - 87\%$), Reject ($< 70\%$).
4. **DOM AST Text Node Extraction & 65% Prompt Compression**: Compresses token payload from 1,870 down to 650 tokens per run ($5.04/yr LLM API cost).
5. **0-Token Semantic Cache & Translation Memory Vector RAG**.
6. **Open-Source Enterprise Security & Observability**: Built-in HTML XSS Security Sanitizer, Idempotency Key Manager, Cohen's Kappa Evaluator Drift Tracker, and OpenTelemetry Tracing.
7. **Persistent Compliance Audit Logging & Saved Disk Repository**.
8. **TCO Financial Model**: $4,205/yr total OPEX yielding **$19,890/yr labor savings (373% ROI)** with a **2.5-month payback period**.

---

## 📂 Public Repository Deliverables Structure

```text
├── README.md                              # Primary Repository Overview & Quickstart
├── SOLUTION_DESIGN.md                     # Deliverable 1: Solution Design Document
├── TCO_ROI_MODEL.md                       # Deliverable 3: TCO & Financial ROI Model
├── WALKTHROUGH_DECK.md                    # Deliverable 4: Presentation Deck
├── backend/                               # Python 3.10+ FastAPI Microservice Backend
├── frontend/                              # Next.js 14 App Router TypeScript Web Studio
├── docker-compose.yml                     # Single-Command Container Orchestrator
└── start_all.py                           # Python Local Development Launcher
```

---

## 🚀 Quickstart Guide

### Option 1: Native Python & Next.js Launcher
Ensure Python 3.10+ and Node.js 18+ are installed:

```powershell
python start_all.py
```

* **Frontend Studio**: `http://localhost:3000`
* **FastAPI Backend & API Docs**: `http://localhost:8000/docs`

---

### Option 2: Docker Single-Command Deployment

```bash
docker compose up --build
```

---

## 🧪 Automated Testing

Run the Pytest suite:

```powershell
$env:PYTHONPATH="backend"; .venv\Scripts\python.exe -m pytest backend/tests/
```

Result: `15 passed in 0.51s` (100% pass rate).
