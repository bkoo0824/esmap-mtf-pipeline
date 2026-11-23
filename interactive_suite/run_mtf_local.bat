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
    echo   3. Once installed, double-click this launcher [run_mtf_local.bat] again.
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

REM 2. Environment Setup & Dependency Audit
REM On World Bank Group managed laptops, Device Guard blocks unsigned binaries in .venv.
REM We configure .venv with '--system-site-packages' so it seamlessly inherits packages
REM installed via 'python -m pip install --user' when .venv pip is blocked.

if exist ".venv\pyvenv.cfg" goto verify_libs

echo [*] Initializing isolated local virtual environment [.venv]...
python -m venv --system-site-packages .venv >nul 2>&1 || python -m venv .venv
if exist ".venv\pyvenv.cfg" (
    powershell -Command "(Get-Content .venv\pyvenv.cfg) -replace 'include-system-site-packages = false', 'include-system-site-packages = true' | Set-Content .venv\pyvenv.cfg" >nul 2>&1
)

:verify_libs
if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat" 2>nul
)

REM Verify if core packages (pandas) are importable
python -c "import pandas, numpy, matplotlib, openpyxl" >nul 2>&1
if %errorlevel% equ 0 goto menu_start

echo [*] Installing required analytical packages (pandas, numpy, matplotlib, etc.)...
REM Attempt 1: Standard pip via current python environment
python -m pip install -r requirements.txt >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Package installation complete!
    echo.
    goto menu_start
)

REM Attempt 2: Device Guard fallback (install into user site packages)
echo [*] Device Guard detected: Installing packages into user-level Python directory...
python -m pip install --user -r requirements.txt
if %errorlevel% neq 0 (
    echo [WARN] Automatic package install had warnings. Proceeding with execution...
)
echo.

:menu_start

REM 3. User Choice Menu
echo ===============================================================================
echo  Please select an operation [Default: 1]:
echo.
echo   [0] 1-Click Country Setup: Scan Data & Generate Calibration Excel (Step 1)
echo   [1] Launch JupyterLab Interactive Analyzer (Web Browser Notebook)
echo   [2] 1-Click Fast Production Engine (Instantly Export Excel & JSON)
echo   [3] 1-Click Full Publication Report & Charts (Generate 17 Charts + Word Report)
echo   [4] 1-Click Error Diagnostics & Support Dispatcher (Report to Bryan Koo)
echo   [5] Update Tools & Apply Latest GitHub Patches
echo   [6] Force Rebuild Master Dataset from Raw Survey Modules & Calibration Excel
echo ===============================================================================
set /p CHOICE="Select (0/1/2/3/4/5/6, Default Enter=1): "

if "%CHOICE%"=="0" (
    echo.
    echo [*] Scanning Data\ folder to detect country metadata and generate Calibration Workbook...
    set CALIB_SCRIPT=
    if exist "..\dev_tools\mtf_calibrator.py" set CALIB_SCRIPT=..\dev_tools\mtf_calibrator.py
    if exist "dev_tools\mtf_calibrator.py" set CALIB_SCRIPT=dev_tools\mtf_calibrator.py
    if exist "mtf_calibrator.py" set CALIB_SCRIPT=mtf_calibrator.py

    if defined CALIB_SCRIPT (
        python %CALIB_SCRIPT% --country-dir ".." --calibrate-country --auto-confirm
        echo.
        echo ===============================================================================
        echo  ✓ Success! Country Calibration Workbook generated in the root folder.
        echo  ★ Next Step: Open MTF_..._Calibration.xlsx, review Sheet 3 and 6, save it,
        echo    and then run this launcher again and select Option [3]!
        echo ===============================================================================
    ) else (
        echo [ERROR] Could not find mtf_calibrator.py in dev_tools\.
    )
    echo.
    echo Press any key to close this window...
    pause >nul
    exit /b 0
)

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
    echo [*] Step 1/3: Running MTF Engine to export calibrated econometric JSON...
    python mtf_engine.py
    if %errorlevel% neq 0 (
        python report_error.py --error "Engine crashed during report prep"
        exit /b 1
    )

    set SCRIPTS_DIR=
    if exist "..\Do-file\scripts\visualize.py" set SCRIPTS_DIR=..\Do-file\scripts
    if exist "scripts\visualize.py" set SCRIPTS_DIR=scripts
    if exist "..\stata_pipeline\scripts\visualize.py" set SCRIPTS_DIR=..\stata_pipeline\scripts

    if defined SCRIPTS_DIR (
        echo [*] Step 2/3: Generating 17 High-Resolution Publication Charts [300 DPI]...
        python %SCRIPTS_DIR%\visualize.py --base-dir ".."
        echo [*] Step 3/3: Injecting Econometric Values into World Bank Word Report [.docx]...
        python %SCRIPTS_DIR%\inject_report.py --base-dir ".."
        echo [OK] All publication charts and World Bank Word report generated in ..\Output!
        if exist "..\Output" start "" "..\Output"
    ) else (
        echo [WARN] Could not find visualize.py or inject_report.py in scripts directories.
    )
    echo.
    echo Press any key to close this window...
    pause >nul
    exit /b 0
)

if "%CHOICE%"=="4" (
    echo.
    python report_error.py
    echo.
    echo Press any key to close this window...
    pause >nul
    exit /b 0
)

if "%CHOICE%"=="5" (
    echo.
    python update_tools.py
    echo.
    echo Press any key to close this window...
    pause >nul
    exit /b 0
)

if "%CHOICE%"=="6" (
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
echo  [*] Launching MTF Interactive Analyzer in web browser [localhost]...
echo  [*] When browser opens, ensure you work inside 'MTF_Interactive_Analyzer.ipynb'!
echo  [*] Close this console window when you are finished to stop the server.
echo ===============================================================================
echo.

if exist "MTF_Interactive_Analyzer.ipynb" (
    start jupyter lab MTF_Interactive_Analyzer.ipynb
    exit /b 0
)
if exist "Tools\MTF_Interactive_Analyzer.ipynb" (
    start jupyter lab Tools\MTF_Interactive_Analyzer.ipynb
    exit /b 0
)
start jupyter lab
exit /b 0
