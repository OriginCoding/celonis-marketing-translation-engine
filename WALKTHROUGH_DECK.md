# Live Debrief Presentation Deck: Marketing Asset Translation Engine

**Presenter:** Sr. Applied AI Engineer Candidate  
**Target Audience:** Technical & Non-Technical Reviewers  
**Format:** 45-Minute Live Debrief (Presentation + Live Agent Demo + Q&A)  

---

## Slide 1: Title & Framing
### Marketing Asset Translation Engine
**Architecting an Agentic Localization Pipeline with AI Quality Gates & HITL Routing**

* **Goal**: Transform Celonis' manual localization workflow into a scalable, intelligent translation engine.
* **Target Impact**: 55% TTM reduction for text/HTML assets, 70% reduction in Language Champion review time.

---

## Slide 2: The Situation & Problem Framing
### Current State Bottlenecks
* **Volume**: 400+ marketing deliverables localized per year across 7 languages.
* **Fragmentation**: 6+ disconnected platforms (Jira, Monday, Smartcat, Adobe, Knak, CMS) with zero integration.
* **Friction**: 334 hours/year spent by Language Champions manually reviewing every asset due to invisible quality gates.

---

## Slide 3: Solution Architecture Overview
### Python FastAPI Backend + Next.js 14 Frontend

```
[Ingestion MCP Stub] ──> [TM & Glossary Skill] ──> [Translation Agent]
                                                          │
                                                          ▼
[CMS / Staging] <── [Confidence Router] <── [AI Quality Gate Evaluator]
```

---

## Slide 4: AI Quality Gate & HITL Routing
* **Accuracy (35%)**, **Glossary/DNT (30%)**, **Brand Tone (20%)**, **HTML Tag Integrity (15%)**.
* **Thresholds**: $\ge 88\%$ Auto-Pass, $70\%-87\%$ HITL Review, $< 70\%$ Reject.
* **Hard DNT Rule**: Any DNT violation forces HITL Review or Re-translation regardless of score.

---

## Slide 5: Financial Model & TCO
* **Annual LLM API Cost**: $5.04 / year (2,800 runs @ 650 tokens/run).
* **Total Annual OPEX**: $4,205 / year (including LLM API, hosting, and maintenance).
* **Direct Labor Savings**: $19,890 / year (234 hours saved @ $85/hr).
* **Return on Investment**: **373% Net Direct ROI** with a **2.5-month payback period**.
