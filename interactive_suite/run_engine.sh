#!/usr/bin/env bash
# ===============================================================================
# World Bank ESMAP MTF 1-Click Production Engine Launcher (macOS / Linux)
# ===============================================================================
set -e

echo "==============================================================================="
echo "    World Bank ESMAP Multi-Tier Framework (MTF) 1-Click Production Engine"
echo "                (100% Local Execution - Zero Coding Required)"
echo "==============================================================================="
echo ""

# 1. Activate or initialize virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "[*] 최초 실행: 안전한 로컬 독립 가상환경(.venv)을 구축합니다..."
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
fi

# 2. Execute MTF Engine
if ! python3 mtf_engine.py; then
    echo ""
    echo "==============================================================================="
    echo " ❌ [오류 발생] MTF 엔진 실행 중 문제가 발생했습니다."
    echo "    진단 로그를 생성하고 Bryan Koo에게 이메일 보고를 준비합니다..."
    echo "==============================================================================="
    python3 report_error.py --error "MTF Engine crashed during 1-click execution"
    exit 1
fi

# 3. Open Output folder if available
if [ -d "Output" ]; then
    if command -v xdg-open &> /dev/null; then
        xdg-open "Output" > /dev/null 2>&1 &
    elif command -v open &> /dev/null; then
        open "Output" > /dev/null 2>&1 &
    fi
fi

echo "==============================================================================="
echo " [완료] 분석 결과 파일(Excel, JSON)이 Output/ 폴더에 저장되었습니다!"
echo "==============================================================================="
