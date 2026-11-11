**************************************************************************
*  01_setup.do                                                           *
*  Guinea-Bissau MTF Pipeline — Setup, Survey Design & Validation             *
**************************************************************************

use "$wip_hh/MTF_2024_HH_Guinea-Bissau_Master.dta", clear
set more off

di "---------------------------------------------------------"
di " Validating Master Dataset: MTF_2024_HH_Guinea-Bissau_Master.dta"
di " Total Observations: " _N
di "---------------------------------------------------------"

* Verify and declare survey design
capture confirm numeric variable SEC_A_Q06
if _rc != 0 {
    capture drop psu_id
    egen psu_id = group(SEC_A_Q06)
    lab var psu_id "Primary Sampling Unit (Numeric EA ID)"
    local psu_use "psu_id"
}
else {
    local psu_use "SEC_A_Q06"
}
svyset `psu_use' [pw=hh_wt], strata(strata_id) singleunit(centered)
svydescribe

* Quick diagnostic summary of core disaggregation variables
di "Disaggregation summary (weighted):"
svy: tabulate loc_urban_rural
svy: tabulate hh_head_gender
svy: tabulate hh_exp_quintile

save "$wip_hh/MTF_2024_HH_Guinea-Bissau_Master.dta", replace
di " 01_setup.do complete — Master dataset validated."
