**************************************************************************
*  00_country_harmonization.do                                           *
*  Country-Specific Harmonization & Dynamic Recodes: Guinea-Bissau        *
*  Auto-calibrated from other_specify_calibration.xlsx                   *
**************************************************************************

di "===> Executing Country Harmonization Module: Guinea-Bissau"

* -------------------------------------------------------------------------
* 0. DYNAMIC CALIBRATION WORKBOOK VERIFICATION
* -------------------------------------------------------------------------
capture confirm file "$tools/other_specify_calibration.xlsx"
if !_rc {
    di " [CALIBRATION] Dynamic calibration workbook verified: $tools/other_specify_calibration.xlsx"
}

* -------------------------------------------------------------------------
* 1. SPECIAL MISSING CODES CLEANING
* -------------------------------------------------------------------------
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
* Cookstoves Typology (SEC_G_Q05_oth): Reclassify charcoal braziers to Code 2 (Traditional Stove)
capture confirm variable SEC_G_Q05_oth
if !_rc {
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

* Solar Device Roster Purpose (SEC_C_Q125_oth)
capture confirm variable SEC_C_Q125_oth
if !_rc {
    capture replace SEC_C_Q125 = 4 if inlist(lower(trim(SEC_C_Q125_oth)), "rádio", "radio")
    capture replace has_radio = 1 if inlist(lower(trim(SEC_C_Q125_oth)), "rádio", "radio")
}

* Fuel Purchase Frequency (SEC_I_Q07_oth): Map Portuguese "as need arises" to mode
capture confirm variable SEC_I_Q07_oth
if !_rc {
    capture replace SEC_I_Q07 = 6 if inlist(lower(trim(SEC_I_Q07_oth)), "de vez em quando", "depende de consumo", "depende de comsumo")
    capture replace SEC_I_Q07 = 3 if inlist(lower(trim(SEC_I_Q07_oth)), "a cada dois dias")
}

* Fuel Collection Frequency (SEC_I_Q13_oth): Map Portuguese responses
capture confirm variable SEC_I_Q13_oth
if !_rc {
    capture replace SEC_I_Q13 = 15 if inlist(lower(trim(SEC_I_Q13_oth)), "a cada dois dias")
    capture replace SEC_I_Q13 = 19 if inlist(lower(trim(SEC_I_Q13_oth)), "depende de consumo", "depende de comsumo", "algumas vezes no mês")
}

* -------------------------------------------------------------------------
* 4. DEFAULT MISSING TREATMENT & ATTRITION GUARDRAIL FOR UNCLASSIFIED 'OTHER'
* -------------------------------------------------------------------------
* Enforces Zero-Assumption Principle: unclassified 'Other' (555, 96) codes
* default to missing (.), with a 5% attrition alert threshold.

local target_vars SEC_G_Q05 SEC_C_Q02 SEC_C_Q40 SEC_C_Q78 SEC_C_Q100 SEC_I_Q07 SEC_I_Q13
foreach v of local target_vars {
    capture confirm variable `v'
    if !_rc {
        quietly count if inlist(`v', 555, 96)
        local unclass_n = r(N)
        quietly count if !missing(`v')
        local total_valid = r(N)
        if `total_valid' > 0 & `unclass_n' > 0 {
            local missing_pct = (`unclass_n' / `total_valid') * 100
            if `missing_pct' > 5.0 {
                di as error " [WARNING] High unclassified 'Other' rate in `v': " %4.1f `missing_pct' "% (N = `unclass_n'/`total_valid'). Review calibration sheet."
            }
            else {
                di as text " [DEFAULT] Recoding unclassified Other to missing in `v': N = `unclass_n' (" %4.1f `missing_pct' "%)"
            }
            replace `v' = . if inlist(`v', 555, 96)
        }
    }
}

capture confirm file "$wip_hh/cookstoves_clean.dta"
if !_rc {
    preserve
        use "$wip_hh/cookstoves_clean.dta", clear
        capture confirm variable SEC_G_Q05
        if !_rc {
            quietly count if inlist(SEC_G_Q05, 555, 96)
            if r(N) > 0 {
                local unclass_cs = r(N)
                quietly count if !missing(SEC_G_Q05)
                local total_cs = r(N)
                local cs_pct = (`unclass_cs' / `total_cs') * 100
                if `cs_pct' > 5.0 {
                    di as error " [WARNING] High unclassified Other in cookstoves_clean.dta: " %4.1f `cs_pct' "% (N = `unclass_cs'/`total_cs')."
                }
                else {
                    di as text " [DEFAULT] Recoding unclassified Other to missing in cookstoves_clean.dta: N = `unclass_cs' (" %4.1f `cs_pct' "%)"
                }
                replace SEC_G_Q05 = . if inlist(SEC_G_Q05, 555, 96)
                save "$wip_hh/cookstoves_clean.dta", replace
            }
        }
    restore
}

capture confirm file "$wip_hh/mainstove_matched.dta"
if !_rc {
    preserve
        use "$wip_hh/mainstove_matched.dta", clear
        capture confirm variable SEC_G_Q05
        if !_rc {
            quietly count if inlist(SEC_G_Q05, 555, 96)
            if r(N) > 0 {
                replace SEC_G_Q05 = . if inlist(SEC_G_Q05, 555, 96)
                save "$wip_hh/mainstove_matched.dta", replace
            }
        }
    restore
}

* Persist harmonized changes to disk
capture confirm file "$wip_hh/$master_dta"
if !_rc {
    save "$wip_hh/$master_dta", replace
    di " [SAVED] Harmonized changes committed to $wip_hh/$master_dta"
}
