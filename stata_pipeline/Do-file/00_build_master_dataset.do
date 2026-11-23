	**************************************************************************
	*  00_build_master_dataset.do                                            *
	*  Namibia MTF Pipeline — Raw Data Processing & Master Dataset Builder  *
	*                                                                        *
	*  Processes raw modules in $raw_hh and $user/Data/weights/:            *
	*    1. Demographics: Household size, head sex/age from hhroster.dta    *
	*    2. Sampling weights & Strata from calibrated weights Excel         *
	*    3. Non-energy expenditure:                                         *
	*       - food.dta (7-day recall)                                       *
	*       - nonfood_1mon.dta (1-month recall)                             *
	*       - nonfood_12mon.dta (12-month recall)                           *
	*    4. Electricity expenditure:                                        *
	*       - Grid (SEC_C_Q25), Mini-grid (SEC_C_Q62)                       *
	*       - Generator (sec_c_generator.dta)                               *
	*       - Rechargeable battery (sec_c_rechar_ba.dta)                    *
	*    5. Fuel expenditure (cooking, heating, productive):                *
	*       - fuel_consumption.dta                                          *
	*    6. Lighting fuel expenditure:                                      *
	*       - fuel_h11.dta (candles, kerosene, dry-cell batteries)          *
	*    7. Total household expenditure & Population-weighted quintiles     *
	*    8. Solar device roster cleaning & main device matching             *
	*    9. Cookstoves roster cleaning & stacking indicators                *
	*   10. Time use: Fuel collection & cooking time by gender              *
	*                                                                        *
	*  Output:                                                               *
	*    $wip_hh/$master_dta                             *
	**************************************************************************

	clear
	set more off


	*===========================================================================
	*  1. DEMOGRAPHICS (FROM HHROSTER.DTA)
	*===========================================================================

	local fn_hhroster = cond("$fn_hhroster" != "", "$fn_hhroster", "hhroster.dta")
	capture confirm file "$raw_hh/`fn_hhroster'"
	if _rc {
		capture confirm file "$raw_hh/section_a1_hh_roster.dta"
		if !_rc local fn_hhroster "section_a1_hh_roster.dta"
	}

	** Demographics: Household size & head characteristics from hhroster.dta
	use "$raw_hh/`fn_hhroster'", clear
	capture confirm variable interview__id
	if _rc {
		capture confirm variable interview__key
		if !_rc clonevar interview__id = interview__key
	}
	bys interview__id: gen hhsize = _N
	lab var hhsize "Household Size"
	keep if SEC_A1_Q4 == 1               // keep household head
	keep interview__id hhsize SEC_A1_Q3 SEC_A1_Q5 SEC_A1_Q7 SEC_A1_Q8 SEC_A1_Q10
	
	clonevar hh_head_gender = SEC_A1_Q3
	lab define hh_head_gender 1 "Male HH Head (MHH)" 2 "Female HH Head (FHH)", replace
	lab val hh_head_gender hh_head_gender
	lab var hh_head_gender "Sex of Household Head"
	
	clonevar hh_head_age = SEC_A1_Q5
	replace hh_head_age = . if hh_head_age > 110 | hh_head_age < 15
	lab var hh_head_age "Age of Household Head (years)"

	* Education level of head (SEC_A1_Q8)
	gen byte hh_head_educ = .
	replace hh_head_educ = 0 if inlist(SEC_A1_Q8, 1, 2) | SEC_A1_Q7 == 2
	replace hh_head_educ = 1 if inrange(SEC_A1_Q8, 3, 9)
	replace hh_head_educ = 2 if inrange(SEC_A1_Q8, 10, 16)
	replace hh_head_educ = 3 if inrange(SEC_A1_Q8, 17, 35)
	lab define hh_head_educ 0 "None" 1 "Primary" 2 "Secondary" 3 "Higher Education", replace
	lab val hh_head_educ hh_head_educ
	lab var hh_head_educ "Education Level of Household Head"

	* Marital status of head (SEC_A1_Q10)
	clonevar hh_head_marital = SEC_A1_Q10
	lab var hh_head_marital "Marital Status of Household Head"

	keep interview__id hhsize hh_head_gender hh_head_age hh_head_educ hh_head_marital SEC_A1_Q3 SEC_A1_Q5 SEC_A1_Q7 SEC_A1_Q8 SEC_A1_Q10
	duplicates drop
	save "$wip_hh/demographics.dta", replace

	* Backward-compatibility stubs (prevents crashes in legacy/custom country do-files):
	preserve
		keep interview__id hhsize
		save "$wip_hh/hhsize.dta", replace
	restore
	preserve
		keep interview__id hh_head_* SEC_A1_*
		save "$wip_hh/headgender.dta", replace
	restore


	*===========================================================================
	*  2. SAMPLING WEIGHTS & SURVEY STRATIFICATION
	*===========================================================================

	capture confirm file "$raw_hh/admin_info.dta"
	if !_rc {
		use "$raw_hh/admin_info.dta", clear
		capture confirm variable interview__id
		if _rc {
			capture confirm variable interview__key
			if !_rc clonevar interview__id = interview__key
		}
		capture clonevar hh_wt = hh_weight_final
		capture confirm variable hh_wt
		if _rc {
			capture clonevar hh_wt = weight
			if _rc gen hh_wt = 1.0
		}

		* Merge core single-household section files
		foreach sec in section_a2 section_b section_c section_d section_e section_g section_k section_n section_o section_q section_r section_s {
			capture confirm file "$raw_hh/`sec'.dta"
			if !_rc {
				preserve
					use "$raw_hh/`sec'.dta", clear
					capture confirm variable interview__id
					if _rc {
						capture confirm variable interview__key
						if !_rc clonevar interview__id = interview__key
					}
					tempfile temp_`sec'
					save "`temp_`sec''"
				restore
				merge 1:1 interview__id using "`temp_`sec''", nogen
			}
		}
	}
	else {
		import excel "$user/Data/weights/sample_selected_energy_survey_20_08_2024.xlsx", ///
			sheet("CalibratedWeight") firstrow case(lower) clear
		rename ea_number SEC_A_Q05
		merge 1:m SEC_A_Q05 using "$raw_hh/MTF_2024_HH_Namibia_Final.dta"
		drop if _merge == 1                  // drop non-matched sample frame rows
		drop _merge

		** Corrected Bryan Koo weight formula:
		gen hh_wt = (firstsampleweight / second_stage_prob) / response_rate
	}
	lab var hh_wt "Final Calibrated Household Weight"

	** Merge demographics (hhsize and head characteristics)
	merge 1:1 interview__id using "$wip_hh/demographics.dta", nogen

	** Population weight:
	gen pop_wt = hh_wt * hhsize
	lab var pop_wt "Final Population Weight (hh_wt × hhsize)"

	** Sampling Unit / EA cluster uniqueness (Comment C21)
	capture confirm variable SEC_A_Q07
	if !_rc {
		capture drop psu_id
		egen psu_id = group(SEC_A_Q07)
	}
	else {
		capture confirm variable SEC_A_Q06
		if !_rc {
			capture drop psu_id
			egen psu_id = group(SEC_A_Q06)
		}
		else {
			capture drop psu_id
			egen psu_id = group(SEC_A_Q05)
		}
	}
	lab var psu_id "Sampling Primary Sampling Unit / Enumeration Area ID (unique clusters)"

	** Locality (Urban / Rural):
	gen loc_urban_rural = .
	capture confirm variable SEC_A_Q05
	if !_rc {
		replace loc_urban_rural = SEC_A_Q05 if inlist(SEC_A_Q05, 1, 2)
	}
	replace loc_urban_rural = 1 if SEC_A_Q03 == 1 & loc_urban_rural == .
	replace loc_urban_rural = 2 if SEC_A_Q03 == 99 & loc_urban_rural == .
	lab define loc_urban_rural 1 "Urban" 2 "Rural", replace
	lab val loc_urban_rural loc_urban_rural
	lab var loc_urban_rural "Urban / Rural Locality"

	** Stratification variable: Region (Admin 1) × Locality
	capture drop strata_id
	capture confirm variable SEC_A_Q01
	if !_rc {
		capture confirm variable SEC_A_Q05
		if !_rc {
			egen strata_id = group(SEC_A_Q01 SEC_A_Q05)
		}
		else {
			egen strata_id = group(SEC_A_Q01 loc_urban_rural)
		}
	}
	else {
		gen strata_id = 1
	}
	lab var strata_id "Survey Stratum: Region × Locality"

	** Household enterprise & informal dwelling
	capture confirm variable SEC_B_Q03
	if !_rc {
		gen inf_dwell = inlist(SEC_B_Q03, 8, 9)
		lab define inf_dwell 1 "Informal Dwelling" 0 "Formal Dwelling", replace
		lab val inf_dwell inf_dwell
		lab var inf_dwell "Informal Dwelling (shack in backyard/settlement)"
	}

	capture confirm variable SEC_A2_Q16
	if !_rc {
		capture confirm variable SEC_A2_Q19
		if !_rc {
			gen hhbiz = (SEC_A2_Q16 == 1 & SEC_A2_Q19 == 1)
			lab define hhbiz 0 "No Enterprise" 1 "HH Enterprise", replace
			lab val hhbiz hhbiz
			lab var hhbiz "Household with Enterprise"
		}
	}

	save "$wip_hh/$master_dta", replace


	*===========================================================================
	*  3. NON-ENERGY EXPENDITURE & CONSUMPTION
	*===========================================================================

	local fn_food = cond("$fn_food" != "", "$fn_food", "food.dta")
	local fn_nonfood_1mon = cond("$fn_nonfood_1mon" != "", "$fn_nonfood_1mon", "nonfood_1mon.dta")
	local fn_nonfood_12mon = cond("$fn_nonfood_12mon" != "", "$fn_nonfood_12mon", "nonfood_12mon.dta")

	** A. Food (7-day recall)
	use "$raw_hh/`fn_food'", clear
	capture confirm variable interview__id
	if _rc {
		capture confirm variable interview__key
		if !_rc clonevar interview__id = interview__key
	}
	replace SEC_O_Q02 = . if SEC_O_Q02 == 888
	replace SEC_O_Q03 = . if SEC_O_Q03 == 888
	replace SEC_O_Q04 = . if SEC_O_Q04 == 888

	egen fooditem_exp   = rowtotal(SEC_O_Q0*)
	gen fooditem_exp_m  = ((fooditem_exp / 7) * 365) / 12
	gen fooditem_exp_yr = (fooditem_exp / 7) * 365

	bys interview__id: egen food_exp_wk = total(fooditem_exp)
	bys interview__id: egen food_exp_m  = total(fooditem_exp_m)
	bys interview__id: egen food_exp_yr = total(fooditem_exp_yr)
	lab var food_exp_wk "Weekly Household Food Expenditure"
	lab var food_exp_m  "Monthly Household Food Expenditure"
	lab var food_exp_yr "Annual Household Food Expenditure"

	keep interview__id food_exp_wk food_exp_m food_exp_yr
	duplicates drop
	save "$wip_hh/food.dta", replace

	** B. Non-food 1-month recall
	use "$raw_hh/`fn_nonfood_1mon'", clear
	capture confirm variable interview__id
	if _rc {
		capture confirm variable interview__key
		if !_rc clonevar interview__id = interview__key
	}
	replace SEC_O_Q1M_1 = . if SEC_O_Q1M_1 == 888
	bys interview__id: egen nonfood_1mon_exp_m = total(SEC_O_Q1M_1)
	gen nonfood_1mon_exp_yr = nonfood_1mon_exp_m * 12
	lab var nonfood_1mon_exp_m  "Monthly Nonfood Expenditure (1-month recall)"
	lab var nonfood_1mon_exp_yr "Annual Nonfood Expenditure (1-month recall)"
	keep interview__id nonfood_1mon_exp_m nonfood_1mon_exp_yr
	duplicates drop
	save "$wip_hh/nonfood_1mon.dta", replace

	** C. Non-food 12-month recall
	use "$raw_hh/`fn_nonfood_12mon'", clear
	capture confirm variable interview__id
	if _rc {
		capture confirm variable interview__key
		if !_rc clonevar interview__id = interview__key
	}
	replace SEC_O_Q12M_1 = . if SEC_O_Q12M_1 == 888
	bys interview__id: egen nonfood_12mon_exp_yr = total(SEC_O_Q12M_1)
	gen nonfood_12mon_exp_m = nonfood_12mon_exp_yr / 12
	lab var nonfood_12mon_exp_m  "Monthly Nonfood Expenditure (12-month recall)"
	lab var nonfood_12mon_exp_yr "Annual Nonfood Expenditure (12-month recall)"
	keep interview__id nonfood_12mon_exp_m nonfood_12mon_exp_yr
	duplicates drop
	save "$wip_hh/nonfood_12mon.dta", replace

	** Merge non-energy expenditure into master
	use "$wip_hh/$master_dta", clear
	merge 1:1 interview__id using "$wip_hh/food.dta", nogen
	merge 1:1 interview__id using "$wip_hh/nonfood_1mon.dta", nogen
	merge 1:1 interview__id using "$wip_hh/nonfood_12mon.dta", nogen

	egen nonenergy_exp_m  = rowtotal(food_exp_m nonfood_1mon_exp_m nonfood_12mon_exp_m)
	egen nonenergy_exp_yr = rowtotal(food_exp_yr nonfood_1mon_exp_yr nonfood_12mon_exp_yr)
	lab var nonenergy_exp_m  "Monthly Total Non-energy Expenditure (food+services)"
	lab var nonenergy_exp_yr "Annual Total Non-energy Expenditure (food+services)"
	save "$wip_hh/$master_dta", replace


	*===========================================================================
	*  4. ELECTRICITY EXPENDITURE
	*===========================================================================

	use "$wip_hh/$master_dta", clear

	** A. Grid electricity (SEC_C_Q25)
	gen grid_exp_m = SEC_C_Q25
	replace grid_exp_m = . if inlist(SEC_C_Q25, 888, 9, -888, 999, -999)
	replace grid_exp_m = 0 if grid_exp_m == . & SEC_C_Q12 == 111  // pays no one
	gen grid_exp_yr = grid_exp_m * 12
	lab var grid_exp_m  "Monthly grid electricity expenditure"
	lab var grid_exp_yr "Annual grid electricity expenditure"

	** B. Mini-grid electricity (SEC_C_Q62)
	gen minigrid_exp_m = SEC_C_Q62
	replace minigrid_exp_m = . if SEC_C_Q62 == 888
	replace minigrid_exp_m = 0 if SEC_C_Q62 == . & SEC_C_Q48 == 111
	gen minigrid_exp_yr = minigrid_exp_m * 12
	lab var minigrid_exp_m  "Monthly mini-grid electricity expenditure"
	lab var minigrid_exp_yr "Annual mini-grid electricity expenditure"

	save "$wip_hh/$master_dta", replace

	local fn_generator = cond("$fn_generator" != "", "$fn_generator", "sec_c_generator.dta")
	local fn_rechar_ba = cond("$fn_rechar_ba" != "", "$fn_rechar_ba", "sec_c_rechar_ba.dta")

	** C. Generator Expenditure (pre-aggregated from generator roster)
	use "$raw_hh/`fn_generator'", clear
	capture confirm variable interview__id
	if _rc {
		capture confirm variable interview__key
		if !_rc clonevar interview__id = interview__key
	}
	replace SEC_C_Q88 = . if SEC_C_Q88 == 888
	gen gen_exp_maint_yr = SEC_C_Q88
	gen gen_exp_maint_m  = gen_exp_maint_yr / 12

	egen nbr_mth_gen = rowtotal(SEC_C_Q84__1-SEC_C_Q84__12)
	replace nbr_mth_gen = 12 if SEC_C_Q84__111 == 1

	replace SEC_C_Q91 = . if SEC_C_Q91 == 888
	gen gen_exp_fuel_m  = SEC_C_Q91
	gen gen_exp_fuel_yr = gen_exp_fuel_m * nbr_mth_gen

	recode gen_exp_maint_m gen_exp_maint_yr gen_exp_fuel_m gen_exp_fuel_yr (. = 0)
	gen gen_exp_item_m  = gen_exp_maint_m + gen_exp_fuel_m
	gen gen_exp_item_yr = gen_exp_maint_yr + gen_exp_fuel_yr

	* Aggregate across multiple generators per household
	bys interview__id: egen gen_exp_tot_m  = total(gen_exp_item_m)
	bys interview__id: egen gen_exp_tot_yr = total(gen_exp_item_yr)
	lab var gen_exp_tot_m  "Monthly total generator expenditure"
	lab var gen_exp_tot_yr "Annual total generator expenditure"
	keep interview__id gen_exp_tot_m gen_exp_tot_yr
	duplicates drop
	save "$wip_hh/generator_exp.dta", replace

	** D. Rechargeable Battery Expenditure (pre-aggregated from rechargeable battery roster)
	use "$raw_hh/`fn_rechar_ba'", clear
	capture confirm variable interview__id
	if _rc {
		capture confirm variable interview__key
		if !_rc clonevar interview__id = interview__key
	}
	egen nbr_mth_rech = rowtotal(SEC_C_Q103__1-SEC_C_Q103__12)
	replace nbr_mth_rech = 12 if SEC_C_Q103__111 == 1

	replace SEC_C_Q108 = . if SEC_C_Q108 == 888
	gen rech_bat_exp_item_m  = SEC_C_Q108
	gen rech_bat_exp_item_yr = rech_bat_exp_item_m * nbr_mth_rech
	recode rech_bat_exp_item_m rech_bat_exp_item_yr (. = 0)

	* Aggregate across multiple batteries per household
	bys interview__id: egen rech_bat_exp_m  = total(rech_bat_exp_item_m)
	bys interview__id: egen rech_bat_exp_yr = total(rech_bat_exp_item_yr)
	lab var rech_bat_exp_m  "Monthly rechargeable battery expenditure"
	lab var rech_bat_exp_yr "Annual rechargeable battery expenditure"
	keep interview__id rech_bat_exp_m rech_bat_exp_yr
	duplicates drop
	save "$wip_hh/rechar_ba_exp.dta", replace

	** Merge pre-aggregated expenditures into master dataset (1:1 is guaranteed)
	use "$wip_hh/$master_dta", clear
	merge 1:1 interview__id using "$wip_hh/generator_exp.dta", nogen
	merge 1:1 interview__id using "$wip_hh/rechar_ba_exp.dta", nogen

	** Combine electricity expenditure
	recode grid_exp_m grid_exp_yr minigrid_exp_m minigrid_exp_yr gen_exp_tot_m gen_exp_tot_yr rech_bat_exp_m rech_bat_exp_yr (. = 0)

	gen elec_exp_m  = grid_exp_m + minigrid_exp_m + gen_exp_tot_m + rech_bat_exp_m
	gen elec_exp_yr = grid_exp_yr + minigrid_exp_yr + gen_exp_tot_yr + rech_bat_exp_yr
	lab var elec_exp_m  "Total Monthly Electricity Expenditure"
	lab var elec_exp_yr "Total Annual Electricity Expenditure"
	save "$wip_hh/$master_dta", replace


	*===========================================================================
	*  5. GENERAL & COOKING FUEL EXPENDITURE (FUEL_CONSUMPTION.DTA)
	*===========================================================================

	local fn_fuel_consump = cond("$fn_fuel_consump" != "", "$fn_fuel_consump", "fuel_consumption.dta")
	capture confirm file "$raw_hh/`fn_fuel_consump'"
	if _rc {
		capture confirm file "$raw_hh/section_i_fuel_consumption_roster.dta"
		if !_rc local fn_fuel_consump "section_i_fuel_consumption_roster.dta"
	}
	use "$raw_hh/`fn_fuel_consump'", clear
	capture confirm variable interview__id
	if _rc {
		capture confirm variable interview__key
		if !_rc clonevar interview__id = interview__key
	}

	gen nbr_month_fuel = SEC_I_Q04
	gen fuel_buy_freq  = SEC_I_Q07

	** Clean frequency "Other, specify" responses
	capture confirm variable SEC_I_Q07_oth
	if !_rc {
		replace fuel_buy_freq = 3  if inlist(lower(SEC_I_Q07_oth), "twice a week", "twice per week")
		replace fuel_buy_freq = 6  if inlist(lower(SEC_I_Q07_oth), "few times a month", "twice per month", "twice a month")
		replace fuel_buy_freq = 12 if inlist(lower(SEC_I_Q07_oth), "3 times per week", "3 times a week", "three times per week")
		replace fuel_buy_freq = 13 if inlist(lower(SEC_I_Q07_oth), "3 times a month", "3 times in a month")
		replace fuel_buy_freq = 14 if lower(SEC_I_Q07_oth) == "after 2 days"
		replace fuel_buy_freq = 15 if inlist(lower(SEC_I_Q07_oth), "every year", "once in a year", "once a year", "after a year")
		replace fuel_buy_freq = 16 if inlist(lower(SEC_I_Q07_oth), "2 years", "every 2 years")
		replace fuel_buy_freq = 17 if inlist(lower(SEC_I_Q07_oth), "4 times per week", "4 times a week")
		replace fuel_buy_freq = 18 if lower(SEC_I_Q07_oth) == "5 times a month"
		replace fuel_buy_freq = 19 if lower(SEC_I_Q07_oth) == "after 8 months"
		replace fuel_buy_freq = 20 if inlist(lower(SEC_I_Q07_oth), "twice in a year", "twice a year")
		replace fuel_buy_freq = 21 if lower(SEC_I_Q07_oth) == "twice per month"
		replace fuel_buy_freq = 22 if inlist(lower(SEC_I_Q07_oth), "not purchased", "never")
		replace fuel_buy_freq = 23 if inlist(lower(SEC_I_Q07_oth), "as needed", "when needed", "rarely", "occasionally")
	}

	** Clean "As need arises" to mode frequency
	replace fuel_buy_freq = 6 if fuel_buy_freq == 23 & inlist(fuel_consumption__id, 1, 2, 4, 5, 7) // monthly
	replace fuel_buy_freq = 1 if fuel_buy_freq == 23 & fuel_consumption__id == 3                     // daily for wood collected

	gen fuel_pay = SEC_I_Q09
	replace fuel_pay = 0 if inlist(fuel_consumption__id, 3, 16) // wood collected, garbage = 0
	replace fuel_pay = . if fuel_pay == 888

	gen fuel_exp_m = .
	replace fuel_exp_m = fuel_pay * 30            if fuel_buy_freq == 1
	replace fuel_exp_m = (fuel_pay / 7) * 30      if fuel_buy_freq == 2
	replace fuel_exp_m = (fuel_pay / 7) * 30 * 2  if fuel_buy_freq == 3
	replace fuel_exp_m = (fuel_pay / 14) * 30     if fuel_buy_freq == 4
	replace fuel_exp_m = (fuel_pay / 21) * 30     if fuel_buy_freq == 5
	replace fuel_exp_m = fuel_pay                 if fuel_buy_freq == 6
	replace fuel_exp_m = fuel_pay / 2             if fuel_buy_freq == 7
	replace fuel_exp_m = fuel_pay / 3             if fuel_buy_freq == 8
	replace fuel_exp_m = fuel_pay / 4             if fuel_buy_freq == 9
	replace fuel_exp_m = fuel_pay / 5             if fuel_buy_freq == 10
	replace fuel_exp_m = fuel_pay / 6             if fuel_buy_freq == 11
	replace fuel_exp_m = (fuel_pay / 7) * 30 * 3  if fuel_buy_freq == 12
	replace fuel_exp_m = fuel_pay * 3             if fuel_buy_freq == 13
	replace fuel_exp_m = (fuel_pay / 2) * 30      if fuel_buy_freq == 14
	replace fuel_exp_m = fuel_pay / 12            if fuel_buy_freq == 15
	replace fuel_exp_m = fuel_pay / 24            if fuel_buy_freq == 16
	replace fuel_exp_m = (fuel_pay / 7) * 30 * 4  if fuel_buy_freq == 17
	replace fuel_exp_m = fuel_pay * 5             if fuel_buy_freq == 18
	replace fuel_exp_m = fuel_pay / 8             if fuel_buy_freq == 19
	replace fuel_exp_m = fuel_pay / 6             if fuel_buy_freq == 20
	replace fuel_exp_m = fuel_pay * 2             if fuel_buy_freq == 21
	replace fuel_exp_m = 0                        if fuel_buy_freq == 22
	replace fuel_exp_m = .                        if fuel_buy_freq == 23

	gen fuel_exp_yr = fuel_exp_m * nbr_month_fuel
	replace fuel_exp_m  = 0 if inlist(fuel_consumption__id, 3, 16)
	replace fuel_exp_yr = 0 if inlist(fuel_consumption__id, 3, 16)

	bys interview__id: egen fuel_exp_tot_m  = total(fuel_exp_m)
	bys interview__id: egen fuel_exp_tot_yr = total(fuel_exp_yr)
	gen fuel_exp_tot_ann_m = fuel_exp_tot_yr / 12

	keep interview__id fuel_exp_tot_m fuel_exp_tot_yr fuel_exp_tot_ann_m
	duplicates drop
	save "$wip_hh/tot_fuel_consumption.dta", replace

	use "$wip_hh/$master_dta", clear
	merge 1:1 interview__id using "$wip_hh/tot_fuel_consumption.dta", nogen
	recode fuel_exp_tot_m fuel_exp_tot_yr fuel_exp_tot_ann_m (. = 0)
	save "$wip_hh/$master_dta", replace


	*===========================================================================
	*  6. LIGHTING FUEL EXPENDITURE (FUEL_H11.DTA)
	*===========================================================================

	local fn_fuel_h11 = cond("$fn_fuel_h11" != "", "$fn_fuel_h11", "fuel_h11.dta")
	use "$raw_hh/`fn_fuel_h11'", clear
	capture confirm variable interview__id
	if _rc {
		capture confirm variable interview__key
		if !_rc clonevar interview__id = interview__key
	}
	capture confirm variable SEC_H_Q14
	if !_rc {
		* 4-question schema (Namibia): Q11=use, Q12=qty, Q13=freq, Q14=payment
		replace SEC_H_Q11 = 1 if SEC_H_Q11 == . & fuel_H11__id != 5
		keep if SEC_H_Q11 == 1

		gen lightfuel_buy_freq = SEC_H_Q13
		capture confirm variable SEC_H_Q13_oth
		if !_rc {
			replace lightfuel_buy_freq = 12 if SEC_H_Q13_oth == "3 times a week"
			replace lightfuel_buy_freq = 13 if SEC_H_Q13_oth == "4 times a month"
			replace lightfuel_buy_freq = 14 if SEC_H_Q13_oth == "for two days"
			replace lightfuel_buy_freq = 15 if inlist(SEC_H_Q13_oth, "once in a year", "every year", "Rarely in a year", "once a year")
			replace lightfuel_buy_freq = 16 if SEC_H_Q13_oth == "every 3 days"
			replace lightfuel_buy_freq = 17 if SEC_H_Q13_oth == "6 times in a month"
			replace lightfuel_buy_freq = 18 if SEC_H_Q13_oth == "twice a year"
			replace lightfuel_buy_freq = 19 if SEC_H_Q13_oth == "twice a month"
			replace lightfuel_buy_freq = 20 if inlist(SEC_H_Q13_oth, "Only when they need to", "Rarely", "They when they need it", "They only buy the whenever they need them", "When electricity goes off", "When the battery dies", "When there is no electricity") | inlist(SEC_H_Q13_oth, "When they need it", "When they need them", "When they need to", "When they needed", "only when they need to", "when she needs", "when she needs it") | inlist(SEC_H_Q13_oth, "when their solar is off", "when there is no electricity", "when they finish", "rarely")
			replace lightfuel_buy_freq = 21 if SEC_H_Q13_oth == "The lamb is not working"

			** Clean "As need arises" to mode
			replace lightfuel_buy_freq = 6 if lightfuel_buy_freq == 20 & fuel_H11__id == 1 // candle - monthly
			replace lightfuel_buy_freq = 6 if lightfuel_buy_freq == 20 & fuel_H11__id == 4 // kerosene - monthly
			replace lightfuel_buy_freq = 2 if lightfuel_buy_freq == 20 & fuel_H11__id == 5 // dry-cell - weekly
		}
		gen lightfuel_pay = SEC_H_Q14
	}
	else {
		* 3-question schema (Liberia/Standard Survey Solutions): Q11=qty, Q12=freq, Q13=payment
		gen lightfuel_buy_freq = SEC_H_Q12
		gen lightfuel_pay = SEC_H_Q13
	}
	gen fuellighting_exp_m = .
	replace fuellighting_exp_m = lightfuel_pay * 30            if lightfuel_buy_freq == 1
	replace fuellighting_exp_m = (lightfuel_pay / 7) * 30      if lightfuel_buy_freq == 2
	replace fuellighting_exp_m = (lightfuel_pay / 7) * 30 * 2  if lightfuel_buy_freq == 3
	replace fuellighting_exp_m = (lightfuel_pay / 14) * 30     if lightfuel_buy_freq == 4
	replace fuellighting_exp_m = (lightfuel_pay / 21) * 30     if lightfuel_buy_freq == 5
	replace fuellighting_exp_m = lightfuel_pay                 if lightfuel_buy_freq == 6
	replace fuellighting_exp_m = lightfuel_pay / 2             if lightfuel_buy_freq == 7
	replace fuellighting_exp_m = lightfuel_pay / 3             if lightfuel_buy_freq == 8
	replace fuellighting_exp_m = lightfuel_pay / 4             if lightfuel_buy_freq == 9
	replace fuellighting_exp_m = lightfuel_pay / 5             if lightfuel_buy_freq == 10
	replace fuellighting_exp_m = lightfuel_pay / 6             if lightfuel_buy_freq == 11
	replace fuellighting_exp_m = (lightfuel_pay / 7) * 30 * 3  if lightfuel_buy_freq == 12
	replace fuellighting_exp_m = lightfuel_pay * 4             if lightfuel_buy_freq == 13
	replace fuellighting_exp_m = (lightfuel_pay / 2) * 30      if lightfuel_buy_freq == 14
	replace fuellighting_exp_m = lightfuel_pay / 12            if lightfuel_buy_freq == 15
	replace fuellighting_exp_m = (lightfuel_pay / 3) * 30      if lightfuel_buy_freq == 16
	replace fuellighting_exp_m = lightfuel_pay * 6             if lightfuel_buy_freq == 17
	replace fuellighting_exp_m = lightfuel_pay / 6             if lightfuel_buy_freq == 18
	replace fuellighting_exp_m = lightfuel_pay * 2             if lightfuel_buy_freq == 19
	replace fuellighting_exp_m = .                             if lightfuel_buy_freq == 20
	replace fuellighting_exp_m = 0                             if lightfuel_buy_freq == 21

	gen fuellighting_exp_yr = fuellighting_exp_m * 12
	bys interview__id: egen lightfuel_exp_tot_m  = total(fuellighting_exp_m)
	bys interview__id: egen lightfuel_exp_tot_yr = total(fuellighting_exp_yr)

	keep interview__id lightfuel_exp_tot_m lightfuel_exp_tot_yr
	duplicates drop
	save "$wip_hh/hhtotal_lightfuel_expenditure.dta", replace

	use "$wip_hh/$master_dta", clear
	merge 1:1 interview__id using "$wip_hh/hhtotal_lightfuel_expenditure.dta", nogen
	recode lightfuel_exp_tot_m lightfuel_exp_tot_yr (. = 0)
	save "$wip_hh/$master_dta", replace


	*===========================================================================
	*  7. TOTAL HOUSEHOLD EXPENDITURE & POPULATION-WEIGHTED QUINTILES
	*===========================================================================

	use "$wip_hh/$master_dta", clear

	gen exp_total_m  = elec_exp_m + nonenergy_exp_m + fuel_exp_tot_ann_m + lightfuel_exp_tot_m
	gen exp_total_yr = elec_exp_yr + nonenergy_exp_yr + fuel_exp_tot_yr + lightfuel_exp_tot_yr
	lab var exp_total_m  "Monthly Total Household Expenditure (N$)"
	lab var exp_total_yr "Annual Total Household Expenditure (N$)"

	gen exp_pc_yr = exp_total_yr / max(1, hhsize)
	lab var exp_pc_yr "Annual Per Capita Household Expenditure"

	* Audit reference: Household-level total expenditure with household weights
	xtile hh_exp_quintile_hhlevel = exp_total_yr [pw=hh_wt], nq(5)
	lab var hh_exp_quintile_hhlevel "Expenditure Quintile (HH-level total expenditure)"

	* Primary: Per capita annual expenditure with population weights (World Bank / LSMS standard)
	xtile hh_exp_quintile = exp_pc_yr [pw=pop_wt], nq(5)
	lab define hh_exp_quintile 1 "Q1 (Poorest)" 2 "Q2" 3 "Q3" 4 "Q4" 5 "Q5 (Richest)", replace
	lab val hh_exp_quintile hh_exp_quintile
	lab var hh_exp_quintile "Expenditure Quintile (Per capita expenditure, pop-weighted Q1-Q5)"

	save "$wip_hh/$master_dta", replace


	*===========================================================================
	*  8. SOLAR ROSTER CLEANING & MAIN SOLAR DEVICE MATCHING
	*===========================================================================

	local fn_solar_device = cond("$fn_solar_device" != "", "$fn_solar_device", "solar_c_device.dta")
	use "$raw_hh/`fn_solar_device'", clear
	capture confirm variable interview__id
	if _rc {
		capture confirm variable interview__key
		if !_rc clonevar interview__id = interview__key
	}
	capture drop if Solar_C_Device__id == .

	replace SEC_C_Q123 = . if SEC_C_Q123 == 888

	capture confirm variable SEC_C_Q125_oth
	if !_rc {
		gen SEC_C_Q125_5 = 1 if regexm(lower(SEC_C_Q125_oth), "phone|cell|telef")
		replace SEC_C_Q122 = 1 if SEC_C_Q125_5 == 1
		gen SEC_C_Q125_6 = 1 if regexm(lower(SEC_C_Q125_oth), "freezer|fridge|gelad|congelad")
		gen SEC_C_Q125_7 = 1 if regexm(lower(SEC_C_Q125_oth), "air condition|ar condicionado|^ac$")
		gen SEC_C_Q125_8 = 1 if regexm(lower(SEC_C_Q125_oth), "pump|bomba")
		gen SEC_C_Q125_9 = 1 if regexm(lower(SEC_C_Q125_oth), "sew|costura")
	}

	capture confirm variable SEC_C_Q127_oth
	if !_rc {
		gen SEC_C_Q127__5 = 1 if regexm(lower(SEC_C_Q127_oth), "phone|cell|telef")
	}

	egen solar_tv        = rowmax(SEC_C_Q125__1 SEC_C_Q127__1)
	egen solar_fan       = rowmax(SEC_C_Q125__2 SEC_C_Q127__2)
	egen solar_fridge    = rowmax(SEC_C_Q125__3 SEC_C_Q127__3)
	egen solar_laptop    = rowmax(SEC_C_Q125__4 SEC_C_Q127__4)
	egen solar_phone     = rowmax(SEC_C_Q125__5 SEC_C_Q127__5 SEC_C_Q122)
	egen solar_appliance = rowmax(solar_tv solar_fan solar_fridge solar_laptop ///
		SEC_C_Q125_6 SEC_C_Q125_7 SEC_C_Q125_8 SEC_C_Q125_9)

	** Reclassify SEC_C_Q128b: 1=SL, 2=SLS, 3=SHS
	replace SEC_C_Q128b = 1 if SEC_C_Q128b != 1 & solar_appliance == 0 & SEC_C_Q123 < 2
	replace SEC_C_Q128b = 2 if SEC_C_Q128b != 2 & solar_appliance == 0 & (SEC_C_Q123 > 1 & SEC_C_Q123 != .)
	replace SEC_C_Q128b = 3 if SEC_C_Q128b != 3 & solar_appliance != 0
	replace SEC_C_Q128b = 1 if SEC_C_Q128b == 2 & solar_appliance == 0 & SEC_C_Q123 == .
	replace SEC_C_Q128b = 1 if SEC_C_Q128b == 3 & solar_appliance == 0 & SEC_C_Q123 == .
	save "$wip_hh/Solar_C_Device_clean.dta", replace

	** Filter main solar device by Q141
	use "$wip_hh/$master_dta", clear
	keep interview__id SEC_C_Q141
	merge 1:m interview__id using "$wip_hh/Solar_C_Device_clean.dta"
	keep if _merge == 3
	drop _merge
	keep if Solar_C_Device__id == SEC_C_Q141 & Solar_C_Device__id != .
	save "$wip_hh/main_solar_matched.dta", replace

	use "$wip_hh/$master_dta", clear
	merge 1:1 interview__id using "$wip_hh/main_solar_matched.dta", nogen

	** Reconcile SEC_C_Q162 with actual solar device type
	egen nbr_elec = rowtotal(SEC_C_Q02 SEC_C_Q40 SEC_C_Q78 SEC_C_Q100 SEC_C_Q117)
	lab var nbr_elec "Number of electricity sources (stacking)"

	replace SEC_C_Q162 = 4 if SEC_C_Q128b == 1 & inlist(SEC_C_Q162, 5, 6)
	replace SEC_C_Q162 = 5 if SEC_C_Q128b == 2 & inlist(SEC_C_Q162, 4, 6)
	replace SEC_C_Q162 = 6 if SEC_C_Q128b == 3 & inlist(SEC_C_Q162, 4, 5)

	replace SEC_C_Q162 = 1 if SEC_C_Q02 == 1 & inlist(SEC_C_Q162, 8, 111) & nbr_elec == 1
	replace SEC_C_Q162 = 4 if SEC_C_Q128b == 1 & (SEC_C_Q117 == 1 & inlist(SEC_C_Q162, 8, 111) & nbr_elec == 1)
	replace SEC_C_Q162 = 5 if SEC_C_Q128b == 2 & (SEC_C_Q117 == 1 & inlist(SEC_C_Q162, 8, 111) & nbr_elec == 1)
	replace SEC_C_Q162 = 6 if SEC_C_Q128b == 3 & (SEC_C_Q117 == 1 & inlist(SEC_C_Q162, 8, 111) & nbr_elec == 1)

	** Clean Q161_oth into appliance dummy variables
	capture drop SEC_C_Q161__7 SEC_C_Q161__8
	capture confirm variable SEC_C_Q161_oth
	if !_rc {
		gen SEC_C_Q161__7 = 1 if SEC_C_Q161_oth == "Air Conditioner and Power tools"
		lab var SEC_C_Q161__7 "Air Conditioner"
		capture replace SEC_C_Q161__555 = 0 if SEC_C_Q161_oth == "Air Conditioner and Power tools"

		gen SEC_C_Q161__8 = 1 if SEC_C_Q161_oth == "microwave"
		lab var SEC_C_Q161__8 "Microwave"
		capture replace SEC_C_Q161__555 = 0 if SEC_C_Q161_oth == "microwave"
	}

	save "$wip_hh/$master_dta", replace


	*===========================================================================
	*  9. COOKSTOVES ROSTER & STACKING (COOKSTOVES.DTA)
	*===========================================================================

	local fn_cookstoves = cond("$fn_cookstoves" != "", "$fn_cookstoves", "cookstoves.dta")
	local fn_stovefuel  = cond("$fn_stovefuel" != "", "$fn_stovefuel", "stove_fuel.dta")
	use "$raw_hh/`fn_cookstoves'", clear
	capture confirm variable interview__id
	if _rc {
		capture confirm variable interview__key
		if !_rc clonevar interview__id = interview__key
	}
	capture drop if cookstoves__id == .

	drop if SEC_G_Q03 == "Does not cook" | SEC_G_Q03 == "microwave oven"
	capture confirm variable SEC_G_Q05_oth
	if !_rc {
		replace SEC_G_Q05 = 1  if SEC_G_Q05_oth == "Fire wood" | SEC_G_Q05_oth == "Wood" | SEC_G_Q05_oth == "open fire on the ground"
		replace SEC_G_Q05 = 19 if SEC_G_Q05_oth == "four plate stove"
		replace SEC_G_Q05 = 23 if SEC_G_Q05_oth == "Gas-Eletric stove"
		replace SEC_G_Q05 = 22 if SEC_G_Q05_oth == "Traditional stove"
	}
	lab define SEC_G_Q05 1 "3-Stones/Open fire stove" 2 "Open Fire with a Stand" 3 "Elephant cook stove" ///
		4 "Portable Rocket Wood Stove" 5 "Mbaula stove" 6 "Indoor wood stove" 7 "Tso-Tso Stove" ///
		8 "Vesto" 9 "Pellet cook stove" 10 "Potable LPG Gas Stove (cylinder)" 11 "Potable LPG cartridge" ///
		12 "Handipack gas burner" 13 "Portable LPG burner" 14 "Gas stove canister" 15 "Biogas stove" ///
		16 "Biofuel Burner" 17 "Box Concentrator Solar" 18 "Open Concentrator Solar" 19 "Electric stove" ///
		20 "Jumbo Zama" 21 "Ezy Stove" 22 "Other traditional/locally built stove" 23 "Gas-electric stove" ///
		555 "Other, Specify", modify
	lab val SEC_G_Q05 SEC_G_Q05
	save "$wip_hh/cookstoves_clean.dta", replace

	** A. Extract and match main stove (cookstoves__id == SEC_G_Q04)
	use "$wip_hh/$master_dta", clear
	keep interview__id SEC_G_Q04
	merge 1:m interview__id using "$wip_hh/cookstoves_clean.dta"
	keep if _merge == 3
	drop _merge
	keep if cookstoves__id == SEC_G_Q04 & cookstoves__id != .
	save "$wip_hh/mainstove_matched.dta", replace

	use "$wip_hh/$master_dta", clear
	merge 1:1 interview__id using "$wip_hh/mainstove_matched.dta", nogen

	** Primary fuel for main stove (SEC_G_Q16)
	capture drop SEC_G_Q16
	gen SEC_G_Q16 = .
	forval f = 1/15 {
		capture confirm var SEC_G_Q16__`f'
		if !_rc replace SEC_G_Q16 = `f' if SEC_G_Q16__`f' == 1
	}
	capture confirm var SEC_G_Q16__111
	if !_rc replace SEC_G_Q16 = 111 if SEC_G_Q16__111 == 1
	replace SEC_G_Q16 = 16 if SEC_G_Q05 == 19 & SEC_G_Q16 == . // electric
	save "$wip_hh/$master_dta", replace

	** B. Match fuel availability for main stove (SEC_G_Q17 from stove_fuel.dta)
	preserve
		keep interview__id SEC_G_Q04 SEC_G_Q16
		save "$wip_hh/mainstove_key.dta", replace

		use "$raw_hh/`fn_stovefuel'", clear
		capture confirm variable interview__id
		if _rc {
			capture confirm variable interview__key
			if !_rc clonevar interview__id = interview__key
		}
		merge m:1 interview__id using "$wip_hh/mainstove_key.dta"
		keep if _merge == 3
		keep if cookstoves__id == SEC_G_Q04 & stove_fuel__id == SEC_G_Q16 & SEC_G_Q16 != .
		keep interview__id SEC_G_Q17
		duplicates drop
		save "$wip_hh/mainstove_fuel_avail.dta", replace
	restore

	merge 1:1 interview__id using "$wip_hh/mainstove_fuel_avail.dta", nogen

	** C. Stacking summary & time-weighted emission tier from cookstoves roster (Bryan's Methodology)
	preserve
		use "$wip_hh/cookstoves_clean.dta", clear
		
		* Stove ISO emission tier by stove type (SEC_G_Q05)
		gen emit_tier = .
		if "$country_iso3" == "GNB" | "$country" == "Guinea-Bissau" {
			replace emit_tier = 0 if inlist(SEC_G_Q05, 1, 2)
			replace emit_tier = 3 if inlist(SEC_G_Q05, 3)
			replace emit_tier = 1 if inlist(SEC_G_Q05, 4)
			replace emit_tier = 4 if inlist(SEC_G_Q05, 5, 6)
			replace emit_tier = 5 if inlist(SEC_G_Q05, 7, 8)
		}
		else {
			replace emit_tier = 0 if inlist(SEC_G_Q05, 1, 2, 3, 5, 22)
			replace emit_tier = 3 if inlist(SEC_G_Q05, 4, 6, 7, 8, 9, 20, 21)
			replace emit_tier = 4 if inlist(SEC_G_Q05, 10, 11, 12, 13, 14, 23)
			replace emit_tier = 5 if inlist(SEC_G_Q05, 15, 16, 17, 18, 19)
		}
		replace emit_tier = 0 if emit_tier == .
		
		* Weekly cooking time per stove
		gen double daily_mins = cond(SEC_G_Q21 < ., SEC_G_Q21, 0) + ///
		                        cond(SEC_G_Q22a < ., SEC_G_Q22a, 0) + ///
		                        cond(SEC_G_Q22b < ., SEC_G_Q22b, 0) + ///
		                        cond(SEC_G_Q22c < ., SEC_G_Q22c, 0)
		gen double days_week = cond(SEC_G_Q19 < ., SEC_G_Q19, 1)
		replace days_week = 1 if days_week < 1
		gen double weekly_time = daily_mins * days_week
		replace weekly_time = 1 if weekly_time <= 0
		
		gen double weighted_emit = emit_tier * weekly_time
		gen byte is_clean = (emit_tier >= 4)
		gen byte is_trad  = (emit_tier == 0)
		gen byte is_ics   = (emit_tier == 3)
		
		collapse (sum) weighted_emit weekly_time ///
		         (count) num_stoves = SEC_G_Q05 ///
		         (max) clean_stove = is_clean ///
		               trad_stove  = is_trad ///
		               ics         = is_ics, by(interview__id)
		
		gen double weighted_emit_tier = round(weighted_emit / weekly_time)
		replace weighted_emit_tier = 5 if weighted_emit_tier > 5 & weighted_emit_tier < .
		replace weighted_emit_tier = 0 if weighted_emit_tier < 0
		gen byte stove_stacking = (num_stoves >= 2)
		gen byte multi_biomass_stacking = (stove_stacking == 1 & clean_stove == 0)
		gen byte stacking_dilution = (clean_stove == 1 & (trad_stove == 1 | ics == 1))
		
		lab var weighted_emit_tier "Household cooking time-weighted emission tier (0-5)"
		lab var clean_stove        "Uses clean fuel stove (LPG/elec/biogas/solar)"
		lab var ics                "Uses Improved Cookstove (ICS)"
		lab var trad_stove         "Uses traditional stove / 3-stone fire"
		lab var stove_stacking     "Number of stoves owned"
		lab var multi_biomass_stacking "Stacks multiple biomass stoves"
		lab var stacking_dilution  "Stove stacking dilution: clean stove owner using biomass stove"
		
		keep interview__id clean_stove ics trad_stove stove_stacking multi_biomass_stacking weighted_emit_tier stacking_dilution
		duplicates drop
		save "$wip_hh/stoves_summary.dta", replace
	restore

	merge 1:1 interview__id using "$wip_hh/stoves_summary.dta", nogen
	recode clean_stove ics trad_stove multi_biomass_stacking (. = 0)
	replace stove_stacking = 0 if stove_stacking == .
	save "$wip_hh/$master_dta", replace


	*===========================================================================
	*  10. TIME USE: FUEL COLLECTION & COOKING TIME BY GENDER
	*===========================================================================

	local fn_time_coll = cond("$fn_time_coll" != "", "$fn_time_coll", "time_collecting.dta")
	local fn_time_use  = cond("$fn_time_use" != "", "$fn_time_use", "time_use.dta")

	** Fuel collection and prep time (time_collecting.dta)
	use "$raw_hh/`fn_time_coll'", clear
	capture confirm variable interview__id
	if _rc {
		capture confirm variable interview__key
		if !_rc clonevar interview__id = interview__key
	}

	capture confirm variable SEC_I_Q13_oth
	if !_rc {
		replace SEC_I_Q13 = 3  if inlist(lower(SEC_I_Q13_oth), "twice a week", "twice per week")
		replace SEC_I_Q13 = 12 if inlist(lower(SEC_I_Q13_oth), "3 times a week", "3 times per week", "three times a week")
		replace SEC_I_Q13 = 13 if inlist(lower(SEC_I_Q13_oth), "4 times a week", "4 times per week")
		replace SEC_I_Q13 = 14 if lower(SEC_I_Q13_oth) == "5 days a week"
		replace SEC_I_Q13 = 15 if inlist(lower(SEC_I_Q13_oth), "2 days", "after 2 days")
		replace SEC_I_Q13 = 16 if inlist(lower(SEC_I_Q13_oth), "once a year", "every year")
		replace SEC_I_Q13 = 17 if lower(SEC_I_Q13_oth) == "3 times a month"
		replace SEC_I_Q13 = 18 if inlist(lower(SEC_I_Q13_oth), "twice per month", "twice a month")
		replace SEC_I_Q13 = 19 if inlist(lower(SEC_I_Q13_oth), "as needed", "when needed", "occasionally", "rarely")
	}

	replace SEC_I_Q12 = 1440 if SEC_I_Q12 > 1440 & SEC_I_Q12 != .

	gen SEC_I_Q12_week = .
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*7          if SEC_I_Q13 == 1
	replace SEC_I_Q12_week = (SEC_I_Q12/60)            if SEC_I_Q13 == 2
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*2          if SEC_I_Q13 == 3
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*(7/14)     if SEC_I_Q13 == 4
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*(7/21)     if SEC_I_Q13 == 5
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*(7/30)     if SEC_I_Q13 == 6
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*(7/60)     if SEC_I_Q13 == 7
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*(7/90)     if SEC_I_Q13 == 8
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*(7/120)    if SEC_I_Q13 == 9
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*(7/150)    if SEC_I_Q13 == 10
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*(7/180)    if SEC_I_Q13 == 11
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*3          if SEC_I_Q13 == 12
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*4          if SEC_I_Q13 == 13
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*5          if SEC_I_Q13 == 14
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*(7/2)      if SEC_I_Q13 == 15
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*(7/360)    if SEC_I_Q13 == 16
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*(3*(7/30)) if SEC_I_Q13 == 17
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*(2*(7/30)) if SEC_I_Q13 == 18
	replace SEC_I_Q12_week = (SEC_I_Q12/60)*(7/30)     if SEC_I_Q13 == 19

	bys interview__id: egen SEC_I_Q12_total = total(SEC_I_Q12_week)
	gen SEC_I_Q14_week = (SEC_I_Q14/60)*7
	bys interview__id: egen SEC_I_Q14_total = total(SEC_I_Q14_week)
	gen cs_fcol_fpre = SEC_I_Q12_total + SEC_I_Q14_total
	lab var cs_fcol_fpre "Fuel collection + prep time (hr/week)"

	** Annual hours by demographic group (time_collecting__id: 1=Women 15+, 2=Girls <15, 3=Men 15+, 4=Boys <15)
	gen yr_coll_hr = SEC_I_Q12_week * 52
	gen women_fuel_hr_yr = yr_coll_hr if time_collecting__id == 1
	gen girls_fuel_hr_yr = yr_coll_hr if time_collecting__id == 2
	gen men_fuel_hr_yr   = yr_coll_hr if time_collecting__id == 3
	gen boys_fuel_hr_yr  = yr_coll_hr if time_collecting__id == 4

	bys interview__id: egen women_fuel_hr_yr_hh = total(women_fuel_hr_yr)
	bys interview__id: egen girls_fuel_hr_yr_hh = total(girls_fuel_hr_yr)
	bys interview__id: egen men_fuel_hr_yr_hh   = total(men_fuel_hr_yr)
	bys interview__id: egen boys_fuel_hr_yr_hh  = total(boys_fuel_hr_yr)

	keep interview__id SEC_I_Q12_total SEC_I_Q14_total cs_fcol_fpre ///
		women_fuel_hr_yr_hh men_fuel_hr_yr_hh girls_fuel_hr_yr_hh boys_fuel_hr_yr_hh
	duplicates drop
	save "$wip_hh/fuel_time.dta", replace

	** Cooking time by gender (time_use.dta)
	use "$raw_hh/`fn_time_use'", clear
	capture confirm variable interview__id
	if _rc {
		capture confirm variable interview__key
		if !_rc clonevar interview__id = interview__key
	}
	drop if SEC_L_Q02 > 1440 & SEC_L_Q02 != .a
	keep if inlist(time_use__id, 1, 2)   // women and girls
	bys interview__id: egen cooktime_female = total(SEC_L_Q02)
	keep interview__id cooktime_female
	duplicates drop
	save "$wip_hh/cooktime_female.dta", replace

	use "$raw_hh/`fn_time_use'", clear
	capture confirm variable interview__id
	if _rc {
		capture confirm variable interview__key
		if !_rc clonevar interview__id = interview__key
	}
	drop if SEC_L_Q02 > 1440 & SEC_L_Q02 != .a
	keep if inlist(time_use__id, 3, 4)   // men and boys
	bys interview__id: egen cooktime_male = total(SEC_L_Q02)
	keep interview__id cooktime_male
	duplicates drop
	save "$wip_hh/cooktime_male.dta", replace

	** Appliances aggregation from appliance.dta / appliances.dta
	preserve
		local fn_app = cond("$fn_appliance" != "", "$fn_appliance", "")
		if "`fn_app'" != "" {
			use "$raw_hh/`fn_app'", clear
		}
		else {
			capture confirm file "$raw_hh/appliances.dta"
			if !_rc {
				use "$raw_hh/appliances.dta", clear
			}
			else {
				use "$raw_hh/appliance.dta", clear
			}
		}
		capture confirm variable interview__id
		if _rc {
			capture confirm variable interview__key
			if !_rc clonevar interview__id = interview__key
		}
		capture clonevar appliances__id = appliance__id
		keep if SEC_F_Q02a > 0 & SEC_F_Q02a < .
		
		forvalues a = 1/42 {
			gen byte app_own_`a' = (appliances__id == `a')
		}

		gen byte is_verylow = inlist(appliances__id, 1, 2, 3, 4, 5, 6, 7, 28, 29)
		gen byte is_low     = inlist(appliances__id, 8, 9, 26, 30, 31, 32, 33)
		gen byte is_med     = inlist(appliances__id, 10, 15, 16, 17, 20, 21, 27, 35, 36)
		gen byte is_high    = inlist(appliances__id, 11, 13, 14, 18)
		gen byte is_veryhigh= inlist(appliances__id, 22, 23, 24, 25, 34)

		gen byte has_lights = inlist(appliances__id, 1, 2, 3, 4)
		gen byte has_charger= inlist(appliances__id, 28, 29)
		gen byte has_radio  = inlist(appliances__id, 6, 7)
		gen byte has_tv     = inlist(appliances__id, 30, 31, 32)
		gen byte has_fridge = inlist(appliances__id, 10, 17)
		gen byte has_iron   = (appliances__id == 13)
		gen byte has_fan    = (appliances__id == 9)
		gen byte has_micro  = (appliances__id == 11)
		gen byte has_wash   = (appliances__id == 18)
		gen byte has_ac     = (appliances__id == 22)
		gen byte has_geyser = inlist(appliances__id, 24, 25)
		gen byte has_torch  = (appliances__id == 5)

		collapse (max) is_verylow is_low is_med is_high is_veryhigh ///
			has_lights has_charger has_radio has_tv has_fridge has_iron ///
			has_fan has_micro has_wash has_ac has_geyser has_torch app_own_*, by(interview__id)

		lab var is_verylow  "Owns Very Low-Load Appliances (Tier 1)"
		lab var is_low      "Owns Low-Load Appliances (Tier 2)"
		lab var is_med      "Owns Medium-Load Appliances (Tier 3)"
		lab var is_high     "Owns High-Load Appliances (Tier 4)"
		lab var is_veryhigh "Owns Very High-Load Appliances (Tier 5)"
		lab var has_torch   "Owns torch/flashlight/lantern"

		save "$wip_hh/appliances_agg.dta", replace
	restore

	** Merge time use and appliances into master
	use "$wip_hh/$master_dta", clear
	merge 1:1 interview__id using "$wip_hh/fuel_time.dta", nogen
	merge 1:1 interview__id using "$wip_hh/cooktime_female.dta", nogen
	merge 1:1 interview__id using "$wip_hh/cooktime_male.dta", nogen
	merge 1:1 interview__id using "$wip_hh/appliances_agg.dta", nogen
	recode is_verylow is_low is_med is_high is_veryhigh ///
		has_lights has_charger has_radio has_tv has_fridge has_iron ///
		has_fan has_micro has_wash has_ac has_geyser has_torch app_own_* (. = 0)

	* Declare survey design on master
	svyset psu_id [pw=hh_wt], strata(strata_id) singleunit(centered)

	save "$wip_hh/$master_dta", replace
	di "========================================================="
	di " 00_build_master_dataset.do COMPLETE"
	di " Master dataset saved: $wip_hh/$master_dta"
	di " Total Observations: " _N
	di "========================================================="
