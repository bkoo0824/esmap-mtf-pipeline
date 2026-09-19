#!/usr/bin/env python3
"""
mtf_calibrator.py — MTF Country Survey Auto-Calibrator & Pipeline Generator
=============================================================================
Author: Bryan Koo / Antigravity AI Executive Secretariat
World Bank ESMAP | Energy Global Practice

Purpose:
  1. Inspects raw country survey directories.
  2. Detects Master Household .dta, rosters, weight structures, and Admin 1 geographic units.
  3. Displays an interactive confirmation diagnostic.
  4. Automatically patches and generates country-specific Do-files, scripts, and directories.

Can be run directly with Python or compiled to a standalone Windows .exe via PyInstaller.
"""

import os
import sys
import re
import shutil
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


STANDARD_ROSTERS = [
    "hhroster.dta", "cookstoves.dta", "appliance.dta", "food.dta",
    "fuel_consumption.dta", "fuel_h11.dta", "solar_c_device.dta",
    "time_use.dta", "nonfood_1mon.dta", "nonfood_12mon.dta"
]


class CookstoveLoader:
    """Reads cookstove_calibration.csv and generates do-file code and report tables."""

    DEFAULT_ROWS = [
        {"questionnaire_code": "1,2", "stove_description": "Three-Stone / Open Fire",
         "iso_emission_tier": "0", "efficiency_tier": "0", "stove_group": "open_fire",
         "primary_fuel": "Gathered firewood", "stat_key_nat": "STOVE_3STONE_N",
         "stat_key_urb": "STOVE_3STONE_U", "stat_key_rur": "STOVE_3STONE_R"},
        {"questionnaire_code": "3,5,22", "stove_description": "Traditional / Local Stove",
         "iso_emission_tier": "0", "efficiency_tier": "0", "stove_group": "traditional",
         "primary_fuel": "Wood / Charcoal", "stat_key_nat": "STOVE_TRAD_N",
         "stat_key_urb": "STOVE_TRAD_U", "stat_key_rur": "STOVE_TRAD_R"},
        {"questionnaire_code": "4,6,7,8,9,20,21", "stove_description": "Improved Cookstove (ICS)",
         "iso_emission_tier": "3", "efficiency_tier": "2", "stove_group": "ics",
         "primary_fuel": "Firewood / Charcoal", "stat_key_nat": "STOVE_ICS_N",
         "stat_key_urb": "STOVE_ICS_U", "stat_key_rur": "STOVE_ICS_R"},
        {"questionnaire_code": "10,11,12,13,14,23", "stove_description": "Clean Fuel: LPG / Biogas",
         "iso_emission_tier": "4", "efficiency_tier": "4", "stove_group": "clean_gas",
         "primary_fuel": "Bottled LPG", "stat_key_nat": "STOVE_CLEAN_N",
         "stat_key_urb": "STOVE_CLEAN_U", "stat_key_rur": "STOVE_CLEAN_R"},
        {"questionnaire_code": "19", "stove_description": "Clean Fuel: Electric Stove",
         "iso_emission_tier": "5", "efficiency_tier": "5", "stove_group": "clean_electric",
         "primary_fuel": "Grid electricity", "stat_key_nat": "STOVE_ELEC_N",
         "stat_key_urb": "STOVE_ELEC_U", "stat_key_rur": "STOVE_ELEC_R"},
    ]

    def __init__(self, csv_path: Optional[Path] = None):
        self.rows = []
        if csv_path and csv_path.exists():
            self._load_csv(csv_path)
        else:
            if csv_path:
                print(f"[WARN] cookstove_calibration.csv not found at {csv_path} — using built-in defaults.",
                      file=sys.stderr)
            self.rows = self.DEFAULT_ROWS

    def _load_csv(self, path: Path):
        import csv
        with open(path, encoding="utf-8") as f:
            # Skip comment lines starting with #
            lines = [l for l in f if not l.lstrip().startswith("#")]
        reader = csv.DictReader(lines)
        self.rows = [r for r in reader if r.get("questionnaire_code", "").strip()]
        print(f"  ✓ Cookstove calibration: {len(self.rows)} stove types loaded from {path.name}")

    def generate_typology_table(self) -> str:
        """Returns Box 3 markdown table content."""
        lines = ["| Cookstove Type | Primary Fuel Used | ISO Emission Tier |",
                 "| :--- | :--- | :---: |"]
        for row in self.rows:
            if row.get("stove_group", "") == "other":
                continue
            tier = row.get("iso_emission_tier", "—").strip()
            tier_label = f"Tier {tier}" if tier.isdigit() else "—"
            lines.append(f"| **{row['stove_description']}** | {row['primary_fuel']} | {tier_label} |")
        return "\n".join(lines)

    def generate_stats_table_rows(self) -> str:
        """Returns Table 3.1 rows using {{PLACEHOLDER}} tags."""
        lines = []
        for row in self.rows:
            if row.get("stove_group", "") == "other":
                continue
            tier = row.get("iso_emission_tier", "—").strip()
            tier_label = f"Tier {tier}" if tier.isdigit() else "—"
            nat = row.get("stat_key_nat", "—").strip()
            urb = row.get("stat_key_urb", "—").strip()
            rur = row.get("stat_key_rur", "—").strip()
            desc = row["stove_description"]
            fuel = row["primary_fuel"]
            lines.append(
                f"| **{desc}** | "
                "`{{" + nat + "}}` | `{{" + urb + "}}` | `{{" + rur + "}}` | "
                f"{fuel} | {tier_label} |"
            )
        return "\n".join(lines)


    def generate_mainstove_stata(self) -> str:
        """Returns Stata replace mainstove = ... block."""
        group_to_int = {
            "open_fire": 1, "traditional": 2, "ics": 3,
            "clean_gas": 4, "clean_electric": 5, "clean_solar": 6,
            "clean_bio": 7, "transitional_bio": 8, "other": 555
        }
        lines = ["capture drop mainstove", "gen mainstove = ."]
        for row in self.rows:
            codes = row.get("questionnaire_code", "").strip().strip('"')
            group = row.get("stove_group", "other").strip()
            val = group_to_int.get(group, 555)
            codes_list = ", ".join(c.strip() for c in codes.split(",") if c.strip())
            if codes_list:
                lines.append(f"\treplace mainstove = {val} if inlist(SEC_G_Q05, {codes_list})")
        return "\n".join(lines)

    def generate_emit_tier_stata(self) -> str:
        """Returns Stata cs_emit_tier assignment block."""
        group_to_int = {
            "open_fire": 1, "traditional": 2, "ics": 3,
            "clean_gas": 4, "clean_electric": 5, "clean_solar": 6,
            "clean_bio": 7, "transitional_bio": 8, "other": 555
        }
        # Build mainstove_val -> iso_tier mapping
        tier_map: dict = {}
        for row in self.rows:
            group = row.get("stove_group", "other").strip()
            val = group_to_int.get(group, 555)
            tier = row.get("iso_emission_tier", "").strip()
            if tier.isdigit() and val not in tier_map:
                tier_map[val] = int(tier)
        # Group by tier value
        from collections import defaultdict
        by_tier: dict = defaultdict(list)
        for mv, tv in tier_map.items():
            by_tier[tv].append(mv)
        lines = ["capture drop cs_emit_tier", "gen cs_emit_tier = ."]
        for tv in sorted(by_tier.keys()):
            mvs = by_tier[tv]
            codes = ", ".join(str(m) for m in sorted(mvs))
            lines.append(f"\treplace cs_emit_tier = {tv} if inlist(mainstove, {codes})")
        lines.append('\tlab var cs_emit_tier "Stove ISO Emission Tier (0-5)"')
        return "\n".join(lines)




class MTFScanner:
    def __init__(self, country_dir: Path):
        self.country_dir = country_dir.resolve()
        self.raw_dir: Optional[Path] = None
        self.master_dta: Optional[Path] = None
        self.rosters_found: List[str] = []
        self.rosters_missing: List[str] = []
        self.params: Dict[str, Any] = {}

    def locate_data_dir(self) -> bool:
        """Find the clean household survey directory."""
        candidates = []
        # Search parent and current directory for survey clean data
        search_roots = [self.country_dir]
        if self.country_dir.parent != self.country_dir:
            search_roots.append(self.country_dir.parent)

        for s_root in search_roots:
            for root, dirs, files in os.walk(s_root):
                rpath = Path(root)
                # Ignore wip, temp, and pilot folders
                if any(x in str(rpath).lower() for x in ['/wip', 'wip_hh', 'pilot']):
                    continue
                dta_files = [f for f in files if f.endswith('.dta')]
                if len(dta_files) >= 5:
                    matches = sum(1 for f in dta_files if f.lower() in STANDARD_ROSTERS)
                    is_clean = 1 if 'clean' in str(rpath).lower() else 0
                    is_hh = 1 if 'household' in str(rpath).lower() else 0
                    candidates.append((rpath, is_clean, is_hh, matches, len(dta_files)))

        if not candidates:
            return False

        # Prioritize: clean folder, household folder, roster matches, total files
        candidates.sort(key=lambda x: (x[1], x[2], x[3], x[4]), reverse=True)
        self.raw_dir = candidates[0][0]
        return True

    def scan_datasets(self) -> Dict[str, Any]:
        """Scan .dta files in raw directory and detect schemas."""
        if not self.raw_dir or not self.raw_dir.exists():
            raise FileNotFoundError(f"Data directory not found in {self.country_dir}")

        all_dta = list(self.raw_dir.glob("*.dta"))
        dta_names = [f.name.lower() for f in all_dta]

        found = []
        missing = []
        for r in STANDARD_ROSTERS:
            if r == "appliance.dta":
                if "appliance.dta" in dta_names:
                    found.append("appliance.dta")
                elif "appliances.dta" in dta_names:
                    found.append("appliances.dta")
                else:
                    missing.append("appliance.dta")
            elif r in dta_names:
                found.append(r)
            else:
                missing.append(r)
        self.rosters_found = found
        self.rosters_missing = missing

        master_candidates = []
        for f in all_dta:
            fname = f.name.lower()
            if any(k in fname for k in ["household", "master", "final"]):
                master_candidates.append(f)

        if not master_candidates:
            master_candidates = sorted(all_dta, key=lambda x: x.stat().st_size, reverse=True)

        self.master_dta = master_candidates[0]
        self._inspect_master_schema()
        return self.params

    def _inspect_master_schema(self):
        self.params["master_filename"] = self.master_dta.name if self.master_dta else "MTF_Household.dta"
        self.params["num_variables"] = 0

        if not HAS_PANDAS:
            print("[WARN] pandas not installed in current python environment — using default schemas.", file=sys.stderr)
            self.params["weight_var"] = "HH_weights"
            self.params["weight_source"] = "embedded"
            self.params["psu_var"] = "SEC_A_Q05"
            self.params["urban_rural_var"] = "SEC_A_Q06"
            self.params["urban_rural_mapping"] = {1: 'Urban', 2: 'Rural'}
            self.params["admin1_var"] = "SEC_A_Q01"
            self.params["admin1_count"] = 15
            self.params["admin1_names"] = ["Bomi", "Bong", "Gbarpolu", "Grand_Bassa", "Grand_Cape_Mount", "Grand_Gedeh", "Grand_Kru", "Lofa", "Margibi", "Maryland", "Montserrado", "Nimba", "River_Cess", "River_Gee", "Sinoe"]
            self.params["admin1_codes"] = [x.upper() for x in self.params["admin1_names"]]
            self.params["admin1_raw_labels"] = self.params["admin1_names"]
            return

        reader = pd.read_stata(self.master_dta, iterator=True)
        var_labels = reader.variable_labels()
        val_labels = reader.value_labels()
        cols = list(var_labels.keys())

        self.params["master_filename"] = self.master_dta.name
        self.params["num_variables"] = len(cols)

        # 1. Weights
        final_weight_candidates = [c for c in cols if any(k in c.lower() for k in ["hhsampleweight", "hh_sample_weight", "hh_weights", "hh_wt", "sampleweight"])]
        if "HHsampleweights" in cols:
            self.params["weight_var"] = "HHsampleweights"
            self.params["weight_source"] = "embedded"
        elif "HH_weights" in cols:
            self.params["weight_var"] = "HH_weights"
            self.params["weight_source"] = "embedded"
        elif "hh_wt" in cols:
            self.params["weight_var"] = "hh_wt"
            self.params["weight_source"] = "embedded"
        elif final_weight_candidates:
            self.params["weight_var"] = final_weight_candidates[0]
            self.params["weight_source"] = "embedded"
        else:
            weight_vars = [c for c in cols if any(k in c.lower() for k in ["weight", "wgt"])]
            if weight_vars:
                self.params["weight_var"] = weight_vars[0]
                self.params["weight_source"] = "embedded"
            else:
                self.params["weight_var"] = "hh_wt"
                self.params["weight_source"] = "external_excel"

        # 2. Locality / Urban-Rural (detect variable with Urban & Rural value labels)
        loc_var = None
        for col, labels in val_labels.items():
            lbl_texts = " ".join([str(v).lower() for v in labels.values()])
            if "urban" in lbl_texts and "rural" in lbl_texts:
                loc_var = col
                break
        if not loc_var:
            for col in ["SEC_A_Q06", "SEC_A_Q05", "SEC_A_Q03", "locality", "urban_rural"]:
                if col in cols and any(k in var_labels.get(col, "").lower() for k in ["rural", "urban", "locality class", "sector"]):
                    loc_var = col
                    break
        self.params["urban_rural_var"] = loc_var if loc_var else "SEC_A_Q06"
        self.params["urban_rural_mapping"] = val_labels.get(self.params["urban_rural_var"], {1: 'Urban', 2: 'Rural'})

        # 3. PSU / EA (cluster variable, must NOT be locality variable)
        psu_var = None
        for col in ["SEC_A_Q07", "SEC_A_Q06", "SEC_A_Q05", "ea_number", "ea_id", "cluster", "psu"]:
            if col in cols and col != self.params["urban_rural_var"]:
                vlabel = var_labels.get(col, "").lower()
                if any(k in vlabel for k in ["ea", "enumeration", "cluster", "psu"]) or any(k in col.lower() for k in ["ea", "cluster", "psu"]):
                    psu_var = col
                    break
        if not psu_var:
            ea_candidates = [c for c in cols if c != self.params["urban_rural_var"] and ("ea" in c.lower() or "cluster" in c.lower())]
            psu_var = ea_candidates[0] if ea_candidates else "SEC_A_Q05"
        self.params["psu_var"] = psu_var

        # 4. Admin 1 (Regions / Counties / Provinces)
        admin1_var = "SEC_A_Q01" if "SEC_A_Q01" in cols else cols[0]
        self.params["admin1_var"] = admin1_var
        admin1_dict = val_labels.get(admin1_var, {})

        if admin1_dict:
            sorted_keys = sorted(admin1_dict.keys())
            names = [str(admin1_dict[k]).strip() for k in sorted_keys]
            clean_names = [re.sub(r'[^a-zA-Z0-9_]', '', n.replace(' ', '_')) for n in names]
            codes = [n.upper() for n in clean_names]
            self.params["admin1_count"] = len(names)
            self.params["admin1_names"] = clean_names
            self.params["admin1_codes"] = codes
            self.params["admin1_raw_labels"] = names
        else:
            self.params["admin1_count"] = 14
            self.params["admin1_names"] = ["Region_" + str(i) for i in range(1, 15)]
            self.params["admin1_codes"] = ["REG_" + str(i) for i in range(1, 15)]
            self.params["admin1_raw_labels"] = self.params["admin1_names"]


class MTFGenerator:
    def __init__(self, template_dir: Path, target_dir: Path, params: Dict[str, Any]):
        self.template_dir = template_dir.resolve()
        self.target_dir = target_dir.resolve()
        self.params = params

    def deploy(self):
        """Deploy and calibrate all do-files and scripts."""
        dofile_out = self.target_dir / "Do-file"
        output_out = self.target_dir / "Output"
        charts_out = output_out / "charts"
        data_wip = self.target_dir / "Data" / "wip"
        data_clean = self.target_dir / "Data" / "clean"
        scripts_out = dofile_out / "scripts"

        for p in [dofile_out, output_out, charts_out, data_wip, data_clean, scripts_out]:
            p.mkdir(parents=True, exist_ok=True)

        self._generate_master_do(dofile_out)
        self._generate_build_master_do(dofile_out)
        self._generate_setup_do(dofile_out)

        for f in ["02_elec_attributes.do", "03_elec_aggregate.do", "05_cooking_aggregate.do"]:
            src = self.template_dir / "Do-file" / f
            if src.exists():
                shutil.copy2(src, dofile_out / f)

        self._generate_cooking_attributes_do(dofile_out)
        self._generate_enhancements_do(dofile_out)
        self._generate_export_do(dofile_out)
        self._deploy_python_scripts(dofile_out, scripts_out)

    def _generate_cooking_attributes_do(self, dofile_out: Path):
        src = self.template_dir / "Do-file" / "04_cooking_attributes.do"
        text = src.read_text(encoding="utf-8")

        mainstove_stata = self.params.get("cookstove_mainstove_stata", "")
        emit_tier_stata = self.params.get("cookstove_emit_tier_stata", "")

        if mainstove_stata:
            pattern = re.compile(r'\t*capture drop mainstove\s*\n\t*gen mainstove = \.\s*\n(?:\t*replace mainstove = [^\n]+\n)+')
            text = pattern.sub(mainstove_stata + "\n", text)

        if emit_tier_stata:
            pattern2 = re.compile(r'\t*capture drop cs_emit_tier[^\n]*\n\t*gen cs_emit_tier = \.\s*\n(?:\t*replace cs_emit_tier = [^\n]+\n)+\s*lab var cs_emit_tier[^\n]+')
            text = pattern2.sub(emit_tier_stata, text)

        (dofile_out / "04_cooking_attributes.do").write_text(text, encoding="utf-8")

    def _generate_master_do(self, dofile_out: Path):
        country = self.params.get("country_name", "Liberia")
        master_name = f"{country}_MTF_Master.do"
        target_file = dofile_out / master_name

        raw_hh_path = str(self.params["raw_dir"]).replace("\\", "/")
        user_path = str(self.target_dir).replace("\\", "/")

        content = f"""**************************************************************************
*                                                                        *
*   title:  {country} MTF Master Pipeline — Automated Indicator Suite      *
*   author: Bryan Koo / ESMAP Global Survey Team                         *
*   date:   Generated by MTF Auto-Calibrator                             *
*                                                                        *
**************************************************************************

*======================    1. USER & PATH SETUP   ============================*

* --- Bryan: Linux (local machine) ---
if c(username)=="bryan" {{
    global user "{user_path}"
}}

* --- Bryan: Windows (WBG OneDrive) ---
if c(username)=="WB453090" {{
    global user "{user_path}"
}}

* --- Kat: Windows (WBG Desktop) ---
if c(username)=="wb570814" {{
    global user "{user_path}"
}}

* Common folder paths
global raw_hh    "{raw_hh_path}"
global wip_hh    "$user/Data/wip"
global clean     "$user/Data/clean"
global output    "$user/Output"
global scripts   "$user/Do-file"
global out_sl    "$output"

* Parameters
global country    "{country}"
global master_dta "MTF_2024_HH_{country}_Master.dta"
global currency   "{self.params.get('currency_code', 'LRD')}"
global usd_rate   {self.params.get('usd_rate', 192.5)}

*======================    2. GLOBAL TOGGLES   ================================*
global run_enhancements 1

*======================    3. MAIN RUN   =====================================*
clear all
set more off
set maxvar 10000

di "========================================================"
di " MTF {country} Master Pipeline — $(c(current_date))"
di "========================================================"

di " [0/7] Master dataset compilation: raw modules & expenditure..."
do "$scripts/00_build_master_dataset.do"

di " [1/7] Setup & survey design validation..."
do "$scripts/01_setup.do"

di " [2/7] Electricity attribute tiers (capacity -> safety)..."
do "$scripts/02_elec_attributes.do"

di " [3/7] Aggregate electricity tier + technology type..."
do "$scripts/03_elec_aggregate.do"

di " [4/7] Cooking MECS attribute tiers (exposure -> availability)..."
do "$scripts/04_cooking_attributes.do"

di " [5/7] Aggregate MECS cooking tier + stove type..."
do "$scripts/05_cooking_aggregate.do"

if $run_enhancements == 1 {{
    di " [6/7] Analytical enhancements..."
    do "$scripts/06_analytical_enhancements.do"
}}

di " [7/7] Export: svy:tabulate -> putexcel -> JSON..."
do "$scripts/07_export.do"

di "========================================================"
di " Pipeline complete. Outputs in: $out_sl"
di "========================================================"
"""
        target_file.write_text(content, encoding="utf-8")

    def _generate_build_master_do(self, dofile_out: Path):
        src = self.template_dir / "Do-file" / "00_build_master_dataset.do"
        text = src.read_text(encoding="utf-8")

        country = self.params.get("country_name", "Liberia")
        master_out = f"MTF_2024_HH_{country}_Master.dta"
        raw_master = self.params["master_filename"]
        weight_var = self.params.get("weight_var", "HH_weights")
        ur_var = self.params.get("urban_rural_var", "SEC_A_Q06")
        admin1_var = self.params.get("admin1_var", "SEC_A_Q01")

        text = re.sub(r'MTF_2024_HH_Namibia_Master\.dta', master_out, text)

        if self.params.get("weight_source") == "embedded":
            weight_block = f"""*===========================================================================
*  2. SAMPLING WEIGHTS & SURVEY STRATIFICATION ({country.upper()})
*===========================================================================

use "$raw_hh/{raw_master}", clear

* Final calibrated household weight (embedded in clean microdata)
gen hh_wt = {weight_var}
lab var hh_wt "Final Calibrated Household Weight"

* Merge household size and head characteristics
merge 1:1 interview__id using "$wip_hh/hhsize.dta", nogen
merge 1:1 interview__id using "$wip_hh/headgender.dta", nogen

* Population weight:
gen pop_wt = hh_wt * hhsize
lab var pop_wt "Final Population Weight (hh_wt × hhsize)"

* Locality (Urban / Rural):
gen loc_urban_rural = .
replace loc_urban_rural = 1 if {ur_var} == 1    // Urban
replace loc_urban_rural = 2 if inlist({ur_var}, 2, 99)    // Rural
lab define loc_urban_rural 1 "Urban" 2 "Rural", replace
lab val loc_urban_rural loc_urban_rural
lab var loc_urban_rural "Urban / Rural Locality"

* Stratification variable: Admin 1 ({admin1_var}) × Locality ({ur_var})
egen strata_id = group({admin1_var} {ur_var})
lab var strata_id "Survey Stratum: Admin 1 × Locality"

save "$wip_hh/{master_out}", replace
"""
            sec2_pattern = re.compile(r'\*={5,}\s*\*  2\. SAMPLING WEIGHTS.*?save "\$wip_hh/[^"]+", replace', re.DOTALL)
            text = sec2_pattern.sub(weight_block.strip(), text)

        (dofile_out / "00_build_master_dataset.do").write_text(text, encoding="utf-8")

    def _generate_setup_do(self, dofile_out: Path):
        country = self.params.get("country_name", "Liberia")
        master_out = f"MTF_2024_HH_{country}_Master.dta"
        psu = self.params.get("psu_var", "SEC_A_Q05")

        content = f"""**************************************************************************
*  01_setup.do                                                           *
*  {country} MTF Pipeline — Setup, Survey Design & Validation             *
**************************************************************************

use "$wip_hh/{master_out}", clear
set more off

di "---------------------------------------------------------"
di " Validating Master Dataset: {master_out}"
di " Total Observations: " _N
di "---------------------------------------------------------"

* Verify and declare survey design
capture confirm numeric variable {psu}
if _rc != 0 {{
    capture drop psu_id
    egen psu_id = group({psu})
    lab var psu_id "Primary Sampling Unit (Numeric EA ID)"
    local psu_use "psu_id"
}}
else {{
    local psu_use "{psu}"
}}
svyset `psu_use' [pw=hh_wt], strata(strata_id) singleunit(centered)
svydescribe

* Quick diagnostic summary of core disaggregation variables
di "Disaggregation summary (weighted):"
svy: tabulate loc_urban_rural
svy: tabulate hh_head_gender
svy: tabulate hh_exp_quintile

save "$wip_hh/{master_out}", replace
di " 01_setup.do complete — Master dataset validated."
"""
        (dofile_out / "01_setup.do").write_text(content, encoding="utf-8")

    def _generate_enhancements_do(self, dofile_out: Path):
        src = self.template_dir / "Do-file" / "06_analytical_enhancements.do"
        text = src.read_text(encoding="utf-8")

        country = self.params.get("country_name", "Liberia")
        master_out = f"MTF_2024_HH_{country}_Master.dta"
        text = re.sub(r'MTF_2024_HH_Namibia_Master\.dta', master_out, text)

        admin1_var = self.params.get("admin1_var", "SEC_A_Q01")
        admin1_names = self.params.get("admin1_names", [])

        lines = [f"*  ENHANCEMENT 11: {len(admin1_names)} SUBDIVISIONS OF {country.upper()} ({admin1_var})",
                 "*===========================================================================",
                 "capture drop reg_*"]
        for idx, name in enumerate(admin1_names, start=1):
            var_name = f"reg_{name.lower()}"
            lines.append(f"gen byte {var_name} = ({admin1_var} == {idx})")

        enh11_block = "\n".join(lines)
        pattern = re.compile(r'\*  ENHANCEMENT 11:.*?(?=save "\$wip_hh)', re.DOTALL)
        text = pattern.sub(enh11_block + "\n\n", text)

        (dofile_out / "06_analytical_enhancements.do").write_text(text, encoding="utf-8")

    def _generate_export_do(self, dofile_out: Path):
        src = self.template_dir / "Do-file" / "07_export.do"
        text = src.read_text(encoding="utf-8")

        country = self.params.get("country_name", "Liberia")
        master_out = f"MTF_2024_HH_{country}_Master.dta"
        text = re.sub(r'MTF_2024_HH_Namibia_Master\.dta', master_out, text)
        text = re.sub(r'MTF_Namibia_Summary\.xlsx', f"MTF_{country}_Summary.xlsx", text)

        admin1_var = self.params.get("admin1_var", "SEC_A_Q01")
        count = self.params.get("admin1_count", 15)
        admin1_names = self.params.get("admin1_names", [])
        admin1_codes = self.params.get("admin1_codes", [])

        names_str = " ".join(admin1_names)
        codes_str = " ".join(admin1_codes)

        reg_setup = f"""local reg_names {names_str}
	local reg_codes {codes_str}

	forval r = 1/{count} {{"""

        text = re.sub(r'local reg_names Kharas.*?\n\s*local reg_codes KHARAS.*?\n\s*forval r = 1/\d+ \{',
                      reg_setup, text, flags=re.DOTALL)

        if admin1_var != "SEC_A_Q01":
            text = text.replace("SEC_A_Q01", admin1_var)

        # Dynamically calibrate scalars_list for the country's Admin 1 codes
        country_reg_scalars = []
        for ccode in admin1_codes:
            country_reg_scalars.append(f"REG_{ccode}_ELEC")
        for ccode in admin1_codes:
            country_reg_scalars.append(f"REG_{ccode}_GRID")
        for ccode in admin1_codes:
            country_reg_scalars.append(f"REG_{ccode}_SOLAR")

        reg_scalars_str = " \\\n\t\t".join([" ".join(country_reg_scalars[i:i+5]) for i in range(0, len(country_reg_scalars), 5)])

        namibia_scalars_pattern = re.compile(r'REG_KHARAS_ELEC.*?REG_ZAMBEZI_SOLAR', re.DOTALL)
        text = namibia_scalars_pattern.sub(reg_scalars_str, text)

        (dofile_out / "07_export.do").write_text(text, encoding="utf-8")

    def _deploy_python_scripts(self, dofile_out: Path, scripts_out: Path):
        country = self.params.get("country_name", "Liberia")
        admin1_count = self.params.get("admin1_count", 15)
        admin1_unit = self.params.get("admin1_unit_label", "county")
        admin1_unit_plural = self.params.get("admin1_unit_label_plural", "counties")
        survey_year = self.params.get("survey_year", "2024")
        strata_count = self.params.get("strata_count", admin1_count * 2)

        src_vis = self.template_dir / "Do-file" / "scripts" / "visualize.py"
        src_inj = self.template_dir / "Do-file" / "scripts" / "inject_report.py"
        src_tpl = self.template_dir / "Do-file" / "MTF_Report_Template.md"

        if src_vis.exists():
            v_text = src_vis.read_text(encoding="utf-8")
            v_text = v_text.replace("MTF_Namibia_Summary.xlsx", f"MTF_{country}_Summary.xlsx")
            (scripts_out / "visualize.py").write_text(v_text, encoding="utf-8")

        if src_inj.exists():
            i_text = src_inj.read_text(encoding="utf-8")
            i_text = i_text.replace("MTF_Namibia_Report", f"MTF_{country}_Report")
            (scripts_out / "inject_report.py").write_text(i_text, encoding="utf-8")

        if src_tpl.exists():
            t_text = src_tpl.read_text(encoding="utf-8")
            # Replace {{COUNTRY_NAME}} and other meta placeholders
            t_text = t_text.replace("{{COUNTRY_NAME}}", country)
            t_text = t_text.replace("{{SURVEY_YEAR}}", survey_year)
            t_text = t_text.replace("{{ADMIN1_COUNT}}", str(admin1_count))
            t_text = t_text.replace("{{ADMIN1_UNIT_LABEL}}", admin1_unit.capitalize())
            t_text = t_text.replace("{{ADMIN1_UNIT_LABEL_PLURAL}}", admin1_unit_plural.capitalize())
            t_text = t_text.replace("{{STRATA_COUNT}}", str(strata_count))

            # Inject cookstove typology table (Box 3) if CSV available
            cookstove_table = self.params.get("cookstove_typology_table", "")
            if cookstove_table:
                t_text = t_text.replace("{{COOKSTOVE_TYPOLOGY_TABLE}}", cookstove_table)
            else:
                t_text = t_text.replace("{{COOKSTOVE_TYPOLOGY_TABLE}}",
                    "*[FILL IN: Confirm cookstove typology with country expert and run the calibrator "
                    "with --cookstove-config to auto-populate this table.]*")

            # Inject Table 3.1 rows from CSV if available
            stats_rows = self.params.get("cookstove_stats_table_rows", "")
            if stats_rows:
                t_text = t_text.replace("{{COOKSTOVE_STATS_TABLE_ROWS}}", stats_rows)
            else:
                t_text = t_text.replace("{{COOKSTOVE_STATS_TABLE_ROWS}}",
                    "| *[FILL IN: Run calibrator with --cookstove-config]* | — | — | — | — | — |")

            # Optional: inject regional module if --include-regional was set
            if self.params.get("include_regional", False):
                reg_src = self.template_dir / "Do-file" / "MTF_Regional_Analysis_Module.md"
                if reg_src.exists():
                    reg_text = reg_src.read_text(encoding="utf-8")
                    reg_text = reg_text.replace("{{COUNTRY_NAME}}", country)
                    reg_text = reg_text.replace("{{ADMIN1_COUNT}}", str(admin1_count))
                    reg_text = reg_text.replace("{{ADMIN1_UNIT_LABEL}}", admin1_unit.capitalize())
                    reg_text = reg_text.replace("{{ADMIN1_UNIT_LABEL_PLURAL}}", admin1_unit_plural.capitalize())
                    regional_comment = ("<!-- ============================================================\n"
                                        "     OPTIONAL REGIONAL MODULE\n"
                                        "     ============================================================ -->")
                    t_text = t_text.replace(regional_comment, reg_text)

            (dofile_out / "MTF_Report_Template.md").write_text(t_text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="MTF Country Survey Auto-Calibrator & Pipeline Generator")
    parser.add_argument("--country-dir", "-c", type=str, required=True,
                        help="Target Country Directory")
    parser.add_argument("--template-dir", "-t", type=str,
                        default="/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/00_MTF_Country_Pipeline_Standard",
                        help="Standard Template Directory")
    parser.add_argument("--country-name", "-n", type=str, default=None,
                        help="Country Name (e.g. Liberia, Nigeria)")
    parser.add_argument("--currency", type=str, default=None,
                        help="Local Currency Code (e.g. LRD, NGN)")
    parser.add_argument("--exchange-rate", type=float, default=None,
                        help="Survey Period Exchange Rate per USD")
    parser.add_argument("--cookstove-config", type=str, default=None,
                        help="Path to cookstove_calibration.csv (default: auto-locate in Tools/ directory)")
    parser.add_argument("--include-regional", action="store_true",
                        help="Include Admin 1 regional analysis module in deployed report template")
    parser.add_argument("--admin1-unit", type=str, default=None,
                        help="Singular name for Admin 1 unit (e.g. county, region, province). Auto-detected if not set.")
    parser.add_argument("--survey-year", type=str, default="2024",
                        help="Survey year (default: 2024)")
    parser.add_argument("--auto-confirm", "-y", action="store_true",
                        help="Automatically apply without interactive prompt")

    args = parser.parse_args()

    country_dir = Path(args.country_dir).resolve()
    template_dir = Path(args.template_dir).resolve()

    print(f"\n==================================================================")
    print(f"   ESMAP MTF Pipeline Auto-Calibrator (World Bank Energy GP)     ")
    print(f"==================================================================")
    print(f" Target Workspace: {country_dir}")
    print(f" Standard Template: {template_dir}\n")

    scanner = MTFScanner(country_dir)
    print(" [1/3] Scanning country directory structure...")
    if not scanner.locate_data_dir():
        print(f"[ERROR] Could not automatically locate survey microdata in {country_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"  ✓ Clean survey directory identified: {scanner.raw_dir.name}")
    print(" [2/3] Inspecting dataset schemas, weights, and Admin 1 units...")
    params = scanner.scan_datasets()
    params["raw_dir"] = scanner.raw_dir

    if args.country_name:
        params["country_name"] = args.country_name
    else:
        match = re.search(r'\d+_([A-Za-z]+)', str(country_dir))
        params["country_name"] = match.group(1) if match else "Country"

    if args.currency:
        params["currency_code"] = args.currency
    else:
        params["currency_code"] = "LRD" if "liberia" in params["country_name"].lower() else "USD"

    if args.exchange_rate:
        params["usd_rate"] = args.exchange_rate
    else:
        params["usd_rate"] = 192.5 if "liberia" in params["country_name"].lower() else 1.0

    # Admin 1 unit label (auto-detect from count or user override)
    if args.admin1_unit:
        params["admin1_unit_label"] = args.admin1_unit.lower()
        params["admin1_unit_label_plural"] = args.admin1_unit.lower() + "s"
    else:
        count = params.get("admin1_count", 14)
        # Heuristic: Liberia has 15 counties, Namibia has 14 regions
        country_lower = params["country_name"].lower()
        if "liberia" in country_lower:
            params["admin1_unit_label"] = "county"
            params["admin1_unit_label_plural"] = "counties"
        elif "mozambique" in country_lower or "nigeria" in country_lower:
            params["admin1_unit_label"] = "province"
            params["admin1_unit_label_plural"] = "provinces"
        else:
            params["admin1_unit_label"] = "region"
            params["admin1_unit_label_plural"] = "regions"

    params["survey_year"] = args.survey_year
    params["strata_count"] = params.get("admin1_count", 14) * 2
    params["include_regional"] = args.include_regional

    # Load cookstove calibration CSV
    if args.cookstove_config:
        cookstove_csv_path = Path(args.cookstove_config).resolve()
    else:
        # Auto-locate in Tools/ next to the calibrator
        default_csv = template_dir / "Tools" / "cookstove_calibration.csv"
        cookstove_csv_path = default_csv if default_csv.exists() else None

    print(" [2b/3] Loading cookstove calibration configuration...")
    cs_loader = CookstoveLoader(cookstove_csv_path)
    params["cookstove_typology_table"] = cs_loader.generate_typology_table()
    params["cookstove_stats_table_rows"] = cs_loader.generate_stats_table_rows()
    params["cookstove_mainstove_stata"] = cs_loader.generate_mainstove_stata()
    params["cookstove_emit_tier_stata"] = cs_loader.generate_emit_tier_stata()

    print("\n------------------ DETECTED CONFIGURATION ------------------")
    print(f"  Country Designation:  {params['country_name']}")
    print(f"  Master Dataset:       {params['master_filename']} ({params['num_variables']} variables)")
    print(f"  Standard Rosters:     {len(scanner.rosters_found)} found, {len(scanner.rosters_missing)} missing")
    print(f"  Sampling Weight:      {params['weight_var']} ({params['weight_source']})")
    print(f"  Primary Sampling EA:  {params['psu_var']}")
    print(f"  Locality Variable:    {params['urban_rural_var']} ({len(params['urban_rural_mapping'])} categories)")
    print(f"  Admin 1 Geographic:   {params['admin1_var']} ({params['admin1_count']} {params['admin1_unit_label_plural']} detected)")
    print(f"  Currency & Rate:      {params['currency_code']} @ {params['usd_rate']} / USD")
    print(f"  Survey Year:          {params['survey_year']}")
    print(f"  Cookstove Types:      {len([r for r in cs_loader.rows if r.get('stove_group') != 'other'])} types calibrated")
    print(f"  Regional Module:      {'INCLUDED (--include-regional)' if args.include_regional else 'EXCLUDED (default — add manually on client request)'}")
    print("------------------------------------------------------------\n")

    if not args.auto_confirm:
        resp = input("Apply this configuration and generate calibrated Do-files? [Y/n]: ").strip().lower()
        if resp and resp != "y":
            print("[INFO] Operation cancelled by user.")
            sys.exit(0)

    print(" [3/3] Generating calibrated country Do-files & scripts...")
    generator = MTFGenerator(template_dir, country_dir, params)
    generator.deploy()

    print("\n  ✓ Calibrated Do-files deployed to: " + str(country_dir / "Do-file"))
    print("  ✓ Master Script: " + f"{params['country_name']}_MTF_Master.do")
    print("  ✓ Cookstove calibration: 04_cooking_attributes.do updated from cookstove_calibration.csv")
    print("  ✓ Report template: country name, cookstove table, and regional module injected.")
    print("  ✓ Automation scripts and report templates configured.")
    print("==================================================================\n")


if __name__ == "__main__":
    main()

