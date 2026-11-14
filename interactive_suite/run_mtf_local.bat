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
    echo [ERROR] 파이썬(Python)이 설치되어 있지 않거나 환경변수(PATH)에 등록되지 않았습니다.
    echo.
    echo -------------------------------------------------------------------------------
    echo  [해결 방법 - 1분 소요]
    echo   1. 잠시 후 열리는 공식 웹페이지에서 파이썬을 다운로드 받아 설치해 주세요.
    echo   2. ★중요★ 설치 첫 화면 맨 아래에 있는:
    echo      [v] "Add python.exe to PATH" (PATH에 Python 추가)
    echo      체크박스를 반드시 체크하고 [Install Now]를 눌러주세요!
    echo   3. 설치 완료 후 본 파일(run_mtf_local.bat)을 다시 더블클릭하시면 됩니다.
    echo -------------------------------------------------------------------------------
    echo.
    echo 웹 브라우저를 열어 파이썬 다운로드 페이지로 이동합니다...
    timeout /t 3 >nul
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Display detected Python version
for /f "tokens=*" %%i in ('python --version') do set PY_VER=%%i
echo [*] 감지된 파이썬 버전: %PY_VER%
echo.

REM 2. Check and initialize local virtual environment (.venv)
if not exist ".venv" (
    echo [*] 최초 실행: 안전한 로컬 독립 가상환경(.venv)을 구축합니다 (약 30초 소요)...
    python -m venv .venv
    if %errorlevel% neq 0 (
        color 0C
        echo [ERROR] 가상환경 생성에 실패했습니다. 관리자 권한을 확인해 주세요.
        pause
        exit /b 1
    )
    echo [*] 필수 라이브러리(pandas, matplotlib, jupyterlab 등)를 자동 설치합니다...
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip >nul 2>&1
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        color 0C
        echo [ERROR] 라이브러리 설치 중 오류가 발생했습니다. 네트워크 연결을 확인해 주세요.
        pause
        exit /b 1
    )
    echo ✓ 라이브러리 설치가 완료되었습니다!
    echo.
) else (
    call .venv\Scripts\activate.bat
)

REM 3. User Choice Menu
echo ===============================================================================
echo  원하시는 작업 번호를 선택해 주세요 [기본값: 1]:
echo.
echo   [1] JupyterLab 대화형 분석기 실행 (웹 브라우저 노트북 환경)
echo   [2] 1-Click 초고속 분석 엔진 실행 (엑셀 및 보고서용 JSON 파일 즉시 생성)
echo   [3] GitHub 최신 도구 및 패치 업데이트
echo ===============================================================================
set /p CHOICE="선택 (1/2/3, 기본값 Enter=1): "

if "%CHOICE%"=="2" (
    echo.
    python mtf_engine.py
    if exist "Output" start "" "Output"
    echo.
    echo 아무 키나 누르시면 창이 닫힙니다...
    pause >nul
    exit /b 0
)

if "%CHOICE%"=="3" (
    echo.
    python update_tools.py
    echo.
    echo 아무 키나 누르시면 창이 닫힙니다...
    pause >nul
    exit /b 0
)

REM Default: Launch Local JupyterLab with the Interactive Analyzer Notebook
echo ===============================================================================
echo  [*] MTF 대화형 분석기를 웹 브라우저에서 실행합니다 (완전한 로컬 실행: localhost)...
echo  [*] 브라우저 창이 열리면 'MTF_Interactive_Analyzer.ipynb' 탭을 확인하세요!
echo  [*] 작업을 마치신 후 이 검은색 콘솔 창을 닫으시면 완전히 종료됩니다.
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
