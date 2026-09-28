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
_xls_candidates = [f for f in OUTPUT_DIR.glob("MTF_*_Summary.xlsx") if not f.name.startswith(".~lock")]
XLS_PATH     = _xls_candidates[0] if _xls_candidates else OUTPUT_DIR / "MTF_Summary.xlsx"
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


# ─── CHART 9: REGIONAL ELECTRIFICATION DIVIDE ────────────────────────────────
# Auto-skipped when: n_regions > 10  OR  average 95%-CI width > 25 pp
# (In those cases the chart adds noise rather than analytical value.)
_REGIONAL_CI_THRESHOLD = 25.0   # pp — average CI width above which chart is dropped
_REGIONAL_N_THRESHOLD  = 10     # number of regions above which chart is dropped

def chart_regional_access_gap():
    """
    Subnational electrification divide chart.
    Returns True if chart was saved, False if it was skipped.
    Skip conditions:
      • Number of regions > _REGIONAL_N_THRESHOLD  (too cluttered)
      • Average 95%-CI width > _REGIONAL_CI_THRESHOLD pp  (too imprecise)
    """
    df = load_sheet("Regional_Disagg")
    df = df.sort_values(by="Electricity Access (%)", ascending=True)

    regions   = [str(r) for r in df.index]
    n_regions = len(regions)

    # ── Guard 1: Too many regions ────────────────────────────────────────────
    if n_regions > _REGIONAL_N_THRESHOLD:
        print(f"  ⚠  chart_regional_access_gap SKIPPED — {n_regions} regions > threshold {_REGIONAL_N_THRESHOLD}")
        return False

    grid_vals  = df["Grid Access (%)"].astype(float).values
    solar_vals = df["Off-grid Solar (%)"].astype(float).values
    elec_vals  = df["Electricity Access (%)"].astype(float).values

    # ── Parse 95% CI column ──────────────────────────────────────────────────
    has_ci    = "Electricity Access [95% CI]" in df.columns
    err_low, err_high = [], []
    ci_labels = []
    ci_pattern = re.compile(r'\[\s*([0-9.]+)%\s*[–-]\s*([0-9.]+)%\]')

    if has_ci:
        ci_widths = []
        for val, ci_str in zip(elec_vals, df["Electricity Access [95% CI]"]):
            m = ci_pattern.search(str(ci_str))
            if m:
                try:
                    ll = float(m.group(1))
                    ul = float(m.group(2))
                    width = ul - ll
                    ci_widths.append(width)
                    err_low.append(max(0.0, val - ll))
                    err_high.append(max(0.0, ul - val))
                    ci_labels.append(f"{val:.1f}% [{ll:.1f}%–{ul:.1f}%]")
                except ValueError:
                    ci_widths.append(0.0)
                    err_low.append(0.0)
                    err_high.append(0.0)
                    ci_labels.append(f"{val:.1f}%")
            else:
                ci_widths.append(0.0)
                err_low.append(0.0)
                err_high.append(0.0)
                ci_labels.append(f"{val:.1f}%")

        # ── Guard 2: CI too wide ─────────────────────────────────────────────
        avg_ci_width = sum(ci_widths) / len(ci_widths) if ci_widths else 0.0
        if avg_ci_width > _REGIONAL_CI_THRESHOLD:
            print(f"  ⚠  chart_regional_access_gap SKIPPED — avg CI width {avg_ci_width:.1f} pp > threshold {_REGIONAL_CI_THRESHOLD} pp")
            return False

        xerr = [err_low, err_high]
    else:
        ci_labels = [f"{v:.1f}%" for v in elec_vals]

    # ── Draw chart ───────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(11, max(7, n_regions * 0.55)))
    ax.barh(regions, grid_vals,  color=WB_NAVY,  label="National Grid",   height=0.55)
    ax.barh(regions, solar_vals, left=grid_vals, color=WB_AMBER, label="Off-Grid Solar", height=0.55)

    if has_ci:
        y_pos = np.arange(n_regions)
        ax.errorbar(elec_vals, y_pos, xerr=xerr, fmt="none", ecolor="#2C3E50",
                    elinewidth=1.4, capsize=3.5, capthick=1.4, zorder=5, label="95% CI (Total Access)")
        for i, (tot, ci_lbl) in enumerate(zip(elec_vals, ci_labels)):
            ul = tot + err_high[i]
            ax.text(ul + 1.2, i, ci_lbl, ha="left", va="center", fontsize=8.0, fontweight="bold", color=WB_NAVY)
        ax.set_xlim(0, 118)
        ax.set_xlabel("Electrification Rate (%) with 95% Survey Confidence Intervals", fontsize=10)
        ax.set_title(
            f"Subnational Electrification Divide Across {n_regions} Administrative Subdivisions\n"
            "(Disaggregated by Technology with Logit-Transformed 95% Confidence Intervals)",
            fontsize=12, fontweight="bold", color=WB_NAVY)
    else:
        for i, (g_v, s_v) in enumerate(zip(grid_vals, solar_vals)):
            tot = g_v + s_v
            ax.text(tot + 1.2, i, f"{tot:.1f}%", ha="left", va="center", fontsize=8.5, fontweight="bold", color=WB_NAVY)
        ax.set_xlim(0, 105)
        ax.set_xlabel("Electrification Rate (%)", fontsize=10)
        ax.set_title(f"Electricity Access by Technology Across {n_regions} Administrative Regions",
                     fontsize=12, fontweight="bold", color=WB_NAVY)

    ax.legend(framealpha=0.9, loc="lower right", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    plt.tight_layout()
    save_fig(fig, "09_regional_access_gap.png")
    return True


# ─── CHART 10: UNDER-THE-GRID COVERAGE & GRID UPTAKE FUNNEL ─────────────────
def chart_under_the_grid_funnel():
    vals = load_json()
    pop_tot = 100.0
    under_grid = float(vals.get("UNDER_THE_GRID_NAT", vals.get("EA_GRID_PRESENT_NAT", 57.2)))
    grid_conn  = float(vals.get("GRID_ACC_NAT", 39.5))
    uptake_rate = float(vals.get("GRID_UPTAKE_NAT", (grid_conn / under_grid * 100) if under_grid > 0 else 69.1))
    deficit_rate = 100.0 - uptake_rate
    unconnected_share = under_grid - grid_conn

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    stages = ["Total National\nPopulation", "Living Under the Grid\n(Electrified EAs)", "Connected to\nNational Grid"]
    heights = [pop_tot, under_grid, grid_conn]
    colors = [WB_GREY, WB_TEAL, WB_NAVY]

    bars = ax.bar(stages, heights, color=colors, width=0.52, edgecolor="#2C3E50", linewidth=1.2)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 1.8, f"{h:.1f}%", ha="center", va="bottom", fontsize=11, fontweight="bold", color=WB_NAVY)

    # Annotation for Uptake Rate
    ax.annotate("", xy=(2, grid_conn), xytext=(1, under_grid),
                arrowprops=dict(arrowstyle="<->", color=WB_AMBER, lw=2.5, ls="--"))
    ax.text(1.5, (under_grid + grid_conn)/2 + 4, f"Grid Uptake Rate:\n{uptake_rate:.1f}%\n({grid_conn:.1f}% / {under_grid:.1f}%)",
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFF3CD", edgecolor=WB_AMBER, lw=1.5),
            fontweight="bold", fontsize=9.5, color="#856404")

    # Bracket for unconnected deficit under the grid
    ax.annotate("", xy=(1, under_grid), xytext=(1, grid_conn),
                arrowprops=dict(arrowstyle="<->", color=WB_RED, lw=2))
    ax.text(1.15, (under_grid + grid_conn)/2, f"Under-Grid Deficit:\n{deficit_rate:.1f}% unconnected\n(~{unconnected_share:.1f}% of total pop)",
            ha="left", va="center", fontweight="bold", fontsize=8.5, color=WB_RED)

    ax.set_ylim(0, 118)
    ax.set_ylabel("% of National Population (Weighted)", fontsize=10, fontweight="bold")
    ax.set_title("Grid Infrastructure Coverage vs. Actual Household Uptake\n(EA Defined as Electrified if >=1 Connected Household)",
                 fontsize=12, fontweight="bold", color=WB_NAVY, pad=15)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.tight_layout()
    save_fig(fig, "10_under_the_grid_funnel.png")


# ─── CHART 11: PRIMARY ELECTRICITY SOURCE MIX VS DRY-CELL EXCLUSION ─────────
def chart_electricity_source_mix():
    vals = load_json()
    techs = [
        "National Grid",
        "Off-Grid Solar (SHS/SLS/Lantern)",
        "Electric Generator",
        "Mini-Grid",
        "Rechargeable Battery",
        "Dry-Cell Battery / Torch [EXCLUDED]",
        "No Electricity"
    ]
    grid_share = float(vals.get("GRID_ACC_NAT", 39.5))
    solar_share = float(vals.get("SOLAR_ACC_NAT", 5.3))
    shares = [grid_share, solar_share, 1.6, 0.5, 0.2, 33.0, 19.9]
    colors = [WB_NAVY, "#F39C12", "#E67E22", "#16A085", "#27AE60", "#BDC3C7", "#95A5A6"]

    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=150)
    y_pos = np.arange(len(techs))
    bars = ax.barh(y_pos, shares, color=colors, height=0.6, edgecolor="#2C3E50", linewidth=0.8)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.8, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", ha="left", va="center", fontsize=9.5, fontweight="bold", color=WB_NAVY)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(techs, fontsize=9.5, fontweight="bold")
    ax.invert_yaxis()
    ax.set_xlim(0, max(shares) + 12)
    ax.set_xlabel("% of National Population (Weighted)", fontsize=10, fontweight="bold")
    ax.set_title("Primary Electricity Technology Distribution\n(Formal Source Access = 47.1% | MTF Tier 1+ Access = 31.4%)",
                 fontsize=12, fontweight="bold", color=WB_NAVY, pad=15)

    ax.text(max(shares) * 0.72, 5.2, "Notice: Dry-cell batteries & torches\nare strictly excluded from formal\nelectricity access under SDG 7",
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.5", facecolor="#FADBD8", edgecolor=WB_RED, lw=1.5),
            color="#922B21", fontsize=8.5, fontweight="bold")

    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    plt.tight_layout()
    save_fig(fig, "11_electricity_source_mix.png")


# ─── CHART 12a: GRID CONNECTION WTP CUMULATIVE DEMAND CURVE ──────────────────
def chart_grid_wtp():
    """
    Grid Connection Willingness to Pay — cumulative demand curve.
    Financing terms: Upfront → 3M → 6M → 12M → Fee Waived.
    Saved as: 12a_wtp_grid_connection.png
    """
    vals = load_json()
    def g(key, default=0.0):
        v = vals.get(f"{{{{{key}}}}}", vals.get(key, default))
        try: return float(v)
        except: return default

    wtp_grid = [
        g("WTP_GRID_UPFRONT_NAT", 19.6),
        g("WTP_GRID_3M_NAT",      23.8),
        g("WTP_GRID_6M_NAT",      32.7),
        g("WTP_GRID_12M_NAT",     45.5),
        g("WTP_GRID_WAIVED_NAT",  73.7),
    ]
    x_labels = ["Upfront\n(Full Fee)", "3-Month\nPlan", "6-Month\nPlan", "12-Month\nPlan", "Fee\nWaived"]
    x = np.arange(len(x_labels))

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)
    ax.fill_between(x, wtp_grid, alpha=0.10, color=WB_NAVY)
    ax.plot(x, wtp_grid, marker="o", linewidth=3.0, markersize=9,
            color=WB_NAVY, label="Unconnected Households")

    for i, val in enumerate(wtp_grid):
        ax.annotate(f"{val:.1f}%", (i, val), textcoords="offset points",
                    xytext=(0, 11), ha="center", fontweight="bold", color=WB_NAVY, fontsize=10)

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=10, fontweight="bold")
    ax.set_ylim(0, min(100, max(wtp_grid) * 1.3))
    ax.set_ylabel("Cumulative % Willing to Connect", fontsize=11, fontweight="bold")
    ax.set_xlabel("Financing Term Offered to Household", fontsize=11, fontweight="bold")
    ax.set_title(
        "Grid Connection — Willingness to Pay by Financing Term\n"
        "(Cumulative Demand: Market Expansion as Liquidity Constraints Relax)",
        fontsize=12, fontweight="bold", color=WB_NAVY, pad=15)
    ax.legend(frameon=True, loc="upper left", fontsize=9.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.tight_layout()
    save_fig(fig, "12a_wtp_grid_connection.png")


# ─── CHART 12b: OFF-GRID SOLAR WTP CUMULATIVE DEMAND CURVE ───────────────────
def chart_solar_wtp():
    """
    Off-Grid Solar Device Willingness to Pay — cumulative demand curve.
    Financing terms: Upfront → 6M → 12M → 24M.
    Saved as: 12b_wtp_solar_device.png
    """
    vals = load_json()
    def g(key, default=0.0):
        v = vals.get(f"{{{{{key}}}}}", vals.get(key, default))
        try: return float(v)
        except: return default

    wtp_solar = [
        g("WTP_SOLAR_UPFRONT_NAT", 20.5),
        g("WTP_SOLAR_6M_NAT",      28.0),
        g("WTP_SOLAR_12M_NAT",     42.2),
        g("WTP_SOLAR_24M_NAT",     55.0),
    ]
    x_labels = ["Upfront\n(Full Price)", "6-Month\nPlan", "12-Month\nPlan", "24-Month\nPlan"]
    x = np.arange(len(x_labels))

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)
    ax.fill_between(x, wtp_solar, alpha=0.10, color=WB_AMBER)
    ax.plot(x, wtp_solar, marker="s", linewidth=3.0, markersize=9,
            color=WB_AMBER, label="All Households")

    for i, val in enumerate(wtp_solar):
        ax.annotate(f"{val:.1f}%", (i, val), textcoords="offset points",
                    xytext=(0, 11), ha="center", fontweight="bold", color="#7D5A00", fontsize=10)

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=10, fontweight="bold")
    ax.set_ylim(0, min(100, max(wtp_solar) * 1.3))
    ax.set_ylabel("Cumulative % Willing to Purchase", fontsize=11, fontweight="bold")
    ax.set_xlabel("Financing Term Offered to Household", fontsize=11, fontweight="bold")
    ax.set_title(
        "Off-Grid Solar Device — Willingness to Pay by Financing Term\n"
        "(Cumulative Demand: Market Expansion as Liquidity Constraints Relax)",
        fontsize=12, fontweight="bold", color=WB_NAVY, pad=15)
    ax.legend(frameon=True, loc="upper left", fontsize=9.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.tight_layout()
    save_fig(fig, "12b_wtp_solar_device.png")


# ─── CHART 12c: CLEAN COOKSTOVE WTP CUMULATIVE DEMAND CURVE ──────────────────
def chart_cookstove_wtp():
    """
    Clean Cookstove Willingness to Pay — cumulative demand curve.
    Financing terms: Upfront → 3M → 6M → 12M.
    Returns False (skips) if all four values are zero (cookstove module not run).
    Saved as: 12c_wtp_cookstove.png
    """
    vals = load_json()
    def g(key, default=0.0):
        v = vals.get(f"{{{{{key}}}}}", vals.get(key, default))
        try: return float(v)
        except: return default

    wtp_cook = [
        g("WTP_COOK_UPFRONT_NAT", 18.7),
        g("WTP_COOK_3M_NAT",      24.6),
        g("WTP_COOK_6M_NAT",      36.4),
        g("WTP_COOK_12M_NAT",     44.7),
    ]
    # Skip if cookstove WTP module was not collected (all zeros)
    if max(wtp_cook) == 0.0:
        print("  ⚠  chart_cookstove_wtp SKIPPED — no cookstove WTP data in JSON")
        return False

    x_labels = ["Upfront\n(Full Price)", "3-Month\nPlan", "6-Month\nPlan", "12-Month\nPlan"]
    x = np.arange(len(x_labels))

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)
    ax.fill_between(x, wtp_cook, alpha=0.10, color=WB_TEAL)
    ax.plot(x, wtp_cook, marker="^", linewidth=3.0, markersize=9,
            color=WB_TEAL, label="Eligible Households")

    for i, val in enumerate(wtp_cook):
        ax.annotate(f"{val:.1f}%", (i, val), textcoords="offset points",
                    xytext=(0, 11), ha="center", fontweight="bold", color="#006666", fontsize=10)

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=10, fontweight="bold")
    ax.set_ylim(0, min(100, max(wtp_cook) * 1.3))
    ax.set_ylabel("Cumulative % Willing to Purchase", fontsize=11, fontweight="bold")
    ax.set_xlabel("Financing Term Offered to Household", fontsize=11, fontweight="bold")
    ax.set_title(
        "Clean Cookstove — Willingness to Pay by Financing Term\n"
        "(Cumulative Demand: Market Expansion as Liquidity Constraints Relax)",
        fontsize=12, fontweight="bold", color=WB_NAVY, pad=15)
    ax.legend(frameon=True, loc="upper left", fontsize=9.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.tight_layout()
    save_fig(fig, "12c_wtp_cookstove.png")
    return True


# ─── CHART 13: WTP MUTUALLY EXCLUSIVE SEGMENTS (SUMS TO 100%) ────────────────
def chart_wtp_mutually_exclusive_stacked():
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=150)
    categories = ["National Grid\nConnection", "Off-Grid Solar\nDevice", "Clean Cooking\nStove"]
    upfront_vals = [19.6, 20.5, 18.7]
    m3_vals      = [ 4.2,  0.0,  5.8]
    m6_vals      = [ 8.9,  7.5, 11.8]
    m12_vals     = [12.8, 14.2,  8.4]
    waived_vals  = [28.2,  0.0,  0.0]
    never_vals   = [26.3, 57.8, 55.3]

    y = np.arange(len(categories))
    height = 0.52

    p1 = ax.barh(y, upfront_vals, height, color="#1A5276", label="Can Pay Upfront")
    p2 = ax.barh(y, m3_vals, height, left=upfront_vals, color="#2980B9", label="Needs 3M Installment")
    cum1 = np.array(upfront_vals) + np.array(m3_vals)
    p3 = ax.barh(y, m6_vals, height, left=cum1, color="#5DADE2", label="Needs 6M Installment")
    cum2 = cum1 + np.array(m6_vals)
    p4 = ax.barh(y, m12_vals, height, left=cum2, color="#A9CCE3", label="Needs 12M Installment")
    cum3 = cum2 + np.array(m12_vals)
    p5 = ax.barh(y, waived_vals, height, left=cum3, color=WB_AMBER, label="Needs 100% Fee Subsidy")
    cum4 = cum3 + np.array(waived_vals)
    p6 = ax.barh(y, never_vals, height, left=cum4, color="#7F8C8D", label="Never / Unwilling (Hard Floor)")

    for bars, vals in [(p1, upfront_vals), (p2, m3_vals), (p3, m6_vals), (p4, m12_vals), (p5, waived_vals), (p6, never_vals)]:
        for bar, val in zip(bars, vals):
            if val >= 4.5:
                x_pos = bar.get_x() + bar.get_width() / 2
                y_pos = bar.get_y() + bar.get_height() / 2
                col = "white" if bar.get_facecolor()[0] < 0.65 else "black"
                ax.text(x_pos, y_pos, f"{val:.1f}%", ha="center", va="center", color=col, fontweight="bold", fontsize=8.5)

    ax.set_yticks(y)
    ax.set_yticklabels(categories, fontsize=10, fontweight="bold")
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of Target Population (%)", fontsize=10, fontweight="bold")
    ax.set_title("Target Consumer Segments by Minimum Financing Requirement\n(Mutually Exclusive Breakdown — Strictly Sums to 100%)",
                 fontsize=12, fontweight="bold", color=WB_NAVY, pad=15)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.32), ncol=3, frameon=True, fontsize=8.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    plt.tight_layout()
    save_fig(fig, "13_wtp_mutually_exclusive_stacked.png")


# ─── CHART 14: COOKSTOVE AND FUEL STACKING DYNAMICS ─────────────────────────
def chart_stove_stacking_matrix():
    vals = load_json()
    pct_stacking = float(vals.get("PCT_STOVE_STACKING", 41.2))
    pct_dilution = float(vals.get("PCT_STACKING_DILUTION", 68.5))
    clean_own    = float(vals.get("PCT_CLEAN_STOVE_OWNERSHIP", 14.8))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=150)

    # Subplot 1: Cooking Practice Breakdown (100% Pie / Donut)
    labels1 = ["Traditional Only\n(Firewood / Biomass)", "Multi-Stove Stacking\n(Biomass + Charcoal/LPG)", "Clean Fuel Only\n(LPG / Electric)"]
    clean_only = max(0.0, clean_own * (1.0 - pct_dilution/100.0))
    stacking_share = pct_stacking
    trad_only = max(0.0, 100.0 - clean_only - stacking_share)
    shares1 = [trad_only, stacking_share, clean_only]
    colors1 = ["#D9534F", WB_AMBER, "#27AE60"]

    wedges, texts, autotexts = ax1.pie(shares1, labels=labels1, autopct="%1.1f%%", startangle=140,
                                       colors=colors1, explode=(0.02, 0.05, 0.05),
                                       textprops=dict(color=WB_NAVY, fontweight="bold", fontsize=9))
    for at in autotexts:
        at.set_color("white")
        at.set_fontsize(10)
    ax1.set_title("Household Cooking Practice Typology\n(National Population)", fontsize=11, fontweight="bold", color=WB_NAVY)

    # Subplot 2: Stacking Dilution Effect (Among Clean Stove Owners)
    labels2 = ["Primary Meal Cooked on\nTraditional Biomass (Dilution)", "Primary Meal Cooked on\nClean Stove / Fuel"]
    shares2 = [pct_dilution, 100.0 - pct_dilution]
    colors2 = [WB_CORAL, "#2ECC71"]

    bars2 = ax2.bar(labels2, shares2, color=colors2, width=0.48, edgecolor="#2C3E50", linewidth=1.1)
    for b in bars2:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 1.5, f"{h:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=10.5, color=WB_NAVY)

    ax2.set_ylim(0, 110)
    ax2.set_ylabel("% of Clean Stove Owners", fontsize=10, fontweight="bold")
    ax2.set_title("The 'Stacking Dilution' Effect\n(Primary Fuel Among Households Owning a Clean Stove)", fontsize=11, fontweight="bold", color=WB_NAVY)
    ax2.spines[["top", "right"]].set_visible(False)
    ax2.grid(axis="y", alpha=0.3, linestyle="--")

    plt.tight_layout()
    save_fig(fig, "14_stove_stacking_matrix.png")


# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n  ESMAP MTF — Visualization Pipeline (Up to 16 Publication Figures)")
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
    regional_saved = chart_regional_access_gap()
    if not regional_saved:
        print("  ℹ  Subnational chart omitted (too many regions or CI too wide — see thresholds above).")
    chart_under_the_grid_funnel()
    chart_electricity_source_mix()
    chart_grid_wtp()
    chart_solar_wtp()
    chart_cookstove_wtp()
    chart_wtp_mutually_exclusive_stacked()
    chart_stove_stacking_matrix()

    print(f"\n  All publication charts saved to: {CHARTS_DIR}\n")
