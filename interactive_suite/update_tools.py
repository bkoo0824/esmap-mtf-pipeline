#!/usr/bin/env python3
"""
update_tools.py — 1-Click Auto-Updater for ESMAP MTF Interactive Tools & Pipeline
Checks for git updates or downloads the latest scripts/notebooks from GitHub.
Strictly preserves local Data/, Output/, and user files without overwriting.
"""
import sys
import shutil
import subprocess
from pathlib import Path
import urllib.request
import zipfile
import tempfile

REPO_URL = "https://github.com/bkoo0824/esmap-mtf-pipeline"
ZIP_URL = "https://github.com/bkoo0824/esmap-mtf-pipeline/archive/refs/heads/main.zip"

def update():
    curr_dir = Path(__file__).resolve().parent
    print("=" * 65)
    print(" 🔄 World Bank ESMAP MTF Pipeline & Tools Auto-Updater")
    print("=" * 65)
    
    # Check if this is inside a git repository
    git_detected = False
    if shutil.which("git"):
        try:
            res = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=curr_dir, capture_output=True, text=True)
            if res.returncode == 0 and res.stdout.strip() == "true":
                git_detected = True
        except Exception:
            pass

    if git_detected:
        print("✓ Git repository detected. Fetching latest updates from GitHub...")
        try:
            res = subprocess.run(["git", "pull", "origin", "main"], cwd=curr_dir, check=True, capture_output=True, text=True)
            print(res.stdout)
            print("✓ Successfully updated via Git!")
            return
        except Exception as e:
            print(f"Notice: 'git pull' encountered an issue ({e}).")
            print("Falling back to direct GitHub release download...")
            
    # Fallback / Non-Git users: Direct GitHub zip download
    print(f"Downloading latest update package from GitHub...")
    print(f"URL: {ZIP_URL}")
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_zip = Path(tmpdir) / "latest.zip"
            urllib.request.urlretrieve(ZIP_URL, tmp_zip)
            print("✓ Download complete. Unpacking updates safely...")
            
            with zipfile.ZipFile(tmp_zip, 'r') as zip_ref:
                extracted_count = 0
                for member in zip_ref.namelist():
                    p = Path(member)
                    parts = p.parts[1:]  # strip root 'esmap-mtf-pipeline-main'
                    if not parts:
                        continue
                    
                    # Safety guard: never touch data or output folders
                    if any(part in ("Data", "Output", "wip", "clean") for part in parts):
                        continue
                    
                    fname = p.name
                    # If this is a tool/script file matching our current directory, or one of the core interactive tools
                    is_core_tool = fname in (
                        "visualize.py", "inject_report.py", "MTF_Report_Template.md",
                        "mtf_builder.py", "mtf_engine.py", "run_mtf_local.bat",
                        "report_error.py", "update_tools.py", "requirements.txt",
                        "MTF_Interactive_Analyzer.ipynb", "mtf_report_values_reference.json"
                    )
                    if fname and ((curr_dir / fname).exists() or is_core_tool):
                        target_file = curr_dir / fname
                        zip_ref.extract(member, tmpdir)
                        src_file = Path(tmpdir) / member
                        shutil.copy2(src_file, target_file)
                        print(f"  ✓ Updated: {fname}")
                        extracted_count += 1

            print(f"\n✓ Update finished! {extracted_count} tools/scripts successfully refreshed.")
            print("  🔒 Confidential Data/ files and custom outputs were fully preserved.")
    except Exception as e:
        print(f"\n[ERROR] Update failed: {e}")
        print("Please check your internet connection or contact Bryan Koo (bkoo@worldbankgroup.org).")

    print("=" * 65)

if __name__ == "__main__":
    update()
