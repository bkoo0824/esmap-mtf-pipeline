**************************************************************************
*                                                                        *
*   World Bank ESMAP Multi-Tier Framework (MTF) Master Pipeline          *
*   title:  MTF_Master.do — End-to-End Econometric Orchestration         *
*   author: Bryan Koo / ESMAP Global Access Analytics Lead               *
*   organization: World Bank Group | Energy Global Practice              *
*                                                                        *
*   Purpose:                                                             *
*     1. Configures multi-OS file paths (Windows WBG OneDrive vs Linux)  *
*     2. Automatically executes the complete 7-stage analytical pipeline *
*     3. Exports official indicators, Word report, and 17 charts (300DPI)*
*                                                                        *
**************************************************************************

clear all
set more off
set maxvar 10000

*==============================================================================*
*  1. USER & MULTI-OS PATH CONFIGURATION                                       *
*==============================================================================*
* Note: ALWAYS use forward slashes (/) for all directory paths across OS platforms.

* Current directory auto-detection (if run from within the country or repo workspace)
local current_dir "`c(pwd)'"

if c(os) == "Windows" {
    * --- Bryan: Windows (WBG Headquarters / Country Office OneDrive) ---
    if c(username) == "WB453090" {
        global user "C:/Users/WB453090/OneDrive - WBG/1_mtf_energy_global_survey/9_Data analysis_MTF countries/37_Guinea-Bissau"
    }
    * --- Collaborators / Consultants (Windows OneDrive / Desktop fallback) ---
    else if inlist(lower(c(username)), "marina", "wb570814") {
        global user "C:/Users/`c(username)'/OneDrive - WBG/1_mtf_energy_global_survey/9_Data analysis_MTF countries/37_Guinea-Bissau"
    }
    else {
        * Auto-fallback to current workspace directory if local
        global user "`current_dir'"
    }
}
else if c(os) == "Unix" {
    * --- Bryan: Linux Ubuntu analytical workstation ---
    if c(username) == "bryan" {
        global user "/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/37_Guinea-Bissau"
    }
    else {
        global user "`current_dir'"
    }
}
else {
    global user "`current_dir'"
}

* Relative path overrides if user folder is the repo root
capture confirm file "$user/Data"
if _rc {
    capture confirm file "`current_dir'/Data"
    if !_rc global user "`current_dir'"
    else {
        capture confirm file "`current_dir'/../Data"
        if !_rc global user "`current_dir'/.."
    }
}

* Core Directory Structure
global raw_hh    "$user/Data"
global wip_hh    "$user/Data"
global clean     "$user/Data/clean"
global output    "$user/Output"
global out_sl    "$output"

* Locate Do-file scripts directory
global scripts   "$user/stata_pipeline/Do-file"
capture confirm file "$scripts/01_setup.do"
if _rc {
    capture confirm file "$user/Do-file/01_setup.do"
    if !_rc global scripts "$user/Do-file"
    else {
        capture confirm file "`current_dir'/01_setup.do"
        if !_rc global scripts "`current_dir'"
    }
}

* Locate Python visualization & report scripts directory
global py_scripts "$user/stata_pipeline/scripts"
capture confirm file "$py_scripts/visualize.py"
if _rc {
    capture confirm file "$user/Do-file/scripts/visualize.py"
    if !_rc global py_scripts "$user/Do-file/scripts"
    else {
        capture confirm file "$user/interactive_suite/visualize.py"
        if !_rc global py_scripts "$user/interactive_suite"
    }
}

* Ensure Output directories exist
capture mkdir "$output"
capture mkdir "$output/log"
capture mkdir "$output/charts"

*==============================================================================*
*  2. LOAD COUNTRY CONFIGURATION GLOBALS                                       *
*==============================================================================*
capture confirm file "$scripts/00_country_globals.do"
if !_rc {
    do "$scripts/00_country_globals.do"
}
else {
    * Default parameters if 00_country_globals.do is absent
    global country          "Guinea-Bissau"
    global country_iso3     "GNB"
    global survey_year      2024
    global master_dta       "MTF_2024_HH_Guinea-Bissau_Master.dta"
    global currency         "XOF"
    global usd_rate         605.0
    global lifeline_tariff  128.0
    global basic_kwh_bundle 365.0
}

* Toggles
global run_enhancements 1

*==============================================================================*
*  3. MASTER LOGGING INITIALIZATION                                            *
*==============================================================================*
capture log close master_log
local log_date : display %tdCCYYNNDD date(c(current_date), "DMY")
log using "$output/log/MTF_${country}_Master_`log_date'.log", name(master_log) text replace

di "========================================================================"
di "  World Bank ESMAP Multi-Tier Framework (MTF) Master Pipeline"
di "  Country:          $country ($country_iso3) - Wave $survey_year"
di "  Master Dataset:   $master_dta"
di "  Working Root:     $user"
di "  Do-File Scripts:  $scripts"
di "  Log File:         $output/log/MTF_${country}_Master_`log_date'.log"
di "  Started:          `c(current_date)' `c(current_time)'"
di "========================================================================"

*==============================================================================*
*  4. PIPELINE EXECUTION SEQUENCE                                              *
*==============================================================================*

* [Stage 0] Check whether Master Dataset exists; compile from raw modules if needed
capture confirm file "$raw_hh/$master_dta"
if _rc {
    di _newline
    di "--> [Stage 0/7] Compiling Master Dataset from 15 Raw CAPI Modules..."
    do "$scripts/00_build_master_dataset.do"
}
else {
    di _newline
    di "--> [Stage 0/7] Master dataset verified: $raw_hh/$master_dta (re-compilation skipped)."
}

* [Stage 0b] Country Harmonization & Verbatim Recoding (if present)
capture confirm file "$scripts/00_country_harmonization.do"
if !_rc {
    di "--> [Stage 0b/7] Running Country-Specific Text Recoding & Harmonization..."
    do "$scripts/00_country_harmonization.do"
}

* [Stage 1] Survey Setup & Stratified Design Validation
di _newline
di "--> [Stage 1/7] Survey Setup & Stratified Sampling Validation..."
do "$scripts/01_setup.do"

* [Stage 2] Electricity 7 Multi-Tier Attributes
di _newline
di "--> [Stage 2/7] Computing Electricity Multi-Tier Attributes (Capacity to Safety)..."
do "$scripts/02_elec_attributes.do"

* [Stage 3] Aggregate Electricity Multi-Tier Framework Index
di _newline
di "--> [Stage 3/7] Aggregating Overall Electricity Access Tier & Source Mix..."
do "$scripts/03_elec_aggregate.do"

* [Stage 4] Clean Cooking MECS Multi-Tier Attributes
di _newline
di "--> [Stage 4/7] Computing Cooking MECS Attributes (Exposure to Availability)..."
do "$scripts/04_cooking_attributes.do"

* [Stage 5] Aggregate Cooking Multi-Tier Index
di _newline
di "--> [Stage 5/7] Aggregating Overall Cooking Access Tier & Stove Typology..."
do "$scripts/05_cooking_aggregate.do"

* [Stage 6] Advanced Policy & Econometric Modules (WTP, Under-the-Grid, Stacking)
if $run_enhancements == 1 {
    di _newline
    di "--> [Stage 6/7] Computing Policy Modules: Under-the-Grid, Barriers, WTP, Gender..."
    do "$scripts/06_analytical_enhancements.do"
}

* [Stage 7] Putexcel Summary Tables & Econometric JSON Token Export
di _newline
di "--> [Stage 7/7] Exporting Econometric Indicator Tables & JSON..."
do "$scripts/07_export.do"

*==============================================================================*
*  5. AUTOMATED WORD REPORT & 17 PUBLICATION CHARTS (PYTHON SIDE-CAR)          *
*==============================================================================*
di _newline
di "========================================================================"
di "  [Optional / Automated] Publication Report & Graphics Generation"
di "========================================================================"

capture confirm file "$py_scripts/visualize.py"
if !_rc {
    di "--> Generating 17 High-Resolution Publication Charts (300 DPI)..."
    shell python "$py_scripts/visualize.py" --base-dir "$user"
}

capture confirm file "$py_scripts/inject_report.py"
if !_rc {
    di "--> Injecting Econometric Values into World Bank Word Report (.docx)..."
    shell python "$py_scripts/inject_report.py" --base-dir "$user"
}

di _newline
di "========================================================================"
di "  ESMAP MTF MASTER PIPELINE COMPLETED SUCCESSFULLY!"
di "  Output Folder:    $output"
di "  Full Excel:       $output/MTF_${country}_Summary.xlsx"
di "  Indicator JSON:   $output/mtf_report_values.json"
di "  Publication Doc:  $output/MTF_${country}_Report.docx"
di "  Finished:         `c(current_date)' `c(current_time)'"
di "========================================================================"

log close master_log
