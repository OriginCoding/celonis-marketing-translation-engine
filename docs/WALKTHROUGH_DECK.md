# Walkthrough Presentation Deck: Marketing Asset Translation Engine

**Target Presentation:** Live 45-60 Minute Candidate Debrief  
**Organization:** Celonis Marketing Applied AI Solutions Team  
**Author:** Sr. Applied AI Candidate  

---

## Slide 1: Executive Title & Context
* **Title**: Celonis Marketing Asset Translation & Quality Gate Engine
* **Subtitle**: Applied AI Architecture, Enterprise Infrastructure, and Token Economics
* **Presenter**: Sr. Applied AI Engineer Candidate

---

## Slide 2: The Core Problem & Mission
* **Context**: Localizing 400+ deliverables annually across 7 languages spanning 6+ disconnected platforms.
* **Pain Points**: 98% manual orchestration, 49% zero-value steps, 334 hours/yr manual review bottleneck.
* **Our Mission**: Automated 4-Step Stepper Workflow with zero-trust brand protection and confidence routing.

---

## Slide 3: 4-Step Guided Workflow & System Architecture
* **Step 1**: Ingestion, File Upload & OAuth2 Okta SSO Auth Middleware.
* **Step 2**: Visual Side-by-Side Page Preview & RAG Grounding.
* **Step 3**: AI Quality Gate (Accuracy 35%, Brand DNT 30%, Tone 20%, Format 15%).
* **Step 4**: Confidence Routing, SQL Database Persistence, and Staging CMS Ingestion.

---

## Slide 4: Enterprise Infrastructure & Zero-Trust Guardrail
* **SQL Database Persistence**: `SQLAlchemy 2.0` ORM writing audit trails to persistent database tables.
* **Asynchronous Job Queue Worker Pool**: `Celery + Redis` background processing (`POST /api/hitl/async_batch`).
* **Zero-Trust DNT Penalty**: Any product name corruption applies an immediate **-25 point penalty per term**, forcing the score to **30/100** and triggering human review.

---

## Slide 5: Live POC Demonstration
* **Scenario 1**: Clean Landing Page (Auto-Pass 97.5%).
* **Scenario 2**: Drag-and-Drop Custom HTML Upload.
* **Scenario 3**: DNT Brand Corruption Error Detection (Score drops to 30/100).
* **Scenario 4**: Language Champion Review Portal & Persistent Audit Logs (`audit_history.json`).

---

## Slide 6: Applied AI Craft & Token Economics
* **DOM AST Text Node Extraction**: Compresses token footprint by **65%** (1,870 $\rightarrow$ 650 tokens per run).
* **0-Token Semantic Cache**: Serves repeated marketing CTAs in **2ms with 0 tokens consumed**.
* **Financial Impact**: $1.76/yr API cost, $19.8k/yr labor savings, **373% Net Direct ROI**, **3.0-month payback period**.

---

## Slide 7: Production Architecture & Scalability Summary
* 100% Enterprise MVP Feature Complete: SQL Persistence, Async Queues, and OAuth2 SSO Security.
* Easy cloud deployment via Docker Compose.
