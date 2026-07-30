from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, Response
from app.services.file_storage_service import FileStorageService

router = APIRouter(prefix="/api/storage", tags=["File Storage Repository"])
storage_service = FileStorageService()

@router.get("/files")
def list_saved_files():
    """Returns list of all saved request and output HTML files."""
    return {
        "total_files": len(storage_service.list_all_saved_files()),
        "files": storage_service.list_all_saved_files()
    }

@router.get("/view/{job_id}/{file_type}", response_class=HTMLResponse)
def view_saved_html_file(job_id: str, file_type: str):
    """Renders raw saved source or output HTML file directly in the browser."""
    content = storage_service.get_file_content(job_id, file_type)
    if not content:
        raise HTTPException(status_code=404, detail="File not found in storage repository.")
    return HTMLResponse(content=content)

@router.get("/download/{job_id}/{file_type}")
def download_saved_html_file(job_id: str, file_type: str):
    """Triggers direct browser download of the saved HTML file."""
    content = storage_service.get_file_content(job_id, file_type)
    if not content:
        raise HTTPException(status_code=404, detail="File not found in storage repository.")
    
    filename = f"{file_type}_{job_id}.html"
    return Response(
        content=content,
        media_type="text/html",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
