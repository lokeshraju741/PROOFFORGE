@echo off
cd /d "%~dp0"
echo ========================================================
echo   Starting ProofForge AI Unified Platform...
echo ========================================================
if exist "backend\venv\Scripts\python.exe" (
    backend\venv\Scripts\python.exe run_all.py
) else (
    python run_all.py
)
pause
