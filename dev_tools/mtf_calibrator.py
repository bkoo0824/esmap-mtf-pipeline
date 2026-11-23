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

try:
    from build_country_calibration import build_calibration_workbook, compile_stata_harmonization_do
    HAS_CALIBRATION_BUILDER = True
except ImportError:
    try:
        from Tools.build_country_calibration import build_calibration_workbook, compile_stata_harmonization_do
        HAS_CALIBRATION_BUILDER = True
    except ImportError:
        HAS_CALIBRATION_BUILDER = False



STANDARD_ROSTERS = [
    "hhroster.dta", "cookstoves.dta", "appliance.dta", "food.dta",
    "fuel_consumption.dta", "fuel_h11.dta", "solar_c_device.dta",
    "time_use.dta", "nonfood_1mon.dta", "nonfood_12mon.dta"
]

ROSTER_PATTERNS = {
    "fn_hhroster": r"^(?:section_)?a1.*(?:hh_)?roster.*\.dta$|^hhroster.*\.dta$",
    "fn_cookstoves": r"^(?:section_)?g.*cookstove.*roster.*\.dta$|^cookstoves?.*\.dta$",
    "fn_stovefuel": r"^(?:section_)?g.*stovefuel.*roster.*\.dta$|^stove_?fuel.*\.dta$",
    "fn_appliance": r"^(?:section_)?f.*appliance.*roster.*\.dta$|^appliances?.*\.dta$",
    "fn_generator": r"^(?:section_)?c.*generator.*roster.*\.dta$|^sec_c_generator.*\.dta$",
    "fn_rechar_ba": r"^(?:section_)?c.*rechargeable.*roster.*\.dta$|^sec_c_rechar_ba.*\.dta$",
    "fn_solar_device": r"^(?:section_)?c.*solar.*device.*roster.*\.dta$|^solar_c_device.*\.dta$",
    "fn_food": r"^(?:section_)?o.*_food_roster.*\.dta$|^food.*\.dta$",
    "fn_nonfood_1mon": r"^(?:section_)?o.*nonfood_?1m.*roster.*\.dta$|^nonfood_?1mon.*\.dta$",
    "fn_nonfood_12mon": r"^(?:section_)?o.*nonfood_?12m.*roster.*\.dta$|^nonfood_?12mon.*\.dta$",
    "fn_fuel_consump": r"^(?:section_)?i.*fuel_?consump.*roster.*\.dta$|^fuel_?consumption.*\.dta$",
    "fn_fuel_h11": r"^(?:section_)?h.*fuel_?h11.*roster.*\.dta$|^fuel_?h11.*\.dta$",
    "fn_lighting_fuel": r"^(?:section_)?h.*lighting_?fuel.*roster.*\.dta$|^lighting_?fuel.*\.dta$",
    "fn_time_coll": r"^(?:section_)?i.*time.*collect.*roster.*\.dta$|^time_?collecting.*\.dta$",
    "fn_time_use": r"^(?:section_)?l\.dta$|^time_?use.*\.dta$",
}


def safe_write_text(file_path: Path, content: str, encoding: str = "utf-8"):
    """Robust file writer to avoid [Errno 9] Bad file descriptor on Windows OneDrive and PyInstaller."""
    p = Path(file_path).resolve()
    os.makedirs(str(p.parent), exist_ok=True)
    raw_data = content.encode(encoding, errors="replace")

    import time
    for attempt in range(5):
        try:
            # Use low-level os.open with explicit binary write flags to bypass CRT buffered stream issues
            flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
            if hasattr(os, "O_BINARY"):
                flags |= os.O_BINARY
            fd = os.open(str(p), flags, 0o666)
            try:
                os.write(fd, raw_data)
            finally:
                os.close(fd)
            return
        except Exception:
            if attempt < 4:
                time.sleep(0.4)
            else:
                # Ultimate fallback: write to user's system temp dir and copy
                import tempfile
                tf = tempfile.NamedTemporaryFile(delete=False)
                try:
                    tf.write(raw_data)
                    tf.close()
                    shutil.copy2(tf.name, str(p))
                finally:
                    try:
                        os.unlink(tf.name)
                    except Exception:
                        pass
                return


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

    def __init__(self, config_path: Optional[Path] = None):
        self.rows = []
        if config_path and config_path.exists():
            if config_path.suffix.lower() in [".xlsx", ".xlsm"]:
                self._load_xlsx(config_path)
            else:
                self._load_csv(config_path)
        else:
            if config_path:
                print(f"[WARN] Cookstove calibration not found at {config_path} — using built-in defaults.",
                      file=sys.stderr)
            self.rows = self.DEFAULT_ROWS

    def _load_xlsx(self, path: Path):
        import openpyxl
        try:
            wb = openpyxl.load_workbook(path, data_only=True)
            if "Cookstove_Typology" not in wb.sheetnames:
                print(f"[WARN] Cookstove_Typology sheet not found in {path.name} — using defaults.", file=sys.stderr)
                self.rows = self.DEFAULT_ROWS
                return
            ws = wb["Cookstove_Typology"]
            headers = [str(cell.value).strip() if cell.value is not None else "" for cell in ws[1]]
            self.rows = []
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not any(row):
                    continue
                r_dict = {headers[i]: str(row[i]).strip() if i < len(row) and row[i] is not None else "" for i in range(len(headers)) if headers[i]}
                if r_dict.get("questionnaire_code"):
                    self.rows.append(r_dict)
            print(f"  ✓ Cookstove calibration: {len(self.rows)} stove types loaded from {path.name} [Sheet: Cookstove_Typology]")
        except Exception as e:
            print(f"[WARN] Failed reading Cookstove_Typology from {path.name}: {e} — using defaults.", file=sys.stderr)
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
        """
        Returns Stata cs_emit_tier assignment block.
        Maps directly from CAPI option codes (SEC_G_Q05) for fine-grained tier assignments
        across different ICS models (e.g. mud rocket vs forced-draft gasifier),
        with fallback to mainstove categories.
        """
        lines = [
            "capture drop cs_emit_tier",
            "gen cs_emit_tier = .",
            "* 1. Fine-grained assignment directly from CAPI questionnaire options (SEC_G_Q05)"
        ]
        assigned_qcodes = set()
        for row in self.rows:
            tier = row.get("iso_emission_tier", "").strip()
            codes = row.get("questionnaire_code", "").strip()
            if tier.isdigit() and codes:
                code_nums = [c.strip() for c in codes.split(",") if c.strip().isdigit()]
                if code_nums:
                    assigned_qcodes.update(code_nums)
                    c_str = ", ".join(code_nums)
                    desc = row.get("stove_description", "Stove").strip()
                    lines.append(f"\tcapture replace cs_emit_tier = {tier} if inlist(SEC_G_Q05, {c_str}) // {desc}")

        # Fallback to mainstove grouping if SEC_G_Q05 is missing or for aggregated variables
        group_to_int = {
            "open_fire": 1, "traditional": 2, "ics": 3,
            "clean_gas": 4, "clean_electric": 5, "clean_solar": 6,
            "clean_bio": 7, "transitional_bio": 8, "other": 555
        }
        tier_map: dict = {}
        for row in self.rows:
            group = row.get("stove_group", "other").strip()
            val = group_to_int.get(group, 555)
            tier = row.get("iso_emission_tier", "").strip()
            if tier.isdigit() and val not in tier_map:
                tier_map[val] = int(tier)

        from collections import defaultdict
        by_tier: dict = defaultdict(list)
        for mv, tv in tier_map.items():
            by_tier[tv].append(mv)

        lines.append("\t* 2. Fallback assignment by mainstove group if cs_emit_tier is still unassigned")
        for tv in sorted(by_tier.keys()):
            mvs = by_tier[tv]
            codes = ", ".join(str(m) for m in sorted(mvs))
            lines.append(f"\treplace cs_emit_tier = {tv} if inlist(mainstove, {codes}) & cs_emit_tier == .")

        lines.append('\tlab var cs_emit_tier "Stove ISO Emission Tier (0-5)"')
        return "\n".join(lines)

    def generate_efcy_tier_stata(self) -> str:
        """Returns Stata cs_efcy_tier assignment block directly from SEC_G_Q05 with mainstove fallback."""
        lines = [
            "capture drop cs_efcy_tier",
            "gen cs_efcy_tier = .",
            "* 1. Fine-grained thermal efficiency assignment from CAPI questionnaire options (SEC_G_Q05)"
        ]
        for row in self.rows:
            tier = row.get("efficiency_tier", "").strip()
            codes = row.get("questionnaire_code", "").strip()
            if tier.isdigit() and codes:
                code_nums = [c.strip() for c in codes.split(",") if c.strip().isdigit()]
                if code_nums:
                    c_str = ", ".join(code_nums)
                    desc = row.get("stove_description", "Stove").strip()
                    lines.append(f"\tcapture replace cs_efcy_tier = {tier} if inlist(SEC_G_Q05, {c_str}) // {desc}")

        group_to_int = {
            "open_fire": 1, "traditional": 2, "ics": 3,
            "clean_gas": 4, "clean_electric": 5, "clean_solar": 6,
            "clean_bio": 7, "transitional_bio": 8, "other": 555
        }
        tier_map: dict = {}
        for row in self.rows:
            group = row.get("stove_group", "other").strip()
            val = group_to_int.get(group, 555)
            tier = row.get("efficiency_tier", "").strip()
            if tier.isdigit() and val not in tier_map:
                tier_map[val] = int(tier)

        from collections import defaultdict
        by_tier: dict = defaultdict(list)
        for mv, tv in tier_map.items():
            by_tier[tv].append(mv)

        lines.append("\t* 2. Fallback assignment by mainstove group if cs_efcy_tier is still unassigned")
        for tv in sorted(by_tier.keys()):
            mvs = by_tier[tv]
            codes = ", ".join(str(m) for m in sorted(mvs))
            lines.append(f"\treplace cs_efcy_tier = {tv} if inlist(mainstove, {codes}) & cs_efcy_tier == .")

        lines.append('\tlab val cs_efcy_tier tier')
        lines.append('\tlab var cs_efcy_tier "Cooking: Efficiency Tier (ISO thermal efficiency)"')
        return "\n".join(lines)

    @classmethod
    def generate_template_csv(cls, country_name: str) -> str:
        """Generates standard CSV content for a new country cookstove calibration."""
        header = f"""# MTF Cookstove Calibration Form — {country_name.capitalize()}
# ==============================================================================
# INSTRUCTIONS FOR COUNTRY COORDINATORS & COOKSTOVE SPECIALISTS:
#
# 1. questionnaire_code (MUST EDIT):
#    - Match the numeric option codes used in Section G of your survey
#      (Question SEC_G_Q05 in Survey Solutions or cookstoves.dta).
#    - Multiple codes must be comma-separated inside double quotes, e.g. "1,2" or "3,5,22".
#
# 2. iso_emission_tier & efficiency_tier (EXPERT REVIEW REQUIRED):
#    - iso_emission_tier: ISO 19867 emission rating from 0 (open fire) to 5 (electric/solar).
#    - efficiency_tier:   ISO thermal efficiency from 0 (< 10%) to 5 (>= 50%).
#
# 3. stove_description & primary_fuel:
#    - Enter the descriptive names for Report Table 3.1 and Box 3.
#
# 4. stove_group (DO NOT CHANGE):
#    - Internal keyword for Stata: open_fire | traditional | ics | clean_gas |
#      clean_electric | clean_solar | clean_bio | transitional_bio | other
#
# 5. stat_key_nat, stat_key_urb, stat_key_rur (DO NOT CHANGE):
#    - Internal placeholder keys linking Stata export to the report template.
# ==============================================================================
questionnaire_code,stove_description,iso_emission_tier,efficiency_tier,stove_group,primary_fuel,notes,stat_key_nat,stat_key_urb,stat_key_rur
"1,2","Three-Stone / Open Fire",0,0,open_fire,Gathered firewood,Very low thermal efficiency (< 10%),STOVE_3STONE_N,STOVE_3STONE_U,STOVE_3STONE_R
"3,5,22","Traditional / Local Stove",0,0,traditional,Wood / Charcoal,Uninsulated metal grate or brazier,STOVE_TRAD_N,STOVE_TRAD_U,STOVE_TRAD_R
"4,6,7,8,9,20,21","Improved Cookstove (ICS)",3,2,ics,Firewood / Charcoal,Enclosed combustion with insulation; confirm tier with expert,STOVE_ICS_N,STOVE_ICS_U,STOVE_ICS_R
"10,11,12,13,14,23","Clean Fuel: LPG / Biogas",4,4,clean_gas,Bottled LPG (Butane/Propane),Tier 4-5 depending on ventilation; confirm with expert,STOVE_CLEAN_N,STOVE_CLEAN_U,STOVE_CLEAN_R
19,"Clean Fuel: Electric Stove",5,5,clean_electric,Grid electricity,Tier 5 when used as primary stove,STOVE_ELEC_N,STOVE_ELEC_U,STOVE_ELEC_R
"17,18","Solar Cooker",5,5,clean_solar,Solar radiation,Typically available only in high-insolation areas,STOVE_SOLAR_N,STOVE_SOLAR_U,STOVE_SOLAR_R
15,"Biogas Stove",5,4,clean_bio,Biogas (anaerobic digester),Confirm availability and prevalence with country team,STOVE_BIO_N,STOVE_BIO_U,STOVE_BIO_R
16,"Biofuel / Ethanol Stove",4,3,transitional_bio,Ethanol / Liquid biofuel,Confirm emission tier with expert (varies by fuel quality),STOVE_BIOFUEL_N,STOVE_BIOFUEL_U,STOVE_BIOFUEL_R
555,"Other Cookstove",,,,Other / Unspecified,Recode from open-text responses after reviewing data,STOVE_OTHER_N,STOVE_OTHER_U,STOVE_OTHER_R
"""
        return header




class MTFScanner:
    def __init__(self, country_dir: Path):
        self.country_dir = country_dir.resolve()
        self.raw_dir: Optional[Path] = None
        self.master_dta: Optional[Path] = None
        self.rosters_found: List[str] = []
        self.rosters_missing: List[str] = []
        self.params: Dict[str, Any] = {}

    def locate_data_dir(self) -> bool:
        """Find the clean household survey directory strictly within the target country workspace first."""
        def scan_tree(search_root: Path):
            cands = []
            for root, dirs, files in os.walk(search_root):
                rpath = Path(root)
                if any(x in str(rpath).lower() for x in ['/wip', 'wip_hh', 'pilot']):
                    continue
                dta_files = [f for f in files if f.endswith('.dta')]
                if len(dta_files) >= 5:
                    # Score matches using regex patterns as well as standard names
                    matches = 0
                    for rkey, rpat in ROSTER_PATTERNS.items():
                        if any(re.search(rpat, f, re.IGNORECASE) for f in dta_files):
                            matches += 1
                    is_clean = 1 if 'clean' in str(rpath).lower() else 0
                    is_hh = 1 if 'household' in str(rpath).lower() else 0
                    is_data = 1 if rpath.name.lower() == 'data' else 0
                    cands.append((rpath, is_data, is_clean, is_hh, matches, len(dta_files)))
            return cands

        # 1. Search inside country_dir strictly first (NEVER bleed into sibling country folders)
        candidates = scan_tree(self.country_dir)

        # 2. If nothing found in country_dir, fallback to country_dir.parent only if country_dir has no DTAs
        if not candidates and self.country_dir.parent != self.country_dir:
            candidates = scan_tree(self.country_dir.parent)

        if not candidates:
            return False

        # Prioritize: 'Data' folder, clean folder, household folder, matched rosters, total files
        candidates.sort(key=lambda x: (x[1], x[2], x[3], x[4], x[5]), reverse=True)
        self.raw_dir = candidates[0][0]
        return True

    def scan_datasets(self) -> Dict[str, Any]:
        """Scan .dta files in raw directory and detect schemas."""
        if not self.raw_dir or not self.raw_dir.exists():
            raise FileNotFoundError(f"Data directory not found in {self.country_dir}")

        all_dta = list(self.raw_dir.glob("*.dta"))
        dta_names = [f.name.lower() for f in all_dta]

        # Match rosters via regex patterns and legacy names
        matched_rosters = {}
        for rkey, rpat in ROSTER_PATTERNS.items():
            for f in all_dta:
                if re.search(rpat, f.name, re.IGNORECASE):
                    matched_rosters[rkey] = f.name
                    break

        found = []
        missing = []
        for r in STANDARD_ROSTERS:
            rbase = r.replace(".dta", "")
            matched = any(rbase in rf.lower() for rf in matched_rosters.values()) or (r in dta_names)
            if matched:
                found.append(r)
            else:
                missing.append(r)

        self.rosters_found = found
        self.rosters_missing = missing
        self.params["roster_mapping"] = matched_rosters

        # Detect whether survey data is organized in split section files (e.g. admin_info.dta, section_c.dta)
        has_admin_info = any(f.name.lower() == "admin_info.dta" for f in all_dta)
        has_section_c = any(f.name.lower() == "section_c.dta" for f in all_dta)
        self.params["is_split_sections"] = has_admin_info or has_section_c

        master_candidates = []
        if has_admin_info:
            master_candidates = [f for f in all_dta if f.name.lower() == "admin_info.dta"]
        elif has_section_c:
            master_candidates = [f for f in all_dta if f.name.lower() == "section_c.dta"]
        else:
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
            self.params["admin1_keys"] = [int(k) for k in sorted_keys]
            self.params["admin1_names"] = clean_names
            self.params["admin1_codes"] = codes
            self.params["admin1_raw_labels"] = names
        else:
            self.params["admin1_count"] = 14
            self.params["admin1_keys"] = list(range(1, 15))
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
        data_wip = self.target_dir / "Data" / "wip_hh"
        data_clean = self.target_dir / "Data" / "clean"
        scripts_out = dofile_out / "scripts"

        for p in [self.target_dir, dofile_out, output_out, charts_out, data_wip, data_clean, scripts_out]:
            try:
                p.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"[WARN] Could not create directory {p}: {e}. Proceeding...", file=sys.stderr)

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
        self._deploy_interactive_tools(self.target_dir / "Tools")

    def _generate_cooking_attributes_do(self, dofile_out: Path):
        src = self.template_dir / "Do-file" / "04_cooking_attributes.do"
        text = src.read_text(encoding="utf-8")

        mainstove_stata = self.params.get("cookstove_mainstove_stata", "")
        emit_tier_stata = self.params.get("cookstove_emit_tier_stata", "")
        efcy_tier_stata = self.params.get("cookstove_efcy_tier_stata", "")

        if mainstove_stata:
            pattern = re.compile(r'\t*capture drop mainstove\s*\n\t*gen mainstove = \.\s*\n(?:\t*replace mainstove = [^\n]+\n)+')
            text = pattern.sub(mainstove_stata + "\n", text)

        if emit_tier_stata:
            pattern2 = re.compile(r'\t*capture drop cs_emit_tier[^\n]*\n\t*gen cs_emit_tier = \.\s*\n(?:\t*replace cs_emit_tier = [^\n]+\n)+\s*lab var cs_emit_tier[^\n]+')
            text = pattern2.sub(emit_tier_stata, text)

        if efcy_tier_stata:
            pattern3 = re.compile(r'\t*capture drop cs_efcy_tier\s*\n\t*gen cs_efcy_tier = \.\s*\n(?:\t*replace cs_efcy_tier = [^\n]+\n)+\s*lab val cs_efcy_tier tier\s*\n\s*lab var cs_efcy_tier[^\n]+')
            text = pattern3.sub(efcy_tier_stata, text)

        safe_write_text(dofile_out / "04_cooking_attributes.do", text)

    def _generate_master_do(self, dofile_out: Path):
        country = self.params.get("country_name", "Liberia")
        master_name = f"{country}_MTF_Master.do"
        target_file = dofile_out / master_name

        rosters_dict = self.params.get("roster_mapping", {})
        roster_lines = []
        for r_macro, r_fname in sorted(rosters_dict.items()):
            roster_lines.append(f'global {r_macro} "{r_fname}"')
        roster_globals_block = "\n".join(roster_lines) if roster_lines else "* Default roster names used" 

        raw_hh_path = str(self.params["raw_dir"]).replace("\\", "/")
        user_path = str(self.target_dir).replace("\\", "/")

        # Derive Windows and Linux representations of paths for cross-OS execution
        # 1. Target dir
        if "/media/bryan/Bryan/MTF/" in user_path:
            rel_sub = user_path.split("/media/bryan/Bryan/MTF/")[1]
            win_user_default = f"C:/Users/WB453090/OneDrive - WBG/1_mtf_energy_global_survey/{rel_sub}"
            unix_user_default = user_path
        elif "1_mtf_energy_global_survey/" in user_path:
            rel_sub = user_path.split("1_mtf_energy_global_survey/")[1]
            win_user_default = user_path
            unix_user_default = f"/media/bryan/Bryan/MTF/{rel_sub}"
        else:
            win_user_default = user_path
            unix_user_default = user_path

        # 2. Raw data dir
        if "/media/bryan/Bryan/MTF/" in raw_hh_path:
            rel_raw = raw_hh_path.split("/media/bryan/Bryan/MTF/")[1]
            win_raw_default = f"C:/Users/WB453090/OneDrive - WBG/1_mtf_energy_global_survey/{rel_raw}"
            unix_raw_default = raw_hh_path
        elif "1_mtf_energy_global_survey/" in raw_hh_path:
            rel_raw = raw_hh_path.split("1_mtf_energy_global_survey/")[1]
            win_raw_default = raw_hh_path
            unix_raw_default = f"/media/bryan/Bryan/MTF/{rel_raw}"
        else:
            win_raw_default = raw_hh_path
            unix_raw_default = raw_hh_path

        current_user = self.params.get("username", "")

        user_block_custom_win = ""
        user_block_custom_unix = ""
        if current_user and current_user not in ["bryan", "WB453090", "wb570814"]:
            user_block_custom_win = f"""    * --- Current Active User ({current_user}) ---
    if c(username) == "{current_user}" {{
        global user "{win_user_default}"
    }}
"""
            user_block_custom_unix = f"""    * --- Current Active User ({current_user}) ---
    if c(username) == "{current_user}" {{
        global user "{unix_user_default}"
    }}
"""

        rel_sub_str = rel_sub if ('/media/bryan/Bryan/MTF/' in user_path or '1_mtf_energy_global_survey/' in user_path) else ''
        rel_raw_str = rel_raw if ('/media/bryan/Bryan/MTF/' in raw_hh_path or '1_mtf_energy_global_survey/' in raw_hh_path) else ''

        user_setup_str = f"""if c(os) == "Windows" {{
{user_block_custom_win}    * --- Bryan: Windows (WBG OneDrive) ---
    if c(username) == "WB453090" {{
        global user "{win_user_default}"
        global raw_hh "{win_raw_default}"
    }}
    * --- Marina / Collaborators: Windows (WBG Desktop / OneDrive) ---
    else if inlist(lower(c(username)), "marina", "wb570814") {{
        global user "C:/Users/`c(username)'/OneDrive - WBG/1_mtf_energy_global_survey/{rel_sub_str}"
        global raw_hh "C:/Users/`c(username)'/OneDrive - WBG/1_mtf_energy_global_survey/{rel_raw_str}"
    }}
    * --- Universal fallback for other Windows users ---
    else {{
        global user "C:/Users/`c(username)'/OneDrive - WBG/1_mtf_energy_global_survey/{rel_sub_str}"
        global raw_hh "C:/Users/`c(username)'/OneDrive - WBG/1_mtf_energy_global_survey/{rel_raw_str}"
    }}
}}
else if c(os) == "Unix" {{
{user_block_custom_unix}    * --- Bryan: Linux (local machine) ---
    if c(username) == "bryan" {{
        global user "{unix_user_default}"
        global raw_hh "{unix_raw_default}"
    }}
    * --- Fallback for other Unix users ---
    else {{
        global user "/media/`c(username)'/Bryan/MTF/{rel_sub_str}"
        global raw_hh "/media/`c(username)'/Bryan/MTF/{rel_raw_str}"
    }}
}}
else {{
    global user "{user_path}"
    global raw_hh "{raw_hh_path}"
}}"""

        content = f"""**************************************************************************
*                                                                        *
*   title:  {country} MTF Master Pipeline — Automated Indicator Suite    *
*   author: Bryan Koo / ESMAP Global Survey Team                         *
*   date:   Generated by MTF Auto-Calibrator                             *
*                                                                        *
**************************************************************************

*======================    1. USER & PATH SETUP   ============================*

{user_setup_str}

* Common folder paths
global wip_hh    "$user/Data/wip_hh"
global clean     "$user/Data/clean"
global output    "$user/Output"
global scripts   "$user/Do-file"
global out_sl    "$output"

* Parameters
global country    "{country}"
global master_dta "MTF_2024_HH_{country}_Master.dta"
global currency   "{self.params.get('currency_code', 'LRD')}"
global usd_rate   {self.params.get('usd_rate', 192.5)}

* Dynamic Roster Filename Definitions
{roster_globals_block}

*======================    2. GLOBAL TOGGLES   ================================*
global run_enhancements 1

*======================    3. MAIN RUN & LOGGING =============================*
clear all
set more off
capture set maxvar 10000

* Create log directory and open master log file
capture log close master_log
capture mkdir "$output/log"
local log_date : display %tdCCYYNNDD date(c(current_date), "DMY")
log using "$output/log/MTF_{country}_Master_`log_date'.log", name(master_log) text replace

di "========================================================"
di " MTF {country} Master Pipeline — $(c(current_date)) $(c(current_time))"
di " Log file: $output/log/MTF_{country}_Master_`log_date'.log"
di "========================================================"

di " [0/7] Master dataset compilation: raw modules & expenditure..."
do "$scripts/00_build_master_dataset.do"

capture confirm file "$scripts/00_country_harmonization.do"
if !_rc {{
    di " [0b/7] Country-specific harmonization & recoding..."
    do "$scripts/00_country_harmonization.do"
}}

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
di " Master log saved to: $output/log/MTF_{country}_Master_`log_date'.log"
di " Completed at: $(c(current_date)) $(c(current_time))"
di "========================================================"

log close master_log
"""
        safe_write_text(target_file, content)

    def _generate_build_master_do(self, dofile_out: Path):
        src = self.template_dir / "Do-file" / "00_build_master_dataset.do"
        text = src.read_text(encoding="utf-8")

        country = self.params.get("country_name", "Liberia")
        master_out = f"MTF_2024_HH_{country}_Master.dta"
        raw_master = self.params["master_filename"]
        weight_var = self.params.get("weight_var", "HH_weights")
        ur_var = self.params.get("urban_rural_var", "SEC_A_Q06")
        admin1_var = self.params.get("admin1_var", "SEC_A_Q01")
        psu_var = self.params.get("psu_var", "SEC_A_Q07")

        text = re.sub(r'MTF_2024_HH_Namibia_Master\.dta', master_out, text)

        is_split = self.params.get("is_split_sections", False)
        if is_split:
            # Build assembly block merging single-HH sections
            split_merge_code = """*===========================================================================
*  2. MULTI-SECTION MASTER DATASET COMPILATION & SAMPLING WEIGHTS
*===========================================================================

use "$raw_hh/admin_info.dta", clear
capture confirm variable interview__id
if _rc {
    capture confirm variable interview__key
    if !_rc clonevar interview__id = interview__key
}

* Merge core single-household section files
foreach sec in section_a2 section_b section_c section_d section_e section_g section_k section_o section_q section_r section_s {
    capture confirm file "$raw_hh/`sec'.dta"
    if !_rc {
        preserve
            use "$raw_hh/`sec'.dta", clear
            capture confirm variable interview__id
            if _rc {
                capture confirm variable interview__key
                if !_rc clonevar interview__id = interview__key
            }
            * Drop redundant overlapping columns before merging
            capture drop SEC_A_Q05 hh_weight_final SEC_C_Q02 SEC_C_Q117
            tempfile temp_`sec'
            save "`temp_`sec''"
        restore
        merge 1:1 interview__id using "`temp_`sec''", nogen
    }
}

* Sampling weights and stratification
gen hh_wt = hh_weight_final
lab var hh_wt "Final Calibrated Household Weight"

* Merge household size and head characteristics
merge 1:1 interview__id using "$wip_hh/hhsize.dta", nogen
merge 1:1 interview__id using "$wip_hh/headgender.dta", nogen

* Population weight:
gen pop_wt = hh_wt * hhsize
lab var pop_wt "Final Population Weight (hh_wt × hhsize)"

* Locality (Urban / Rural):
gen loc_urban_rural = .
replace loc_urban_rural = 1 if SEC_A_Q05 == 1    // Urban
replace loc_urban_rural = 2 if inlist(SEC_A_Q05, 2, 99)    // Rural
lab define loc_urban_rural 1 "Urban" 2 "Rural", replace
lab val loc_urban_rural loc_urban_rural
lab var loc_urban_rural "Urban / Rural Locality"

* Stratification variable: Admin 1 (SEC_A_Q01) × Locality (SEC_A_Q05)
egen strata_id = group(SEC_A_Q01 SEC_A_Q05)
lab var strata_id "Survey Stratum: Admin 1 × Locality"

save "$wip_hh/$master_dta", replace"""
            sec2_pattern = re.compile(r'\*={5,}\s*\*  2\. SAMPLING WEIGHTS.*?save "\$wip_hh/[^"]+", replace', re.DOTALL)
            text = sec2_pattern.sub(split_merge_code.strip(), text)
        elif self.params.get("weight_source") == "embedded":
            weight_block = f"""*===========================================================================
*  2. SAMPLING WEIGHTS & SURVEY STRATIFICATION ({country.upper()})
*===========================================================================

use "$raw_hh/{raw_master}", clear
capture confirm variable interview__id
if _rc {{
    capture confirm variable interview__key
    if !_rc clonevar interview__id = interview__key
}}

* Final calibrated household weight (embedded in clean microdata)
gen hh_wt = {weight_var}
lab var hh_wt "Final Calibrated Household Weight"

* Merge household size and head characteristics
merge 1:1 interview__id using "$wip_hh/demographics.dta", nogen

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

* Primary Sampling Unit (Cluster / EA)
capture confirm numeric variable {psu_var}
if !_rc {{
    gen double psu_id = {psu_var}
}}
else {{
    egen psu_id = group({psu_var})
}}
lab var psu_id "Primary Sampling Unit (Numeric EA ID)"

save "$wip_hh/$master_dta", replace
"""
            sec2_pattern = re.compile(r'\*={5,}\s*\*  2\. SAMPLING WEIGHTS.*?save "\$wip_hh/[^"]+", replace', re.DOTALL)
            text = sec2_pattern.sub(weight_block.strip(), text)

        safe_write_text(dofile_out / "00_build_master_dataset.do", text)

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
        safe_write_text(dofile_out / "01_setup.do", content)

    def _generate_enhancements_do(self, dofile_out: Path):
        src = self.template_dir / "Do-file" / "06_analytical_enhancements.do"
        text = src.read_text(encoding="utf-8")

        country = self.params.get("country_name", "Liberia")
        master_out = f"MTF_2024_HH_{country}_Master.dta"
        text = re.sub(r'MTF_2024_HH_Namibia_Master\.dta', master_out, text)

        admin1_var = self.params.get("admin1_var", "SEC_A_Q01")
        admin1_names = self.params.get("admin1_names", [])

        admin1_keys = self.params.get("admin1_keys", list(range(1, len(admin1_names) + 1)))
        lines = [f"*  ENHANCEMENT 11: {len(admin1_names)} SUBDIVISIONS OF {country.upper()} ({admin1_var})",
                 "*===========================================================================",
                 "capture drop reg_*"]
        for k_val, name in zip(admin1_keys, admin1_names):
            var_name = f"reg_{name.lower()}"
            lines.append(f"gen byte {var_name} = ({admin1_var} == {k_val})")

        enh11_block = "\n".join(lines)
        pattern = re.compile(r'\*  ENHANCEMENT 11:.*?(?=\*  ENHANCEMENT 12:)', re.DOTALL)
        text = pattern.sub(enh11_block + "\n\n\t", text)

        safe_write_text(dofile_out / "06_analytical_enhancements.do", text)

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

        admin1_keys = self.params.get("admin1_keys", list(range(1, count + 1)))
        keys_str = " ".join(str(k) for k in admin1_keys)
        reg_setup = f"""local reg_names {names_str}
\tlocal reg_codes {codes_str}
\tlocal reg_num_codes {keys_str}

\tlocal n_regs : word count `reg_names'
\tforval idx = 1/`n_regs' {{
\t\tlocal rname : word `idx' of `reg_names'
\t\tlocal rcode : word `idx' of `reg_codes'
\t\tlocal r     : word `idx' of `reg_num_codes'"""

        text = re.sub(r'local reg_names Kharas.*?\n\s*local reg_codes KHARAS.*?\n\s*forval r = 1/\d+ \{\s*\n\s*local rname[^\n]*\n\s*local rcode[^\n]*',
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

        reg_scalars_str = " ///\n\t\t".join([" ".join(country_reg_scalars[i:i+5]) for i in range(0, len(country_reg_scalars), 5)])

        namibia_scalars_pattern = re.compile(r'REG_KHARAS_ELEC.*?REG_ZAMBEZI_SOLAR', re.DOTALL)
        text = namibia_scalars_pattern.sub(reg_scalars_str, text)

        safe_write_text(dofile_out / "07_export.do", text)

    def _deploy_python_scripts(self, dofile_out: Path, scripts_out: Path):
        country = self.params.get("country_name", "Liberia")
        admin1_count = self.params.get("admin1_count", 15)
        admin1_unit = self.params.get("admin1_unit_label", "county")
        admin1_unit_plural = self.params.get("admin1_unit_label_plural", "counties")
        survey_year = self.params.get("survey_year", "2024")
        strata_count = self.params.get("strata_count", admin1_count * 2)

        src_vis = self.template_dir / "scripts" / "visualize.py"
        if not src_vis.exists():
            src_vis = self.template_dir / "Do-file" / "scripts" / "visualize.py"

        src_inj = self.template_dir / "scripts" / "inject_report.py"
        if not src_inj.exists():
            src_inj = self.template_dir / "Do-file" / "scripts" / "inject_report.py"

        src_tpl = self.template_dir / "MTF_Report_Template.md"
        if not src_tpl.exists():
            src_tpl = self.template_dir / "Do-file" / "MTF_Report_Template.md"

        if src_vis.exists():
            v_text = src_vis.read_text(encoding="utf-8")
            v_text = v_text.replace("MTF_Namibia_Summary.xlsx", f"MTF_{country}_Summary.xlsx")
            safe_write_text(scripts_out / "visualize.py", v_text)

        if src_inj.exists():
            i_text = src_inj.read_text(encoding="utf-8")
            i_text = i_text.replace("MTF_Namibia_Report", f"MTF_{country}_Report")
            safe_write_text(scripts_out / "inject_report.py", i_text)

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

            safe_write_text(dofile_out / "MTF_Report_Template.md", t_text)

        # Note: Cookstove typology is officially mastered in MTF_<Country>_Calibration.xlsx [Sheet: 3_Cookstove_Typology].
        # We only keep a single cookstove_calibration.csv for downstream legacy compatibility.
        target_csv_generic = scripts_out / "cookstove_calibration.csv"
        active_csv_path = self.params.get("cookstove_csv_path")
        if active_csv_path and Path(active_csv_path).exists():
            try:
                shutil.copy2(active_csv_path, target_csv_generic)
            except Exception:
                pass
        else:
            try:
                csv_content = CookstoveLoader.generate_template_csv(country)
                safe_write_text(target_csv_generic, csv_content)
            except Exception:
                pass

    def _deploy_interactive_tools(self, tools_out: Path):
        """Deploy interactive suite tools (run_mtf_local.sh, mtf_engine.py, etc.) to country Tools/ directory."""
        repo_root = self.template_dir.parent
        interactive_dir = repo_root / "interactive_suite"
        if not interactive_dir.exists():
            interactive_dir = self.template_dir / "Tools"

        if not interactive_dir.exists():
            return

        try:
            tools_out.mkdir(parents=True, exist_ok=True)
            for item in interactive_dir.iterdir():
                if item.name.startswith(('.', '__')) or item.is_dir():
                    continue
                dst = tools_out / item.name
                shutil.copy2(item, dst)
                if dst.suffix in ('.sh', '.command'):
                    try:
                        dst.chmod(dst.stat().st_mode | 0o111)
                    except Exception:
                        pass
        except Exception as e:
            print(f"[WARN] Could not deploy interactive Tools to {tools_out}: {e}", file=sys.stderr)


def find_template_dir(custom_path: Optional[str] = None) -> Path:
    """Auto-discover Standard Template directory across PyInstaller, Windows OneDrive, and Linux."""
    if custom_path:
        p = Path(custom_path).resolve()
        if p.exists() and (p / "Do-file").exists():
            return p

    # 1. PyInstaller bundled temp dir (_MEIPASS)
    if hasattr(sys, "_MEIPASS"):
        meipass_p = Path(sys._MEIPASS)
        if (meipass_p / "Do-file").exists():
            return meipass_p
        if (meipass_p / "stata_pipeline" / "Do-file").exists():
            return meipass_p / "stata_pipeline"
        if (meipass_p / "00_Standard_Template" / "Do-file").exists():
            return meipass_p / "00_Standard_Template"
        if (meipass_p / "00_MTF_Country_Pipeline_Standard" / "Do-file").exists():
            return meipass_p / "00_MTF_Country_Pipeline_Standard"

    # 2. Ascend from the script or executable location
    start_dir = Path(sys.executable if getattr(sys, "frozen", False) else __file__).resolve().parent
    search_chain = [start_dir] + list(start_dir.parents)
    for p in search_chain:
        if (p / "Do-file").exists():
            return p
        if (p / "stata_pipeline" / "Do-file").exists():
            return p / "stata_pipeline"
        if (p / "00_Standard_Template" / "Do-file").exists():
            return p / "00_Standard_Template"
        if (p / "00_MTF_Country_Pipeline_Standard" / "Do-file").exists():
            return p / "00_MTF_Country_Pipeline_Standard"

    # 3. Well-known fallback paths on Windows & Linux
    home = Path.home()
    well_known = [
        # Windows OneDrive paths
        home / "OneDrive - WBG" / "1_mtf_energy_global_survey" / "9_Data analysis_MTF countries" / "0_mtf_analysis_template" / "00_Standard_Template",
        home / "OneDrive - WBG" / "1_mtf_energy_global_survey" / "9_Data analysis_MTF countries" / "00_MTF_Country_Pipeline_Standard",
        # Local repo clone / Work directory
        home / "github" / "esmap-mtf-pipeline" / "stata_pipeline",
        home / "OneDrive" / "Work" / "04-Global_Analytics_&_ESMAP" / "2_MTF_Country_Surveys" / "esmap-mtf-pipeline" / "stata_pipeline",
        home / "OneDrive" / "Work" / "04-Global_Analytics_&_ESMAP" / "2_MTF_Country_Surveys" / "esmap-mtf-pipeline" / "00_Standard_Template",
    ]
    # Only test Linux path on POSIX/Unix systems to prevent C:\media\... fallback on Windows
    if os.name != "nt":
        well_known.append(Path("/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/00_MTF_Country_Pipeline_Standard"))

    for w in well_known:
        try:
            if w.exists() and (w / "Do-file").exists():
                return w.resolve()
        except Exception:
            continue

    # Fallback to start_dir.parent if nothing else matches
    return start_dir.parent


def main():
    parser = argparse.ArgumentParser(description="MTF Country Survey Auto-Calibrator & Pipeline Generator")
    parser.add_argument("--country-dir", "-c", type=str, required=True,
                        help="Target Country Directory")
    parser.add_argument("--template-dir", "-t", type=str, default=None,
                        help="Standard Template Directory (auto-detected if omitted)")
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
    parser.add_argument("--username", "-u", type=str, default=None,
                        help="Operating system / Stata username override (auto-detected if omitted)")
    parser.add_argument("--auto-confirm", "-y", action="store_true",
                        help="Automatically apply without interactive prompt")
    parser.add_argument("--calibrate-country", action="store_true",
                        help="Scan raw datasets, generate MTF_<Country>_Calibration.xlsx, and compile 00_country_harmonization.do")
    parser.add_argument("--compile-harmonization", type=str, default=None,
                        help="Path to MTF_<Country>_Calibration.xlsx to compile into 00_country_harmonization.do")

    args = parser.parse_args()

    country_dir = Path(args.country_dir).resolve()
    template_dir = find_template_dir(args.template_dir)

    print(f"\n==================================================================")
    print(f"   ESMAP MTF Pipeline Auto-Calibrator (World Bank Energy GP)     ")
    print(f"==================================================================")
    print(f" Target Workspace: {country_dir}")
    print(f" Standard Template: {template_dir}\n")

    if not (template_dir / "Do-file").exists():
        print(f"[ERROR] Standard template directory invalid or Do-file/ missing in: {template_dir}", file=sys.stderr)
        sys.exit(1)

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
        # Priority 1: Check existing calibration workbook metadata
        detected_c = None
        for s_dir in [country_dir, country_dir / "config", country_dir / "Tools", Path("config"), Path(".")]:
            if not s_dir.exists():
                continue
            for cal_f in list(s_dir.glob("MTF_*_Calibration.xlsx")) + list(s_dir.glob("mtf_calibration*.xlsx")):
                m = re.match(r"MTF_(.+)_Calibration\.xlsx", cal_f.name)
                if m and m.group(1).lower() not in ["standard", "template"]:
                    detected_c = m.group(1).replace("_", " ").title()
                    break
                try:
                    import openpyxl
                    wb = openpyxl.load_workbook(cal_f, data_only=True, read_only=True)
                    if "Instructions_&_Metadata" in wb.sheetnames:
                        ws = wb["Instructions_&_Metadata"]
                        for row in ws.iter_rows(values_only=True):
                            if row and len(row) >= 2:
                                k = str(row[0]).strip().lower()
                                v = str(row[1]).strip() if row[1] is not None else ""
                                if k == "country name" and v and not v.startswith("{{"):
                                    detected_c = v
                                    break
                except Exception:
                    pass
            if detected_c:
                break
        
        # Priority 2: country_config.yaml
        if not detected_c:
            for s_dir in [country_dir, country_dir / "config", Path("config"), Path(".")]:
                cfg_p = s_dir / "country_config.yaml"
                if cfg_p.exists():
                    try:
                        for line in cfg_p.read_text(encoding="utf-8").splitlines():
                            if line.strip().startswith("country:"):
                                c_val = line.split(":", 1)[1].strip().strip("\"'")
                                if c_val:
                                    detected_c = c_val
                                    break
                    except Exception:
                        pass
                if detected_c:
                    break

        if detected_c:
            params["country_name"] = detected_c
        else:
            match = re.search(r'\d+_([A-Za-z]+)', str(country_dir))
            cand = match.group(1) if match else "Country"
            if cand.lower() in ["test", "interactive_suite", "tools", "data"]:
                cand = "Guinea-Bissau"
            params["country_name"] = cand

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
    import getpass
    params["username"] = args.username if args.username else getpass.getuser()

    # Load cookstove calibration CSV
    # Search Priority:
    # 1. User explicit argument (--cookstove-config)
    # 2. Country-specific in Tools/ (Tools / cookstove_calibration_<country>.csv, hyphen or underscore)
    # 3. Country-specific in country workspace (country_dir / "Do-file" / "scripts" / f"cookstove_calibration_{cname}.csv")
    # 4. Country scripts generic (country_dir / "Do-file" / "scripts" / "cookstove_calibration.csv")
    # 5. Standard default in Tools/ (Tools / cookstove_calibration.csv)
    cname_clean = params["country_name"].lower().strip()
    cname_under = cname_clean.replace("-", "_")
    tools_dir = template_dir / "Tools"
    config_dir = template_dir / "config"

    # Excel Unified Candidates
    excel_candidates = [
        tools_dir / f"mtf_calibration_{cname_under}.xlsx",
        tools_dir / f"mtf_calibration_{cname_clean}.xlsx",
        country_dir / "Do-file" / "scripts" / f"mtf_calibration_{cname_under}.xlsx",
        country_dir / f"mtf_calibration_{cname_under}.xlsx",
        config_dir / f"mtf_calibration_{cname_under}.xlsx",
        config_dir / "mtf_calibration_standard.xlsx",
        tools_dir / "mtf_calibration_standard.xlsx",
        tools_dir / "mtf_calibration.xlsx",
    ]

    # Legacy CSV Candidates
    country_scripts_csv = country_dir / "Do-file" / "scripts" / f"cookstove_calibration_{cname_clean}.csv"
    country_scripts_csv_under = country_dir / "Do-file" / "scripts" / f"cookstove_calibration_{cname_under}.csv"
    country_scripts_csv_generic = country_dir / "Do-file" / "scripts" / "cookstove_calibration.csv"
    tools_country_csv = tools_dir / f"cookstove_calibration_{cname_clean}.csv"
    tools_country_csv_under = tools_dir / f"cookstove_calibration_{cname_under}.csv"
    tools_default_csv = tools_dir / "cookstove_calibration.csv"

    if args.cookstove_config:
        cookstove_csv_path = Path(args.cookstove_config).resolve()
    else:
        # Check Excel unified workbooks first
        found_excel = next((p for p in excel_candidates if p.exists()), None)
        if found_excel:
            cookstove_csv_path = found_excel
        elif tools_country_csv.exists() and "MUST EDIT" not in tools_country_csv.read_text(encoding="utf-8")[:300]:
            cookstove_csv_path = tools_country_csv
        elif tools_country_csv_under.exists() and "MUST EDIT" not in tools_country_csv_under.read_text(encoding="utf-8")[:300]:
            cookstove_csv_path = tools_country_csv_under
        elif country_scripts_csv.exists() and "MUST EDIT" not in country_scripts_csv.read_text(encoding="utf-8")[:300]:
            cookstove_csv_path = country_scripts_csv
        elif country_scripts_csv_under.exists() and "MUST EDIT" not in country_scripts_csv_under.read_text(encoding="utf-8")[:300]:
            cookstove_csv_path = country_scripts_csv_under
        elif tools_country_csv.exists():
            cookstove_csv_path = tools_country_csv
        elif tools_country_csv_under.exists():
            cookstove_csv_path = tools_country_csv_under
        elif country_scripts_csv.exists():
            cookstove_csv_path = country_scripts_csv
        elif country_scripts_csv_generic.exists():
            cookstove_csv_path = country_scripts_csv_generic
        elif tools_default_csv.exists():
            cookstove_csv_path = tools_default_csv
        else:
            # If no calibration file exists at all, auto-generate country-specific template in Tools/
            cookstove_csv_path = tools_dir / f"cookstove_calibration_{cname_clean}.csv"
            try:
                template_text = CookstoveLoader.generate_template_csv(params["country_name"])
                safe_write_text(cookstove_csv_path, template_text)
                print(f"  ★ Generated new country cookstove calibration template: {cookstove_csv_path.name}")
            except Exception:
                cookstove_csv_path = None

    # If country-specific CSV does not exist in Tools/, create one automatically for easy expert editing
    if tools_dir.exists() and not tools_country_csv.exists():
        try:
            template_text = CookstoveLoader.generate_template_csv(params["country_name"])
            safe_write_text(tools_country_csv, template_text)
            print(f"  ★ Created country cookstove calibration form: Tools/{tools_country_csv.name}")
        except Exception:
            pass

    print(f" [2b/3] Loading cookstove calibration configuration (Source: {cookstove_csv_path.name if cookstove_csv_path else 'Built-in Defaults'})...")
    cs_loader = CookstoveLoader(cookstove_csv_path)
    params["cookstove_csv_path"] = cookstove_csv_path
    params["cookstove_typology_table"] = cs_loader.generate_typology_table()
    params["cookstove_stats_table_rows"] = cs_loader.generate_stats_table_rows()
    params["cookstove_mainstove_stata"] = cs_loader.generate_mainstove_stata()
    params["cookstove_emit_tier_stata"] = cs_loader.generate_emit_tier_stata()
    params["cookstove_efcy_tier_stata"] = cs_loader.generate_efcy_tier_stata()

    print("\n------------------ DETECTED CONFIGURATION ------------------")
    print(f"  Target User / System: {params['username']} (auto-configured in Master Do-file)")
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

    if getattr(args, "calibrate_country", False):
        print("\n [Country Calibration] Building country metadata codebook & harmonization...")
        if HAS_CALIBRATION_BUILDER:
            calib_out = country_dir / f"MTF_{params['country_name']}_Calibration.xlsx"
            build_calibration_workbook(scanner.raw_dir, calib_out, params['country_name'])
            dofile_dir = country_dir / "Do-file"
            dofile_dir.mkdir(parents=True, exist_ok=True)
            compile_stata_harmonization_do(calib_out, dofile_dir / "00_country_harmonization.do", params['country_name'])
            print(f"  ★ Generated Country Calibration Workbook: {calib_out.name}")
            print(f"  ★ Compiled Harmonization Do-file: Do-file/00_country_harmonization.do")
        else:
            print("  [WARN] build_country_calibration module not found — skipping harmonization.")

    if getattr(args, "compile_harmonization", None):
        xlsx_path = Path(args.compile_harmonization).resolve()
        if xlsx_path.exists() and HAS_CALIBRATION_BUILDER:
            dofile_dir = country_dir / "Do-file"
            dofile_dir.mkdir(parents=True, exist_ok=True)
            compile_stata_harmonization_do(xlsx_path, dofile_dir / "00_country_harmonization.do", params['country_name'])
            print(f"  ★ Compiled Harmonization Do-file from {xlsx_path.name}")

    print("==================================================================\n")


if __name__ == "__main__":
    main()

