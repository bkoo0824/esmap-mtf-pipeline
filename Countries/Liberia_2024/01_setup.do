**************************************************************************
*  01_setup.do                                                           *
*  Liberia MTF Pipeline — Setup, Survey Design & Validation             *
**************************************************************************

use "$wip_hh/MTF_2024_HH_Liberia_Master.dta", clear
set more off

di "---------------------------------------------------------"
di " Validating Master Dataset: MTF_2024_HH_Liberia_Master.dta"
di " Total Observations: " _N
di "---------------------------------------------------------"

* Verify and declare survey design
svyset SEC_A_Q05 [pw=hh_wt], strata(strata_id) singleunit(centered)
svydescribe

* Quick diagnostic summary of core disaggregation variables
di "Disaggregation summary (weighted):"
svy: tabulate loc_urban_rural
svy: tabulate hh_head_gender
svy: tabulate hh_exp_quintile

save "$wip_hh/MTF_2024_HH_Liberia_Master.dta", replace
di " 01_setup.do complete — Master dataset validated."
