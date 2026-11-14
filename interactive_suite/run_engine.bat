@echo off
chcp 65001 >nul
title World Bank ESMAP MTF 1-Click Production Engine
color 0A

echo ===============================================================================
echo     World Bank ESMAP Multi-Tier Framework (MTF) 1-Click Production Engine
echo                 (100%% Local Execution - Zero Coding Required)
echo ===============================================================================
echo.

REM 1. Activate or initialize local virtual environment (.venv)
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo [*] First-time setup: Initializing isolated local virtual environment (.venv)...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip >nul 2>&1
    pip install -r requirements.txt
)

REM 2. Execute MTF Engine (Auto-detects Data/ and exports Excel + JSON)
python mtf_engine.py
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ===============================================================================
    echo  [ERROR] An error occurred during MTF Engine execution.
    echo  Generating diagnostic report and preparing email dispatch to Bryan Koo...
    echo ===============================================================================
    echo.
    python report_error.py --error "MTF Engine crashed during 1-click execution"
    pause
    exit /b 1
)

REM 3. Open Output folder in Explorer
if exist "Output" (
    echo [*] Opening Output folder...
    start "" "Output"
)

echo.
echo ===============================================================================
echo  [SUCCESS] Analysis results (Excel, JSON) saved to Output/ folder!
echo  Press any key to close this window...
echo ===============================================================================
pause >nul
