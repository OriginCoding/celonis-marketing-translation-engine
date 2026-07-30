import os
import json
import time
import traceback
from datetime import datetime
from typing import List, Dict, Any
from pydantic import BaseModel

class AuditLogEntry(BaseModel):
    audit_id: str
    job_id: str
    asset_name: str
    timestamp: str
    action: str  # AUTO_PASS_PUBLISH, CHAMPION_APPROVED, CHAMPION_REJECTED, SYSTEM_ERROR, GUARDRAIL_FAILURE
    reviewer: str
    reviewer_notes: str
    overall_score: float
    dnt_violations_count: int
    destination: str
    error_details: str = ""

class AuditService:
    def __init__(self, log_path: str = "logs/audit_history.json"):
        self.log_path = log_path
        self.memory_logs: List[Dict[str, Any]] = []
        self._ensure_log_dir()
        self._load_existing_logs()

    def _ensure_log_dir(self):
        log_dir = os.path.dirname(self.log_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    def _load_existing_logs(self):
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, "r", encoding="utf-8") as f:
                    self.memory_logs = json.load(f)
            except Exception:
                self.memory_logs = []

    def record_event(
        self,
        job_id: str,
        asset_name: str,
        action: str,
        reviewer: str = "Automated Router / Language Champion",
        reviewer_notes: str = "",
        overall_score: float = 97.5,
        dnt_violations_count: int = 0,
        destination: str = "Staging CMS / Translation Memory",
        error_details: str = ""
    ) -> AuditLogEntry:
        entry = AuditLogEntry(
            audit_id=f"AUD-{int(time.time()*1000)}",
            job_id=job_id,
            asset_name=asset_name,
            timestamp=datetime.now().isoformat(),
            action=action,
            reviewer=reviewer,
            reviewer_notes=reviewer_notes,
            overall_score=overall_score,
            dnt_violations_count=dnt_violations_count,
            destination=destination,
            error_details=error_details
        )
        
        self.memory_logs.insert(0, entry.model_dump())
        
        # Persist to disk audit_history.json
        try:
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(self.memory_logs, f, indent=2)
        except Exception as e:
            print(f"Error persisting audit log: {e}")
            
        return entry

    def record_error_event(
        self,
        job_id: str,
        asset_name: str,
        error_message: str,
        exception_obj: Exception = None
    ) -> AuditLogEntry:
        err_stack = traceback.format_exc() if exception_obj else error_message
        return self.record_event(
            job_id=job_id,
            asset_name=asset_name,
            action="SYSTEM_ERROR",
            reviewer="Error Monitoring System",
            reviewer_notes=f"CRITICAL SYSTEM ERROR: {error_message}",
            overall_score=0.0,
            dnt_violations_count=0,
            destination="Error Alert Queue & Incident Logs",
            error_details=err_stack
        )

    def get_all_logs(self) -> List[Dict[str, Any]]:
        return self.memory_logs
