export interface PipelineRequest {
  ticket_id?: string;
  source_tool?: string;
  asset_filename?: string;
  inject_error?: boolean;
  threshold_auto_pass?: number;
  threshold_hitl?: number;
}

export interface PipelineResponse {
  job_id: string;
  asset_name: string;
  source_html: string;
  translated_html: string;
  quality_score: {
    accuracy: number;
    glossary_dnt: number;
    brand_tone: number;
    html_structure: number;
    overall_confidence: number;
    dnt_violations: string[];
    glossary_violations: string[];
    formatting_issues: string[];
    critique_feedback: string;
  };
  routing_decision: {
    status: "AUTO_PASS" | "HITL_REVIEW" | "REJECT_RETRANSLATE";
    threshold_auto_pass: number;
    threshold_hitl: number;
    reasoning: string;
    assigned_to: string;
    recommended_action: string;
  };
  trace_events: Array<{
    id: string;
    timestamp: string;
    stage: string;
    agent_name: string;
    tool_name?: string;
    message: string;
    status: "INFO" | "SUCCESS" | "WARNING" | "ERROR";
    tokens_used?: number;
    latency_ms?: number;
  }>;
  execution_time_ms: number;
  active_glossary_count: number;
  active_tm_count: number;
  self_correction_passes: number;
}

const FASTAPI_BASE_URL = "http://localhost:8000";

export async function runAgentPipeline(req: PipelineRequest): Promise<PipelineResponse> {
  try {
    const res = await fetch(`${FASTAPI_BASE_URL}/api/agent/process`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ticket_id: req.ticket_id || "LOC-4082",
        source_tool: req.source_tool || "Jira",
        asset_filename: req.asset_filename || "context_model_page.html",
        inject_error: req.inject_error || false,
        threshold_auto_pass: req.threshold_auto_pass || 88.0,
        threshold_hitl: req.threshold_hitl || 70.0,
      }),
    });

    if (!res.ok) {
      throw new Error(`FastAPI returned status ${res.status}`);
    }

    return await res.json();
  } catch (err) {
    console.warn("FastAPI offline, fallback to built-in local client response", err);
    // Offline fallback generator
    return getOfflineMockResponse(req);
  }
}

function getOfflineMockResponse(req: PipelineRequest): PipelineResponse {
  const isError = req.inject_error || false;
  return {
    job_id: `JOB-LOC-4082-${Date.now()}`,
    asset_name: req.asset_filename || "context_model_page.html",
    source_html: `<h1>Give Enterprise AI operational clarity</h1><p>The Celonis Context Model provides operational context through a dynamic, real-time digital twin...</p><a href="/contact">Talk to a Celonis expert</a>`,
    translated_html: isError
      ? `<h1>Aporte claridad operativa a la IA empresarial</h1><p>El Celonis Context Model proporciona contexto operativo...</p><a href="/contact">Hable con un experto de Celonis</a><p>Agente C (Corrupted DNT)</p>`
      : `<h1>Aporte claridad operativa a la IA empresarial</h1><p>El Celonis Context Model proporciona contexto operativo mediante un gemelo digital dinámico...</p><a href="/contact">Hable con un experto de Celonis</a>`,
    quality_score: {
      accuracy: 95.0,
      glossary_dnt: isError ? 50.0 : 100.0,
      brand_tone: 96.0,
      html_structure: 100.0,
      overall_confidence: isError ? 68.5 : 97.2,
      dnt_violations: isError ? ["DNT term 'Agent C' was altered to 'Agente C'"] : [],
      glossary_violations: [],
      formatting_issues: [],
      critique_feedback: isError
        ? "CRITICAL: 1 Do-Not-Translate (DNT) term altered."
        : "PASS: Asset passed all AI Quality Gate checks with zero DNT violations.",
    },
    routing_decision: {
      status: isError ? "HITL_REVIEW" : "AUTO_PASS",
      threshold_auto_pass: req.threshold_auto_pass || 88.0,
      threshold_hitl: req.threshold_hitl || 70.0,
      reasoning: isError
        ? "Overridden to HITL Review due to critical DNT violation."
        : "Auto-Pass: Confidence score (97.2%) exceeds threshold (88.0%). Zero DNT violations.",
      assigned_to: isError
        ? "Language Champion (Spanish Team)"
        : "Automated CMS / Staging Pipeline",
      recommended_action: isError
        ? "Inspect pre-highlighted DNT alteration in review portal."
        : "Approve asset for staging deployment and ingest into Translation Memory.",
    },
    trace_events: [
      {
        id: "tr-1",
        timestamp: new Date().toISOString(),
        stage: "Ingestion",
        agent_name: "IngestionAgent",
        tool_name: "JiraMCP.fetchAsset",
        message: "Ingested brief LOC-4082 and HTML payload.",
        status: "INFO",
        tokens_used: 150,
        latency_ms: 45.0,
      },
      {
        id: "tr-2",
        timestamp: new Date().toISOString(),
        stage: "Knowledge Grounding",
        agent_name: "GlossaryRAGAgent",
        tool_name: "TMVectorRAG.search",
        message: "Matched 30 glossary DNT terms and 1 TM segment.",
        status: "SUCCESS",
        tokens_used: 320,
        latency_ms: 62.0,
      },
      {
        id: "tr-3",
        timestamp: new Date().toISOString(),
        stage: "Translation",
        agent_name: "TranslationAgent",
        tool_name: "GeminiFreeLLM.generateText",
        message: "Generated Spanish HTML preserving DOM structure and DNT terms.",
        status: isError ? "WARNING" : "SUCCESS",
        tokens_used: 950,
        latency_ms: 420.0,
      },
      {
        id: "tr-4",
        timestamp: new Date().toISOString(),
        stage: "Quality Gate",
        agent_name: "QualityGateAgent",
        tool_name: "QualityGateJudge.evaluate",
        message: `Evaluated metrics (Confidence: ${isError ? 68.5 : 97.2}%).`,
        status: isError ? "WARNING" : "SUCCESS",
        tokens_used: 400,
        latency_ms: 180.0,
      },
    ],
    execution_time_ms: 707.0,
    active_glossary_count: 30,
    active_tm_count: 4,
    self_correction_passes: isError ? 1 : 0,
  };
}
