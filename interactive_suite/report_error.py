#!/usr/bin/env python3
"""
report_error.py — ESMAP MTF 1-Click System Diagnostics & Error Reporter
=============================================================================
Author: Bryan Koo / Antigravity AI Executive Operating Agent
World Bank ESMAP | Energy Global Practice

Purpose:
  1. Automatically captures comprehensive system, Python environment, library,
     and survey dataset integrity diagnostics into 'mtf_error_report.txt'.
  2. Automatically launches the user's default email client (Outlook, Mail, etc.)
     with Bryan Koo (bkoo@worldbankgroup.org) pre-filled in the To field, an
     informative subject line, and an executive briefing body.
  3. Ensures non-technical team members can report any issue in exactly 1 click.
"""

import os
import sys
import platform
import datetime
import webbrowser
import urllib.parse
from pathlib import Path
from typing import Optional, List, Dict, Any


SUPPORT_EMAIL = "bkoo@worldbankgroup.org"
REPORT_FILENAME = "mtf_error_report.txt"


def collect_diagnostics(error_traceback: Optional[str] = None) -> str:
    """Collects system, library, file existence, and data column diagnostics."""
    lines: List[str] = []
    lines.append("=================================================================")
    lines.append("   World Bank ESMAP MTF Pipeline - Diagnostic & Error Report     ")
    lines.append("=================================================================")
    lines.append(f"Timestamp:       {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Operating System:{platform.platform()} ({platform.system()} {platform.machine()})")
    lines.append(f"Python Binary:   {sys.executable}")
    lines.append(f"Python Version:  {sys.version.split()[0]}")
    lines.append(f"Working Dir:     {Path.cwd()}")
    lines.append("")

    # 1. Core Libraries
    lines.append("--- [1] Environment Libraries ---")
    for pkg in ["pandas", "numpy", "matplotlib", "openpyxl", "jupyterlab"]:
        try:
            mod = __import__(pkg)
            ver = getattr(mod, "__version__", "installed")
            lines.append(f"  ✓ {pkg:<12}: {ver}")
        except ImportError:
            lines.append(f"  ✗ {pkg:<12}: NOT INSTALLED")
    lines.append("")

    # 2. Directory & Data Files Audit
    lines.append("--- [2] Local Data Directory Audit ---")
    data_dir = Path("Data")
    if data_dir.exists():
        files = list(data_dir.glob("*"))
        lines.append(f"  📁 Data/ folder exists: {len(files)} files found")
        master_files = [f for f in files if "master" in f.name.lower() and f.suffix == ".dta"]
        other_dtas = [f for f in files if f.suffix == ".dta" and f not in master_files]
        if master_files:
            for mf in master_files:
                sz = mf.stat().st_size / 1024 / 1024
                lines.append(f"    ⭐ [MASTER DATASET] {mf.name} ({sz:.2f} MB)")
        else:
            lines.append("    ⚠️ No file with 'master' in name found in Data/.")

        lines.append(f"    • Other .dta files in Data/: {len(other_dtas)} files")
    else:
        lines.append("  ❌ Data/ folder DOES NOT EXIST in current directory.")
    lines.append("")

    # 3. In-Depth Dataset Integrity Check
    lines.append("--- [3] Master Dataset Integrity Inspection ---")
    master_path = None
    candidate_dirs = [Path("Data"), Path("Data/wip_hh"), Path(".")]
    for sdir in candidate_dirs:
        if sdir.exists():
            for f in sdir.glob("*.dta"):
                if "master" in f.name.lower():
                    master_path = f
                    break
            if master_path:
                break

    if master_path:
        try:
            import pandas as pd
            lines.append(f"  Testing read on: {master_path.name}...")
            df = pd.read_stata(master_path, convert_categoricals=False)
            lines.append(f"  ✓ Successfully read: {len(df):,} households across {len(df.columns):,} variables.")

            # Check critical columns
            req_cols = {
                "hh_wt": "Survey Sample Weight",
                "loc_urban_rural": "Urban/Rural Locality",
                "elc_aggr_tier": "Electricity Aggregated Tier",
                "cs_aggr_tier": "Cooking Aggregated Tier",
                "elec_tech_type": "Primary Electricity Tech Type",
                "hh_head_gender": "Household Head Gender",
                "hh_exp_quintile": "Household Consumption Quintile"
            }
            lines.append("  Key Variable Presence:")
            for c, desc in req_cols.items():
                if c in df.columns:
                    valid_cnt = df[c].notna().sum()
                    lines.append(f"    ✓ {c:<18}: FOUND ({valid_cnt:,} non-missing) - {desc}")
                else:
                    lines.append(f"    ✗ {c:<18}: MISSING! - {desc}")

            # Weighted sum check
            if "hh_wt" in df.columns:
                tot_pop = df["hh_wt"].sum()
                lines.append(f"  Total Survey-Weighted Households: {tot_pop:,.0f}")
        except Exception as e_data:
            lines.append(f"  ❌ Failed to inspect dataset: {e_data}")
    else:
        lines.append("  ⚠️ No master .dta file available to inspect.")
    lines.append("")

    # 4. Error Traceback (if any)
    lines.append("--- [4] Error & Traceback Details ---")
    if error_traceback:
        lines.append(error_traceback.strip())
    else:
        lines.append("  (No active runtime crash. User manually generated system diagnostic log.)")
    lines.append("=================================================================")
    return "\n".join(lines)


def launch_email_client(report_path: Path, error_snippet: str = ""):
    """Launches default email composer pre-addressed to Bryan Koo."""
    subject = f"[ESMAP MTF Support] Diagnostic Report from {platform.node() or 'Team Member'}"
    body = (
        f"Dear Bryan,\n\n"
        f"I encountered an issue or generated a diagnostic report for the ESMAP MTF analytical pipeline.\n\n"
        f"--- Quick Error Snippet ---\n"
        f"{error_snippet[:300] if error_snippet else 'System diagnostic attached.'}\n"
        f"---------------------------\n\n"
        f"Please find my '{report_path.name}' attached to this email.\n\n"
        f"Environment Summary:\n"
        f"- OS: {platform.system()} ({platform.platform()})\n"
        f"- Python: {sys.version.split()[0]}\n\n"
        f"Best regards,\n"
    )

    mailto_url = f"mailto:{SUPPORT_EMAIL}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
    try:
        webbrowser.open(mailto_url)
        return True
    except Exception as e:
        print(f"  (Note: Could not automatically open email composer: {e})")
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description="1-Click ESMAP MTF Error Reporter.")
    parser.add_argument("--error", help="Optional error message string to record.")
    parser.add_argument("--auto", action="store_true", help="Non-interactive auto-mode.")
    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("    WORLD BANK ESMAP MTF 1-CLICK SYSTEM DIAGNOSTICS & SUPPORT")
    print("=" * 70)
    print("[*] Gathering system environment and survey data integrity...")

    report_text = collect_diagnostics(args.error)
    report_file = Path.cwd() / REPORT_FILENAME
    report_file.write_text(report_text, encoding="utf-8")

    print(f"✓ Diagnostic report successfully generated: {report_file.name}")
    print(f"  Location: {report_file.resolve()}")
    print("-" * 70)

    print("[*] Opening your email client to send report to Bryan Koo...")
    opened = launch_email_client(report_file, args.error or "")

    print("=" * 70)
    if opened:
        print("📧 이메일 작성 창(Outlook/기본 메일)이 자동으로 열렸습니다!")
        print(f"   1. 받는 사람: {SUPPORT_EMAIL}")
        print(f"   2. 생성된 '{report_file.name}' 파일을 메일에 첨부해 주세요.")
        print("   3. [전송]을 누르시면 Bryan Koo에게 즉시 전달됩니다.")
    else:
        print(f"📧 이메일 작성을 위해 '{report_file.name}' 파일을 첨부하여")
        print(f"   {SUPPORT_EMAIL} (Bryan Koo)에게 메일 또는 Teams로 전달해 주세요!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
