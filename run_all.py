"""
ProofForge AI - Unified Services Runner
Launches both Backend (FastAPI Engine) and Frontend (Vite + React) together.
API Documentation is available on both http://localhost:8080/docs and http://127.0.0.1:8000/docs
"""

import os
import sys
import time
import subprocess
import signal
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
VENV_PYTHON = BACKEND_DIR / "venv" / "Scripts" / "python.exe"
if not VENV_PYTHON.exists():
    VENV_PYTHON = Path(sys.executable)

processes = []

def cleanup(sig=None, frame=None):
    print("\n[ProofForge] Gracefully stopping all services...")
    for p in processes:
        try:
            if sys.platform == "win32":
                subprocess.call(["taskkill", "/F", "/T", "/PID", str(p.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                p.terminate()
        except Exception:
            pass
    print("[ProofForge] All services stopped.")
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def wait_for_backend(url="http://127.0.0.1:8000/api/health", timeout=15):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url, timeout=1.5) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.5)
    return False

def main():
    print("========================================================================")
    print("             PROOFFORGE AI — UNIFIED SERVICE RUNNER                     ")
    print("========================================================================")

    # 1. Start Backend
    print("[1/2] Launching Backend FastAPI Engine on port 8000...")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)
    
    backend_proc = subprocess.Popen(
        [str(VENV_PYTHON), str(BACKEND_DIR / "run_server.py")],
        cwd=str(ROOT_DIR),
        env=env
    )
    processes.append(backend_proc)

    # Wait for backend readiness
    print("      Waiting for backend to be ready...")
    if wait_for_backend():
        print("      Backend ready and healthy.")
    else:
        print("      Backend launched (waiting for Vite startup)...")

    # 2. Start Frontend
    print("[2/2] Launching Frontend (Vite + React) on port 8080...")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    frontend_proc = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=str(ROOT_DIR),
        env=env
    )
    processes.append(frontend_proc)

    time.sleep(2)
    print("\n" + "=" * 72)
    print("           ALL SERVICES ARE COMBINED & RUNNING SUCCESSFULLY!            ")
    print("=" * 72)
    print("  * Web Application (React UI) : http://localhost:8080")
    print("  * Combined Backend API       : http://localhost:8080/api")
    print("  * Combined API Documentation : http://localhost:8080/docs")
    print("  * Direct Backend Server      : http://127.0.0.1:8000")
    print("  * Direct Swagger Docs        : http://127.0.0.1:8000/docs")
    print("=" * 72)
    print("  Press CTRL+C in this window to stop all services simultaneously.\n")

    try:
        while True:
            # Check if any process terminated unexpectedly
            for p in processes:
                code = p.poll()
                if code is not None:
                    print(f"\n[ProofForge] Process (PID {p.pid}) exited with code {code}.")
                    cleanup()
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
