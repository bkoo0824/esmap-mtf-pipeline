
	**************************************************************************
	*  02_elec_attributes.do                                                 *
	*  Namibia MTF Pipeline — 7 Electricity Attribute Tiers                 *
	*                                                                        *
	*  Source logic: Namibia_electricityANDcooking.do (lines 796–2450)      *
	*                                                                        *
	*  Attributes produced (each 0–5):                                       *
	*    elc_cap_tier   — Capacity                                           *
	*    elc_avbl_tier  — Availability (daytime × evening, min)              *
	*    elc_rel_tier   — Reliability (outage freq + duration)               *
	*    elc_qual_tier  — Quality (voltage damage)                           *
	*    elc_leg_tier   — Formality (payment to authorized utility)          *
	*    elc_sft_tier   — Safety (electrocution/fire past 12 months)         *
	*    elc_affrd_tier — Affordability (365 kWh/yr < 5% HH expenditure)    *
	*                                                                        *
	*  Technology variable:                                                  *
	*    SEC_C_Q162:  1=Grid, 2=Mini-grid, 3=Generator, 4=Solar Lantern,    *
	*                 5=SLS, 6=SHS, 7=Rech Battery, 8=Dry-cell, 111=No elec *
	**************************************************************************

	use "$wip_hh/$master_dta", clear
	set more off

	* Shared tier label
	label define tier 0 "Tier 0" 1 "Tier 1" 2 "Tier 2" 3 "Tier 3" 4 "Tier 4" 5 "Tier 5", replace

	** Defensive safeguard: Ensure all possible source variables exist in master
	foreach v in SEC_C_Q27 SEC_C_Q28 SEC_C_Q29 SEC_C_Q30a SEC_C_Q30b SEC_C_Q35 SEC_C_Q38 SEC_C_Q12 ///
	             SEC_C_Q65 SEC_C_Q66 SEC_C_Q67 SEC_C_Q68a SEC_C_Q68b SEC_C_Q73 SEC_C_Q76 SEC_C_Q48 ///
	             SEC_C_Q93 SEC_C_Q94 SEC_C_Q98 ///
	             SEC_C_Q111 SEC_C_Q112 SEC_C_Q116 ///
	             SEC_C_Q148 SEC_C_Q149 SEC_C_Q152 ///
	             SEC_C_Q117 SEC_C_Q122 SEC_C_Q124 SEC_C_Q125__111 SEC_C_Q161_oth {
		capture confirm var `v'
		if _rc gen `v' = .
	}
	forval i = 1/35 {
		capture confirm var SEC_F_Q01__`i'
		if _rc gen SEC_F_Q01__`i' = 0
	}
	forval i = 1/8 {
		capture confirm var SEC_C_Q161__`i'
		if _rc gen SEC_C_Q161__`i' = 0
	}
	forval i = 1/4 {
		capture confirm var SEC_C_Q125__`i'
		if _rc gen SEC_C_Q125__`i' = 0
	}
	forval i = 1/5 {
		capture confirm var SEC_C_Q127__`i'
		if _rc gen SEC_C_Q127__`i' = 0
	}

	** Convenience variables (if not already defined)
	capture drop mob_chrge radio
	gen mob_chrge = (SEC_C_Q122 == 1) if SEC_C_Q117 == 1
	gen radio     = (SEC_C_Q124 == 1) if SEC_C_Q117 == 1


	*===========================================================================
	*  A. CAPACITY TIER
	*  Grid/Mini-grid → Tier 5 (assume sufficient capacity)
	*  Generator, SHS, Rech Battery → based on highest appliance used
	*  SLS, Solar Lantern → fractional score per household size
	*===========================================================================

	** (1) RECHARGEABLE BATTERY (HHs whose electricity source is rech batt only)
	gen rech_app_tier = .
	replace rech_app_tier = 1 if nbr_elec==1 & SEC_C_Q162==7 & (SEC_F_Q01__1==1 | SEC_F_Q01__2==1 | SEC_F_Q01__3==1 | SEC_F_Q01__4==1 | SEC_F_Q01__7==1 | SEC_F_Q01__28==1 | SEC_F_Q01__29==1 | SEC_F_Q01__33==1)
	replace rech_app_tier = 2 if nbr_elec==1 & SEC_C_Q162==7 & (SEC_F_Q01__8==1 | SEC_F_Q01__9==1 | SEC_F_Q01__30==1 | SEC_F_Q01__31==1 | SEC_F_Q01__32==1 | SEC_F_Q01__26==1)
	replace rech_app_tier = 3 if nbr_elec==1 & SEC_C_Q162==7 & (SEC_F_Q01__10==1 | SEC_F_Q01__15==1 | SEC_F_Q01__16==1 | SEC_F_Q01__17==1 | SEC_F_Q01__21==1 | SEC_F_Q01__27==1)
	replace rech_app_tier = 4 if nbr_elec==1 & SEC_C_Q162==7 & (SEC_F_Q01__14==1 | SEC_F_Q01__18==1 | SEC_F_Q01__11==1 | SEC_F_Q01__13==1)
	replace rech_app_tier = 5 if nbr_elec==1 & SEC_C_Q162==7 & (SEC_F_Q01__22==1 | SEC_F_Q01__23==1 | SEC_F_Q01__24==1 | SEC_F_Q01__25==1)
	lab val rech_app_tier tier
	lab var rech_app_tier "Appliance power tier (rechargeable battery)"

	** (2) GENERATOR (HHs whose electricity source is generator only)
	gen gen_app_tier = .
	replace gen_app_tier = 1 if nbr_elec==1 & SEC_C_Q162==3 & (SEC_F_Q01__1==1 | SEC_F_Q01__2==1 | SEC_F_Q01__3==1 | SEC_F_Q01__4==1 | SEC_F_Q01__7==1 | SEC_F_Q01__28==1 | SEC_F_Q01__29==1 | SEC_F_Q01__33==1)
	replace gen_app_tier = 2 if nbr_elec==1 & SEC_C_Q162==3 & (SEC_F_Q01__8==1 | SEC_F_Q01__9==1 | SEC_F_Q01__30==1 | SEC_F_Q01__31==1 | SEC_F_Q01__32==1 | SEC_F_Q01__26==1)
	replace gen_app_tier = 3 if nbr_elec==1 & SEC_C_Q162==3 & (SEC_F_Q01__10==1 | SEC_F_Q01__15==1 | SEC_F_Q01__16==1 | SEC_F_Q01__17==1 | SEC_F_Q01__21==1 | SEC_F_Q01__27==1)
	replace gen_app_tier = 4 if nbr_elec==1 & SEC_C_Q162==3 & (SEC_F_Q01__14==1 | SEC_F_Q01__18==1 | SEC_F_Q01__11==1 | SEC_F_Q01__13==1)
	replace gen_app_tier = 5 if nbr_elec==1 & SEC_C_Q162==3 & (SEC_F_Q01__22==1 | SEC_F_Q01__23==1 | SEC_F_Q01__24==1 | SEC_F_Q01__25==1)
	lab val gen_app_tier tier
	lab var gen_app_tier "Appliance power tier (generator)"

	** Clean Q161_oth into appliance dummy variables (if not already done)
	capture confirm var SEC_C_Q161__7
	if _rc {
		gen SEC_C_Q161__7 = (SEC_C_Q161_oth == "Air Conditioner and Power tools")
		lab var SEC_C_Q161__7 "Air Conditioner"
	}
	capture confirm var SEC_C_Q161__8
	if _rc {
		gen SEC_C_Q161__8 = (SEC_C_Q161_oth == "microwave")
		lab var SEC_C_Q161__8 "Microwave"
	}

	** Ensure other-specified solar appliance variables exist
	foreach v in SEC_C_Q125_5 SEC_C_Q125_6 SEC_C_Q125_7 SEC_C_Q125_8 SEC_C_Q125_9 {
		capture confirm var `v'
		if _rc gen `v' = 0
	}

	** Appliance power level for solar (main solar source)
	gen solar_app_tier = .
	replace solar_app_tier = 0 if inlist(SEC_C_Q162, 4, 5, 6) & SEC_C_Q125__111 == 1
	replace solar_app_tier = 1 if inlist(SEC_C_Q162, 4, 5, 6) & ///
		(SEC_C_Q161__1==1 | SEC_C_Q161__2==1 | SEC_C_Q125_5==1)
	replace solar_app_tier = 2 if inlist(SEC_C_Q162, 4, 5, 6) & ///
		(SEC_C_Q125__1==1 | SEC_C_Q125__2==1 | SEC_C_Q125__4==1 | SEC_C_Q125_9==1 | SEC_C_Q161__3==1 | SEC_C_Q161__4==1)
	replace solar_app_tier = 3 if inlist(SEC_C_Q162, 4, 5, 6) & ///
		(SEC_C_Q125__3==1 | SEC_C_Q125_6==1 | SEC_C_Q125_8==1 | SEC_C_Q161__5==1)
	replace solar_app_tier = 4 if inlist(SEC_C_Q162, 4, 5, 6) & SEC_C_Q161__8 == 1
	replace solar_app_tier = 5 if inlist(SEC_C_Q162, 4, 5, 6) & ///
		(SEC_C_Q161__7==1 | SEC_C_Q125_7==1)
	lab val solar_app_tier tier
	lab var solar_app_tier "Appliance power tier (solar)"

	** Combined appliance power across all off-grid tech
	gen applpower = .
	replace applpower = 0 if solar_app_tier == 0
	forval lv = 1/5 {
		replace applpower = `lv' if applpower==. & ///
			(rech_app_tier==`lv' | gen_app_tier==`lv' | solar_app_tier==`lv')
	}

	** Capacity tier
	gen elc_cap_tier5 = (SEC_C_Q162==1 | SEC_C_Q162==2) | ///
		((inlist(SEC_C_Q162, 3, 6, 7)) & applpower==5)
	gen elc_cap_tier4 = inlist(SEC_C_Q162, 3, 6, 7) & applpower==4
	gen elc_cap_tier3 = inlist(SEC_C_Q162, 3, 6, 7) & applpower==3
	gen elc_cap_tier2 = (inlist(SEC_C_Q162, 3, 7) & applpower==2) | ///
		(SEC_C_Q162==6 & applpower<=2)
	gen elc_cap_tier1 = inlist(SEC_C_Q162, 3, 7) & (applpower==. | applpower < 2)

	gen elc_cap_tier0 = inlist(SEC_C_Q162, 8, 111)

	** Solar Lantern (SL) and SLS sub-tier: fractional score
	gen elc_cap_tier01 = .
	replace elc_cap_tier01 = 2/hhsize if SEC_C_Q162 == 5         // SLS
	replace elc_cap_tier01 = 0.7      if SEC_C_Q162 == 5 & elc_cap_tier01 > 0.7 & elc_cap_tier01 != .
	replace elc_cap_tier01 = elc_cap_tier01 + 0.3 if SEC_C_Q162 == 5 & (mob_chrge==1 | radio==1)
	replace elc_cap_tier01 = 1/hhsize if SEC_C_Q162 == 4         // SL
	replace elc_cap_tier01 = 0.7      if SEC_C_Q162 == 4 & elc_cap_tier01 > 0.7 & elc_cap_tier01 != .
	replace elc_cap_tier01 = elc_cap_tier01 + 0.3 if SEC_C_Q162 == 4 & (mob_chrge==1 | radio==1)

	* Weighted mean cut-off for SL/SLS
	quietly sum elc_cap_tier01 [aw=hh_wt]
	local sl_cutoff = r(mean)
	replace elc_cap_tier1 = 1 if elc_cap_tier01 > `sl_cutoff' & elc_cap_tier01 != .
	replace elc_cap_tier0 = 1 if elc_cap_tier01 <= `sl_cutoff' & elc_cap_tier01 != .

	* Final capacity tier variable
	gen elc_cap_tier = 0 if elc_cap_tier0 == 1
	forval lv = 1/5 {
		replace elc_cap_tier = `lv' if elc_cap_tier`lv' == 1
	}
	lab val elc_cap_tier tier
	lab var elc_cap_tier "Electricity: Capacity Tier (0–5)"


	*===========================================================================
	*  B. AVAILABILITY TIER
	*  Day+Night availability (Tier 0/2/3/4/5) × Evening availability (0/1/2/3/5)
	*  Aggregate = min(day tier, evening tier)
	*  Missing imputed by cluster mode for grid; tech mode for solar
	*===========================================================================

	** Unify day/night and evening hours across technologies
	gen dur_day = .
	replace dur_day = SEC_C_Q27  if SEC_C_Q162 == 1  // grid
	replace dur_day = SEC_C_Q65  if SEC_C_Q162 == 2  // mini-grid
	replace dur_day = SEC_C_Q93  if SEC_C_Q162 == 3  // generator
	replace dur_day = SEC_C_Q148 if inlist(SEC_C_Q162, 4, 5, 6) // solar
	replace dur_day = SEC_C_Q111 if SEC_C_Q162 == 7  // rech battery
	replace dur_day = . if dur_day == 888

	gen dur_eve = .
	replace dur_eve = SEC_C_Q28  if SEC_C_Q162 == 1
	replace dur_eve = SEC_C_Q66  if SEC_C_Q162 == 2
	replace dur_eve = SEC_C_Q94  if SEC_C_Q162 == 3
	replace dur_eve = SEC_C_Q149 if inlist(SEC_C_Q162, 4, 5, 6)
	replace dur_eve = SEC_C_Q112 if SEC_C_Q162 == 7
	replace dur_eve = . if dur_eve == 888

	** Day tier
	gen elc_durd_tier = 5 if dur_day >= 23 & dur_day < .
	replace elc_durd_tier = 4 if dur_day < 23
	replace elc_durd_tier = 3 if dur_day < 16
	replace elc_durd_tier = 2 if dur_day < 8
	replace elc_durd_tier = 0 if dur_day < 4
	lab val elc_durd_tier tier
	lab var elc_durd_tier "Day & Night Availability Tier"

	** Evening tier
	gen elc_dure_tier = 5 if dur_eve == 4
	replace elc_dure_tier = 3 if dur_eve < 4
	replace elc_dure_tier = 2 if dur_eve < 3
	replace elc_dure_tier = 1 if dur_eve < 2
	replace elc_dure_tier = 0 if dur_eve < 1
	lab val elc_dure_tier tier
	lab var elc_dure_tier "Evening Availability Tier (18–22h)"

	** Missing value imputation (cluster mode for grid; tech mode for others)
	sort SEC_A_Q05
	foreach tech_code in 1 {         // grid: cluster-level imputation
		foreach stub in durd dure {
			egen mode_`stub'_`tech_code' = mode(elc_`stub'_tier) ///
				if SEC_C_Q162 == `tech_code', min by(SEC_A_Q05)
			replace elc_`stub'_tier = mode_`stub'_`tech_code' ///
				if SEC_C_Q162 == `tech_code' & elc_`stub'_tier == .
		}
	}
	foreach tech_code in 4 5 6 {     // solar types: technology-level imputation
		foreach stub in durd dure {
			egen mode_`stub'_`tech_code' = mode(elc_`stub'_tier) ///
				if SEC_C_Q162 == `tech_code', min
			replace elc_`stub'_tier = mode_`stub'_`tech_code' ///
				if SEC_C_Q162 == `tech_code' & elc_`stub'_tier == .
		}
	}

	** Aggregate availability tier = min(day, evening)
	egen elc_avbl_tier = rmin(elc_durd_tier elc_dure_tier) ///
		if elc_durd_tier != . & elc_dure_tier != .
	lab val elc_avbl_tier tier
	lab var elc_avbl_tier "Electricity: Availability Tier (min of day & evening)"


	*===========================================================================
	*  C. RELIABILITY TIER  (grid + mini-grid only)
	*  Based on outage frequency (per week) + total outage duration (hrs/wk)
	*  Tier 3: >14/wk  |  Tier 4: 3–14/wk OR ≤3 with ≥2h  |  Tier 5: ≤3 & <2h
	*  Non-grid HHs: left as missing (only grid/mini-grid face outages)
	*===========================================================================

	** Grid outage duration (hours + minutes → decimal hours)
	gen SEC_C_Q30_hr  = SEC_C_Q30a
	replace SEC_C_Q30_hr  = . if SEC_C_Q30_hr  == 888
	replace SEC_C_Q30_hr  = 0 if inlist(SEC_C_Q29, 0, 111)    // "no outages"
	gen SEC_C_Q30_min = SEC_C_Q30b
	replace SEC_C_Q30_min = . if SEC_C_Q30_min == 888
	replace SEC_C_Q30_min = 0 if inlist(SEC_C_Q29, 0, 111)
	replace SEC_C_Q30_min = 0 if SEC_C_Q30_hr != . & SEC_C_Q30_min == .
	replace SEC_C_Q30_hr  = 0 if SEC_C_Q30_hr == . & SEC_C_Q30_min != .
	gen SEC_C_Q30 = SEC_C_Q30_hr + (SEC_C_Q30_min / 60)

	** Mini-grid outage duration
	gen SEC_C_Q68_hr  = SEC_C_Q68a
	replace SEC_C_Q68_hr  = . if SEC_C_Q68_hr  == 888
	replace SEC_C_Q68_hr  = 0 if inlist(SEC_C_Q67, 0, 111)
	gen SEC_C_Q68_min = SEC_C_Q68b
	replace SEC_C_Q68_min = . if SEC_C_Q68_min == 888
	replace SEC_C_Q68_min = 0 if inlist(SEC_C_Q67, 0, 111)
	gen SEC_C_Q68 = SEC_C_Q68_hr + (SEC_C_Q68_min / 60)

	foreach v in SEC_C_Q29 SEC_C_Q30 SEC_C_Q67 SEC_C_Q68 {
		replace `v' = . if `v' == 888
	}
	foreach v in SEC_C_Q29 SEC_C_Q67 {
		replace `v' = 0 if `v' == 111   // "no outages" → 0
	}

	gen dis_frq = SEC_C_Q29 if SEC_C_Q162 == 1
	replace dis_frq = SEC_C_Q67 if SEC_C_Q162 == 2
	replace dis_frq = 0 if dis_frq == . & SEC_C_Q30 != .   // has duration but no frequency

	gen dis_dur = SEC_C_Q30 if SEC_C_Q162 == 1
	replace dis_dur = SEC_C_Q68 if SEC_C_Q162 == 2

	** Reliability tier
	gen elc_rel_tier = 3 if dis_frq > 14 & dis_frq != .
	replace elc_rel_tier = 4 if (dis_frq > 3 & dis_frq <= 14) | (dis_frq <= 3 & dis_dur >= 2)
	replace elc_rel_tier = 5 if dis_frq <= 3 & dis_dur < 2
	lab val elc_rel_tier tier
	lab var elc_rel_tier "Electricity: Reliability Tier (grid/mini-grid only)"

	** Impute missing via cluster mode
	sort SEC_A_Q05
	foreach code in 1 2 {
		local lbl = cond(`code'==1, "grid", "minigrid")
		egen rel_mode_`lbl' = mode(elc_rel_tier) if SEC_C_Q162==`code', min by(SEC_A_Q05)
		replace elc_rel_tier = rel_mode_`lbl' if SEC_C_Q162==`code' & elc_rel_tier==.
	}


	*===========================================================================
	*  D. QUALITY TIER  (grid + mini-grid only)
	*  Binary: appliance damaged by voltage fluctuation in past 12 months
	*  Tier 3 = damaged, Tier 5 = not damaged
	*===========================================================================

	gen appl_dam = .
	replace appl_dam = 0 if (SEC_C_Q35==0 & SEC_C_Q162==1) | (SEC_C_Q73==0 & SEC_C_Q162==2)
	replace appl_dam = 1 if (SEC_C_Q35==1 & SEC_C_Q162==1) | (SEC_C_Q73==1 & SEC_C_Q162==2)

	gen elc_qual_tier = 3 if appl_dam == 1
	replace elc_qual_tier = 5 if appl_dam == 0
	lab val elc_qual_tier tier
	lab var elc_qual_tier "Electricity: Quality Tier (voltage damage)"

	sort SEC_A_Q05
	foreach code in 1 2 {
		local lbl = cond(`code'==1, "grid", "minigrid")
		capture egen qual_mode_`lbl' = mode(elc_qual_tier) if SEC_C_Q162==`code', min by(SEC_A_Q05)
		replace elc_qual_tier = qual_mode_`lbl' if SEC_C_Q162==`code' & elc_qual_tier==.
	}


	*===========================================================================
	*  E. FORMALITY TIER  (grid + mini-grid only)
	*  Tier 3 = no payment (free/unauthorized), Tier 5 = payment to utility
	*===========================================================================

	gen elec_pay = .
	replace elec_pay = 1 if (SEC_C_Q12 != 111 & SEC_C_Q162==1) | (SEC_C_Q48 != 111 & SEC_C_Q162==2)
	replace elec_pay = 0 if (SEC_C_Q12 == 111 & SEC_C_Q162==1) | (SEC_C_Q48 == 111 & SEC_C_Q162==2)

	gen elc_leg_tier = 3 if elec_pay == 0
	replace elc_leg_tier = 5 if elec_pay == 1
	lab val elc_leg_tier tier
	lab var elc_leg_tier "Electricity: Formality Tier"


	*===========================================================================
	*  F. SAFETY TIER  (all electricity technologies)
	*  Tier 3 = accident/death in past 12 months; Tier 5 = no accident
	*===========================================================================

	gen elec_injury = ///
		(SEC_C_Q38==1  & SEC_C_Q162==1) | ///   // grid
		(SEC_C_Q76==1  & SEC_C_Q162==2) | ///   // mini-grid
		(SEC_C_Q98==1  & SEC_C_Q162==3) | ///   // generator
		(SEC_C_Q116==1 & SEC_C_Q162==7) | ///   // rech battery
		(SEC_C_Q152==1 & inlist(SEC_C_Q162, 4, 5, 6)) // solar
	replace elec_injury = . if inlist(SEC_C_Q162, 8, 111)   // no electricity

	gen elc_sft_tier = 3 if elec_injury == 1
	replace elc_sft_tier = 5 if elec_injury == 0
	lab val elc_sft_tier tier
	lab var elc_sft_tier "Electricity: Safety Tier (injury/accident past 12mo)"


	*===========================================================================
	*  G. AFFORDABILITY TIER (MTF standard: 365 kWh/yr < 5% HH expenditure)
	*  Tariff: ERONGO RED FY24/25 average = N$2.7072/kWh
	*  Threshold: cost of 365 kWh/yr ÷ annual HH expenditure < 5%
	*  Tier 2 = unaffordable (≥5%); Tier 5 = affordable (<5%)
	*===========================================================================

	local tariff_avg = 2.7072   // N$/kWh, average of prepaid and postpaid

	gen elec_cost_365kwh = `tariff_avg' * 365
	lab var elec_cost_365kwh "Annual cost of 365 kWh at Erongo RED FY24/25 tariff (N$)"

	gen elec_share_365kwh = elec_cost_365kwh / exp_total_yr   // may be missing if exp==0
	lab var elec_share_365kwh "Share of 365 kWh annual cost in total HH expenditure"

	gen elc_affrd_tier = 2 if elec_share_365kwh >= 0.05 & elec_share_365kwh != .
	replace elc_affrd_tier = 5 if elec_share_365kwh < 0.05 & elec_share_365kwh != .
	lab val elc_affrd_tier tier
	lab var elc_affrd_tier "Electricity: Affordability Tier (365kWh/yr < 5% HH exp)"


	*---------------------------------------------------------------------------
	* Save
	*---------------------------------------------------------------------------
	save "$wip_hh/$master_dta", replace
	di " 02_elec_attributes.do complete"
