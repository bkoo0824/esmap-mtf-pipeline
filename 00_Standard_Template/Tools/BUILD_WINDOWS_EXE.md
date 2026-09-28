# Instructions: Compiling `mtf_calibrator.py` into a Standalone Windows Executable (`mtf_calibrator.exe`)

This script can be packaged into a standalone, portable Windows `.exe` that runs on any World Bank Group Windows laptop without needing Python or Stata pre-installed.

---

### Method A: One-Click Build Script on Windows (`build_exe.bat`)

Save the following commands as `build_exe.bat` inside `00_MTF_Country_Pipeline_Standard\Tools\`:

```bat
@echo off
title MTF Auto-Calibrator EXE Builder
echo ========================================================
echo   Building Standalone Windows Executable: mtf_calibrator.exe
echo ========================================================

REM 1. Ensure PyInstaller and Pandas are installed
pip install --upgrade pyinstaller pandas openpyxl

REM 2. Compile standalone one-file executable
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
```

---

### Method B: Manual Command Line Execution (PowerShell or CMD)

Open PowerShell in `00_MTF_Country_Pipeline_Standard\Tools\` and run:

```powershell
pip install pyinstaller pandas openpyxl
pyinstaller --noconfirm --onefile --console --name "mtf_calibrator" --add-data "..\Do-file;Do-file" --hidden-import "pandas" --hidden-import "openpyxl" mtf_calibrator.py
```

The resulting standalone executable will be located in:
`00_MTF_Country_Pipeline_Standard\Tools\dist\mtf_calibrator.exe`

---

### How to Use the `.exe` on Any Country:

Simply run the executable in the Command Prompt / PowerShell, passing the target country folder:

```cmd
mtf_calibrator.exe --country-dir "C:\Users\WB453090\OneDrive - WBG\1_mtf_energy_global_survey\9_Data analysis_MTF countries\35_Liberia(2024)\06. Data Analysis" --country-name "Liberia" --currency "LRD" --exchange-rate 192.5
```

The tool will:
1. Scan the raw data folders and rosters.
2. Detect the master dataset, weight variables, PSU, and Admin 1 geographic units.
3. Show the detected configuration table and prompt for confirmation.
4. Automatically write and patch all country-specific Do-files (`Master.do`, `00_build_master.do`, `01_setup.do`, `06_analytical_enhancements.do`, `07_export.do`) and python report scripts.
