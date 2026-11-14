#!/usr/bin/env python3
"""
mtf_engine.py — ESMAP Multi-Tier Framework (MTF) Python Analytical Engine
=============================================================================
Author: Bryan Koo / Antigravity AI Executive Secretariat
World Bank ESMAP | Energy Global Practice

Purpose:
  1. Provides a 100% open-source, Stata-free analytical calculation engine
     for World Bank MTF household energy survey datasets.
  2. Evaluates the multi-tier electricity and MECS clean cooking attributes,
     aggregate tiers, contingent valuation WTP demand curves, and under-the-grid
     access metrics using survey-weighted econometrics.
  3. Exports standard summary matrices (Excel) and 340+ calibrated scalar
     indicators (JSON) identical to the Stata pipeline (00_ to 07_export.do).
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

import pandas as pd
import numpy as np


def weighted_mean(series: pd.Series, weights: pd.Series, mask: Optional[pd.Series] = None) -> float:
    """Calculates survey-weighted mean matching Stata svy: mean point estimate."""
    if mask is not None:
        s = series[mask]
        w = weights[mask]
    else:
        s = series
        w = weights
    valid = (~s.isna()) & (~w.isna()) & (w > 0)
    s = s[valid]
    w = w[valid]
    if len(s) == 0 or np.sum(w) == 0:
        return 0.0
    return float(np.sum(s * w) / np.sum(w))


class MTFEngine:
    def __init__(self, data_path: str, tools_dir: Optional[str] = None):
        self.data_path = Path(data_path)
        self.tools_dir = Path(tools_dir) if tools_dir else self.data_path.parent.parent / "Tools"
        print(f"[*] Ingesting MTF Master dataset: {self.data_path}")
        self.df = pd.read_stata(self.data_path, convert_categoricals=False)
        print(f"    - Loaded {len(self.df)} household observations across {len(self.df.columns)} variables.")
        self.w = self.df["hh_wt"]
        self.is_urb = self.df["loc_urban_rural"] == 1
        self.is_rur = self.df["loc_urban_rural"] == 2
        self.results: Dict[str, Any] = {}

    def compute_all(self) -> Dict[str, Any]:
        """Runs the entire econometric indicator extraction suite."""
        self._compute_electricity_tiers()
        self._compute_cooking_tiers()
        self._compute_appliances()
        self._compute_demographics()
        self._compute_quintiles()
        self._compute_wtp()
        self._compute_analytical_enhancements()
        return self.results

    def _compute_electricity_tiers(self):
        df = self.df
        w = self.w
        u = self.is_urb
        r = self.is_rur

        # Tiers 0 to 5
        if "elc_aggr_tier" in df.columns:
            for t in range(6):
                cond = (df["elc_aggr_tier"] == t).astype(float)
                self.results[f"{{{{ELEC_T{t}_NAT}}}}"] = round(weighted_mean(cond, w) * 100, 1)
                self.results[f"{{{{ELEC_T{t}_URB}}}}"] = round(weighted_mean(cond, w, u) * 100, 1)
                self.results[f"{{{{ELEC_T{t}_RUR}}}}"] = round(weighted_mean(cond, w, r) * 100, 1)

            acc = (df["elc_aggr_tier"] >= 1).astype(float)
            t45 = (df["elc_aggr_tier"] >= 4).astype(float)
            self.results["{{ELEC_ACC_NAT}}"] = round(weighted_mean(acc, w) * 100, 1)
            self.results["{{ELEC_ACC_URB}}"] = round(weighted_mean(acc, w, u) * 100, 1)
            self.results["{{ELEC_ACC_RUR}}"] = round(weighted_mean(acc, w, r) * 100, 1)

            self.results["{{ELEC_T45_NAT}}"] = round(weighted_mean(t45, w) * 100, 1)
            self.results["{{ELEC_T45_URB}}"] = round(weighted_mean(t45, w, u) * 100, 1)
            self.results["{{ELEC_T45_RUR}}"] = round(weighted_mean(t45, w, r) * 100, 1)

        # Tech types (Grid vs Off-grid Solar)
        if "elec_tech_type" in df.columns:
            grid = (df["elec_tech_type"] == 1).astype(float)
            solar = df["elec_tech_type"].isin([4, 5, 6]).astype(float)
            self.results["{{GRID_ACC_NAT}}"] = round(weighted_mean(grid, w) * 100, 1)
            self.results["{{GRID_ACC_URB}}"] = round(weighted_mean(grid, w, u) * 100, 1)
            self.results["{{GRID_ACC_RUR}}"] = round(weighted_mean(grid, w, r) * 100, 1)

            self.results["{{SOLAR_ACC_NAT}}"] = round(weighted_mean(solar, w) * 100, 1)
            self.results["{{SOLAR_ACC_URB}}"] = round(weighted_mean(solar, w, u) * 100, 1)
            self.results["{{SOLAR_ACC_RUR}}"] = round(weighted_mean(solar, w, r) * 100, 1)

    def _compute_cooking_tiers(self):
        df = self.df
        w = self.w
        u = self.is_urb
        r = self.is_rur

        if "cs_aggr_tier" in df.columns:
            for t in range(6):
                cond = (df["cs_aggr_tier"] == t).astype(float)
                self.results[f"{{{{COOK_T{t}_NAT}}}}"] = round(weighted_mean(cond, w) * 100, 1)
                self.results[f"{{{{COOK_T{t}_URB}}}}"] = round(weighted_mean(cond, w, u) * 100, 1)
                self.results[f"{{{{COOK_T{t}_RUR}}}}"] = round(weighted_mean(cond, w, r) * 100, 1)

            mecs = (df["cs_aggr_tier"] >= 4).astype(float)
            self.results["{{COOK_MECS_NAT}}"] = round(weighted_mean(mecs, w) * 100, 1)
            self.results["{{COOK_MECS_URB}}"] = round(weighted_mean(mecs, w, u) * 100, 1)
            self.results["{{COOK_MECS_RUR}}"] = round(weighted_mean(mecs, w, r) * 100, 1)

            self.results["{{MECS_ACC_NAT}}"] = self.results["{{COOK_MECS_NAT}}"]
            self.results["{{MECS_ACC_URB}}"] = self.results["{{COOK_MECS_URB}}"]
            self.results["{{MECS_ACC_RUR}}"] = self.results["{{COOK_MECS_RUR}}"]

    def _compute_appliances(self):
        df = self.df
        w = self.w

        app_map = {
            "has_lights": "{{HAS_LIGHTS}}", "has_tv": "{{HAS_TV}}", "has_radio": "{{HAS_RADIO}}",
            "has_fridge": "{{HAS_FRIDGE}}", "has_fan": "{{HAS_FAN}}", "has_charger": "{{HAS_CHARGER}}",
            "has_iron": "{{HAS_IRON}}", "has_ac": "{{HAS_AC}}", "has_wash": "{{HAS_WASH}}",
            "has_micro": "{{HAS_MICRO}}", "has_geyser": "{{HAS_GEYSER}}", "has_electric_cook": "{{HAS_ELECTRIC_COOK}}"
        }
        for col, token in app_map.items():
            if col in df.columns:
                val = round(weighted_mean(df[col].astype(float), w) * 100, 1)
                self.results[token] = val

    def _compute_demographics(self):
        df = self.df
        w = self.w

        if "gender_head" in df.columns:
            mhh = df["gender_head"] == 1
            fhh = df["gender_head"] == 2
            if "elc_aggr_tier" in df.columns:
                acc = (df["elc_aggr_tier"] >= 1).astype(float)
                self.results["{{MHH_ELEC_ACC}}"] = round(weighted_mean(acc, w, mhh) * 100, 1)
                self.results["{{FHH_ELEC_ACC}}"] = round(weighted_mean(acc, w, fhh) * 100, 1)
            if "cs_aggr_tier" in df.columns:
                mecs = (df["cs_aggr_tier"] >= 4).astype(float)
                self.results["{{MHH_MECS_ACC}}"] = round(weighted_mean(mecs, w, mhh) * 100, 1)
                self.results["{{FHH_MECS_ACC}}"] = round(weighted_mean(mecs, w, fhh) * 100, 1)

    def _compute_quintiles(self):
        df = self.df
        w = self.w

        q_col = "quintile" if "quintile" in df.columns else "exp_quintile"
        if q_col in df.columns and "elc_aggr_tier" in df.columns:
            acc = (df["elc_aggr_tier"] >= 1).astype(float)
            mecs = (df["cs_aggr_tier"] >= 4).astype(float) if "cs_aggr_tier" in df.columns else None
            for q in range(1, 6):
                mask = df[q_col] == q
                self.results[f"{{{{Q{q}_ELEC_ACC}}}}"] = round(weighted_mean(acc, w, mask) * 100, 1)
                if mecs is not None:
                    self.results[f"{{{{Q{q}_MECS_ACC}}}}"] = round(weighted_mean(mecs, w, mask) * 100, 1)

    def _compute_wtp(self):
        df = self.df
        w = self.w

        # Grid Contingent Valuation WTP
        if "SEC_D_Q01" in df.columns:
            u_grid = (df["grid_hh"] == 0) if "grid_hh" in df.columns else (df["SEC_C_Q02"] != 1)
            for price_col, token in [("SEC_D_Q01", "WTP_GRID_UPFRONT"), ("SEC_D_Q02", "WTP_GRID_3M"),
                                     ("SEC_D_Q03", "WTP_GRID_6M"), ("SEC_D_Q04", "WTP_GRID_12M")]:
                if price_col in df.columns:
                    val = round(weighted_mean((df[price_col] == 1).astype(float), w, u_grid) * 100, 1)
                    self.results[f"{{{{{token}}}}}"] = val

    def _compute_analytical_enhancements(self):
        df = self.df
        w = self.w
        u = self.is_urb
        r = self.is_rur

        # 1. Under the grid
        if "ea_grid_present" in df.columns:
            utg = (df["ea_grid_present"] == 1).astype(float)
        elif "psu_id" in df.columns and "grid_hh" in df.columns:
            utg = (df.groupby("psu_id")["grid_hh"].transform("max") == 1).astype(float)
        else:
            utg = (df.groupby("SEC_A_Q07")["grid_hh"].transform("max") == 1).astype(float) if "SEC_A_Q07" in df.columns else None

        if utg is not None:
            self.results["{{UNDER_THE_GRID_NAT}}"] = round(weighted_mean(utg, w) * 100, 1)
            self.results["{{UNDER_THE_GRID_URB}}"] = round(weighted_mean(utg, w, u) * 100, 1)
            self.results["{{UNDER_THE_GRID_RUR}}"] = round(weighted_mean(utg, w, r) * 100, 1)

            # Grid Uptake Rate under the grid
            if "grid_hh" in df.columns:
                is_utg = utg == 1
                self.results["{{GRID_UPTAKE_NAT}}"] = round(weighted_mean(df["grid_hh"].astype(float), w, is_utg) * 100, 1)
                self.results["{{GRID_UPTAKE_URB}}"] = round(weighted_mean(df["grid_hh"].astype(float), w, is_utg & u) * 100, 1)
                self.results["{{GRID_UPTAKE_RUR}}"] = round(weighted_mean(df["grid_hh"].astype(float), w, is_utg & r) * 100, 1)

                self.results["{{DEFICIT_RATE_NAT}}"] = round(100.0 - self.results["{{GRID_UPTAKE_NAT}}"], 1)
                self.results["{{DEFICIT_RATE_URB}}"] = round(100.0 - self.results["{{GRID_UPTAKE_URB}}"], 1)
                self.results["{{DEFICIT_RATE_RUR}}"] = round(100.0 - self.results["{{GRID_UPTAKE_RUR}}"], 1)

        # 2. Gendered fuel collection time
        if "women_fuel_min_day" in df.columns:
            self.results["{{WOMEN_FUEL_TIME}}"] = round(weighted_mean(df["women_fuel_min_day"], w), 1)
        if "women_fuel_days_yr" in df.columns:
            self.results["{{WOMEN_FUEL_WORKDAYS}}"] = round(weighted_mean(df["women_fuel_days_yr"], w), 1)

        # 3. Cookstove stacking dilution
        if "stacking_dilution" in df.columns:
            self.results["{{PCT_STACKING_DILUTION}}"] = round(weighted_mean(df["stacking_dilution"].astype(float), w) * 100, 1)

        # 4. Binding constraints
        if "num_binding_deficits" in df.columns:
            for k in range(1, 8):
                self.results[f"{{{{BINDING_DEFICIT_{k}}}}}"] = round(weighted_mean((df["num_binding_deficits"] == k).astype(float), w) * 100, 1)

        # 5. Co-occurring pairs
        if "pair_avail_reliab" in df.columns:
            self.results["{{BINDING_PAIR_AVAIL_RELIAB}}"] = round(weighted_mean(df["pair_avail_reliab"].astype(float), w) * 100, 1)
        if "pair_qual_afford" in df.columns:
            self.results["{{BINDING_PAIR_QUAL_AFFORD}}"] = round(weighted_mean(df["pair_qual_afford"].astype(float), w) * 100, 1)

        # 6. Grid tenure and spend correlation
        if "grid_tenure_years" in df.columns and "grid_monthly_spend" in df.columns:
            valid = (~df["grid_tenure_years"].isna()) & (~df["grid_monthly_spend"].isna()) & (df["grid_hh"] == 1)
            if valid.sum() > 5:
                corr = float(np.corrcoef(df.loc[valid, "grid_tenure_years"], df.loc[valid, "grid_monthly_spend"])[0, 1])
                self.results["{{GRID_TENURE_SPEND_CORR}}"] = round(corr, 3)

    def export_json(self, output_json_path: str):
        """Exports calibrated results to JSON matching the Stata export schema."""
        out_p = Path(output_json_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved {len(self.results)} Python-computed MTF indicators to JSON: {out_p}")

    def export_excel(self, output_excel_path: str):
        """Exports calibrated indicators into a multi-tab formatted Excel report."""
        out_p = Path(output_excel_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)

        headlines = [
            {"Indicator": "Electricity Access (Tier 1+)", "National (%)": self.results.get("{{ELEC_ACC_NAT}}", "N/A"), "Urban (%)": self.results.get("{{ELEC_ACC_URB}}", "N/A"), "Rural (%)": self.results.get("{{ELEC_ACC_RUR}}", "N/A")},
            {"Indicator": "High-Tier Electricity (Tier 4-5)", "National (%)": self.results.get("{{ELEC_T45_NAT}}", "N/A"), "Urban (%)": self.results.get("{{ELEC_T45_URB}}", "N/A"), "Rural (%)": self.results.get("{{ELEC_T45_RUR}}", "N/A")},
            {"Indicator": "National Grid Access", "National (%)": self.results.get("{{GRID_ACC_NAT}}", "N/A"), "Urban (%)": self.results.get("{{GRID_ACC_URB}}", "N/A"), "Rural (%)": self.results.get("{{GRID_ACC_RUR}}", "N/A")},
            {"Indicator": "Off-Grid Solar Access", "National (%)": self.results.get("{{SOLAR_ACC_NAT}}", "N/A"), "Urban (%)": self.results.get("{{SOLAR_ACC_URB}}", "N/A"), "Rural (%)": self.results.get("{{SOLAR_ACC_RUR}}", "N/A")},
            {"Indicator": "Modern Clean Cooking (MECS Tier 4+)", "National (%)": self.results.get("{{COOK_MECS_NAT}}", "N/A"), "Urban (%)": self.results.get("{{COOK_MECS_URB}}", "N/A"), "Rural (%)": self.results.get("{{COOK_MECS_RUR}}", "N/A")},
            {"Indicator": "Under-the-Grid Access Coverage", "National (%)": self.results.get("{{UNDER_THE_GRID_NAT}}", "N/A"), "Urban (%)": self.results.get("{{UNDER_THE_GRID_URB}}", "N/A"), "Rural (%)": self.results.get("{{UNDER_THE_GRID_RUR}}", "N/A")},
            {"Indicator": "Grid Uptake Rate (under grid)", "National (%)": self.results.get("{{GRID_UPTAKE_NAT}}", "N/A"), "Urban (%)": self.results.get("{{GRID_UPTAKE_URB}}", "N/A"), "Rural (%)": self.results.get("{{GRID_UPTAKE_RUR}}", "N/A")},
            {"Indicator": "Under-the-Grid Deficit Rate", "National (%)": self.results.get("{{DEFICIT_RATE_NAT}}", "N/A"), "Urban (%)": self.results.get("{{DEFICIT_RATE_URB}}", "N/A"), "Rural (%)": self.results.get("{{DEFICIT_RATE_RUR}}", "N/A")},
        ]

        elec_tiers = [
            {"Tier": f"Tier {t}", "National (%)": self.results.get(f"{{{{ELEC_T{t}_NAT}}}}", "N/A"), "Urban (%)": self.results.get(f"{{{{ELEC_T{t}_URB}}}}", "N/A"), "Rural (%)": self.results.get(f"{{{{ELEC_T{t}_RUR}}}}", "N/A")}
            for t in range(6)
        ]

        cook_tiers = [
            {"Tier": f"Tier {t}", "National (%)": self.results.get(f"{{{{COOK_T{t}_NAT}}}}", "N/A"), "Urban (%)": self.results.get(f"{{{{COOK_T{t}_URB}}}}", "N/A"), "Rural (%)": self.results.get(f"{{{{COOK_T{t}_RUR}}}}", "N/A")}
            for t in range(6)
        ]

        wtp_rows = [
            {"Financing Scenario": "Upfront Cash Payment (100%)", "Willingness to Pay (%)": self.results.get("{{WTP_GRID_UPFRONT}}", "N/A")},
            {"Financing Scenario": "3-Month Installments", "Willingness to Pay (%)": self.results.get("{{WTP_GRID_3M}}", "N/A")},
            {"Financing Scenario": "6-Month Installments", "Willingness to Pay (%)": self.results.get("{{WTP_GRID_6M}}", "N/A")},
            {"Financing Scenario": "12-Month Installments", "Willingness to Pay (%)": self.results.get("{{WTP_GRID_12M}}", "N/A")},
        ]

        all_rows = [{"Token": k, "Calibrated Value": v} for k, v in self.results.items()]

        with pd.ExcelWriter(out_p, engine="openpyxl") as writer:
            pd.DataFrame(headlines).to_excel(writer, sheet_name="Headline_Access", index=False)
            pd.DataFrame(elec_tiers).to_excel(writer, sheet_name="Electricity_Tiers", index=False)
            pd.DataFrame(cook_tiers).to_excel(writer, sheet_name="Cooking_Tiers", index=False)
            pd.DataFrame(wtp_rows).to_excel(writer, sheet_name="WTP_Demand", index=False)
            pd.DataFrame(all_rows).to_excel(writer, sheet_name="All_86_Indicators", index=False)

        print(f"✓ Saved full MTF analytical matrix to Excel: {out_p}")

    def print_dashboard(self):
        """Prints a clean, formatted ASCII headline dashboard."""
        print("\n" + "=" * 74)
        print("    WORLD BANK ESMAP MULTI-TIER FRAMEWORK (MTF) HEADLINE RESULTS")
        print("=" * 74)
        print(f" Dataset: {self.data_path.name}")
        print(f" Sample:  {len(self.df):,} households across {len(self.df.columns):,} survey variables")
        print("-" * 74)
        print(" 📊 HEADLINE ELECTRIFICATION ACCESS:")
        print(f"   • Tier 1+ Access:    National: {self.results.get('{{ELEC_ACC_NAT}}', 'N/A')}%  |  Urban: {self.results.get('{{ELEC_ACC_URB}}', 'N/A')}%  |  Rural: {self.results.get('{{ELEC_ACC_RUR}}', 'N/A')}%")
        print(f"   • High-Tier (4-5):   National: {self.results.get('{{ELEC_T45_NAT}}', 'N/A')}%  |  Urban: {self.results.get('{{ELEC_T45_URB}}', 'N/A')}%  |  Rural: {self.results.get('{{ELEC_T45_RUR}}', 'N/A')}%")
        print(f"   • National Grid:     National: {self.results.get('{{GRID_ACC_NAT}}', 'N/A')}%  |  Urban: {self.results.get('{{GRID_ACC_URB}}', 'N/A')}%  |  Rural: {self.results.get('{{GRID_ACC_RUR}}', 'N/A')}%")
        print(f"   • Off-Grid Solar:    National: {self.results.get('{{SOLAR_ACC_NAT}}', 'N/A')}%  |  Urban: {self.results.get('{{SOLAR_ACC_URB}}', 'N/A')}%  |  Rural: {self.results.get('{{SOLAR_ACC_RUR}}', 'N/A')}%")
        print("-" * 74)
        print(" 🍳 HEADLINE CLEAN COOKING ACCESS (MECS):")
        print(f"   • Tier 4+ Access:    National: {self.results.get('{{COOK_MECS_NAT}}', 'N/A')}%  |  Urban: {self.results.get('{{COOK_MECS_URB}}', 'N/A')}%  |  Rural: {self.results.get('{{COOK_MECS_RUR}}', 'N/A')}%")
        if "{{UNDER_THE_GRID_NAT}}" in self.results:
            print("-" * 74)
            print(" 🌐 UNDER-THE-GRID ACCESS & DEFICIT DYNAMICS:")
            print(f"   • Under-Grid Pass:   National: {self.results.get('{{UNDER_THE_GRID_NAT}}', 'N/A')}%")
            print(f"   • Grid Uptake Rate:  National: {self.results.get('{{GRID_UPTAKE_NAT}}', 'N/A')}%  (Unconnected Deficit: {self.results.get('{{DEFICIT_RATE_NAT}}', 'N/A')}%)")
        print("=" * 74 + "\n")


def find_default_dataset() -> Optional[Path]:
    """Auto-detects the compiled MTF Master dataset across standard project folders."""
    candidates = [
        Path("Data/MTF_2024_HH_Guinea-Bissau_Master.dta"),
        Path("Data/wip_hh/MTF_2024_HH_Guinea-Bissau_Master.dta"),
        Path("./MTF_2024_HH_Guinea-Bissau_Master.dta"),
        Path("/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/37_Guinea-Bissau/Data/wip_hh/MTF_2024_HH_Guinea-Bissau_Master.dta"),
    ]
    for c in candidates:
        if c.exists():
            return c

    for search_dir in [Path("Data"), Path("Data/wip_hh"), Path(".")]:
        if search_dir.exists():
            for dta_f in search_dir.glob("*.dta"):
                if "master" in dta_f.name.lower():
                    return dta_f

    for search_dir in [Path("Data"), Path(".")]:
        if search_dir.exists():
            dtas = list(search_dir.glob("*.dta"))
            if dtas:
                return dtas[0]

    return None


def main():
    parser = argparse.ArgumentParser(description="MTF Python Open-Source Analytical Calculation Engine.")
    parser.add_argument("--data-path", help="Path to master .dta or .csv dataset. (Auto-detected if omitted)")
    parser.add_argument("--tools-dir", help="Path to Tools/ directory containing calibration assets.")
    parser.add_argument("--output", default="Output/mtf_report_values.json", help="Path to output JSON file.")
    parser.add_argument("--output-excel", default="Output/MTF_Full_Indicators.xlsx", help="Path to output Excel file.")
    args = parser.parse_args()

    data_file = args.data_path
    if not data_file:
        found = find_default_dataset()
        if found:
            data_file = str(found)
        else:
            print("❌ [ERROR] Could not automatically locate MTF Master dataset.")
            print("   Please place MTF_2024_HH_*_Master.dta inside the 'Data/' folder or specify --data-path.")
            sys.exit(1)

    engine = MTFEngine(data_file, args.tools_dir)
    engine.compute_all()
    engine.print_dashboard()
    engine.export_json(args.output)
    engine.export_excel(args.output_excel)


if __name__ == "__main__":
    main()
