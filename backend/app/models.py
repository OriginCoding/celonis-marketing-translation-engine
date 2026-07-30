from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class GlossaryItem(BaseModel):
    term_en: str
    term_es: str
    dnt: bool = False
    notes: Optional[str] = ""

class TMSegment(BaseModel):
    id: str = "tm-1"
    source_en: str
    target_es: str
    domain: str = "marketing"
    quality_score: float = 1.0
    last_used: str = "2026-07-26"

class TranslationJobRequest(BaseModel):
    ticket_id: str = "LOC-4082"
    source_tool: str = "Jira"
    asset_filename: str = "context_model_page.html"
    source_language: str = "en"
    target_language: str = "es"
    campaign_name: str = "Enterprise AI Operational Clarity 2026"
    inject_error: bool = False
    threshold_auto_pass: float = 88.0
    threshold_hitl: float = 70.0

class QualityMetricBreakdown(BaseModel):
    accuracy: float = Field(..., ge=0.0, le=100.0)
    glossary_dnt: float = Field(..., ge=0.0, le=100.0)
    brand_tone: float = Field(..., ge=0.0, le=100.0)
    html_structure: float = Field(..., ge=0.0, le=100.0)
    overall_confidence: float = Field(..., ge=0.0, le=100.0)
    dnt_violations: List[str] = Field(default_factory=list)
    glossary_violations: List[str] = Field(default_factory=list)
    formatting_issues: List[str] = Field(default_factory=list)
    critique_feedback: str = ""

class RoutingDecision(BaseModel):
    status: str  # "AUTO_PASS", "HITL_REVIEW", "REJECT_RETRANSLATE"
    threshold_auto_pass: float
    threshold_hitl: float
    reasoning: str
    assigned_to: str
    recommended_action: str

class TraceEvent(BaseModel):
    id: str
    timestamp: str
    stage: str
    agent_name: str
    tool_name: Optional[str] = None
    message: str
    status: str  # "INFO", "SUCCESS", "WARNING", "ERROR"
    tokens_used: Optional[int] = 0
    latency_ms: Optional[float] = 0.0

class PipelineResult(BaseModel):
    job_id: str
    asset_name: str
    source_html: str
    translated_html: str
    quality_score: QualityMetricBreakdown
    routing_decision: RoutingDecision
    trace_events: List[TraceEvent]
    execution_time_ms: float
    active_glossary_count: int
    active_tm_count: int
    self_correction_passes: int
