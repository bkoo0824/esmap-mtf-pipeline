#!/usr/bin/env python3
"""
ESMAP MTF Pipeline — Git Synchronization & Privacy Guard Helper
===============================================================
Ensures zero data leakage, automates safe staging, and simplifies
collaboration between Task Team Leaders and Data Scientists.

Usage:
  python3 git_sync.py --status
  python3 git_sync.py --sync -m "Update cooking tiers for Nigeria"
  python3 git_sync.py --pull
  python3 git_sync.py --import-country Liberia_2024 --source "/path/to/Do-file"
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path

FORBIDDEN_EXTS = ('.dta', '.xlsx', '.xls', '.xlsm', '.sav', '.zsav', '.sas7bdat')
REPO_DIR = Path(__file__).resolve().parent


def run_cmd(cmd, cwd=REPO_DIR, capture=False):
    """Run a shell command safely."""
    if capture:
        res = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return res
    res = subprocess.run(cmd, cwd=cwd)
    return res


def scan_for_data_leaks():
    """Scan all files in repo directory for accidentally placed data files."""
    leaks = []
    for root, dirs, files in os.walk(REPO_DIR):
        # Skip .git directory
        if '.git' in root:
            continue
        for f in files:
            p = Path(root) / f
            if p.suffix.lower() in FORBIDDEN_EXTS:
                leaks.append(p.relative_to(REPO_DIR))
            elif p.stat().st_size > 5 * 1024 * 1024:
                leaks.append(f"{p.relative_to(REPO_DIR)} (>{p.stat().st_size // (1024*1024)}MB)")
    return leaks


def show_status():
    """Display repository status and security check."""
    print("\n==================================================================")
    print("   ESMAP MTF Pipeline — Repository Health & Safety Check          ")
    print("==================================================================")
    
    # 1. Data Privacy Check
    leaks = scan_for_data_leaks()
    if leaks:
        print(" [!] WARNING: DATA PRIVACY ALERT — Potential survey data files detected:")
        for l in leaks:
            print(f"     ❌ {l}")
        print(" Remove these files before committing!")
    else:
        print("  ✓ Data Privacy Check: Clean (Zero .dta / .xlsx files in repo)")

    # 2. Git Status
    print("\n [Git Status]:")
    run_cmd(['git', 'status', '-s'])
    print("==================================================================\n")


def safe_sync(message, push=True):
    """Stage safe files, commit, and push."""
    # 1. Pre-check for leaks
    leaks = scan_for_data_leaks()
    if leaks:
        print("\n[SECURITY ABORT] Cannot commit! Unsaved data files found in repo tree:", file=sys.stderr)
        for l in leaks:
            print(f"  ❌ {l}", file=sys.stderr)
        print("Please move these files to your local OneDrive data directory.", file=sys.stderr)
        sys.exit(1)

    # 2. Stage safe files only
    run_cmd(['git', 'add', '-A'])

    # 3. Check if anything is staged
    diff_res = run_cmd(['git', 'diff', '--cached', '--quiet'], capture=True)
    if diff_res.returncode == 0:
        print("[INFO] Working tree clean — nothing new to commit.")
        if push:
            check_and_push()
        return

    # 4. Commit
    print(f"\n[COMMITTING]: {message}")
    res = run_cmd(['git', 'commit', '-m', message])
    if res.returncode != 0:
        print("[ERROR] Git commit failed.", file=sys.stderr)
        sys.exit(1)

    # 5. Push if requested
    if push:
        check_and_push()


def check_and_push():
    """Push commits to GitHub if remote exists."""
    remotes = run_cmd(['git', 'remote'], capture=True).stdout.strip()
    if not remotes:
        print("\n[NOTE] No remote repository configured yet.")
        print("To connect your GitHub repository, run:")
        print("  git remote add origin git@github.com:<org-or-user>/esmap-mtf-pipeline.git")
        print("  git push -u origin main\n")
        return

    print("\n[PUSHING] Syncing with GitHub...")
    res = run_cmd(['git', 'push', 'origin', 'HEAD'])
    if res.returncode == 0:
        print("  ✓ Successfully pushed to GitHub.")
    else:
        print("[WARN] Git push returned non-zero code. Check your network or GitHub credentials.", file=sys.stderr)


def safe_pull():
    """Pull upstream changes cleanly."""
    remotes = run_cmd(['git', 'remote'], capture=True).stdout.strip()
    if not remotes:
        print("[ERROR] No remote configured to pull from.", file=sys.stderr)
        return
    print("\n[PULLING] Fetching latest updates from GitHub...")
    run_cmd(['git', 'pull', '--rebase', 'origin', 'HEAD'])


def import_country(country_tag, source_dir):
    """Import do-files and configs from a local country analysis directory."""
    src = Path(source_dir).resolve()
    if not src.exists():
        print(f"[ERROR] Source directory not found: {src}", file=sys.stderr)
        sys.exit(1)

    dest = REPO_DIR / "Countries" / country_tag
    dest.mkdir(parents=True, exist_ok=True)

    copied = 0
    for ext in ["*.do", "*.csv", "*.md"]:
        for f in src.glob(ext):
            shutil.copy2(f, dest / f.name)
            copied += 1

    print(f"\n  ✓ Successfully imported {copied} code files from {src.name} into Countries/{country_tag}/")
    print("Run `python3 git_sync.py --status` to review changes.")


def main():
    parser = argparse.ArgumentParser(description="ESMAP MTF Pipeline Git Sync & Privacy Guard Helper")
    parser.add_argument("--status", "-s", action="store_true", help="Check repo status and scan for data leaks")
    parser.add_argument("--sync", action="store_true", help="Stage safe code, commit, and push")
    parser.add_argument("--commit", "-c", action="store_true", help="Stage and commit without pushing")
    parser.add_argument("-m", "--message", type=str, default=None, help="Commit message")
    parser.add_argument("--push", action="store_true", help="Push commits to GitHub")
    parser.add_argument("--pull", action="store_true", help="Pull latest commits from GitHub")
    parser.add_argument("--import-country", type=str, default=None, help="Country folder name (e.g. Liberia_2024)")
    parser.add_argument("--source", type=str, default=None, help="Source directory with do-files to import")

    args = parser.parse_args()

    if args.import_country:
        if not args.source:
            print("[ERROR] --source directory path is required when importing a country.", file=sys.stderr)
            sys.exit(1)
        import_country(args.import_country, args.source)
        return

    if args.status:
        show_status()
        return

    if args.pull:
        safe_pull()
        return

    if args.commit or args.sync:
        msg = args.message
        if not msg:
            msg = input("Enter commit description: ").strip()
            if not msg:
                print("[INFO] Commit cancelled: Empty message.")
                sys.exit(0)
        safe_sync(msg, push=args.sync)
        return

    if args.push:
        check_and_push()
        return

    # Default if no arguments
    show_status()


if __name__ == "__main__":
    main()
