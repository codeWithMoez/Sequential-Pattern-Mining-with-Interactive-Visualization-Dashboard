@echo off
REM Windows Batch Script to Run Sequential Pattern Mining Application

echo ========================================
echo Sequential Pattern Mining Dashboard
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
pip show fastapi >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo Dependencies already installed.
)

echo.
echo [2/3] Starting Backend API...
echo Backend will run on http://localhost:8000
echo.
start "Backend API" cmd /k "python backend/main.py"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

echo.
echo [3/3] Starting Frontend Dashboard...
echo Frontend will open in your browser automatically.
echo.
echo ========================================
echo READY! Use Ctrl+C to stop servers.
echo ========================================
echo.

streamlit run frontend/app.py

REM If streamlit exits, cleanup
taskkill /FI "WindowTitle eq Backend API*" /T /F >nul 2>&1
