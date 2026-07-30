import os
import pytest
from app.agents.orchestrator import Orchestrator
from app.agents.quality_gate import QualityGateJudge
from app.models import TranslationJobRequest
from app.api.hitl import record_human_review_decision, ReviewActionRequest
from app.core.security import UserProfile
from app.services.file_storage_service import FileStorageService

orchestrator = Orchestrator()

def test_hard_test_1_dnt_brand_tampering():
    filepath = "hard_test_1_dnt_brand_tampering.html"
    assert os.path.exists(filepath), f"File {filepath} does not exist!"
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    req = TranslationJobRequest(
        ticket_id="TEST-HARD-1",
        asset_filename="hard_test_1_dnt_brand_tampering.html",
        inject_error=True
    )
    res = orchestrator.run_pipeline(req, content)
    
    assert res.quality_score.glossary_dnt <= 50.0
    assert res.quality_score.overall_confidence < 70.0
    assert res.routing_decision.status in ["HITL_REVIEW", "REJECT_RETRANSLATE"]

def test_hard_test_2_nested_dom_structure():
    filepath = "hard_test_2_nested_dom_structure.html"
    assert os.path.exists(filepath)
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    req = TranslationJobRequest(
        ticket_id="TEST-HARD-2",
        asset_filename="hard_test_2_nested_dom_structure.html",
        inject_error=False
    )
    res = orchestrator.run_pipeline(req, content)
    
    assert res.quality_score.accuracy > 0
    assert res.translated_html is not None

def test_hard_test_3_loanwords_and_untranslated():
    filepath = "hard_test_3_loanwords_and_untranslated.html"
    assert os.path.exists(filepath)
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    req = TranslationJobRequest(
        ticket_id="TEST-HARD-3",
        asset_filename="hard_test_3_loanwords_and_untranslated.html",
        inject_error=False
    )
    res = orchestrator.run_pipeline(req, content)
    
    assert res.quality_score.overall_confidence > 0

def test_hard_test_4_adversarial_injection():
    filepath = "hard_test_4_adversarial_injection.html"
    assert os.path.exists(filepath)
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    req = TranslationJobRequest(
        ticket_id="TEST-HARD-4",
        asset_filename="hard_test_4_adversarial_injection.html",
        inject_error=True
    )
    res = orchestrator.run_pipeline(req, content)
    
    assert res.quality_score.overall_confidence < 88.0

def test_grounding_and_hallucination_verifier():
    source_html = "<h1>Save 334 Hours & 373% ROI</h1><a href='/demo'>Demo</a>"
    # Target HTML missing number 373 and missing link /demo
    translated_html = "<h1>Ahorre 334 horas y ROI increible</h1><a>Demo</a>"
    
    issues = QualityGateJudge._verify_grounded_facts(source_html, translated_html)
    assert len(issues) == 2
    assert any("373" in issue for issue in issues)
    assert any("/demo" in issue for issue in issues)

def test_human_review_score_logging_accuracy():
    mock_user = UserProfile(user_id="USR-999", email="test.champion@celonis.com", role="Champion")
    
    req_reject = ReviewActionRequest(
        job_id="JOB-TEST-REJECT",
        asset_name="hard_test_1_dnt_brand_tampering.html",
        action="REJECT",
        reviewer="Test Lead",
        reviewer_notes="DNT violation detected.",
        overall_score=59.2
    )
    res_reject = record_human_review_decision(req_reject, mock_user)
    assert res_reject["status"] == "REJECTED"
    assert res_reject["audit_entry"].overall_score == 59.2
    assert res_reject["audit_entry"].action == "CHAMPION_REJECTED"

    req_approve = ReviewActionRequest(
        job_id="JOB-TEST-APPROVE",
        asset_name="context_model_page.html",
        action="APPROVE",
        reviewer="Test Lead",
        reviewer_notes="Copy verified.",
        overall_score=97.5
    )
    res_approve = record_human_review_decision(req_approve, mock_user)
    assert res_approve["status"] == "APPROVED"
    assert res_approve["audit_entry"].overall_score == 97.5
    assert res_approve["audit_entry"].action == "CHAMPION_APPROVED"

def test_file_storage_repository_saving_and_retrieval():
    storage = FileStorageService(base_dir="storage")
    saved = storage.save_job_files(
        job_id="JOB-UNIT-TEST-123",
        asset_name="test_page.html",
        source_html="<h1>Source</h1>",
        translated_html="<h1>Translated</h1>"
    )
    assert os.path.exists(saved["source_path"])
    assert os.path.exists(saved["translated_path"])
    
    src_content = storage.get_file_content("JOB-UNIT-TEST-123", "source")
    out_content = storage.get_file_content("JOB-UNIT-TEST-123", "output")
    
    assert src_content == "<h1>Source</h1>"
    assert out_content == "<h1>Translated</h1>"
