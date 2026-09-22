# 🌐 ESMAP Multi-Tier Framework (MTF) Country Survey Automation Blueprint
## Standard Operating Guideline: From Raw Microdata to Publication-Grade Diagnostics

**Global Lead & Principal Architect:** Bryan Bonsuk Koo (Senior Energy Specialist, TTL)  
**Program:** Energy Sector Management Assistance Program (ESMAP) | World Bank Group  
**Target Audience:** Energy Specialists, Econometricians, Data Scientists, and Research Analysts

---

## 1. Executive Rationale & The Automation Model

The Multi-Tier Framework (MTF) redefines household energy access measurement from binary grid connections and simple stove ownership into a multidimensional diagnostic of quality, reliability, capacity, duration, affordability, safety, and health. 

Historically, country-level MTF diagnostics required 3 to 6 months of ad-hoc Stata scripting, manual tabular compilation, and tedious report copying, leading to version discrepancies and human error. 

The **Namibia MTF 2024 Automation Blueprint** establishes a **modular, reproducible, and portable pipeline** that compresses data analysis, visualization, and diagnostic report generation from months to **under 3 minutes**:

```
[Raw CAPI Microdata (30+ rosters)]
               │
               ▼
[Phase 1: Master Compilation] ───────► Aggregates 4-pillar consumption, demographic headship, appliances
               │
               ▼
[Phase 2: MTF Attribute Engine] ─────► Computes 7 Electricity + 6 MECS Cooking Tiers (Tiers 0–5)
               │
               ▼
[Phase 3: Analytical Enhancements] ──► WTP cash vs installments, under-the-grid uptake, fuel stacking
               │
               ▼
[Phase 4: Multi-Matrix Export] ──────► 10-Sheet Excel Matrix + 260+ Calibrated Scalar JSON Store
               │
       ┌───────┴─────────────────────────┐
       ▼                                 ▼
[Phase 5: Publication Visuals]   [Phase 6: Automated Document Injection]
 (9 Charts at 300 DPI)            (Word .docx + Web Markdown, 100% Filled)
```

---

## 2. Standard Country Folder Architecture

To ensure turnkey portability across survey countries (e.g., Namibia ➔ Liberia ➔ Mozambique ➔ Nigeria 2024), all country repositories must adhere to the standardized directory layout:

```text
<Country_MTF_Folder>/
│
├── 00_COUNTRY_PIPELINE_GUIDELINE.md    <-- Country-specific execution protocol
│
├── Data/
│   ├── raw/                            <-- Untouched raw CAPI datasets (Survey Solutions / SurveyCTO)
│   │   ├── Household/                  <-- Household master roster & core survey sections
│   │   ├── hhroster.dta                <-- Individual demographic roster
│   │   ├── appliances.dta              <-- Appliance ownership by device code
│   │   └── clean_stoves.dta            <-- Multi-stove use roster
│   ├── wip/                            <-- Intermediate working files (harmonized, merged)
│   │   └── MTF_YYYY_HH_<Country>_Master.dta
│   └── clean/                          <-- Fully classified analytical master dataset
│       └── MTF_YYYY_HH_<Country>_Clean.dta
│
├── Do-file/
│   ├── <Country>_MTF_Master.do         <-- Master orchestrator executing do-files 00 to 07
│   ├── 00_build_master_dataset.do      <-- Ingestion, consumption aggregation, weights, rosters
│   ├── 01_setup.do                     <-- Global paths, stratification, country parameters
│   ├── 02_elec_attributes.do           <-- 7 Electricity Access Attributes
│   ├── 03_elec_aggregate.do            <-- Aggregate Electricity Tier (0–5)
│   ├── 04_cooking_attributes.do        <-- 6 MECS Cooking Attributes
│   ├── 05_cooking_aggregate.do         <-- Aggregate MECS Cooking Tier & Primary Fuel/Stove
│   ├── 06_analytical_enhancements.do   <-- WTP, under-the-grid, gender, regional disaggregations
│   ├── 07_export.do                    <-- Survey-weighted export to Excel and JSON
│   ├── MTF_Report_Template.md          <-- Master 5-chapter report template with {{PLACEHOLDER}} tags
│   └── scripts/
│       ├── visualize.py                <-- Generates all 9 publication-grade charts (300 DPI)
│       └── inject_report.py            <-- Populates Markdown & compiles publication Word .docx
│
└── Output/
    ├── MTF_<Country>_Summary.xlsx      <-- 10-sheet comprehensive statistical indicator matrix
    ├── mtf_report_values.json          <-- Calibrated indicator key-value store (260+ keys)
    ├── MTF_<Country>_Report.md         <-- Web-ready Markdown report (0 unfilled placeholders)
    ├── MTF_<Country>_Report.docx       <-- Corporate ESMAP Word publication document
    └── charts/                         <-- 9 High-resolution PNG figures (300 DPI)
        ├── 01_elec_tier_distribution.png
        ├── 02_cooking_tier_distribution.png
        ├── 03_elec_attribute_radar.png
        ├── 04_quintile_access_curve.png
        ├── 05_gender_fuel_collection_time.png
        ├── 06_grid_barriers_wtp.png
        ├── 07_stove_technology_fuels.png
        ├── 08_gender_demographics_access.png
        └── 09_regional_access_gap.png
```

---

## 3. Demarcation: Universal MTF Core vs. Country-Specific Customization

The core strength of this pipeline is strict separation of concerns. While **80% of the analytical framework is universal**, **20% must be adapted** to local institutions, currencies, and sampling designs.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   UNIVERSAL MTF CORE (DO NOT MODIFY)                   │
├────────────────────────────────────────────────────────────────────────┤
│ • 02_elec_attributes.do      : Multi-tier thresholds (3W, 50W, 200W...) │
│ • 03_elec_aggregate.do       : Aggregate tier min() logic              │
│ • 04_cooking_attributes.do   : ISO Tier ventilation, safety, stacking  │
│ • 05_cooking_aggregate.do    : Aggregate MECS tier algorithm           │
│ • MTF Methodology Chapter    : Multi-tier definitions, attribute radar │
│ • Output Engine & Charting   : Stacked bars, radars, income curves     │
│ • Document Injector (.docx)  : ESMAP corporate styling & XML rendering │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               COUNTRY-SPECIFIC CUSTOMIZATION (ADAPT HERE)               │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Survey Weights & Stratification (00_build_master_dataset.do)        │
│    - Sampling strata (e.g. Namibia: Region × Locality; Liberia:        │
│      County × Locality × Grid EAs).                                    │
│ 2. Consumption Expenditure Aggregation (00_build_master_dataset.do)     │
│    - Local food item rosters, local currency units (NAD, LRD, USD),   │
│      durables depreciation, recall periods.                            │
│ 3. Power Sector & Utility Topology (06_analytical_enhancements.do)     │
│    - National utilities (NamPower/REDs vs. LEC in Liberia).            │
│    - Off-grid programs (Solar Revolving Fund vs. RREA mini-grids).     │
│ 4. Administrative Subdivisions (06_analytical_enhancements.do)         │
│    - Admin 1 units: 14 Regions (Namibia) vs. 15 Counties (Liberia).   │
│ 5. Macroeconomic Context & Sector Narrative (MTF_Report_Template.md)   │
│    - Country GDP per capita, Gini coefficient, national compacts      │
│      (e.g., Harambee Plan vs. Liberia PAPD / ASCENT Liberia).         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Automated Country Calibration & Porting Guide

Instead of manually editing Stata scripts, the pipeline provides the **MTF Auto-Calibrator** (`mtf_calibrator.py` / `mtf_calibrator.exe`) which scans the microdata, discovers variables, deploys calibrated country Stata scripts, and populates the report template — all in under 10 seconds.

### Option A: Fully Automated Calibration (Recommended)

Run the auto-calibrator from CLI (or run `mtf_calibrator.exe` on Windows):

```bash
# Minimum required arguments:
python3 "00_MTF_Country_Pipeline_Standard/Tools/mtf_calibrator.py" \
  --country-dir "/path/to/Country_Folder/06. Data Analysis" \
  --country-name "Liberia" \
  --currency "LRD" \
  --exchange-rate 192.5

# Full options — with cookstove CSV and regional module:
python3 "00_MTF_Country_Pipeline_Standard/Tools/mtf_calibrator.py" \
  --country-dir "/path/to/Country_Folder/06. Data Analysis" \
  --country-name "Liberia" \
  --currency "LRD" \
  --exchange-rate 192.5 \
  --cookstove-config "00_MTF_Country_Pipeline_Standard/Tools/cookstove_calibration.csv" \
  --survey-year 2024 \
  --include-regional
```

**All available arguments:**

| Argument | Required | Description |
|:---|:---:|:---|
| `--country-dir` | ✅ | Path to the country's `06. Data Analysis` folder |
| `--country-name` | — | Country name (e.g. `Liberia`). Auto-detected from folder name if not set. |
| `--currency` | — | Local currency code (e.g. `LRD`, `NAD`, `NGN`) |
| `--exchange-rate` | — | Survey-period USD exchange rate |
| `--cookstove-config` | — | Path to `cookstove_calibration.csv`. **Auto-located from `Tools/`** if not set. |
| `--include-regional` | — | Flag: if set, injects the Admin 1 regional module into the deployed report template |
| `--admin1-unit` | — | Override Admin 1 unit label (e.g. `county`, `region`, `province`). Auto-detected if not set. |
| `--survey-year` | — | Survey year for report headers (default: `2024`) |
| `--auto-confirm` / `-y` | — | Skip confirmation prompt (for scripted/batch execution) |

**What the Auto-Calibrator does:**
1. **Directory Discovery**: Locates clean microdata folders (skipping `wip` or `pilot` directories).
2. **Schema & Variable Detection**: Inspects `.dta` headers to auto-detect weights, PSU, locality, and Admin 1 units.
3. **Cookstove Calibration Loading** (`--cookstove-config`): Reads `cookstove_calibration.csv` to generate:
   - The `mainstove` classification block and `cs_emit_tier` ISO tier block in `04_cooking_attributes.do`
   - Box 3 "Typology of Cookstoves" in the report template
   - Table 3.1 cookstove distribution rows with `{{PLACEHOLDER}}` tags
4. **Code Generation & Patching**: Generates `<Country>_MTF_Master.do`, `00_build_master_dataset.do`, `01_setup.do`, `06_analytical_enhancements.do`, and `07_export.do`.
5. **Report Template Deployment**: Copies `MTF_Report_Template.md` and injects:
   - `{{COUNTRY_NAME}}` → country name throughout the template
   - `{{SURVEY_YEAR}}`, `{{ADMIN1_COUNT}}`, `{{ADMIN1_UNIT_LABEL_PLURAL}}` → contextual metadata
   - `{{COOKSTOVE_TYPOLOGY_TABLE}}` → Box 3 table from CSV
   - `{{COOKSTOVE_STATS_TABLE_ROWS}}` → Table 3.1 rows from CSV
   - Optionally the full Admin 1 Regional Analysis Module (if `--include-regional` is set)

---

### Cookstove Calibration — Expert Review Required

Before running the calibrator for a new country, the coordinator must review `Tools/cookstove_calibration.csv`:

```
questionnaire_code, stove_description, iso_emission_tier, efficiency_tier, stove_group, primary_fuel
```

- **`questionnaire_code`**: The numeric value codes from the country's Section G stove question.
- **`iso_emission_tier`**: ISO 19867 emission tier (0–5). **Must be confirmed with a cookstove expert.**
- **`efficiency_tier`**: ISO efficiency tier (0–5). **Must be confirmed with a cookstove expert.**
- **`stove_group`**: Internal category (`open_fire`, `traditional`, `ics`, `clean_gas`, `clean_electric`, `clean_solar`, `clean_bio`, `transitional_bio`, `other`).

The template CSV is pre-filled with standard Namibia/Liberia defaults. Modify the `questionnaire_code` column to match the new country's questionnaire. Request expert confirmation of `iso_emission_tier` before finalizing.

---

### Regional Analysis Module — Optional

By default, the report template **does not include** Admin 1 regional disaggregated analysis. This is excluded because:
- Sample sizes per Admin 1 unit vary significantly across countries
- Regional section requires manual narrative review
- Not all clients request this level of disaggregation

**To include the regional module:**
- Option 1 (Automatic): Add `--include-regional` to the calibrator command. The module is auto-populated with detected Admin 1 units and injected into Section 2.2.
- Option 2 (Manual): After running the calibrator, copy the relevant sections from `Do-file/MTF_Regional_Analysis_Module.md` and paste them into Section 2.2 of the deployed report template.

---

### Option B: Compiling the Standalone Windows Executable (`mtf_calibrator.exe`)

For team members working on standard World Bank Windows laptops without Python installed:
1. Navigate to `00_MTF_Country_Pipeline_Standard/Tools/`.
2. Double-click `build_exe.bat` (or run `pip install pyinstaller pandas openpyxl && pyinstaller --onefile mtf_calibrator.py`).
3. The standalone portable binary will be built in `Tools/dist/mtf_calibrator.exe`.

---

### Option C: Executing the One-Click Country Pipeline

Once calibrated, run the 3-step execution pipeline:
```bash
# 1. Execute Stata Master Pipeline (builds datasets, runs attributes, exports summary matrix & JSON)
stata-se -b do "Do-file/<Country>_MTF_Master.do"

# 2. Render publication-grade figures (9 charts at 300 DPI)
python3 "Do-file/scripts/visualize.py"

# 3. Inject indicators into diagnostic report (Word .docx + Markdown)
python3 "Do-file/scripts/inject_report.py"
```

---

### Coordinator Manual Tasks (After Calibration)

The following report sections require **manual completion** by the coordinator — they cannot be automated:

| Section | Action Required |
|:---|:---|
| **Acknowledgements** | Fill in: Government ministry, utility partners, survey team, enumerator count, total households |
| **Table of Abbreviations** | Add country-specific acronyms (utility name, regulatory body, program names, currency code) |
| **Dev. & Energy Challenge** | Write country-specific narrative: GDP, Gini, development plan, electrification commitment |
| **Country Context (Section 1.1)** | Describe national power sector: regulatory body, utility, distribution entities, tariff schedule |
| **Chapter 5 Policy Recommendations** | Name the specific ministry, utility, and donor programs for each pillar |
| **Annex 2 — Sampling Strategy** | Confirm and update the strata count and sampling design description |
| **Cookstove ISO Tier confirmation** | Expert review of `cookstove_calibration.csv` before running the pipeline |

---



## 5. Summary Matrix & Indicator Nomenclature

The pipeline exports **260+ calibrated indicators** across 10 structured dimensions in `MTF_<Country>_Summary.xlsx`:

| Sheet # | Sheet Name | Contents |
|:---:|:---|:---|
| **1** | `Electricity_Tiers` | Tiers 0 to 5 distribution across National, Urban, Rural |
| **2** | `Cooking_Tiers` | Modern Energy Cooking Services (MECS) Tiers 0 to 5 |
| **3** | `Disagg_UrbanRural` | Grid connection, off-grid solar, appliance ownership, outages |
| **4** | `Disagg_Quintile` | Access rates across expenditure quintiles Q1 (poorest) to Q5 (richest) |
| **5** | `Disagg_Gender` | Electricity & cooking tiers by Female- vs. Male-Headed households |
| **6** | `Grid_Barriers_WTP` | Connection barriers, WTP upfront vs. 12-month installments |
| **7** | `Solar_WTP_Issues` | Solar lantern/SHS adoption, capacity constraints, fund awareness |
| **8** | `Appliances_Use` | Appliance ownership by load level (very low to very high load) |
| **9** | `Regional_Disagg` | Subnational electrification and technology rates across Admin 1 units |
| **10** | `Gender_Profiles` | Head age, education, widowhood, credit access, cooking/fuel time |

---

## 6. Execution Troubleshooting & Best Practices

1. **Survey Weight Syntax in Stata:**  
   Always use survey-weighted commands (`svyset [pw=hh_wt], strata(strata) psu(ea_id)`) or survey-weighted proportions (`svy: mean ...` or `mean ... [pw=hh_wt]`). Avoid unweighted `summarize` for report-bound indicators.
2. **String Matching in Installment Choices:**  
   Avoid long `inlist()` expressions with 10+ string variants in Stata. Instead, use clean regex matching:
   `replace fuel_buy_freq = 15 if regexm(lower(SEC_I_Q07_oth), "year")`
3. **Word Document XML Preservation:**  
   The `inject_report.py` script renders the Word document directly from the injected Markdown file, guaranteeing that table widths, callout borders, and 300-DPI charts are rendered cleanly without Microsoft Word XML corruption.

---

## 7. Team Collaboration, Version Control & Data Privacy (GitHub Monorepo)

To collaborate with data scientists and country economists across different survey countries, the pipeline is version-controlled in a centralized private GitHub repository:

**Repository URL:** [https://github.com/bkoo0824/esmap-mtf-pipeline](https://github.com/bkoo0824/esmap-mtf-pipeline)

### Architecture: Strict Code/Data Separation
- **Data Layer (OneDrive / SharePoint):** All survey microdata (`*.dta`, `*.xlsx`, `Data/clean`, `Data/wip`) remains strictly on your local/shared institutional OneDrive under World Bank access controls. Microdata is NEVER uploaded to GitHub.
- **Code Layer (GitHub):** All Stata do-files (`00` to `07`), Python tools, cookstove configuration forms, and Markdown templates are version-controlled in the private Monorepo.
- **Bridge (`c(username)`):** Stata master scripts dynamically resolve data paths based on the analyst's OS username (e.g. `WB453090`, `bryan`, `wb123456`).

### Automated Data Privacy Guard (Pre-Commit Hook)
A pre-commit security hook (`.git/hooks/pre-commit`) actively intercepts every commit:
- Scans staged files for microdata formats (`.dta`, `.xlsx`, `.sav`, `.sas7bdat`).
- Scans file sizes: strictly aborts commits containing any file > 5 MB.
- Prevents accidental `git add .` data leaks.

### 1-Command CLI Helper (`git_sync.py`)
Run the helper tool from the root of the repository:

```bash
# Check repository health and confirm zero data files exist in the repo:
python3 git_sync.py --status

# Validate safety, stage safe code, commit, and push in one step:
python3 git_sync.py --sync -m "Update cooking attribute tiers for Nigeria"

# Pull latest revisions from team members:
python3 git_sync.py --pull

# Import updated do-files from your local analysis directory into the repository:
python3 git_sync.py --import-country "Nigeria_2024" --source "/path/to/07. Data Analysis/Do-file"
```

### Data Scientist Onboarding Checklist
1. **Clone Repo:** `git clone git@github.com:bkoo0824/esmap-mtf-pipeline.git`
2. **Add OneDrive Path:** Open `Countries/<Country>/<Country>_MTF_Master.do` and add your username block in Section 1:
   ```stata
   if c(username) == "wb123456" {
       global user "C:/Users/wb123456/OneDrive - WBG/06. Data Analysis"
   }
   ```
3. **Branch & PR:** Always create a feature branch (`git checkout -b feature/country-fix`), commit changes, push, and open a Pull Request against `main`.
