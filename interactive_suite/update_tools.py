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
                # Filter members: if curr_dir is interactive_suite, prioritize members from interactive_suite/
                members = zip_ref.namelist()
                interactive_members = [m for m in members if "interactive_suite/" in m and not m.endswith("/")]

                for member in members:
                    if member.endswith("/"):
                        continue
                    p = Path(member)
                    parts = p.parts[1:]  # strip root 'esmap-mtf-pipeline-main'
                    if not parts:
                        continue
                    
                    # Safety guard: never touch data or output folders
                    if any(part in ("Data", "Output", "wip", "clean") for part in parts):
                        continue
                    
                    # 1. Update interactive_suite files
                    if "interactive_suite/" in member and curr_dir.name == "interactive_suite":
                        target_file = curr_dir / p.name
                        zip_ref.extract(member, tmpdir)
                        shutil.copy2(Path(tmpdir) / member, target_file)
                        print(f"  ✓ Updated [interactive]: {p.name}")
                        extracted_count += 1
                    # 2. Update dev_tools files (mtf_calibrator.py, etc.)
                    elif "dev_tools/" in member:
                        target_dev = curr_dir.parent / "dev_tools" if curr_dir.name == "interactive_suite" else curr_dir / "dev_tools"
                        if target_dev.exists():
                            target_file = target_dev / p.name
                            zip_ref.extract(member, tmpdir)
                            shutil.copy2(Path(tmpdir) / member, target_file)
                            print(f"  ✓ Updated [dev_tools]: {p.name}")
                            extracted_count += 1
                    # 3. Update stata_pipeline / Do-file templates
                    elif "stata_pipeline/Do-file/" in member:
                        base_root = curr_dir.parent if curr_dir.name == "interactive_suite" else curr_dir
                        for candidate in [base_root / "stata_pipeline" / "Do-file", base_root / "Do-file"]:
                            if candidate.exists():
                                target_file = candidate / p.name
                                zip_ref.extract(member, tmpdir)
                                shutil.copy2(Path(tmpdir) / member, target_file)
                                print(f"  ✓ Updated [Do-file]: {p.name}")
                                extracted_count += 1

            print(f"\n✓ Update finished! {extracted_count} tools/scripts successfully refreshed.")
            print("  🔒 Confidential Data/ files and custom outputs were fully preserved.")
    except Exception as e:
        print(f"\n[ERROR] Update failed: {e}")
        print("Please check your internet connection or contact Bryan Koo (bkoo@worldbankgroup.org).")

    print("=" * 65)

if __name__ == "__main__":
    update()
