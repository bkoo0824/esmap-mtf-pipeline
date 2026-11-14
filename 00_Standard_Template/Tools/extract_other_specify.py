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
from pathlib import Path
from typing import Dict, Any, List

import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation


# Styling Palette (World Bank ESMAP Standards)
NAVY_HEADER = PatternFill(start_color="002244", end_color="002244", fill_type="solid")
TEAL_HEADER = PatternFill(start_color="008080", end_color="008080", fill_type="solid")
GRAY_BG = PatternFill(start_color="F2F4F7", end_color="F2F4F7", fill_type="solid")
YELLOW_FILL = PatternFill(start_color="FFF3CD", end_color="FFF3CD", fill_type="solid")

FONT_HEADER = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
FONT_BOLD = Font(name="Calibri", size=10, bold=True)
FONT_BODY = Font(name="Calibri", size=10)
FONT_NOTE = Font(name="Calibri", size=9, italic=True, color="555555")

THIN_BORDER = Border(
    left=Side(style="thin", color="D0D5DD"),
    right=Side(style="thin", color="D0D5DD"),
    top=Side(style="thin", color="D0D5DD"),
    bottom=Side(style="thin", color="D0D5DD"),
)


def extract_other_specify(data_dir: str, output_xlsx: str):
    data_path = Path(data_dir)
    dta_files = sorted(glob.glob(str(data_path / "*.dta")))
    if not dta_files:
        print(f"[ERROR] No .dta files found in {data_dir}", file=sys.stderr)
        return

    print(f"[*] Scanning {len(dta_files)} microdata files in {data_dir}...")

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
                        "coordinator_approved_code": suggested_code,
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
    # 3. BUILD OPENPYXL WORKBOOK WITH STYLING & DATA VALIDATION
    # -------------------------------------------------------------------------
    os.makedirs(os.path.dirname(os.path.abspath(output_xlsx)), exist_ok=True)
    wb = openpyxl.Workbook()
    
    # Sheet 1: Other_Specify_Recodes
    ws1 = wb.active
    ws1.title = "Other_Specify_Recodes"
    ws1.views.sheetView[0].showGridLines = True

    display_cols = [
        "file_name", "variable_name", "variable_label", "parent_variable",
        "parent_variable_label", "existing_options_summary", "raw_text_response",
        "english_translation", "frequency_count", "suggested_target_code",
        "suggested_target_label", "coordinator_approved_code", "notes"
    ]

    # Write Headers
    ws1.append(display_cols)
    for col_idx, col_name in enumerate(display_cols, start=1):
        cell = ws1.cell(row=1, column=col_idx)
        cell.fill = NAVY_HEADER
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    approved_col_letter = get_column_letter(display_cols.index("coordinator_approved_code") + 1)

    # Group DataValidations by formula to avoid Excel bloating
    dv_cache: Dict[str, DataValidation] = {}

    for row_idx, row_data in enumerate(out_df.to_dict(orient="records"), start=2):
        row_vals = [row_data[c] for c in display_cols]
        ws1.append(row_vals)

        # Style cells
        for col_idx in range(1, len(display_cols) + 1):
            c = ws1.cell(row=row_idx, column=col_idx)
            c.font = FONT_BODY
            c.border = THIN_BORDER
            col_name = display_cols[col_idx - 1]
            if col_name in ["frequency_count", "suggested_target_code", "coordinator_approved_code"]:
                c.alignment = Alignment(horizontal="center", vertical="center")
            elif col_name == "existing_options_summary":
                c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            else:
                c.alignment = Alignment(horizontal="left", vertical="center")

            # Highlight approved code column for coordinator attention
            if col_name == "coordinator_approved_code":
                c.fill = YELLOW_FILL

        # Add DataValidation Dropdown to coordinator_approved_code
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
                ws1.add_data_validation(dv)
                dv_cache[formula_str] = dv
            dv_cache[formula_str].add(f"{approved_col_letter}{row_idx}")

    # Set Column Widths for Sheet 1
    col_widths = {
        "file_name": 24, "variable_name": 18, "variable_label": 28,
        "parent_variable": 16, "parent_variable_label": 26, "existing_options_summary": 45,
        "raw_text_response": 26, "english_translation": 24, "frequency_count": 12,
        "suggested_target_code": 16, "suggested_target_label": 26,
        "coordinator_approved_code": 22, "notes": 28
    }
    for col_idx, col_name in enumerate(display_cols, start=1):
        col_letter = get_column_letter(col_idx)
        ws1.column_dimensions[col_letter].width = col_widths.get(col_name, 18)

    ws1.freeze_panes = "G2"  # Freeze panes at raw_text_response for convenient lateral scrolling

    # -------------------------------------------------------------------------
    # 4. SHEET 2: VALUE_CODEBOOK REFERENCE TAB
    # -------------------------------------------------------------------------
    ws2 = wb.create_sheet(title="Value_Codebook")
    ws2.views.sheetView[0].showGridLines = True

    cb_headers = ["file_name", "parent_variable", "parent_variable_label", "option_code", "option_label"]
    ws2.append(cb_headers)
    for col_idx, col_name in enumerate(cb_headers, start=1):
        cell = ws2.cell(row=1, column=col_idx)
        cell.fill = TEAL_HEADER
        cell.font = FONT_HEADER
        cell.alignment = Alignment(horizontal="center", vertical="center")

    cb_df = pd.DataFrame(codebook_records)
    if not cb_df.empty:
        cb_df.sort_values(by=["file_name", "parent_variable", "option_code"], inplace=True)
        for row_idx, row_data in enumerate(cb_df.to_dict(orient="records"), start=2):
            ws2.append([row_data[c] for c in cb_headers])
            for col_idx in range(1, len(cb_headers) + 1):
                c = ws2.cell(row=row_idx, column=col_idx)
                c.font = FONT_BODY
                c.border = THIN_BORDER
                if cb_headers[col_idx - 1] == "option_code":
                    c.alignment = Alignment(horizontal="center", vertical="center")
                else:
                    c.alignment = Alignment(horizontal="left", vertical="center")

    cb_widths = {"file_name": 26, "parent_variable": 18, "parent_variable_label": 32, "option_code": 14, "option_label": 36}
    for col_idx, col_name in enumerate(cb_headers, start=1):
        col_letter = get_column_letter(col_idx)
        ws2.column_dimensions[col_letter].width = cb_widths.get(col_name, 20)

    ws2.freeze_panes = "A2"

    wb.save(output_xlsx)
    print(f"✓ Generated upgraded calibration workbook with {len(out_df)} recode rows & {len(cb_df)} codebook entries:")
    print(f"  {output_xlsx}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract Other, specify variables into calibration Excel form.")
    parser.add_argument("--data-dir", required=True, help="Path to directory containing .dta microdata.")
    parser.add_argument("--output", required=True, help="Path to output .xlsx calibration form.")
    args = parser.parse_args()
    extract_other_specify(args.data_dir, args.output)
