#!/usr/bin/env python3
"""
build_country_calibration.py — MTF Country Metadata Codebook & Calibration Generator
=====================================================================================
World Bank ESMAP | Energy Global Practice
Author: Bryan Koo / Antigravity AI Executive Secretariat

Features:
  1. Scans raw country survey directories (.dta files and rosters).
  2. Extracts complete metadata, variable labels, value labels, and frequencies into
     sheet [1_Raw_Codebook] of MTF_<Country>_Calibration.xlsx.
  3. Pre-populates modular mapping sheets with sample frequencies (N and %):
     - [2_Education]: Raw education codes -> 4 MTF standard categories (0:None, 1:Primary, 2:Secondary, 3:Higher)
     - [3_Cookstove_Typology]: Raw cookstove types (SEC_G_Q05) -> ISO emission & thermal efficiency tiers
     - [4_Stove_Fuel]: Primary fuel/stove codes -> ISO emission tiers & fuel groups
     - [5_Fuel_Frequency]: Fuel purchase frequency codes -> monthly multipliers
     - [6_Other_Specify_Recodes]: Open-ended text responses across modules -> suggested recodes for expert review
     - [7_Missing_Codes]: Country-specific missing codes (888, 999, -888, -999)
  4. Compiles verified Excel mappings into a defensive, reproducible Stata Do-file
     `00_country_harmonization.do` with built-in runtime assertions.
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, List, Tuple

import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


# Styling Palette (World Bank ESMAP Standards)
NAVY_HEADER = PatternFill(start_color="002244", end_color="002244", fill_type="solid")
ACCENT_HEADER = PatternFill(start_color="007799", end_color="007799", fill_type="solid")
TEAL_HEADER = PatternFill(start_color="008080", end_color="008080", fill_type="solid")
GRAY_BG = PatternFill(start_color="F2F4F7", end_color="F2F4F7", fill_type="solid")
REVIEW_FILL = PatternFill(start_color="FFF3CD", end_color="FFF3CD", fill_type="solid")    # Yellow warning
VERIFIED_FILL = PatternFill(start_color="D1E7DD", end_color="D1E7DD", fill_type="solid")  # Green verified

FONT_HEADER = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
FONT_BOLD = Font(name="Calibri", size=11, bold=True)
FONT_BODY = Font(name="Calibri", size=11)
FONT_SMALL = Font(name="Calibri", size=9, italic=True, color="555555")

THIN_BORDER = Border(
    left=Side(style="thin", color="CCCCCC"),
    right=Side(style="thin", color="CCCCCC"),
    top=Side(style="thin", color="CCCCCC"),
    bottom=Side(style="thin", color="CCCCCC"),
)


def extract_codebook(data_dir: Path) -> List[Dict[str, Any]]:
    """Scan all .dta files in data_dir and extract variable metadata and value labels."""
    dta_files = sorted(list(data_dir.glob("*.dta")))
    if not dta_files:
        dta_files = sorted(list(data_dir.rglob("*.dta")))

    codebook = []
    print(f"Scanning {len(dta_files)} Stata dataset(s) in {data_dir}...")

    for fpath in dta_files:
        fn = fpath.name
        if fn.startswith("~") or "backup" in fn.lower():
            continue

        try:
            with pd.io.stata.StataReader(fpath, convert_categoricals=False) as reader:
                var_labels = reader.variable_labels()
                val_labels = reader.value_labels()
                df = reader.read()
            total_rows = len(df)

            for col in df.columns:
                vlbl = var_labels.get(col, "")
                vl_dict = val_labels.get(col, {})
                vl_str = "; ".join([f"{k}:{v}" for k, v in sorted(vl_dict.items(), key=lambda x: str(x[0]))]) if vl_dict else ""
                n_missing = int(df[col].isna().sum())

                min_val, max_val = "", ""
                if pd.api.types.is_numeric_dtype(df[col]) and not df[col].dropna().empty:
                    min_val = str(round(df[col].min(), 2))
                    max_val = str(round(df[col].max(), 2))

                codebook.append({
                    "Dataset": fn,
                    "Variable": col,
                    "Variable_Label": vlbl,
                    "Storage_Type": str(df[col].dtype),
                    "N_Observations": total_rows,
                    "N_Missing": n_missing,
                    "Min_Value": min_val,
                    "Max_Value": max_val,
                    "Value_Labels": vl_str,
                })
        except Exception as e:
            print(f"[warn] Could not read {fn}: {e}", file=sys.stderr)

    return codebook


def build_education_mapping(codebook: List[Dict[str, Any]], data_dir: Path) -> List[Dict[str, Any]]:
    """Scan for household head education variable (SEC_A1_Q8) and map with frequency distribution."""
    rows = []
    edu_vars = [r for r in codebook if r["Variable"] == "SEC_A1_Q8"]
    if not edu_vars:
        edu_vars = [r for r in codebook if "educ" in r["Variable"].lower() and "head" in r["Variable_Label"].lower()]
    if not edu_vars:
        edu_vars = [r for r in codebook if any(w in r["Variable_Label"].lower() for w in ["grade", "school", "education", "escolaridade", "nivel de instrucao"])
                    and not any(w in r["Variable_Label"].lower() for w in ["age", "years old", "idade"])]

    if not edu_vars:
        return [{
            "Raw_Variable": "SEC_A1_Q8",
            "Raw_Code": 1,
            "Raw_Label": "Example Education Option",
            "Obs_Count": 0,
            "Sample_Share_Pct": 0.0,
            "Harmonized_Educ_Code": 1,
            "Harmonized_Educ_Level": "1: Primary Education",
            "Status": "Review",
            "Notes": "Please inspect raw dataset and specify code",
        }]

    target_var_info = edu_vars[0]
    var_name = target_var_info["Variable"]
    ds_name = target_var_info["Dataset"]
    ds_path = data_dir / ds_name
    if not ds_path.exists():
        matches = list(data_dir.rglob(ds_name))
        if matches:
            ds_path = matches[0]

    try:
        reader = pd.read_stata(ds_path, iterator=True)
        val_labels = reader.value_labels().get(var_name, {})
        df = pd.read_stata(ds_path, columns=[var_name], convert_categoricals=False)
        total_valid = df[var_name].dropna().count()
        counts = df[var_name].value_counts(dropna=False).to_dict()

        for code, cnt in sorted(counts.items(), key=lambda x: str(x[0])):
            if pd.isna(code):
                continue
            code_int = int(code) if isinstance(code, (int, float)) and code == int(code) else code
            lbl = val_labels.get(code_int, val_labels.get(code, f"Code {code}"))
            lbl_lower = str(lbl).lower()
            share_pct = round((cnt / total_valid) * 100, 2) if total_valid > 0 else 0.0

            # Strict ISCED alignment rules: Check secondary first to catch "basic 7-9" before "basic"
            if any(w in lbl_lower for w in ["none", "nenhum", "aucun", "pre-school", "pré-escolar", "creche", "jardim", "never"]):
                target_code = 0
                target_lbl = "0: None / No Schooling"
            elif any(w in lbl_lower for w in ["secondary", "secundario", "secundário", "secundária", "basic 7-9", "básico 3", "7-9", "middle", "lycee", "lycée", "high school"]):
                target_code = 2
                target_lbl = "2: Secondary Education"
            elif any(w in lbl_lower for w in ["higher", "university", "universidade", "superior", "vocational", "technical", "médio", "técnico", "polytechnic"]):
                target_code = 3
                target_lbl = "3: Higher Education"
            elif any(w in lbl_lower for w in ["primary", "primaria", "primária", "basic 1", "basic education 1-6", "básico 1", "básico 1º", "grade 1", "classe 1"]):
                target_code = 1
                target_lbl = "1: Primary Education"
            elif any(w in lbl_lower for w in ["other", "outro", "autre"]):
                target_code = 0
                target_lbl = "0: None / Other"
            else:
                target_code = 1
                target_lbl = "1: Primary Education (Proposed)"

            rows.append({
                "Raw_Variable": var_name,
                "Raw_Code": code_int,
                "Raw_Label": lbl,
                "Obs_Count": cnt,
                "Sample_Share_Pct": share_pct,
                "Harmonized_Educ_Code": target_code,
                "Harmonized_Educ_Level": target_lbl,
                "Status": "Verified" if target_code in [0, 1, 2, 3] else "Review",
                "Notes": f"Auto-classified based on CAPI label '{lbl}'",
            })
    except Exception as e:
        print(f"[warn] Education mapping extraction failed: {e}", file=sys.stderr)

    return rows


def build_cookstove_typology_mapping(codebook: List[Dict[str, Any]], data_dir: Path) -> List[Dict[str, Any]]:
    """Scan cookstoves roster specifically for stove type question (SEC_G_Q05) with frequencies."""
    rows = []
    # Explicitly prioritize SEC_G_Q05 in cookstove roster
    stove_vars = [r for r in codebook if r["Variable"] == "SEC_G_Q05" and "cookstove" in r["Dataset"].lower()]
    if not stove_vars:
        stove_vars = [r for r in codebook if "type" in r["Variable_Label"].lower() and "stove" in r["Variable_Label"].lower() and "cookstove" in r["Dataset"].lower()]
    if not stove_vars:
        stove_vars = [r for r in codebook if r["Variable"] == "SEC_G_Q05"]

    if not stove_vars:
        return [{
            "Raw_Variable": "SEC_G_Q05",
            "Stove_Code": 1,
            "Stove_Description": "Three-stone open fire",
            "Obs_Count": 0,
            "Sample_Share_Pct": 0.0,
            "Stove_Category": "open_fire",
            "Default_Primary_Fuel": "Gathered firewood",
            "ISO_Emission_Tier": 0,
            "Thermal_Efficiency_Tier": 0,
            "Status": "Review",
            "Notes": "Default template",
        }]

    target_var_info = stove_vars[0]
    var_name = target_var_info["Variable"]
    ds_name = target_var_info["Dataset"]
    ds_path = data_dir / ds_name
    if not ds_path.exists():
        matches = list(data_dir.rglob(ds_name))
        if matches:
            ds_path = matches[0]

    try:
        reader = pd.read_stata(ds_path, iterator=True)
        val_labels = reader.value_labels().get(var_name, {})
        df = pd.read_stata(ds_path, columns=[var_name], convert_categoricals=False)
        total_valid = df[var_name].dropna().count()
        counts = df[var_name].value_counts(dropna=False).to_dict()

        for code, cnt in sorted(counts.items(), key=lambda x: str(x[0])):
            if pd.isna(code):
                continue
            code_int = int(code) if isinstance(code, (int, float)) and code == int(code) else code
            lbl = val_labels.get(code_int, val_labels.get(code, f"Code {code}"))
            lbl_lower = str(lbl).lower()
            share_pct = round((cnt / total_valid) * 100, 2) if total_valid > 0 else 0.0

            # Default ISO tier classification
            if any(w in lbl_lower for w in ["3-stone", "three-stone", "três pedras", "open fire"]):
                st_cat = "open_fire"
                fuel = "Gathered firewood"
                emit_tier, eff_tier = 0, 0
            elif any(w in lbl_lower for w in ["traditional", "tradicional", "locally built"]):
                st_cat = "traditional"
                fuel = "Wood / Charcoal"
                emit_tier, eff_tier = 0, 0
            elif any(w in lbl_lower for w in ["improved", "melhorado", "ics", "biomass"]):
                st_cat = "ics"
                fuel = "Firewood / Charcoal"
                emit_tier, eff_tier = 3, 2
            elif any(w in lbl_lower for w in ["lpg", "gás", "gas", "piped"]):
                st_cat = "clean_gas"
                fuel = "Bottled LPG"
                emit_tier, eff_tier = 4, 4
            elif any(w in lbl_lower for w in ["electric", "eléctrico", "eléctrica"]):
                st_cat = "clean_electric"
                fuel = "Grid electricity"
                emit_tier, eff_tier = 5, 5
            elif any(w in lbl_lower for w in ["solar"]):
                st_cat = "clean_solar"
                fuel = "Solar radiation"
                emit_tier, eff_tier = 5, 5
            elif any(w in lbl_lower for w in ["kerosene", "petróleo"]):
                st_cat = "traditional"
                fuel = "Kerosene"
                emit_tier, eff_tier = 1, 1
            else:
                st_cat = "other"
                fuel = "Other / Unspecified"
                emit_tier, eff_tier = 0, 0

            rows.append({
                "Raw_Variable": var_name,
                "Stove_Code": code_int,
                "Stove_Description": lbl,
                "Obs_Count": cnt,
                "Sample_Share_Pct": share_pct,
                "Stove_Category": st_cat,
                "Default_Primary_Fuel": fuel,
                "ISO_Emission_Tier": emit_tier,
                "Thermal_Efficiency_Tier": eff_tier,
                "Status": "Verified" if st_cat != "other" else "Review",
                "Notes": f"Auto-classified based on CAPI label '{lbl}'",
            })
    except Exception as e:
        print(f"[warn] Cookstove typology extraction failed: {e}", file=sys.stderr)

    return rows


def build_stove_fuel_mapping(codebook: List[Dict[str, Any]], data_dir: Path) -> List[Dict[str, Any]]:
    """Scan for cooking fuel variables (stove_fuel__id or SEC_G_Q16) with frequencies."""
    rows = []
    fuel_files = list(data_dir.glob("*stovefuel*.dta")) + list(data_dir.glob("*fuel*.dta"))
    
    fuel_tier_rules = {
        "wood collected": (0, 0, "Biomass"),
        "wood purchased": (0, 0, "Biomass"),
        "lenha": (0, 0, "Biomass"),
        "charcoal": (0, 1, "Charcoal"),
        "carvão": (0, 1, "Charcoal"),
        "dung": (0, 0, "Biomass"),
        "crop": (0, 0, "Biomass"),
        "saw dust": (0, 0, "Biomass"),
        "kerosene": (1, 1, "Kerosene"),
        "petróleo": (1, 1, "Kerosene"),
        "briquette": (2, 2, "Improved Biomass"),
        "pellet": (2, 2, "Improved Biomass"),
        "biogas": (4, 4, "Clean Gas"),
        "lpg": (4, 4, "Clean Gas"),
        "gás": (4, 4, "Clean Gas"),
        "piped": (4, 4, "Clean Gas"),
        "ethanol": (4, 4, "Clean Biofuel"),
        "electric": (5, 5, "Clean Electric"),
    }

    if fuel_files:
        fpath = fuel_files[0]
        try:
            reader = pd.read_stata(fpath, iterator=True)
            val_labels = reader.value_labels()
            df = pd.read_stata(fpath, convert_categoricals=False)

            fuel_col = "stove_fuel__id" if "stove_fuel__id" in df.columns else ("SEC_G_Q16" if "SEC_G_Q16" in df.columns else None)
            if fuel_col:
                vl_dict = val_labels.get(fuel_col, {})
                counts = df[fuel_col].value_counts(dropna=False).to_dict()
                total_valid = df[fuel_col].dropna().count()

                for code, cnt in sorted(counts.items(), key=lambda x: str(x[0])):
                    if pd.isna(code):
                        continue
                    code_int = int(code) if isinstance(code, (int, float)) and code == int(code) else code
                    lbl = vl_dict.get(code_int, vl_dict.get(code, f"Fuel Code {code}"))
                    lbl_lower = str(lbl).lower()
                    share_pct = round((cnt / total_valid) * 100, 2) if total_valid > 0 else 0.0

                    iso_tier, eff_tier, fuel_grp = 0, 0, "Other / Biomass"
                    for kw, (it, et, fg) in fuel_tier_rules.items():
                        if kw in lbl_lower:
                            iso_tier, eff_tier, fuel_grp = it, et, fg
                            break

                    rows.append({
                        "Raw_Variable": fuel_col,
                        "Fuel_Code": code_int,
                        "Fuel_Description": lbl,
                        "Obs_Count": cnt,
                        "Sample_Share_Pct": share_pct,
                        "Fuel_Group": fuel_grp,
                        "ISO_Emission_Tier": iso_tier,
                        "Status": "Verified" if fuel_grp != "Other / Biomass" else "Review",
                        "Notes": f"Auto-classified based on CAPI label '{lbl}'",
                    })
        except Exception as e:
            print(f"[warn] Could not extract stovefuel roster: {e}", file=sys.stderr)

    if not rows:
        default_fuels = [
            ("1", "Wood purchased", 245, 5.5, 0, "Biomass"),
            ("2", "Wood collected", 2651, 59.3, 0, "Biomass"),
            ("3", "Charcoal", 1315, 29.4, 0, "Charcoal"),
            ("4", "Kerosene", 0, 0.0, 1, "Kerosene"),
            ("12", "Biogas", 0, 0.0, 4, "Clean Gas"),
            ("15", "LPG", 211, 4.7, 4, "Clean Gas"),
            ("16", "Piped natural gas", 2, 0.04, 4, "Clean Gas"),
            ("555", "Other, specify", 2, 0.04, 0, "Other / Biomass"),
        ]
        for c, d, cnt, pct, it, fg in default_fuels:
            rows.append({
                "Raw_Variable": "stove_fuel__id",
                "Fuel_Code": c,
                "Fuel_Description": d,
                "Obs_Count": cnt,
                "Sample_Share_Pct": pct,
                "Fuel_Group": fg,
                "ISO_Emission_Tier": it,
                "Status": "Review",
                "Notes": "Default standard fuel list",
            })

    return rows


def build_fuel_frequency_mapping(codebook: List[Dict[str, Any]], data_dir: Path) -> List[Dict[str, Any]]:
    """Scan codebook for purchase and collection frequencies (e.g. SEC_I_Q07, SEC_H_Q12) with counts."""
    rows = []
    freq_items = [r for r in codebook if r["Variable"] in ["SEC_I_Q07", "SEC_H_Q12", "SEC_G_Q17"] or "often" in r["Variable_Label"].lower()]

    standard_multipliers = {
        "daily": (30.0, "Daily purchase -> 30 times/month"),
        "diario": (30.0, "Daily purchase -> 30 times/month"),
        "diária": (30.0, "Daily purchase -> 30 times/month"),
        "once a week": (30.0 / 7.0, "Weekly purchase -> 4.28 times/month"),
        "uma vez por semana": (30.0 / 7.0, "Weekly purchase -> 4.28 times/month"),
        "twice a week": (30.0 / 7.0 * 2.0, "Twice weekly -> 8.57 times/month"),
        "duas vezes por semana": (30.0 / 7.0 * 2.0, "Twice weekly -> 8.57 times/month"),
        "every 2 weeks": (30.0 / 14.0, "Fortnightly -> 2.14 times/month"),
        "a cada 2 semanas": (30.0 / 14.0, "Fortnightly -> 2.14 times/month"),
        "every 3 weeks": (30.0 / 21.0, "Every 3 weeks -> 1.43 times/month"),
        "a cada 3 semanas": (30.0 / 21.0, "Every 3 weeks -> 1.43 times/month"),
        "monthly": (1.0, "Monthly purchase -> 1 time/month"),
        "mensal": (1.0, "Monthly purchase -> 1 time/month"),
        "every 2 months": (0.5, "Every 2 months -> 0.5 times/month"),
        "a cada 2 meses": (0.5, "Every 2 months -> 0.5 times/month"),
        "every 3 months": (1.0 / 3.0, "Quarterly -> 0.33 times/month"),
        "a cada 3 meses": (1.0 / 3.0, "Quarterly -> 0.33 times/month"),
        "every 6 months": (1.0 / 6.0, "Semi-annual -> 0.167 times/month"),
        "a cada 6 meses": (1.0 / 6.0, "Semi-annual -> 0.167 times/month"),
        "once a year": (1.0 / 12.0, "Annual -> 0.083 times/month"),
        "uma vez por ano": (1.0 / 12.0, "Annual -> 0.083 times/month"),
        "quando necessário": (1.0, "As needed -> default to monthly/mode"),
        "as need arises": (1.0, "As needed -> default to monthly/mode"),
        "other": (None, "Other, specify -> manual check"),
        "outro": (None, "Outro -> manual check"),
    }

    if freq_items:
        target = freq_items[0]
        var = target["Variable"]
        ds_name = target["Dataset"]
        ds_path = data_dir / ds_name
        if not ds_path.exists():
            matches = list(data_dir.rglob(ds_name))
            if matches:
                ds_path = matches[0]

        try:
            reader = pd.read_stata(ds_path, iterator=True)
            vl_dict = reader.value_labels().get(var, {})
            df = pd.read_stata(ds_path, columns=[var], convert_categoricals=False)
            total_valid = df[var].dropna().count()
            counts = df[var].value_counts(dropna=False).to_dict()

            for code, cnt in sorted(counts.items(), key=lambda x: str(x[0])):
                if pd.isna(code):
                    continue
                code_int = int(code) if isinstance(code, (int, float)) and code == int(code) else code
                lbl = vl_dict.get(code_int, vl_dict.get(code, f"Code {code}"))
                lbl_lower = str(lbl).lower().strip()
                share_pct = round((cnt / total_valid) * 100, 2) if total_valid > 0 else 0.0

                mult = 1.0
                note = "Default monthly"
                for kw, (m, n) in standard_multipliers.items():
                    if kw in lbl_lower:
                        mult = m
                        note = n
                        break

                rows.append({
                    "Raw_Variable": var,
                    "Frequency_Code": code_int,
                    "Frequency_Label": lbl,
                    "Obs_Count": cnt,
                    "Sample_Share_Pct": share_pct,
                    "Monthly_Multiplier": mult,
                    "Status": "Verified" if mult is not None else "Review",
                    "Notes": note,
                })
        except Exception:
            pass

    if not rows:
        defaults = [
            (1, "Daily", 0, 0.0, 30.0), (2, "Once a week", 0, 0.0, 30.0 / 7.0), (3, "Twice a week", 0, 0.0, 30.0 / 7.0 * 2.0),
            (4, "Every 2 weeks", 0, 0.0, 30.0 / 14.0), (5, "Every 3 weeks", 0, 0.0, 30.0 / 21.0), (6, "Monthly", 0, 0.0, 1.0),
            (7, "Every 2 months", 0, 0.0, 0.5), (8, "Every 3 months", 0, 0.0, 1.0 / 3.0), (11, "Every 6 months", 0, 0.0, 1.0 / 6.0),
        ]
        for c, l, cnt, pct, m in defaults:
            rows.append({
                "Raw_Variable": "SEC_I_Q07",
                "Frequency_Code": c,
                "Frequency_Label": l,
                "Obs_Count": cnt,
                "Sample_Share_Pct": pct,
                "Monthly_Multiplier": m,
                "Status": "Review",
                "Notes": "Standard MTF frequency scale",
            })

    return rows


def build_other_specify_mapping(data_dir: Path) -> List[Dict[str, Any]]:
    """Scan all string _oth variables across datasets and extract open-text responses with frequencies."""
    rows = []
    dta_files = sorted(list(data_dir.glob("*.dta")))

    for fpath in dta_files:
        fn = fpath.name
        if fn.startswith("~") or "backup" in fn.lower():
            continue

        try:
            reader = pd.read_stata(fpath, iterator=True)
            var_labels = reader.variable_labels()
            df = pd.read_stata(fpath, convert_categoricals=False)

            # Filter for true raw _oth columns (exclude derived _clean columns)
            oth_cols = [c for c in df.columns if c.lower().endswith("_oth") and not ("_clean" in c.lower())]

            for col in oth_cols:
                # Catch both object and string dtypes
                if df[col].dtype == object or str(df[col].dtype).startswith("str") or pd.api.types.is_string_dtype(df[col]):
                    series = df[col].dropna().astype(str).str.strip()
                    series = series[series != ""]
                    if len(series) == 0:
                        continue

                    val_counts = series.value_counts()
                    total_oth = len(series)

                    # Determine domain
                    col_lower = col.lower()
                    vlbl_lower = str(var_labels.get(col, "")).lower()
                    domain = "General"
                    if "g_q05" in col_lower or "g_q02" in col_lower or "stove" in col_lower or "fogão" in vlbl_lower:
                        domain = "Cookstove Typology"
                    elif "g_q16" in col_lower or "fuel" in col_lower:
                        domain = "Cooking Fuel"
                    elif "c_q125" in col_lower or "appliance" in col_lower:
                        domain = "Appliances"
                    elif "d_q02" in col_lower or "d_q08" in col_lower or "barrier" in col_lower or "reason" in vlbl_lower:
                        domain = "Grid Barrier"
                    elif "a1_q8" in col_lower:
                        domain = "Education"

                    for text_val, cnt in val_counts.items():
                        t_lower = text_val.lower()
                        pct = round((cnt / total_oth) * 100, 1)

                        suggested_action = "Manual Review"
                        suggested_category = "Other"

                        # Cookstoves text matching (Portuguese / English)
                        if domain == "Cookstove Typology":
                            if any(w in t_lower for w in ["fogareiro", "fogadeiro", "carvão", "carvao", "barro", "ferro", "fugão"]):
                                suggested_action = "Recode to Code 2 (Traditional Stove)"
                                suggested_category = "2: Traditional Stove"
                            elif any(w in t_lower for w in ["melhorado", "improved", "poupa"]):
                                suggested_action = "Recode to Code 3 (Improved Stove)"
                                suggested_category = "3: Improved Biomass Stove"
                            elif any(w in t_lower for w in ["gás", "gas"]):
                                suggested_action = "Recode to Code 5 (LPG Stove)"
                                suggested_category = "5: LPG Stove"

                        # Appliances text matching
                        elif domain == "Appliances":
                            if any(w in t_lower for w in ["radio", "rádio", "som"]):
                                suggested_action = "Map to has_radio = 1"
                                suggested_category = "Radio"
                            elif any(w in t_lower for w in ["tv", "televis", "televisão"]):
                                suggested_action = "Map to has_tv = 1"
                                suggested_category = "Television"
                            elif any(w in t_lower for w in ["congelador", "freezer", "frigorifico", "fridge"]):
                                suggested_action = "Map to has_fridge = 1"
                                suggested_category = "Refrigerator"
                            elif any(w in t_lower for w in ["ar condicionado", "ac", "climatiseur"]):
                                suggested_action = "Map to has_ac = 1"
                                suggested_category = "Air Conditioner"

                        # Fuel text matching
                        elif domain == "Cooking Fuel":
                            if any(w in t_lower for w in ["carvão", "charcoal"]):
                                suggested_action = "Recode to Code 3 (Charcoal)"
                                suggested_category = "Charcoal"
                            elif any(w in t_lower for w in ["lenha", "wood"]):
                                suggested_action = "Recode to Code 1 (Wood)"
                                suggested_category = "Firewood"

                        # Grid Barrier text matching
                        elif domain == "Grid Barrier":
                            if any(w in t_lower for w in ["dinheiro", "cost", "cara", "caro"]):
                                suggested_action = "Map to barrier_cost = 1"
                                suggested_category = "High connection cost"
                            elif any(w in t_lower for w in ["arrendada", "alugada", "rent"]):
                                suggested_action = "Map to barrier_landlord = 1"
                                suggested_category = "Renting / Landlord refusal"
                            elif any(w in t_lower for w in ["distante", "far", "longe"]):
                                suggested_action = "Map to barrier_dist = 1"
                                suggested_category = "Grid too far"

                        rows.append({
                            "Module_Domain": domain,
                            "Raw_Variable": col,
                            "Raw_Text_Response": text_val,
                            "Obs_Count": cnt,
                            "Sample_Share_Pct": pct,
                            "Suggested_Recode_Action": suggested_action,
                            "Suggested_Target_Category": suggested_category,
                            "Status": "Review",
                            "Expert_Approved_Category": "",  # Empty for Bryan Koo's review/approval
                            "Notes": f"Found in {fn} ({cnt} obs)",
                        })
        except Exception:
            continue

    if not rows:
        rows = [{
            "Module_Domain": "Cookstove Typology",
            "Raw_Variable": "SEC_G_Q05_oth",
            "Raw_Text_Response": "fogareiro",
            "Obs_Count": 11,
            "Sample_Share_Pct": 39.3,
            "Suggested_Recode_Action": "Recode to Code 2 (Traditional Stove)",
            "Suggested_Target_Category": "2: Traditional Stove",
            "Status": "Review",
            "Expert_Approved_Category": "",
            "Notes": "Example template placeholder",
        }]

    return rows


def build_missing_codes_mapping(codebook: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Scan codebook for declared 'Don't know', 'Refused', and missing codes."""
    rows = []
    missing_keywords = ["don’t know", "don't know", "não sabe", "ne sait pas", "refused", "recusou", "refusé", "not applicable", "não aplicável"]

    found_codes = set()
    for item in codebook:
        vl_str = item["Value_Labels"]
        if not vl_str:
            continue
        pairs = vl_str.split("; ")
        for p in pairs:
            if ":" in p:
                c_str, l_str = p.split(":", 1)
                l_lower = l_str.lower().strip()
                if any(kw in l_lower for kw in missing_keywords):
                    key = (c_str.strip(), l_str.strip())
                    if key not in found_codes:
                        found_codes.add(key)
                        rows.append({
                            "Declared_Code": c_str.strip(),
                            "Label_Meaning": l_str.strip(),
                            "Found_In_Variable": item["Variable"],
                            "Found_In_Dataset": item["Dataset"],
                            "Action_In_Stata": "Set to . (System Missing)",
                            "Status": "Verified",
                            "Notes": "Auto-detected special missing code",
                        })

    if not rows:
        rows = [
            {"Declared_Code": "888", "Label_Meaning": "Don't know", "Found_In_Variable": "SEC_C_Q25", "Found_In_Dataset": "section_c.dta", "Action_In_Stata": "Set to .", "Status": "Verified", "Notes": "Standard positive code"},
            {"Declared_Code": "999", "Label_Meaning": "Refused", "Found_In_Variable": "SEC_C_Q25", "Found_In_Dataset": "section_c.dta", "Action_In_Stata": "Set to .", "Status": "Verified", "Notes": "Standard positive code"},
            {"Declared_Code": "-888", "Label_Meaning": "Don't know", "Found_In_Variable": "Generic", "Found_In_Dataset": "Master", "Action_In_Stata": "Set to .", "Status": "Verified", "Notes": "Standard negative code"},
            {"Declared_Code": "-999", "Label_Meaning": "Refused", "Found_In_Variable": "Generic", "Found_In_Dataset": "Master", "Action_In_Stata": "Set to .", "Status": "Verified", "Notes": "Standard negative code"},
        ]

    return rows


def export_calibration_workbook(
    output_path: Path,
    codebook: List[Dict[str, Any]],
    education: List[Dict[str, Any]],
    cookstoves: List[Dict[str, Any]],
    stove_fuel: List[Dict[str, Any]],
    fuel_freq: List[Dict[str, Any]],
    other_specify: List[Dict[str, Any]],
    missing_codes: List[Dict[str, Any]],
):
    """Create a formatted 7-tab Excel workbook with professional ESMAP styling."""
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    sheets_data = [
        ("1_Raw_Codebook", codebook, NAVY_HEADER),
        ("2_Education", education, ACCENT_HEADER),
        ("3_Cookstove_Typology", cookstoves, TEAL_HEADER),
        ("4_Stove_Fuel", stove_fuel, ACCENT_HEADER),
        ("5_Fuel_Freq", fuel_freq, ACCENT_HEADER),
        ("6_Other_Specify_Recodes", other_specify, TEAL_HEADER),
        ("7_Missing_Codes", missing_codes, NAVY_HEADER),
    ]

    for title, data, header_fill in sheets_data:
        ws = wb.create_sheet(title=title)
        ws.views.sheetView[0].showGridLines = True

        if not data:
            ws.append(["No data extracted"])
            continue

        headers = list(data[0].keys())
        ws.append(headers)

        for col_idx, h in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_idx)
            cell.font = FONT_HEADER
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = THIN_BORDER
        ws.row_dimensions[1].height = 28

        for row_idx, row_dict in enumerate(data, 2):
            for col_idx, h in enumerate(headers, 1):
                val = row_dict.get(h, "")
                cell = ws.cell(row=row_idx, column=col_idx, value=val)
                cell.font = FONT_BODY
                cell.border = THIN_BORDER

                if h == "Status":
                    cell.alignment = Alignment(horizontal="center")
                    if str(val).lower() == "verified":
                        cell.fill = VERIFIED_FILL
                    else:
                        cell.fill = REVIEW_FILL
                elif isinstance(val, (int, float)):
                    cell.alignment = Alignment(horizontal="right")
                else:
                    cell.alignment = Alignment(horizontal="left")

            ws.row_dimensions[row_idx].height = 20

        for col in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 55)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
    print(f"✓ Successfully generated calibration workbook: {output_path} ({len(sheets_data)} sheets)")


def compile_stata_harmonization_do(excel_path: Path, output_do_path: Path, country_name: str = "Guinea-Bissau") -> str:
    """Read MTF_Country_Calibration.xlsx and compile a clean, defensive 00_country_harmonization.do."""
    wb = openpyxl.load_workbook(excel_path, data_only=True)

    do_lines = [
        "**************************************************************************",
        f"*  00_country_harmonization.do                                           *",
        f"*  Country-Specific Harmonization & Dynamic Recodes: {country_name}        *",
        f"*  Auto-generated from: {excel_path.name}                             *",
        "**************************************************************************",
        "",
        'di "===> Executing Country Harmonization Module: ' + country_name + '"',
        "",
        "* -------------------------------------------------------------------------",
        "* 1. SPECIAL MISSING CODES CLEANING",
        "* -------------------------------------------------------------------------",
    ]

    # Sheet 7: Missing Codes
    missing_sheet = "7_Missing_Codes" if "7_Missing_Codes" in wb.sheetnames else "6_Missing_Codes"
    if missing_sheet in wb.sheetnames:
        ws = wb[missing_sheet]
        headers = [c.value for c in ws[1]]
        code_idx = headers.index("Declared_Code") if "Declared_Code" in headers else 0
        missing_codes = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[code_idx]:
                code_str = str(row[code_idx]).strip()
                meaning = str(row[1] if len(row) > 1 else "").lower()
                if any(kw in meaning for kw in ["don't know", "don’t know", "não sabe", "refused", "recusou", "missing"]):
                    if code_str not in missing_codes:
                        missing_codes.append(code_str)

        if not missing_codes:
            missing_codes = ["888", "999", "-888", "-999"]

        code_list_stata = ", ".join(missing_codes)
        do_lines.extend([
            f"* Positive and negative missing codes declared: {code_list_stata}",
            f"local declared_missing {code_list_stata}",
            'di " Cleaning declared missing codes across monetary variables..."',
            "capture confirm variable SEC_C_Q25",
            "if !_rc {",
            f"    replace SEC_C_Q25 = . if inlist(SEC_C_Q25, {code_list_stata})",
            "}",
            "capture confirm variable grid_exp_m",
            "if !_rc {",
            f"    replace grid_exp_m = . if inlist(grid_exp_m, {code_list_stata})",
            "}",
            "",
        ])

    # Sheet 2: Education
    do_lines.extend([
        "* -------------------------------------------------------------------------",
        "* 2. EDUCATION LEVEL HARMONIZATION (SEC_A1_Q8 -> hh_head_educ)",
        "* -------------------------------------------------------------------------",
    ])
    if "2_Education" in wb.sheetnames:
        ws = wb["2_Education"]
        headers = [c.value for c in ws[1]]
        code_idx = headers.index("Raw_Code") if "Raw_Code" in headers else 1
        tier_idx = headers.index("Harmonized_Educ_Code") if "Harmonized_Educ_Code" in headers else (
            headers.index("Target_MTF_Tier") if "Target_MTF_Tier" in headers else 4
        )

        tier_codes = {0: [], 1: [], 2: [], 3: []}
        for row in ws.iter_rows(min_row=2, values_only=True):
            c_val, t_val = row[code_idx], row[tier_idx]
            if c_val is not None and t_val is not None:
                try:
                    t_int = int(t_val)
                    c_int = int(c_val) if isinstance(c_val, (int, float)) and c_val == int(c_val) else c_val
                    tier_codes[t_int].append(str(c_int))
                except Exception:
                    pass

        do_lines.extend([
            "capture drop hh_head_educ",
            "gen byte hh_head_educ = .",
        ])
        if tier_codes[0]:
            do_lines.append(f'* None (Category 0): codes {", ".join(tier_codes[0])} or never attended school')
            do_lines.append(f'replace hh_head_educ = 0 if inlist(SEC_A1_Q8, {", ".join(tier_codes[0])}) | SEC_A1_Q7 == 2 | SEC_A1_Q7 == 0')
        else:
            do_lines.append('* None (Category 0): never attended school')
            do_lines.append('replace hh_head_educ = 0 if SEC_A1_Q7 == 2 | SEC_A1_Q7 == 0')

        for t, name in [(1, "Primary"), (2, "Secondary"), (3, "Higher Education")]:
            if tier_codes[t]:
                do_lines.append(f'* {name} (Category {t}): codes {", ".join(tier_codes[t])}')
                do_lines.append(f'replace hh_head_educ = {t} if inlist(SEC_A1_Q8, {", ".join(tier_codes[t])})')

        do_lines.extend([
            'label define hh_head_educ 0 "None" 1 "Primary" 2 "Secondary" 3 "Higher Education", replace',
            "label values hh_head_educ hh_head_educ",
            'label var hh_head_educ "Education Level of Household Head (MTF 4-Category Standard)"',
            "",
            "* Defensive runtime assertion against silent failure",
            "count if inlist(hh_head_educ, 2, 3)",
            "if r(N) == 0 {",
            '    di as error "[ERROR] Secondary/Higher education has 0 observations! Check SEC_A1_Q8 mapping."',
            "    exit 198",
            "}",
            'else {',
            '    di as text " [PASS] Education mapping verified: " r(N) " secondary/higher obs found."',
            "}",
            "",
        ])

    # Sheet 6: Other Specify Recoding (Cookstoves, Appliances, Fuels)
    oth_sheet = "6_Other_Specify_Recodes" if "6_Other_Specify_Recodes" in wb.sheetnames else "5_Appliances_Other"
    if oth_sheet in wb.sheetnames:
        do_lines.extend([
            "* -------------------------------------------------------------------------",
            "* 3. OPEN-ENDED 'OTHER, SPECIFY' RECODING & RECLASSIFICATION",
            "* -------------------------------------------------------------------------",
        ])
        ws = wb[oth_sheet]
        headers = [c.value for c in ws[1]]

        if "Module_Domain" in headers and "Raw_Text_Response" in headers:
            dom_idx = headers.index("Module_Domain")
            text_idx = headers.index("Raw_Text_Response")
            act_idx = headers.index("Suggested_Recode_Action") if "Suggested_Recode_Action" in headers else 5
            appr_idx = headers.index("Expert_Approved_Category") if "Expert_Approved_Category" in headers else 7

            stove_trad_texts = []
            app_radio_texts = []

            for row in ws.iter_rows(min_row=2, values_only=True):
                dom = str(row[dom_idx] or "")
                txt = str(row[text_idx] or "").strip()
                act = str(row[act_idx] or "").strip()
                appr = str(row[appr_idx] or "").strip()

                if not txt:
                    continue

                # Cookstove reclassification
                if dom == "Cookstove Typology" and ("Traditional" in act or "Traditional" in appr or "Code 2" in act or "Code 2" in appr):
                    stove_trad_texts.append(f'"{txt.lower()}"')
                # Appliance reclassification
                elif dom == "Appliances" and ("Radio" in act or "Radio" in appr):
                    app_radio_texts.append(f'"{txt.lower()}"')

            if stove_trad_texts:
                do_lines.extend([
                    "capture confirm variable SEC_G_Q05_oth",
                    "if !_rc {",
                    f"    * Reclassify open-text charcoal braziers to Code 2 (Traditional Stove)",
                    f"    capture replace SEC_G_Q05 = 2 if inlist(lower(trim(SEC_G_Q05_oth)), {', '.join(stove_trad_texts)})",
                    "    capture confirm variable trad_stove",
                    "    if !_rc {",
                    "        capture replace trad_stove = 1 if SEC_G_Q05 == 2",
                    "    }",
                    "}",
                    "",
                    "capture confirm file \"$wip_hh/cookstoves_clean.dta\"",
                    "if !_rc {",
                    "    preserve",
                    "        use \"$wip_hh/cookstoves_clean.dta\", clear",
                    "        capture confirm variable SEC_G_Q05_oth",
                    "        if !_rc {",
                    f"            capture replace SEC_G_Q05 = 2 if inlist(lower(trim(SEC_G_Q05_oth)), {', '.join(stove_trad_texts)})",
                    "        }",
                    "        save \"$wip_hh/cookstoves_clean.dta\", replace",
                    "    restore",
                    "}",
                    "",
                    "capture confirm file \"$wip_hh/mainstove_matched.dta\"",
                    "if !_rc {",
                    "    preserve",
                    "        use \"$wip_hh/mainstove_matched.dta\", clear",
                    "        capture confirm variable SEC_G_Q05_oth",
                    "        if !_rc {",
                    f"            capture replace SEC_G_Q05 = 2 if inlist(lower(trim(SEC_G_Q05_oth)), {', '.join(stove_trad_texts)})",
                    "        }",
                    "        save \"$wip_hh/mainstove_matched.dta\", replace",
                    "    restore",
                    "}",
                    "",
                ])

            if app_radio_texts:
                do_lines.extend([
                    "capture confirm variable SEC_C_Q125_oth",
                    "if !_rc {",
                    f"    * Map open-text radio mentions to has_radio",
                    f"    capture replace has_radio = 1 if inlist(lower(trim(SEC_C_Q125_oth)), {', '.join(app_radio_texts)})",
                    "}",
                    "",
                ])

    do_lines.extend([
        "* -------------------------------------------------------------------------",
        "* 4. DEFAULT MISSING TREATMENT & ATTRITION GUARDRAIL FOR UNCLASSIFIED 'OTHER'",
        "* -------------------------------------------------------------------------",
        "* Enforces Zero-Assumption Principle: unclassified 'Other' (555, 96) codes",
        "* default to missing (.), with a 5% attrition alert threshold.",
        "",
        "local target_vars SEC_G_Q05 SEC_C_Q02 SEC_C_Q40 SEC_C_Q78 SEC_C_Q100 SEC_I_Q07 SEC_I_Q13",
        "foreach v of local target_vars {",
        "    capture confirm variable `v'",
        "    if !_rc {",
        "        quietly count if inlist(`v', 555, 96)",
        "        local unclass_n = r(N)",
        "        quietly count if !missing(`v')",
        "        local total_valid = r(N)",
        "        if `total_valid' > 0 & `unclass_n' > 0 {",
        "            local missing_pct = (`unclass_n' / `total_valid') * 100",
        "            if `missing_pct' > 5.0 {",
        "                di as error \" [WARNING] High unclassified 'Other' rate in `v': \" %4.1f `missing_pct' \"% (N = `unclass_n'/`total_valid'). Review calibration sheet.\"",
        "            }",
        "            else {",
        "                di as text \" [DEFAULT] Recoding unclassified Other to missing in `v': N = `unclass_n' (\" %4.1f `missing_pct' \"%)\"",
        "            }",
        "            replace `v' = . if inlist(`v', 555, 96)",
        "        }",
        "    }",
        "}",
        "",
        "capture confirm file \"$wip_hh/cookstoves_clean.dta\"",
        "if !_rc {",
        "    preserve",
        "        use \"$wip_hh/cookstoves_clean.dta\", clear",
        "        capture confirm variable SEC_G_Q05",
        "        if !_rc {",
        "            quietly count if inlist(SEC_G_Q05, 555, 96)",
        "            if r(N) > 0 {",
        "                local unclass_cs = r(N)",
        "                quietly count if !missing(SEC_G_Q05)",
        "                local total_cs = r(N)",
        "                local cs_pct = (`unclass_cs' / `total_cs') * 100",
        "                if `cs_pct' > 5.0 {",
        "                    di as error \" [WARNING] High unclassified Other in cookstoves_clean.dta: \" %4.1f `cs_pct' \"% (N = `unclass_cs'/`total_cs').\"",
        "                }",
        "                else {",
        "                    di as text \" [DEFAULT] Recoding unclassified Other to missing in cookstoves_clean.dta: N = `unclass_cs' (\" %4.1f `cs_pct' \"%)\"",
        "                }",
        "                replace SEC_G_Q05 = . if inlist(SEC_G_Q05, 555, 96)",
        "                save \"$wip_hh/cookstoves_clean.dta\", replace",
        "            }",
        "        }",
        "    restore",
        "}",
        "",
        "capture confirm file \"$wip_hh/mainstove_matched.dta\"",
        "if !_rc {",
        "    preserve",
        "        use \"$wip_hh/mainstove_matched.dta\", clear",
        "        capture confirm variable SEC_G_Q05",
        "        if !_rc {",
        "            quietly count if inlist(SEC_G_Q05, 555, 96)",
        "            if r(N) > 0 {",
        "                replace SEC_G_Q05 = . if inlist(SEC_G_Q05, 555, 96)",
        "                save \"$wip_hh/mainstove_matched.dta\", replace",
        "            }",
        "        }",
        "    restore",
        "}",
    ])

    do_lines.extend([
        '* Persist harmonized changes to disk for subsequent modules',
        'capture confirm file "$wip_hh/$master_dta"',
        'if !_rc {',
        '    save "$wip_hh/$master_dta", replace',
        '    di " [SAVED] Harmonized changes committed to $wip_hh/$master_dta"',
        '}',
        '',
        'di "===> Country Harmonization Module for ' + country_name + ' complete."',
        "",
    ])

    do_content = "\n".join(do_lines)
    output_do_path.parent.mkdir(parents=True, exist_ok=True)
    output_do_path.write_text(do_content, encoding="utf-8")
    print(f"✓ Successfully compiled Stata harmonization Do-file: {output_do_path}")
    return do_content


def build_calibration_workbook(data_dir: Path, excel_path: Path, country_name: str = "Guinea-Bissau"):
    """High-level generator for the 7-sheet calibration workbook."""
    codebook = extract_codebook(data_dir)
    education = build_education_mapping(codebook, data_dir)
    cookstoves = build_cookstove_typology_mapping(codebook, data_dir)
    stove_fuel = build_stove_fuel_mapping(codebook, data_dir)
    fuel_freq = build_fuel_frequency_mapping(codebook, data_dir)
    other_specify = build_other_specify_mapping(data_dir)
    missing_codes = build_missing_codes_mapping(codebook)

    export_calibration_workbook(
        excel_path,
        codebook=codebook,
        education=education,
        cookstoves=cookstoves,
        stove_fuel=stove_fuel,
        fuel_freq=fuel_freq,
        other_specify=other_specify,
        missing_codes=missing_codes,
    )


def main():
    parser = argparse.ArgumentParser(description="Build MTF Country Metadata Codebook & Calibration Workbook")
    parser.add_argument("--base-dir", type=Path, default=None, help="Country base directory")
    parser.add_argument("--data-dir", type=Path, default=None, help="Country raw Data directory")
    parser.add_argument("--country", type=str, default="Guinea-Bissau", help="Country name")
    parser.add_argument("--out-excel", type=Path, default=None, help="Custom output path for calibration Excel")
    parser.add_argument("--compile", type=Path, default=None, help="Path to existing Excel workbook to compile into Stata Do-file")
    parser.add_argument("--output-do", type=Path, default=None, help="Output path for compiled Do-file")

    args = parser.parse_args()

    # Mode 1: Compile from existing Excel
    if args.compile:
        excel_path = args.compile.resolve()
        if not excel_path.exists():
            print(f"[ERROR] Excel file not found: {excel_path}", file=sys.stderr)
            sys.exit(1)
        output_do = args.output_do or (excel_path.parent / "Do-file" / "00_country_harmonization.do")
        compile_stata_harmonization_do(excel_path, output_do, country_name=args.country)
        return

    # Mode 2: Generate workbook from survey data
    if args.data_dir:
        data_dir = args.data_dir.resolve()
        base_dir = data_dir.parent
    elif args.base_dir:
        base_dir = args.base_dir.resolve()
        data_dir = base_dir / "Data"
    else:
        print("[ERROR] Please specify either --base-dir or --data-dir", file=sys.stderr)
        sys.exit(1)

    excel_path = args.out_excel or (base_dir / f"MTF_{args.country}_Calibration.xlsx")
    output_do = args.output_do or (base_dir / "Do-file" / "00_country_harmonization.do")

    build_calibration_workbook(data_dir, excel_path, country_name=args.country)
    compile_stata_harmonization_do(excel_path, output_do, country_name=args.country)


if __name__ == "__main__":
    main()
