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
echo " Please select an operation [Default: 1]:"
echo ""
echo "  [0] 1-Click Country Setup: Scan Data & Generate Calibration Excel (Step 1)"
echo "  [1] Launch JupyterLab Interactive Analyzer (Web Browser Notebook)"
echo "  [2] 1-Click Fast Production Engine (Instantly Export Excel & JSON)"
echo "  [3] 1-Click Full Publication Report & Charts (Generate 17 Charts + Word Report)"
echo "  [4] 1-Click Error Diagnostics & Support Dispatcher (Report to Bryan Koo)"
echo "  [5] Update Tools & Apply Latest GitHub Patches"
echo "  [6] Force Rebuild Master Dataset from Raw Survey Modules & Calibration Excel"
echo "==============================================================================="
read -p "Select (0/1/2/3/4/5/6, Default Enter=1): " CHOICE

if [ "$CHOICE" = "0" ]; then
    echo ""
    echo "[*] Scanning Data/ folder to detect country metadata and generate Calibration Workbook..."
    CALIB_SCRIPT=""
    for c_candidate in "../dev_tools/mtf_calibrator.py" "dev_tools/mtf_calibrator.py" "mtf_calibrator.py"; do
        if [ -f "$c_candidate" ]; then
            CALIB_SCRIPT="$c_candidate"
            break
        fi
    done

    if [ -n "$CALIB_SCRIPT" ]; then
        python3 "$CALIB_SCRIPT" --country-dir ".." --calibrate-country --auto-confirm
        echo ""
        echo "==============================================================================="
        echo " ✓ Success! Country Calibration Workbook generated in the root folder."
        echo " ★ Next Step: Open MTF_..._Calibration.xlsx, review Sheet 3 and 6, save it,"
        echo "   and then run this launcher again and select Option [3]!"
        echo "==============================================================================="
    else
        echo "❌ [ERROR] Could not find mtf_calibrator.py in dev_tools/."
    fi
    exit 0
fi

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
    echo "[*] Step 1/3: Running MTF Engine to export calibrated econometric JSON..."
    python3 mtf_engine.py

    # Detect scripts location: either ../Do-file/scripts, scripts/, or ../stata_pipeline/scripts
    SCRIPTS_DIR=""
    for s_candidate in "../Do-file/scripts" "scripts" "../stata_pipeline/scripts"; do
        if [ -f "$s_candidate/visualize.py" ]; then
            SCRIPTS_DIR="$s_candidate"
            break
        fi
    done

    if [ -n "$SCRIPTS_DIR" ]; then
        echo "[*] Step 2/3: Generating 17 High-Resolution Publication Charts (300 DPI)..."
        python3 "$SCRIPTS_DIR/visualize.py" --base-dir ".."

        echo "[*] Step 3/3: Injecting Econometric Values into World Bank Word Report (.docx)..."
        python3 "$SCRIPTS_DIR/inject_report.py" --base-dir ".."

        echo "✓ All publication charts and World Bank Word report generated in ../Output!"
        if [ -d "../Output" ]; then
            if command -v xdg-open &> /dev/null; then
                xdg-open "../Output" > /dev/null 2>&1 &
            elif command -v open &> /dev/null; then
                open "../Output" > /dev/null 2>&1 &
            fi
        fi
    else
        echo "⚠️ [WARN] Could not find visualize.py or inject_report.py in ../Do-file/scripts."
        echo "   Please ensure Do-files and scripts were deployed by mtf_calibrator.py."
    fi
    exit 0
fi

if [ "$CHOICE" = "4" ]; then
    echo ""
    python3 report_error.py
    exit 0
fi

if [ "$CHOICE" = "5" ]; then
    echo ""
    python3 update_tools.py
    exit 0
fi

if [ "$CHOICE" = "6" ]; then
    echo ""
    echo "[*] Force-rebuilding Master Dataset from raw survey modules and calibration workbook..."
    if ! python3 mtf_engine.py --rebuild; then
        python3 report_error.py --error "Engine crashed during master rebuild"
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

# Default: Launch Jupyter
echo "[*] Launching local browser interface (localhost)..."
if [ -f "MTF_Interactive_Analyzer.ipynb" ]; then
    jupyter lab MTF_Interactive_Analyzer.ipynb
elif [ -f "Tools/MTF_Interactive_Analyzer.ipynb" ]; then
    jupyter lab Tools/MTF_Interactive_Analyzer.ipynb
else
    jupyter lab
fi
