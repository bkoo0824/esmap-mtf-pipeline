#!/usr/bin/env python3
"""
mtf_builder.py — End-to-End Master Dataset Compilation Engine
=============================================================================
Author: Bryan Koo / Antigravity AI Executive Operating Agent
World Bank ESMAP | Energy Global Practice

Purpose:
  Ingests the 15 raw Survey Solutions CAPI modules (*.dta) and compiles the
  authoritative MTF Master Household Dataset (MTF_2024_HH_<Country>_Master.dta),
  replicating Stata's 00_build_master_dataset.do with exact zero-divergence parity.
"""

import sys
import os
import re
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List
import warnings
import numpy as np
import pandas as pd
warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
try:
    import yaml
except ImportError:
    yaml = None


class MTFMasterBuilder:
    """Compiles raw Survey Solutions modules into an authoritative MTF Master Dataset."""

    def __init__(self, raw_dir: Optional[Path] = None, config_path: Optional[Path] = None):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.raw_dir = Path(raw_dir) if raw_dir else self._find_raw_dir()
        self.config = self._load_config(config_path)
        self.excel_recodes: Dict[str, Dict[str, Any]] = {}
        self.cookstove_typology: Dict[int, Dict[str, Any]] = {}
        self._load_calibration_workbook()
        self.df_master: Optional[pd.DataFrame] = None

    def _find_raw_dir(self) -> Path:
        """Auto-discovers the directory containing raw survey files."""
        candidates = [
            Path("Data/raw"),
            Path("Data"),
            Path("Data/wip_hh"),
            Path.cwd() / "Data",
            Path.cwd(),
            Path(".."),
            Path("../Data"),
            self.base_dir / "Data",
            self.base_dir
        ]
        for c in candidates:
            if c.exists():
                if (c / "admin_info.dta").exists():
                    return c
                for f in c.glob("*.dta"):
                    fname = f.name.lower()
                    if ("household" in fname or "hh" in fname or "energy" in fname) and "master" not in fname:
                        return c
        return Path("..") if (Path("..") / "hhroster.dta").exists() else Path("Data")

    @staticmethod
    def _col(df: pd.DataFrame, col_name: str, default: Any = np.nan) -> pd.Series:
        """Safely retrieves a column as a pandas Series matching df index, avoiding scalar bool indexing errors."""
        if col_name in df.columns:
            return df[col_name]
        return pd.Series(default, index=df.index)

    def _load_config(self, config_path: Optional[Path]) -> Dict[str, Any]:
        """Loads country_config.yaml or dynamically inspects raw survey modules."""
        # Check if monolithic raw household dataset exists in raw_dir
        monolithic_hh = None
        if hasattr(self, "raw_dir") and self.raw_dir and self.raw_dir.exists():
            for f in self.raw_dir.glob("*.dta"):
                fname = f.name.lower()
                if ("household" in fname or "energy" in fname or "field" in fname or "hh" in fname) and "master" not in fname and "roster" not in fname and not fname.startswith("section_"):
                    monolithic_hh = f
                    break

        cfg: Dict[str, Any] = {}
        search_paths = [
            Path(config_path) if config_path else None,
            self.base_dir / "config" / "country_config.yaml",
            self.raw_dir / "country_config.yaml",
            Path.cwd() / "country_config.yaml",
            Path.cwd() / "config" / "country_config.yaml",
            Path("..") / "country_config.yaml"
        ]
        for p in search_paths:
            if p and p.exists() and yaml is not None:
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        cfg = yaml.safe_load(f) or {}
                    break
                except Exception:
                    pass

        # Check for Calibration Workbook Instructions_&_Metadata sheet or MTF_<Country>_Calibration.xlsx
        if not cfg.get("country"):
            calib_search = [self.raw_dir, self.base_dir, Path(".."), Path("."), self.base_dir / "config"]
            for s_dir in calib_search:
                if not (s_dir and s_dir.exists()):
                    continue
                for cal_f in list(s_dir.glob("MTF_*_Calibration.xlsx")) + list(s_dir.glob("mtf_calibration*.xlsx")):
                    # Check filename first
                    m = re.match(r"MTF_(.+)_Calibration\.xlsx", cal_f.name)
                    if m and m.group(1).lower() not in ["standard", "template"]:
                        cfg["country"] = m.group(1).replace("_", " ").title()
                        break
                    # Check Instructions_&_Metadata sheet
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
                                        cfg["country"] = v
                                    elif k == "country iso3 code" and v and not v.startswith("{{"):
                                        cfg["country_iso3"] = v
                            if cfg.get("country"):
                                break
                    except Exception:
                        pass
                if cfg.get("country"):
                    break

        # If monolithic household data is found, auto-detect country metadata
        if monolithic_hh:
            try:
                # Infer country from filename first, e.g. Gambia_MTF_Energy_HH_Field.dta
                m_file = re.match(r"^([A-Za-z]+)_MTF", monolithic_hh.name)
                if m_file and not cfg.get("country"):
                    cfg["country"] = m_file.group(1).title()

                with pd.read_stata(monolithic_hh, iterator=True) as reader:
                    sample = reader.read(1)
                detected_country = None
                if "country_name" in sample.columns:
                    detected_country = str(sample["country_name"].iloc[0]).strip().title()
                elif "country" in sample.columns:
                    detected_country = str(sample["country"].iloc[0]).strip().title()

                if detected_country:
                    cfg["country"] = detected_country
                
                if cfg.get("country"):
                    c_name = cfg["country"]
                    iso_map = {"Liberia": "LBR", "Guinea-Bissau": "GNB", "Namibia": "NAM", "Nigeria": "NGA", "Rwanda": "RWA", "Ethiopia": "ETH", "Kenya": "KEN", "Gambia": "GMB"}
                    cfg["country_iso3"] = iso_map.get(c_name, c_name[:3].upper())
                    cfg["master_dta"] = f"MTF_2024_HH_{c_name}_Master.dta"
            except Exception as e:
                pass

        if not cfg.get("country"):
            cfg["country"] = "Guinea-Bissau"
            cfg["country_iso3"] = "GNB"
            cfg["survey_year"] = 2024
            cfg["master_dta"] = "MTF_2024_HH_Guinea-Bissau_Master.dta"
            cfg["currency"] = "XOF"
            cfg["usd_rate"] = 605.0
            cfg["lifeline_tariff"] = 128.0
            cfg["basic_kwh_bundle"] = 365.0

        if "raw_modules" not in cfg:
            cfg["raw_modules"] = {
                "admin_info": {"primary": "admin_info.dta", "fallbacks": []},
                "hhroster": {"primary": "section_a1_hh_roster.dta", "fallbacks": ["hhroster.dta"]},
                "food": {"primary": "section_o_food_roster.dta", "fallbacks": ["food.dta"]},
                "nonfood_1mon": {"primary": "section_o_nonfood_1mon_roster.dta", "fallbacks": ["nonfood_1mon.dta"]},
                "nonfood_12mon": {"primary": "section_o_nonfood_12mon_roster.dta", "fallbacks": ["nonfood_12mon.dta"]},
                "generator": {"primary": "section_c_generator_roster.dta", "fallbacks": ["sec_c_generator.dta"]},
                "rechar_ba": {"primary": "section_c_rechargeablebattery_roster.dta", "fallbacks": ["sec_c_rechar_ba.dta"]},
                "fuel_consump": {"primary": "section_i_fuel_consumption_roster.dta", "fallbacks": ["fuel_consumption.dta"]},
                "fuel_h11": {"primary": "section_h_fuel_h11_roster.dta", "fallbacks": ["fuel_h11.dta"]},
                "solar_device": {"primary": "section_c_solardevice_roster.dta", "fallbacks": ["solar_c_device.dta"]},
                "cookstoves": {"primary": "section_g_cookstoves_roster.dta", "fallbacks": ["cookstoves.dta"]},
                "stove_fuel": {"primary": "section_g_stovefuel_roster.dta", "fallbacks": ["stove_fuel.dta"]},
                "time_coll": {"primary": "section_i_time_collecting_roster.dta", "fallbacks": ["time_collecting.dta"]},
                "time_use": {"primary": "section_i_time_use_roster.dta", "fallbacks": ["time_use.dta"]},
                "appliances": {"primary": "section_f_appliance_roster.dta", "fallbacks": ["appliances.dta", "appliance.dta"]}
            }
        return cfg

    def _resolve_file(self, mod_key: str) -> Optional[Path]:
        """Resolves the path to a raw module by checking primary, fallback names, and case-insensitivity."""
        raw_mods = self.config.get("raw_modules", {})
        mod_info = raw_mods.get(mod_key, {})
        names = []
        if isinstance(mod_info, dict):
            if "primary" in mod_info:
                names.append(mod_info["primary"])
            names.extend(mod_info.get("fallbacks", []))
        elif isinstance(mod_info, str):
            names.append(mod_info)

        # Standard Survey Solutions CAPI naming fallbacks
        capi_fallbacks = {
            "generator": ["SEC_C_GENERATOR.dta", "sec_c_generator.dta", "generator.dta"],
            "rechar_ba": ["SEC_C_RECHAR_BA.dta", "sec_c_rechar_ba.dta", "rechar_ba.dta"],
            "solar_device": ["Solar_C_Device.dta", "solar_c_device.dta", "solar_device.dta"],
            "fuel_h11": ["fuel_H11.dta", "fuel_h11.dta"],
            "cookstoves": ["cookstoves.dta"],
            "appliances": ["appliances.dta", "appliance.dta"],
            "hhroster": ["hhroster.dta", "section_a1_hh_roster.dta"],
            "food": ["food.dta"],
            "nonfood_1mon": ["nonfood_1mon.dta"],
            "nonfood_12mon": ["nonfood_12mon.dta"],
            "fuel_consump": ["fuel_consumption.dta"],
            "time_coll": ["time_collecting.dta", "time_coll.dta"],
            "time_use": ["time_use.dta"],
            "lighting_fuel": ["lighting_fuel.dta"],
            "solar_business": ["solar_business.dta"]
        }
        names.extend(capi_fallbacks.get(mod_key, []))

        # 1. Exact match attempt
        for n in names:
            p = self.raw_dir / n
            if p.exists():
                return p

        # 2. Case-insensitive matching attempt (crucial for Linux cross-platform Survey Solutions)
        try:
            actual_files = {f.name.lower(): f for f in self.raw_dir.glob("*.dta")}
            for n in names:
                n_low = n.lower()
                if n_low in actual_files:
                    return actual_files[n_low]
        except Exception:
            pass

        return None

    @staticmethod
    def _normalize_id(df: pd.DataFrame) -> pd.DataFrame:
        """Ensures interview__id is present by copying interview__key if necessary."""
        if "interview__id" not in df.columns and "interview__key" in df.columns:
            df = df.copy()
            df["interview__id"] = df["interview__key"]
        return df

    def _load_calibration_workbook(self) -> None:
        """Loads unified mtf_calibration_<country>.xlsx (or legacy standalone files) if present."""
        iso3 = str(self.config.get("country_iso3", "")).lower().strip()
        cname = str(self.config.get("country", "")).lower().replace(" ", "_").replace("-", "_").strip()

        candidates = [
            # 1. Target country-specific calibration workbook
            self.raw_dir / f"MTF_{cname.capitalize()}_Calibration.xlsx",
            self.base_dir / f"MTF_{cname.capitalize()}_Calibration.xlsx",
            Path(f"MTF_{cname.capitalize()}_Calibration.xlsx"),
            Path(f"../MTF_{cname.capitalize()}_Calibration.xlsx"),
            self.raw_dir / f"mtf_calibration_{iso3}.xlsx",
            self.raw_dir / f"mtf_calibration_{cname}.xlsx",
            self.base_dir / "config" / f"mtf_calibration_{iso3}.xlsx",
            self.base_dir / "config" / f"mtf_calibration_{cname}.xlsx",
            Path(f"mtf_calibration_{iso3}.xlsx"),
            Path(f"mtf_calibration_{cname}.xlsx"),
            # 2. Project standard calibration workbook
            self.base_dir / "config" / "mtf_calibration_standard.xlsx",
            self.raw_dir / "mtf_calibration_standard.xlsx",
            Path("mtf_calibration_standard.xlsx"),
            self.base_dir / "config" / "mtf_calibration.xlsx",
            self.raw_dir / "mtf_calibration.xlsx",
            Path("mtf_calibration.xlsx"),
            # 3. Example Reference fallback
            self.base_dir / "examples" / "guinea_bissau_reference" / "mtf_calibration_guinea_bissau.xlsx",
            # 4. Legacy Fallbacks
            self.base_dir / "config" / "other_specify_calibration.xlsx",
            self.base_dir / "Tools" / "other_specify_calibration.xlsx",
            self.raw_dir / "other_specify_calibration.xlsx",
            Path("other_specify_calibration.xlsx")
        ]

        for c in candidates:
            if not c.exists():
                continue
            try:
                xl = pd.ExcelFile(c)

                # A. Ingest Other_Specify_Recodes
                if "Other_Specify_Recodes" in xl.sheet_names:
                    df_cal = xl.parse("Other_Specify_Recodes")
                    code_col = "coordinator_approved_code" if "coordinator_approved_code" in df_cal.columns and df_cal["coordinator_approved_code"].notna().any() else "suggested_target_code"
                    if "variable_name" in df_cal.columns and "raw_text_response" in df_cal.columns and code_col in df_cal.columns:
                        valid_rows = df_cal[df_cal[code_col].notna()]
                        for _, row in valid_rows.iterrows():
                            var = str(row["variable_name"]).strip()
                            txt = str(row["raw_text_response"]).strip().lower()
                            code_raw = str(row[code_col]).strip()
                            if code_raw in [".", "Missing", "missing", "[Missing (.)]"]:
                                code_val = np.nan
                            else:
                                try:
                                    code_val = float(code_raw)
                                except ValueError:
                                    code_val = code_raw
                            if var not in self.excel_recodes:
                                self.excel_recodes[var] = {}
                            self.excel_recodes[var][txt] = code_val
                        print(f"[*] Dynamic Recodes Active: Ingested {len(valid_rows)} recodes from {c.name}")

                # B. Ingest Cookstove_Typology
                if "Cookstove_Typology" in xl.sheet_names:
                    df_cs = xl.parse("Cookstove_Typology")
                    if "questionnaire_code" in df_cs.columns:
                        for _, r in df_cs.iterrows():
                            q_code_raw = str(r["questionnaire_code"]).strip()
                            if not q_code_raw or q_code_raw == "nan":
                                continue
                            codes = [code_item.strip() for code_item in q_code_raw.split(",")]
                            try:
                                emit = float(r["iso_emission_tier"]) if pd.notna(r.get("iso_emission_tier")) and str(r.get("iso_emission_tier")).strip() != "" else np.nan
                            except ValueError:
                                emit = np.nan
                            try:
                                eff = float(r["efficiency_tier"]) if pd.notna(r.get("efficiency_tier")) and str(r.get("efficiency_tier")).strip() != "" else np.nan
                            except ValueError:
                                eff = np.nan
                            s_group = str(r.get("stove_group", "")).strip()
                            desc = str(r.get("stove_description", "")).strip()
                            for c_str in codes:
                                try:
                                    c_int = int(float(c_str))
                                    self.cookstove_typology[c_int] = {
                                        "iso_emission_tier": emit,
                                        "efficiency_tier": eff,
                                        "stove_group": s_group,
                                        "description": desc
                                    }
                                except ValueError:
                                    pass
                        print(f"[*] Dynamic Cookstove Typology Active: Ingested {len(self.cookstove_typology)} stove codes from {c.name}")

                # C. Ingest National_Tariff_Benchmark
                if "National_Tariff_Benchmark" in xl.sheet_names:
                    try:
                        df_tf = xl.parse("National_Tariff_Benchmark")
                        if "iso3" in df_tf.columns and "tariff_per_kwh_local" in df_tf.columns:
                            matched = df_tf[df_tf["iso3"].astype(str).str.upper().str.strip() == iso3.upper()]
                            if not matched.empty:
                                val = float(matched.iloc[0]["tariff_per_kwh_local"])
                                self.tariff_per_kwh = val
                                print(f"[*] Dynamic Tariff Benchmark Active: Loaded {val} local currency/kWh from {c.name} [Sheet: National_Tariff_Benchmark]")
                    except Exception as tf_err:
                        print(f"[!] Note: Could not parse National_Tariff_Benchmark from {c}: {tf_err}")

                if self.excel_recodes or self.cookstove_typology or hasattr(self, "tariff_per_kwh"):
                    return
            except Exception as e:
                print(f"[!] Note: Could not read calibration from {c}: {e}")

    def _load_excel_calibration(self) -> Dict[str, Dict[str, Any]]:
        """Legacy helper returning loaded string recodes."""
        return self.excel_recodes

    def _apply_excel_recodes(self, df: pd.DataFrame, parent_col: str, oth_col: str) -> pd.DataFrame:
        """Applies dynamic Excel recodes from other_specify_calibration.xlsx to parent_col."""
        if not hasattr(self, "excel_recodes") or not self.excel_recodes or oth_col not in df.columns:
            return df
        recodes = self.excel_recodes.get(oth_col, {})
        if not recodes:
            return df
        for txt, new_code in recodes.items():
            mask = df[oth_col].astype(str).str.lower().str.strip() == txt
            if mask.sum() > 0:
                df.loc[mask, parent_col] = new_code
        return df

    def build_all(self) -> pd.DataFrame:
        """Executes the complete raw ETL sequence matching Stata's 00_build_master_dataset.do."""
        print("=" * 70)
        print("   World Bank ESMAP MTF End-to-End Master Dataset Compilation Engine")
        print("=" * 70)
        print(f"[*] Raw Survey Data Directory: {self.raw_dir.resolve()}")
        print(f"[*] Target Country: {self.config.get('country')} ({self.config.get('country_iso3')})")

        # 1. Demographics
        print("[1/9] Processing Household Demographics (hhsize, head age, gender, education)...")
        df_demo = self._process_demographics()

        # 2. Base Household & Core Sections
        print("[2/9] Merging Administrative Identifiers and Core Survey Modules...")
        df_base = self._process_core_sections(df_demo)

        # 3. Consumption & Expenditures
        print("[3/9] Annualizing Non-Energy & Energy Expenditures, Generating Quintiles...")
        df_exp = self._process_expenditures(df_base)

        # 4. Cookstoves & Emissions
        print("[4/9] Processing Cookstoves Roster, Stacking & ISO Emission Tiers...")
        df_cook = self._process_cookstoves(df_exp)

        # 5. Solar Devices & Technology Reclassification
        print("[5/9] Cleaning Solar Device Rosters and Reconciling Power Sources...")
        df_solar = self._process_solar(df_cook)

        # 6. Appliances & Gender Time-Use
        print("[6/9] Aggregating Appliance Load Tiers & Fuel Collection Time...")
        df_app = self._process_appliances_and_time(df_solar)

        # 7. Cooking Multi-Tier Framework Tiers
        print("[7/9] Computing 6 MECS Cooking Attributes & Multi-Tier Aggregates...")
        df_cook_tiers = self._process_cooking_tiers(df_app)

        # 8. Electricity Multi-Tier Framework Tiers
        print("[8/9] Computing 7 MTF Electricity Attributes & Multi-Tier Aggregates...")
        df_elec_tiers = self._process_electricity_tiers(df_cook_tiers)

        # 9. Under-the-Grid Analytics, Barriers & Willingness-to-Pay (WTP)
        print("[9/9] Generating Under-the-Grid Analytics, Barriers & WTP Curves...")
        self.df_master = self._process_policy_and_barriers(df_elec_tiers)

        print("-" * 70)
        print(f"✓ Master Dataset compilation complete: {len(self.df_master):,} households across {len(self.df_master.columns):,} variables.")
        print("=" * 70)
        return self.df_master

    def _process_demographics(self) -> pd.DataFrame:
        f_path = self._resolve_file("hhroster")
        if not f_path:
            raise FileNotFoundError("Raw household roster file (hhroster) not found.")
        
        df_raw = pd.read_stata(f_path, convert_categoricals=False)
        df_raw = self._normalize_id(df_raw)

        # Basic household size
        hhsize = df_raw.groupby("interview__id").size().rename("hhsize").reset_index()

        # Household Head characteristics
        head_col = "SEC_B_Q03" if "SEC_B_Q03" in df_raw.columns else ("SEC_A1_Q4" if "SEC_A1_Q4" in df_raw.columns else None)
        if head_col:
            head_mask = df_raw[head_col] == 1
            heads = df_raw[head_mask].copy()
        else:
            heads = df_raw.copy()

        heads = heads.drop_duplicates(subset=["interview__id"], keep="first")

        head_cols = {"interview__id": "interview__id"}
        if "SEC_B_Q01" in heads.columns:
            head_cols["SEC_B_Q01"] = "hh_head_gender"
        elif "SEC_A1_Q3" in heads.columns:
            head_cols["SEC_A1_Q3"] = "hh_head_gender"

        if "SEC_B_Q02" in heads.columns:
            head_cols["SEC_B_Q02"] = "hh_head_age"
        elif "SEC_A1_Q5" in heads.columns:
            head_cols["SEC_A1_Q5"] = "hh_head_age"

        if "SEC_B_Q04" in heads.columns:
            head_cols["SEC_B_Q04"] = "hh_head_marital"
        elif "SEC_A1_Q10" in heads.columns:
            head_cols["SEC_A1_Q10"] = "hh_head_marital"

        if "SEC_B_Q05" in heads.columns:
            head_cols["SEC_B_Q05"] = "hh_head_edu"
        elif "SEC_A1_Q8" in heads.columns:
            head_cols["SEC_A1_Q8"] = "hh_head_edu"

        heads_clean = heads[list(head_cols.keys())].rename(columns=head_cols)

        # Clean hh_head_age: replace with nan if > 110 or < 15
        if "hh_head_age" in heads_clean.columns:
            heads_clean.loc[(heads_clean["hh_head_age"] > 110) | (heads_clean["hh_head_age"] < 15), "hh_head_age"] = np.nan

        # Harmonized Education Level (SEC_A1_Q8 -> hh_head_educ)
        edu_raw = heads["SEC_A1_Q8"] if "SEC_A1_Q8" in heads.columns else (heads["SEC_B_Q05"] if "SEC_B_Q05" in heads.columns else None)
        if edu_raw is not None:
            q7 = heads.get("SEC_A1_Q7", pd.Series(np.nan, index=heads.index))
            edu_tier = pd.Series(np.nan, index=heads.index)
            if edu_raw.max() > 6:
                # Full Survey Solutions CAPI 35-grade education scale
                edu_tier.loc[edu_raw.isin([1, 2]) | (q7 == 2)] = 0.0
                edu_tier.loc[edu_raw.between(3, 9)] = 1.0
                edu_tier.loc[edu_raw.between(10, 16)] = 2.0
                edu_tier.loc[edu_raw.between(17, 35)] = 3.0
            else:
                edu_tier.loc[edu_raw.isin([1, 555]) | q7.isin([0, 2])] = 0.0
                edu_tier.loc[edu_raw == 2] = 1.0
                edu_tier.loc[edu_raw.isin([3, 4])] = 2.0
                edu_tier.loc[edu_raw.isin([5, 6])] = 3.0
            heads_clean["hh_head_educ"] = edu_tier
            heads_clean["head_educ_none"] = np.where(edu_tier.notna(), (edu_tier == 0).astype(float), np.nan)
            heads_clean["head_educ_prim"] = np.where(edu_tier.notna(), (edu_tier == 1).astype(float), np.nan)
            heads_clean["head_educ_sec"]  = np.where(edu_tier.notna(), (edu_tier == 2).astype(float), np.nan)
            heads_clean["head_educ_high"] = np.where(edu_tier.notna(), (edu_tier == 3).astype(float), np.nan)

        df_demo = hhsize.merge(heads_clean, on="interview__id", how="left")
        return df_demo

    def _process_core_sections(self, df_demo: pd.DataFrame) -> pd.DataFrame:
        # Check if monolithic raw household dataset exists
        monolithic_hh = None
        if hasattr(self, "raw_dir") and self.raw_dir and self.raw_dir.exists():
            for f in self.raw_dir.glob("*.dta"):
                fname = f.name.lower()
                if ("household" in fname or "energy" in fname or "field" in fname or "hh" in fname) and "master" not in fname and "roster" not in fname and not fname.startswith("section_"):
                    monolithic_hh = f
                    break

        if monolithic_hh:
            raw_hh = pd.read_stata(monolithic_hh, convert_categoricals=False)
            raw_hh = self._normalize_id(raw_hh)
            df = raw_hh.merge(df_demo, on="interview__id", how="left")

            # Map sampling weights
            if "HH_weights" in df.columns:
                df["hh_wt"] = df["HH_weights"].astype(np.float32)
            elif "hh_weight_final" in df.columns:
                df["hh_wt"] = df["hh_weight_final"].astype(np.float32)
            elif "weight" in df.columns:
                df["hh_wt"] = df["weight"].astype(np.float32)
            elif "hh_wt" not in df.columns:
                df["hh_wt"] = 1.0

            # Urban/Rural Locality: 1=Urban, 2=Rural
            if "loc_urban_rural" not in df.columns:
                if "SEC_A_Q06" in df.columns:
                    df["loc_urban_rural"] = df["SEC_A_Q06"].replace({99: 2})
                elif "SEC_A_Q05" in df.columns and set(df["SEC_A_Q05"].dropna().unique()).issubset({1, 2}):
                    df["loc_urban_rural"] = df["SEC_A_Q05"]
                elif "SEC_A_Q03" in df.columns:
                    df["loc_urban_rural"] = np.where(df["SEC_A_Q03"] == 1, 1, np.where(df["SEC_A_Q03"] == 99, 2, np.nan))
                else:
                    df["loc_urban_rural"] = 1

            # Strata: sorted unique (SEC_A_Q01, SEC_A_Q06) mapped to 1..N
            if "strata_id" not in df.columns:
                if "SEC_A_Q01" in df.columns and "SEC_A_Q06" in df.columns:
                    strata_df = df[["SEC_A_Q01", "SEC_A_Q06"]].drop_duplicates().sort_values(["SEC_A_Q01", "SEC_A_Q06"]).reset_index(drop=True)
                    strata_df["strata_id"] = range(1, len(strata_df) + 1)
                    df = df.merge(strata_df, on=["SEC_A_Q01", "SEC_A_Q06"], how="left")
                else:
                    df["strata_id"] = 1

            # PSU: sorted unique SEC_A_Q07 mapped to 1..N
            if "psu_id" not in df.columns:
                if "SEC_A_Q07" in df.columns:
                    unique_psus = sorted(df["SEC_A_Q07"].dropna().unique())
                    psu_df = pd.DataFrame({"SEC_A_Q07": unique_psus, "psu_id": range(1, len(unique_psus) + 1)})
                    df = df.merge(psu_df, on="SEC_A_Q07", how="left")
                else:
                    df["psu_id"] = 1

            # Population weight
            if "hhsize" in df.columns:
                df["pop_wt"] = (df["hh_wt"].astype(np.float32) * df["hhsize"].astype(np.float32))
            else:
                df["pop_wt"] = df["hh_wt"]
            return df

        df = df_demo.copy()

        # Administrative / Sampling information
        f_admin = self._resolve_file("admin_info")
        if f_admin:
            admin = pd.read_stata(f_admin, convert_categoricals=False)
            admin = self._normalize_id(admin)
            
            # Map weights
            if "hh_weight_final" in admin.columns:
                admin["hh_wt"] = admin["hh_weight_final"]
            elif "weight" in admin.columns:
                admin["hh_wt"] = admin["weight"]
            elif "hh_wt" not in admin.columns:
                admin["hh_wt"] = 1.0

            # PSU
            if "psu_id" not in admin.columns:
                if "SEC_A_Q07" in admin.columns:
                    admin["psu_id"] = admin["SEC_A_Q07"]
                elif "SEC_A_Q06" in admin.columns:
                    admin["psu_id"] = admin["SEC_A_Q06"]
                elif "ea_code" in admin.columns:
                    admin["psu_id"] = admin["ea_code"]
                else:
                    admin["psu_id"] = admin.get("SEC_A_Q05", pd.Series(range(1, len(admin) + 1), index=admin.index))

            # Urban/Rural Locality: 1=Urban, 2=Rural
            if "loc_urban_rural" not in admin.columns:
                if "SEC_A_Q05" in admin.columns and set(admin["SEC_A_Q05"].dropna().unique()).issubset({1, 2}):
                    admin["loc_urban_rural"] = admin["SEC_A_Q05"]
                elif "SEC_A_Q03" in admin.columns and set(admin["SEC_A_Q03"].dropna().unique()).issubset({1, 99}):
                    admin["loc_urban_rural"] = np.where(admin["SEC_A_Q03"] == 1, 1, np.where(admin["SEC_A_Q03"] == 99, 2, np.nan))
                elif "SEC_A_Q06" in admin.columns and set(admin["SEC_A_Q06"].dropna().unique()).issubset({1, 2}):
                    admin["loc_urban_rural"] = admin["SEC_A_Q06"]
                else:
                    admin["loc_urban_rural"] = admin.get("urban_rural", 1)

            # Strata
            if "strata_id" not in admin.columns:
                if "SEC_A_Q01" in admin.columns and "SEC_A_Q05" in admin.columns:
                    admin["strata_id"] = pd.factorize(admin["SEC_A_Q01"].astype(str) + "_" + admin["SEC_A_Q05"].astype(str))[0] + 1
                else:
                    admin["strata_id"] = 1

            df = df.merge(admin, on="interview__id", how="left", suffixes=("", "_admin"))

        # Merge core household single-record modules (Sections A to N)
        core_files = sorted(list(self.raw_dir.glob("section_*.dta")))
        for f in core_files:
            fname = f.name.lower()
            if "roster" in fname or "device" in fname:
                continue
            sec_df = pd.read_stata(f, convert_categoricals=False)
            sec_df = self._normalize_id(sec_df)
            if "interview__id" in sec_df.columns and sec_df["interview__id"].duplicated().any():
                continue
            cols_to_drop = [c for c in sec_df.columns if c in df.columns and c != "interview__id"]
            sec_df = sec_df.drop(columns=cols_to_drop)
            df = df.merge(sec_df, on="interview__id", how="left")

        df = df.copy()

        # Ensure population weight exists
        if "hh_wt" in df.columns and "hhsize" in df.columns:
            df["pop_wt"] = df["hh_wt"] * df["hhsize"]
        else:
            df["pop_wt"] = df.get("hh_wt", 1.0)

        return df

    def _process_expenditures(self, df_base: pd.DataFrame) -> pd.DataFrame:
        df = df_base.copy()

        # 1. Food (7-day recall)
        f_food = self._resolve_file("food")
        if f_food:
            food = pd.read_stata(f_food, convert_categoricals=False)
            food = self._normalize_id(food)
            q_cols = [c for c in food.columns if c.startswith("SEC_O_Q0")]
            if q_cols:
                for c in ["SEC_O_Q02", "SEC_O_Q03", "SEC_O_Q04"]:
                    if c in food.columns:
                        food[c] = food[c].replace({888: np.nan})
                food["fooditem_exp"] = food[q_cols].sum(axis=1)
                food["fooditem_exp_yr"] = (food["fooditem_exp"] / 7.0) * 365.0
                food_sum = food.groupby("interview__id")["fooditem_exp_yr"].sum().rename("food_exp_yr").reset_index()
                df = df.merge(food_sum, on="interview__id", how="left")

        # 2. Non-food 1-month
        f_nf1 = self._resolve_file("nonfood_1mon")
        if f_nf1:
            nf1 = pd.read_stata(f_nf1, convert_categoricals=False)
            nf1 = self._normalize_id(nf1)
            nf1_col = "SEC_O_Q1M_1" if "SEC_O_Q1M_1" in nf1.columns else ("SEC_O_Q08" if "SEC_O_Q08" in nf1.columns else None)
            if nf1_col:
                nf1[nf1_col] = nf1[nf1_col].replace({888: np.nan})
                nf1_sum = (nf1.groupby("interview__id")[nf1_col].sum() * 12.0).rename("nonfood_1mon_exp_yr").reset_index()
                df = df.merge(nf1_sum, on="interview__id", how="left")

        # 3. Non-food 12-month
        f_nf12 = self._resolve_file("nonfood_12mon")
        if f_nf12:
            nf12 = pd.read_stata(f_nf12, convert_categoricals=False)
            nf12 = self._normalize_id(nf12)
            nf12_col = "SEC_O_Q12M_1" if "SEC_O_Q12M_1" in nf12.columns else ("SEC_O_Q12" if "SEC_O_Q12" in nf12.columns else None)
            if nf12_col:
                nf12[nf12_col] = nf12[nf12_col].replace({888: np.nan})
                nf12_sum = nf12.groupby("interview__id")[nf12_col].sum().rename("nonfood_12mon_exp_yr").reset_index()
                df = df.merge(nf12_sum, on="interview__id", how="left")

        # 4. Electricity expenditure (Grid, Minigrid, Generator, Rech Battery)
        grid_m = df["SEC_C_Q25"].replace({888: np.nan, 9: np.nan, -888: np.nan, 999: np.nan, -999: np.nan}) if "SEC_C_Q25" in df.columns else pd.Series(np.nan, index=df.index)
        if "SEC_C_Q12" in df.columns:
            grid_m.loc[grid_m.isna() & (df["SEC_C_Q12"] == 111)] = 0.0
        grid_m = grid_m.fillna(0.0)

        minigrid_m = df["SEC_C_Q62"].replace({888: np.nan, 9: np.nan, -888: np.nan, 999: np.nan, -999: np.nan}) if "SEC_C_Q62" in df.columns else pd.Series(np.nan, index=df.index)
        if "SEC_C_Q48" in df.columns:
            minigrid_m.loc[minigrid_m.isna() & (df["SEC_C_Q48"] == 111)] = 0.0
        minigrid_m = minigrid_m.fillna(0.0)

        elec_base_yr = (grid_m + minigrid_m) * 12.0

        f_gen = self._resolve_file("generator")
        if f_gen:
            gen_df = pd.read_stata(f_gen, convert_categoricals=False)
            gen_df = self._normalize_id(gen_df)
            merged_gen = df[["interview__id"]].merge(gen_df, on="interview__id", how="left")
            q88 = merged_gen["SEC_C_Q88"].replace({888: np.nan}) if "SEC_C_Q88" in merged_gen.columns else pd.Series(np.nan, index=df.index)
            gen_exp_maint_yr = q88.fillna(0.0)

            nbr_cols = [f"SEC_C_Q84__{i}" for i in range(1, 13) if f"SEC_C_Q84__{i}" in merged_gen.columns]
            nbr_mth_gen = merged_gen[nbr_cols].fillna(0).sum(axis=1) if nbr_cols else pd.Series(12.0, index=df.index)
            if "SEC_C_Q84__111" in merged_gen.columns:
                nbr_mth_gen.loc[merged_gen["SEC_C_Q84__111"] == 1] = 12.0

            q91 = merged_gen["SEC_C_Q91"].replace({888: np.nan}) if "SEC_C_Q91" in merged_gen.columns else pd.Series(np.nan, index=df.index)
            gen_exp_yr = (q91 * nbr_mth_gen).fillna(0.0)
            df["gen_exp_tot_yr"] = gen_exp_maint_yr + gen_exp_yr
        else:
            df["gen_exp_tot_yr"] = 0.0

        f_rech = self._resolve_file("rechar_ba")
        if f_rech:
            rech_df = pd.read_stata(f_rech, convert_categoricals=False)
            rech_df = self._normalize_id(rech_df)
            nbr_r_cols = [c for c in rech_df.columns if c.startswith("SEC_C_Q103__") and not c.endswith("111")]
            nbr_rech = rech_df[nbr_r_cols].sum(axis=1) if nbr_r_cols else pd.Series(12.0, index=rech_df.index)
            if "SEC_C_Q103__111" in rech_df.columns:
                nbr_rech.loc[rech_df["SEC_C_Q103__111"] == 1] = 12.0
            rech_yr = rech_df.get("SEC_C_Q108", pd.Series(0.0, index=rech_df.index)).replace({888: np.nan}).fillna(0.0) * nbr_rech
            rech_agg = rech_yr.groupby(rech_df["interview__id"]).sum().rename("rech_bat_exp_yr").reset_index()
            df = df.merge(rech_agg, on="interview__id", how="left")
        else:
            df["rech_bat_exp_yr"] = 0.0

        df["gen_exp_tot_yr"] = df["gen_exp_tot_yr"].fillna(0.0)
        df["rech_bat_exp_yr"] = df["rech_bat_exp_yr"].fillna(0.0)
        df["elec_exp_yr"] = elec_base_yr + df["gen_exp_tot_yr"] + df["rech_bat_exp_yr"]

        # 5. Lighting & other fuels (Section H roster)
        f_h11 = self._resolve_file("fuel_h11")
        if f_h11:
            h11 = pd.read_stata(f_h11, convert_categoricals=False)
            h11 = self._normalize_id(h11)
            freq_l = h11["SEC_H_Q13"] if "SEC_H_Q14" in h11.columns else h11.get("SEC_H_Q12", 1)
            pay_l = h11["SEC_H_Q14"] if "SEC_H_Q14" in h11.columns else h11.get("SEC_H_Q13", 0.0)

            m_l = pd.Series(np.nan, index=h11.index)
            m_l.loc[freq_l == 1] = pay_l * 30.0
            m_l.loc[freq_l == 2] = (pay_l / 7.0) * 30.0
            m_l.loc[freq_l == 3] = (pay_l / 7.0) * 30.0 * 2.0
            m_l.loc[freq_l == 4] = (pay_l / 14.0) * 30.0
            m_l.loc[freq_l == 5] = (pay_l / 21.0) * 30.0
            m_l.loc[freq_l == 6] = pay_l
            m_l.loc[freq_l == 7] = pay_l / 2.0
            m_l.loc[freq_l == 8] = pay_l / 3.0
            m_l.loc[freq_l == 9] = pay_l / 4.0
            m_l.loc[freq_l == 10] = pay_l / 5.0
            m_l.loc[freq_l == 11] = pay_l / 6.0
            m_l.loc[freq_l == 12] = (pay_l / 7.0) * 30.0 * 3.0
            m_l.loc[freq_l == 13] = pay_l * 4.0
            m_l.loc[freq_l == 14] = (pay_l / 2.0) * 30.0
            m_l.loc[freq_l == 15] = pay_l / 12.0
            m_l.loc[freq_l == 16] = (pay_l / 3.0) * 30.0
            m_l.loc[freq_l == 17] = pay_l * 6.0
            m_l.loc[freq_l == 18] = pay_l / 6.0
            m_l.loc[freq_l == 19] = pay_l * 2.0

            yr_l = m_l.fillna(0.0) * 12.0
            h11_tot = yr_l.groupby(h11["interview__id"]).sum().rename("lightfuel_exp_tot_yr").reset_index()
            df = df.merge(h11_tot, on="interview__id", how="left")

        # 6. Cooking fuels (Section I fuel consumption)
        f_fc = self._resolve_file("fuel_consump")
        if f_fc:
            fc = pd.read_stata(f_fc, convert_categoricals=False)
            fc = self._normalize_id(fc)
            nbr_m = fc["SEC_I_Q04"].fillna(12.0) if "SEC_I_Q04" in fc.columns else 12.0
            freq_c = self._col(fc, "SEC_I_Q07", 4)
            pay_c = self._col(fc, "SEC_I_Q09", 0.0).replace({888: np.nan})

            fid = self._col(fc, "fuel_consumption__id", 0)
            pay_c.loc[fid.isin([3, 16])] = 0.0

            m_c = pd.Series(np.nan, index=fc.index)
            m_c.loc[freq_c == 1] = pay_c * 30.0
            m_c.loc[freq_c == 2] = (pay_c / 7.0) * 30.0
            m_c.loc[freq_c == 3] = (pay_c / 7.0) * 30.0 * 2.0
            m_c.loc[freq_c == 4] = (pay_c / 14.0) * 30.0
            m_c.loc[freq_c == 5] = (pay_c / 21.0) * 30.0
            m_c.loc[freq_c == 6] = pay_c
            m_c.loc[freq_c == 7] = pay_c / 2.0
            m_c.loc[freq_c == 8] = pay_c / 3.0
            m_c.loc[freq_c == 9] = pay_c / 4.0
            m_c.loc[freq_c == 10] = pay_c / 5.0
            m_c.loc[freq_c == 11] = pay_c / 6.0
            m_c.loc[freq_c == 12] = (pay_c / 7.0) * 30.0 * 3.0
            m_c.loc[freq_c == 13] = pay_c * 3.0
            m_c.loc[freq_c == 14] = (pay_c / 2.0) * 30.0
            m_c.loc[freq_c == 15] = pay_c / 12.0
            m_c.loc[freq_c == 16] = pay_c / 24.0
            m_c.loc[freq_c == 17] = (pay_c / 7.0) * 30.0 * 4.0
            m_c.loc[freq_c == 18] = pay_c * 5.0
            m_c.loc[freq_c == 19] = pay_c / 8.0
            m_c.loc[freq_c == 20] = pay_c / 6.0
            m_c.loc[freq_c == 21] = pay_c * 2.0
            m_c.loc[freq_c == 22] = 0.0

            yr_c = m_c.fillna(0.0) * nbr_m
            fc_tot = yr_c.groupby(fc["interview__id"]).sum().rename("fuel_exp_tot_yr").reset_index()
            df = df.merge(fc_tot, on="interview__id", how="left")

        # Fill missing expenditure components with 0
        exp_vars = ["food_exp_yr", "nonfood_1mon_exp_yr", "nonfood_12mon_exp_yr", "elec_exp_yr", "lightfuel_exp_tot_yr", "fuel_exp_tot_yr"]
        for v in exp_vars:
            if v in df.columns:
                df[v] = df[v].fillna(0.0)
            else:
                df[v] = 0.0

        # Total annualized expenditure
        df["exp_total_yr"] = df["food_exp_yr"] + df["nonfood_1mon_exp_yr"] + df["nonfood_12mon_exp_yr"] + df["elec_exp_yr"] + df["lightfuel_exp_tot_yr"] + df["fuel_exp_tot_yr"]
        df["exp_pc_yr"] = df["exp_total_yr"] / df["hhsize"].clip(lower=1)

        # Generate Population-Weighted Quintiles matching Stata xtile
        valid_pop = df["pop_wt"].notna()
        q_series = pd.Series(np.nan, index=df.index)
        q_series.loc[valid_pop] = self._compute_weighted_quintiles(df.loc[valid_pop, "exp_total_yr"], df.loc[valid_pop, "pop_wt"])
        df["hh_exp_quintile"] = q_series

        # Audit reference: Household-level total expenditure with household weights
        df["hh_exp_quintile_hhlevel"] = self._compute_weighted_quintiles(df["exp_total_yr"], df["hh_wt"])
        return df

    @staticmethod
    def _compute_weighted_quintiles(values: pd.Series, weights: pd.Series) -> pd.Series:
        """Assigns 1..5 quintiles based on population-weighted cumulative distribution matching Stata xtile."""
        df_temp = pd.DataFrame({"val": values, "wt": weights}).sort_values("val").reset_index()
        df_temp["cum_wt"] = df_temp["wt"].cumsum()
        tot_wt = df_temp["wt"].sum()
        cuts = [0.2 * tot_wt, 0.4 * tot_wt, 0.6 * tot_wt, 0.8 * tot_wt]
        idx_cuts = [np.searchsorted(df_temp["cum_wt"], c) for c in cuts]
        val_cuts = [df_temp.loc[i, "val"] for i in idx_cuts]
        df_temp["quintile"] = np.searchsorted(val_cuts, df_temp["val"], side="left") + 1
        return df_temp.set_index("index")["quintile"].reindex(values.index)

    def _process_cookstoves(self, df_base: pd.DataFrame) -> pd.DataFrame:
        df = df_base.copy()
        f_stoves = self._resolve_file("cookstoves")
        if not f_stoves:
            return df

        stoves = pd.read_stata(f_stoves, convert_categoricals=False)
        stoves = self._normalize_id(stoves)

        if "cookstoves__id" in stoves.columns:
            stoves = stoves[stoves["cookstoves__id"].notna()].copy()

        if "SEC_G_Q03" in stoves.columns:
            stoves = stoves[~stoves["SEC_G_Q03"].isin(["Does not cook", "microwave oven"])]

        if "SEC_G_Q05_oth" in stoves.columns:
            # Apply dynamic Excel recodes if available
            stoves = self._apply_excel_recodes(stoves, "SEC_G_Q05", "SEC_G_Q05_oth")
            stoves.loc[stoves["SEC_G_Q05_oth"].astype(str).str.lower().str.strip().isin([
                "fogareiro", "fugão a carvão", "fogareiro com carvão", "figareiro",
                "fogão de carvão", "fogadeiro", "construído com pesas de ferro para cozinhar", "fogadero"
            ]), "SEC_G_Q05"] = 2
            stoves.loc[stoves["SEC_G_Q05_oth"].isin(["Fire wood", "Wood", "open fire on the ground"]), "SEC_G_Q05"] = 1
            stoves.loc[stoves["SEC_G_Q05_oth"] == "four plate stove", "SEC_G_Q05"] = 19
            stoves.loc[stoves["SEC_G_Q05_oth"] == "Gas-Eletric stove", "SEC_G_Q05"] = 23
            stoves.loc[stoves["SEC_G_Q05_oth"] == "Traditional stove", "SEC_G_Q05"] = 22

        if "SEC_G_Q05" in stoves.columns:
            stoves.loc[stoves["SEC_G_Q05"].isin([555, 96]), "SEC_G_Q05"] = np.nan

        # Time-weighted emissions
        stype = stoves.get("SEC_G_Q05", pd.Series(np.nan, index=stoves.index))
        emit_tier = pd.Series(0.0, index=stoves.index)
        if hasattr(self, "cookstove_typology") and self.cookstove_typology:
            for c_int, info in self.cookstove_typology.items():
                t = info.get("iso_emission_tier")
                if pd.notna(t):
                    emit_tier.loc[stype == c_int] = float(t)
        elif self.config.get("country_iso3") == "GNB" or self.config.get("country") == "Guinea-Bissau":
            emit_tier.loc[stype.isin([1, 2])] = 0.0
            emit_tier.loc[stype == 3] = 3.0
            emit_tier.loc[stype == 4] = 1.0
            emit_tier.loc[stype.isin([5, 6])] = 4.0
            emit_tier.loc[stype.isin([7, 8])] = 5.0
        else:
            emit_tier.loc[stype.isin([1, 2, 3, 5, 22])] = 0.0
            emit_tier.loc[stype.isin([4, 6, 7, 8, 9, 20, 21])] = 3.0
            emit_tier.loc[stype.isin([10, 11, 12, 13, 14, 23])] = 4.0
            emit_tier.loc[stype.isin([15, 16, 17, 18, 19])] = 5.0
        stoves["emit_tier"] = emit_tier

        # Cooking time per stove
        daily = pd.Series(0.0, index=stoves.index)
        for q in ["SEC_G_Q21", "SEC_G_Q22a", "SEC_G_Q22b", "SEC_G_Q22c"]:
            if q in stoves.columns:
                daily += stoves[q].fillna(0.0)

        days = stoves.get("SEC_G_Q19", 1.0).fillna(1.0).clip(lower=1.0)
        weekly = (daily * days).clip(lower=1.0)
        stoves["weekly_time"] = weekly
        stoves["weighted_emit"] = stoves["emit_tier"] * weekly

        emit_agg = stoves.groupby("interview__id").agg(
            weighted_sum=("weighted_emit", "sum"),
            time_sum=("weekly_time", "sum"),
            stove_count=("SEC_G_Q05", "count")
        ).reset_index()

        ratio = emit_agg["weighted_sum"] / emit_agg["time_sum"]
        emit_agg["weighted_emit_tier"] = np.floor(ratio + 0.5).clip(0, 5)
        df = df.merge(emit_agg[["interview__id", "weighted_emit_tier", "stove_count"]], on="interview__id", how="left")

        # Stacking summary: clean_stove, ics, trad_stove, stove_stacking
        try:
            stype_code = pd.Series(np.nan, index=stoves.index)
            stype_code.loc[stype.isin([1, 2, 3, 5, 22])] = 1.0
            stype_code.loc[stype.isin([4, 6, 7, 8, 9, 20, 21])] = 2.0
            stype_code.loc[stype.isin([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 23])] = 3.0
            stoves["stove_type_cat"] = stype_code

            counts = stoves.groupby("interview__id").size() - 1
            stoves["stacking_num"] = stoves["interview__id"].map(counts)
            wide = stoves.pivot(index="interview__id", columns="cookstoves__id", values=["stove_type_cat", "stacking_num"])
            wide.columns = [f"{col}_{int(val)}" for col, val in wide.columns]
            if "stacking_num_1" in wide.columns:
                wide["stove_stacking"] = wide["stacking_num_1"] + 1.0
            else:
                wide["stove_stacking"] = 1.0

            s_cols = [c for c in wide.columns if c.startswith("stove_type_cat_")]
            wide["clean_stove"] = wide[s_cols].isin([3]).any(axis=1).astype(float)
            wide["ics"] = wide[s_cols].isin([2]).any(axis=1).astype(float)
            wide["trad_stove"] = wide[s_cols].isin([1]).any(axis=1).astype(float)

            df = df.merge(wide[["clean_stove", "ics", "trad_stove", "stove_stacking"]].reset_index(), on="interview__id", how="left")
            df["clean_stove"] = df["clean_stove"].fillna(0.0)
            df["ics"] = df["ics"].fillna(0.0)
            df["trad_stove"] = df["trad_stove"].fillna(0.0)
            df["stove_stacking"] = df["stove_stacking"].fillna(0.0)
        except Exception:
            pass

        return df

    def _process_solar(self, df_base: pd.DataFrame) -> pd.DataFrame:
        df = df_base.copy()
        f_solar = self._resolve_file("solar_device")
        if not f_solar:
            return df

        solar = pd.read_stata(f_solar, convert_categoricals=False)
        solar = self._normalize_id(solar)
        if "Solar_C_Device__id" in solar.columns:
            solar = solar[solar["Solar_C_Device__id"].notna()].copy()

        # TV, fan, fridge, laptop (phone excluded from heavy appliances!)
        s_tv = solar[["SEC_C_Q125__1", "SEC_C_Q127__1"]].max(axis=1) if "SEC_C_Q125__1" in solar.columns else pd.Series(0, index=solar.index)
        s_fan = solar[["SEC_C_Q125__2", "SEC_C_Q127__2"]].max(axis=1) if "SEC_C_Q125__2" in solar.columns else pd.Series(0, index=solar.index)
        s_fridge = solar[["SEC_C_Q125__3", "SEC_C_Q127__3"]].max(axis=1) if "SEC_C_Q125__3" in solar.columns else pd.Series(0, index=solar.index)
        s_laptop = solar[["SEC_C_Q125__4", "SEC_C_Q127__4"]].max(axis=1) if "SEC_C_Q125__4" in solar.columns else pd.Series(0, index=solar.index)
        oth_app_cols = [c for c in ["SEC_C_Q125_6", "SEC_C_Q125_7", "SEC_C_Q125_8", "SEC_C_Q125_9"] if c in solar.columns]
        s_oth = solar[oth_app_cols].max(axis=1) if oth_app_cols else pd.Series(0, index=solar.index)

        solar_appl = pd.concat([s_tv, s_fan, s_fridge, s_laptop, s_oth], axis=1).max(axis=1).fillna(0)

        q123 = solar.get("SEC_C_Q123", np.nan).replace({888: np.nan})
        q128b = solar.get("SEC_C_Q128b", np.nan).copy()

        q128b.loc[(q128b != 1) & (solar_appl == 0) & (q123 < 2)] = 1
        q128b.loc[(q128b != 2) & (solar_appl == 0) & (q123 > 1) & q123.notna()] = 2
        q128b.loc[(q128b != 3) & (solar_appl != 0)] = 3
        q128b.loc[(q128b == 2) & (solar_appl == 0) & q123.isna()] = 1
        q128b.loc[(q128b == 3) & (solar_appl == 0) & q123.isna()] = 1
        solar["SEC_C_Q128b_reclass"] = q128b

        if "SEC_C_Q141" in df.columns:
            main_keys = df[["interview__id", "SEC_C_Q141"]].dropna()
            main_solar = solar.merge(main_keys, left_on=["interview__id", "Solar_C_Device__id"], right_on=["interview__id", "SEC_C_Q141"])
            main_solar = main_solar.drop_duplicates("interview__id")
            if "SEC_C_Q128b_reclass" in main_solar.columns:
                main_solar["SEC_C_Q128b"] = main_solar["SEC_C_Q128b_reclass"]

            cols_to_merge = ["interview__id"] + [c for c in main_solar.columns if c not in df.columns]
            df = df.merge(main_solar[cols_to_merge], on="interview__id", how="left")
            if "SEC_C_Q128b_reclass" in main_solar.columns:
                df["SEC_C_Q128b"] = main_solar.set_index("interview__id")["SEC_C_Q128b"].reindex(df["interview__id"]).values

        return df

    def _process_appliances_and_time(self, df_base: pd.DataFrame) -> pd.DataFrame:
        df = df_base.copy()

        # Time Use
        f_time = self._resolve_file("time_use")
        if f_time:
            tu = pd.read_stata(f_time, convert_categoricals=False)
            tu = self._normalize_id(tu)
            if "time_use__id" in tu.columns and "SEC_L_Q02" in tu.columns:
                tu_fem = tu[tu["time_use__id"].isin([1, 2])].groupby("interview__id")["SEC_L_Q02"].sum().rename("cooktime_female").reset_index()
                tu_mal = tu[tu["time_use__id"].isin([3, 4])].groupby("interview__id")["SEC_L_Q02"].sum().rename("cooktime_male").reset_index()
                df = df.merge(tu_fem, on="interview__id", how="left").merge(tu_mal, on="interview__id", how="left")

        # Appliances
        f_app = self._resolve_file("appliances")
        if f_app:
            app = pd.read_stata(f_app, convert_categoricals=False)
            app = self._normalize_id(app)
            aid_col = "appliances__id" if "appliances__id" in app.columns else "appliance__id"
            if aid_col in app.columns and "SEC_F_Q02a" in app.columns:
                owns = app[app["SEC_F_Q02a"] > 0].copy()
                aid = owns[aid_col]
                owns["is_verylow"] = aid.isin([1, 2, 3, 4, 5, 6, 7, 28, 29]).astype(int)
                owns["is_low"] = aid.isin([8, 9, 26, 30, 31, 32, 33]).astype(int)
                owns["is_med"] = aid.isin([10, 15, 16, 17, 20, 21, 27, 35, 36]).astype(int)
                owns["is_high"] = aid.isin([11, 13, 14, 18]).astype(int)
                owns["is_veryhigh"] = aid.isin([22, 23, 24, 25, 34]).astype(int)
                owns["has_lights"] = aid.isin([1, 2, 3, 4]).astype(int)
                owns["has_fridge"] = aid.isin([10, 17]).astype(int)
                owns["has_fan"] = (aid == 9).astype(int)
                owns["has_tv"] = aid.isin([30, 31, 32]).astype(int)
                owns["has_charger"] = aid.isin([28, 29]).astype(int)
                owns["has_radio"] = aid.isin([6, 7]).astype(int)
                owns["has_iron"] = (aid == 13).astype(int)
                owns["has_micro"] = (aid == 11).astype(int)
                owns["has_wash"] = (aid == 18).astype(int)
                owns["has_ac"] = (aid == 22).astype(int)
                owns["has_geyser"] = aid.isin([24, 25]).astype(int)
                owns["has_torch"] = (aid == 5).astype(int)

                for a in range(1, 43):
                    owns[f"app_own_{a}"] = (aid == a).astype(int)

                app_agg = owns.groupby("interview__id").max().reset_index()
                app_vars = [
                    "is_verylow", "is_low", "is_med", "is_high", "is_veryhigh",
                    "has_lights", "has_fridge", "has_fan", "has_tv",
                    "has_charger", "has_radio", "has_iron", "has_micro", "has_wash", "has_ac", "has_geyser", "has_torch"
                ] + [f"app_own_{a}" for a in range(1, 43)]
                cols_app = ["interview__id"] + [c for c in app_vars if c in owns.columns]
                df = df.merge(app_agg[cols_app], on="interview__id", how="left")

        app_fill_vars = [
            "is_verylow", "is_low", "is_med", "is_high", "is_veryhigh",
            "has_lights", "has_fridge", "has_fan", "has_tv",
            "has_charger", "has_radio", "has_iron", "has_micro", "has_wash", "has_ac", "has_geyser", "has_torch"
        ] + [f"app_own_{a}" for a in range(1, 43)]
        for c in app_fill_vars:
            if c in df.columns:
                df[c] = df[c].fillna(0).astype(int)

        return df

    def _process_cooking_tiers(self, df_base: pd.DataFrame) -> pd.DataFrame:
        """Matches main cookstove and computes full 6 MECS Cooking Attributes and Tier Aggregates."""
        df = df_base.copy()

        # Match main stove by SEC_G_Q04
        f_stoves = self._resolve_file("cookstoves")
        if f_stoves:
            stoves = pd.read_stata(f_stoves, convert_categoricals=False)
            stoves = self._normalize_id(stoves)
            stoves = stoves[stoves["cookstoves__id"].notna()].copy()
            if "SEC_G_Q03" in stoves.columns:
                stoves = stoves[~stoves["SEC_G_Q03"].isin(["Does not cook", "microwave oven"])]
            
            if "SEC_G_Q05_oth" in stoves.columns:
                stoves.loc[stoves["SEC_G_Q05_oth"].astype(str).str.lower().str.strip().isin([
                    "fogareiro", "fugão a carvão", "fogareiro com carvão", "figareiro",
                    "fogão de carvão", "fogadeiro", "construído com pesas de ferro para cozinhar", "fogadero"
                ]), "SEC_G_Q05"] = 2
                stoves.loc[stoves["SEC_G_Q05_oth"].isin(["Fire wood", "Wood", "open fire on the ground"]), "SEC_G_Q05"] = 1
                stoves.loc[stoves["SEC_G_Q05_oth"] == "four plate stove", "SEC_G_Q05"] = 19
                stoves.loc[stoves["SEC_G_Q05_oth"] == "Gas-Eletric stove", "SEC_G_Q05"] = 23
                stoves.loc[stoves["SEC_G_Q05_oth"] == "Traditional stove", "SEC_G_Q05"] = 22

            if "SEC_G_Q05" in stoves.columns:
                stoves.loc[stoves["SEC_G_Q05"].isin([555, 96]), "SEC_G_Q05"] = np.nan
                
            if "SEC_G_Q04" in df.columns:
                main_match = stoves.merge(df[["interview__id", "SEC_G_Q04"]].dropna(), left_on=["interview__id", "cookstoves__id"], right_on=["interview__id", "SEC_G_Q04"])
                cols_keep = [c for c in main_match.columns if c not in df.columns or c == "interview__id"]
                main_sub = main_match[cols_keep].drop_duplicates("interview__id")
                df = df.merge(main_sub, on="interview__id", how="left")

        # Primary fuel SEC_G_Q16
        q16_cols = [c for c in df.columns if c.startswith("SEC_G_Q16__") and not c.endswith("111")]
        if q16_cols:
            df["SEC_G_Q16"] = np.nan
            for idx in range(1, 16):
                col_name = f"SEC_G_Q16__{idx}"
                if col_name in df.columns:
                    df.loc[df[col_name] == 1, "SEC_G_Q16"] = idx
            if "SEC_G_Q16__111" in df.columns:
                df.loc[df["SEC_G_Q16__111"] == 1, "SEC_G_Q16"] = 111
            if "SEC_G_Q05" in df.columns:
                df.loc[(df["SEC_G_Q05"] == 19) & df["SEC_G_Q16"].isna(), "SEC_G_Q16"] = 16

        # Match fuel availability SEC_G_Q17 from stove_fuel.dta
        f_sf = self._resolve_file("stove_fuel")
        if f_sf and "SEC_G_Q16" in df.columns and "SEC_G_Q04" in df.columns:
            sf = pd.read_stata(f_sf, convert_categoricals=False)
            sf = self._normalize_id(sf)
            sf_match = sf.merge(df[["interview__id", "SEC_G_Q04", "SEC_G_Q16"]].dropna(), left_on=["interview__id", "cookstoves__id", "stove_fuel__id"], right_on=["interview__id", "SEC_G_Q04", "SEC_G_Q16"])
            if "SEC_G_Q17" in sf_match.columns:
                sf_sub = sf_match[["interview__id", "SEC_G_Q17"]].drop_duplicates("interview__id")
                if "SEC_G_Q17" in df.columns:
                    df = df.drop(columns=["SEC_G_Q17"])
                df = df.merge(sf_sub, on="interview__id", how="left")

        # Fuel collection & time from time_coll.dta
        f_tc = self._resolve_file("time_coll")
        if f_tc:
            tc = pd.read_stata(f_tc, convert_categoricals=False)
            tc = self._normalize_id(tc)
            tc["SEC_I_Q12"] = tc["SEC_I_Q12"].clip(upper=1440.0)
            
            mult_map = {
                1: 7.0, 2: 1.0, 3: 2.0, 4: 7.0 / 14.0, 5: 7.0 / 21.0, 6: 7.0 / 30.0,
                7: 7.0 / 60.0, 8: 7.0 / 90.0, 9: 7.0 / 120.0, 10: 7.0 / 150.0, 11: 7.0 / 180.0,
                12: 3.0, 13: 4.0, 14: 5.0, 15: 7.0 / 2.0, 16: 7.0 / 360.0, 17: 3.0 * (7.0 / 30.0),
                18: 2.0 * (7.0 / 30.0), 19: 7.0 / 30.0
            }
            tc = self._apply_excel_recodes(tc, "SEC_I_Q13", "SEC_I_Q13_oth")
            q13 = self._col(tc, "SEC_I_Q13", np.nan)
            mult = q13.map(mult_map)
            tc["SEC_I_Q12_week"] = ((self._col(tc, "SEC_I_Q12", 0.0).fillna(0.0) / 60.0) * mult).astype(np.float32)
            tc["SEC_I_Q14_week"] = ((self._col(tc, "SEC_I_Q14", 0.0).fillna(0.0) / 60.0) * 7.0).astype(np.float32)
            
            tc_tot12 = tc.groupby("interview__id")["SEC_I_Q12_week"].sum(min_count=0).astype(np.float32).rename("SEC_I_Q12_total")
            tc_tot14 = tc.groupby("interview__id")["SEC_I_Q14_week"].sum(min_count=0).astype(np.float32).rename("SEC_I_Q14_total")
            
            tc_hh = pd.concat([tc_tot12, tc_tot14], axis=1).reset_index()
            tc_hh["cs_fcol_fpre"] = (tc_hh["SEC_I_Q12_total"] + tc_hh["SEC_I_Q14_total"]).astype(np.float32)
            
            tc["yr_coll_hr"] = tc["SEC_I_Q12_week"] * 52.0
            tid = self._col(tc, "time_collecting__id", 0)
            tc["women_fuel_hr_yr"] = np.where(tid == 1, tc["yr_coll_hr"], 0.0)
            tc["girls_fuel_hr_yr"] = np.where(tid == 2, tc["yr_coll_hr"], 0.0)
            tc["men_fuel_hr_yr"]   = np.where(tid == 3, tc["yr_coll_hr"], 0.0)
            tc["boys_fuel_hr_yr"]  = np.where(tid == 4, tc["yr_coll_hr"], 0.0)
            
            demo_tot = tc.groupby("interview__id").agg(
                women_fuel_hr_yr_hh=("women_fuel_hr_yr", "sum"),
                girls_fuel_hr_yr_hh=("girls_fuel_hr_yr", "sum"),
                men_fuel_hr_yr_hh=("men_fuel_hr_yr", "sum"),
                boys_fuel_hr_yr_hh=("boys_fuel_hr_yr", "sum")
            ).reset_index()
            
            tc_merged = tc_hh.merge(demo_tot, on="interview__id", how="left")
            for c in ["SEC_I_Q12_total", "SEC_I_Q14_total", "cs_fcol_fpre", "women_fuel_hr_yr_hh", "girls_fuel_hr_yr_hh", "men_fuel_hr_yr_hh", "boys_fuel_hr_yr_hh"]:
                if c in df.columns:
                    df = df.drop(columns=[c])
            df = df.merge(tc_merged, on="interview__id", how="left")
            for c in ["SEC_I_Q12_total", "SEC_I_Q14_total", "cs_fcol_fpre", "women_fuel_hr_yr_hh", "girls_fuel_hr_yr_hh", "men_fuel_hr_yr_hh", "boys_fuel_hr_yr_hh"]:
                df[c] = df[c].fillna(0.0)
        else:
            df["cs_fcol_fpre"] = 0.0

        # 1. Main stove mapping
        stype = df["SEC_G_Q05"] if "SEC_G_Q05" in df.columns else pd.Series(np.nan, index=df.index)
        mainstove = pd.Series(np.nan, index=df.index)
        if self.config.get("country_iso3") == "GNB" or self.config.get("country") == "Guinea-Bissau":
            mainstove.loc[stype == 1] = 1.0
            mainstove.loc[stype.isin([2, 4])] = 2.0
            mainstove.loc[stype == 3] = 3.0
            mainstove.loc[stype.isin([5, 6])] = 4.0
            mainstove.loc[stype == 7] = 5.0
            mainstove.loc[stype == 8] = 6.0
        else:
            mainstove.loc[stype.isin([1, 2])] = 1.0
            mainstove.loc[stype.isin([3, 5, 22])] = 2.0
            mainstove.loc[stype.isin([4, 6, 7, 8, 9, 20, 21])] = 3.0
            mainstove.loc[stype.isin([10, 11, 12, 13, 14, 23])] = 4.0
            mainstove.loc[stype.isin([19])] = 5.0
            mainstove.loc[stype.isin([17, 18])] = 6.0
            mainstove.loc[stype.isin([15])] = 7.0
            mainstove.loc[stype.isin([16])] = 8.0
        mainstove.loc[stype == 555] = 555.0

        # Correct misclassified gas stoves per Kat's code
        if "SEC_G_Q16__15" in df.columns:
            mainstove.loc[(mainstove != 4) & (df["SEC_G_Q16__15"] == 1)] = 4.0

        df["mainstove"] = mainstove
        df["electricstove"] = (mainstove == 5).astype(int)

        # 2. cs_emit_tier (ISO emission tier)
        cs_emit = pd.Series(np.nan, index=df.index)
        if self.config.get("country_iso3") == "GNB" or self.config.get("country") == "Guinea-Bissau":
            cs_emit.loc[stype.isin([1, 2])] = 0.0
            cs_emit.loc[stype == 3] = 3.0
            cs_emit.loc[stype == 4] = 1.0
            cs_emit.loc[stype.isin([5, 6])] = 4.0
            cs_emit.loc[stype.isin([7, 8])] = 5.0
        else:
            cs_emit.loc[stype.isin([1, 2])] = 0.0
            cs_emit.loc[stype.isin([3, 5, 22])] = 0.0
            cs_emit.loc[stype.isin([4, 6, 7, 8, 9, 20, 21])] = 3.0
            cs_emit.loc[stype.isin([10, 11, 12, 13, 14, 23])] = 4.0
            cs_emit.loc[stype.isin([19])] = 5.0
            cs_emit.loc[stype.isin([17, 18])] = 5.0
            cs_emit.loc[stype.isin([15])] = 5.0
            cs_emit.loc[stype.isin([16])] = 4.0

            cs_emit.loc[mainstove.isin([1, 2]) & cs_emit.isna()] = 0.0
            cs_emit.loc[mainstove.isin([3]) & cs_emit.isna()] = 3.0
            cs_emit.loc[mainstove.isin([4, 8]) & cs_emit.isna()] = 4.0
            cs_emit.loc[mainstove.isin([5, 6, 7]) & cs_emit.isna()] = 5.0
        df["cs_emit_tier"] = cs_emit

        # 3. Ventilation & Exposure Tier (cs_exp_tier)
        q14 = self._col(df, "SEC_G_Q14", np.nan)
        q15_1 = self._col(df, "SEC_G_Q15__1", 0)
        q15_2 = self._col(df, "SEC_G_Q15__2", 0)
        q15_111 = self._col(df, "SEC_G_Q15__111", 0)
        q28 = self._col(df, "SEC_G_Q28", np.nan).replace({20: 1})

        vent_strc = pd.Series(np.nan, index=df.index)
        vent_strc.loc[(q14 == 5) | mainstove.isin([4, 5, 6, 7, 8])] = 5.0
        vent_strc.loc[q14 == 4] = 4.0
        vent_strc.loc[q14.isin([1, 2, 3]) & ((q15_1 == 1) | (q15_2 == 1))] = 3.0
        vent_strc.loc[q14.isin([1, 2, 3]) & (q28 >= 2) & (q28 != 888) & vent_strc.isna()] = 2.0
        vent_strc.loc[q14.isin([1, 2, 3]) & (q28 == 1) & (q28 != 888) & vent_strc.isna()] = 1.0
        vent_strc.loc[q14.isin([1, 2, 3]) & (q15_111 == 1) & (q28 == 0) & vent_strc.isna()] = 0.0

        vent_tier = pd.Series(np.nan, index=df.index)
        vent_tier.loc[vent_strc.isin([0, 1, 2])] = 2.0
        vent_tier.loc[vent_strc == 3] = 3.0
        vent_tier.loc[vent_strc.isin([4, 5])] = 5.0

        cs_exp = pd.Series(np.nan, index=df.index)
        cs_exp.loc[cs_emit == 5] = 5.0
        cs_exp.loc[(cs_emit == 4) & (vent_tier == 5)] = 5.0
        cs_exp.loc[(cs_emit == 4) & vent_tier.isin([2, 3])] = 4.0
        cs_exp.loc[(cs_emit == 3) & (vent_tier == 5)] = 4.0
        cs_exp.loc[(cs_emit == 3) & (vent_tier == 3)] = 3.0
        cs_exp.loc[(cs_emit == 3) & (vent_tier == 2)] = 2.0
        cs_exp.loc[(cs_emit == 2) & (vent_tier == 5)] = 3.0
        cs_exp.loc[(cs_emit == 2) & (vent_tier == 3)] = 2.0
        cs_exp.loc[(cs_emit == 2) & (vent_tier == 2)] = 1.0
        cs_exp.loc[(cs_emit == 1) & (vent_tier == 5)] = 2.0
        cs_exp.loc[(cs_emit == 1) & (vent_tier == 3)] = 1.0
        cs_exp.loc[(cs_emit == 1) & (vent_tier == 2)] = 0.0
        cs_exp.loc[(cs_emit == 0) & (vent_tier == 5)] = 1.0
        cs_exp.loc[(cs_emit == 0) & vent_tier.isin([2, 3])] = 0.0
        cs_exp.loc[cs_exp.isna() & vent_tier.isna() & mainstove.notna()] = cs_emit.loc[cs_exp.isna() & vent_tier.isna() & mainstove.notna()]

        trad_mode = cs_exp.loc[mainstove == 2].mode()
        if not trad_mode.empty:
            cs_exp.loc[(mainstove == 2) & cs_exp.isna()] = trad_mode.min()
        ics_mode = cs_exp.loc[mainstove == 3].mode()
        if not ics_mode.empty:
            cs_exp.loc[(mainstove == 3) & cs_exp.isna()] = ics_mode.min()
        cs_exp.loc[(mainstove == 1) & cs_exp.isna()] = 0.0
        cs_exp.loc[mainstove.isin([4, 5, 6, 7, 8]) & cs_exp.isna()] = 5.0
        df["cs_exp_tier"] = cs_exp

        # 4. Efficiency Tier (cs_efcy_tier)
        cs_efcy = pd.Series(np.nan, index=df.index)
        if self.config.get("country_iso3") == "GNB" or self.config.get("country") == "Guinea-Bissau":
            cs_efcy.loc[stype.isin([1, 2, 4])] = 0.0
            cs_efcy.loc[stype == 3] = 2.0
            cs_efcy.loc[stype.isin([5, 6])] = 4.0
            cs_efcy.loc[stype.isin([7, 8])] = 5.0
        else:
            cs_efcy.loc[stype.isin([1, 2])] = 0.0
            cs_efcy.loc[stype.isin([3, 5, 22])] = 0.0
            cs_efcy.loc[stype.isin([4, 6, 7, 8, 9, 20, 21])] = 2.0
            cs_efcy.loc[stype.isin([10, 11, 12, 13, 14, 23])] = 4.0
            cs_efcy.loc[stype.isin([19])] = 5.0
            cs_efcy.loc[stype.isin([17, 18])] = 5.0
            cs_efcy.loc[stype.isin([15])] = 4.0
            cs_efcy.loc[stype.isin([16])] = 3.0

            cs_efcy.loc[mainstove.isin([1, 2]) & cs_efcy.isna()] = 0.0
            cs_efcy.loc[mainstove.isin([3]) & cs_efcy.isna()] = 2.0
            cs_efcy.loc[mainstove.isin([8]) & cs_efcy.isna()] = 3.0
            cs_efcy.loc[mainstove.isin([4, 7]) & cs_efcy.isna()] = 4.0
            cs_efcy.loc[mainstove.isin([5, 6]) & cs_efcy.isna()] = 5.0
        df["cs_efcy_tier"] = cs_efcy

        # Convenience Tier
        fcol = df["cs_fcol_fpre"].astype(np.float32)
        cs_conv = pd.Series(np.nan, index=df.index)
        cs_conv.loc[fcol >= 7.0] = 1.0
        cs_conv.loc[(fcol >= 3.0) & (fcol < 7.0)] = 2.0
        cs_conv.loc[(fcol >= 1.5) & (fcol < 3.0)] = 3.0
        cs_conv.loc[(fcol >= 0.5) & (fcol < 1.5)] = 4.0
        cs_conv.loc[fcol < 0.5] = 5.0
        cs_conv.loc[mainstove.isin([4, 5, 6, 7, 8])] = 5.0
        df["cs_conv_tier"] = cs_conv.fillna(5.0)

        # Safety Tier
        q23 = df["SEC_G_Q23"] if "SEC_G_Q23" in df.columns else pd.Series(np.nan, index=df.index)
        cs_sfty = pd.Series(5.0, index=df.index)
        cs_sfty.loc[q23 == 1] = 0.0
        cs_sfty.loc[q23.isin([2, 5, 7])] = 2.0
        cs_sfty.loc[q23.isin([3, 4, 6])] = 3.0
        df["cs_sfty_tier"] = cs_sfty

        # Affordability Tier (fuel spend < 5% HH exp)
        cf_share = df["fuel_exp_tot_yr"] / df["exp_total_yr"].clip(lower=1.0)
        cs_affd = pd.Series(5.0, index=df.index)
        cs_affd.loc[cf_share >= 0.05] = 2.0
        df["cs_affd_tier"] = cs_affd

        # Availability Tier
        q17 = df["SEC_G_Q17"] if "SEC_G_Q17" in df.columns else pd.Series(np.nan, index=df.index)
        cs_avbl = pd.Series(np.nan, index=df.index)
        cs_avbl.loc[q17 == 4] = 2.0
        cs_avbl.loc[q17 == 3] = 3.0
        cs_avbl.loc[q17 == 2] = 4.0
        cs_avbl.loc[q17 == 1] = 5.0
        cs_avbl.loc[mainstove.isin([5, 6, 7, 8])] = 5.0
        m1_mode = cs_avbl.loc[mainstove == 1].mode()
        if not m1_mode.empty:
            cs_avbl.loc[(mainstove == 1) & cs_avbl.isna()] = m1_mode.iloc[0]
        m4_mode = cs_avbl.loc[mainstove == 4].mode()
        if not m4_mode.empty:
            cs_avbl.loc[(mainstove == 4) & cs_avbl.isna()] = m4_mode.iloc[0]
        df["cs_avbl_tier"] = cs_avbl.fillna(5.0)

        # Aggregate MECS Cooking Tier = min(Exposure, Convenience, Safety, Availability)
        df["cs_aggr_tier"] = df[["cs_exp_tier", "cs_conv_tier", "cs_sfty_tier", "cs_avbl_tier"]].min(axis=1)
        df["cs_aggr_tier_6attr"] = df[["cs_exp_tier", "cs_efcy_tier", "cs_conv_tier", "cs_sfty_tier", "cs_affd_tier", "cs_avbl_tier"]].min(axis=1)
        df["mecs_access"] = np.where(df["cs_aggr_tier"].notna(), (df["cs_aggr_tier"] >= 1).astype(float), np.nan)
        df["mecs_modern"] = np.where(df["cs_aggr_tier"].notna(), (df["cs_aggr_tier"] >= 4).astype(float), np.nan)
        df["mecs_trans"] = np.where(df["cs_aggr_tier"].notna(), df["cs_aggr_tier"].isin([2, 3]).astype(float), np.nan)

        # Stove Primary Type
        spt = pd.Series(np.nan, index=df.index)
        spt.loc[mainstove == 1] = 1.0
        spt.loc[mainstove.isin([2, 3])] = 2.0
        spt.loc[mainstove == 4] = 3.0
        spt.loc[mainstove.isin([7, 8])] = 4.0
        spt.loc[mainstove.isin([5, 6])] = 5.0
        df["stove_primary_type"] = spt

        return df

    def _process_electricity_tiers(self, df_base: pd.DataFrame) -> pd.DataFrame:
        """Reconciles electricity sources and computes 7 MTF Electricity Attributes and Aggregates."""
        df = df_base.copy()

        # Reconcile SEC_C_Q162 with actual solar device type
        elec_src_cols = [c for c in ["SEC_C_Q02", "SEC_C_Q40", "SEC_C_Q78", "SEC_C_Q100", "SEC_C_Q117"] if c in df.columns]
        df["nbr_elec"] = df[elec_src_cols].fillna(0).sum(axis=1)

        q128b = self._col(df, "SEC_C_Q128b", np.nan)
        q162 = self._col(df, "SEC_C_Q162", np.nan).copy()
        q02 = self._col(df, "SEC_C_Q02", 0)
        q117 = self._col(df, "SEC_C_Q117", 0)
        nbr_e = df["nbr_elec"]

        # If SEC_C_Q162 is entirely missing/empty, initialize from primary sources
        if q162.isna().all():
            q40 = self._col(df, "SEC_C_Q40", 0)
            q78 = self._col(df, "SEC_C_Q78", 0)
            q100 = self._col(df, "SEC_C_Q100", 0)
            q162.loc[q02 == 1] = 1
            q162.loc[(q162.isna()) & (q40 == 1)] = 2
            q162.loc[(q162.isna()) & (q78 == 1)] = 3
            q162.loc[(q162.isna()) & (q117 == 1) & (q128b == 1)] = 4
            q162.loc[(q162.isna()) & (q117 == 1) & (q128b == 2)] = 5
            q162.loc[(q162.isna()) & (q117 == 1) & (q128b == 3)] = 6
            q162.loc[(q162.isna()) & (q117 == 1)] = 5
            q162.loc[(q162.isna()) & (q100 == 1)] = 7
            q162 = q162.fillna(8)

        q162.loc[(q128b == 1) & q162.isin([5, 6])] = 4
        q162.loc[(q128b == 2) & q162.isin([4, 6])] = 5
        q162.loc[(q128b == 3) & q162.isin([4, 5])] = 6

        q162.loc[(q02 == 1) & (q162.isna() | q162.isin([8, 111])) & (nbr_e == 1)] = 1
        q162.loc[(q128b == 1) & (q117 == 1) & (q162.isna() | q162.isin([8, 111])) & (nbr_e == 1)] = 4
        q162.loc[(q128b == 2) & (q117 == 1) & (q162.isna() | q162.isin([8, 111])) & (nbr_e == 1)] = 5
        q162.loc[(q128b == 3) & (q117 == 1) & (q162.isna() | q162.isin([8, 111])) & (nbr_e == 1)] = 6
        df["SEC_C_Q162"] = q162

        # elec_tech_type: 1=Grid, 2=Mini-grid, 3=Generator, 4=SHS, 5=SLS, 6=SL, 7=Rech Battery, 8=No Access / Dry-cell
        tech = pd.Series(np.nan, index=df.index)
        tech.loc[q162 == 1] = 1
        tech.loc[q162 == 2] = 2
        tech.loc[q162 == 3] = 3
        tech.loc[q162 == 6] = 4
        tech.loc[q162 == 5] = 5
        tech.loc[q162 == 4] = 6
        tech.loc[q162 == 7] = 7
        tech.loc[q162.isin([8, 111])] = 8
        tech = tech.fillna(8)
        df["elec_tech_type"] = tech

        df["grid_hh"] = (df["elec_tech_type"] == 1).astype(int)
        df["solar_hh"] = df["elec_tech_type"].isin([4, 5, 6]).astype(int)

        # Capacity Tier
        mob_chrge = (df["SEC_C_Q122"] == 1) if "SEC_C_Q122" in df.columns else pd.Series(False, index=df.index)
        radio = (df["SEC_C_Q124"] == 1) if "SEC_C_Q124" in df.columns else pd.Series(False, index=df.index)
        if "SEC_C_Q117" in df.columns:
            mob_chrge = mob_chrge & (df["SEC_C_Q117"] == 1)
            radio = radio & (df["SEC_C_Q117"] == 1)

        sl_score = pd.Series(np.nan, index=df.index)
        sls_mask = (q162 == 5)
        sl_score.loc[sls_mask] = (2.0 / df.loc[sls_mask, "hhsize"]).clip(upper=0.7)
        sl_score.loc[sls_mask & (mob_chrge | radio)] += 0.3

        sl_mask = (q162 == 4)
        sl_score.loc[sl_mask] = (1.0 / df.loc[sl_mask, "hhsize"]).clip(upper=0.7)
        sl_score.loc[sl_mask & (mob_chrge | radio)] += 0.3
        df["elc_cap_tier01"] = sl_score

        sl_valid = sl_score.dropna()
        if len(sl_valid) > 0:
            w_sl = df.loc[sl_valid.index, "hh_wt"]
            sl_cutoff = float(np.sum(sl_valid * w_sl) / np.sum(w_sl))
        else:
            sl_cutoff = 0.3428549

        # Solar appliance tier & applpower
        sat = pd.Series(np.nan, index=df.index)
        sat.loc[q162.isin([4, 5, 6]) & (self._col(df, "SEC_C_Q125__111", 0) == 1)] = 0.0
        sat.loc[q162.isin([4, 5, 6]) & ((self._col(df, "SEC_C_Q161__1", 0) == 1) | (self._col(df, "SEC_C_Q161__2", 0) == 1) | (self._col(df, "SEC_C_Q125_5", 0) == 1))] = 1.0
        sat.loc[q162.isin([4, 5, 6]) & ((self._col(df, "SEC_C_Q125__1", 0) == 1) | (self._col(df, "SEC_C_Q125__2", 0) == 1) | (self._col(df, "SEC_C_Q125__4", 0) == 1) | (self._col(df, "SEC_C_Q125_9", 0) == 1) | (self._col(df, "SEC_C_Q161__3", 0) == 1) | (self._col(df, "SEC_C_Q161__4", 0) == 1))] = 2.0
        sat.loc[q162.isin([4, 5, 6]) & ((self._col(df, "SEC_C_Q125__3", 0) == 1) | (self._col(df, "SEC_C_Q125_6", 0) == 1) | (self._col(df, "SEC_C_Q125_8", 0) == 1) | (self._col(df, "SEC_C_Q161__5", 0) == 1))] = 3.0
        sat.loc[q162.isin([4, 5, 6]) & (self._col(df, "SEC_C_Q161__8", 0) == 1)] = 4.0
        sat.loc[q162.isin([4, 5, 6]) & ((self._col(df, "SEC_C_Q161__7", 0) == 1) | (self._col(df, "SEC_C_Q125_7", 0) == 1))] = 5.0
        df["solar_app_tier"] = sat
        df["solar_app_tier"] = sat

        # Rechargeable battery and generator appliance power tiers
        def _get_app_tier(tech_code: int) -> pd.Series:
            m = (nbr_e == 1) & (q162 == tech_code)
            tier = pd.Series(np.nan, index=df.index)
            t1_cols = [f"SEC_F_Q01__{i}" for i in [1, 2, 3, 4, 7, 28, 29, 33] if f"SEC_F_Q01__{i}" in df.columns]
            t2_cols = [f"SEC_F_Q01__{i}" for i in [8, 9, 30, 31, 32, 26] if f"SEC_F_Q01__{i}" in df.columns]
            t3_cols = [f"SEC_F_Q01__{i}" for i in [10, 15, 16, 17, 21, 27] if f"SEC_F_Q01__{i}" in df.columns]
            t4_cols = [f"SEC_F_Q01__{i}" for i in [14, 18, 11, 13] if f"SEC_F_Q01__{i}" in df.columns]
            t5_cols = [f"SEC_F_Q01__{i}" for i in [22, 23, 24, 25] if f"SEC_F_Q01__{i}" in df.columns]

            if t1_cols: tier.loc[m & (df[t1_cols].max(axis=1) == 1)] = 1.0
            if t2_cols: tier.loc[m & (df[t2_cols].max(axis=1) == 1)] = 2.0
            if t3_cols: tier.loc[m & (df[t3_cols].max(axis=1) == 1)] = 3.0
            if t4_cols: tier.loc[m & (df[t4_cols].max(axis=1) == 1)] = 4.0
            if t5_cols: tier.loc[m & (df[t5_cols].max(axis=1) == 1)] = 5.0
            return tier

        rech_app_tier = _get_app_tier(7)
        gen_app_tier = _get_app_tier(3)

        applpower = pd.Series(np.nan, index=df.index)
        applpower.loc[sat == 0] = 0.0
        for lv in range(1, 6):
            applpower.loc[applpower.isna() & ((rech_app_tier == lv) | (gen_app_tier == lv) | (sat == lv))] = float(lv)
        df["applpower"] = applpower

        # Build elc_cap_tier exactly matching Stata
        elc_cap0 = q162.isin([8, 111]).astype(int)
        elc_cap1 = (q162.isin([3, 7]) & (applpower.isna() | (applpower < 2))).astype(int)
        elc_cap2 = ((q162.isin([3, 7]) & (applpower == 2)) | ((q162 == 6) & (applpower.fillna(0) <= 2))).astype(int)
        elc_cap3 = (q162.isin([3, 6, 7]) & (applpower == 3)).astype(int)
        elc_cap4 = (q162.isin([3, 6, 7]) & (applpower == 4)).astype(int)
        elc_cap5 = (q162.isin([1, 2]) | (q162.isin([3, 6, 7]) & (applpower == 5))).astype(int)

        elc_cap1.loc[sl_score > sl_cutoff] = 1
        elc_cap0.loc[sl_score <= sl_cutoff] = 1

        elc_cap = pd.Series(0.0, index=df.index)
        for lv, col_vec in [(1, elc_cap1), (2, elc_cap2), (3, elc_cap3), (4, elc_cap4), (5, elc_cap5)]:
            elc_cap.loc[col_vec == 1] = float(lv)
        df["elc_cap_tier"] = elc_cap

        # Availability Tier
        dur_day = pd.Series(np.nan, index=df.index)
        dur_day.loc[q162 == 1] = self._col(df, "SEC_C_Q27", np.nan)
        dur_day.loc[q162 == 2] = self._col(df, "SEC_C_Q65", np.nan)
        dur_day.loc[q162 == 3] = self._col(df, "SEC_C_Q93", np.nan)
        dur_day.loc[q162.isin([4, 5, 6])] = self._col(df, "SEC_C_Q148", np.nan)
        dur_day.loc[q162 == 7] = self._col(df, "SEC_C_Q111", np.nan)
        dur_day = dur_day.replace({888: np.nan})

        dur_eve = pd.Series(np.nan, index=df.index)
        dur_eve.loc[q162 == 1] = self._col(df, "SEC_C_Q28", np.nan)
        dur_eve.loc[q162 == 2] = self._col(df, "SEC_C_Q66", np.nan)
        dur_eve.loc[q162 == 3] = self._col(df, "SEC_C_Q94", np.nan)
        dur_eve.loc[q162.isin([4, 5, 6])] = self._col(df, "SEC_C_Q149", np.nan)
        dur_eve.loc[q162 == 7] = self._col(df, "SEC_C_Q112", np.nan)
        dur_eve = dur_eve.replace({888: np.nan})

        elc_durd = pd.Series(np.nan, index=df.index)
        elc_durd.loc[dur_day >= 23] = 5.0
        elc_durd.loc[(dur_day < 23) & (dur_day >= 16)] = 4.0
        elc_durd.loc[(dur_day < 16) & (dur_day >= 8)] = 3.0
        elc_durd.loc[(dur_day < 8) & (dur_day >= 4)] = 2.0
        elc_durd.loc[dur_day < 4] = 0.0

        elc_dure = pd.Series(np.nan, index=df.index)
        elc_dure.loc[dur_eve >= 4] = 5.0
        elc_dure.loc[(dur_eve < 4) & (dur_eve >= 3)] = 3.0
        elc_dure.loc[(dur_eve < 3) & (dur_eve >= 2)] = 2.0
        elc_dure.loc[(dur_eve < 2) & (dur_eve >= 1)] = 1.0
        elc_dure.loc[dur_eve < 1] = 0.0

        if "SEC_A_Q05" in df.columns:
            grid_m = (q162 == 1)
            for s_var in [elc_durd, elc_dure]:
                for ea, grp in df[grid_m].groupby("SEC_A_Q05"):
                    ea_m = s_var.loc[grp.index].dropna().mode()
                    if not ea_m.empty:
                        s_var.loc[grp.index] = s_var.loc[grp.index].fillna(ea_m.min())

        for scode in [4, 5, 6]:
            sm = (q162 == scode)
            for s_var in [elc_durd, elc_dure]:
                smode = s_var.loc[sm].dropna().mode()
                if not smode.empty:
                    s_var.loc[sm] = s_var.loc[sm].fillna(smode.min())

        valid_avbl = elc_durd.notna() & elc_dure.notna()
        elc_avbl = pd.Series(np.nan, index=df.index)
        elc_avbl.loc[valid_avbl] = pd.concat([elc_durd, elc_dure], axis=1).min(axis=1).loc[valid_avbl]
        df["elc_avbl_tier"] = elc_avbl

        # Reliability Tier (grid/mini-grid only)
        # Grid outage duration (SEC_C_Q30 from Q30a hr + Q30b min)
        q30_hr = df["SEC_C_Q30a"].replace({888: np.nan}).copy() if "SEC_C_Q30a" in df.columns else pd.Series(np.nan, index=df.index)
        if "SEC_C_Q29" in df.columns:
            q30_hr.loc[df["SEC_C_Q29"] == 111] = 0.0
        q30_min = df["SEC_C_Q30b"].replace({888: np.nan}).copy() if "SEC_C_Q30b" in df.columns else pd.Series(np.nan, index=df.index)
        if "SEC_C_Q29" in df.columns:
            q30_min.loc[df["SEC_C_Q29"] == 111] = 0.0
        q30_min.loc[q30_hr.notna() & q30_min.isna()] = 0.0
        q30_hr.loc[q30_hr.isna() & q30_min.notna()] = 0.0
        df["SEC_C_Q30"] = q30_hr + (q30_min / 60.0)

        # Mini-grid outage duration (SEC_C_Q68 from Q68a hr + Q68b min)
        q68_hr = df["SEC_C_Q68a"].replace({888: np.nan}).copy() if "SEC_C_Q68a" in df.columns else pd.Series(np.nan, index=df.index)
        if "SEC_C_Q67" in df.columns:
            q68_hr.loc[df["SEC_C_Q67"] == 111] = 0.0
        q68_min = df["SEC_C_Q68b"].replace({888: np.nan}).copy() if "SEC_C_Q68b" in df.columns else pd.Series(np.nan, index=df.index)
        if "SEC_C_Q67" in df.columns:
            q68_min.loc[df["SEC_C_Q67"] == 111] = 0.0
        q68_min.loc[q68_hr.notna() & q68_min.isna()] = 0.0
        q68_hr.loc[q68_hr.isna() & q68_min.notna()] = 0.0
        df["SEC_C_Q68"] = q68_hr + (q68_min / 60.0)

        dis_frq = pd.Series(np.nan, index=df.index)
        q29_s = (df["SEC_C_Q29"] if "SEC_C_Q29" in df.columns else pd.Series(np.nan, index=df.index)).replace({888: np.nan, 111: 0.0})
        q67_s = (df["SEC_C_Q67"] if "SEC_C_Q67" in df.columns else pd.Series(np.nan, index=df.index)).replace({888: np.nan, 111: 0.0})
        dis_frq.loc[q162 == 1] = q29_s
        dis_frq.loc[q162 == 2] = q67_s

        dis_dur = pd.Series(np.nan, index=df.index)
        dis_dur.loc[q162 == 1] = df["SEC_C_Q30"].replace({888: np.nan})
        dis_dur.loc[q162 == 2] = df["SEC_C_Q68"].replace({888: np.nan})

        # Match Stata line 268: replace dis_frq = 0 if dis_frq == . & SEC_C_Q30 != .
        dis_frq.loc[dis_frq.isna() & df["SEC_C_Q30"].notna()] = 0.0

        elc_rel = pd.Series(np.nan, index=df.index)
        elc_rel.loc[dis_frq > 14] = 3.0
        # In Stata: dis_dur >= 2 is true when dis_dur is missing (.) because . is +inf in Stata
        c_dur_ge2 = (dis_dur >= 2) | dis_dur.isna()
        elc_rel.loc[((dis_frq > 3) & (dis_frq <= 14)) | ((dis_frq <= 3) & c_dur_ge2)] = 4.0
        elc_rel.loc[(dis_frq <= 3) & (dis_dur < 2)] = 5.0

        # Cluster mode imputation by SEC_A_Q05
        if "SEC_A_Q05" in df.columns:
            for code in [1, 2]:
                m = (q162 == code)
                for ea, grp in df[m].groupby("SEC_A_Q05"):
                    ea_m = elc_rel.loc[grp.index].dropna().mode()
                    if not ea_m.empty:
                        elc_rel.loc[grp.index] = elc_rel.loc[grp.index].fillna(ea_m.min())
        df["elc_rel_tier"] = elc_rel
        df["dis_frq"] = dis_frq
        df["dis_dur"] = dis_dur

        # Quality Tier (grid/mini-grid only)
        appl_dam = pd.Series(np.nan, index=df.index)
        q35 = self._col(df, "SEC_C_Q35", np.nan)
        q73 = self._col(df, "SEC_C_Q73", np.nan)
        appl_dam.loc[(q35 == 0) & (q162 == 1)] = 0.0
        appl_dam.loc[(q35 == 1) & (q162 == 1)] = 1.0
        appl_dam.loc[(q73 == 0) & (q162 == 2)] = 0.0
        appl_dam.loc[(q73 == 1) & (q162 == 2)] = 1.0

        elc_qual = pd.Series(np.nan, index=df.index)
        elc_qual.loc[appl_dam == 1] = 3.0
        elc_qual.loc[appl_dam == 0] = 5.0
        for code in [1, 2]:
            m = (q162 == code)
            ov_qual = elc_qual.loc[m].mode()
            if not ov_qual.empty:
                elc_qual.loc[m & elc_qual.isna()] = ov_qual.iloc[0]
        df["elc_qual_tier"] = elc_qual

        # Formality Tier (grid/mini-grid only)
        elec_pay = pd.Series(np.nan, index=df.index)
        q12 = self._col(df, "SEC_C_Q12", np.nan)
        q48 = self._col(df, "SEC_C_Q48", np.nan)
        elec_pay.loc[(q12 != 111) & (q162 == 1)] = 1.0
        elec_pay.loc[(q12 == 111) & (q162 == 1)] = 0.0
        elec_pay.loc[(q48 != 111) & (q162 == 2)] = 1.0
        elec_pay.loc[(q48 == 111) & (q162 == 2)] = 0.0
        elc_leg = pd.Series(np.nan, index=df.index)
        elc_leg.loc[elec_pay == 0] = 3.0
        elc_leg.loc[elec_pay == 1] = 5.0
        df["elc_leg_tier"] = elc_leg

        # Safety Tier
        elec_inj = pd.Series(0.0, index=df.index)
        q38 = self._col(df, "SEC_C_Q38", 0)
        q76 = self._col(df, "SEC_C_Q76", 0)
        q98 = self._col(df, "SEC_C_Q98", 0)
        q116 = self._col(df, "SEC_C_Q116", 0)
        q152 = self._col(df, "SEC_C_Q152", 0)
        elec_inj.loc[(q38 == 1) & (q162 == 1)] = 1.0
        elec_inj.loc[(q76 == 1) & (q162 == 2)] = 1.0
        elec_inj.loc[(q98 == 1) & (q162 == 3)] = 1.0
        elec_inj.loc[(q116 == 1) & (q162 == 7)] = 1.0
        elec_inj.loc[(q152 == 1) & q162.isin([4, 5, 6])] = 1.0
        elec_inj.loc[q162.isin([8, 111])] = np.nan

        elc_sft = pd.Series(np.nan, index=df.index)
        elc_sft.loc[elec_inj == 1] = 3.0
        elc_sft.loc[elec_inj == 0] = 5.0
        df["elc_sft_tier"] = elc_sft

        # Affordability Tier (365 kWh < 5% HH exp)
        tariff_avg = getattr(self, "tariff_per_kwh", 2.7072)
        cost_365 = tariff_avg * 365.0
        share_365 = cost_365 / df["exp_total_yr"].clip(lower=1.0)
        elc_affrd = pd.Series(5.0, index=df.index)
        elc_affrd.loc[share_365 >= 0.05] = 2.0
        df["elc_affrd_tier"] = elc_affrd

        # Adjusted tiers (non-grid/mini-grid defaulted to 5 to avoid penalizing off-grid)
        rel_adj = df["elc_rel_tier"].copy()
        rel_adj.loc[(~q162.isin([1, 2])) & rel_adj.isna()] = 5.0
        df["elc_rel_tier_adj"] = rel_adj

        qual_adj = df["elc_qual_tier"].copy()
        qual_adj.loc[(~q162.isin([1, 2])) & qual_adj.isna()] = 5.0
        df["elc_qual_tier_adj"] = qual_adj

        leg_adj = df["elc_leg_tier"].copy()
        leg_adj.loc[(~q162.isin([1, 2])) & leg_adj.isna()] = 5.0
        df["elc_leg_tier_adj"] = leg_adj

        # Aggregate Electricity Tier = min of all 7 attributes
        elc_attrs = ["elc_cap_tier", "elc_avbl_tier", "elc_rel_tier_adj", "elc_qual_tier_adj", "elc_affrd_tier", "elc_leg_tier_adj", "elc_sft_tier"]
        df["elc_aggr_tier"] = df[elc_attrs].min(axis=1)
        df["elec_access"] = np.where(df["elc_aggr_tier"].notna(), (df["elc_aggr_tier"] >= 1).astype(float), np.nan)
        df["elc_t45"] = np.where(df["elc_aggr_tier"].notna(), df["elc_aggr_tier"].isin([4, 5]).astype(float), np.nan)

        return df

    def _process_policy_and_barriers(self, df_base: pd.DataFrame) -> pd.DataFrame:
        """Under-the-grid spatial analytics, connection barriers, and WTP demand curves."""
        df = df_base.copy()

        # Under-the-Grid Analytics (clustered by Locality/EA name SEC_A_Q05 if available, else psu_id)
        if "SEC_A_Q05" in df.columns:
            df["ea_grid_present"] = df.groupby("SEC_A_Q05")["grid_hh"].transform("max")
        else:
            df["ea_grid_present"] = df.groupby("psu_id")["grid_hh"].transform("max")
        df["under_the_grid"] = (df["ea_grid_present"] == 1).astype(int)
        df["under_grid_unconnected"] = ((df["ea_grid_present"] == 1) & (df["grid_hh"] == 0)).astype(int)

        # Grid connection barriers (SEC_C_Q03)
        q03 = self._col(df, "SEC_C_Q03", np.nan)
        unconn = (df["grid_hh"] == 0) & q03.notna()
        df["barrier_cost"] = np.where(unconn, (q03 == 1).astype(float), np.nan)
        df["barrier_dist"] = np.where(unconn, (q03 == 2).astype(float), np.nan)
        df["barrier_tariff"] = np.where(unconn, (q03 == 3).astype(float), np.nan)
        df["barrier_landlord"] = np.where(unconn, (q03 == 4).astype(float), np.nan)
        df["barrier_unrel"] = np.where(unconn, (q03 == 5).astype(float), np.nan)
        df["barrier_admin"] = np.where(unconn, q03.isin([6, 7]).astype(float), np.nan)

        # WTP Grid (Contingent valuation bidding: Cumulative adoption demand curve)
        q_d3 = self._col(df, "SEC_D_Q03", np.nan)
        q_d4 = self._col(df, "SEC_D_Q04", np.nan)
        q_d5 = self._col(df, "SEC_D_Q05", np.nan)
        q_d6 = self._col(df, "SEC_D_Q06", np.nan)
        q_d7 = self._col(df, "SEC_D_Q07", np.nan)
        d_valid = (df["grid_hh"] == 0) & q_d3.notna()
        wtp_12m_cond = ((q_d3 == 1) | (q_d4 == 1) | (q_d5 == 1) | (q_d6 == 1))
        df["wtp_grid_upfront"] = np.where(d_valid, (q_d3 == 1).astype(float), np.nan)
        df["wtp_grid_3m"] = np.where(d_valid, ((q_d3 == 1) | (q_d4 == 1)).astype(float), np.nan)
        df["wtp_grid_6m"] = np.where(d_valid, ((q_d3 == 1) | (q_d4 == 1) | (q_d5 == 1)).astype(float), np.nan)
        df["wtp_grid_12m"] = np.where(d_valid, wtp_12m_cond.astype(float), np.nan)
        # Cumulative waived: connected at 12M or accepts 100% subsidy (Rule 6.5)
        df["wtp_grid_waived"] = np.where(d_valid, (wtp_12m_cond | (q_d7 == 1)).astype(float), np.nan)
        df["wtp_grid_never"] = np.where((df["grid_hh"] == 0) & q_d7.notna(), (q_d7 == 2).astype(float), np.nan)

        # Grid WTP by Randomized Price Point
        df = df.copy()
        rand_pct = self._col(df, "random_percentage", np.nan)
        for pct_val, p_code in [(0.14, "14"), (0.29, "29"), (0.43, "43"), (0.57, "57"), (0.71, "71"), (1.00, "100")]:
            mask_p = d_valid & (np.isclose(rand_pct, pct_val, atol=0.01))
            wtp_p_12m = ((q_d3 == 1) | (q_d4 == 1) | (q_d5 == 1) | (q_d6 == 1))
            df[f"wtp_grid_p{p_code}_upfront"] = np.where(mask_p, (q_d3 == 1).astype(float), np.nan)
            df[f"wtp_grid_p{p_code}_3m"] = np.where(mask_p, ((q_d3 == 1) | (q_d4 == 1)).astype(float), np.nan)
            df[f"wtp_grid_p{p_code}_6m"] = np.where(mask_p, ((q_d3 == 1) | (q_d4 == 1) | (q_d5 == 1)).astype(float), np.nan)
            df[f"wtp_grid_p{p_code}_12m"] = np.where(mask_p, wtp_p_12m.astype(float), np.nan)
            df[f"wtp_grid_p{p_code}_waived"] = np.where(mask_p, (wtp_p_12m | (q_d7 == 1)).astype(float), np.nan)
            df[f"wtp_grid_p{p_code}_never"] = np.where((df["grid_hh"] == 0) & (np.isclose(rand_pct, pct_val, atol=0.01)) & q_d7.notna(), (q_d7 == 2).astype(float), np.nan)

        # WTP Solar (Cumulative adoption demand curve)
        q_e2 = self._col(df, "SEC_E_Q02", np.nan)
        q_e3 = self._col(df, "SEC_E_Q03", np.nan)
        q_e4 = self._col(df, "SEC_E_Q04", np.nan)
        q_e5 = self._col(df, "SEC_E_Q05", np.nan)
        e_valid = q_e2.notna()
        df["wtp_solar_upfront"] = np.where(e_valid, (q_e2 == 1).astype(float), np.nan)
        df["wtp_solar_6m"] = np.where(e_valid, ((q_e2 == 1) | (q_e3 == 1)).astype(float), np.nan)
        df["wtp_solar_12m"] = np.where(e_valid, ((q_e2 == 1) | (q_e3 == 1) | (q_e4 == 1)).astype(float), np.nan)
        df["wtp_solar_24m"] = np.where(e_valid, ((q_e2 == 1) | (q_e3 == 1) | (q_e4 == 1) | (q_e5 == 1)).astype(float), np.nan)
        df["wtp_solar_never"] = np.where(q_e5.notna(), (q_e5 == 2).astype(float), np.nan)

        # Solar WTP by System Tier and Subsidy Level
        sys_col = self._col(df, "solar_system", np.nan)
        is_t1 = sys_col.isin([1, 1.0, "Tier 1", "1"])
        is_t2 = sys_col.isin([2, 2.0, "Tier 2", "2"])
        is_pooled = pd.Series(True, index=df.index)
        rand_pct_solar = self._col(df, "random_percentage_3", np.nan)

        for sys_code, sys_mask in [("t1", is_t1), ("t2", is_t2), ("pooled", is_pooled)]:
            for pct_val, p_code in [(0.33, "33"), (0.66, "66"), (1.00, "100")]:
                mask_sp = sys_mask & (np.isclose(rand_pct_solar, pct_val, atol=0.02)) & e_valid
                df[f"wtp_solar_{sys_code}_p{p_code}_upfront"] = np.where(mask_sp, (q_e2 == 1).astype(float), np.nan)
                df[f"wtp_solar_{sys_code}_p{p_code}_6m"] = np.where(mask_sp, ((q_e2 == 1) | (q_e3 == 1)).astype(float), np.nan)
                df[f"wtp_solar_{sys_code}_p{p_code}_12m"] = np.where(mask_sp, ((q_e2 == 1) | (q_e3 == 1) | (q_e4 == 1)).astype(float), np.nan)
                df[f"wtp_solar_{sys_code}_p{p_code}_24m"] = np.where(mask_sp, ((q_e2 == 1) | (q_e3 == 1) | (q_e4 == 1) | (q_e5 == 1)).astype(float), np.nan)
                df[f"wtp_solar_{sys_code}_p{p_code}_never"] = np.where(mask_sp & q_e5.notna(), ((q_e5 == 0) | (q_e5 == 2)).astype(float), np.nan)

        # WTP Cookstoves (Section K Contingent valuation bidding)
        q_k3 = self._col(df, "SEC_K_Q03", np.nan)
        q_k4 = self._col(df, "SEC_K_Q04", np.nan)
        q_k5 = self._col(df, "SEC_K_Q05", np.nan)
        q_k6 = self._col(df, "SEC_K_Q06", np.nan)
        q_k7 = self._col(df, "SEC_K_Q07", np.nan)
        k_valid = q_k3.notna()
        df["wtp_cook_upfront"] = np.where(k_valid, (q_k3 == 1).astype(float), np.nan)
        df["wtp_cook_3m"] = np.where(k_valid, ((q_k3 == 1) | (q_k4 == 1)).astype(float), np.nan)
        df["wtp_cook_6m"] = np.where(k_valid, ((q_k3 == 1) | (q_k4 == 1) | (q_k5 == 1)).astype(float), np.nan)
        df["wtp_cook_12m"] = np.where(k_valid, ((q_k3 == 1) | (q_k4 == 1) | (q_k5 == 1) | (q_k6 == 1)).astype(float), np.nan)
        df["wtp_cook_never"] = np.where(k_valid, ((q_k6 == 2) | q_k7.notna()).astype(float), np.nan)
        df["refuse_cook_cost"] = np.where(q_k7.notna(), (q_k7 == 1).astype(float), np.nan)

        # Refusal costs
        q_d8 = self._col(df, "SEC_D_Q08", np.nan)
        q_e6 = self._col(df, "SEC_E_Q06", np.nan)
        df["refuse_wiring_cost"] = np.where(q_d8.notna(), (q_d8 == 1).astype(float), np.nan)
        df["refuse_solar_cost"] = np.where(q_e6.notna(), (q_e6 == 1).astype(float), np.nan)

        return df

    def export_master(self, output_path: Optional[Path] = None) -> Path:
        """Saves the compiled dataframe to Stata .dta format (version 118)."""
        if self.df_master is None:
            self.build_all()

        if output_path is None:
            master_name = self.config.get("master_dta", "MTF_Master.dta")
            output_path = Path("Data") / master_name
        else:
            output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"[*] Exporting compiled MTF Master dataset to: {output_path.resolve()}...")
        self.df_master.to_stata(output_path, write_index=False, version=118)
        print(f"✓ Successfully wrote {len(self.df_master):,} rows and {len(self.df_master.columns):,} columns.")
        return output_path


def main():
    parser = argparse.ArgumentParser(description="World Bank ESMAP MTF End-to-End Master Dataset Builder.")
    parser.add_argument("--raw-dir", help="Directory containing raw Survey Solutions .dta files.")
    parser.add_argument("--config", help="Path to country_config.yaml.")
    parser.add_argument("--output", help="Target output .dta file path.")
    args = parser.parse_args()

    builder = MTFMasterBuilder(raw_dir=args.raw_dir, config_path=args.config)
    builder.build_all()
    out = builder.export_master(args.output)
    print(f"\n[DONE] Master dataset ready at: {out}")


if __name__ == "__main__":
    main()
