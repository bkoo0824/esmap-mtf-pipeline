#!/usr/bin/env python3
"""
sync_config.py — Synchronizes country_config.yaml to STATA globals (00_country_globals.do).
Ensures zero parameter divergence between Python and STATA pipelines.
"""
import sys
from pathlib import Path
import yaml

def sync_config(config_yaml_path=None, output_do_path=None):
    base_dir = Path(__file__).resolve().parent.parent
    if config_yaml_path is None:
        config_yaml_path = base_dir / "config" / "country_config.yaml"
    else:
        config_yaml_path = Path(config_yaml_path)

    if output_do_path is None:
        output_do_path = base_dir / "stata_pipeline" / "Do-file" / "00_country_globals.do"
    else:
        output_do_path = Path(output_do_path)

    if not config_yaml_path.exists():
        print(f"❌ Error: Config file not found: {config_yaml_path}")
        sys.exit(1)

    with open(config_yaml_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    lines = [
        "* ==============================================================================",
        "* Auto-generated from config/country_config.yaml by sync_config.py",
        "* DO NOT EDIT DIRECTLY. Edit config/country_config.yaml and re-run sync_config.py",
        "* ==============================================================================",
        "",
        f'global country          "{cfg.get("country", "")}"',
        f'global country_iso3     "{cfg.get("country_iso3", "")}"',
        f'global survey_year      {cfg.get("survey_year", 2024)}',
        f'global master_dta       "{cfg.get("master_dta", "")}"',
        f'global currency         "{cfg.get("currency", "")}"',
        f'global usd_rate         {cfg.get("usd_rate", 1.0)}',
        f'global lifeline_tariff  {cfg.get("lifeline_tariff", 0.0)}',
        f'global basic_kwh_bundle {cfg.get("basic_kwh_bundle", 365.0)}',
        ""
    ]

    # Raw modules
    raw_mods = cfg.get("raw_modules", {})
    lines.append("* Raw Module Filenames")
    for key, val in raw_mods.items():
        if key == "core_sections":
            continue
        primary_fn = val.get("primary", "") if isinstance(val, dict) else str(val)
        lines.append(f'global fn_{key:<13} "{primary_fn}"')

    output_do_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_do_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"✓ Successfully generated STATA globals: {output_do_path}")
    print(f"  Country: {cfg.get('country')} ({cfg.get('country_iso3')}) | Currency: {cfg.get('currency')} | USD: {cfg.get('usd_rate')}")

if __name__ == "__main__":
    sync_config()
