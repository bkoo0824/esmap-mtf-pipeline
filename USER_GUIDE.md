# World Bank ESMAP Multi-Tier Framework (MTF) Pipeline & Interactive Suite
## Comprehensive User Manual: Non-STATA & STATA Operational Workflows

**World Bank Group | Energy Sector Management Assistance Program (ESMAP)**  
*Global Survey & Access Analytics Team*  
**Repository:** [https://github.com/bkoo0824/esmap-mtf-pipeline](https://github.com/bkoo0824/esmap-mtf-pipeline)  
**Lead Contact:** Bryan Koo, Senior Energy Specialist ([bkoo@worldbankgroup.org](mailto:bkoo@worldbankgroup.org))

---

## 1. Architecture & Division of Labor

The ESMAP MTF analytical architecture operates on a strict **Two-Track Confidentiality and Division of Labor Model**:

```
+---------------------------------------------------------------------------------+
|                               DATA GOVERNANCE ARCHITECTURE                       |
+---------------------------------------------------------------------------------+
|                                                                                 |
|   [Track 1: Open-Source Codebase - GitHub]       [Track 2: Confidential Microdata] |
|   - Version-controlled on GitHub                - Air-gapped on Bank OneDrive   |
|   - Zero survey microdata (*.dta, *.xlsx)       - Restricted access controls    |
|   - Automated 1-click execution & updates       - Stored in local Data/ only    |
|                                                                                 |
+---------------------------------------------------------------------------------+
```

### Institutional Roles:
1. **STATA Lead (Data Scientist / Econometrician):**
   - Compiles the 15 raw Survey Solutions modules (`section_a1`, `section_c`, etc.) into a **single, authoritative Master Dataset** (`MTF_2024_HH_<Country>_Master.dta`, ~40MB).
   - Establishes national consumption aggregates, annualized expenditure, poverty quintiles, and survey sampling weights.
   - Distributes the single `.dta` file to team members via secure World Bank OneDrive.
2. **Non-STATA Users (Sector Economists, Policy Analysts, Consultants, TTLs):**
   - Requires **no Stata license** and **no programming experience**.
   - Places the single master `.dta` file into `interactive_suite/Data/`.
   - Double-clicks a single launcher script to explore multi-tier metrics, test tariff/subsidy policy scenarios, and export publication-ready tables in their local web browser.

---

## 2. Track 1: Non-STATA User Guide (Interactive Suite)

**Target Audience:** Team members who need to analyze MTF data, produce disaggregated statistics, test policy scenarios, and export formatted tables without Stata.

### Step 1: Download & Unpack the Analytics Toolkit
1. Navigate to the official GitHub repository:  
   👉 **[https://github.com/bkoo0824/esmap-mtf-pipeline](https://github.com/bkoo0824/esmap-mtf-pipeline)**
2. Click the green **`[Code]`** button at the top right, then select **`[Download ZIP]`**.
3. Extract `esmap-mtf-pipeline-main.zip` onto your local machine (e.g., your Desktop or Documents folder).
   *(Git users may alternatively run: `git clone https://github.com/bkoo0824/esmap-mtf-pipeline.git`)*

### Step 2: Place the Survey Microdata (.dta)
1. Download the official country master dataset (`MTF_2024_HH_<Country>_Master.dta`, e.g., `MTF_2024_HH_Guinea-Bissau_Master.dta`) from the secure World Bank OneDrive link provided by the project lead.
2. Place this single `.dta` file directly into the **`interactive_suite/Data/`** folder.
   > **Note:** Do NOT place raw survey section files (`section_a1.dta`, `section_b.dta`, etc.) here. Only the compiled master dataset is needed.

### Step 3: Install Python (One-Time Setup, ~1 Minute)
*If Python 3.10+ is already installed on your machine, skip to Step 4.*
1. Visit the official Python download portal: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download and run the installer.
3. ⚠️ **Critical Checkpoint:**
   - On the very first installation screen, you **MUST check the box**:  
     **`[v] Add python.exe to PATH`**
   - Click **`[Install Now]`**.

### Step 4: 1-Click Launch (Zero Terminal Commands & Zero Coding)

Choose the workflow that best fits your immediate need:

#### Option A: 1-Click Production Engine (Fastest & Zero Coding - Recommended)
If you want to calculate all 86+ MTF indicators and export both the formatted Excel workbook (`MTF_Full_Indicators.xlsx`) and the report token file (`mtf_report_values.json`) without opening a browser or writing code:
- **Windows Users:** Double-click **`run_engine.bat`**.
- **Mac / Linux Users:** Double-click or run **`./run_engine.sh`**.
> **What happens automatically:**  
> The script auto-discovers your dataset in `Data/`, computes all survey-weighted indicators in 3 seconds, displays an executive summary table in the console, saves `Output/MTF_Full_Indicators.xlsx` and `Output/mtf_report_values.json`, and automatically opens the `Output/` folder!

#### Option B: Interactive Browser Notebook (JupyterLab)
If you want to interactively explore data, run customized crosstabs, or simulate tariff policies:
- **Windows Users:** Double-click **`run_mtf_local.bat`**.
- **Mac / Linux Users:** Double-click or run **`./run_mtf_local.sh`**.
- An interactive menu appears: press **Enter** (default: `[1]`) to launch JupyterLab in your browser.

> ⚠️ **Important UI Tip in JupyterLab:**  
> When the browser opens, look at the tabs: **Always work inside `MTF_Interactive_Analyzer.ipynb`** (orange notebook icon with cells).  
> *Do NOT open `.py` files (like `mtf_engine.py`) in JupyterLab — `.py` files are internal engine scripts without interactive cells, so the `Run` menu will appear disabled (greyed out).*

---

### Step 5: Explore, Simulate & Export in Your Browser
When **`MTF_Interactive_Analyzer.ipynb`** is active, click any cell and press **`Shift + Enter`** (or click the top **`▶ Run`** button) to run:

1. **Module 1: Disaggregations & Multi-Tier Metrics**
   - Survey-weighted MTF electricity access rates (Tier 1+ vs. Tier 0) and MECS clean cooking rates.
   - Disaggregated across Urban/Rural, Male vs. Female Household Heads (`hh_head_gender`), and National Income Quintiles (Q1 to Q5).
2. **Module 2: Vulnerability Targeting & Policy Filters**
   - **Under-the-Grid Deficit:** Identifies households residing directly under existing national grid lines who remain unconnected due to high connection charges.
   - **Clean Cooking Stacking:** Identifies clean stove owners who continue to use biomass/charcoal stoves (cooking exposure dilution).
3. **Module 3: Policy Scenario & Tariff Shock Simulator**
   - Dynamically models the impact of electricity tariff adjustments (-30% to +50%) against national lifeline benchmarks (e.g., EAGB social tariff @ 128 XOF/kWh).
   - Evaluates basic electricity bundle affordability (365 kWh/year) for the poorest 20% (Quintile 1).
4. **Module 4: 1-Click Production Engine & Full Export (`mtf_engine`)**
   - Runs the complete vectorized calculation engine right inside the notebook.
   - Displays headline findings and automatically exports:
     - 📁 `Output/MTF_Full_Indicators.xlsx` (5-sheet Excel matrix: Headline, Electricity Tiers, Cooking Tiers, WTP, All Indicators)
     - 📁 `Output/mtf_report_values.json` (340+ calibrated scalar tokens for Word report injection)
5. **Module 5: Ad-hoc Custom Tables Export**
   - Exports custom cross-tabulations and simulation matrices directly to `MTF_Interactive_Analysis_Output.xlsx`.
6. **Module 6: 1-Click Diagnostics & Remote Support**
   - If you encounter any unexpected error, execute this cell.
   - Generates an instant diagnostic log (`mtf_diagnostic_report.txt`) recording your environment, data file sizes, and variable integrity for one-click email support.

### Step 6: Ongoing Updates & Maintenance
- **Updating the Tools:** When new analytical modules or patches are released on GitHub, double-click **`update_mtf.bat`** (Windows) or **`update_mtf.sh`** (Mac/Linux).  
  *Your local `Data/` folder and custom output files are 100% safe and will never be overwritten.*
- **Technical Support:** Email your `mtf_diagnostic_report.txt` and a screenshot to **Bryan Koo** ([bkoo@worldbankgroup.org](mailto:bkoo@worldbankgroup.org)).

---

## 3. Track 2: STATA User Guide (Production Econometric Pipeline)

**Target Audience:** Lead data scientists and country economists responsible for raw survey data curation, country harmonization, econometric tier evaluation, and macro-level diagnostic publication.

### Step 1: Clone the Monorepo
```bash
git clone git@github.com:bkoo0824/esmap-mtf-pipeline.git
cd esmap-mtf-pipeline
```

### Step 2: Directory Layout & Reference Implementations
- **Core Stata Engine (`stata_pipeline/Do-file/`):** Universal econometric modules (`00_` through `07_`).
- **Country Customization Reference (`examples/guinea_bissau_reference/`):**
  - `00_country_harmonization.do`: Country-specific verbatim text recoding and missing value guardrails.
  - `cookstove_calibration.csv`: Multi-tier stove typology mapping.
  - `Guinea-Bissau_MTF_Master.do`: Master orchestration do-file.
- **Reporting Scripts (`stata_pipeline/scripts/`):** Publication-grade 300 DPI graphics (`visualize.py`) and automated Word report injection (`inject_report.py`).

### Step 3: Configure the Master Do-File
Copy `examples/guinea_bissau_reference/Guinea-Bissau_MTF_Master.do` to your analytical working directory or rename it for your target country (`<Country>_MTF_Master.do`). Configure the top macro block:

```stata
*======================    1. USER & PATH SETUP   ============================*
if c(os) == "Windows" {
    global user "C:/Users/`c(username)'/OneDrive - WBG/1_mtf_energy_global_survey/9_Data analysis_MTF countries/37_Guinea-Bissau"
    global raw_hh "$user/Data"
}
else if c(os) == "Unix" {
    global user "/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/37_Guinea-Bissau"
    global raw_hh "$user/Data"
}

* Paths (Always use forward slashes '/')
global wip_hh    "$user/Data/wip_hh"
global clean     "$user/Data/clean"
global output    "$user/Output"
global scripts   "/path/to/esmap-mtf-pipeline/stata_pipeline/Do-file"

* Macroeconomic & Country Parameters
global country      "Guinea-Bissau"
global country_iso3 "GNB"
global master_dta   "MTF_2024_HH_Guinea-Bissau_Master.dta"
global currency     "XOF"
global usd_rate     605.0
```

### Step 4: Country Harmonization & Guardrails (`00_country_harmonization.do`)
1. Review country open-ended responses using `dev_tools/extract_other_specify.py`.
2. Map local verbatim expressions (e.g., Portuguese artisanal braziers `"fogareiro"` to Code 2 Traditional Stove).
3. **Zero-Assumption Rule:** Unclassified open-ended responses automatically recode to system missing (`.`). If unclassified responses exceed 5% of the sample, an automatic error alert is raised.

### Step 5: Execute the Master Pipeline in Stata
Execute the master do-file in Stata SE/MP:
```stata
do "/path/to/Guinea-Bissau_MTF_Master.do"
```

#### Pipeline Execution Sequence:
| Stage | Do-File | Operations Performed |
| :--- | :--- | :--- |
| **[0/7]** | `00_build_master_dataset.do` | Merges 15 raw modules; computes household size, head characteristics, annualized consumption aggregates (food $\times 52$, non-food $\times 12$), population-weighted quintiles, and multi-stove cooking time weights. |
| **[0b/7]**| `00_country_harmonization.do` | Country-specific verbatim recoding and missing guardrails. |
| **[1/7]** | `01_setup.do` | Validates survey design; sets complex survey weights (`svyset [pw=weight_hh], psu(psu_id) strata(strata)`). |
| **[2/7]** | `02_elec_attributes.do` | Evaluates 7 electricity attributes: Capacity, Availability (Day/Night), Reliability (imputed zero-outage durations), Quality, Affordability (dynamic national lifeline tariff integration), Formality, and Safety. |
| **[3/7]** | `03_elec_aggregate.do` | Multi-tier horizontal index (Tier 0–5) and primary technology classification. |
| **[4/7]** | `04_cooking_attributes.do` | MECS multi-tier cooking attributes: Cooking time-weighted emissions, ventilation, safety, and fuel availability. |
| **[5/7]** | `05_cooking_aggregate.do` | Aggregate cooking tier; stove stacking and exposure dilution indices. |
| **[6/7]** | `06_analytical_enhancements.do`| Under-the-grid densification deficit, contingent valuation WTP demand curves (Grid, Solar, Cooking), and 100% mutually exclusive subsidy segments. |
| **[7/7]** | `07_export.do` | Automated matrix export: `MTF_Namibia_Summary.xlsx`, `MTF_Figures_Data.xlsx`, and `mtf_report_values.json`. |

### Step 6: Automated Graphics & Word Report Injection
Once Stata finishes exporting to `$output`, generate the 14 publication-grade figures and inject all values into the formal World Bank Word report:

```bash
# 1. Generate 14 publication charts (300 DPI, World Bank styling)
python3 stata_pipeline/scripts/visualize.py \
    --data "$output/MTF_Figures_Data.xlsx" \
    --outdir "$output/charts"

# 2. Inject calculated tokens and charts into Word diagnostic report
python3 stata_pipeline/scripts/inject_report.py \
    --json "$output/mtf_report_values.json" \
    --charts "$output/charts" \
    --template stata_pipeline/MTF_Report_Template.md \
    --output "$output/MTF_Guinea-Bissau_Report.docx"
```

---

## 4. Quick Comparison: Which Track Should I Use?

| Feature / Need | Track 1: Non-STATA User | Track 2: STATA User |
| :--- | :---: | :---: |
| **Software Required** | Free Web Browser + Python (Automatic) | Stata 17+ SE/MP + Python |
| **Target Audience** | Sector Economists, TTLs, Policy Analysts | Data Scientists, Survey Leads |
| **Input Data Required** | Single Master File (`MTF_*_Master.dta`) | 15 Raw Survey Solutions Modules |
| **Execution Method** | Double-click `run_mtf_local.bat` | Run `do <Country>_MTF_Master.do` |
| **Primary Capabilities** | Cross-tabs, Quintiles, Tariff Shocks, Excel | Raw ETL, Econometric Tiers, Word Reports |
| **Local Data Privacy** | 100% Air-Gapped (localhost) | 100% Air-Gapped (Local / OneDrive) |
| **Update Mechanism** | Double-click `update_mtf.bat` | `git pull origin main` |

---

## 5. Frequently Asked Questions (FAQ)

**Q1: Can non-Stata users run this on an airplane or in the field without internet?**  
Yes. After the one-time initial package setup (~30 seconds), the local environment runs 100% offline on `localhost`. Internet access is only required when clicking `update_mtf.bat` to pull tool updates from GitHub.

**Q2: Is our survey microdata exposed to GitHub?**  
No. The repository enforces a strict `.gitignore` policy that blocks all `.dta`, `.xlsx`, and raw survey directories. GitHub hosts open-source code only. Microdata remains securely stored on institutional World Bank drives and local air-gapped disks.

**Q3: What should I do if an error occurs in the interactive analyzer?**  
Scroll to **Module 5** at the bottom of `MTF_Interactive_Analyzer.ipynb` and run the cell. Attach the generated `mtf_diagnostic_report.txt` file to an email and send it to [bkoo@worldbankgroup.org](mailto:bkoo@worldbankgroup.org) for instant technical support.
