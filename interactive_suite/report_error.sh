#!/usr/bin/env bash
# ===============================================================================
# World Bank ESMAP MTF 1-Click Error Reporter (macOS / Linux)
# ===============================================================================
set -e

if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

python3 report_error.py
