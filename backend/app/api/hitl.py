from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.services.audit_service import AuditService
from app.core.security import get_current_user, UserProfile
from app.workers.celery_app import async_worker
from app.agents.orchestrator import Orchestrator
from app.models import TranslationJobRequest

router = APIRouter(prefix="/api/hitl", tags=["HITL Governance"])
audit_service = AuditService()
orchestrator = Orchestrator()

class ReviewActionRequest(BaseModel):
    job_id: str
    asset_name: Optional[str] = "marketing_document.html"
    action: str  # APPROVE or REJECT
    reviewer: Optional[str] = "Language Champion Lead"
    reviewer_notes: Optional[str] = ""
    overall_score: Optional[float] = None
    dnt_violations_count: Optional[int] = 0

class SelfCorrectRequest(BaseModel):
    asset_name: str
    source_html: Optional[str] = ""
    critique_feedback: Optional[str] = ""
    current_pass: Optional[int] = 1

@router.post("/review")
def record_human_review_decision(
    payload: ReviewActionRequest,
    current_user: UserProfile = Depends(get_current_user)
):
    reviewer_name = f"{current_user.email} ({payload.reviewer or 'Language Champion'})"
    
    if payload.action == "APPROVE":
        audit_entry = audit_service.record_event(
            job_id=payload.job_id,
            asset_name=payload.asset_name or "marketing_document.html",
            action="CHAMPION_APPROVED",
            reviewer=reviewer_name,
            reviewer_notes=payload.reviewer_notes or "Verified Spanish phrasing. Approved for production publishing.",
            overall_score=payload.overall_score if payload.overall_score is not None else 97.5,
            dnt_violations_count=payload.dnt_violations_count or 0,
            destination="Staging CMS & Translation Memory Ingestion"
        )
        return {
            "status": "APPROVED",
            "message": "Asset approved by Language Champion and logged to persistent audit database.",
            "audit_entry": audit_entry,
            "sso_user": current_user
        }
    else:
        audit_entry = audit_service.record_event(
            job_id=payload.job_id,
            asset_name=payload.asset_name or "marketing_document.html",
            action="CHAMPION_REJECTED",
            reviewer=reviewer_name,
            reviewer_notes=payload.reviewer_notes or "Rejected due to phrasing or DNT term alteration. Returned for re-translation.",
            overall_score=payload.overall_score if payload.overall_score is not None else 30.0,
            dnt_violations_count=payload.dnt_violations_count or 2,
            destination="Translation Agent Reflexion Feedback Loop"
        )
        return {
            "status": "REJECTED",
            "message": "Asset rejected and returned to AI translation feedback loop with critique notes.",
            "audit_entry": audit_entry,
            "sso_user": current_user
        }

@router.post("/self_correct")
def execute_agent_self_correction(payload: SelfCorrectRequest):
    """
    Reflexion Loop with Explicit Pass Tracking (Pass 1 -> Pass 2 -> Pass 3).
    Takes a rejected document, analyzes critique feedback, re-prompts TranslationAgent,
    increments pass counter, and logs iteration to persistent audit ledger.
    """
    next_pass_num = (payload.current_pass or 0) + 1

    req = TranslationJobRequest(
        ticket_id=f"REFLEXION-PASS-{next_pass_num}",
        asset_filename=payload.asset_name,
        inject_error=False
    )
    
    # Run pipeline with clean DNT enforcement instructions and critique feedback ingestion
    result = orchestrator.run_pipeline(
        request=req,
        sample_html=payload.source_html or None,
        is_reflexion=True,
        critique_feedback=payload.critique_feedback
    )
    result.self_correction_passes = next_pass_num

    # Record Dynamic Reflexion Iteration Event in Audit Store
    audit_service.record_event(
        job_id=result.job_id,
        asset_name=payload.asset_name,
        action=f"REFLEXION_PASS_{next_pass_num}_" + ("AUTO_PASS" if result.routing_decision.status == "AUTO_PASS" else "REVIEW_REQUIRED"),
        reviewer=f"AI Agent Reflexion Loop (Pass #{next_pass_num})",
        reviewer_notes=f"[Reflexion Pass #{next_pass_num}] {result.quality_score.critique_feedback}",
        overall_score=result.quality_score.overall_confidence,
        dnt_violations_count=len(result.quality_score.dnt_violations),
        destination="Staging CMS / TM Ingestion" if result.routing_decision.status == "AUTO_PASS" else f"Language Champion HITL Review Queue (Pass #{next_pass_num})"
    )

    return result

@router.post("/async_batch")
def submit_async_batch_job(
    payload: Dict[str, Any],
    current_user: UserProfile = Depends(get_current_user)
):
    job_id = async_worker.enqueue_job("batch_translation_pipeline", payload)
    return {
        "status": "202_ACCEPTED",
        "message": "Batch translation payload enqueued to Celery async worker queue.",
        "job_id": job_id,
        "submitted_by": current_user.email
    }

@router.get("/async_job/{job_id}")
def check_async_job_status(job_id: str):
    return async_worker.get_job_status(job_id)

@router.get("/audit_logs")
def fetch_audit_history_logs():
    return {
        "total_records": len(audit_service.get_all_logs()),
        "log_filepath": "backend/logs/audit_history.json",
        "audit_records": audit_service.get_all_logs()
    }
