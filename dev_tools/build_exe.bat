@echo off
title MTF Auto-Calibrator EXE Builder
echo ========================================================
echo   Building Standalone Windows Executable: mtf_calibrator.exe
echo ========================================================

pip install --upgrade pyinstaller pandas openpyxl

pyinstaller --noconfirm --onefile --console ^
    --name "mtf_calibrator" ^
    --add-data "..\Do-file;Do-file" ^
    --add-data "cookstove_calibration*.csv;Tools" ^
    --hidden-import "pandas" ^
    --hidden-import "openpyxl" ^
    mtf_calibrator.py

echo.
echo ========================================================
echo   Build Complete!
echo   Standalone EXE located in: dist\mtf_calibrator.exe
echo ========================================================
pause
