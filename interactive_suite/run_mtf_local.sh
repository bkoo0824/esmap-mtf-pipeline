#!/usr/bin/env bash
# ===============================================================================
# World Bank ESMAP MTF Local Interactive Analyzer Launcher (macOS / Linux)
# ===============================================================================

set -e

echo "==============================================================================="
echo "    World Bank ESMAP Multi-Tier Framework (MTF) Local Analytics Launcher"
echo "              (100% Local Execution - Confidential Data Protected)"
echo "==============================================================================="
echo ""

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ [ERROR] Python 3 is not installed."
    echo "   Please install Python 3 via https://www.python.org/downloads/ or brew install python"
    exit 1
fi

echo "✓ Detected Python: $(python3 --version)"

# 2. Virtual environment
if [ ! -d ".venv" ]; then
    echo "[*] Initializing isolated local virtual environment (.venv)..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
    echo "✓ Setup complete!"
else
    source .venv/bin/activate
fi

# 3. User Choice Menu
echo "==============================================================================="
echo " 원하시는 작업 번호를 선택해 주세요 [기본값: 1]:"
echo ""
echo "  [1] JupyterLab 대화형 분석기 실행 (웹 브라우저 노트북 환경)"
echo "  [2] 1-Click 초고속 분석 엔진 실행 (엑셀 및 보고서용 JSON 파일 즉시 생성)"
echo "  [3] 1-Click 오류 진단 및 지원 요청 (Report an Error to Bryan Koo)"
echo "  [4] GitHub 최신 도구 및 패치 업데이트"
echo "==============================================================================="
read -p "선택 (1/2/3/4, 기본값 Enter=1): " CHOICE

if [ "$CHOICE" = "2" ]; then
    echo ""
    if ! python3 mtf_engine.py; then
        python3 report_error.py --error "Engine crashed from launcher menu"
    else
        if [ -d "Output" ]; then
            if command -v xdg-open &> /dev/null; then
                xdg-open "Output" > /dev/null 2>&1 &
            elif command -v open &> /dev/null; then
                open "Output" > /dev/null 2>&1 &
            fi
        fi
    fi
    exit 0
fi

if [ "$CHOICE" = "3" ]; then
    echo ""
    python3 report_error.py
    exit 0
fi

if [ "$CHOICE" = "4" ]; then
    echo ""
    python3 update_tools.py
    exit 0
fi

# Default: Launch Jupyter
echo "[*] Launching local browser interface (localhost)..."
if [ -f "MTF_Interactive_Analyzer.ipynb" ]; then
    jupyter lab MTF_Interactive_Analyzer.ipynb
elif [ -f "Tools/MTF_Interactive_Analyzer.ipynb" ]; then
    jupyter lab Tools/MTF_Interactive_Analyzer.ipynb
else
    jupyter lab
fi
