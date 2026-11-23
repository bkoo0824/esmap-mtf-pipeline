@echo off
chcp 65001 >nul
title World Bank ESMAP MTF Tools - 1-Click Auto-Updater
color 0A

echo ===============================================================================
echo     World Bank ESMAP Multi-Tier Framework (MTF) Tools Auto-Updater
echo                 [GitHub Sync and Safe Script Refresh]
echo ===============================================================================
echo.

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" update_tools.py
) else (
    python update_tools.py
)

echo.
echo ===============================================================================
echo  Update complete! Press any key to close this window.
echo ===============================================================================
pause >nul
exit /b 0
