@echo off
title MTF Report Injector EXE Builder
echo ============================================================
echo   Building Standalone Windows Executable: inject_report.exe
echo   ESMAP MTF Pipeline -- World Bank Energy GP
echo ============================================================
echo.

REM 1. Ensure required packages are installed
pip install --upgrade pyinstaller python-docx pillow openpyxl

echo.
echo [Building EXE...]
echo.

REM 2. Compile standalone one-file executable
REM    Bundles: MTF_Report_Template.md (template), pillow (image), python-docx (Word export), openpyxl (Excel export)
pyinstaller --noconfirm --onefile --console ^
    --name "inject_report" ^
    --add-data "..\MTF_Report_Template.md;Do-file" ^
    --hidden-import "docx" ^
    --hidden-import "docx.shared" ^
    --hidden-import "docx.enum.text" ^
    --hidden-import "docx.enum.table" ^
    --hidden-import "docx.oxml" ^
    --hidden-import "docx.oxml.ns" ^
    --hidden-import "PIL" ^
    --hidden-import "PIL.Image" ^
    --hidden-import "openpyxl" ^
    --hidden-import "openpyxl.styles" ^
    --hidden-import "openpyxl.utils" ^
    inject_report.py

echo.
echo ============================================================
echo   Build Complete!
echo   Standalone EXE located in: dist\inject_report.exe
echo ============================================================
echo.
echo   USAGE EXAMPLES:
echo.
echo   Option A: Run from the country analysis folder (auto-detects paths)
echo   ---------------------------------------------------------------
echo   inject_report.exe --base-dir "C:\...\35_Liberia(2024)\06. Data Analysis"
echo.
echo   Option B: Run with explicit parameters
echo   ---------------------------------------------------------------
echo   inject_report.exe --country Liberia --json "...\Output\mtf_report_values.json"
echo.
pause
