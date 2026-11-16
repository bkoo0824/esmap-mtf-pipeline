@echo off
chcp 65001 >nul
title World Bank ESMAP MTF Local Interactive Analyzer
color 0B

echo ===============================================================================
echo     World Bank ESMAP Multi-Tier Framework (MTF) Local Analytics Launcher
echo               (100%% Local Execution - Confidential Data Protected)
echo ===============================================================================
echo.

REM 1. Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python is not installed or not added to your system PATH.
    echo.
    echo -------------------------------------------------------------------------------
    echo  [Resolution - Takes 1 Minute]
    echo   1. The official Python download page will open in your browser.
    echo   2. ★CRITICAL CHECKPOINT★ On the very first installer screen:
    echo      [v] "Add python.exe to PATH"
    echo      Check this box before clicking [Install Now]!
    echo   3. Once installed, double-click this launcher (run_mtf_local.bat) again.
    echo -------------------------------------------------------------------------------
    echo.
    echo Opening web browser to Python download page...
    timeout /t 3 >nul
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Display detected Python version
for /f "tokens=*" %%i in ('python --version') do set PY_VER=%%i
echo [*] Detected Python version: %PY_VER%
echo.

REM 2. Check and initialize local virtual environment (.venv)
if not exist ".venv" (
    echo [*] First-time setup: Initializing isolated local virtual environment (.venv)...
    python -m venv .venv
    if %errorlevel% neq 0 (
        color 0C
        echo [ERROR] Failed to create virtual environment. Please check write permissions.
        pause
        exit /b 1
    )
    echo [*] Installing required libraries (pandas, matplotlib, jupyterlab, etc.)...
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip >nul 2>&1
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        color 0C
        echo [ERROR] Failed to install libraries. Please check your internet connection.
        pause
        exit /b 1
    )
    echo ✓ Library installation complete!
    echo.
) else (
    call .venv\Scripts\activate.bat
)

REM 3. User Choice Menu
echo ===============================================================================
echo  Please select an operation [Default: 1]:
echo.
echo   [1] Launch JupyterLab Interactive Analyzer (Web Browser Notebook)
echo   [2] 1-Click Fast Production Engine (Instantly Export Excel & JSON)
echo   [3] 1-Click Error Diagnostics & Support Dispatcher (Report to Bryan Koo)
echo   [4] Update Tools & Apply Latest GitHub Patches
echo ===============================================================================
set /p CHOICE="Select (1/2/3/4, Default Enter=1): "

if "%CHOICE%"=="2" (
    echo.
    python mtf_engine.py
    if %errorlevel% neq 0 (
        python report_error.py --error "Engine crashed from launcher menu"
    ) else (
        if exist "Output" start "" "Output"
    )
    echo.
    echo Press any key to close this window...
    pause >nul
    exit /b 0
)

if "%CHOICE%"=="3" (
    echo.
    python report_error.py
    echo.
    echo Press any key to close this window...
    pause >nul
    exit /b 0
)

if "%CHOICE%"=="4" (
    echo.
    python update_tools.py
    echo.
    echo Press any key to close this window...
    pause >nul
    exit /b 0
)

if "%CHOICE%"=="5" (
    echo.
    echo [*] Force-rebuilding Master Dataset from raw survey modules and calibration workbook...
    python mtf_engine.py --rebuild
    if %errorlevel% neq 0 (
        python report_error.py --error "Engine crashed during master rebuild"
    ) else (
        if exist "Output" start "" "Output"
    )
    echo.
    echo Press any key to close this window...
    pause >nul
    exit /b 0
)

REM Default: Launch Local JupyterLab with the Interactive Analyzer Notebook
echo ===============================================================================
echo  [*] Launching MTF Interactive Analyzer in web browser (localhost)...
echo  [*] When browser opens, ensure you work inside 'MTF_Interactive_Analyzer.ipynb'!
echo  [*] Close this console window when you are finished to stop the server.
echo ===============================================================================
echo.

if exist "MTF_Interactive_Analyzer.ipynb" (
    start jupyter lab MTF_Interactive_Analyzer.ipynb
) else if exist "Tools\MTF_Interactive_Analyzer.ipynb" (
    start jupyter lab Tools\MTF_Interactive_Analyzer.ipynb
) else (
    start jupyter lab
)

exit /b 0
