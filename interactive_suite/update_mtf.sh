#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

echo "==============================================================================="
echo "    World Bank ESMAP Multi-Tier Framework (MTF) Tools Auto-Updater"
echo "                (GitHub Sync & Safe Script Refresh)"
echo "==============================================================================="
echo ""

if [ -f ".venv/bin/python" ]; then
    .venv/bin/python update_tools.py
else
    python3 update_tools.py
fi

echo ""
echo "==============================================================================="
echo " Update complete! Press [Enter] to exit..."
echo "==============================================================================="
read -p ""
