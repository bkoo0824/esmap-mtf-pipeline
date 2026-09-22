
	**************************************************************************
	*  06_analytical_enhancements.do                                         *
	*  Namibia MTF Pipeline — 4 "So What?" Analytical Enhancements          *
	*                                                                        *
	*  Toggled by: global run_enhancements 1  (set in Master.do)            *
	*                                                                        *
	*  Enhancement 1: Attribute Deficit Gap                                  *
	*    For grid-connected HHs: which attribute pulls tier below Tier 4?   *
	*  Enhancement 2: Stove Stacking Dilution                                *
	*    HHs owning clean stoves but remaining in Exposure Tier 0–1        *
	*  Enhancement 3: Fuel Collection Opportunity Cost                       *
	*    Women's annual fuel collection hours → equivalent working days      *
	*  Enhancement 4: Technology–Tier Alignment                              *
	*    Mean tier by electricity technology (solar lanterns stuck at T1?)   *
	**************************************************************************

	use "$wip_hh/$master_dta", clear
	set more off

	capture confirm variable grid_hh
	if _rc gen byte grid_hh = (elec_tech_type == 1)

	capture confirm variable solar_hh
	if _rc gen byte solar_hh = inlist(elec_tech_type, 4, 5, 6)


	*===========================================================================
	*  ENHANCEMENT 1: ATTRIBUTE DEFICIT GAP
	*  For grid-connected households (elec_tech_type == 1):
	*  Flag which attribute is the binding constraint pulling aggregate < Tier 4
	*===========================================================================

	* For grid HHs: identify which attribute(s) = binding constraint at < Tier 4
	foreach attr in cap avbl rel qual affrd leg sft {
		gen deficit_`attr' = (elc_`attr'_tier < 4) if elec_tech_type == 1
		lab var deficit_`attr' "Grid HH deficit: `attr' tier < Tier 4"
	}
	* Use adjusted tiers for optional attributes
	replace deficit_rel  = (elc_rel_tier_adj  < 4) if elec_tech_type == 1
	replace deficit_qual = (elc_qual_tier_adj < 4) if elec_tech_type == 1
	replace deficit_leg  = (elc_leg_tier_adj  < 4) if elec_tech_type == 1

	* Overall: grid HH below Tier 4
	gen deficit_any = (elc_aggr_tier < 4) if elec_tech_type == 1
	lab var deficit_any "Grid HH with aggregate tier < Tier 4 (any deficit)"

	* Which attribute is the binding minimum (causes the lowest aggregate)
	gen binding_attr = ""
	foreach attr in cap avbl rel qual affrd leg sft {
		replace binding_attr = "`attr'" ///
			if elec_tech_type == 1 & elc_`attr'_tier == elc_aggr_tier & elc_aggr_tier < 4
	}
	lab var binding_attr "Binding deficit attribute for grid HH below Tier 4"


	*===========================================================================
	*  ENHANCEMENT 2: STOVE STACKING DILUTION
	*  Flag: owns clean fuel stove but Exposure tier ≤ 1 (biomass stacking)
	*===========================================================================

	gen stacking_dilution = 0
	replace stacking_dilution = 1 if ///
		clean_stove == 1 &         /// owns a clean fuel stove
		cs_exp_tier <= 1 &         /// exposure tier pulled down by biomass use
		cs_exp_tier != .
	lab define stacking_dilution 0 "No dilution" 1 "Stove stacking dilution", replace
	lab val stacking_dilution stacking_dilution
	lab var stacking_dilution "Stove stacking dilution: clean stove owner but Exposure Tier ≤1"

	* Sub-flag: owns BOTH clean stove AND traditional stove
	gen own_both_stoves = (clean_stove == 1 & trad_stove == 1)
	lab var own_both_stoves "Owns both clean fuel AND traditional stove (stacking risk)"


	*===========================================================================
	*  ENHANCEMENT 3: FUEL COLLECTION OPPORTUNITY COST
	*  Women's annual fuel collection hours → equivalent working days (÷8)
	*  Source: time_collecting.dta  — individual-level, filtered by sex/age
	*===========================================================================

	preserve
		use "$raw_hh/time_collecting.dta", clear

		* Recode frequency
		replace SEC_I_Q12 = 1440 if SEC_I_Q12 > 1440 & SEC_I_Q12 != .
		gen wk_coll = .
		replace wk_coll = (SEC_I_Q12/60)*7           if SEC_I_Q13 == 1
		replace wk_coll = (SEC_I_Q12/60)             if SEC_I_Q13 == 2
		replace wk_coll = (SEC_I_Q12/60)*2           if SEC_I_Q13 == 3
		replace wk_coll = (SEC_I_Q12/60)*(7/14)      if SEC_I_Q13 == 4
		replace wk_coll = (SEC_I_Q12/60)*(7/21)      if SEC_I_Q13 == 5
		replace wk_coll = (SEC_I_Q12/60)*(7/30)      if SEC_I_Q13 == 6
		replace wk_coll = (SEC_I_Q12/60)*(7/60)      if SEC_I_Q13 == 7
		replace wk_coll = (SEC_I_Q12/60)*(7/90)      if SEC_I_Q13 == 8
		replace wk_coll = (SEC_I_Q12/60)*(7/120)     if SEC_I_Q13 == 9
		replace wk_coll = (SEC_I_Q12/60)*(7/30)      if SEC_I_Q13 == 19  // as needed → monthly

		** Annual hours
		gen yr_coll_hr = wk_coll * 52

		** By demographic group directly from time_collecting__id:
		** 1=Women 15+, 2=Girls <15, 3=Men 15+, 4=Boys <15
		gen women_fuel_hr_yr = yr_coll_hr if time_collecting__id == 1
		gen girls_fuel_hr_yr = yr_coll_hr if time_collecting__id == 2
		gen men_fuel_hr_yr   = yr_coll_hr if time_collecting__id == 3
		gen boys_fuel_hr_yr  = yr_coll_hr if time_collecting__id == 4

		bys interview__id: egen women_fuel_hr_yr_hh = total(women_fuel_hr_yr)
		bys interview__id: egen girls_fuel_hr_yr_hh = total(girls_fuel_hr_yr)
		bys interview__id: egen men_fuel_hr_yr_hh   = total(men_fuel_hr_yr)
		bys interview__id: egen boys_fuel_hr_yr_hh  = total(boys_fuel_hr_yr)

		keep interview__id women_fuel_hr_yr_hh men_fuel_hr_yr_hh ///
			girls_fuel_hr_yr_hh boys_fuel_hr_yr_hh
		duplicates drop
		save "$wip_hh/fuel_time_by_sex.dta", replace
	restore

	merge 1:1 interview__id using "$wip_hh/fuel_time_by_sex.dta", nogen

	** Equivalent working days (÷8 hrs/day) and school days lost
	gen women_fuel_workdays_yr = women_fuel_hr_yr_hh / 8
	gen girls_fuel_schooldays_yr = girls_fuel_hr_yr_hh / 8
	lab var women_fuel_hr_yr_hh    "Women 15+: annual fuel collection hours"
	lab var men_fuel_hr_yr_hh      "Men 15+: annual fuel collection hours"
	lab var girls_fuel_hr_yr_hh    "Girls <15: annual fuel collection hours"
	lab var boys_fuel_hr_yr_hh     "Boys <15: annual fuel collection hours"
	lab var women_fuel_workdays_yr "Women 15+: equivalent working days/yr lost to fuel collection (÷8h)"
	lab var girls_fuel_schooldays_yr "Girls <15: equivalent school days/yr lost to fuel collection (÷8h)"


	*===========================================================================
	*  ENHANCEMENT 4: TECHNOLOGY–TIER ALIGNMENT
	*  Flag: solar lantern users (elec_tech_type==6) with mean aggregate tier ≤ 1
	*  Compare mean tier by technology type
	*===========================================================================

	gen sl_tier1_stuck = (elec_tech_type == 6 & elc_aggr_tier <= 1)
	lab var sl_tier1_stuck "Solar Lantern user stuck at Tier 0 or 1"

	gen shs_tier2plus = (elec_tech_type == 4 & elc_aggr_tier >= 2)
	lab var shs_tier2plus "SHS user achieving Tier 2 or above"


	*===========================================================================
	*  ENHANCEMENT 5: GRID CONNECTION BARRIERS & "UNDER THE GRID" UPTAKE
	*===========================================================================

	* Barriers among unconnected households (SEC_C_Q03)
	capture drop barrier_cost barrier_dist barrier_tariff barrier_landlord barrier_unrel barrier_admin
	gen byte barrier_cost     = (SEC_C_Q03 == 1) if grid_hh == 0 & SEC_C_Q03 < .
	gen byte barrier_dist     = (SEC_C_Q03 == 2) if grid_hh == 0 & SEC_C_Q03 < .
	gen byte barrier_tariff   = (SEC_C_Q03 == 3) if grid_hh == 0 & SEC_C_Q03 < .
	gen byte barrier_landlord = (SEC_C_Q03 == 4) if grid_hh == 0 & SEC_C_Q03 < .
	gen byte barrier_unrel    = (SEC_C_Q03 == 5) if grid_hh == 0 & SEC_C_Q03 < .
	gen byte barrier_admin    = (inlist(SEC_C_Q03, 6, 7)) if grid_hh == 0 & SEC_C_Q03 < .

	lab var barrier_cost     "Grid barrier: Connection cost too high"
	lab var barrier_dist     "Grid barrier: Grid too far / unavailable"
	lab var barrier_tariff   "Grid barrier: Monthly fee too expensive"
	lab var barrier_landlord "Grid barrier: Renting / landlord decision"
	lab var barrier_unrel    "Grid barrier: Service unreliable"
	lab var barrier_admin    "Grid barrier: Administrative delay / complicated"

	* Under the grid: EA has grid infrastructure, but HH is not connected
	capture drop ea_grid_present under_the_grid under_grid_unconnected grid_uptake
	capture confirm variable psu_id
	if !_rc bys psu_id: egen ea_grid_present = max(grid_hh)
	else    bys SEC_A_Q07: egen ea_grid_present = max(grid_hh)
	lab var ea_grid_present "Enumeration Area has at least 1 grid-connected household"

	gen byte under_the_grid = (ea_grid_present == 1)
	lab var under_the_grid "Household lives in electrified EA ('under the grid')"

	gen byte under_grid_unconnected = (ea_grid_present == 1 & grid_hh == 0)
	lab var under_grid_unconnected "Living in electrified EA but unconnected ('under the grid deficit')"

	gen byte grid_uptake = grid_hh if ea_grid_present == 1
	lab var grid_uptake "Household grid uptake rate among EAs with grid"

	* Grid connection history & expenditure
	capture drop grid_years grid_wait_days grid_monthly_spend
	clonevar grid_years = SEC_C_Q06
	lab var grid_years "Number of years connected to national grid"

	clonevar grid_wait_days = SEC_C_Q10
	replace grid_wait_days = . if grid_wait_days > 730
	lab var grid_wait_days "Days waited from application to grid connection"

	gen grid_monthly_spend = SEC_C_Q23
	replace grid_monthly_spend = SEC_C_Q25 if grid_monthly_spend == . | grid_monthly_spend == 0
	lab var grid_monthly_spend "Monthly expenditure on grid electricity (N$)"


	*===========================================================================
	*  ENHANCEMENT 6: WILLINGNESS TO PAY (WTP) FOR GRID CONNECTION (SEC_D)
	*===========================================================================

	capture drop wtp_grid_upfront wtp_grid_3m wtp_grid_6m wtp_grid_12m wtp_grid_waived wtp_grid_never refuse_wiring_cost
	gen byte wtp_grid_upfront = (SEC_D_Q03 == 1) if grid_hh == 0 & SEC_D_Q03 < .
	gen byte wtp_grid_3m      = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1) if grid_hh == 0 & SEC_D_Q03 < .
	gen byte wtp_grid_6m      = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1 | SEC_D_Q05 == 1) if grid_hh == 0 & SEC_D_Q03 < .
	gen byte wtp_grid_12m     = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1 | SEC_D_Q05 == 1 | SEC_D_Q06 == 1) if grid_hh == 0 & SEC_D_Q03 < .
	gen byte wtp_grid_waived  = (SEC_D_Q07 == 1) if grid_hh == 0 & SEC_D_Q07 < .
	gen byte wtp_grid_never   = (SEC_D_Q07 == 2) if grid_hh == 0 & SEC_D_Q07 < .
	gen byte refuse_wiring_cost = (SEC_D_Q08 == 1) if SEC_D_Q08 < .

	lab var wtp_grid_upfront "WTP grid connection: upfront"
	lab var wtp_grid_3m      "WTP grid connection: 3-month installment"
	lab var wtp_grid_6m      "WTP grid connection: 6-month installment"
	lab var wtp_grid_12m     "WTP grid connection: 12-month installment"
	lab var wtp_grid_waived  "WTP grid connection: if connection fee waived"
	lab var wtp_grid_never   "Will NEVER connect to grid under any terms"
	lab var refuse_wiring_cost "Refuses grid because cannot afford internal wiring"


	*===========================================================================
	*  ENHANCEMENT 7: WTP FOR SOLAR & SOLAR REVOLVING FUND (SEC_E)
	*===========================================================================

	capture drop wtp_solar_upfront wtp_solar_6m wtp_solar_12m wtp_solar_24m wtp_solar_never refuse_solar_cost srf_aware
	gen byte wtp_solar_upfront = (SEC_E_Q02 == 1) if SEC_E_Q02 < .
	gen byte wtp_solar_6m      = (SEC_E_Q02 == 1 | SEC_E_Q03 == 1) if SEC_E_Q02 < .
	gen byte wtp_solar_12m     = (SEC_E_Q02 == 1 | SEC_E_Q03 == 1 | SEC_E_Q04 == 1) if SEC_E_Q02 < .
	gen byte wtp_solar_24m     = (SEC_E_Q02 == 1 | SEC_E_Q03 == 1 | SEC_E_Q04 == 1 | SEC_E_Q05 == 1) if SEC_E_Q02 < .
	gen byte wtp_solar_never   = (SEC_E_Q05 == 2) if SEC_E_Q05 < .
	gen byte refuse_solar_cost = (SEC_E_Q06 == 1) if SEC_E_Q06 < .
	gen byte srf_aware = .
	capture confirm variable SEC_E_Q07
	if !_rc {
		replace srf_aware = (SEC_E_Q07 == 1) if SEC_E_Q07 < .
	}

	lab var wtp_solar_upfront "WTP Solar Device: upfront"
	lab var wtp_solar_6m      "WTP Solar Device: 6-month installment"
	lab var wtp_solar_12m     "WTP Solar Device: 12-month installment"
	lab var wtp_solar_24m     "WTP Solar Device: 24-month installment"
	lab var wtp_solar_never   "Will NEVER purchase solar device"
	lab var refuse_solar_cost "Cannot afford solar device payment"
	lab var srf_aware         "Aware of government Solar Revolving Fund (SRF)"


	*===========================================================================
	*  ENHANCEMENT 8: BACKUP LIGHTING SOLUTIONS FOR GRID HOUSEHOLDS
	*===========================================================================

	capture drop grid_backup_candle grid_backup_torch grid_backup_solar grid_backup_none
	gen byte grid_backup_candle = (SEC_H_Q03__1 == 1) if grid_hh == 1
	capture confirm variable has_torch
	if !_rc gen byte grid_backup_torch = (has_torch == 1) if grid_hh == 1
	else    gen byte grid_backup_torch = 0 if grid_hh == 1
	gen byte grid_backup_solar  = (solar_hh == 1) if grid_hh == 1
	gen byte grid_backup_none   = (SEC_C_Q32 == 111) if grid_hh == 1

	lab var grid_backup_candle "Grid HH uses candles as backup lighting"
	lab var grid_backup_torch  "Grid HH uses torch / dry-cell as backup lighting"
	lab var grid_backup_solar  "Grid HH uses solar device as backup lighting"
	lab var grid_backup_none   "Grid HH has NO backup lighting"


	*===========================================================================
	*  ENHANCEMENT 9: COOKSTOVE PURCHASE DECISION (SEC_G_Q07)
	*===========================================================================

	capture drop cook_dec_female cook_dec_male cook_dec_joint
	gen byte cook_dec_female = (SEC_G_Q07 == 1) if SEC_G_Q07 < .
	gen byte cook_dec_male   = (SEC_G_Q07 == 2) if SEC_G_Q07 < .
	gen byte cook_dec_joint  = (SEC_G_Q07 == 3) if SEC_G_Q07 < .

	lab var cook_dec_female "Cookstove purchase decided by female household member"
	lab var cook_dec_male   "Cookstove purchase decided by male household member"
	lab var cook_dec_joint  "Cookstove purchase decided jointly"


	*===========================================================================
	*  ENHANCEMENT 9b: WTP FOR CLEAN COOKSTOVES (SEC_K)
	*===========================================================================

	capture drop wtp_cook_upfront wtp_cook_3m wtp_cook_6m wtp_cook_12m wtp_cook_never refuse_cook_cost
	gen byte wtp_cook_upfront = (SEC_K_Q03 == 1) if SEC_K_Q03 < .
	gen byte wtp_cook_3m      = (SEC_K_Q03 == 1 | SEC_K_Q04 == 1) if SEC_K_Q03 < .
	gen byte wtp_cook_6m      = (SEC_K_Q03 == 1 | SEC_K_Q04 == 1 | SEC_K_Q05 == 1) if SEC_K_Q03 < .
	gen byte wtp_cook_12m     = (SEC_K_Q03 == 1 | SEC_K_Q04 == 1 | SEC_K_Q05 == 1 | SEC_K_Q06 == 1) if SEC_K_Q03 < .
	gen byte wtp_cook_never   = (SEC_K_Q06 == 2 | SEC_K_Q07 < .) if SEC_K_Q03 < .
	gen byte refuse_cook_cost = (SEC_K_Q07 == 1) if SEC_K_Q07 < .

	lab var wtp_cook_upfront "WTP Clean Cookstove: upfront"
	lab var wtp_cook_3m      "WTP Clean Cookstove: 3-month installment"
	lab var wtp_cook_6m      "WTP Clean Cookstove: 6-month installment"
	lab var wtp_cook_12m     "WTP Clean Cookstove: 12-month installment"
	lab var wtp_cook_never   "Will NEVER purchase clean cookstove"
	lab var refuse_cook_cost "Cannot afford clean cookstove payment"


	*===========================================================================
	*  ENHANCEMENT 10: HEAD DEMOGRAPHICS & FINANCIAL ACCESS
	*===========================================================================

	capture drop credit_access head_educ_none head_educ_prim head_educ_sec head_educ_high ///
		head_marital_single head_marital_married head_marital_widow head_marital_divsep

	gen byte credit_access = (SEC_B_Q16__1 == 1 | SEC_B_Q16__2 == 1 | SEC_B_Q16__3 == 1 | SEC_B_Q16__4 == 1 | SEC_B_Q16__5 == 1)
	lab var credit_access "Household has access to loans / credit from formal/informal sources"

	gen byte head_educ_none = (hh_head_educ == 0) if hh_head_educ < .
	gen byte head_educ_prim = (hh_head_educ == 1) if hh_head_educ < .
	gen byte head_educ_sec  = (hh_head_educ == 2) if hh_head_educ < .
	gen byte head_educ_high = (hh_head_educ == 3) if hh_head_educ < .

	gen byte head_marital_single  = (hh_head_marital == 1) if hh_head_marital < .
	gen byte head_marital_married = (inlist(hh_head_marital, 2, 3, 4)) if hh_head_marital < .
	gen byte head_marital_widow   = (hh_head_marital == 5) if hh_head_marital < .
	gen byte head_marital_divsep  = (inlist(hh_head_marital, 6, 7)) if hh_head_marital < .


	*===========================================================================
	*  ENHANCEMENT 11: 37 SUBDIVISIONS OF NIGERIA (SEC_A_Q01)
*===========================================================================
capture drop reg_*
gen byte reg_sokoto = (SEC_A_Q01 == 1)
gen byte reg_zamfara = (SEC_A_Q01 == 2)
gen byte reg_katsina = (SEC_A_Q01 == 3)
gen byte reg_jigawa = (SEC_A_Q01 == 4)
gen byte reg_yobe = (SEC_A_Q01 == 5)
gen byte reg_borno = (SEC_A_Q01 == 6)
gen byte reg_adamawa = (SEC_A_Q01 == 7)
gen byte reg_gombe = (SEC_A_Q01 == 8)
gen byte reg_bauchi = (SEC_A_Q01 == 9)
gen byte reg_kano = (SEC_A_Q01 == 10)
gen byte reg_kaduna = (SEC_A_Q01 == 11)
gen byte reg_kebbi = (SEC_A_Q01 == 12)
gen byte reg_niger = (SEC_A_Q01 == 13)
gen byte reg_fct = (SEC_A_Q01 == 14)
gen byte reg_nasarawa = (SEC_A_Q01 == 15)
gen byte reg_plateau = (SEC_A_Q01 == 16)
gen byte reg_taraba = (SEC_A_Q01 == 17)
gen byte reg_benue = (SEC_A_Q01 == 18)
gen byte reg_kogi = (SEC_A_Q01 == 19)
gen byte reg_kwara = (SEC_A_Q01 == 20)
gen byte reg_oyo = (SEC_A_Q01 == 21)
gen byte reg_osun = (SEC_A_Q01 == 22)
gen byte reg_ekiti = (SEC_A_Q01 == 23)
gen byte reg_ondo = (SEC_A_Q01 == 24)
gen byte reg_edo = (SEC_A_Q01 == 25)
gen byte reg_anambra = (SEC_A_Q01 == 26)
gen byte reg_enugu = (SEC_A_Q01 == 27)
gen byte reg_ebonyi = (SEC_A_Q01 == 28)
gen byte reg_cross_river = (SEC_A_Q01 == 29)
gen byte reg_akwa_ibom = (SEC_A_Q01 == 30)
gen byte reg_abia = (SEC_A_Q01 == 31)
gen byte reg_imo = (SEC_A_Q01 == 32)
gen byte reg_rivers = (SEC_A_Q01 == 33)
gen byte reg_bayelsa = (SEC_A_Q01 == 34)
gen byte reg_delta = (SEC_A_Q01 == 35)
gen byte reg_lagos = (SEC_A_Q01 == 36)
gen byte reg_ogun = (SEC_A_Q01 == 37)

save "$wip_hh/$master_dta", replace
	di " 06_analytical_enhancements.do complete (Enhancements 1-11)"
