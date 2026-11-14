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

# 3. Launch Jupyter
echo "[*] Launching local browser interface (localhost)..."
if [ -f "MTF_Interactive_Analyzer.ipynb" ]; then
    jupyter lab MTF_Interactive_Analyzer.ipynb
elif [ -f "Tools/MTF_Interactive_Analyzer.ipynb" ]; then
    jupyter lab Tools/MTF_Interactive_Analyzer.ipynb
else
    jupyter lab
fi
