# ESMAP MTF Pipeline — Survey "Other, Specify" Calibration Generator
# ==============================================================================
# Scans country microdata (.dta) files for open-text "Other, specify" responses,
# cataloging parent variable value labels, calculating empirical frequencies,
# attaching existing option summaries, and generating a standardized Excel
# calibration workbook with inline data validation dropdowns and a dedicated
# Value_Codebook reference tab for country coordinator review.
# ==============================================================================

import os
import sys
import glob
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation


# Styling Palette (World Bank ESMAP Standards)
NAVY_HEADER = PatternFill(start_color="002244", end_color="002244", fill_type="solid")
TEAL_HEADER = PatternFill(start_color="008080", end_color="008080", fill_type="solid")
DARK_GRAY_HEADER = PatternFill(start_color="333333", end_color="333333", fill_type="solid")
GRAY_BG = PatternFill(start_color="F2F4F7", end_color="F2F4F7", fill_type="solid")
YELLOW_FILL = PatternFill(start_color="FFF3CD", end_color="FFF3CD", fill_type="solid")
LIGHT_BLUE_FILL = PatternFill(start_color="E6F0FA", end_color="E6F0FA", fill_type="solid")

FONT_TITLE = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
FONT_HEADER = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
FONT_SECTION = Font(name="Calibri", size=11, bold=True, color="002244")
FONT_BOLD = Font(name="Calibri", size=10, bold=True)
FONT_BODY = Font(name="Calibri", size=10)
FONT_NOTE = Font(name="Calibri", size=9, italic=True, color="555555")

THIN_BORDER = Border(
    left=Side(style="thin", color="D0D5DD"),
    right=Side(style="thin", color="D0D5DD"),
    top=Side(style="thin", color="D0D5DD"),
    bottom=Side(style="thin", color="D0D5DD"),
)

DEFAULT_COOKSTOVE_ROWS = [
    {
        "questionnaire_code": "1,2", "stove_description": "Three-Stone / Open Fire",
        "iso_emission_tier": 0, "efficiency_tier": 0, "stove_group": "open_fire",
        "primary_fuel": "Gathered firewood", "notes": "Very low thermal efficiency (< 10%)",
        "stat_key_nat": "STOVE_3STONE_N", "stat_key_urb": "STOVE_3STONE_U", "stat_key_rur": "STOVE_3STONE_R",
    },
    {
        "questionnaire_code": "3,5,22", "stove_description": "Traditional / Local Stove",
        "iso_emission_tier": 0, "efficiency_tier": 0, "stove_group": "traditional",
        "primary_fuel": "Wood / Charcoal", "notes": "Uninsulated metal grate or brazier",
        "stat_key_nat": "STOVE_TRAD_N", "stat_key_urb": "STOVE_TRAD_U", "stat_key_rur": "STOVE_TRAD_R",
    },
    {
        "questionnaire_code": "4,6,7,8,9,20,21", "stove_description": "Improved Cookstove (ICS)",
        "iso_emission_tier": 3, "efficiency_tier": 2, "stove_group": "ics",
        "primary_fuel": "Firewood / Charcoal", "notes": "Enclosed combustion chamber (Tier 1-3 emission)",
        "stat_key_nat": "STOVE_ICS_N", "stat_key_urb": "STOVE_ICS_U", "stat_key_rur": "STOVE_ICS_R",
    },
    {
        "questionnaire_code": "10,11,12,13,14,23", "stove_description": "Clean Fuel: LPG / Biogas",
        "iso_emission_tier": 4, "efficiency_tier": 4, "stove_group": "clean_gas",
        "primary_fuel": "Bottled LPG", "notes": "Clean burning gas fuel",
        "stat_key_nat": "STOVE_CLEAN_N", "stat_key_urb": "STOVE_CLEAN_U", "stat_key_rur": "STOVE_CLEAN_R",
    },
    {
        "questionnaire_code": "19", "stove_description": "Clean Fuel: Electric Stove",
        "iso_emission_tier": 5, "efficiency_tier": 5, "stove_group": "clean_electric",
        "primary_fuel": "Grid electricity", "notes": "Zero indoor emissions",
        "stat_key_nat": "STOVE_ELEC_N", "stat_key_urb": "STOVE_ELEC_U", "stat_key_rur": "STOVE_ELEC_R",
    },
]

GNB_COOKSTOVE_ROWS = [
    {
        "questionnaire_code": "1", "stove_description": "Three-Stone / Open Fire",
        "iso_emission_tier": 0, "efficiency_tier": 0, "stove_group": "open_fire",
        "primary_fuel": "Gathered firewood", "notes": "Very low thermal efficiency (< 10%)",
        "stat_key_nat": "STOVE_3STONE_N", "stat_key_urb": "STOVE_3STONE_U", "stat_key_rur": "STOVE_3STONE_R",
    },
    {
        "questionnaire_code": "2", "stove_description": "Traditional / Locally Built Stove",
        "iso_emission_tier": 0, "efficiency_tier": 0, "stove_group": "traditional",
        "primary_fuel": "Wood / Charcoal", "notes": "Uninsulated local brazier (fogareiro)",
        "stat_key_nat": "STOVE_TRAD_N", "stat_key_urb": "STOVE_TRAD_U", "stat_key_rur": "STOVE_TRAD_R",
    },
    {
        "questionnaire_code": "3", "stove_description": "Improved Biomass Stove (ICS)",
        "iso_emission_tier": 3, "efficiency_tier": 2, "stove_group": "ics",
        "primary_fuel": "Firewood / Charcoal", "notes": "Enclosed combustion chamber with insulation",
        "stat_key_nat": "STOVE_ICS_N", "stat_key_urb": "STOVE_ICS_U", "stat_key_rur": "STOVE_ICS_R",
    },
    {
        "questionnaire_code": "4", "stove_description": "Kerosene Stove",
        "iso_emission_tier": 1, "efficiency_tier": 1, "stove_group": "traditional",
        "primary_fuel": "Kerosene", "notes": "Kerosene burner (Tier 1 emission)",
        "stat_key_nat": "STOVE_TRAD_N", "stat_key_urb": "STOVE_TRAD_U", "stat_key_rur": "STOVE_TRAD_R",
    },
    {
        "questionnaire_code": "5,6", "stove_description": "Clean Fuel: LPG / Piped Gas",
        "iso_emission_tier": 4, "efficiency_tier": 4, "stove_group": "clean_gas",
        "primary_fuel": "Bottled LPG / Piped Gas", "notes": "Clean gaseous fuel",
        "stat_key_nat": "STOVE_CLEAN_N", "stat_key_urb": "STOVE_CLEAN_U", "stat_key_rur": "STOVE_CLEAN_R",
    },
    {
        "questionnaire_code": "7", "stove_description": "Clean Fuel: Electric Stove",
        "iso_emission_tier": 5, "efficiency_tier": 5, "stove_group": "clean_electric",
        "primary_fuel": "Grid electricity", "notes": "Zero indoor emissions",
        "stat_key_nat": "STOVE_ELEC_N", "stat_key_urb": "STOVE_ELEC_U", "stat_key_rur": "STOVE_ELEC_R",
    },
    {
        "questionnaire_code": "8", "stove_description": "Solar Cooker",
        "iso_emission_tier": 5, "efficiency_tier": 5, "stove_group": "clean_solar",
        "primary_fuel": "Solar radiation", "notes": "Clean solar cooking",
        "stat_key_nat": "STOVE_SOLAR_N", "stat_key_urb": "STOVE_SOLAR_U", "stat_key_rur": "STOVE_SOLAR_R",
    },
    {
        "questionnaire_code": "555", "stove_description": "Other Cookstove",
        "iso_emission_tier": "", "efficiency_tier": "", "stove_group": "other",
        "primary_fuel": "Other / Unspecified", "notes": "Recode from open-text responses after reviewing data",
        "stat_key_nat": "STOVE_OTHER_N", "stat_key_urb": "STOVE_OTHER_U", "stat_key_rur": "STOVE_OTHER_R",
    },
]


def extract_other_specify(
    data_dir: str,
    output_xlsx: str,
    country: str = "Guinea-Bissau",
    country_iso3: str = "GNB",
    cookstove_config: Optional[str] = None,
    existing_calibration: Optional[str] = None
):
    data_path = Path(data_dir)
    dta_files = sorted(glob.glob(str(data_path / "*.dta")))
    if not dta_files:
        print(f"[ERROR] No .dta files found in {data_dir}", file=sys.stderr)
        return

    print(f"[*] Scanning {len(dta_files)} microdata files in {data_dir}...")

    # -------------------------------------------------------------------------
    # 0. CHECK FOR EXISTING CALIBRATION TO PRESERVE MANUAL EDITS
    # -------------------------------------------------------------------------
    existing_approved: Dict[Tuple[str, str], str] = {}
    existing_cookstoves: Optional[List[Dict[str, Any]]] = None
    existing_meta: Dict[str, Any] = {}

    out_path = Path(output_xlsx)
    sources_to_check: List[Path] = []
    if existing_calibration and Path(existing_calibration).exists():
        sources_to_check.append(Path(existing_calibration))
    if out_path.exists() and out_path not in sources_to_check:
        sources_to_check.append(out_path)
    for default_p in [
        Path(data_dir).parent / "Tools" / "other_specify_calibration.xlsx",
        Path("Tools/other_specify_calibration.xlsx"),
        Path("/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/37_Guinea-Bissau/Tools/other_specify_calibration.xlsx")
    ]:
        if default_p.exists() and default_p not in sources_to_check:
            sources_to_check.append(default_p)

    for src_path in sources_to_check:
        try:
            try:
                ex_df = pd.read_excel(src_path, sheet_name="Other_Specify_Recodes")
                if "variable_name" in ex_df.columns and "raw_text_response" in ex_df.columns and "coordinator_approved_code" in ex_df.columns:
                    for _, r in ex_df.iterrows():
                        v = str(r["variable_name"]).strip()
                        t = str(r["raw_text_response"]).strip().lower()
                        c = r["coordinator_approved_code"]
                        if pd.notna(c) and str(c).strip() != "":
                            existing_approved[(v, t)] = str(c).strip()
            except Exception:
                pass

            if not existing_cookstoves:
                try:
                    ex_cs = pd.read_excel(src_path, sheet_name="Cookstove_Typology")
                    if not ex_cs.empty and "questionnaire_code" in ex_cs.columns:
                        existing_cookstoves = ex_cs.to_dict(orient="records")
                except Exception:
                    pass

            if not existing_meta:
                try:
                    ex_meta_df = pd.read_excel(src_path, sheet_name="Instructions_&_Metadata", header=None)
                    for _, r in ex_meta_df.iterrows():
                        k = str(r[0]).strip() if pd.notna(r[0]) else ""
                        val = r[1] if len(r) > 1 and pd.notna(r[1]) else ""
                        if k:
                            existing_meta[k] = val
                except Exception:
                    pass
        except Exception as e:
            print(f"[!] Note: Could not read from {src_path.name}: {e}")

    if existing_approved:
        print(f"    - Ingested {len(existing_approved)} pre-approved coordinator recodes from existing source(s).")

    # -------------------------------------------------------------------------
    # 1. PRE-SCAN: BUILD GLOBAL CATALOG OF VALUE LABELS & DUMMIES
    # -------------------------------------------------------------------------
    global_val_labels: Dict[str, Dict[int, str]] = {}
    global_var_labels: Dict[str, str] = {}
    global_dummies: Dict[str, Dict[str, str]] = {}

    for fpath in dta_files:
        try:
            reader = pd.io.stata.StataReader(fpath)
            v_labels = reader.variable_labels()
            val_labels = reader.value_labels()
            global_var_labels.update(v_labels)

            # Store value labels (normalize key to uppercase for robust matching)
            for k, v in val_labels.items():
                if k not in global_val_labels:
                    global_val_labels[k] = {int(code): str(lbl) for code, lbl in v.items()}

            # Catalog multi-select dummy variables (e.g. SEC_C_Q125__1, SEC_C_Q125__2)
            for col, lbl in v_labels.items():
                if "__" in col:
                    parts = col.split("__", 1)
                    parent = parts[0]
                    code = parts[1]
                    if parent not in global_dummies:
                        global_dummies[parent] = {}
                    global_dummies[parent][code] = str(lbl).strip()
        except Exception as e:
            pass

    print(f"    - Cataloged {len(global_val_labels)} value label sets & {len(global_dummies)} multi-select dummy parents.")

    # -------------------------------------------------------------------------
    # 2. SCAN OPEN-ENDED "OTHER, SPECIFY" RESPONSES & RESOLVE PARENTS
    # -------------------------------------------------------------------------
    records: List[Dict[str, Any]] = []
    codebook_records: List[Dict[str, Any]] = []
    seen_codebook_keys = set()

    for fpath in dta_files:
        fname = os.path.basename(fpath)
        try:
            reader = pd.io.stata.StataReader(fpath)
            var_labels = reader.variable_labels()
            df = pd.read_stata(fpath, convert_categoricals=False)

            for col in df.columns:
                lbl = var_labels.get(col, "")
                if col.endswith("_Portu_clean") or col.endswith("_eng_clean"):
                    continue

                is_oth = ("oth" in col.lower() or "specify" in col.lower() or 
                          "other" in lbl.lower() or "specify" in lbl.lower())
                
                if not is_oth:
                    continue

                s = df[col].dropna()
                s_str = s[s.apply(lambda x: isinstance(x, str) and x.strip() not in ["", ".", "nan"])]
                if len(s_str) == 0:
                    continue

                # Resolve Parent Variable
                parent_var = re.sub(r'[_]?(?:oth(?:er)?|specify|spec)$', '', col, flags=re.IGNORECASE)
                if parent_var == col:
                    # Fallback check
                    parent_var = re.sub(r'oth$', '', col, flags=re.IGNORECASE)

                parent_lbl = global_var_labels.get(parent_var, var_labels.get(parent_var, ""))

                # Retrieve Options for Parent Variable
                options_dict: Dict[Any, str] = {}
                if parent_var in global_val_labels:
                    options_dict = global_val_labels[parent_var]
                elif parent_var.upper() in global_val_labels:
                    options_dict = global_val_labels[parent_var.upper()]
                elif parent_var in global_dummies:
                    options_dict = global_dummies[parent_var]
                elif parent_var.upper() in global_dummies:
                    options_dict = global_dummies[parent_var.upper()]

                # Build Inline Options Summary String
                if options_dict:
                    opts_str_list = [f"{k}: {v}" for k, v in options_dict.items()]
                    options_summary = " | ".join(opts_str_list)
                    # Catalog to Value_Codebook tab
                    for code_val, label_val in options_dict.items():
                        cb_key = (parent_var, str(code_val))
                        if cb_key not in seen_codebook_keys:
                            seen_codebook_keys.add(cb_key)
                            codebook_records.append({
                                "file_name": fname,
                                "parent_variable": parent_var,
                                "parent_variable_label": parent_lbl,
                                "option_code": str(code_val),
                                "option_label": str(label_val),
                            })
                else:
                    options_summary = "(No predefined options cataloged)"

                # Look for corresponding translation columns in dataset
                eng_col = f"{col}_eng_clean" if f"{col}_eng_clean" in df.columns else None
                port_col = f"{col}_Portu_clean" if f"{col}_Portu_clean" in df.columns else None

                val_counts = s_str.value_counts()
                for val, count in val_counts.items():
                    raw_text = str(val).strip()
                    eng_text = ""
                    if eng_col:
                        m = df[df[col] == val][eng_col].dropna()
                        if len(m) > 0:
                            eng_text = str(m.iloc[0]).strip()
                    elif port_col:
                        m = df[df[col] == val][port_col].dropna()
                        if len(m) > 0:
                            eng_text = str(m.iloc[0]).strip()

                    # Suggest default mappings based on common MTF patterns
                    suggested_code = ""
                    suggested_label = ""
                    notes = ""

                    raw_l = raw_text.lower()
                    if "sec_g_q05" in col.lower():
                        if any(k in raw_l for k in ["fogareiro", "fugão", "carvão", "ferro"]):
                            suggested_code = "2"
                            suggested_label = "Traditional / Local Stove (Charcoal brazier)"
                            notes = "Artisanal charcoal brazier / iron stand"
                    elif "sec_c_q125" in col.lower():
                        if "rádio" in raw_l or "radio" in raw_l:
                            suggested_code = "4"
                            suggested_label = "Radio"
                    elif "sec_c_q127" in col.lower():
                        if any(k in raw_l for k in ["lanterna", "lâmpada", "lampada"]):
                            suggested_code = "1"
                            suggested_label = "Lighting"
                        elif any(k in raw_l for k in ["telemóvel", "telemovel", "telefone"]):
                            suggested_code = "2"
                            suggested_label = "Phone charging"
                        elif any(k in raw_l for k in ["rádio", "radio"]):
                            suggested_code = "4"
                            suggested_label = "Radio"

                    recode_key = (col, raw_l)
                    approved_code = existing_approved.get(recode_key, suggested_code)

                    records.append({
                        "file_name": fname,
                        "variable_name": col,
                        "variable_label": lbl,
                        "parent_variable": parent_var,
                        "parent_variable_label": parent_lbl,
                        "existing_options_summary": options_summary,
                        "raw_text_response": raw_text,
                        "english_translation": eng_text,
                        "frequency_count": count,
                        "suggested_target_code": suggested_code,
                        "suggested_target_label": suggested_label,
                        "coordinator_approved_code": approved_code,
                        "notes": notes,
                        "_options_dict": options_dict  # internal helper for DataValidation
                    })
        except Exception as e:
            print(f"[WARN] Failed processing {fname}: {e}", file=sys.stderr)

    out_df = pd.DataFrame(records)
    if out_df.empty:
        print("[WARN] No Other, specify text records found.")
        return

    # Sort by file_name, variable_name, and frequency descending
    out_df.sort_values(by=["file_name", "variable_name", "frequency_count"], ascending=[True, True, False], inplace=True)

    # -------------------------------------------------------------------------
    # 3. BUILD OPENPYXL WORKBOOK WITH 4 TABS
    # -------------------------------------------------------------------------
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.Workbook()

    # =========================================================================
    # TAB 1: Instructions_&_Metadata
    # =========================================================================
    ws_meta = wb.active
    ws_meta.title = "Instructions_&_Metadata"
    ws_meta.views.sheetView[0].showGridLines = True

    # Title Banner
    ws_meta.merge_cells("A1:G1")
    title_cell = ws_meta["A1"]
    title_cell.value = "World Bank ESMAP Multi-Tier Framework (MTF) — Unified Country Calibration Workbook"
    title_cell.fill = NAVY_HEADER
    title_cell.font = FONT_TITLE
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws_meta.row_dimensions[1].height = 36

    # Section 1: Survey Metadata
    ws_meta["A3"] = "1. Survey Administrative Metadata"
    ws_meta["A3"].font = FONT_SECTION

    metadata_rows = [
        ("Country Name", existing_meta.get("Country Name", country)),
        ("Country ISO3 Code", existing_meta.get("Country ISO3 Code", country_iso3)),
        ("Survey Wave / Year", existing_meta.get("Survey Wave / Year", "2024")),
        ("National Currency Name & Code", existing_meta.get("National Currency Name & Code", "West African CFA Franc (XOF)" if country_iso3 == "GNB" else "Local Currency")),
        ("Exchange Rate to USD (LCU/USD)", existing_meta.get("Exchange Rate to USD (LCU/USD)", 600.0 if country_iso3 == "GNB" else 1.0)),
        ("Calibration Status", existing_meta.get("Calibration Status", "Approved" if existing_approved else "In Review")),
        ("Lead Reviewer / Coordinator", existing_meta.get("Lead Reviewer / Coordinator", "World Bank ESMAP MTF Team")),
        ("Last Updated Timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    ]

    for idx, (label, val) in enumerate(metadata_rows, start=4):
        ws_meta[f"A{idx}"] = label
        ws_meta[f"A{idx}"].font = FONT_BOLD
        ws_meta[f"A{idx}"].fill = GRAY_BG
        ws_meta[f"A{idx}"].border = THIN_BORDER

        ws_meta[f"B{idx}"] = val
        ws_meta[f"B{idx}"].font = FONT_BODY
        ws_meta[f"B{idx}"].border = THIN_BORDER
        if label == "Calibration Status":
            ws_meta[f"B{idx}"].fill = LIGHT_BLUE_FILL
            ws_meta[f"B{idx}"].alignment = Alignment(horizontal="center", vertical="center")

    # Section 2: Instructions
    ws_meta["A13"] = "2. Workbook Structure & Country Team Instructions"
    ws_meta["A13"].font = FONT_SECTION

    inst_texts = [
        ("Cookstove_Typology", "Reviewed by Clean Cooking Specialist: Defines ISO 19867 emission tiers (0–5), thermal efficiency, and stove groups for every stove model code in Section G (SEC_G_Q05)."),
        ("Other_Specify_Recodes", "Reviewed by Survey Statistician / Country Economist: Catalog of open-text CAPI responses for Section G (stoves), Section I (fuel collection frequency), and Section C (appliances). Select approved numeric codes from dropdowns or set [Missing (.)] to exclude."),
        ("Value_Codebook", "Reference Dictionary: Automated catalog of all parent variables, value labels, and option codes extracted directly from survey microdata."),
        ("Pipeline Integration", "This single Excel workbook is auto-detected by interactive_suite/mtf_builder.py, interactive_suite/mtf_engine.py, and dev_tools/mtf_calibrator.py, eliminating separate CSV/XLSX maintenance."),
    ]

    for idx, (title, desc) in enumerate(inst_texts, start=15):
        ws_meta[f"A{idx}"] = title
        ws_meta[f"A{idx}"].font = FONT_BOLD
        ws_meta[f"A{idx}"].fill = GRAY_BG
        ws_meta[f"A{idx}"].border = THIN_BORDER

        ws_meta.merge_cells(f"B{idx}:G{idx}")
        cell = ws_meta[f"B{idx}"]
        cell.value = desc
        cell.font = FONT_BODY
        cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        for col_char in ["B", "C", "D", "E", "F", "G"]:
            ws_meta[f"{col_char}{idx}"].border = THIN_BORDER
        ws_meta.row_dimensions[idx].height = 24

    ws_meta.column_dimensions["A"].width = 30
    ws_meta.column_dimensions["B"].width = 45
    ws_meta.column_dimensions["C"].width = 20
    ws_meta.column_dimensions["D"].width = 20
    ws_meta.column_dimensions["E"].width = 20
    ws_meta.column_dimensions["F"].width = 20
    ws_meta.column_dimensions["G"].width = 20

    # =========================================================================
    # TAB 2: Cookstove_Typology
    # =========================================================================
    ws_cs = wb.create_sheet(title="Cookstove_Typology")
    ws_cs.views.sheetView[0].showGridLines = True

    cs_headers = [
        "questionnaire_code", "stove_description", "iso_emission_tier",
        "efficiency_tier", "stove_group", "primary_fuel", "notes",
        "stat_key_nat", "stat_key_urb", "stat_key_rur"
    ]
    ws_cs.append(cs_headers)
    for col_idx, col_name in enumerate(cs_headers, start=1):
        cell = ws_cs.cell(row=1, column=col_idx)
        cell.fill = NAVY_HEADER
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws_cs.row_dimensions[1].height = 26

    # Determine stove rows to populate
    if existing_cookstoves:
        cs_rows = existing_cookstoves
    elif cookstove_config and Path(cookstove_config).exists():
        import csv
        with open(cookstove_config, encoding="utf-8") as f:
            lines = [l for l in f if not l.lstrip().startswith("#")]
        reader = csv.DictReader(lines)
        cs_rows = [r for r in reader if r.get("questionnaire_code", "").strip()]
    elif country_iso3 == "GNB" or "guinea" in country.lower():
        cs_rows = GNB_COOKSTOVE_ROWS
    else:
        cs_rows = DEFAULT_COOKSTOVE_ROWS

    # Data validation for ISO tiers and stove groups
    dv_iso = DataValidation(type="list", formula1='"0, 1, 2, 3, 4, 5"', allow_blank=True)
    dv_group = DataValidation(
        type="list",
        formula1='"open_fire, traditional, ics, clean_gas, clean_electric, clean_solar, clean_bio, transitional_bio, other"',
        allow_blank=True
    )
    ws_cs.add_data_validation(dv_iso)
    ws_cs.add_data_validation(dv_group)

    for row_idx, r in enumerate(cs_rows, start=2):
        row_vals = [r.get(c, "") for c in cs_headers]
        ws_cs.append(row_vals)
        for col_idx in range(1, len(cs_headers) + 1):
            c = ws_cs.cell(row=row_idx, column=col_idx)
            c.font = FONT_BODY
            c.border = THIN_BORDER
            col_name = cs_headers[col_idx - 1]
            if col_name in ["questionnaire_code", "iso_emission_tier", "efficiency_tier", "stove_group"]:
                c.alignment = Alignment(horizontal="center", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center")

            # Highlight ISO tiers and stove group as editable fields
            if col_name in ["iso_emission_tier", "efficiency_tier"]:
                c.fill = YELLOW_FILL
                dv_iso.add(c.coordinate)
            elif col_name == "stove_group":
                c.fill = LIGHT_BLUE_FILL
                dv_group.add(c.coordinate)

    cs_widths = {
        "questionnaire_code": 18, "stove_description": 32, "iso_emission_tier": 16,
        "efficiency_tier": 16, "stove_group": 18, "primary_fuel": 26, "notes": 40,
        "stat_key_nat": 16, "stat_key_urb": 16, "stat_key_rur": 16
    }
    for col_idx, col_name in enumerate(cs_headers, start=1):
        col_letter = get_column_letter(col_idx)
        ws_cs.column_dimensions[col_letter].width = cs_widths.get(col_name, 18)
    ws_cs.freeze_panes = "A2"

    # =========================================================================
    # TAB 3: Other_Specify_Recodes
    # =========================================================================
    ws_oth = wb.create_sheet(title="Other_Specify_Recodes")
    ws_oth.views.sheetView[0].showGridLines = True

    display_cols = [
        "file_name", "variable_name", "variable_label", "parent_variable",
        "parent_variable_label", "existing_options_summary", "raw_text_response",
        "english_translation", "frequency_count", "suggested_target_code",
        "suggested_target_label", "coordinator_approved_code", "notes"
    ]
    ws_oth.append(display_cols)
    for col_idx, col_name in enumerate(display_cols, start=1):
        cell = ws_oth.cell(row=1, column=col_idx)
        cell.fill = NAVY_HEADER
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws_oth.row_dimensions[1].height = 26

    approved_col_letter = get_column_letter(display_cols.index("coordinator_approved_code") + 1)
    dv_cache: Dict[str, DataValidation] = {}

    for row_idx, row_data in enumerate(out_df.to_dict(orient="records"), start=2):
        row_vals = [row_data[c] for c in display_cols]
        ws_oth.append(row_vals)

        for col_idx in range(1, len(display_cols) + 1):
            c = ws_oth.cell(row=row_idx, column=col_idx)
            c.font = FONT_BODY
            c.border = THIN_BORDER
            col_name = display_cols[col_idx - 1]
            if col_name in ["frequency_count", "suggested_target_code", "coordinator_approved_code"]:
                c.alignment = Alignment(horizontal="center", vertical="center")
            elif col_name == "existing_options_summary":
                c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            else:
                c.alignment = Alignment(horizontal="left", vertical="center")

            if col_name == "coordinator_approved_code":
                c.fill = YELLOW_FILL

        # Data validation dropdown for coordinator_approved_code
        opts = row_data.get("_options_dict", {})
        if opts:
            valid_codes = [str(k) for k in opts.keys()]
            dropdown_items = valid_codes + ["[Missing (.)]", "[Keep Other]"]
            formula_str = f'"{", ".join(dropdown_items)}"'
        else:
            formula_str = '"[Missing (.)], [Keep Other]"'

        if len(formula_str) <= 255:
            if formula_str not in dv_cache:
                dv = DataValidation(type="list", formula1=formula_str, allow_blank=True)
                ws_oth.add_data_validation(dv)
                dv_cache[formula_str] = dv
            dv_cache[formula_str].add(f"{approved_col_letter}{row_idx}")

    oth_widths = {
        "file_name": 24, "variable_name": 18, "variable_label": 28,
        "parent_variable": 16, "parent_variable_label": 26, "existing_options_summary": 45,
        "raw_text_response": 26, "english_translation": 24, "frequency_count": 12,
        "suggested_target_code": 16, "suggested_target_label": 26,
        "coordinator_approved_code": 22, "notes": 28
    }
    for col_idx, col_name in enumerate(display_cols, start=1):
        col_letter = get_column_letter(col_idx)
        ws_oth.column_dimensions[col_letter].width = oth_widths.get(col_name, 18)
    ws_oth.freeze_panes = "G2"

    # =========================================================================
    # TAB 4: Value_Codebook
    # =========================================================================
    ws_cb = wb.create_sheet(title="Value_Codebook")
    ws_cb.views.sheetView[0].showGridLines = True

    cb_headers = ["file_name", "parent_variable", "parent_variable_label", "option_code", "option_label"]
    ws_cb.append(cb_headers)
    for col_idx, col_name in enumerate(cb_headers, start=1):
        cell = ws_cb.cell(row=1, column=col_idx)
        cell.fill = TEAL_HEADER
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws_cb.row_dimensions[1].height = 26

    cb_df = pd.DataFrame(codebook_records)
    if not cb_df.empty:
        cb_df.sort_values(by=["file_name", "parent_variable", "option_code"], inplace=True)
        for row_idx, row_data in enumerate(cb_df.to_dict(orient="records"), start=2):
            ws_cb.append([row_data[c] for c in cb_headers])
            for col_idx in range(1, len(cb_headers) + 1):
                c = ws_cb.cell(row=row_idx, column=col_idx)
                c.font = FONT_BODY
                c.border = THIN_BORDER
                if cb_headers[col_idx - 1] == "option_code":
                    c.alignment = Alignment(horizontal="center", vertical="center")
                else:
                    c.alignment = Alignment(horizontal="left", vertical="center")

    cb_widths = {"file_name": 26, "parent_variable": 18, "parent_variable_label": 32, "option_code": 14, "option_label": 36}
    for col_idx, col_name in enumerate(cb_headers, start=1):
        col_letter = get_column_letter(col_idx)
        ws_cb.column_dimensions[col_letter].width = cb_widths.get(col_name, 20)
    ws_cb.freeze_panes = "A2"

    wb.save(output_xlsx)
    print(f"✓ Generated unified calibration workbook with 4 tabs:")
    print(f"  1. Instructions_&_Metadata ({len(metadata_rows)} parameters)")
    print(f"  2. Cookstove_Typology ({len(cs_rows)} stove models)")
    print(f"  3. Other_Specify_Recodes ({len(out_df)} verbatim text entries)")
    print(f"  4. Value_Codebook ({len(cb_df)} codebook records)")
    print(f"  --> Saved to: {output_xlsx}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate unified country calibration workbook from survey microdata.")
    parser.add_argument("--data-dir", required=True, help="Path to directory containing .dta microdata.")
    parser.add_argument("--output", required=True, help="Path to output .xlsx calibration workbook.")
    parser.add_argument("--country", default="Guinea-Bissau", help="Target country name.")
    parser.add_argument("--country-iso3", default="GNB", help="Target country ISO3 code.")
    parser.add_argument("--cookstove-config", default=None, help="Optional legacy cookstove CSV to import initial rows.")
    parser.add_argument("--existing-calibration", default=None, help="Optional path to existing calibration file to import approvals.")
    args = parser.parse_args()
    extract_other_specify(args.data_dir, args.output, args.country, args.country_iso3, args.cookstove_config, args.existing_calibration)
