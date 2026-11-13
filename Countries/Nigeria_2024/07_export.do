
	**************************************************************************
	*  07_export.do                                                          *
	*  Namibia MTF Pipeline — Weighted Tables → Excel + JSON                *
	*                                                                        *
	*  Survey design: svyset already declared in 01_setup.do                *
	*  Output Excel: $out_sl/MTF_Nigeria_Summary.xlsx (5 sheets)            *
	*    Sheet 1: Electricity_Tiers    — National + Urban/Rural             *
	*    Sheet 2: Cooking_Tiers        — National + Urban/Rural             *
	*    Sheet 3: Disagg_UrbanRural    — All indicators × Urban/Rural       *
	*    Sheet 4: Disagg_Quintile      — All indicators × Q1–Q5             *
	*    Sheet 5: Disagg_Gender        — All indicators × MHH/FHH           *
	*  Output JSON: $out_sl/mtf_report_values.json (placeholder key-values) *
	**************************************************************************

	* Standalone fallback for paths
	if "$wip_hh" == "" {
		if c(username)=="bryan" {
			global user "/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/30_Namibia/Data Analysis"
		}
		if c(username)=="WB453090" {
			global user "C:\Users\WB453090\OneDrive - WBG\1_mtf_energy_global_survey\9_Data analysis_MTF countries\30_Namibia\Data Analysis"
		}
		if c(username)=="wb570814" {
			global user "C:\Users\wb570814\OneDrive - WBG\Desktop\MTF-desktop\Namibia\Data analysis"
		}
		global raw_hh    "$user/Data/household data/Household"
		global wip_hh    "$user/Data/wip_hh"
		global clean     "$user/Data/clean"
		global output    "$user/Output"
		global scripts   "$user/Do-file/streamlined"
		global out_sl    "$output/streamlined"
	}

	use "$wip_hh/$master_dta", clear
	set more off

	* Declare survey design (strata = Region × Locality, PSU = EA)
	svyset SEC_A_Q05 [pw=hh_wt], strata(strata_id) singleunit(centered)

	* Output path
	local xls "$out_sl/MTF_Nigeria_Summary.xlsx"
	local json_out "$out_sl/mtf_report_values.json"

	*===========================================================================
	*  HELPER MACRO: Run svy:tabulate and store percent matrix
	*  Usage: svy_pct varname [subgroup_condition] matrix_name
	*===========================================================================

	* We store all computed scalars in a local list and write JSON at the end.
	* Each scalar is named: json_PLACEHOLDER

	*===========================================================================
	*  SHEET 1: ELECTRICITY TIERS
	*===========================================================================

	putexcel set "`xls'", sheet("Electricity_Tiers") replace

	* Row headers
	putexcel A1 = "Electricity Tier"    B1 = "National (%)"  C1 = "Urban (%)"  D1 = "Rural (%)"
	forval t = 0/5 {
		putexcel A`=`t'+2' = "Tier `t'"
	}
	putexcel A8   = "Access (Tier 1+)"
	putexcel A9   = "High Access (Tier 4+)"
	putexcel A10  = "Grid Connected"
	putexcel A11  = "Off-grid Solar"

	forval t = 0/5 {
		capture drop elc_t`t'
		gen byte elc_t`t' = (elc_aggr_tier == `t') if elc_aggr_tier != .
	}
	capture drop elc_t45
	capture drop grid_hh
	capture drop solar_hh
	gen byte elc_t45 = (elc_aggr_tier >= 4) if elc_aggr_tier != .
	gen byte grid_hh  = (elec_tech_type == 1)
	gen byte solar_hh = inlist(elec_tech_type, 4, 5, 6)

	* National
	svy: mean elc_t0 elc_t1 elc_t2 elc_t3 elc_t4 elc_t5 elec_access elc_t45 grid_hh solar_hh
	forval t = 0/5 {
		local val = e(b)[1, `t'+1] * 100
		putexcel B`=`t'+2' = `val'
		scalar json_ELEC_T`t'_NAT = `val'
	}
	putexcel B8  = (e(b)[1,7] * 100)
	putexcel B9  = (e(b)[1,8] * 100)
	putexcel B10 = (e(b)[1,9] * 100)
	putexcel B11 = (e(b)[1,10] * 100)
	scalar json_ELEC_ACC_NAT  = e(b)[1,7] * 100
	scalar json_ELEC_T45_NAT  = e(b)[1,8] * 100
	scalar json_GRID_ACC_NAT  = e(b)[1,9] * 100
	scalar json_SOLAR_ACC_NAT = e(b)[1,10] * 100

	* Urban
	svy, subpop(if loc_urban_rural == 1): mean elc_t0 elc_t1 elc_t2 elc_t3 elc_t4 elc_t5 elec_access elc_t45 grid_hh solar_hh
	forval t = 0/5 {
		local val = e(b)[1, `t'+1] * 100
		putexcel C`=`t'+2' = `val'
		scalar json_ELEC_T`t'_URB = `val'
	}
	putexcel C8  = (e(b)[1,7] * 100)
	putexcel C9  = (e(b)[1,8] * 100)
	putexcel C10 = (e(b)[1,9] * 100)
	putexcel C11 = (e(b)[1,10] * 100)
	scalar json_ELEC_ACC_URB  = e(b)[1,7] * 100
	scalar json_ELEC_T45_URB  = e(b)[1,8] * 100
	scalar json_GRID_ACC_URB  = e(b)[1,9] * 100
	scalar json_SOLAR_ACC_URB = e(b)[1,10] * 100

	* Rural
	svy, subpop(if loc_urban_rural == 2): mean elc_t0 elc_t1 elc_t2 elc_t3 elc_t4 elc_t5 elec_access elc_t45 grid_hh solar_hh
	forval t = 0/5 {
		local val = e(b)[1, `t'+1] * 100
		putexcel D`=`t'+2' = `val'
		scalar json_ELEC_T`t'_RUR = `val'
	}
	putexcel D8  = (e(b)[1,7] * 100)
	putexcel D9  = (e(b)[1,8] * 100)
	putexcel D10 = (e(b)[1,9] * 100)
	putexcel D11 = (e(b)[1,10] * 100)
	scalar json_ELEC_ACC_RUR  = e(b)[1,7] * 100
	scalar json_ELEC_T45_RUR  = e(b)[1,8] * 100
	scalar json_GRID_ACC_RUR  = e(b)[1,9] * 100
	scalar json_SOLAR_ACC_RUR = e(b)[1,10] * 100

	putexcel save


	*===========================================================================
	*  SHEET 2: COOKING TIERS
	*===========================================================================

	putexcel set "`xls'", sheet("Cooking_Tiers") modify

	putexcel A1 = "Cooking MECS Tier"  B1 = "National (%)"  C1 = "Urban (%)"  D1 = "Rural (%)"
	forval t = 0/5 {
		putexcel A`=`t'+2' = "Tier `t'"
	}
	putexcel A8  = "MECS Access (Tier 1+)"
	putexcel A9  = "MECS Modern (Tier 4–5)"
	putexcel A10 = "MECS Transitional (Tier 2–3)"
	putexcel A11 = "Three-stone / Open Fire"
	putexcel A12 = "Clean Fuel Stove (LPG/Elec)"

	forval t = 0/5 {
		capture drop cs_t`t'
		gen byte cs_t`t' = (cs_aggr_tier == `t') if cs_aggr_tier != .
	}
	capture drop threestone_hh cleanstove_hh
	gen byte threestone_hh = inlist(mainstove, 1, 2)
	gen byte cleanstove_hh = inlist(mainstove, 4, 5, 6, 7, 8)

	foreach loc in NAT URB RUR {
		if "`loc'" == "NAT" local cond ""
		if "`loc'" == "URB" local cond "subpop(if loc_urban_rural == 1)"
		if "`loc'" == "RUR" local cond "subpop(if loc_urban_rural == 2)"
		local col = cond("`loc'" == "NAT", "B", cond("`loc'" == "URB", "C", "D"))

		if "`cond'" == "" svy: mean cs_t0 cs_t1 cs_t2 cs_t3 cs_t4 cs_t5 mecs_access mecs_modern mecs_trans threestone_hh cleanstove_hh
		else svy, `cond': mean cs_t0 cs_t1 cs_t2 cs_t3 cs_t4 cs_t5 mecs_access mecs_modern mecs_trans threestone_hh cleanstove_hh

		forval t = 0/5 {
			local val = e(b)[1, `t'+1] * 100
			putexcel `col'`=`t'+2' = `val'
			scalar json_COOK_T`t'_`loc' = `val'
		}
		putexcel `col'8  = (e(b)[1,7] * 100)
		putexcel `col'9  = (e(b)[1,8] * 100)
		putexcel `col'10 = (e(b)[1,9] * 100)
		putexcel `col'11 = (e(b)[1,10] * 100)
		putexcel `col'12 = (e(b)[1,11] * 100)

		scalar json_MECS_ACC_`loc'    = e(b)[1,7] * 100
		scalar json_MECS_MOD_`loc'    = e(b)[1,8] * 100
		scalar json_TRANS_COOK_`loc'  = e(b)[1,9] * 100
		scalar json_THREESTONE_`loc'  = e(b)[1,10] * 100
		scalar json_CLEAN_STOVE_`loc' = e(b)[1,11] * 100
	}

	putexcel save


	*===========================================================================
	*  SHEET 3: DISAGG_URBANRURAL — All indicators × Urban/Rural & Tech
	*===========================================================================

	putexcel set "`xls'", sheet("Disagg_UrbanRural") modify

	local row = 1
	putexcel A`row' = "Indicator" B`row' = "National" C`row' = "Urban" D`row' = "Rural" ///
		E`row' = "Grid Urban" F`row' = "Grid Rural" G`row' = "Off-Grid Urban" H`row' = "Off-Grid Rural"
	local row = 2

	foreach var in elec_access mecs_access mecs_modern mecs_trans ///
		grid_hh solar_hh elc_t45 threestone_hh cleanstove_hh ///
		elc_cap_tier elc_avbl_tier elc_rel_tier_adj elc_qual_tier_adj ///
		elc_affrd_tier elc_leg_tier_adj elc_sft_tier elc_aggr_tier ///
		cs_exp_tier cs_efcy_tier cs_conv_tier cs_sfty_tier cs_affd_tier cs_avbl_tier cs_aggr_tier {

		putexcel A`row' = "`var'"

		* Standard locations: National, Urban, Rural
		foreach loc in NAT URB RUR {
			if "`loc'" == "NAT" local cond ""
			if "`loc'" == "URB" local cond "subpop(if loc_urban_rural == 1)"
			if "`loc'" == "RUR" local cond "subpop(if loc_urban_rural == 2)"
			local col = cond("`loc'" == "NAT", "B", cond("`loc'" == "URB", "C", "D"))

			capture {
				if "`cond'" == "" svy: mean `var'
				else svy, `cond': mean `var'
				local val = e(b)[1,1]
				putexcel `col'`row' = `val'
			}
		}

		* Grid & Off-grid disaggregated by Urban/Rural
		* Col E: Grid Urban
		capture {
			svy, subpop(if grid_hh == 1 & loc_urban_rural == 1): mean `var'
			putexcel E`row' = (e(b)[1,1])
		}
		* Col F: Grid Rural
		capture {
			svy, subpop(if grid_hh == 1 & loc_urban_rural == 2): mean `var'
			putexcel F`row' = (e(b)[1,1])
		}
		* Col G: Off-Grid Urban
		capture {
			svy, subpop(if solar_hh == 1 & loc_urban_rural == 1): mean `var'
			putexcel G`row' = (e(b)[1,1])
		}
		* Col H: Off-Grid Rural
		capture {
			svy, subpop(if solar_hh == 1 & loc_urban_rural == 2): mean `var'
			putexcel H`row' = (e(b)[1,1])
		}

		local row = `row' + 1
	}
	putexcel save


	*===========================================================================
	*  SHEET 4: DISAGG_QUINTILE — All indicators × Q1–Q5
	*===========================================================================

	putexcel set "`xls'", sheet("Disagg_Quintile") modify

	local row = 1
	putexcel A`row' = "Indicator" B`row' = "Q1 Poorest" C`row' = "Q2" D`row' = "Q3" ///
		E`row' = "Q4" F`row' = "Q5 Richest"
	local row = 2

	foreach var in elec_access mecs_access mecs_modern elc_aggr_tier cs_aggr_tier ///
		grid_hh solar_hh threestone_hh cleanstove_hh elc_t45 ///
		elc_cap_tier elc_avbl_tier elc_affrd_tier cs_exp_tier cs_conv_tier cs_affd_tier {

		putexcel A`row' = "`var'"
		local cols "B C D E F"
		local q = 1
		foreach col of local cols {
			capture {
				svy, subpop(if hh_exp_quintile == `q'): mean `var'
				local val = e(b)[1,1]
				putexcel `col'`row' = `val'
				* Store key JSON values for electricity and MECS access by quintile
				if "`var'" == "elec_access" scalar json_Q`q'_ELEC_ACC = `val' * 100
				if "`var'" == "mecs_access"  scalar json_Q`q'_MECS_ACC  = `val' * 100
			}
			local q = `q' + 1
		}
		local row = `row' + 1
	}
	putexcel save


	*===========================================================================
	*  SHEET 5: DISAGG_GENDER — All indicators × MHH/FHH
	*===========================================================================

	putexcel set "`xls'", sheet("Disagg_Gender") modify

	local row = 1
	putexcel A`row' = "Indicator" B`row' = "Male HH Head (MHH)" C`row' = "Female HH Head (FHH)"
	local row = 2

	foreach var in elec_access mecs_access mecs_modern elc_aggr_tier cs_aggr_tier ///
		grid_hh solar_hh threestone_hh cleanstove_hh elc_t45 ///
		elc_cap_tier elc_avbl_tier elc_affrd_tier cs_exp_tier cs_conv_tier cs_affd_tier {

		putexcel A`row' = "`var'"
		local col = "B"
		forval g = 1/2 {
			capture {
				svy, subpop(if hh_head_gender == `g'): mean `var'
				local val = e(b)[1,1]
				putexcel `col'`row' = `val'
				if "`var'" == "elec_access" & `g'==1 scalar json_MHH_ELEC_ACC = `val' * 100
				if "`var'" == "elec_access" & `g'==2 scalar json_FHH_ELEC_ACC = `val' * 100
				if "`var'" == "mecs_access"  & `g'==1 scalar json_MHH_MECS_ACC  = `val' * 100
				if "`var'" == "mecs_access"  & `g'==2 scalar json_FHH_MECS_ACC  = `val' * 100
			}
			local col = "C"
		}
		local row = `row' + 1
	}
	putexcel save


	*===========================================================================
	*  ADDITIONAL JSON SCALARS: Time use + Analytical enhancements
	*===========================================================================

	* Gendered fuel collection time (minutes per day = weekly hrs × 60 / 7)
	svy: mean women_fuel_hr_yr_hh men_fuel_hr_yr_hh girls_fuel_hr_yr_hh boys_fuel_hr_yr_hh
	scalar json_WOMEN_FUEL_TIME = e(b)[1,1] / 52 / 7 * 60   // mean min/day
	scalar json_MEN_FUEL_TIME   = e(b)[1,2] / 52 / 7 * 60
	scalar json_WOMEN_FUEL_WORKDAYS = e(b)[1,1] / 8          // working days/yr

	* Stove stacking dilution %
	svy: mean stacking_dilution own_both_stoves
	scalar json_PCT_STOVE_STACKING = e(b)[1,2] * 100
	scalar json_PCT_STACKING_DILUTION = e(b)[1,1] * 100

	* Grid attribute deficits
	svy, subpop(if elec_tech_type == 1): ///
		mean deficit_cap deficit_avbl deficit_rel deficit_qual deficit_affrd deficit_leg deficit_sft
	scalar json_PCT_CAP_LIMITED   = e(b)[1,1] * 100
	scalar json_PCT_EVE_SHORTAGE  = e(b)[1,2] * 100

	* Solar lanterns stuck at Tier 1
	svy, subpop(if elec_tech_type == 6): mean sl_tier1_stuck
	scalar json_PCT_SL_STUCK_T1 = e(b)[1,1] * 100

	* Outage frequency for grid HHs
	svy, subpop(if elec_tech_type == 1): mean dis_frq
	scalar json_AVG_OUTAGES_PER_WEEK = e(b)[1,1]

	* Voltage damage %
	svy, subpop(if elec_tech_type == 1): mean deficit_qual
	scalar json_PCT_VOLTAGE_DAMAGE = e(b)[1,1] * 100

	* Clean stove ownership %
	svy: mean clean_stove
	scalar json_PCT_CLEAN_STOVE_OWNERSHIP = e(b)[1,1] * 100

	* Stove type disaggregations for Table 2
	capture drop stove_3stone
	capture drop stove_trad
	capture drop stove_ics
	capture drop stove_clean
	capture drop stove_elec
	gen byte stove_3stone = (mainstove == 1)
	gen byte stove_trad   = (mainstove == 2)
	gen byte stove_ics    = (mainstove == 3)
	gen byte stove_clean  = inlist(mainstove, 4, 6, 7, 8)
	gen byte stove_elec   = (mainstove == 5)

	svy: mean stove_3stone stove_trad stove_ics stove_clean stove_elec
	scalar json_STOVE_3STONE_N = e(b)[1,1] * 100
	scalar json_STOVE_TRAD_N   = e(b)[1,2] * 100
	scalar json_STOVE_ICS_N    = e(b)[1,3] * 100
	scalar json_STOVE_CLEAN_N  = e(b)[1,4] * 100
	scalar json_STOVE_ELEC_N   = e(b)[1,5] * 100

	svy, subpop(if loc_urban_rural == 1): mean stove_3stone stove_trad stove_ics stove_clean stove_elec
	scalar json_STOVE_3STONE_U = e(b)[1,1] * 100
	scalar json_STOVE_TRAD_U   = e(b)[1,2] * 100
	scalar json_STOVE_ICS_U    = e(b)[1,3] * 100
	scalar json_STOVE_CLEAN_U  = e(b)[1,4] * 100
	scalar json_STOVE_ELEC_U   = e(b)[1,5] * 100

	svy, subpop(if loc_urban_rural == 2): mean stove_3stone stove_trad stove_ics stove_clean stove_elec
	scalar json_STOVE_3STONE_R = e(b)[1,1] * 100
	scalar json_STOVE_TRAD_R   = e(b)[1,2] * 100
	scalar json_STOVE_ICS_R    = e(b)[1,3] * 100
	scalar json_STOVE_CLEAN_R  = e(b)[1,4] * 100
	scalar json_STOVE_ELEC_R   = e(b)[1,5] * 100

	* Shorthand aliases for Table 1
	forval t = 0/5 {
		scalar json_ELEC_T`t'_N = json_ELEC_T`t'_NAT
		scalar json_ELEC_T`t'_U = json_ELEC_T`t'_URB
		scalar json_ELEC_T`t'_R = json_ELEC_T`t'_RUR
	}

	* Cooking time by gender (min/day)
	svy: mean cooktime_female cooktime_male
	scalar json_WOMEN_COOK_TIME = e(b)[1,1]
	scalar json_MEN_COOK_TIME   = e(b)[1,2]


	*===========================================================================
	*  SHEET 6: GRID BARRIERS & WTP
	*===========================================================================

	putexcel set "`xls'", sheet("Grid_Barriers_WTP") modify
	local row = 1
	putexcel A`row' = "Metric" B`row' = "National (%)" C`row' = "Urban (%)" D`row' = "Rural (%)"
	local row = 2

	local grid_vars ///
		barrier_cost barrier_dist barrier_tariff barrier_landlord barrier_unrel barrier_admin ///
		under_the_grid under_grid_unconnected grid_uptake ///
		wtp_grid_upfront wtp_grid_3m wtp_grid_6m wtp_grid_12m wtp_grid_waived wtp_grid_never refuse_wiring_cost

	foreach var of local grid_vars {
		putexcel A`row' = "`var'"
		foreach loc in NAT URB RUR {
			if "`loc'" == "NAT" local cond ""
			if "`loc'" == "URB" local cond "subpop(if loc_urban_rural == 1)"
			if "`loc'" == "RUR" local cond "subpop(if loc_urban_rural == 2)"
			local col = cond("`loc'" == "NAT", "B", cond("`loc'" == "URB", "C", "D"))

			capture {
				if "`cond'" == "" svy: mean `var'
				else svy, `cond': mean `var'
				local val = e(b)[1,1] * 100
				putexcel `col'`row' = `val'
				local uc_var = upper("`var'")
				scalar json_`uc_var'_`loc' = `val'
			}
		}
		local row = `row' + 1
	}

	* Grid history & spending (means in levels)
	foreach var in grid_years grid_wait_days grid_monthly_spend {
		putexcel A`row' = "`var'"
		foreach loc in NAT URB RUR {
			if "`loc'" == "NAT" local cond "subpop(if grid_hh == 1)"
			if "`loc'" == "URB" local cond "subpop(if grid_hh == 1 & loc_urban_rural == 1)"
			if "`loc'" == "RUR" local cond "subpop(if grid_hh == 1 & loc_urban_rural == 2)"
			local col = cond("`loc'" == "NAT", "B", cond("`loc'" == "URB", "C", "D"))

			capture {
				svy, `cond': mean `var'
				local val = e(b)[1,1]
				putexcel `col'`row' = `val'
				local uc_var = upper("`var'")
				scalar json_`uc_var'_`loc' = `val'
			}
		}
		local row = `row' + 1
	}
	putexcel save


	*===========================================================================
	*  SHEET 7: SOLAR WTP & BACKUP LIGHTING
	*===========================================================================

	putexcel set "`xls'", sheet("Solar_WTP_Issues") modify
	local row = 1
	putexcel A`row' = "Metric" B`row' = "National (%)" C`row' = "Urban (%)" D`row' = "Rural (%)"
	local row = 2

	local solar_vars ///
		wtp_solar_upfront wtp_solar_6m wtp_solar_12m wtp_solar_24m wtp_solar_never refuse_solar_cost srf_aware ///
		grid_backup_candle grid_backup_torch grid_backup_solar grid_backup_none

	foreach var of local solar_vars {
		putexcel A`row' = "`var'"
		foreach loc in NAT URB RUR {
			if "`loc'" == "NAT" local cond ""
			if "`loc'" == "URB" local cond "subpop(if loc_urban_rural == 1)"
			if "`loc'" == "RUR" local cond "subpop(if loc_urban_rural == 2)"
			local col = cond("`loc'" == "NAT", "B", cond("`loc'" == "URB", "C", "D"))

			capture {
				if "`cond'" == "" svy: mean `var'
				else svy, `cond': mean `var'
				local val = e(b)[1,1] * 100
				putexcel `col'`row' = `val'
				local uc_var = upper("`var'")
				scalar json_`uc_var'_`loc' = `val'
			}
		}
		local row = `row' + 1
	}
	putexcel save


	*===========================================================================
	*  SHEET 8: APPLIANCES OWNERSHIP BY LOAD LEVEL
	*===========================================================================

	putexcel set "`xls'", sheet("Appliances_Use") modify
	local row = 1
	putexcel A`row' = "Appliance / Load Tier" B`row' = "National (%)" C`row' = "Urban (%)" D`row' = "Rural (%)" E`row' = "Grid HH (%)" F`row' = "Off-grid Solar (%)"
	local row = 2

	local app_vars ///
		is_verylow is_low is_med is_high is_veryhigh ///
		has_lights has_charger has_radio has_tv has_fridge has_iron ///
		has_fan has_micro has_wash has_ac has_geyser

	foreach var of local app_vars {
		putexcel A`row' = "`var'"
		* National, Urban, Rural
		foreach loc in NAT URB RUR {
			if "`loc'" == "NAT" local cond ""
			if "`loc'" == "URB" local cond "subpop(if loc_urban_rural == 1)"
			if "`loc'" == "RUR" local cond "subpop(if loc_urban_rural == 2)"
			local col = cond("`loc'" == "NAT", "B", cond("`loc'" == "URB", "C", "D"))

			capture {
				if "`cond'" == "" svy: mean `var'
				else svy, `cond': mean `var'
				local val = e(b)[1,1] * 100
				putexcel `col'`row' = `val'
				local uc_var = upper("`var'")
				scalar json_`uc_var'_`loc' = `val'
			}
		}
		* Grid vs Off-grid Solar
		capture {
			svy, subpop(if grid_hh == 1): mean `var'
			putexcel E`row' = (e(b)[1,1] * 100)
			local uc_var = upper("`var'")
			scalar json_`uc_var'_GRID = e(b)[1,1] * 100
		}
		capture {
			svy, subpop(if solar_hh == 1): mean `var'
			putexcel F`row' = (e(b)[1,1] * 100)
			local uc_var = upper("`var'")
			scalar json_`uc_var'_SOLAR = e(b)[1,1] * 100
		}
		local row = `row' + 1
	}
	putexcel save


	*===========================================================================
	*  SHEET 9: REGIONAL ELECTRIFICATION (14 REGIONS OF NAMIBIA)
	*===========================================================================

	putexcel set "`xls'", sheet("Regional_Disagg") modify
	local row = 1
	putexcel A`row' = "Region" ///
		B`row' = "Electricity Access (%)" C`row' = "Electricity Access [95% CI]" ///
		D`row' = "Grid Access (%)"        E`row' = "Grid Access [95% CI]" ///
		F`row' = "Off-grid Solar (%)"     G`row' = "Off-grid Solar [95% CI]" ///
		H`row' = "High Access Tier 4-5 (%)" I`row' = "High Access Tier 4-5 [95% CI]" ///
		J`row' = "MECS Access (%)"        K`row' = "MECS Access [95% CI]"
	local row = 2

	local reg_names SOKOTO ZAMFARA KATSINA JIGAWA YOBE BORNO ADAMAWA GOMBE BAUCHI KANO KADUNA KEBBI NIGER FCT NASARAWA PLATEAU TARABA BENUE KOGI KWARA OYO OSUN EKITI ONDO EDO ANAMBRA ENUGU EBONYI CROSS_RIVER AKWA_IBOM ABIA IMO RIVERS BAYELSA DELTA LAGOS OGUN
	local reg_codes SOKOTO ZAMFARA KATSINA JIGAWA YOBE BORNO ADAMAWA GOMBE BAUCHI KANO KADUNA KEBBI NIGER FCT NASARAWA PLATEAU TARABA BENUE KOGI KWARA OYO OSUN EKITI ONDO EDO ANAMBRA ENUGU EBONYI CROSS_RIVER AKWA_IBOM ABIA IMO RIVERS BAYELSA DELTA LAGOS OGUN

	forval r = 1/37 {
		local rname : word `r' of `reg_names'
		local rcode : word `r' of `reg_codes'
		local rdisp = subinstr("`rname'", "_", " ", .)
		putexcel A`row' = "`rdisp'"

		capture {
			svy, subpop(if SEC_A_Q01 == `r'): proportion elec_access grid_hh solar_hh elc_t45 mecs_access
			matrix T = r(table)

			* T matrix indices for proportion = 1 (positive outcome):
			* Col 2: elec_access==1; Col 4: grid_hh==1; Col 6: solar_hh==1; Col 8: elc_t45==1; Col 10: mecs_access==1
			* Row 1: Point estimate (b), Row 5: LL, Row 6: UL

			local e_b  = T[1,2] * 100
			local e_ll = T[5,2] * 100
			local e_ul = T[6,2] * 100
			local e_ci : display %4.1f `e_b' "% [" %4.1f `e_ll' "% – " %4.1f `e_ul' "%]"
			putexcel B`row' = `e_b'
			putexcel C`row' = "`e_ci'"

			local g_b  = T[1,4] * 100
			local g_ll = T[5,4] * 100
			local g_ul = T[6,4] * 100
			local g_ci : display %4.1f `g_b' "% [" %4.1f `g_ll' "% – " %4.1f `g_ul' "%]"
			putexcel D`row' = `g_b'
			putexcel E`row' = "`g_ci'"

			local s_b  = T[1,6] * 100
			local s_ll = T[5,6] * 100
			local s_ul = T[6,6] * 100
			local s_ci : display %4.1f `s_b' "% [" %4.1f `s_ll' "% – " %4.1f `s_ul' "%]"
			putexcel F`row' = `s_b'
			putexcel G`row' = "`s_ci'"

			local t_b  = T[1,8] * 100
			local t_ll = T[5,8] * 100
			local t_ul = T[6,8] * 100
			local t_ci : display %4.1f `t_b' "% [" %4.1f `t_ll' "% – " %4.1f `t_ul' "%]"
			putexcel H`row' = `t_b'
			putexcel I`row' = "`t_ci'"

			local m_b  = T[1,10] * 100
			local m_ll = T[5,10] * 100
			local m_ul = T[6,10] * 100
			local m_ci : display %4.1f `m_b' "% [" %4.1f `m_ll' "% – " %4.1f `m_ul' "%]"
			putexcel J`row' = `m_b'
			putexcel K`row' = "`m_ci'"

			* Export point and CI interval strings for report templates
			scalar json_REG_`rcode'_ELEC     = `e_b'
			scalar json_REG_`rcode'_ELEC_LL  = `e_ll'
			scalar json_REG_`rcode'_ELEC_UL  = `e_ul'
			scalar json_REG_`rcode'_ELEC_CI  = "`e_ci'"

			scalar json_REG_`rcode'_GRID     = `g_b'
			scalar json_REG_`rcode'_GRID_LL  = `g_ll'
			scalar json_REG_`rcode'_GRID_UL  = `g_ul'
			scalar json_REG_`rcode'_GRID_CI  = "`g_ci'"

			scalar json_REG_`rcode'_SOLAR    = `s_b'
			scalar json_REG_`rcode'_SOLAR_LL = `s_ll'
			scalar json_REG_`rcode'_SOLAR_UL = `s_ul'
			scalar json_REG_`rcode'_SOLAR_CI = "`s_ci'"

			scalar json_REG_`rcode'_T45      = `t_b'
			scalar json_REG_`rcode'_T45_LL   = `t_ll'
			scalar json_REG_`rcode'_T45_UL   = `t_ul'
			scalar json_REG_`rcode'_T45_CI   = "`t_ci'"

			scalar json_REG_`rcode'_MECS     = `m_b'
			scalar json_REG_`rcode'_MECS_LL  = `m_ll'
			scalar json_REG_`rcode'_MECS_UL  = `m_ul'
			scalar json_REG_`rcode'_MECS_CI  = "`m_ci'"
		}
		local row = `row' + 1
	}
	putexcel save


	*===========================================================================
	*  SHEET 10: GENDER DEMOGRAPHICS & DECISION MAKING
	*===========================================================================

	putexcel set "`xls'", sheet("Gender_Profiles") modify
	local row = 1
	putexcel A`row' = "Indicator" B`row' = "Male HH Head (MHH)" C`row' = "Female HH Head (FHH)"
	local row = 2

	* Head share %
	svy: mean hh_head_gender
	scalar json_PCT_MHH = e(b)[1,1] == 1
	* Mean age
	svy, subpop(if hh_head_gender == 1): mean hh_head_age
	scalar json_HEAD_AGE_MHH = e(b)[1,1]
	putexcel A`row' = "Mean Age of Head" B`row' = (e(b)[1,1])
	svy, subpop(if hh_head_gender == 2): mean hh_head_age
	scalar json_HEAD_AGE_FHH = e(b)[1,1]
	putexcel C`row' = (e(b)[1,1])
	local row = `row' + 1

	* Demographics & credit dummies
	local g_vars ///
		head_educ_none head_educ_prim head_educ_sec head_educ_high ///
		head_marital_single head_marital_married head_marital_widow head_marital_divsep ///
		credit_access wtp_grid_upfront wtp_grid_12m wtp_solar_upfront wtp_solar_12m

	foreach var of local g_vars {
		putexcel A`row' = "`var'"
		forval g = 1/2 {
			local col = cond(`g' == 1, "B", "C")
			local g_tag = cond(`g' == 1, "MHH", "FHH")
			capture {
				svy, subpop(if hh_head_gender == `g'): mean `var'
				local val = e(b)[1,1] * 100
				putexcel `col'`row' = `val'
				local uc_var = upper("`var'")
				scalar json_`uc_var'_`g_tag' = `val'
			}
		}
		local row = `row' + 1
	}

	* Cookstove decision making
	svy: mean cook_dec_female cook_dec_male cook_dec_joint
	scalar json_COOK_DEC_FEMALE_NAT = e(b)[1,1] * 100
	scalar json_COOK_DEC_MALE_NAT   = e(b)[1,2] * 100
	scalar json_COOK_DEC_JOINT_NAT  = e(b)[1,3] * 100
	putexcel A`row' = "Cookstove Decision: Female" B`row' = (e(b)[1,1] * 100) C`row' = (e(b)[1,1] * 100)
	local row = `row' + 1
	putexcel A`row' = "Cookstove Decision: Male" B`row' = (e(b)[1,2] * 100) C`row' = (e(b)[1,2] * 100)
	local row = `row' + 1
	putexcel A`row' = "Cookstove Decision: Joint" B`row' = (e(b)[1,3] * 100) C`row' = (e(b)[1,3] * 100)
	putexcel save

	*===========================================================================
	*  SHEET 11: COOKING WTP & DECISION MAKING
	*===========================================================================
	putexcel set "`xls'", sheet("Cooking_WTP") modify
	local row = 1
	putexcel A`row' = "Metric" B`row' = "National (%)" C`row' = "Urban (%)" D`row' = "Rural (%)"
	local row = 2

	local cook_wtp_vars ///
		cook_dec_female cook_dec_male cook_dec_joint ///
		wtp_cook_upfront wtp_cook_3m wtp_cook_6m wtp_cook_12m wtp_cook_never refuse_cook_cost

	foreach var of local cook_wtp_vars {
		putexcel A`row' = "`var'"
		foreach loc in NAT URB RUR {
			if "`loc'" == "NAT" local cond ""
			if "`loc'" == "URB" local cond "subpop(if loc_urban_rural == 1)"
			if "`loc'" == "RUR" local cond "subpop(if loc_urban_rural == 2)"
			local col = cond("`loc'" == "NAT", "B", cond("`loc'" == "URB", "C", "D"))

			capture {
				if "`cond'" == "" svy: mean `var'
				else svy, `cond': mean `var'
				local val = e(b)[1,1] * 100
				putexcel `col'`row' = `val'
				local uc_var = upper("`var'")
				scalar json_`uc_var'_`loc' = `val'
			}
		}
		local row = `row' + 1
	}
	putexcel save


	*===========================================================================
	*  WRITE EXPANDED JSON FILE
	*===========================================================================

	file open jf using "`json_out'", write replace
	file write jf `"{"' _newline

	local scalars_list ///
		ELEC_T0_NAT ELEC_T1_NAT ELEC_T2_NAT ELEC_T3_NAT ELEC_T4_NAT ELEC_T5_NAT ///
		ELEC_T0_URB ELEC_T1_URB ELEC_T2_URB ELEC_T3_URB ELEC_T4_URB ELEC_T5_URB ///
		ELEC_T0_RUR ELEC_T1_RUR ELEC_T2_RUR ELEC_T3_RUR ELEC_T4_RUR ELEC_T5_RUR ///
		ELEC_T0_N ELEC_T1_N ELEC_T2_N ELEC_T3_N ELEC_T4_N ELEC_T5_N ///
		ELEC_T0_U ELEC_T1_U ELEC_T2_U ELEC_T3_U ELEC_T4_U ELEC_T5_U ///
		ELEC_T0_R ELEC_T1_R ELEC_T2_R ELEC_T3_R ELEC_T4_R ELEC_T5_R ///
		ELEC_ACC_NAT ELEC_ACC_URB ELEC_ACC_RUR ///
		ELEC_T45_NAT ELEC_T45_URB ELEC_T45_RUR ///
		GRID_ACC_NAT GRID_ACC_URB GRID_ACC_RUR ///
		SOLAR_ACC_NAT SOLAR_ACC_URB SOLAR_ACC_RUR ///
		COOK_T0_NAT COOK_T1_NAT COOK_T2_NAT COOK_T3_NAT COOK_T4_NAT COOK_T5_NAT ///
		COOK_T0_URB COOK_T1_URB COOK_T2_URB COOK_T3_URB COOK_T4_URB COOK_T5_URB ///
		COOK_T0_RUR COOK_T1_RUR COOK_T2_RUR COOK_T3_RUR COOK_T4_RUR COOK_T5_RUR ///
		MECS_ACC_NAT MECS_ACC_URB MECS_ACC_RUR ///
		TRANS_COOK_NAT TRANS_COOK_URB TRANS_COOK_RUR ///
		THREESTONE_NAT THREESTONE_URB THREESTONE_RUR ///
		CLEAN_STOVE_NAT CLEAN_STOVE_URB CLEAN_STOVE_RUR ///
		STOVE_3STONE_N STOVE_3STONE_U STOVE_3STONE_R ///
		STOVE_TRAD_N STOVE_TRAD_U STOVE_TRAD_R ///
		STOVE_ICS_N STOVE_ICS_U STOVE_ICS_R ///
		STOVE_CLEAN_N STOVE_CLEAN_U STOVE_CLEAN_R ///
		STOVE_ELEC_N STOVE_ELEC_U STOVE_ELEC_R ///
		Q1_ELEC_ACC Q2_ELEC_ACC Q3_ELEC_ACC Q4_ELEC_ACC Q5_ELEC_ACC ///
		Q1_MECS_ACC Q2_MECS_ACC Q3_MECS_ACC Q4_MECS_ACC Q5_MECS_ACC ///
		MHH_ELEC_ACC FHH_ELEC_ACC MHH_MECS_ACC FHH_MECS_ACC ///
		WOMEN_FUEL_TIME MEN_FUEL_TIME WOMEN_FUEL_WORKDAYS ///
		WOMEN_COOK_TIME MEN_COOK_TIME ///
		PCT_STOVE_STACKING PCT_STACKING_DILUTION PCT_CLEAN_STOVE_OWNERSHIP ///
		PCT_CAP_LIMITED PCT_EVE_SHORTAGE PCT_VOLTAGE_DAMAGE ///
		AVG_OUTAGES_PER_WEEK PCT_SL_STUCK_T1 ///
		BARRIER_COST_NAT BARRIER_COST_URB BARRIER_COST_RUR ///
		BARRIER_DIST_NAT BARRIER_DIST_URB BARRIER_DIST_RUR ///
		BARRIER_TARIFF_NAT BARRIER_TARIFF_URB BARRIER_TARIFF_RUR ///
		BARRIER_LANDLORD_NAT BARRIER_LANDLORD_URB BARRIER_LANDLORD_RUR ///
		BARRIER_UNREL_NAT BARRIER_UNREL_URB BARRIER_UNREL_RUR ///
		BARRIER_ADMIN_NAT BARRIER_ADMIN_URB BARRIER_ADMIN_RUR ///
		UNDER_THE_GRID_NAT UNDER_THE_GRID_URB UNDER_THE_GRID_RUR ///
		UNDER_GRID_UNCONNECTED_NAT UNDER_GRID_UNCONNECTED_URB UNDER_GRID_UNCONNECTED_RUR ///
		GRID_UPTAKE_NAT GRID_UPTAKE_URB GRID_UPTAKE_RUR ///
		GRID_YEARS_NAT GRID_YEARS_URB GRID_YEARS_RUR ///
		GRID_WAIT_DAYS_NAT GRID_MONTHLY_SPEND_NAT GRID_MONTHLY_SPEND_URB GRID_MONTHLY_SPEND_RUR ///
		WTP_GRID_UPFRONT_NAT WTP_GRID_UPFRONT_URB WTP_GRID_UPFRONT_RUR ///
		WTP_GRID_3M_NAT WTP_GRID_6M_NAT WTP_GRID_12M_NAT WTP_GRID_WAIVED_NAT WTP_GRID_NEVER_NAT ///
		REFUSE_WIRING_COST_NAT ///
		WTP_COOK_UPFRONT_NAT WTP_COOK_UPFRONT_URB WTP_COOK_UPFRONT_RUR ///
		WTP_COOK_3M_NAT WTP_COOK_3M_URB WTP_COOK_3M_RUR ///
		WTP_COOK_6M_NAT WTP_COOK_6M_URB WTP_COOK_6M_RUR ///
		WTP_COOK_12M_NAT WTP_COOK_12M_URB WTP_COOK_12M_RUR ///
		WTP_COOK_NEVER_NAT WTP_COOK_NEVER_URB WTP_COOK_NEVER_RUR ///
		REFUSE_COOK_COST_NAT REFUSE_COOK_COST_URB REFUSE_COOK_COST_RUR ///
		WTP_SOLAR_UPFRONT_NAT WTP_SOLAR_6M_NAT WTP_SOLAR_12M_NAT WTP_SOLAR_24M_NAT WTP_SOLAR_NEVER_NAT ///
		REFUSE_SOLAR_COST_NAT SRF_AWARE_NAT SRF_AWARE_URB SRF_AWARE_RUR ///
		GRID_BACKUP_CANDLE_NAT GRID_BACKUP_CANDLE_URB GRID_BACKUP_CANDLE_RUR ///
		GRID_BACKUP_TORCH_NAT GRID_BACKUP_SOLAR_NAT GRID_BACKUP_NONE_NAT ///
		IS_VERYLOW_NAT IS_LOW_NAT IS_MED_NAT IS_HIGH_NAT IS_VERYHIGH_NAT ///
		IS_VERYLOW_URB IS_LOW_URB IS_MED_URB IS_HIGH_URB IS_VERYHIGH_URB ///
		IS_VERYLOW_RUR IS_LOW_RUR IS_MED_RUR IS_HIGH_RUR IS_VERYHIGH_RUR ///
		HAS_LIGHTS_NAT HAS_CHARGER_NAT HAS_RADIO_NAT HAS_TV_NAT HAS_FRIDGE_NAT ///
		HAS_IRON_NAT HAS_FAN_NAT HAS_MICRO_NAT HAS_WASH_NAT HAS_AC_NAT HAS_GEYSER_NAT ///
		HEAD_AGE_MHH HEAD_AGE_FHH ///
		HEAD_EDUC_NONE_MHH HEAD_EDUC_NONE_FHH HEAD_EDUC_PRIM_MHH HEAD_EDUC_PRIM_FHH ///
		HEAD_EDUC_SEC_MHH HEAD_EDUC_SEC_FHH HEAD_EDUC_HIGH_MHH HEAD_EDUC_HIGH_FHH ///
		HEAD_MARITAL_SINGLE_MHH HEAD_MARITAL_SINGLE_FHH HEAD_MARITAL_MARRIED_MHH HEAD_MARITAL_MARRIED_FHH ///
		HEAD_MARITAL_WIDOW_MHH HEAD_MARITAL_WIDOW_FHH HEAD_MARITAL_DIVSEP_MHH HEAD_MARITAL_DIVSEP_FHH ///
		CREDIT_ACCESS_MHH CREDIT_ACCESS_FHH ///
		WTP_GRID_UPFRONT_MHH WTP_GRID_UPFRONT_FHH WTP_GRID_12M_MHH WTP_GRID_12M_FHH ///
		WTP_SOLAR_UPFRONT_MHH WTP_SOLAR_UPFRONT_FHH ///
		COOK_DEC_FEMALE_NAT COOK_DEC_MALE_NAT COOK_DEC_JOINT_NAT ///
		REG_SOKOTO_ELEC REG_ZAMFARA_ELEC REG_KATSINA_ELEC REG_JIGAWA_ELEC REG_YOBE_ELEC ///
		REG_BORNO_ELEC REG_ADAMAWA_ELEC REG_GOMBE_ELEC REG_BAUCHI_ELEC REG_KANO_ELEC ///
		REG_KADUNA_ELEC REG_KEBBI_ELEC REG_NIGER_ELEC REG_FCT_ELEC REG_NASARAWA_ELEC ///
		REG_PLATEAU_ELEC REG_TARABA_ELEC REG_BENUE_ELEC REG_KOGI_ELEC REG_KWARA_ELEC ///
		REG_OYO_ELEC REG_OSUN_ELEC REG_EKITI_ELEC REG_ONDO_ELEC REG_EDO_ELEC ///
		REG_ANAMBRA_ELEC REG_ENUGU_ELEC REG_EBONYI_ELEC REG_CROSS_RIVER_ELEC REG_AKWA_IBOM_ELEC ///
		REG_ABIA_ELEC REG_IMO_ELEC REG_RIVERS_ELEC REG_BAYELSA_ELEC REG_DELTA_ELEC ///
		REG_LAGOS_ELEC REG_OGUN_ELEC REG_SOKOTO_GRID REG_ZAMFARA_GRID REG_KATSINA_GRID ///
		REG_JIGAWA_GRID REG_YOBE_GRID REG_BORNO_GRID REG_ADAMAWA_GRID REG_GOMBE_GRID ///
		REG_BAUCHI_GRID REG_KANO_GRID REG_KADUNA_GRID REG_KEBBI_GRID REG_NIGER_GRID ///
		REG_FCT_GRID REG_NASARAWA_GRID REG_PLATEAU_GRID REG_TARABA_GRID REG_BENUE_GRID ///
		REG_KOGI_GRID REG_KWARA_GRID REG_OYO_GRID REG_OSUN_GRID REG_EKITI_GRID ///
		REG_ONDO_GRID REG_EDO_GRID REG_ANAMBRA_GRID REG_ENUGU_GRID REG_EBONYI_GRID ///
		REG_CROSS_RIVER_GRID REG_AKWA_IBOM_GRID REG_ABIA_GRID REG_IMO_GRID REG_RIVERS_GRID ///
		REG_BAYELSA_GRID REG_DELTA_GRID REG_LAGOS_GRID REG_OGUN_GRID REG_SOKOTO_SOLAR ///
		REG_ZAMFARA_SOLAR REG_KATSINA_SOLAR REG_JIGAWA_SOLAR REG_YOBE_SOLAR REG_BORNO_SOLAR ///
		REG_ADAMAWA_SOLAR REG_GOMBE_SOLAR REG_BAUCHI_SOLAR REG_KANO_SOLAR REG_KADUNA_SOLAR ///
		REG_KEBBI_SOLAR REG_NIGER_SOLAR REG_FCT_SOLAR REG_NASARAWA_SOLAR REG_PLATEAU_SOLAR ///
		REG_TARABA_SOLAR REG_BENUE_SOLAR REG_KOGI_SOLAR REG_KWARA_SOLAR REG_OYO_SOLAR ///
		REG_OSUN_SOLAR REG_EKITI_SOLAR REG_ONDO_SOLAR REG_EDO_SOLAR REG_ANAMBRA_SOLAR ///
		REG_ENUGU_SOLAR REG_EBONYI_SOLAR REG_CROSS_RIVER_SOLAR REG_AKWA_IBOM_SOLAR REG_ABIA_SOLAR ///
		REG_IMO_SOLAR REG_RIVERS_SOLAR REG_BAYELSA_SOLAR REG_DELTA_SOLAR REG_LAGOS_SOLAR ///
		REG_OGUN_SOLAR

	local first = 1
	foreach sc of local scalars_list {
		capture confirm scalar json_`sc'
		if !_rc {
			local v = string(scalar(json_`sc'), "%8.1f")
			if !`first' file write jf "," _newline
			file write jf `"  "{{`sc'}}": `v'"'
			local first = 0
		}
	}

	file write jf _newline `"}"' _newline
	file close jf

	di " 07_export.do complete (10 sheets + expanded JSON)"
	di " Excel: `xls'"
	di " JSON:  `json_out'"
