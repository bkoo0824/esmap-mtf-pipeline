
	**************************************************************************
	*                                                                        *
	*   title:  Liberia MTF Master Pipeline — Automated Indicator Suite      *
	*   author: Bryan Koo / Gouthami (source: Liberia_electricityANDcooking.do)  *
	*   date:   Sep 2026                                                     *
	*   note:   Generates all MTF indicators + disaggregated exports         *
	*           Sources: Electricity (7 attr) + Cooking MECS (6 attr)       *
	*                                                                        *
	*   Sub-scripts:                                                         *
	*     01_setup.do              — weights, strata, demographics           *
	*     02_elec_attributes.do   — 7 electricity attribute tiers           *
	*     03_elec_aggregate.do    — aggregate electricity tier               *
	*     04_cooking_attributes.do — 6 MECS cooking attribute tiers         *
	*     05_cooking_aggregate.do — aggregate cooking tier                  *
	*     06_analytical_enhancements.do — "So What?" analytics (toggle)     *
	*     07_export.do            — svy:tabulate + putexcel + JSON           *
	*                                                                        *
	*   Output:                                                              *
	*     $output/streamlined/MTF_Liberia_Summary.xlsx  (5-sheet workbook)  *
	*     $output/streamlined/mtf_report_values.json    (placeholder values) *
	*                                                                        *
	*   Easy Lookup: Ctrl+F                                                  *
	*     - Setup:   jumptosetup                                             *
	*     - Run:     jumptomain                                              *
	**************************************************************************


*======================    1. USER & PATH SETUP   ============================*
																// jumptosetup

*======================    1. USER & PATH SETUP   ============================*

* --- Bryan: Linux (local machine) ---
if c(username)=="bryan" {
    global user "/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/35_Liberia(2024)/06. Data Analysis"
}

* --- Bryan: Windows (WBG OneDrive) ---
if c(username)=="WB453090" {
    global user "C:\Users\WB453090\OneDrive - WBG\1_mtf_energy_global_survey\9_Data analysis_MTF countries\35_Liberia(2024)\06. Data Analysis"
}

* Common folder paths
global raw_hh    "/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/35_Liberia(2024)/05. Data/Survey/Clean Data/Household"
global wip_hh    "$user/Data/wip"
global clean     "$user/Data/clean"
global output    "$user/Output"
global scripts   "$user/Do-file"
global out_sl    "$output"

*======================    2. GLOBAL TOGGLES   ================================*

* Set to 1 to run the 4 analytical enhancement blocks, 0 to skip
	global run_enhancements 1

* Survey design: Stratification = Region (SEC_A_Q01) × Locality (SEC_A_Q03)
*   PSU = EA number (SEC_A_Q05)
*   Note: svyset is declared in 01_setup.do after hh_wt is constructed


*======================    3. MAIN RUN   =====================================*
																// jumptomain
	clear all
	set more off
	set maxvar 10000

	di "========================================================"
	di " MTF Liberia Master Pipeline — $(c(current_date))"
	di "========================================================"

	di " [0/7] Master dataset compilation: raw modules & expenditure..."
	do "$scripts/00_build_master_dataset.do"

	di " [1/7] Setup & survey design validation..."
	do "$scripts/01_setup.do"

	di " [2/7] Electricity attribute tiers (capacity → safety)..."
	do "$scripts/02_elec_attributes.do"

	di " [3/7] Aggregate electricity tier + technology type..."
	do "$scripts/03_elec_aggregate.do"

	di " [4/7] Cooking MECS attribute tiers (exposure → availability)..."
	do "$scripts/04_cooking_attributes.do"

	di " [5/7] Aggregate MECS cooking tier + stove type..."
	do "$scripts/05_cooking_aggregate.do"

	if $run_enhancements == 1 {
		di " [6/7] Analytical enhancements (deficit gap, stacking, time use)..."
		do "$scripts/06_analytical_enhancements.do"
	}
	else {
		di " [6/7] Skipping analytical enhancements (run_enhancements = 0)"
	}

	di " [7/7] Export: svy:tabulate → putexcel → JSON..."
	do "$scripts/07_export.do"

	di "========================================================"
	di " Pipeline complete. Outputs in: $out_sl"
	di "========================================================"
