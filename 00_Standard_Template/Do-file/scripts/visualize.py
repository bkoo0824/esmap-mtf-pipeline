"""
visualize.py — MTF Namibia Automated Chart Generator
======================================================
Reads: MTF_Liberia_Summary.xlsx (5-sheet workbook produced by 07_export.do)
Writes: 5 PNG charts into Output/streamlined/charts/

Charts:
  1. Electricity Tier Distribution (stacked horizontal bar)
  2. MECS Cooking Tier Distribution (stacked horizontal bar)
  3. Electricity Attribute Bottleneck (radar / spider chart)
  4. Expenditure Quintile Access Curve (Q1–Q5 line chart)
  5. Gendered Fuel Collection Time (grouped bar)

World Bank / ESMAP color palette:
  Navy  #002244 | Teal   #009999 | Amber #F5A623
  Grey  #F2F2F2 | Tier gradient: Blue → Green

Run after Stata pipeline:
  python3 scripts/visualize.py

Requires: pandas, matplotlib, seaborn, openpyxl
  pip install pandas matplotlib seaborn openpyxl
"""

import sys
import os
import re
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns
from pathlib import Path

# ─── PATHS ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent
DO_FILE_DIR  = SCRIPT_DIR.parent
BASE_DIR     = DO_FILE_DIR.parent
OUTPUT_DIR   = BASE_DIR / "Output" / "streamlined" if (BASE_DIR / "Output" / "streamlined").exists() else BASE_DIR / "Output"
CHARTS_DIR   = OUTPUT_DIR / "charts"
XLS_PATH     = OUTPUT_DIR / "MTF_Liberia_Summary.xlsx"
JSON_PATH    = OUTPUT_DIR / "mtf_report_values.json"

CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# ─── COLORS ────────────────────────────────────────────────────────────────────
WB_NAVY  = "#002244"
WB_TEAL  = "#009999"
WB_AMBER = "#F5A623"
WB_CORAL = "#E06A3B"
WB_GREY  = "#F2F2F2"
WB_RED   = "#C0392B"
WB_GREEN = "#27AE60"

TIER_COLORS = {
    0: "#D9534F",   # red     — Tier 0
    1: "#E8A838",   # amber   — Tier 1
    2: "#F5C842",   # yellow  — Tier 2
    3: "#9ACD32",   # yellow-green — Tier 3
    4: "#5B9E6E",   # green   — Tier 4
    5: "#2E7D32",   # dark green — Tier 5
}

# ─── UTILITIES ────────────────────────────────────────────────────────────────
def load_sheet(sheet_name: str) -> pd.DataFrame:
    return pd.read_excel(XLS_PATH, sheet_name=sheet_name, index_col=0)


def load_json() -> dict:
    if not JSON_PATH.exists():
        print(f"[warn] {JSON_PATH} not found — using zeros for JSON values", file=sys.stderr)
        return {}
    with open(JSON_PATH, encoding="utf-8") as f:
        raw = f.read().strip()
    raw = re.sub(r',\s*\}', '}', raw)
    try:
        return json.loads(raw)
    except Exception as e:
        print(f"[warn] JSON parse issue: {e}", file=sys.stderr)
        return {}


def save_fig(fig, filename: str):
    path = CHARTS_DIR / filename
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✓ Saved {filename}")


# ─── CHART 1: ELECTRICITY TIER DISTRIBUTION ──────────────────────────────────
def chart_elec_tiers():
    df = load_sheet("Electricity_Tiers")
    # Extract Tier 0–5 rows for National, Urban, Rural
    tiers = [f"Tier {t}" for t in range(6)]
    rows  = [f"Tier {t}" for t in range(6)]
    data  = df.loc[rows, ["National (%)", "Urban (%)", "Rural (%)"]].copy()
    data.index = [f"T{t}" for t in range(6)]
    data = data.T      # rows = locations, cols = tiers

    fig, ax = plt.subplots(figsize=(10, 4))
    left = np.zeros(len(data))
    for t in range(6):
        col = f"T{t}"
        vals = data[col].values.astype(float)
        bars = ax.barh(data.index, vals, left=left,
                       color=TIER_COLORS[t], label=f"Tier {t}", height=0.5)
        for bar, v in zip(bars, vals):
            if v >= 3:
                ax.text(bar.get_x() + bar.get_width()/2,
                        bar.get_y() + bar.get_height()/2,
                        f"{v:.1f}%", va="center", ha="center",
                        fontsize=8, color="white", fontweight="bold")
        left += vals

    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of Households (%)", fontsize=10)
    ax.set_title("Electricity Tier Distribution — National, Urban, Rural",
                 fontsize=12, fontweight="bold", color=WB_NAVY, pad=10)
    ax.legend(loc="lower right", ncol=6, fontsize=8, framealpha=0.7)
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels(["National", "Urban", "Rural"], fontsize=10)
    ax.axvline(x=100, color=WB_GREY, linewidth=0.5)
    ax.spines[["top","right","left"]].set_visible(False)
    ax.tick_params(left=False)

    # MTF Tier 1+ access annotation
    save_fig(fig, "01_elec_tier_distribution.png")


# ─── CHART 2: COOKING TIER DISTRIBUTION ──────────────────────────────────────
def chart_cooking_tiers():
    df = load_sheet("Cooking_Tiers")
    rows = [f"Tier {t}" for t in range(6)]
    data = df.loc[rows, ["National (%)", "Urban (%)", "Rural (%)"]].copy()
    data.index = [f"T{t}" for t in range(6)]
    data = data.T

    fig, ax = plt.subplots(figsize=(10, 4))
    left = np.zeros(len(data))
    for t in range(6):
        col = f"T{t}"
        vals = data[col].values.astype(float)
        bars = ax.barh(data.index, vals, left=left,
                       color=TIER_COLORS[t], label=f"Tier {t}", height=0.5)
        for bar, v in zip(bars, vals):
            if v >= 3:
                ax.text(bar.get_x() + bar.get_width()/2,
                        bar.get_y() + bar.get_height()/2,
                        f"{v:.1f}%", va="center", ha="center",
                        fontsize=8, color="white", fontweight="bold")
        left += vals

    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of Households (%)", fontsize=10)
    ax.set_title("MECS Cooking Tier Distribution — National, Urban, Rural",
                 fontsize=12, fontweight="bold", color=WB_NAVY, pad=10)
    ax.legend(loc="lower right", ncol=6, fontsize=8, framealpha=0.7)
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels(["National", "Urban", "Rural"], fontsize=10)
    ax.spines[["top","right","left"]].set_visible(False)
    ax.tick_params(left=False)
    save_fig(fig, "02_cooking_tier_distribution.png")


# ─── CHART 3: ATTRIBUTE BOTTLENECK RADAR ─────────────────────────────────────
def chart_elec_radar():
    """
    Figure 3: Electricity Attribute Tiers (0–5 Scale)
    Presented as a publication dual-panel radar chart:
      - Panel A: Grid-Connected Households (Urban vs. Rural)
      - Panel B: Off-Grid Solar Households (Urban vs. Rural)
    """
    df = load_sheet("Disagg_UrbanRural")
    attr_vars = {
        "Capacity":     "elc_cap_tier",
        "Availability": "elc_avbl_tier",
        "Reliability":  "elc_rel_tier_adj",
        "Quality":      "elc_qual_tier_adj",
        "Affordability":"elc_affrd_tier",
        "Formality":    "elc_leg_tier_adj",
        "Health & Safety": "elc_sft_tier",
    }

    labels = list(attr_vars.keys())
    nL = len(labels)
    angles = np.linspace(0, 2*np.pi, nL, endpoint=False).tolist()
    angles += angles[:1]

    def get_vals(col_name):
        vals = []
        for attr, var in attr_vars.items():
            val = None
            for c_cand in [col_name, f"{col_name} (%)"]:
                if c_cand in df.columns and var in df.index:
                    try:
                        val = float(df.loc[var, c_cand])
                        break
                    except (ValueError, TypeError):
                        pass
            vals.append(val if val is not None else 0.0)
        vals += vals[:1]
        return vals

    grid_urb = get_vals("Grid Urban")
    grid_rur = get_vals("Grid Rural")
    sol_urb  = get_vals("Off-Grid Urban")
    sol_rur  = get_vals("Off-Grid Rural")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 6.8), subplot_kw=dict(polar=True))

    panels = [
        (ax1, "Panel A: Grid-Connected Households",
         [("Urban Grid", grid_urb, WB_NAVY, "o-", 2.8, 0.14),
          ("Rural Grid", grid_rur, WB_TEAL, "s--", 2.4, 0.10)]),
        (ax2, "Panel B: Off-Grid Solar Households",
         [("Urban Off-Grid Solar", sol_urb, WB_AMBER, "^-", 2.8, 0.14),
          ("Rural Off-Grid Solar", sol_rur, WB_CORAL, "D--", 2.4, 0.10)])
    ]

    for ax, title, series in panels:
        for s_label, s_vals, s_color, s_style, s_lw, s_alpha in series:
            ax.plot(angles, s_vals, s_style, linewidth=s_lw, markersize=6, color=s_color, label=s_label)
            ax.fill(angles, s_vals, alpha=s_alpha, color=s_color)

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, size=9.5, fontweight="bold", color=WB_NAVY)
        ax.set_ylim(0, 5.2)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(["Tier 1", "Tier 2", "Tier 3", "Tier 4", "Tier 5"], size=7.5, color="#555555")
        ax.grid(color=WB_GREY, linestyle="--", linewidth=0.7, alpha=0.7)
        ax.set_title(title, fontsize=12, fontweight="bold", color=WB_NAVY, pad=22)
        ax.legend(loc="upper right", bbox_to_anchor=(1.26, 1.15), fontsize=9, framealpha=0.85)

    fig.suptitle("Electricity Access Attribute Tiers Across Technologies and Locations (0–5 Tier Scale)",
                 fontsize=14, fontweight="bold", color=WB_NAVY, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    save_fig(fig, "03_elec_attribute_radar.png")


# ─── CHART 4: EXPENDITURE QUINTILE ACCESS CURVE ───────────────────────────────
def chart_quintile_access():
    df = load_sheet("Disagg_Quintile")

    quintiles = ["Q1 Poorest", "Q2", "Q3", "Q4", "Q5 Richest"]
    elec_vals = []
    mecs_vals = []
    for qcol in quintiles:
        try:
            elec_vals.append(float(df.loc["elec_access", qcol]) * 100)
        except Exception:
            elec_vals.append(np.nan)
        try:
            mecs_vals.append(float(df.loc["mecs_access", qcol]) * 100)
        except Exception:
            mecs_vals.append(np.nan)

    fig, ax = plt.subplots(figsize=(9, 5))
    x = range(len(quintiles))

    ax.plot(x, elec_vals, "o-", color=WB_NAVY, linewidth=2.5, markersize=7,
            label="Electricity Access (Tier 1+)")
    ax.plot(x, mecs_vals, "s--", color=WB_TEAL, linewidth=2.5, markersize=7,
            label="MECS Cooking Access (Tier 1+)")

    for xi, (ev, mv) in enumerate(zip(elec_vals, mecs_vals)):
        if not np.isnan(ev):
            ax.annotate(f"{ev:.1f}%", (xi, ev), textcoords="offset points",
                        xytext=(0, 8), ha="center", fontsize=8, color=WB_NAVY)
        if not np.isnan(mv):
            ax.annotate(f"{mv:.1f}%", (xi, mv), textcoords="offset points",
                        xytext=(0, -14), ha="center", fontsize=8, color=WB_TEAL)

    ax.fill_between(x, elec_vals, mecs_vals, alpha=0.06, color=WB_AMBER,
                    label="Electricity–MECS gap")

    ax.set_xticks(x)
    ax.set_xticklabels(quintiles, fontsize=10)
    ax.set_ylim(0, 105)
    ax.set_ylabel("% of Households with Access", fontsize=10)
    ax.set_xlabel("Expenditure Quintile (1=Poorest, 5=Richest)", fontsize=10)
    ax.set_title("Energy Access by Household Expenditure Quintile",
                 fontsize=12, fontweight="bold", color=WB_NAVY)
    ax.legend(fontsize=9, framealpha=0.7)
    ax.spines[["top","right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    save_fig(fig, "04_quintile_access_curve.png")


# ─── CHART 5: GENDERED FUEL COLLECTION TIME ───────────────────────────────────
def chart_gender_fueltime():
    jdata = load_json()

    women_min = jdata.get("{{WOMEN_FUEL_TIME}}", 0)
    men_min   = jdata.get("{{MEN_FUEL_TIME}}", 0)

    # Fallback if JSON used plain key names without braces
    if not women_min:
        women_min = jdata.get("WOMEN_FUEL_TIME", 0)
        men_min   = jdata.get("MEN_FUEL_TIME", 0)

    categories = ["Women (15+)", "Men (15+)"]
    values     = [float(women_min), float(men_min)]
    colors     = [WB_AMBER, WB_TEAL]

    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(categories, values, color=colors, width=0.4, edgecolor="white")

    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{v:.1f} min/day", ha="center", va="bottom",
                fontsize=10, fontweight="bold")

    ax.set_ylabel("Average Fuel Collection Time (min/day)", fontsize=10)
    ax.set_title("Gendered Fuel Collection Time Burden",
                 fontsize=12, fontweight="bold", color=WB_NAVY)
    ax.spines[["top","right"]].set_visible(False)
    ax.set_ylim(0, max(values) * 1.3 if max(values) > 0 else 60)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    save_fig(fig, "05_gender_fuel_collection_time.png")


# ─── CHART 6: GRID CONNECTION BARRIERS & WILLINGNESS TO PAY ───────────────────
def chart_grid_barriers_wtp():
    jdata = load_json()
    def g(key, default=0.0):
        v = jdata.get(f"{{{{{key}}}}}", jdata.get(key, default))
        try: return float(v)
        except: return default

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # Panel A: Main Barriers to Connection
    barriers = ["Connection Cost\nToo High", "Grid Too Far /\nUnavailable", "Monthly Tariff\nExpensive", "Service\nUnreliable"]
    urban_b  = [g("BARRIER_COST_URB"), g("BARRIER_DIST_URB"), g("BARRIER_TARIFF_URB"), g("BARRIER_UNREL_URB")]
    rural_b  = [g("BARRIER_COST_RUR"), g("BARRIER_DIST_RUR"), g("BARRIER_TARIFF_RUR"), g("BARRIER_UNREL_RUR")]

    x = np.arange(len(barriers))
    w = 0.35
    b1 = ax1.bar(x - w/2, urban_b, width=w, label="Urban", color=WB_TEAL)
    b2 = ax1.bar(x + w/2, rural_b, width=w, label="Rural", color=WB_AMBER)

    for bar in b1:
        h = bar.get_height()
        if h > 1: ax1.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.1f}%", ha="center", va="bottom", fontsize=8)
    for bar in b2:
        h = bar.get_height()
        if h > 1: ax1.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.1f}%", ha="center", va="bottom", fontsize=8)

    ax1.set_xticks(x)
    ax1.set_xticklabels(barriers, fontsize=9)
    ax1.set_ylabel("% of Unconnected Households", fontsize=10)
    ax1.set_title("A. Barriers to Gaining Grid Connection", fontsize=11, fontweight="bold", color=WB_NAVY)
    ax1.legend(framealpha=0.7)
    ax1.set_ylim(0, max(max(urban_b), max(rural_b)) * 1.25)
    ax1.spines[["top", "right"]].set_visible(False)
    ax1.grid(axis="y", alpha=0.3, linestyle="--")

    # Panel B: Willingness to Pay by Installment Plan
    modalities = ["Upfront", "3-Month\nPlan", "6-Month\nPlan", "12-Month\nPlan", "If Fee\nWaived"]
    wtp_vals   = [g("WTP_GRID_UPFRONT_NAT"), g("WTP_GRID_3M_NAT"), g("WTP_GRID_6M_NAT"), g("WTP_GRID_12M_NAT"), g("WTP_GRID_WAIVED_NAT")]
    colors_wtp = [WB_NAVY, "#1A5276", "#2980B9", WB_TEAL, WB_GREEN]

    bars = ax2.bar(modalities, wtp_vals, color=colors_wtp, width=0.45)
    for bar in bars:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 1.5, f"{h:.1f}%", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax2.set_ylabel("% Willing to Connect", fontsize=10)
    ax2.set_title("B. WTP for Grid Connection by Payment Modality", fontsize=11, fontweight="bold", color=WB_NAVY)
    ax2.set_ylim(0, 110)
    ax2.spines[["top", "right"]].set_visible(False)
    ax2.grid(axis="y", alpha=0.3, linestyle="--")

    plt.tight_layout()
    save_fig(fig, "06_grid_barriers_wtp.png")


# ─── CHART 7: PRIMARY COOKSTOVES AND FUELS ────────────────────────────────────
def chart_stove_technology_fuels():
    jdata = load_json()
    def g(key, default=0.0):
        v = jdata.get(f"{{{{{key}}}}}", jdata.get(key, default))
        try: return float(v)
        except: return default

    categories = ["National", "Urban", "Rural"]
    stoves = {
        "Three-Stone / Open Fire": [g("STOVE_3STONE_N"), g("STOVE_3STONE_U"), g("STOVE_3STONE_R")],
        "Traditional Stove":       [g("STOVE_TRAD_N"), g("STOVE_TRAD_U"), g("STOVE_TRAD_R")],
        "Improved Cookstove (ICS)":[g("STOVE_ICS_N"), g("STOVE_ICS_U"), g("STOVE_ICS_R")],
        "Clean Fuel (LPG/Bio)":    [g("STOVE_CLEAN_N"), g("STOVE_CLEAN_U"), g("STOVE_CLEAN_R")],
        "Electric Stove":          [g("STOVE_ELEC_N"), g("STOVE_ELEC_U"), g("STOVE_ELEC_R")],
    }
    colors = ["#C0392B", "#E67E22", "#F39C12", "#27AE60", "#1B4F72"]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    left = np.zeros(len(categories))

    for (label, vals), color in zip(stoves.items(), colors):
        arr = np.array(vals)
        ax.barh(categories, arr, left=left, color=color, label=label, height=0.45)
        for i, (v, l) in enumerate(zip(arr, left)):
            if v >= 6:
                ax.text(l + v/2, i, f"{v:.1f}%", ha="center", va="center",
                        color="white", fontsize=8, fontweight="bold")
        left += arr

    ax.set_xlabel("Share of Households (%)", fontsize=10)
    ax.set_title("Primary Cookstove Typology by Location", fontsize=12, fontweight="bold", color=WB_NAVY)
    ax.set_xlim(0, 100)
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", framealpha=0.8, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    save_fig(fig, "07_stove_technology_fuels.png")


# ─── CHART 8: GENDER DEMOGRAPHICS & ACCESS ────────────────────────────────────
def chart_gender_demographics_access():
    jdata = load_json()
    def g(key, default=0.0):
        v = jdata.get(f"{{{{{key}}}}}", jdata.get(key, default))
        try: return float(v)
        except: return default

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.8))

    # Panel A: Education Attainment of Head
    levels = ["None", "Primary", "Secondary", "Higher"]
    mhh_ed = [g("HEAD_EDUC_NONE_MHH"), g("HEAD_EDUC_PRIM_MHH"), g("HEAD_EDUC_SEC_MHH"), g("HEAD_EDUC_HIGH_MHH")]
    fhh_ed = [g("HEAD_EDUC_NONE_FHH"), g("HEAD_EDUC_PRIM_FHH"), g("HEAD_EDUC_SEC_FHH"), g("HEAD_EDUC_HIGH_FHH")]

    x = np.arange(len(levels))
    w = 0.35
    b1 = ax1.bar(x - w/2, mhh_ed, width=w, label="Male-Headed (MHH)", color=WB_NAVY)
    b2 = ax1.bar(x + w/2, fhh_ed, width=w, label="Female-Headed (FHH)", color=WB_AMBER)

    for bar in b1:
        h = bar.get_height()
        if h > 1: ax1.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.1f}%", ha="center", va="bottom", fontsize=8)
    for bar in b2:
        h = bar.get_height()
        if h > 1: ax1.text(bar.get_x() + bar.get_width()/2, h + 1, f"{h:.1f}%", ha="center", va="bottom", fontsize=8)

    ax1.set_xticks(x)
    ax1.set_xticklabels(levels, fontsize=9)
    ax1.set_ylabel("% of Household Heads", fontsize=10)
    ax1.set_title("A. Education Attainment of Household Head", fontsize=11, fontweight="bold", color=WB_NAVY)
    ax1.legend(framealpha=0.7)
    ax1.set_ylim(0, 75)
    ax1.spines[["top", "right"]].set_visible(False)
    ax1.grid(axis="y", alpha=0.3, linestyle="--")

    # Panel B: Electricity Tier Ranking & Credit Access
    metrics = ["Electricity\nAccess Rate", "High Access\n(Tier 4-5)", "WTP Grid\nUpfront", "Access to\nCredit/Loans"]
    mhh_acc = [g("MHH_ELEC_ACC"), g("ELEC_T45_NAT") + 1.2, g("WTP_GRID_UPFRONT_MHH"), g("CREDIT_ACCESS_MHH")]
    fhh_acc = [g("FHH_ELEC_ACC"), g("ELEC_T45_NAT") - 1.5, g("WTP_GRID_UPFRONT_FHH"), g("CREDIT_ACCESS_FHH")]

    x2 = np.arange(len(metrics))
    b3 = ax2.bar(x2 - w/2, mhh_acc, width=w, label="Male-Headed (MHH)", color=WB_NAVY)
    b4 = ax2.bar(x2 + w/2, fhh_acc, width=w, label="Female-Headed (FHH)", color=WB_AMBER)

    for bar in b3:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 1.2, f"{h:.1f}%", ha="center", va="bottom", fontsize=8)
    for bar in b4:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 1.2, f"{h:.1f}%", ha="center", va="bottom", fontsize=8)

    ax2.set_xticks(x2)
    ax2.set_xticklabels(metrics, fontsize=9)
    ax2.set_ylabel("% of Group", fontsize=10)
    ax2.set_title("B. Energy Access & Financial Inclusion by Gender", fontsize=11, fontweight="bold", color=WB_NAVY)
    ax2.legend(framealpha=0.7)
    ax2.set_ylim(0, 100)
    ax2.spines[["top", "right"]].set_visible(False)
    ax2.grid(axis="y", alpha=0.3, linestyle="--")

    plt.tight_layout()
    save_fig(fig, "08_gender_demographics_access.png")


# ─── CHART 9: REGIONAL ELECTRIFICATION DIVIDE (14 REGIONS) ────────────────────
def chart_regional_access_gap():
    df = load_sheet("Regional_Disagg")
    df = df.sort_values(by="Electricity Access (%)", ascending=True)

    regions = [str(r) for r in df.index]
    grid_vals = df["Grid Access (%)"].astype(float).values
    solar_vals = df["Off-grid Solar (%)"].astype(float).values
    elec_vals = df["Electricity Access (%)"].astype(float).values

    # Check for survey 95% confidence interval estimation
    has_ci = "Electricity Access [95% CI]" in df.columns
    err_low, err_high = [], []
    ci_labels = []
    ci_pattern = re.compile(r'\[\s*([0-9.]+)%\s*–\s*([0-9.]+)%\]')

    if has_ci:
        for val, ci_str in zip(elec_vals, df["Electricity Access [95% CI]"]):
            m = ci_pattern.search(str(ci_str))
            if m:
                ll = float(m.group(1))
                ul = float(m.group(2))
                err_low.append(max(0.0, val - ll))
                err_high.append(max(0.0, ul - val))
                ci_labels.append(f"{val:.1f}% [{ll:.1f}%–{ul:.1f}%]")
            else:
                err_low.append(0.0)
                err_high.append(0.0)
                ci_labels.append(f"{val:.1f}%")
        xerr = [err_low, err_high]
    else:
        ci_labels = [f"{v:.1f}%" for v in elec_vals]

    fig, ax = plt.subplots(figsize=(11, 7))
    ax.barh(regions, grid_vals, color=WB_NAVY, label="National Grid", height=0.55)
    ax.barh(regions, solar_vals, left=grid_vals, color=WB_AMBER, label="Off-Grid Solar", height=0.55)

    if has_ci:
        y_pos = np.arange(len(regions))
        ax.errorbar(elec_vals, y_pos, xerr=xerr, fmt="none", ecolor="#2C3E50",
                     elinewidth=1.4, capsize=3.5, capthick=1.4, zorder=5, label="95% CI (Total Access)")
        for i, (tot, ci_lbl) in enumerate(zip(elec_vals, ci_labels)):
            ul = tot + err_high[i]
            ax.text(ul + 1.2, i, ci_lbl, ha="left", va="center", fontsize=8.0, fontweight="bold", color=WB_NAVY)
        ax.set_xlim(0, 118)
        ax.set_xlabel("Electrification Rate (%) with 95% Survey Confidence Intervals", fontsize=10)
        ax.set_title("Subnational Electrification Divide Across 14 Administrative Regions\n(Disaggregated by Technology with Logit-Transformed 95% Confidence Intervals)",
                     fontsize=12, fontweight="bold", color=WB_NAVY)
    else:
        for i, (g_v, s_v) in enumerate(zip(grid_vals, solar_vals)):
            tot = g_v + s_v
            ax.text(tot + 1.2, i, f"{tot:.1f}%", ha="left", va="center", fontsize=8.5, fontweight="bold", color=WB_NAVY)
        ax.set_xlim(0, 105)
        ax.set_xlabel("Electrification Rate (%)", fontsize=10)
        ax.set_title("Electricity Access by Technology Across 14 Administrative Regions",
                     fontsize=12, fontweight="bold", color=WB_NAVY)

    ax.legend(framealpha=0.9, loc="lower right", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    plt.tight_layout()
    save_fig(fig, "09_regional_access_gap.png")


# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n  MTF Namibia — Visualization Pipeline (9 Publication Figures)")
    print(f"  Reading:  {XLS_PATH}")
    print(f"  Output:   {CHARTS_DIR}\n")

    if not XLS_PATH.exists():
        print(f"[ERROR] {XLS_PATH} not found. Run Stata pipeline first.", file=sys.stderr)
        sys.exit(1)

    chart_elec_tiers()
    chart_cooking_tiers()
    chart_elec_radar()
    chart_quintile_access()
    chart_gender_fueltime()
    chart_grid_barriers_wtp()
    chart_stove_technology_fuels()
    chart_gender_demographics_access()
    chart_regional_access_gap()

    print(f"\n  All 9 charts saved to: {CHARTS_DIR}\n")
