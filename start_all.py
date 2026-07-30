import subprocess
import sys
import os
import time

sys.stdout.reconfigure(encoding='utf-8')

print("⚡ Starting Celonis Marketing Asset Translation Engine (Full-Stack)...")
print("----------------------------------------------------------------------")

root_dir = os.path.abspath(os.path.dirname(__file__))
venv_python = os.path.join(root_dir, ".venv", "Scripts", "python.exe")
frontend_dir = os.path.join(root_dir, "frontend")

# 1. Launch FastAPI Backend Microservice (Port 8000)
print("🐍 Starting Python FastAPI Backend on http://localhost:8000 (OpenAPI Docs: http://localhost:8000/docs)...")
backend_process = subprocess.Popen([venv_python, "run_backend.py"], cwd=root_dir)

time.sleep(2)

# 2. Launch Next.js 14 Frontend Studio (Port 3000)
print("⚡ Starting Next.js 14 Frontend Studio on http://localhost:3000...")
frontend_process = subprocess.Popen("npm run dev", cwd=frontend_dir, shell=True)

print("----------------------------------------------------------------------")
print("✅ Full-Stack Application is running!")
print("🌐 Next.js Studio UI: http://localhost:3000")
print("📖 FastAPI Swagger Docs: http://localhost:8000/docs")
print("----------------------------------------------------------------------")
print("Press Ctrl+C to stop all servers.")

try:
    backend_process.wait()
    frontend_process.wait()
except KeyboardInterrupt:
    print("\n🛑 Stopping servers...")
    backend_process.terminate()
    frontend_process.terminate()
    print("✓ All servers stopped.")
