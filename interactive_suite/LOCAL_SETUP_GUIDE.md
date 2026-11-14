# 📘 ESMAP MTF Local Interactive Suite: Operational User Guide
**World Bank ESMAP Multi-Tier Framework (MTF) Local Analytics Toolkit**

This guide provides a comprehensive step-by-step manual for **team members without a Stata license and without programming or Git experience**. It enables you to independently explore MTF household survey data on your local PC, run policy simulations, export publication-ready tables, and receive 1-click updates and automated remote support.

---

## 🔒 1. Data Governance & Air-Gapped Privacy

- **100% Offline / Local Execution (Air-Gapped):**
  - Household survey microdata is strictly confidential World Bank data and is **never uploaded** to Google Drive, public clouds, or GitHub.
  - All econometric calculations occur entirely within **your local PC memory (`localhost`)**.
- **Strict Two-Track Governance:**
  - **GitHub:** Hosts only open-source analysis code, Jupyter notebooks, and batch launchers (zero microdata).
  - **Survey Data (`.dta`):** Shared only with authorized team members via secure World Bank OneDrive and stored strictly in your local `Data/` folder.

---

## 📥 2. Initial Setup (One-Time Only, ~3 Minutes)

### [Step 1] Download the Analytics Toolkit
1. Open your web browser and navigate to the official GitHub repository:  
   👉 **[https://github.com/bkoo0824/esmap-mtf-pipeline](https://github.com/bkoo0824/esmap-mtf-pipeline)**
2. Click the green **`[Code]`** button at the top right, then click **`[Download ZIP]`**.
3. Extract `esmap-mtf-pipeline-main.zip` onto your local PC (e.g., your Desktop or Documents folder).  
   *(Git users may alternatively run `git clone https://github.com/bkoo0824/esmap-mtf-pipeline.git`)*

### [Step 2] Place the Survey Microdata (.dta)
1. You have two flexible options for your data:
   - **Option A (Pre-compiled Master):** Place the official country master dataset (`MTF_2024_HH_<Country>_Master.dta`, e.g., `MTF_2024_HH_Guinea-Bissau_Master.dta`) directly inside the **`interactive_suite/Data/`** folder.
   - **Option B (Raw Survey Solutions Modules):** Place the 15 raw Survey Solutions `.dta` files (`admin_info.dta`, `section_a1_hh_roster.dta`, `section_c_*.dta`, etc.) inside the **`interactive_suite/Data/`** folder.
2. The engine will automatically detect your files: if the Master dataset is not yet compiled, it will invoke `mtf_builder.py` and compile it on the fly with zero numerical divergence from Stata!
3. *(Optional)* Place your unified country calibration workbook (`mtf_calibration_<country>.xlsx`) in `config/` or `interactive_suite/Data/` if custom clean cooking emission tiers or open-text verbatim recodes are required.

### [Step 3] Install Python (Skip if Python 3.10+ is already installed)
1. Go to the [Official Python Download Page](https://www.python.org/downloads/) and click **[Download Python]**.
2. Run the downloaded installer.
3. ⚠️ **Critical Checkpoint (Must Follow):**
   - On the very first installer screen, you **MUST check the box**:  
     **`[v] Add python.exe to PATH`**
   - Click **`[Install Now]`** to complete installation in about 1 minute.

---

## ⚡ 3. 1-Click Launch & Execution (Two Simple Workflows)

No terminal commands or programming knowledge are required. Simply double-click with your mouse.

### [Workflow A] 1-Click Fast Production Engine (Recommended! ⭐)
If you want to calculate all 370+ MTF indicators (matching Stata 100% across 11 sheets) and instantly obtain `Output/MTF_Full_Indicators.xlsx`:
- **Windows Users:** Double-click **`run_engine.bat`**.
- **Mac / Linux Users:** Double-click or execute **`./run_engine.sh`**.

> **What happens automatically:**  
> 1. Automatically detects your master dataset in `Data/` and calculates all survey-weighted indicators in seconds.  
> 2. Displays an executive summary dashboard (National, Urban, Rural) directly in the console window.  
> 3. Saves `Output/MTF_Full_Indicators.xlsx` (11 comprehensive sheets including the `Indicator_Catalog`) and `Output/mtf_report_values.json` (370+ calibrated tokens).  
> 4. Automatically opens the `Output/` folder in File Explorer!  
> 5. If any error occurs, it automatically captures the diagnostic traceback into `mtf_error_report.txt` and opens your email composer pre-addressed to Bryan Koo.

---

### [Workflow B] JupyterLab Interactive Browser Notebook
If you want to interactively explore data, apply custom demographic filters, or simulate electricity tariff shocks:
- **Windows Users:** Double-click **`run_mtf_local.bat`**.
- **Mac / Linux Users:** Run **`./run_mtf_local.sh`**.
- A menu will prompt you to choose an option (press **Enter** for default `[1]`):
  - `[1]`: Launch JupyterLab Interactive Notebook
  - `[2]`: 1-Click Fast Production Engine (Excel & JSON)
  - `[3]`: 1-Click Error Diagnostics & Support Dispatcher (Report to Bryan Koo)
  - `[4]`: Update Tools & Apply Latest GitHub Patches

> ⚠️ **Important UI Tip in JupyterLab:**  
> - When your browser opens, look at the tabs: **Always work inside `MTF_Interactive_Analyzer.ipynb`** (orange notebook icon with interactive cells)!  
> - Do NOT double-click `.py` files (such as `mtf_engine.py`) in the file sidebar — `.py` files are backend computation scripts without notebook cells, causing the `▶ Run` button to be greyed out.

### [Overview of the 6 Analytical Modules]
Click any cell in `MTF_Interactive_Analyzer.ipynb` and press **`Shift + Enter`** (or click the top **`▶ Run`** button) to execute:
1. **Module 1 (Crosstabs & Disaggregation):** Access rates and Multi-Tier distributions across Urban/Rural, Gender of Household Head, and Consumption Quintiles (Q1–Q5).
2. **Module 2 (Vulnerability & Deficit Targeting):** Profiles Under-the-Grid unconnected deficit households and clean cooking biomass-stacking dilution.
3. **Module 3 (Policy Scenario Simulator):** Simulates electricity tariff adjustments (-30% to +50%) and measures lifeline basic bundle affordability for the poorest quintile.
4. **Module 4 (1-Click Full MTF Indicators & Export):** Invokes `mtf_engine` directly inside the notebook to generate the full 11-sheet Excel and calibrated JSON files.
5. **Module 5 (Ad-Hoc Custom Tables Export):** Exports custom cross-tabulation tables to `MTF_Interactive_Analysis_Output.xlsx`.
6. **Module 6 (1-Click Diagnostics & Support Dispatcher):** Instantly audits your environment, creates `mtf_error_report.txt`, and opens an email draft to Bryan Koo.

---

## 🔄 4. 1-Click Updates & Maintenance

When new features or bug fixes are published to GitHub, you can update without using Git:
- **How to Update:**
  - Double-click **`update_mtf.bat`** (Windows) or run **`./update_mtf.sh`** (Mac/Linux).
- **Safety Guarantee:**
  - The updater only refreshes tool scripts and notebooks.
  - Your local **survey datasets (`Data/`) and generated outputs (`Output/`) are 100% safe and will NEVER be overwritten**.

---

## 🩺 5. 1-Click Frictionless Error Reporting System

If you encounter any crash, missing variable warning, or unexpected behavior, you can report it in exactly **1 click**:

### [Method 1] Dedicated 1-Click Error Reporter (Easiest! ⭐)
- **Windows:** Double-click **`report_error.bat`**.
- **Mac / Linux:** Run **`./report_error.sh`**.
- **Automated Workflow:**
  1. The script audits your system environment, Python version, required packages, and `Data/` folder integrity, writing **`mtf_error_report.txt`**.
  2. Your default email client (Outlook, Mail) automatically opens pre-filled with:
     - **To:** `bkoo@worldbankgroup.org` (Bryan Koo)
     - **Subject:** `[ESMAP MTF Support] Diagnostic Report from <Host/User>`
     - **Body:** Pre-populated diagnostic summary.
  3. Simply attach the generated `mtf_error_report.txt` file and click **[Send]**!

### [Method 2] Automated Crash Interceptor
- If `run_engine.bat` stops due to an error, it will automatically catch the traceback, generate `mtf_error_report.txt`, and launch the email composer for you.

### [Method 3] JupyterLab Module 6
- If working inside the notebook, run **`Module 6: 1-Click System Diagnostics & Support Dispatcher`** to trigger the same automated diagnostic report and email draft.

---

## 💡 6. Frequently Asked Questions (FAQ)

- **Q. How do I shut down the tools after finishing my work?**
  - Simply close your web browser tab and close the black terminal/console window.
- **Q. Can I use this completely offline on flights or field missions?**
  - Yes! After the one-time initial library setup (~1 minute), the suite runs **100% offline on `localhost` without requiring any internet connection**. (Internet is only needed when clicking `update_mtf.bat` to pull updates.)
- **Q. Is my survey data safe?**
  - Yes. No survey microdata ever leaves your PC. Only technical diagnostic logs (`mtf_error_report.txt`) are shared when you request technical support.
