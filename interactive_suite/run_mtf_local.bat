@echo off
cd /d "%~dp0"
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
echo  Please select an operation:
echo.
echo   [0] Step 1: Scan Raw Data ^& Generate Calibration Excel Workbook
echo   [1] Step 2: Build Master Dataset from Raw Survey Modules (.dta)
echo   [2] Step 3: Run Full Production Calculation Engine (Excel ^& JSON)
echo.
echo   [3] Advanced: Launch JupyterLab Interactive Analyzer (Web Browser Notebook)
echo   [4] Support: 1-Click Error Diagnostics ^& Support Dispatcher (Report to Bryan Koo)
echo   [5] Maintenance: Update Tools ^& Apply Latest GitHub Patches
echo   [Q] Quit / Exit
echo ===============================================================================
set /p CHOICE="Enter choice [0-5, or Q to quit] (Default=2): "

if /i "%CHOICE%"=="Q" exit /b 0
if "%CHOICE%"=="" set CHOICE=2

if "%CHOICE%"=="0" goto run_option_0
if "%CHOICE%"=="1" goto run_option_6
if "%CHOICE%"=="2" goto run_option_3
if "%CHOICE%"=="3" goto run_option_1
if "%CHOICE%"=="4" goto run_option_4
if "%CHOICE%"=="5" goto run_option_5
goto run_option_3

:run_option_0
echo.
echo [*] 1-Click Country Setup: Scan Data ^& Generate Calibration Workbook...
echo If you want to specify a Country Name, enter it below (or press Enter to auto-detect):
set "USER_COUNTRY="
set /p USER_COUNTRY=Country Name: 

set "CALIB_SCRIPT="
if exist "%~dp0..\dev_tools\mtf_calibrator.py" set "CALIB_SCRIPT=%~dp0..\dev_tools\mtf_calibrator.py"
if not defined CALIB_SCRIPT if exist "%~dp0dev_tools\mtf_calibrator.py" set "CALIB_SCRIPT=%~dp0dev_tools\mtf_calibrator.py"
if not defined CALIB_SCRIPT if exist "%~dp0mtf_calibrator.py" set "CALIB_SCRIPT=%~dp0mtf_calibrator.py"
if not defined CALIB_SCRIPT if exist "..\dev_tools\mtf_calibrator.py" set "CALIB_SCRIPT=..\dev_tools\mtf_calibrator.py"
if not defined CALIB_SCRIPT if exist "dev_tools\mtf_calibrator.py" set "CALIB_SCRIPT=dev_tools\mtf_calibrator.py"
if not defined CALIB_SCRIPT if exist "mtf_calibrator.py" set "CALIB_SCRIPT=mtf_calibrator.py"

if not defined CALIB_SCRIPT (
    echo [*] mtf_calibrator.py not found locally. Running automatic update to download it...
    python update_tools.py
    if exist "%~dp0..\dev_tools\mtf_calibrator.py" set "CALIB_SCRIPT=%~dp0..\dev_tools\mtf_calibrator.py"
    if not defined CALIB_SCRIPT if exist "%~dp0dev_tools\mtf_calibrator.py" set "CALIB_SCRIPT=%~dp0dev_tools\mtf_calibrator.py"
    if not defined CALIB_SCRIPT if exist "..\dev_tools\mtf_calibrator.py" set "CALIB_SCRIPT=..\dev_tools\mtf_calibrator.py"
    if not defined CALIB_SCRIPT if exist "dev_tools\mtf_calibrator.py" set "CALIB_SCRIPT=dev_tools\mtf_calibrator.py"
)

if defined CALIB_SCRIPT (
    if defined USER_COUNTRY (
        python "%CALIB_SCRIPT%" --country-dir ".." --country-name "%USER_COUNTRY%" --calibrate-country --auto-confirm
    ) else (
        python "%CALIB_SCRIPT%" --country-dir ".." --calibrate-country --auto-confirm
    )
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

:run_option_2
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

:run_option_3
echo.
echo [*] Step 1/3: Running MTF Engine to export calibrated econometric JSON...
python mtf_engine.py
if %errorlevel% neq 0 (
    python report_error.py --error "Engine crashed during report prep"
    exit /b 1
)

REM Ensure outputs in interactive_suite\Output are mirrored to ..\Output if running inside interactive_suite
if exist "Output\mtf_report_values.json" (
    if not exist "..\Output" mkdir "..\Output" >nul 2>&1
    copy /y "Output\mtf_report_values.json" "..\Output\" >nul 2>&1
    copy /y "Output\MTF_Full_Indicators.xlsx" "..\Output\" >nul 2>&1
)

REM Discover visualize.py, inject_report.py, and MTF_Report_Template.md
set "VIS_SCRIPT="
if exist "visualize.py" set "VIS_SCRIPT=visualize.py"
if not defined VIS_SCRIPT if exist "..\stata_pipeline\scripts\visualize.py" set "VIS_SCRIPT=..\stata_pipeline\scripts\visualize.py"
if not defined VIS_SCRIPT if exist "..\Do-file\scripts\visualize.py" set "VIS_SCRIPT=..\Do-file\scripts\visualize.py"
if not defined VIS_SCRIPT if exist "scripts\visualize.py" set "VIS_SCRIPT=scripts\visualize.py"
if not defined VIS_SCRIPT if exist "stata_pipeline\scripts\visualize.py" set "VIS_SCRIPT=stata_pipeline\scripts\visualize.py"

set "INJ_SCRIPT="
if exist "inject_report.py" set "INJ_SCRIPT=inject_report.py"
if not defined INJ_SCRIPT if exist "..\stata_pipeline\scripts\inject_report.py" set "INJ_SCRIPT=..\stata_pipeline\scripts\inject_report.py"
if not defined INJ_SCRIPT if exist "..\Do-file\scripts\inject_report.py" set "INJ_SCRIPT=..\Do-file\scripts\inject_report.py"
if not defined INJ_SCRIPT if exist "scripts\inject_report.py" set "INJ_SCRIPT=scripts\inject_report.py"
if not defined INJ_SCRIPT if exist "stata_pipeline\scripts\inject_report.py" set "INJ_SCRIPT=stata_pipeline\scripts\inject_report.py"

set "TEMPLATE_PATH="
if exist "MTF_Report_Template.md" set "TEMPLATE_PATH=MTF_Report_Template.md"
if not defined TEMPLATE_PATH if exist "..\stata_pipeline\MTF_Report_Template.md" set "TEMPLATE_PATH=..\stata_pipeline\MTF_Report_Template.md"
if not defined TEMPLATE_PATH if exist "..\Do-file\MTF_Report_Template.md" set "TEMPLATE_PATH=..\Do-file\MTF_Report_Template.md"

set "BASE_TARGET=."
if exist "..\stata_pipeline" set "BASE_TARGET=.."
if exist "..\Do-file" set "BASE_TARGET=.."

if not defined VIS_SCRIPT (
    echo [ERROR] visualize.py not found!
    echo Please select Option [5] Update Tools to download the required scripts from GitHub.
) else (
    echo [*] Step 2/3: Generating 17 High-Resolution Publication Charts [300 DPI]...
    python "%VIS_SCRIPT%" --base-dir "%BASE_TARGET%"
)

if not defined INJ_SCRIPT (
    echo [ERROR] inject_report.py not found!
    echo Please select Option [5] Update Tools to download the required scripts from GitHub.
) else (
    echo [*] Step 3/3: Injecting Econometric Values into World Bank Word Report [.docx]...
    if defined TEMPLATE_PATH (
        python "%INJ_SCRIPT%" --base-dir "%BASE_TARGET%" --template "%TEMPLATE_PATH%"
    ) else (
        python "%INJ_SCRIPT%" --base-dir "%BASE_TARGET%"
    )
    echo.
    echo ===============================================================================
    echo  [OK] Success! Publication charts and World Bank Word report generated.
    echo ===============================================================================
    REM Ensure charts and reports are available in both Output\ and ..\Output\
    if exist "..\Output" (
        if exist "Output\charts" xcopy /y /i /e "Output\charts" "..\Output\charts" >nul 2>&1
        if exist "..\Output\charts" xcopy /y /i /e "..\Output\charts" "Output\charts" >nul 2>&1
        REM Clean up any stale TEST report artifacts
        del /f /q Output\MTF_TEST_*.* Output\MTF_Test_*.* "Output\MTF_interactive_suite_*.*" >nul 2>&1
        del /f /q ..\Output\MTF_TEST_*.* ..\Output\MTF_Test_*.* "..\Output\MTF_interactive_suite_*.*" >nul 2>&1
        copy /y Output\MTF_*.* ..\Output\ >nul 2>&1
        copy /y ..\Output\MTF_*.* Output\ >nul 2>&1
        start "" "..\Output"
    ) else if exist "Output" (
        del /f /q Output\MTF_TEST_*.* Output\MTF_Test_*.* "Output\MTF_interactive_suite_*.*" >nul 2>&1
        start "" "Output"
    )
)
echo.
echo Press any key to close this window...
pause >nul
exit /b 0

:run_option_4
echo.
python report_error.py
echo.
echo Press any key to close this window...
pause >nul
exit /b 0

:run_option_5
echo.
python update_tools.py
echo.
echo Press any key to close this window...
pause >nul
exit /b 0

:run_option_6
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

:run_option_1

REM Default: Launch Local JupyterLab with the Interactive Analyzer Notebook
echo ===============================================================================
echo  [*] Launching MTF Interactive Analyzer in web browser [localhost]...
echo  [*] When browser opens, ensure you work inside 'MTF_Interactive_Analyzer.ipynb'!
echo  [*] Close this console window when you are finished to stop the server.
echo ===============================================================================
echo.

python -c "import jupyterlab" >nul 2>&1
if %errorlevel% neq 0 (
    echo [NOTE] JupyterLab is not yet installed in this environment.
    echo [*] Running Option [2] Fast Production Engine directly instead...
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
