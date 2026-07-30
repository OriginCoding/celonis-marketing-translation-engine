from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.models import TranslationJobRequest, PipelineResult
from app.agents.orchestrator import Orchestrator
from app.workers.celery_app import async_worker
import time

router = APIRouter(prefix="/api/agent", tags=["Agent Pipeline"])
orchestrator = Orchestrator()

class UploadContentRequest(BaseModel):
    filename: str
    html_content: str
    inject_error: Optional[bool] = False

class BatchUploadRequest(BaseModel):
    files: List[UploadContentRequest]

@router.post("/process", response_model=PipelineResult)
def process_translation_job(request: TranslationJobRequest):
    result = orchestrator.run_pipeline(request)
    return result

@router.post("/upload_content", response_model=PipelineResult)
def upload_content_and_process(payload: UploadContentRequest):
    if not payload.html_content or not payload.html_content.strip():
        raise HTTPException(status_code=400, detail="HTML content cannot be empty.")
    
    request = TranslationJobRequest(
        ticket_id=f"UPLOAD-{int(time.time())}",
        asset_filename=payload.filename or "uploaded_document.html",
        inject_error=payload.inject_error or False
    )
    
    result = orchestrator.run_pipeline(request, payload.html_content)
    return result

@router.post("/batch_process")
def batch_upload_async_process(payload: BatchUploadRequest):
    if not payload.files or len(payload.files) == 0:
        raise HTTPException(status_code=400, detail="No files provided for batch processing.")
    
    job_id = async_worker.enqueue_job(
        task_name="batch_multi_file_pipeline",
        payload={
            "file_count": len(payload.files),
            "filenames": [f.filename for f in payload.files]
        }
    )
    
    # Process files and log audit entries for each file in background queue
    results = []
    for item in payload.files:
        request = TranslationJobRequest(
            ticket_id=f"BATCH-{int(time.time())}",
            asset_filename=item.filename,
            inject_error=item.inject_error or False
        )
        res = orchestrator.run_pipeline(request, item.html_content)
        results.append({
            "filename": item.filename,
            "job_id": res.job_id,
            "overall_score": res.quality_score.overall_confidence,
            "status": res.routing_decision.status
        })
        
    return {
        "status": "202_ACCEPTED",
        "message": f"Successfully enqueued and processed {len(payload.files)} files into Celery async worker pool.",
        "async_job_id": job_id,
        "batch_summary": results
    }
