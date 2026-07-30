import pytest
from app.resilience.html_sanitizer import HTMLSanitizer
from app.resilience.idempotency import IdempotencyManager
from app.services.eval_benchmark_service import EvalBenchmarkService
from app.services.telemetry_service import TelemetryService

def test_html_xss_sanitization():
    unsafe_html = "<h1>Title</h1><script>alert('XSS')</script><p onload='malicious()'>Content</p>"
    clean_html = HTMLSanitizer.sanitize(unsafe_html)
    assert "<script>" not in clean_html
    assert "onload" not in clean_html
    assert "<h1>Title</h1>" in clean_html
    assert "<p>Content</p>" in clean_html

def test_idempotency_manager():
    manager = IdempotencyManager()
    key = "idemp-key-12345"
    response_payload = {"status": "SUCCESS", "translated_html": "<p>Hola</p>"}
    
    assert manager.check_key(key) is None
    manager.record_key(key, response_payload)
    cached = manager.check_key(key)
    assert cached is not None
    assert cached["status"] == "SUCCESS"

def test_evaluator_alignment_cohens_kappa():
    human_reviews = [True, True, False, True, False]
    ai_decisions  = [True, True, False, True, False]
    kappa = EvalBenchmarkService.calculate_cohen_kappa(human_reviews, ai_decisions)
    assert kappa == 1.0  # Perfect agreement

def test_telemetry_trace_generation():
    trace = TelemetryService.start_trace("JOB-999", "sample.html")
    TelemetryService.add_span(trace, "llm_translation", 45.2, {"model": "gemini-2.5-flash"})
    final_trace = TelemetryService.end_trace(trace)
    
    assert final_trace["job_id"] == "JOB-999"
    assert final_trace["prompt_version"] == "v1.3.0-enterprise"
    assert len(final_trace["spans"]) == 1
    assert final_trace["total_latency_ms"] >= 0.0
