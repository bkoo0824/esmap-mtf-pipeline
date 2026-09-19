# 📘 ESMAP MTF Country Diagnostic Pipeline
## A Beginner's Step-by-Step Guide for Energy Specialists & Country Coordinators

**World Bank Group | Energy Sector Management Assistance Program (ESMAP)**  
*For Task Team Leaders, Country Coordinators, and Energy Economists*

---

## 🌟 Welcome! What Does This Pipeline Do?

Welcome to the **ESMAP Multi-Tier Framework (MTF) Country Diagnostic Pipeline**. 

You do **not** need to be a data scientist, programmer, or Git expert to use these tools! This system was designed to take raw, complex household survey datasets and turn them into finished diagnostic reports automatically in **three simple steps**:

```
 ┌────────────────────────┐      ┌────────────────────────┐      ┌────────────────────────┐
 │   1. CLEAN SURVEY      │      │    2. STATA MASTER     │      │   3. CHARTS & REPORT   │
 │   Survey Solutions .dta│ ───► │  Calculates 260+ Multi-│ ───► │  9 publication figures │
 │   files on OneDrive    │      │  Tier access indicators│      │  + completed Word doc  │
 └────────────────────────┘      └────────────────────────┘      └────────────────────────┘
```

Everything is automated:
1. **The Auto-Calibrator** reads your survey microdata and creates all country-specific do-files in under 10 seconds.
2. **The Stata Pipeline** calculates multi-tier access tiers (Tier 0 to Tier 5), electricity capacity, reliability, cooking exposure tiers, affordability, and willingness to pay.
3. **The Report Generator** injects every single number, table, and 300-DPI publication chart directly into a ready-to-publish Word (`.docx`) report.

---

## 💻 1. What Software Do You Need to Install? (One-Time Setup)

You only need **three standard programs** installed on your World Bank or personal laptop:

### Program 1: Stata (SE or MP, Version 16, 17, or 18)
- **What it does:** Runs the econometric calculations and builds the MTF indicators.
- **How to get it:** Standard World Bank software available via WBG AppPortal / Software Center.
- **Setup check:** In Stata, type `set maxvar 10000, permanently` in the command window and press Enter.

---

### Program 2: Python 3 (For Publication Figures & Word Report Injection)
Python runs two helper scripts: one creates the 9 charts (`visualize.py`), and one fills out the Word document (`inject_report.py`).

1. **Download Python:**
   - Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest Python 3 installer for Windows/Mac.
2. **CRITICAL INSTALL STEP (Windows Users):**
   - On the very first screen of the installer, **check the box that says:**  
     ☑️ **"Add Python to PATH"** (at the bottom).
   - Then click **"Install Now"**.
3. **Install the Required Libraries (One Single Command):**
   - Open your terminal or Windows Command Prompt (`cmd.exe` or PowerShell).
   - Type this command and press Enter:
     ```bash
     pip install pandas openpyxl matplotlib seaborn python-docx pillow
     ```
   *(Or navigate to the repo folder and run: `pip install -r requirements.txt`)*

> [!TIP]
> **No Python on your machine? No problem!**  
> If you are on a restricted World Bank laptop without Python, you can run the standalone **`mtf_calibrator.exe`** in the `Tools/` folder directly by double-clicking it without installing Python!

---

### Program 3: GitHub Desktop (The Easiest Way to Share Code)
Instead of typing complicated Git commands in a black terminal window, use **GitHub Desktop**—a free, visual program with buttons:

1. **Download GitHub Desktop:** Go to [desktop.github.com](https://desktop.github.com/) and install it.
2. **Sign In:** Log in with your GitHub account (the one you shared with the TTL).
3. **Clone the Pipeline:**
   - In GitHub Desktop, click **File > Clone Repository...**
   - Select `bkoo0824/esmap-mtf-pipeline`.
   - Choose a local folder on your computer (e.g. `C:\Users\your_username\Documents\GitHub\`).
   - Click **Clone**.

---

## 🔒 The Golden Rule: Data Privacy & Where Files Live

World Bank survey datasets contain confidential household information (GPS coordinates, family names, income). To protect client confidentiality:

| Where does it go? | Content Type | Examples | Allowed on GitHub? |
|:---|:---|:---|:---:|
| **Local OneDrive / Shared Drive** | Microdata & Datasets | `*.dta`, `*.xlsx`, `Data/clean/`, `Data/wip/` | ❌ **NEVER** |
| **Local OneDrive / Shared Drive** | Final Generated Deliverables | `Output/MTF_Summary.xlsx`, Word docs | ❌ **NEVER** |
| **GitHub Repository** | Code, Scripts, Templates | `.do`, `.py`, `.md`, `cookstove_calibration.csv` | ✅ **YES** |

> [!NOTE]
> **Built-in Security Guard:** The repository has an automatic security hook installed. If you ever accidentally try to commit a `.dta` or `.xlsx` file, the system will actively reject the commit and alert you with an error message.

---

## 🚶 Step-by-Step Workflow: Processing a Country Survey

### Step 1: Set Up Your Survey Data Folder on OneDrive

In your country folder on OneDrive, make sure you have this simple folder structure:

```
📁 Country_Folder (e.g., 06. Data Analysis/)
│
├── 📁 Data/
│   ├── 📁 clean/       <-- Copy your clean Survey Solutions .dta files here
│   └── 📁 wip/         <-- Leave empty (scratch space for Stata merges)
│
├── 📁 Do-file/         <-- Where the calibrated Stata do-files will live
└── 📁 Output/          <-- Where final charts and Word reports will be created
```

---

### Step 2: Calibrate the Pipeline for Your Country (Takes 10 Seconds)

Instead of manually editing 8 different Stata files, run the **Auto-Calibrator**:

1. Open your terminal / command prompt.
2. Run this command (adjusting the paths and country name):
   ```bash
   python3 "Tools/mtf_calibrator.py" \
     --country-dir "/path/to/your/country/06. Data Analysis" \
     --country-name "Liberia" \
     --currency "LRD" \
     --exchange-rate 192.5
   ```
   *(On Windows, you can also use `mtf_calibrator.exe`)*

**What the Calibrator does automatically:**
- Scans all `.dta` survey rosters.
- Detects the sampling weights (`HH_weights`, `HHsampleweights`), EA clusters, and Urban/Rural indicators.
- Discovers the subnational Admin 1 units (e.g. 15 counties for Liberia, 37 states for Nigeria).
- Writes customized Stata scripts directly into your `Do-file/` folder.

---

### Step 3: Review the Cookstove Calibration Form

Before running the calculations, check the cookstove options:
1. In the `Tools/` folder (or inside your country folder), open **`cookstove_calibration.csv`** in Microsoft Excel.
2. Check that the questionnaire codes in the first column match your survey questionnaire (Section G, question 5).
3. Have your local energy or clean cooking specialist confirm the **ISO Emission Tier** (Tier 0 to Tier 5) for each stove type.
4. Save the file (keep it as CSV format).

---

### Step 4: Run the Stata Pipeline (The Core Calculations)

1. Open **Stata**.
2. In Stata, open your country's master file:  
   `Do-file/<Country>_MTF_Master.do` (for example, `Liberia_MTF_Master.do`).
3. Look at **Section 1 (User & Path Setup)** at the top of the file:
   ```stata
   * --- Add your World Bank username and OneDrive path ---
   if c(username) == "wb123456" {
       global user "C:/Users/wb123456/OneDrive - WBG/06. Data Analysis"
   }
   ```
   Replace `wb123456` with your Windows username, and put the path to your folder.
4. Click the **Execute (Do)** button in Stata (or press `Ctrl + D`).
5. **Sit back and relax!** Stata will run modules `00` through `07`:
   - It compiles household size and expenditure quintiles.
   - It calculates electricity capacity, availability, reliability, quality, and safety tiers.
   - It calculates cooking exposure tiers, ventilation, convenience, and fuel collection time.
   - It exports **`MTF_<Country>_Summary.xlsx`** (260+ indicators across 10 sheets) and **`mtf_report_values.json`** into your `Output/` folder!

---

### Step 5: Generate Publication Figures & the Word Report

Once Stata finishes, generate the visual figures and Word document:

1. Open your terminal or Command Prompt in the `Do-file/` folder.
2. **Generate the 9 Publication Figures:**
   ```bash
   python scripts/visualize.py
   ```
   *Result:* 9 high-resolution charts are saved in `Output/charts/` (Stacked Access Bars, Radar Spider Charts, Income Quintile Curves, etc.).

3. **Inject Indicators into the Diagnostic Report:**
   ```bash
   python scripts/inject_report.py
   ```
   *Result:* The script reads `MTF_Report_Template.md`, fills in all `{{INDICATOR}}` tags with the exact numbers calculated by Stata, embeds the charts, and outputs:
   - **`MTF_<Country>_Diagnostic_Report.docx`** (Finished Microsoft Word document!)
   - **`MTF_<Country>_Diagnostic_Report.md`** (Markdown version)

---

### Step 6: Collaborate & Sync with Your Team via GitHub

If you modified a do-file, adjusted a threshold, or improved a calculation:

#### Option A: Using GitHub Desktop (Visual & Easy)
1. Open **GitHub Desktop**.
2. It will automatically show the files you changed on the left.
3. In the bottom-left box:
   - Type a short summary (e.g., *"Updated cooking tiers for Nigeria"*).
4. Click **Commit to main** (or commit to your feature branch).
5. Click **Push origin** at the top right.  
   *Done! Your changes are backed up and shared with the team.*

#### Option B: Using the `git_sync.py` Helper (Terminal)
If you prefer the command line:
```bash
python3 git_sync.py --sync -m "Updated cooking tiers for Nigeria"
```
The helper automatically scans for data leaks, stages your code, commits, and pushes in a single keystroke.

---

## ❓ Frequently Asked Questions & Troubleshooting

### Q1: Stata says `no room to add more variables`
- **Fix:** Type `set maxvar 10000, permanently` in Stata's command bar, press Enter, and restart Stata.

### Q2: Stata says `file ... not found`
- **Fix:** Check Section 1 of `<Country>_MTF_Master.do`. Make sure the path in `global user` points to the exact folder on your computer where `Data/` and `Do-file/` are located. Remember to use forward slashes (`/`) even on Windows!

### Q3: In Command Prompt, typing `python` gives an error: `'python' is not recognized`
- **Fix:** When Python was installed, the checkbox "Add Python to PATH" was not selected. Re-run the Python installer from [python.org](https://www.python.org/), choose **Modify**, and make sure **"Add Python to environment variables / PATH"** is checked.

### Q4: How do I change the local currency or exchange rate?
- **Fix:** In `<Country>_MTF_Master.do`, lines 25–28:
  ```stata
  global currency   "LRD"     // Put your 3-letter currency code
  global usd_rate   192.5     // Put survey period exchange rate per USD
  ```

### Q5: Can I open and edit `cookstove_calibration.csv` in Excel?
- **Yes!** Double-click it to open in Excel. Make your edits to the codes and descriptions. When saving, select **CSV (Comma delimited) (*.csv)**.

---

## 📞 Support & Contacts
If you encounter any issues or need custom variables added for your country survey, please contact:
- **Bryan Koo** (Senior Energy Specialist, World Bank ESMAP) — `bkoo@worldbank.org`
- **ESMAP Energy Access Team** — Global MTF Survey Diagnostics Helpdesk
