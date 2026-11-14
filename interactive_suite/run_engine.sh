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
    echo "[*] First-time setup: Initializing isolated local virtual environment (.venv)..."
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
fi

# 2. Execute MTF Engine
if ! python3 mtf_engine.py; then
    echo ""
    echo "==============================================================================="
    echo " ❌ [ERROR] An error occurred during MTF Engine execution."
    echo "    Generating diagnostic report and preparing email dispatch to Bryan Koo..."
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
echo " [SUCCESS] Analysis results (Excel, JSON) saved to Output/ folder!"
echo "==============================================================================="
