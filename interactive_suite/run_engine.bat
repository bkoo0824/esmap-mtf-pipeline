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
    echo [*] 최초 실행: 안전한 로컬 독립 가상환경(.venv)을 확인합니다...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip >nul 2>&1
    pip install -r requirements.txt
)

REM 2. Execute MTF Engine (Auto-detects Data/ and exports Excel + JSON)
python mtf_engine.py

REM 3. Open Output folder in Explorer
if exist "Output" (
    echo [*] 결과물 폴더(Output/)를 엽니다...
    start "" "Output"
)

echo.
echo ===============================================================================
echo  [완료] 결과 파일(Excel, JSON)이 Output/ 폴더에 성공적으로 생성되었습니다.
echo  창을 닫으려면 아무 키나 누르세요...
echo ===============================================================================
pause >nul
