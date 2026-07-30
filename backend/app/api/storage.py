from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, Response
from app.services.file_storage_service import FileStorageService

router = APIRouter(prefix="/api/storage", tags=["File Storage Repository"])
storage_service = FileStorageService()

MOCK_IMAGE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="600" height="300" viewBox="0 0 600 300">
  <rect width="100%" height="100%" fill="#1a1f2c"/>
  <rect x="10" y="10" width="580" height="280" rx="8" fill="#242b3d" stroke="#3b82f6" stroke-width="2"/>
  <text x="50%" y="45%" dominant-baseline="middle" text-anchor="middle" fill="#60a5fa" font-family="sans-serif" font-size="20" font-weight="bold">
    📊 Agent C Dashboard Preview
  </text>
  <text x="50%" y="62%" dominant-baseline="middle" text-anchor="middle" fill="#94a3b8" font-family="sans-serif" font-size="14">
    Powered by Celonis Process Intelligence
  </text>
</svg>"""

@router.get("/files")
def list_saved_files():
    """Returns list of all saved request and output HTML files."""
    return {
        "total_files": len(storage_service.list_all_saved_files()),
        "files": storage_service.list_all_saved_files()
    }

@router.get("/view/{job_id}/{file_type}")
def view_saved_html_file(job_id: str, file_type: str):
    """Renders raw saved source or output HTML file, or placeholder images directly in the browser."""
    if file_type.endswith((".png", ".jpg", ".jpeg", ".svg", ".gif")) or "png" in file_type or "jpg" in file_type:
        return Response(content=MOCK_IMAGE_SVG, media_type="image/svg+xml")

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
