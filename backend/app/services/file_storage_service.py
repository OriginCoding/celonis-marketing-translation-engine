import os
import json
import time
from typing import List, Dict, Any, Optional

class FileStorageService:
    """
    Open-Source File Storage Manager.
    Saves input file requests and localized output HTML files with versioning,
    allowing viewing, inspection, and direct browser downloading.
    """

    def __init__(self, base_dir: str = "storage"):
        self.base_dir = base_dir
        self.input_dir = os.path.join(base_dir, "input")
        self.output_dir = os.path.join(base_dir, "output")
        self._ensure_dirs()

    def _ensure_dirs(self):
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def _sanitize_job_id(self, job_id: str) -> str:
        """Security Guardrail: Prevent directory traversal attacks."""
        clean = os.path.basename(job_id.replace("\\", "/"))
        return clean or "default_job"

    def save_job_files(
        self,
        job_id: str,
        asset_name: str,
        source_html: str,
        translated_html: str
    ) -> Dict[str, str]:
        safe_job_id = self._sanitize_job_id(job_id)
        job_in_dir = os.path.join(self.input_dir, safe_job_id)
        job_out_dir = os.path.join(self.output_dir, safe_job_id)
        os.makedirs(job_in_dir, exist_ok=True)
        os.makedirs(job_out_dir, exist_ok=True)

        clean_asset_name = os.path.basename(asset_name)
        source_path = os.path.join(job_in_dir, f"source_{clean_asset_name}")
        translated_path = os.path.join(job_out_dir, f"translated_es_{clean_asset_name}")

        with open(source_path, "w", encoding="utf-8") as f:
            f.write(source_html)

        with open(translated_path, "w", encoding="utf-8") as f:
            f.write(translated_html)

        # Meta info
        meta_path = os.path.join(job_out_dir, "meta.json")
        meta = {
            "job_id": safe_job_id,
            "asset_name": clean_asset_name,
            "timestamp": time.time(),
            "source_size_bytes": len(source_html.encode("utf-8")),
            "translated_size_bytes": len(translated_html.encode("utf-8")),
            "source_path": source_path,
            "translated_path": translated_path
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        return {
            "source_path": source_path,
            "translated_path": translated_path
        }

    def list_all_saved_files(self) -> List[Dict[str, Any]]:
        records = []
        if not os.path.exists(self.output_dir):
            return records

        for job_id in os.listdir(self.output_dir):
            job_dir = os.path.join(self.output_dir, job_id)
            meta_path = os.path.join(job_dir, "meta.json")
            if os.path.isfile(meta_path):
                try:
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                        records.append(meta)
                except Exception:
                    continue

        records.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        return records

    def get_file_content(self, job_id: str, file_type: str) -> Optional[str]:
        safe_job_id = self._sanitize_job_id(job_id)
        if file_type == "source":
            job_dir = os.path.join(self.input_dir, safe_job_id)
        else:
            job_dir = os.path.join(self.output_dir, safe_job_id)

        if not os.path.exists(job_dir):
            return None

        for fname in os.listdir(job_dir):
            if fname != "meta.json" and (
                (file_type == "source" and fname.startswith("source_")) or
                (file_type == "output" and fname.startswith("translated_"))
            ):
                fpath = os.path.join(job_dir, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    return f.read()
        return None
