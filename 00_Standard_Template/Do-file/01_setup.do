	**************************************************************************
	*  01_setup.do                                                           *
	*  Namibia MTF Pipeline — Setup, Survey Design & Environment Validation *
	*                                                                        *
	*  Loads:    $wip_hh/$master_dta                    *
	*  Declares: svyset with Region × Locality stratification               *
	*  Verifies: Demographics, weights, quintiles, and essential variables  *
	**************************************************************************

	use "$wip_hh/$master_dta", clear
	set more off

	di "---------------------------------------------------------"
	di " Validating Master Dataset: $master_dta"
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

	di "Expenditure summary (N$):"
	summarize exp_total_yr exp_total_m [aw=hh_wt], detail

	save "$wip_hh/$master_dta", replace
	di " 01_setup.do complete — Master dataset validated."
