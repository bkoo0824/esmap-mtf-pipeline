# World Bank ESMAP Multi-Tier Framework (MTF) Pipeline Monorepo

**World Bank Group | Energy Sector Management Assistance Program (ESMAP)**  
*Global Survey & Access Analytics Team*

This repository houses the global standard analytical codebase for national **Multi-Tier Framework (MTF)** household energy access diagnostics. It provides a dual-engine architecture: an open-source interactive analytical suite for non-technical researchers and a production-grade Stata econometric pipeline for macro-level country diagnostics.

---

## 🚀 3-Minute Quickstart for Team Members (No Stata Required)

If you do not have a Stata license and want to explore MTF microdata, run policy simulations, or export publication-ready reports, charts, and tables:

1. **Download the Package:** Click the green **`[Code]`** button above ➔ **`[Download ZIP]`** and extract to your computer.
2. **Place Data:** Drop your country `.dta` file (or raw Survey Solutions modules) into the `interactive_suite/Data/` folder (or your country's root directory).
3. **Launch with 1-Click:**
   - **Windows:** Double-click [`interactive_suite/run_mtf_local.bat`](file:///home/bryan/github/esmap-mtf-pipeline/interactive_suite/run_mtf_local.bat)
   - **Mac / Linux:** Open terminal, navigate to `interactive_suite/` (or country `Tools/`), and run `./run_mtf_local.sh`
4. **Choose Your Desired Output from the Menu:**
   - **Option `[0]`**: **1-Click Country Setup** (scans raw `Data/`, detects country metadata, and generates `MTF_<Country>_Calibration.xlsx` for your manual review).
   - **Option `[1]`**: Launch JupyterLab Interactive Analyzer in your web browser.
   - **Option `[2]`**: 1-Click Fast Production Engine (exports 11-sheet Excel & JSON indicators).
   - **Option `[3]`**: **1-Click Full Publication Report & Charts** (auto-generates 17 high-res 300 DPI publication charts and compiles the complete World Bank diagnostic Word report `.docx`).
   - **Option `[6]`**: Force Rebuild Master Dataset from raw Survey Solutions modules and calibration workbook.
5. **Get Updates:** When new tools are released, double-click [`interactive_suite/update_mtf.bat`](file:///home/bryan/github/esmap-mtf-pipeline/interactive_suite/update_mtf.bat) (preserves your local `Data/` completely).

👉 *See [**`USER_GUIDE.md`**](file:///home/bryan/github/esmap-mtf-pipeline/USER_GUIDE.md) for the comprehensive End-to-End User Manual (Non-STATA & STATA Workflows).*  
👉 *See [`interactive_suite/LOCAL_SETUP_GUIDE.md`](file:///home/bryan/github/esmap-mtf-pipeline/interactive_suite/LOCAL_SETUP_GUIDE.md) for non-technical step-by-step instructions.*

---

## 🔒 Data Privacy & Architecture Protocol

### Strict Code-Only Policy
Under no circumstances is World Bank survey microdata (`*.dta`, `*.xlsx`, `Data/`) committed to this repository.
- **Microdata Storage:** Stored exclusively on institutional **OneDrive / SharePoint** or secured air-gapped analytical drives under World Bank access controls.
- **Code Repository:** Version-controlled exclusively on **GitHub**.
- **Local Bridge:** Stata master do-files and the Python engine dynamically bridge code and microdata using relative `Data/` paths and user path fallbacks.

---

## 📂 4-Pillar Repository Topology

```
esmap-mtf-pipeline/
│
├── config/                        <-- Standard Calibration Templates
│   └── mtf_calibration_standard.xlsx <-- Unified 5-Sheet Calibration Workbook (Stoves, Recodes, Tariff)
│
├── interactive_suite/             <-- [Pillar 1] Non-Technical Team Interactive Analyzer
│   ├── MTF_Interactive_Analyzer.ipynb  <-- 5-module Jupyter analysis suite & diagnostics
│   ├── run_mtf_local.bat          <-- Windows 1-click launcher
│   ├── run_mtf_local.sh           <-- Mac/Linux/Chromebook launcher
│   ├── update_mtf.bat             <-- Windows 1-click GitHub updater
│   ├── update_mtf.sh              <-- Mac/Linux 1-click GitHub updater
│   ├── update_tools.py            <-- Safe GitHub updater engine (preserves Data/)
│   ├── mtf_engine.py              <-- Vectorized survey-weighted calculation engine
│   ├── LOCAL_SETUP_GUIDE.md       <-- Non-technical user guide
│   └── Data/                      <-- Drop-in target for .dta microdata (.gitkeep)
│
├── stata_pipeline/                <-- [Pillar 2] Expert Stata Econometric Engine
│   ├── Do-file/                   <-- Core modules (00 to 07)
│   │   ├── 00_build_master_dataset.do
│   │   ├── 01_setup.do
│   │   ├── 02_elec_attributes.do
│   │   ├── 03_elec_aggregate.do
│   │   ├── 04_cooking_attributes.do
│   │   ├── 05_cooking_aggregate.do
│   │   ├── 06_analytical_enhancements.do
│   │   └── 07_export.do
│   ├── scripts/                   <-- 14 publication charts & docx report injector
│   │   ├── visualize.py
│   │   └── inject_report.py
│   ├── cookstove_calibration.csv  <-- Standard multi-tier stove typology
│   ├── MTF_Report_Template.md     <-- Standard diagnostic chapter template
│   └── README.md                  <-- Detailed Stata pipeline documentation
│
├── examples/                      <-- [Pillar 3] Reference Country Customization
│   └── guinea_bissau_reference/   <-- Canonical sample harmonization & master runner
│       ├── 00_country_harmonization.do
│       ├── Guinea-Bissau_MTF_Master.do
│       ├── mtf_calibration_guinea_bissau.xlsx <-- Unified 5-Sheet Country Calibration
│       └── README.md
│
├── dev_tools/                     <-- [Pillar 4] Developer & Packaging Utilities
│   ├── build_country_calibration.py  <-- Auto-generates country calibration templates
│   ├── extract_other_specify.py   <-- Extracts open-ended survey text to Excel
│   ├── mtf_calibrator.py          <-- Standalone Tkinter calibration GUI
│   ├── mtf_calibrator.spec        <-- PyInstaller bundling specification
│   ├── build_exe.bat              <-- Windows standalone EXE build script
│   └── BUILD_WINDOWS_EXE.md       <-- Packaging manual
│
├── tests/                         <-- CI/CD & Automated Dual-Engine Parity Gate
│   ├── test_engine_parity.py      <-- Stata vs. Python numerical equivalence tests
│   ├── test_inject_report.py      <-- Word/Markdown report injection validator
│   ├── test_adversarial_m1_*.py   <-- Adversarial robustness tests
│   └── test_adversarial_m2_*.py   <-- Figure sequence and label monotonicity tests
│
├── requirements.txt               <-- Minimal Python dependencies
└── git_sync.py                    <-- Pre-commit data leak scanner & sync tool
```

---

## 📊 Publication Graphics Suite & Report Injection Pipeline

The pipeline generates publication-grade graphics (300 DPI) and full diagnostic reports across three synchronized deliverables:

1. **Automated Diagnostic Report (`MTF_{Country}_Report.md` / `.docx`):**
   Full multi-chapter diagnostic automatically populated with country values, econometric tables, and figure embeds.
2. **Designer Excel Package (`MTF_{Country}_Report_Figures_Data.xlsx`):**
   Clean workbook with a **Figure Index** tab and individual data tabs (`Fig01` to `Fig14`) tailored for desktop publishers and infographic designers.
3. **Advanced Econometric Figure Suite (`visualize.py`):**
   - **Tiers & Attributes:** Multi-tier horizontal distributions and dual-panel radar bottlenecks (Grid vs. Off-Grid).
   - **Under-the-Grid Funnel:** Electrified PSU coverage vs. actual grid uptake rates and densification deficit.
   - **Standalone WTP Cumulative Demand Curves:**
     - **Figure 7a:** Grid connection demand across terms (Upfront, 3M, 6M, 12M, Fee Waived).
     - **Figure 7b:** Off-grid solar device demand across terms (Upfront, 6M, 12M, 24M PAYG).
     - **Figure 7c:** Clean cookstove demand across terms (Upfront, 3M, 6M, 12M).
   - **Mutually Exclusive Consumer Segments (100% Partition):** Minimum subsidy requirements without double-counting.
   - **Clean Cooking Stacking & Dilution:** Stacking dynamics and exposure dilution among clean stove owners.
