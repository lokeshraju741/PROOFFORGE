import os
import sys
from pathlib import Path

# Add backend directory to sys.path so imports work cleanly
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir.parent))

if __name__ == "__main__":
    import uvicorn
    print("=======================================================")
    print("  ProofForge AI Evidence Intelligence Backend Server   ")
    print("  URL: http://127.0.0.1:8000                           ")
    print("  Swagger Docs: http://127.0.0.1:8000/docs             ")
    print("=======================================================")
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
