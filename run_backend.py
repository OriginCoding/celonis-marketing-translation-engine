import sys
import os
import uvicorn

# Ensure UTF-8 encoding for Windows console output
sys.stdout.reconfigure(encoding='utf-8')

# Add backend directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

if __name__ == "__main__":
    print("🚀 Launching Celonis Marketing Asset Translation Engine FastAPI Backend on http://localhost:8000...")
    print("📖 Swagger OpenAPI Docs available at http://localhost:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, app_dir="backend")
