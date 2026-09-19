# ESMAP Multi-Tier Framework (MTF) Pipeline Monorepo

**World Bank Group | Energy Sector Management Assistance Program (ESMAP)**  
*Global Survey & Access Analytics Team*

This repository houses the version-controlled Stata econometric do-files, Python figure-generation scripts, and automated diagnostic report generators for national **Multi-Tier Framework (MTF)** household energy access diagnostics.

---

## 🔒 Data Privacy & Architecture Protocol

### Strict Code-Only Policy
Under no circumstances is World Bank survey microdata (`*.dta`, `*.xlsx`, `Data/`) stored or committed in this repository.
- **Microdata Storage:** Stored exclusively on institutional **OneDrive / SharePoint** under World Bank access controls.
- **Code Repository:** Version-controlled exclusively on **GitHub**.
- **Local Bridge:** Stata master do-files (`<Country>_MTF_Master.do`) bridge code and data dynamically using `c(username)` path blocks.

---

## 📂 Repository Topology

```
esmap-mtf-pipeline/
│
├── 00_Standard_Template/         <-- Master Pipeline Engine
│   ├── Do-file/                  <-- Core modules (00 to 07) & scripts/
│   ├── Tools/                    <-- mtf_calibrator.py, cookstove forms, EXE builder
│   └── README_PIPELINE_GUIDELINE.md
│
├── Countries/                    <-- Country Implementations
│   ├── Liberia_2024/             <-- 15 counties, LRD @ 192.5
│   └── Nigeria_2024/             <-- 37 states, NGN @ 1,580, 26 cookstove types
│
├── git_sync.py                   <-- Automated privacy check & sync helper
└── .github/
    └── hooks/pre-commit          <-- Automated pre-commit data leak blocker
```

---

## 🚀 Team Collaboration Workflow

### For Data Scientists & Consultants

1. **Clone the Repository:**
   ```bash
   git clone git@github.com:<your-org>/esmap-mtf-pipeline.git
   cd esmap-mtf-pipeline
   ```

2. **Configure Your Local Path in Stata Master Do-File:**
   Open `Countries/<Country>/<Country>_MTF_Master.do` and add your World Bank username and local OneDrive data path:
   ```stata
   * --- Data Scientist: Windows ---
   if c(username) == "wb123456" {
       global user "C:/Users/wb123456/OneDrive - WBG/06. Data Analysis"
   }
   ```

3. **Create a Feature Branch:**
   ```bash
   git checkout -b feature/country-topic-update
   ```

4. **Synchronize & Push Safely:**
   ```bash
   # Run the sync helper (automatically checks for data leaks before staging):
   python3 git_sync.py --sync -m "Update cooking attribute thresholds for Nigeria"
   ```

5. **Open a Pull Request:**
   Submit a PR on GitHub for review by the Task Team Leader.

---

## 🛠️ Sync Helper Commands (`git_sync.py`)

| Command | Purpose |
|:---|:---|
| `python3 git_sync.py --status` | Run repository safety check and view git status |
| `python3 git_sync.py --sync -m "message"` | Safety scan, stage safe files, commit, and push |
| `python3 git_sync.py --pull` | Safely pull latest commits from remote |
| `python3 git_sync.py --import-country <Name> --source <Path>` | Import country do-files from local data analysis directory |

---
*Maintained by Bryan Koo, Senior Energy Specialist, World Bank ESMAP.*
