import pytest
from app.models import TranslationJobRequest
from app.agents.orchestrator import Orchestrator
from app.services.glossary_service import GlossaryService
from app.services.tm_service import TMService
from app.resilience.dnt_verifier import DntVerifier
from app.resilience.html_guardrail import HtmlGuardrail

def test_glossary_service():
    service = GlossaryService()
    items = service.get_all()
    dnt_terms = [item.term_en for item in service.get_dnt_terms()]
    assert len(items) >= 30
    assert "Celonis" in dnt_terms
    assert "Agent C" in dnt_terms
    assert "Celonis Process Intelligence" in dnt_terms

def test_tm_service():
    service = TMService()
    match = service.search("Talk to a Celonis expert")
    assert match is not None
    assert match[0].target_es == "Hable con un experto de Celonis"

def test_dnt_verifier():
    service = GlossaryService()
    glossary = service.get_all()
    src = "<p>Celonis Agent C Process Intelligence</p>"
    trans_valid = "<p>Celonis Agent C Process Intelligence</p>"
    trans_corrupt = "<p>Celonis Agente C Inteligencia de Procesos</p>"

    dnt_v1, g_v1, score1 = DntVerifier.verify(src, trans_valid, glossary)
    assert len(dnt_v1) == 0
    assert score1 == 100.0

    dnt_v2, g_v2, score2 = DntVerifier.verify(src, trans_corrupt, glossary)
    assert len(dnt_v2) > 0
    assert score2 < 100.0

def test_orchestrator_pipeline():
    orchestrator = Orchestrator()
    req = TranslationJobRequest(asset_filename="context_model_page.html")
    sample_html = "<h1>Give Enterprise AI operational clarity</h1><p>The Celonis Context Model provides operational context...</p>"
    
    result = orchestrator.run_pipeline(req, sample_html)
    assert result.quality_score.overall_confidence >= 85.0
    assert result.routing_decision.status in ["AUTO_PASS", "HITL_REVIEW"]
