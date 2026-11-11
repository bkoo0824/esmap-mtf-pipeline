**************************************************************************
*  00_country_harmonization.do                                           *
*  Country-Specific Harmonization & Dynamic Recodes: Guinea-Bissau        *
*  Auto-generated from: MTF_Guinea-Bissau_Calibration.xlsx                             *
**************************************************************************

di "===> Executing Country Harmonization Module: Guinea-Bissau"

* -------------------------------------------------------------------------
* 1. SPECIAL MISSING CODES CLEANING
* -------------------------------------------------------------------------
* Positive and negative missing codes declared: 888, 9, -888
local declared_missing 888, 9, -888
di " Cleaning declared missing codes across monetary variables..."
capture confirm variable SEC_C_Q25
if !_rc {
    replace SEC_C_Q25 = . if inlist(SEC_C_Q25, 888, 9, -888)
}
capture confirm variable grid_exp_m
if !_rc {
    replace grid_exp_m = . if inlist(grid_exp_m, 888, 9, -888)
}

* -------------------------------------------------------------------------
* 2. EDUCATION LEVEL HARMONIZATION (SEC_A1_Q8 -> hh_head_educ)
* -------------------------------------------------------------------------
capture drop hh_head_educ
gen byte hh_head_educ = .
* None (Category 0): codes 1, 555 or never attended school
replace hh_head_educ = 0 if inlist(SEC_A1_Q8, 1, 555) | SEC_A1_Q7 == 2 | SEC_A1_Q7 == 0
* Primary (Category 1): codes 2
replace hh_head_educ = 1 if inlist(SEC_A1_Q8, 2)
* Secondary (Category 2): codes 3, 4
replace hh_head_educ = 2 if inlist(SEC_A1_Q8, 3, 4)
* Higher Education (Category 3): codes 5, 6
replace hh_head_educ = 3 if inlist(SEC_A1_Q8, 5, 6)
label define hh_head_educ 0 "None" 1 "Primary" 2 "Secondary" 3 "Higher Education", replace
label values hh_head_educ hh_head_educ
label var hh_head_educ "Education Level of Household Head (MTF 4-Category Standard)"

* Defensive runtime assertion against silent failure
count if inlist(hh_head_educ, 2, 3)
if r(N) == 0 {
    di as error "[ERROR] Secondary/Higher education has 0 observations! Check SEC_A1_Q8 mapping."
    exit 198
}
else {
    di as text " [PASS] Education mapping verified: " r(N) " secondary/higher obs found."
}

* -------------------------------------------------------------------------
* 3. OPEN-ENDED 'OTHER, SPECIFY' RECODING & RECLASSIFICATION
* -------------------------------------------------------------------------
capture confirm variable SEC_G_Q05_oth
if !_rc {
    * Reclassify open-text charcoal braziers to Code 2 (Traditional Stove)
    capture replace SEC_G_Q05 = 2 if inlist(lower(trim(SEC_G_Q05_oth)), "fogareiro", "fugão a carvão", "fogareiro com carvão", "figareiro", "fogão de carvão", "fogadeiro", "construído com pesas de ferro para cozinhar", "fogadero")
    capture confirm variable trad_stove
    if !_rc {
        capture replace trad_stove = 1 if SEC_G_Q05 == 2
    }
}

capture confirm file "$wip_hh/cookstoves_clean.dta"
if !_rc {
    preserve
        use "$wip_hh/cookstoves_clean.dta", clear
        capture confirm variable SEC_G_Q05_oth
        if !_rc {
            capture replace SEC_G_Q05 = 2 if inlist(lower(trim(SEC_G_Q05_oth)), "fogareiro", "fugão a carvão", "fogareiro com carvão", "figareiro", "fogão de carvão", "fogadeiro", "construído com pesas de ferro para cozinhar", "fogadero")
        }
        save "$wip_hh/cookstoves_clean.dta", replace
    restore
}

capture confirm file "$wip_hh/mainstove_matched.dta"
if !_rc {
    preserve
        use "$wip_hh/mainstove_matched.dta", clear
        capture confirm variable SEC_G_Q05_oth
        if !_rc {
            capture replace SEC_G_Q05 = 2 if inlist(lower(trim(SEC_G_Q05_oth)), "fogareiro", "fugão a carvão", "fogareiro com carvão", "figareiro", "fogão de carvão", "fogadeiro", "construído com pesas de ferro para cozinhar", "fogadero")
        }
        save "$wip_hh/mainstove_matched.dta", replace
    restore
}

capture confirm variable SEC_C_Q125_oth
if !_rc {
    * Map open-text radio mentions to has_radio
    capture replace has_radio = 1 if inlist(lower(trim(SEC_C_Q125_oth)), "rádio")
}

* Persist harmonized changes to disk for subsequent modules
capture confirm file "$wip_hh/$master_dta"
if !_rc {
    save "$wip_hh/$master_dta", replace
    di " [SAVED] Harmonized changes committed to $wip_hh/$master_dta"
}

di "===> Country Harmonization Module for Guinea-Bissau complete."
