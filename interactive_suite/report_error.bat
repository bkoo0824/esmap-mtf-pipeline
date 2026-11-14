@echo off
chcp 65001 >nul
title World Bank ESMAP MTF 1-Click Error Reporter
color 0E

echo ===============================================================================
echo     World Bank ESMAP Multi-Tier Framework (MTF) 1-Click Error Reporter
echo ===============================================================================
echo.

REM 1. Activate Virtual Environment if exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

REM 2. Run Diagnostic & Error Reporter
python report_error.py

pause
