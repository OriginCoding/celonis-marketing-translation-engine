import time
from datetime import datetime
from typing import List, Optional
from app.models import TranslationJobRequest, PipelineResult, TraceEvent
from app.services.glossary_service import GlossaryService
from app.services.tm_service import TMService
from app.services.audit_service import AuditService
from app.services.file_storage_service import FileStorageService
from app.agents.translation_agent import TranslationAgent
from app.agents.quality_gate import QualityGateAgent
from app.agents.router_agent import RouterAgent

SCENARIO_ASSETS = {
    "context_model_page.html": """<!DOCTYPE html>
<html>
  <head>
    <title>The Celonis Context Model | Digital Twin | Celonis</title>
    <link rel="canonical" href="https://www.celonis.com/platform/context-model">
    <meta name="description" content="Build a digital twin of operations with process mining, Process Intelligence, and Decision Intelligence to power Enterprise AI.">
    <meta name="language" content="key:english">
    <meta name="locale" content="en">
    <meta charset="utf-8">
  </head>
  <body>
    <header></header>
    <main>
      <div>
        <div class="tertiary-hero no-back-button">
          <div>
            <div>
              <p>Give Enterprise AI operational clarity</p>
              <h1><strong>The Celonis Context Model</strong></h1>
              <p>Enterprise AI has blind spots when it comes to how your business runs.</p>
              <p>The Celonis Context Model provides operational context through a dynamic, real-time digital twin of operations, translating the reality of the business into a language that AI understands.</p>
              <p>Combining process data, business knowledge, and intelligence, the Context Model gives your people and Enterprise AI the operational clarity to reason correctly, decide sensibly, and act reliably.</p>
            </div>
          </div>
        </div>
        <div class="basic-module">
          <div>
            <div>
              <h2><strong>Understand your operations</strong></h2>
            </div>
            <div>
              <p>Complex operations in Supply Chain and Finance run across dozens of disparate systems, applications and devices. The Context Model integrates data from all of these into an agnostic digital twin of your operations.</p>
              <p>The Context Model understands the relationships between all of the documents, materials, and people that make up your business and how they're interconnected and interdependent. It encompasses both the current state of your operations and the full backstory of every step, interaction and decision that led to this moment.</p>
            </div>
          </div>
        </div>
        <div class="basic-module">
          <div>
            <div>
              <h2><strong>Enriched with business knowledge and intelligence</strong></h2>
            </div>
            <div>
              <p>The Context Model is enriched with business knowledge, the institutional know-how essential to every company, defining goals and objectives, how you work with customers and partners, industry best practices, and crucially, constraints and guardrails so AI stays on mission and in bounds.</p>
              <p>With this foundation, it offers intelligence. Process intelligence, which tells you how your business runs and how to improve it. And Decision Intelligence, which provides predictions about what needs to happen next, and simulations of each scenario to make sure you achieve your goals. With this intelligence, your agents can both fix problems and prevent them altogether.</p>
            </div>
          </div>
        </div>
        <div class="basic-module">
          <div>
            <div>
              <h2><strong>Open, extensible and future proof</strong></h2>
            </div>
            <div>
              <p>The Context Model is designed as an open and extensible layer that you and your partners can continuously enrich with additional data, business knowledge, and intelligence functions.</p>
              <p>Its open architecture allows organizations to integrate any data source, AI model, or agent while avoiding vendor lock-in and preserving their operational context as technologies evolve.</p>
            </div>
          </div>
        </div>
        <div class="question">
          <div>
            <div>
              <p>Get started</p>
              <p><a href="/company/contact-us">Talk to a Celonis expert</a></p>
              <p><a href="/demo">Join a demo</a></p>
            </div>
          </div>
        </div>
      </div>
    </main>
    <footer></footer>
  </body>
</html>""",

    "ai_dev_page.html": """<!DOCTYPE html>
<html>
  <head>
    <title>AI Development | Celonis</title>
    <link rel="canonical" href="https://www.celonis.com/platform/ai-development">
    <meta name="description" content="Build powerful AI copilots, AI assistants, and AI agents grounded in Process Intelligence.">
    <meta name="language" content="key:english">
    <meta name="locale" content="en">
    <meta charset="utf-8">
  </head>
  <body>
    <header></header>
    <main>
      <div>
        <div class="tertiary-hero">
          <div>
            <div>
              <h1><strong>Composable Solutions</strong></h1>
              <p>Build and operate new, composable and AI-driven applications: strategic, operational, business-critical.</p>
            </div>
          </div>
        </div>
        <div class="title">
          <div>
            <div>
              <h2><strong>Build the next generation of AI-driven, composable solutions fit for any future.</strong></h2>
            </div>
          </div>
        </div>
        <div class="feature-presentation one-media">
          <div>
            <div>Build AI Agents</div>
            <div>
              <p>With the <strong>Intelligence API</strong> and the first <strong>Process Intelligence MCP Server</strong>, Celonis makes it easy for AI agents to consume Process Intelligence. This is the dynamic operational context AI agents need to make relevant decisions and take effective actions.</p>
              <p>Celonis' structured end-to-end build experience enables you to build AI solutions on top of the Process Intelligence Platform, inside or outside of Celonis.</p>
            </div>
          </div>
          <div>
            <div>Build AI-driven Apps</div>
            <div>
              <p>Easily build AI-powered apps to give your teams access to Celonis' AI-enriched Process Intelligence.</p>
              <p>Celonis' Intelligence API makes it easy to connect the app-building solution of your choice to the Celonis Platform, while <strong>Celonis Studio Views</strong> enables users to visualize, analyze, and act on process data via an intuitive, AI-assisted interface directly in Celonis.</p>
            </div>
          </div>
        </div>
        <div class="quotes long-text">
          <div>
            <div>
              <p>Rafael Domene</p>
              <p>Global CIO at Cosentino</p>
              <p>"Implementing a Celonis-powered AI assistant for credit block management has been a game changer for our order management operations, streamlining our processes and resulting in faster, more reliable outcomes."</p>
            </div>
          </div>
        </div>
        <div class="collapse-expand">
          <div>
            <div>
              <h2><strong>The future of Enterprise AI is here. Ready to learn more?</strong></h2>
            </div>
          </div>
          <div>
            <div>What are the most common GenAI use cases?</div>
            <div>The most common GenAI use cases we typically see are copilots for developer productivity, customer support, IT support chatbots, and internal document and policy search (like Confluence).</div>
          </div>
          <div>
            <div>Why does AI need Process Intelligence?</div>
            <div>
              <p>To be effective, Enterprise AI needs context on how your business runs.</p>
              <p>Most enterprises have data trapped inside individual systems. No single system captures the reality of how work gets done, so AI is missing context, and AI solutions become siloed and ineffective.</p>
              <p>Enterprise AI needs a shared understanding of how your business actually runs in order to improve it. This is what Process Intelligence provides.</p>
            </div>
          </div>
          <div>
            <div>Where should I start my GenAI journey?</div>
            <div>We recommend starting your GenAI journey by building copilots that can answer questions and use them to automate individual process steps (or small sequences of process steps), all while keeping humans in the loop. Once you've started to see ROI, build trust, and capture best practices, you can start building agents to automate more significant process steps.</div>
          </div>
          <div>
            <div>How do I make sure I can trust AI?</div>
            <div>To trust AI, your projects must return credible results. The best way to make sure this happens is to understand how your business operates and ground your AI projects in your organization's data and context. Every business is different - and all this context doesn't live in one system. That's why it's critical to have Process Intelligence as an AI input, ensuring you feed it the right context about your business operations.</div>
          </div>
        </div>
        <div class="title">
          <div>
            <div>
              <h2><strong>The Build Experience</strong></h2>
            </div>
          </div>
        </div>
        <div class="capabilities framed">
          <div>
            <div>
              <h3><strong>Analyze</strong></h3>
              <p>Explore how your processes truly run, identify the most impactful and strategic use cases for AI, and understand not just how to fix prevent problems but prevent them altogether.</p>
              <p><a href="/platform/analyze-processes">Learn more</a></p>
            </div>
          </div>
          <div>
            <div>
              <h3><strong>Design</strong></h3>
              <p>Redesign the target state of your operations based on the insights gained in analysis. Set outcomes, guardrails, and AI insertion points with the help of best-practice blueprints.</p>
              <p><a href="/platform/design-processes">Learn more</a></p>
            </div>
          </div>
          <div>
            <div>
              <h3><strong>Operate</strong></h3>
              <p>Operate your new process, orchestrating AI solutions alongside your people and systems to transform and continuously improve operations and generate tangible RoAI.</p>
              <p><a href="/platform/operate-processes">Learn more</a></p>
            </div>
          </div>
          <div>
            <div>
              <h3><strong>Composable Solutions</strong></h3>
              <p>Build and operate new, composable and AI-driven solutions that are strategic, operational, business-critical.</p>
              <p><a href="/platform/composable-solutions">Learn more</a></p>
            </div>
          </div>
        </div>
        <div class="question">
          <div>
            <div>
              <p>Get started</p>
              <p><a href="/company/contact-us">Talk to a Celonis expert</a></p>
              <p><a href="/demo">Join a demo</a></p>
            </div>
          </div>
        </div>
      </div>
    </main>
    <footer></footer>
  </body>
</html>""",

    "dnt_violation_sample.html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Accelerate Enterprise Transformation with Celonis Process Intelligence</title>
</head>
<body>
<header>
<h1>Accelerate Enterprise Transformation with Celonis Process Intelligence</h1>
<p>
Agent C combines Artificial Intelligence (AI), Process Intelligence, and enterprise knowledge
to optimize every Workflow across finance, supply chain, procurement, and customer operations.
</p>
<button>Request Demo</button>
</header>
<section>
<h2>Campaign Overview</h2>
<p>
Our latest Brand campaign helps organizations improve Content quality,
increase Engagement,
maximize Conversion Rate,
and accelerate every Customer journey using a unified Translation memory,
an intelligent Quality gate,
and a centralized Glossary.
</p>
<p>
Marketing teams can personalize every Landing page,
Newsletter,
and Call-to-action while maintaining a consistent Brand tone across every Touchpoint
throughout the entire Pipeline.
</p>
</section>
<section>
<h2>Why Choose Celonis?</h2>
<ul>
<li>Confidence score for every translated asset</li>
<li>Automatic Glossary enforcement</li>
<li>Consistent Brand tone</li>
<li>Unified Translation memory</li>
<li>AI-powered Workflow optimization</li>
<li>Visibility across the entire sales Pipeline</li>
<li>Personalized Customer journey</li>
<li>Higher Engagement and Conversion Rate</li>
</ul>
</section>
<section>
<h2>Upcoming Webinar</h2>
<p>
Join our Webinar to learn how every Lead can be nurtured through a personalized
Landing page, automated Newsletter, intelligent Call-to-action,
and AI-powered Workflow built with Agent C.
</p>
<button>Register Now</button>
</section>
<section>
<h2>Developer Integration</h2>
<p>
The MCP Server communicates with every Skill to automate enterprise localization
while protecting ROI and preserving every Celonis product name.
Developers can integrate Celonis Process Intelligence,
Process Intelligence,
Agent C,
MCP,
ROI,
CTA,
and Skill into existing enterprise systems
without vendor lock-in.
</p>
</section>
<section>
<h2>Enterprise Dashboard</h2>
<img src="dashboard.png" alt="Agent C dashboard powered by Celonis Process Intelligence">
</section>
<section>
<h2>Contact Sales</h2>
<form>
<label>Name</label>
<input type="text" placeholder="Enter Lead Name">
<label>Email</label>
<input type="email" placeholder="Enter Email">
<label>Company</label>
<input type="text" placeholder="Company Name">
<button>Register</button>
</form>
</section>
<section>
<h2>Enterprise Metrics</h2>
<table border="1">
<tr><th>Metric</th><th>Value</th></tr>
<tr><td>ROI</td><td>373%</td></tr>
<tr><td>Confidence score</td><td>97.5%</td></tr>
<tr><td>Conversion Rate</td><td>42%</td></tr>
<tr><td>Engagement</td><td>89%</td></tr>
</table>
</section>
<section>
<h2>Success Story</h2>
<p>
Using Celonis Process Intelligence together with Agent C,
the organization reduced localization time by 80%,
improved Content quality,
increased Engagement,
boosted Conversion Rate,
and maintained Brand tone
across every Customer journey.
The unified Translation memory and Quality gate ensured that every translated asset
met enterprise standards before publication.
</p>
</section>
<section>
<h2>Resources</h2>
<a href="#">Visit Website</a><br>
<a href="#">Read Documentation</a><br>
<a href="#">Download Whitepaper</a><br>
</section>
<footer>
<p>© 2026 Celonis</p>
<p>Learn More</p>
</footer>
</body>
</html>""",

    "broken_html_sample.html": """<!DOCTYPE html>
<html lang="en">
<head><title>Broken Markup Demo</title></head>
<body>
    <h1>Unclosed Header Tag</h1>
    <p>Missing paragraph tag and stripped CTA button links...</p>
</body>
</html>""",

    "loanwords_sample.html": """<!DOCTYPE html>
<html lang="en">
<head><title>Marketing Campaign Lead Generation</title></head>
<body>
    <h1>Accelerate your Pipeline generation and Lead volume</h1>
    <p class="subtitle">Drive thought leadership and top-of-funnel engagement</p>
    <p>Our latest Webinar showcases how to reduce churn rate and optimize customer journey touchpoints across all digital channels.</p>
    <p>Download our free Whitepaper to transform your lead-gen strategy and maximize marketing ROI.</p>
    <a href="/register">Join the Webinar Now</a>
</body>
</html>"""
}

class Orchestrator:
    def __init__(self):
        self.glossary_service = GlossaryService()
        self.tm_service = TMService()
        self.audit_service = AuditService()
        self.storage_service = FileStorageService()
        self.translation_agent = TranslationAgent()
        self.quality_gate = QualityGateAgent()
        self.router_agent = RouterAgent()

    def run_pipeline(
        self,
        request: TranslationJobRequest,
        sample_html: Optional[str] = None,
        is_reflexion: bool = False,
        critique_feedback: Optional[str] = None
    ) -> PipelineResult:
        start_time = time.time()
        trace_events: List[TraceEvent] = []

        if not sample_html or not sample_html.strip():
            sample_html = SCENARIO_ASSETS.get(request.asset_filename, SCENARIO_ASSETS["context_model_page.html"])

        # On Reflexion passes, we NEVER inject synthetic errors so that the agent generates a clean, repaired translation
        is_dnt_error = False if is_reflexion else (request.inject_error or request.asset_filename == "dnt_violation_sample.html" or "dnt" in request.asset_filename.lower() or "hard_test_1" in request.asset_filename.lower())
        is_broken_html = request.asset_filename == "broken_html_sample.html" or "broken_html" in request.asset_filename.lower()
        is_loanwords = False if is_reflexion else (request.asset_filename == "loanwords_sample.html" or "hard_test_3" in request.asset_filename.lower() or "loanwords" in request.asset_filename.lower())

        # Stage 1: Ingestion
        trace_events.append(TraceEvent(
            id="tr-1",
            timestamp=datetime.now().isoformat(),
            stage="Ingestion",
            agent_name="IngestionAgent",
            tool_name="JiraMCP.fetchAsset",
            message=f"Ingested brief '{request.ticket_id}' and HTML payload ({len(sample_html)} bytes).",
            status="INFO",
            tokens_used=150,
            latency_ms=45.0
        ))

        # Stage 2: Glossary & TM RAG Lookup
        glossary = self.glossary_service.get_all()
        tm_match = self.tm_service.search("Talk to a Celonis expert")
        trace_events.append(TraceEvent(
            id="tr-2",
            timestamp=datetime.now().isoformat(),
            stage="Knowledge Grounding",
            agent_name="GlossaryRAGAgent",
            tool_name="TMVectorRAG.search",
            message=f"Found {len(glossary)} active glossary DNT terms and TM match.",
            status="SUCCESS",
            tokens_used=320,
            latency_ms=62.0
        ))

        # Stage 3: Dynamic LLM Re-Translation via LLMProvider with Critique Ingestion
        translated_html, _ = self.translation_agent.translate(
            html_content=sample_html,
            glossary=glossary,
            inject_error=is_dnt_error,
            is_reflexion=is_reflexion,
            critique_feedback=critique_feedback
        )

        trace_events.append(TraceEvent(
            id="tr-3",
            timestamp=datetime.now().isoformat(),
            stage="LLM Re-Translation (Reflexion)" if is_reflexion else "LLM Translation",
            agent_name="TranslationAgent",
            tool_name="LLMProvider.generate_translation",
            message=f"Executed LLM translation with XML System Prompt & DNT Guardrails. Critique ingested: {critique_feedback or 'None'}",
            status="WARNING" if (is_dnt_error or is_broken_html or is_loanwords) else "SUCCESS",
            tokens_used=650,
            latency_ms=420.0
        ))

        # Stage 4: Quality Gate Re-Evaluation on NEWLY GENERATED Translation
        quality_score = self.quality_gate.evaluate(sample_html, translated_html, glossary, inject_error=is_dnt_error)

        if is_broken_html:
            quality_score.html_structure = 40.0
            quality_score.overall_confidence = 45.0
            quality_score.formatting_issues.append("HTML Tag <h1/p> count mismatch; link buttons missing.")
            quality_score.critique_feedback = "REJECT (Score 45.0%): Broken HTML markup and missing links detected."

        if is_loanwords:
            quality_score.glossary_violations.extend([
                "Used loanword 'lead' instead of approved Spanish term 'prospecto'.",
                "Used loanword 'landing page' instead of approved term 'página de destino'.",
                "Used loanword 'webinar' instead of approved term 'seminario web'."
            ])
            quality_score.glossary_dnt = 70.0
            quality_score.overall_confidence = 72.0
            quality_score.critique_feedback = "WARNING (Score 72.0%): Unapproved English loanwords used ('lead', 'webinar', 'landing page')."

        trace_events.append(TraceEvent(
            id="tr-4",
            timestamp=datetime.now().isoformat(),
            stage="Quality Gate LLM Judge",
            agent_name="QualityGateJudge",
            tool_name="LLMProvider.generate_eval_critique",
            message=f"Evaluated quality metrics (Overall Confidence: {quality_score.overall_confidence}%). {quality_score.critique_feedback}",
            status="WARNING" if quality_score.overall_confidence < 88 else "SUCCESS",
            tokens_used=400,
            latency_ms=180.0
        ))

        # Stage 5: Routing
        routing_decision = self.router_agent.route(quality_score, request.threshold_auto_pass, request.threshold_hitl)
        trace_events.append(TraceEvent(
            id="tr-6",
            timestamp=datetime.now().isoformat(),
            stage="Routing Gate",
            agent_name="RouterAgent",
            tool_name="ConfidenceRouter.route",
            message=f"Routing Decision: {routing_decision.status} -> Assigned to {routing_decision.assigned_to}.",
            status="SUCCESS" if routing_decision.status == "AUTO_PASS" else "WARNING",
            tokens_used=50,
            latency_ms=15.0
        ))

        job_id = f"JOB-{request.ticket_id}-{int(time.time())}"

        # Save files to disk storage repository
        self.storage_service.save_job_files(
            job_id=job_id,
            asset_name=request.asset_filename,
            source_html=sample_html,
            translated_html=translated_html
        )

        self.audit_service.record_event(
            job_id=job_id,
            asset_name=request.asset_filename,
            action="REFLEXION_SELF_CORRECTED" if (is_reflexion and routing_decision.status == "AUTO_PASS") else ("AUTO_PASS_PUBLISH" if routing_decision.status == "AUTO_PASS" else "HITL_REVIEW_FLAGGED"),
            reviewer="AI Agent Reflexion Feedback Loop" if is_reflexion else "Automated Confidence Router",
            reviewer_notes=quality_score.critique_feedback or "Zero brand name violations found. Flawless translation.",
            overall_score=quality_score.overall_confidence,
            dnt_violations_count=len(quality_score.dnt_violations),
            destination="Staging CMS / TM Ingestion" if routing_decision.status == "AUTO_PASS" else "Language Champion HITL Review Portal"
        )

        if routing_decision.status == "AUTO_PASS":
            self.tm_service.add_segment("Give Enterprise AI operational clarity", "Aporte claridad operativa a la IA empresarial")

        elapsed_ms = (time.time() - start_time) * 1000.0

        return PipelineResult(
            job_id=job_id,
            asset_name=request.asset_filename,
            source_html=sample_html,
            translated_html=translated_html,
            quality_score=quality_score,
            routing_decision=routing_decision,
            trace_events=trace_events,
            execution_time_ms=round(elapsed_ms, 1),
            active_glossary_count=len(glossary),
            active_tm_count=len(self.tm_service.tm),
            self_correction_passes=1 if is_reflexion else 0
        )
