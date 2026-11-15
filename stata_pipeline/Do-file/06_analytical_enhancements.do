
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
		capture drop deficit_`attr'
		gen deficit_`attr' = (elc_`attr'_tier < 4) if elec_tech_type == 1
		lab var deficit_`attr' "Grid HH deficit: `attr' tier < Tier 4"
	}

	* Overall: grid HH below Tier 4
	capture drop deficit_any
	gen deficit_any = (elc_aggr_tier < 4) if elec_tech_type == 1
	lab var deficit_any "Grid HH with aggregate tier < Tier 4 (any deficit)"

	* Multiple simultaneous binding constraints (Comment C18)
	capture drop num_binding_deficits
	egen num_binding_deficits = rowtotal(deficit_cap deficit_avbl deficit_rel deficit_qual deficit_affrd deficit_leg deficit_sft) if elec_tech_type == 1
	lab var num_binding_deficits "Number of simultaneous binding constraints below Tier 4"

	* Co-occurring binding constraint pairs (Availability + Reliability, Availability + Affordability, etc.)
	capture drop deficit_avbl_rel deficit_avbl_affd deficit_rel_qual
	gen byte deficit_avbl_rel  = (deficit_avbl == 1 & deficit_rel == 1) if elec_tech_type == 1
	gen byte deficit_avbl_affd = (deficit_avbl == 1 & deficit_affrd == 1) if elec_tech_type == 1
	gen byte deficit_rel_qual  = (deficit_rel == 1 & deficit_qual == 1) if elec_tech_type == 1
	lab var deficit_avbl_rel  "Co-occurring deficit: Availability + Reliability"
	lab var deficit_avbl_affd "Co-occurring deficit: Availability + Affordability"
	lab var deficit_rel_qual  "Co-occurring deficit: Reliability + Quality"

	* Primary binding minimum attribute
	capture drop binding_attr
	gen binding_attr = ""
	foreach attr in cap avbl rel qual affrd leg sft {
		replace binding_attr = "`attr'" ///
			if elec_tech_type == 1 & elc_`attr'_tier == elc_aggr_tier & elc_aggr_tier < 4
	}
	lab var binding_attr "Primary binding deficit attribute for grid HH below Tier 4"


	*===========================================================================
	*  ENHANCEMENT 2: STOVE STACKING DILUTION
	*  Flag: owns clean fuel stove but Exposure tier ≤ 1 (biomass stacking)
	*===========================================================================

	capture drop stacking_dilution
	gen stacking_dilution = 0
	replace stacking_dilution = 1 if ///
		clean_stove == 1 & (trad_stove == 1 | ics == 1) & ///
		cs_exp_tier <= 2 & cs_exp_tier != .
	lab define stacking_dilution 0 "No dilution" 1 "Stove stacking dilution", replace
	lab val stacking_dilution stacking_dilution
	lab var stacking_dilution "Stove stacking dilution: clean stove owner but Exposure Tier ≤1"

	* Sub-flag: owns BOTH clean stove AND traditional stove
	gen own_both_stoves = (clean_stove == 1 & trad_stove == 1)
	lab var own_both_stoves "Owns both clean fuel AND traditional stove (stacking risk)"

	* Multi-biomass stacking (Two or more traditional/biomass stoves, e.g. open fire + charcoal)
	capture confirm variable multi_biomass_stacking
	if _rc gen multi_biomass_stacking = (stove_stacking >= 2 & clean_stove == 0)
	gen any_stove_stacking = (stove_stacking >= 2)
	lab var any_stove_stacking "Any stove stacking (owns >= 2 cookstoves)"


	*===========================================================================
	*  ENHANCEMENT 3: FUEL COLLECTION OPPORTUNITY COST
	*  Women's annual fuel collection hours → equivalent working days (÷8)
	*  Source: time_collecting.dta  — individual-level, filtered by sex/age
	*===========================================================================

	* Demographic fuel hours already merged from time_collecting.dta in 00_build_master_dataset.do
	capture confirm variable women_fuel_hr_yr_hh
	if _rc {
		gen women_fuel_hr_yr_hh = .
		gen men_fuel_hr_yr_hh = .
		gen girls_fuel_hr_yr_hh = .
		gen boys_fuel_hr_yr_hh = .
	}

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
	if !_rc {
		bys psu_id: egen ea_grid_present = max(grid_hh)
	}
	else {
		capture confirm variable SEC_A_Q06
		if !_rc bys SEC_A_Q06: egen ea_grid_present = max(grid_hh)
		else {
			capture confirm variable SEC_A_Q07
			if !_rc bys SEC_A_Q07: egen ea_grid_present = max(grid_hh)
			else bys SEC_A_Q05: egen ea_grid_present = max(grid_hh)
		}
	}
	lab var ea_grid_present "Grid infrastructure present in Enumeration Area (EA)"

	gen byte under_the_grid = (ea_grid_present == 1)
	lab var under_the_grid "Household lives in electrified EA ('under the grid')"

	gen byte under_grid_unconnected = (ea_grid_present == 1 & grid_hh == 0)
	lab var under_grid_unconnected "Living in electrified EA but unconnected ('under the grid deficit')"

	gen byte grid_uptake = grid_hh if ea_grid_present == 1
	lab var grid_uptake "Household grid uptake rate among EAs with grid"

	* Energy Poverty Penalty: Coping lighting expenditures (Table 2.2)
	capture drop coping_spend coping_pct
	gen coping_spend = lightfuel_exp_tot_m
	gen coping_pct   = (coping_spend / exp_total_m) * 100 if exp_total_m > 0 & exp_total_m < .
	lab var coping_spend "Monthly expenditure on coping lighting (candles/kerosene/batteries)"
	lab var coping_pct   "Coping lighting expenditure as % of monthly total expenditure"

	* Grid connection history & expenditure (Comment C22)
	capture drop grid_years grid_wait_days grid_monthly_spend grid_tenure_cat
	clonevar grid_years = SEC_C_Q06
	lab var grid_years "Number of years connected to national grid"

	clonevar grid_wait_days = SEC_C_Q10
	replace grid_wait_days = . if grid_wait_days > 730
	lab var grid_wait_days "Days waited from application to grid connection"

	gen grid_monthly_spend = SEC_C_Q23
	replace grid_monthly_spend = SEC_C_Q25 if grid_monthly_spend == . | grid_monthly_spend == 0
	lab var grid_monthly_spend "Monthly expenditure on grid electricity ($currency)"

	* Grid tenure categories (<1 yr, 1-2 yrs, 3-4 yrs, 5-9 yrs, 10+ yrs)
	gen byte grid_tenure_cat = .
	replace grid_tenure_cat = 1 if grid_years < 1 & grid_years != .
	replace grid_tenure_cat = 2 if grid_years >= 1 & grid_years < 3
	replace grid_tenure_cat = 3 if grid_years >= 3 & grid_years < 5
	replace grid_tenure_cat = 4 if grid_years >= 5 & grid_years < 10
	replace grid_tenure_cat = 5 if grid_years >= 10 & grid_years < .
	lab define grid_tenure_cat 1 "<1 Year" 2 "1–2 Years" 3 "3–4 Years" 4 "5–9 Years" 5 "10+ Years", replace
	lab val grid_tenure_cat grid_tenure_cat
	lab var grid_tenure_cat "Grid connection tenure category"


	*===========================================================================
	*  ENHANCEMENT 6: WILLINGNESS TO PAY (WTP) FOR GRID CONNECTION (SEC_D)
	*===========================================================================

	capture drop wtp_grid_upfront wtp_grid_3m wtp_grid_6m wtp_grid_12m wtp_grid_waived wtp_grid_never refuse_wiring_cost
	gen byte wtp_grid_upfront = (SEC_D_Q03 == 1) if grid_hh == 0 & SEC_D_Q03 < .
	gen byte wtp_grid_3m      = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1) if grid_hh == 0 & SEC_D_Q03 < .
	gen byte wtp_grid_6m      = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1 | SEC_D_Q05 == 1) if grid_hh == 0 & SEC_D_Q03 < .
	gen byte wtp_grid_12m     = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1 | SEC_D_Q05 == 1 | SEC_D_Q06 == 1) if grid_hh == 0 & SEC_D_Q03 < .
	gen byte wtp_grid_waived  = (wtp_grid_12m == 1 | SEC_D_Q07 == 1) if grid_hh == 0 & SEC_D_Q03 < .
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
	*  ENHANCEMENT 6b: DISAGGREGATED WTP BY PRICE SPLIT (GRID CONNECTION)
	*  Allows plotting multi-curve panels crossing connection fee price points
	*  (100%, 57%, 29%, 14%) with installment financing horizons (Upfront, 3M, 6M, 12M, Waived).
	*===========================================================================

	capture drop wtp_grid_p100_upfront wtp_grid_p100_3m wtp_grid_p100_6m wtp_grid_p100_12m wtp_grid_p100_waived
	capture drop wtp_grid_p57_upfront  wtp_grid_p57_3m  wtp_grid_p57_6m  wtp_grid_p57_12m  wtp_grid_p57_waived
	capture drop wtp_grid_p29_upfront  wtp_grid_p29_3m  wtp_grid_p29_6m  wtp_grid_p29_12m  wtp_grid_p29_waived
	capture drop wtp_grid_p14_upfront  wtp_grid_p14_3m  wtp_grid_p14_6m  wtp_grid_p14_12m  wtp_grid_p14_waived

	capture confirm variable random_percentage
	if !_rc {
		* Vectorized WTP loops across all 6 randomized price benchmarks and payment horizons
		local p_list "100 71 57 43 29 14"
		foreach p of local p_list {
			local p_cond "random_percentage >= 0.95 & random_percentage <= 1.05"
			if "`p'" == "71" local p_cond "random_percentage >= 0.68 & random_percentage <= 0.75"
			if "`p'" == "57" local p_cond "random_percentage >= 0.54 & random_percentage <= 0.60"
			if "`p'" == "43" local p_cond "random_percentage >= 0.40 & random_percentage <= 0.46"
			if "`p'" == "29" local p_cond "random_percentage >= 0.26 & random_percentage <= 0.32"
			if "`p'" == "14" local p_cond "random_percentage >= 0.12 & random_percentage <= 0.16"
			
			foreach t in upfront 3m 6m 12m waived never {
				capture drop wtp_grid_p`p'_`t'
				gen byte wtp_grid_p`p'_`t' = wtp_grid_`t' if `p_cond' & grid_hh == 0
			}
		}
	}
	else {
		capture confirm variable index_random
		if !_rc {
			* 100% full fee (index_random == 5)
			gen byte wtp_grid_p100_upfront = (SEC_D_Q03 == 1) if index_random == 5 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p100_3m      = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1) if index_random == 5 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p100_6m      = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1 | SEC_D_Q05 == 1) if index_random == 5 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p100_12m     = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1 | SEC_D_Q05 == 1 | SEC_D_Q06 == 1) if index_random == 5 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p100_waived  = (wtp_grid_p100_12m == 1 | SEC_D_Q07 == 1) if index_random == 5 & grid_hh == 0 & SEC_D_Q03 < .

			* 57% fee (index_random == 3)
			gen byte wtp_grid_p57_upfront  = (SEC_D_Q03 == 1) if index_random == 3 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p57_3m       = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1) if index_random == 3 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p57_6m       = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1 | SEC_D_Q05 == 1) if index_random == 3 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p57_12m      = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1 | SEC_D_Q05 == 1 | SEC_D_Q06 == 1) if index_random == 3 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p57_waived   = (wtp_grid_p57_12m == 1 | SEC_D_Q07 == 1) if index_random == 3 & grid_hh == 0 & SEC_D_Q03 < .

			* 29% fee (index_random == 1)
			gen byte wtp_grid_p29_upfront  = (SEC_D_Q03 == 1) if index_random == 1 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p29_3m       = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1) if index_random == 1 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p29_6m       = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1 | SEC_D_Q05 == 1) if index_random == 1 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p29_12m      = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1 | SEC_D_Q05 == 1 | SEC_D_Q06 == 1) if index_random == 1 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p29_waived   = (wtp_grid_p29_12m == 1 | SEC_D_Q07 == 1) if index_random == 1 & grid_hh == 0 & SEC_D_Q03 < .

			* 14% fee (index_random == 0)
			gen byte wtp_grid_p14_upfront  = (SEC_D_Q03 == 1) if index_random == 0 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p14_3m       = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1) if index_random == 0 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p14_6m       = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1 | SEC_D_Q05 == 1) if index_random == 0 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p14_12m      = (SEC_D_Q03 == 1 | SEC_D_Q04 == 1 | SEC_D_Q05 == 1 | SEC_D_Q06 == 1) if index_random == 0 & grid_hh == 0 & SEC_D_Q03 < .
			gen byte wtp_grid_p14_waived   = (wtp_grid_p14_12m == 1 | SEC_D_Q07 == 1) if index_random == 0 & grid_hh == 0 & SEC_D_Q03 < .
		}
	}


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
	*  ENHANCEMENT 7b: DISAGGREGATED WTP BY SYSTEM TIER & SUBSIDY LEVEL (SOLAR)
	*===========================================================================
	capture confirm variable random_percentage_3
	if !_rc {
		capture confirm variable solar_system
		if !_rc {
			foreach s in t1 t2 pooled {
				local s_cond "1 == 1"
				if "`s'" == "t1" local s_cond "solar_system == 1 | solar_system == 1.0"
				if "`s'" == "t2" local s_cond "solar_system == 2 | solar_system == 2.0"

				foreach p in 33 66 100 {
					local p_cond "random_percentage_3 >= 0.95 & random_percentage_3 <= 1.05"
					if "`p'" == "66" local p_cond "random_percentage_3 >= 0.60 & random_percentage_3 <= 0.72"
					if "`p'" == "33" local p_cond "random_percentage_3 >= 0.30 & random_percentage_3 <= 0.36"

					foreach t in upfront 6m 12m 24m never {
						capture drop wtp_solar_`s'_p`p'_`t'
						gen byte wtp_solar_`s'_p`p'_`t' = wtp_solar_`t' if `s_cond' & `p_cond'
					}
				}
			}
		}
	}


	*===========================================================================
	*  ENHANCEMENT 7b: WTP FOR CLEAN COOKSTOVES (SEC_K / SEC_G CONTINGENT VALUATION)
	*===========================================================================

	capture drop wtp_cook_upfront wtp_cook_3m wtp_cook_6m wtp_cook_12m wtp_cook_never refuse_cook_cost
	* Clean Cookstove Bidding Module (Section K in standard MTF, Section G in some countries)
	capture confirm variable SEC_K_Q03
	if !_rc {
		gen byte wtp_cook_upfront = (SEC_K_Q03 == 1) if SEC_K_Q03 < .
		gen byte wtp_cook_3m      = (SEC_K_Q03 == 1 | SEC_K_Q04 == 1) if SEC_K_Q03 < .
		gen byte wtp_cook_6m      = (SEC_K_Q03 == 1 | SEC_K_Q04 == 1 | SEC_K_Q05 == 1) if SEC_K_Q03 < .
		gen byte wtp_cook_12m     = (SEC_K_Q03 == 1 | SEC_K_Q04 == 1 | SEC_K_Q05 == 1 | SEC_K_Q06 == 1) if SEC_K_Q03 < .
		gen byte wtp_cook_never   = (SEC_K_Q06 == 2 | SEC_K_Q07 < .) if SEC_K_Q03 < .
		capture confirm variable SEC_K_Q07
		if !_rc gen byte refuse_cook_cost = (SEC_K_Q07 == 1) if SEC_K_Q07 < .
		else    gen byte refuse_cook_cost = (wtp_cook_never == 1) if wtp_cook_never < .
	}
	else {
		capture confirm variable SEC_G_Q20
		if !_rc {
			gen byte wtp_cook_upfront = (SEC_G_Q20 == 1) if SEC_G_Q20 < .
			gen byte wtp_cook_3m      = (SEC_G_Q20 == 1 | SEC_G_Q21 == 1) if SEC_G_Q20 < .
			gen byte wtp_cook_6m      = (SEC_G_Q20 == 1 | SEC_G_Q21 == 1 | SEC_G_Q22 == 1) if SEC_G_Q20 < .
			gen byte wtp_cook_12m     = (SEC_G_Q20 == 1 | SEC_G_Q21 == 1 | SEC_G_Q22 == 1 | SEC_G_Q23 == 1) if SEC_G_Q20 < .
			gen byte wtp_cook_never   = (SEC_G_Q23 == 2) if SEC_G_Q20 < .
			gen byte refuse_cook_cost = (wtp_cook_never == 1) if wtp_cook_never < .
		}
	}

	lab var wtp_cook_upfront "WTP Clean Cookstove: upfront"
	lab var wtp_cook_3m      "WTP Clean Cookstove: 3-month installment"
	lab var wtp_cook_6m      "WTP Clean Cookstove: 6-month installment"
	lab var wtp_cook_12m     "WTP Clean Cookstove: 12-month installment"
	lab var wtp_cook_never   "Will NEVER purchase clean cookstove"
	lab var refuse_cook_cost "Cannot afford clean cookstove payment"

	*===========================================================================
	*  ENHANCEMENT 7c: DISAGGREGATED WTP BY PRICE SPLIT (SOLAR & COOKING)
	*  Allows plotting multi-curve panels crossing price subsidies (33%, 66%, 100%)
	*  with installment financing horizons (Upfront, 6M, 12M, 24M).
	*===========================================================================

	capture drop wtp_solar_p100_upfront wtp_solar_p100_6m wtp_solar_p100_12m wtp_solar_p100_24m
	capture drop wtp_solar_p66_upfront wtp_solar_p66_6m wtp_solar_p66_12m wtp_solar_p66_24m
	capture drop wtp_solar_p33_upfront wtp_solar_p33_6m wtp_solar_p33_12m wtp_solar_p33_24m

	capture confirm variable index_random_3
	if !_rc {
		* 100% full price (index_random_3 == 2)
		gen byte wtp_solar_p100_upfront = (SEC_E_Q02 == 1) if index_random_3 == 2 & SEC_E_Q02 < .
		gen byte wtp_solar_p100_6m      = (SEC_E_Q02 == 1 | SEC_E_Q03 == 1) if index_random_3 == 2 & SEC_E_Q02 < .
		gen byte wtp_solar_p100_12m     = (SEC_E_Q02 == 1 | SEC_E_Q03 == 1 | SEC_E_Q04 == 1) if index_random_3 == 2 & SEC_E_Q02 < .
		gen byte wtp_solar_p100_24m     = (SEC_E_Q02 == 1 | SEC_E_Q03 == 1 | SEC_E_Q04 == 1 | SEC_E_Q05 == 1) if index_random_3 == 2 & SEC_E_Q02 < .
		
		* 66% price (index_random_3 == 1)
		gen byte wtp_solar_p66_upfront  = (SEC_E_Q02 == 1) if index_random_3 == 1 & SEC_E_Q02 < .
		gen byte wtp_solar_p66_6m       = (SEC_E_Q02 == 1 | SEC_E_Q03 == 1) if index_random_3 == 1 & SEC_E_Q02 < .
		gen byte wtp_solar_p66_12m      = (SEC_E_Q02 == 1 | SEC_E_Q03 == 1 | SEC_E_Q04 == 1) if index_random_3 == 1 & SEC_E_Q02 < .
		gen byte wtp_solar_p66_24m      = (SEC_E_Q02 == 1 | SEC_E_Q03 == 1 | SEC_E_Q04 == 1 | SEC_E_Q05 == 1) if index_random_3 == 1 & SEC_E_Q02 < .

		* 33% price (index_random_3 == 0)
		gen byte wtp_solar_p33_upfront  = (SEC_E_Q02 == 1) if index_random_3 == 0 & SEC_E_Q02 < .
		gen byte wtp_solar_p33_6m       = (SEC_E_Q02 == 1 | SEC_E_Q03 == 1) if index_random_3 == 0 & SEC_E_Q02 < .
		gen byte wtp_solar_p33_12m      = (SEC_E_Q02 == 1 | SEC_E_Q03 == 1 | SEC_E_Q04 == 1) if index_random_3 == 0 & SEC_E_Q02 < .
		gen byte wtp_solar_p33_24m      = (SEC_E_Q02 == 1 | SEC_E_Q03 == 1 | SEC_E_Q04 == 1 | SEC_E_Q05 == 1) if index_random_3 == 0 & SEC_E_Q02 < .
	}

	* Clean Cookstove WTP disaggregated by randomized price proportion (random_perc_k: 1.0, 0.66, 0.33)
	capture drop wtp_cook_p100_upfront wtp_cook_p100_6m wtp_cook_p100_12m wtp_cook_p100_24m
	capture drop wtp_cook_p66_upfront wtp_cook_p66_6m wtp_cook_p66_12m wtp_cook_p66_24m
	capture drop wtp_cook_p33_upfront wtp_cook_p33_6m wtp_cook_p33_12m wtp_cook_p33_24m

	capture confirm variable random_perc_k
	if !_rc {
		* 100% full price
		gen byte wtp_cook_p100_upfront = (SEC_K_Q03 == 1) if random_perc_k >= 0.99 & random_perc_k <= 1.01 & SEC_K_Q03 < .
		gen byte wtp_cook_p100_6m      = (SEC_K_Q03 == 1 | SEC_K_Q04 == 1) if random_perc_k >= 0.99 & random_perc_k <= 1.01 & SEC_K_Q03 < .
		gen byte wtp_cook_p100_12m     = (SEC_K_Q03 == 1 | SEC_K_Q04 == 1 | SEC_K_Q05 == 1) if random_perc_k >= 0.99 & random_perc_k <= 1.01 & SEC_K_Q03 < .
		gen byte wtp_cook_p100_24m     = (SEC_K_Q03 == 1 | SEC_K_Q04 == 1 | SEC_K_Q05 == 1 | SEC_K_Q06 == 1) if random_perc_k >= 0.99 & random_perc_k <= 1.01 & SEC_K_Q03 < .

		* 66% price
		gen byte wtp_cook_p66_upfront  = (SEC_K_Q03 == 1) if random_perc_k >= 0.60 & random_perc_k <= 0.70 & SEC_K_Q03 < .
		gen byte wtp_cook_p66_6m       = (SEC_K_Q03 == 1 | SEC_K_Q04 == 1) if random_perc_k >= 0.60 & random_perc_k <= 0.70 & SEC_K_Q03 < .
		gen byte wtp_cook_p66_12m      = (SEC_K_Q03 == 1 | SEC_K_Q04 == 1 | SEC_K_Q05 == 1) if random_perc_k >= 0.60 & random_perc_k <= 0.70 & SEC_K_Q03 < .
		gen byte wtp_cook_p66_24m      = (SEC_K_Q03 == 1 | SEC_K_Q04 == 1 | SEC_K_Q05 == 1 | SEC_K_Q06 == 1) if random_perc_k >= 0.60 & random_perc_k <= 0.70 & SEC_K_Q03 < .

		* 33% price
		gen byte wtp_cook_p33_upfront  = (SEC_K_Q03 == 1) if random_perc_k >= 0.30 & random_perc_k <= 0.40 & SEC_K_Q03 < .
		gen byte wtp_cook_p33_6m       = (SEC_K_Q03 == 1 | SEC_K_Q04 == 1) if random_perc_k >= 0.30 & random_perc_k <= 0.40 & SEC_K_Q03 < .
		gen byte wtp_cook_p33_12m      = (SEC_K_Q03 == 1 | SEC_K_Q04 == 1 | SEC_K_Q05 == 1) if random_perc_k >= 0.30 & random_perc_k <= 0.40 & SEC_K_Q03 < .
		gen byte wtp_cook_p33_24m      = (SEC_K_Q03 == 1 | SEC_K_Q04 == 1 | SEC_K_Q05 == 1 | SEC_K_Q06 == 1) if random_perc_k >= 0.30 & random_perc_k <= 0.40 & SEC_K_Q03 < .
	}

	* Outage intervals for grid households (SEC_C_Q29, dropping 888 "Don't know")
	capture drop outages_per_wk outages_lt3_wk outages_3to14_wk outages_gt14_wk
	gen double outages_per_wk = .
	capture confirm variable SEC_C_Q29
	if !_rc {
		replace outages_per_wk = SEC_C_Q29 if grid_hh == 1 & SEC_C_Q29 < 888
	}
	gen byte outages_lt3_wk   = (outages_per_wk < 3) if outages_per_wk < .
	gen byte outages_3to14_wk = (outages_per_wk >= 3 & outages_per_wk <= 14) if outages_per_wk < .
	gen byte outages_gt14_wk  = (outages_per_wk > 14) if outages_per_wk < .
	lab var outages_lt3_wk   "Grid outages: fewer than 3 times per week (<3/wk)"
	lab var outages_3to14_wk "Grid outages: 3 to 14 times per week (3-14/wk)"
	lab var outages_gt14_wk  "Grid outages: more than 14 times per week (>14/wk)"

	* Electric stove adoption among grid households
	capture drop elec_stove_grid
	capture confirm variable elec_stove
	if !_rc gen byte elec_stove_grid = (elec_stove == 1) if grid_hh == 1
	else    gen byte elec_stove_grid = 0 if grid_hh == 1
	lab var elec_stove_grid "Grid-connected household owns an electric cookstove"


	*===========================================================================
	*  ENHANCEMENT 8: BACKUP LIGHTING SOLUTIONS FOR GRID HOUSEHOLDS
	*===========================================================================

	capture drop grid_backup_candle grid_backup_torch grid_backup_solar grid_backup_none
	capture confirm variable SEC_H_Q03__1
	if !_rc gen byte grid_backup_candle = (SEC_H_Q03__1 == 1) if grid_hh == 1
	else    gen byte grid_backup_candle = 0 if grid_hh == 1
	capture confirm variable has_torch
	if !_rc gen byte grid_backup_torch = (has_torch == 1) if grid_hh == 1
	else    gen byte grid_backup_torch = 0 if grid_hh == 1
	gen byte grid_backup_solar  = (solar_hh == 1) if grid_hh == 1
	capture confirm variable SEC_C_Q32
	if !_rc gen byte grid_backup_none   = (SEC_C_Q32 == 111) if grid_hh == 1
	else    gen byte grid_backup_none   = 0 if grid_hh == 1

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
	*  ENHANCEMENT 11: 14 REGIONS OF NAMIBIA (SEC_A_Q01)
	*===========================================================================

	capture drop reg_*
	gen byte reg_kharas       = (SEC_A_Q01 == 1)
	gen byte reg_erongo       = (SEC_A_Q01 == 2)
	gen byte reg_hardap       = (SEC_A_Q01 == 3)
	gen byte reg_kavango_e    = (SEC_A_Q01 == 4)
	gen byte reg_kavango_w    = (SEC_A_Q01 == 5)
	gen byte reg_khomas       = (SEC_A_Q01 == 6)
	gen byte reg_kunene       = (SEC_A_Q01 == 7)
	gen byte reg_ohangwena    = (SEC_A_Q01 == 8)
	gen byte reg_omaheke      = (SEC_A_Q01 == 9)
	gen byte reg_omusati      = (SEC_A_Q01 == 10)
	gen byte reg_oshana       = (SEC_A_Q01 == 11)
	gen byte reg_oshikoto     = (SEC_A_Q01 == 12)
	gen byte reg_otjozondjupa = (SEC_A_Q01 == 13)
	gen byte reg_zambezi      = (SEC_A_Q01 == 14)


	*===========================================================================
	*  ENHANCEMENT 12: ENERGY POVERTY PENALTY & COPING MECHANISM EXPENDITURES
	*  Coping fuel expenditure (dry-cell batteries, candles, kerosene, phone charging)
	*  and budget share relative to total household monthly consumption expenditure.
	*===========================================================================

	capture drop coping_spend coping_pct
	* Calculate total monthly spending on lighting substitutes (Section H + phone charging)
	gen double coping_spend = 0
	capture confirm variable lightfuel_exp_tot_m
	if !_rc replace coping_spend = coping_spend + cond(lightfuel_exp_tot_m < ., lightfuel_exp_tot_m, 0)
	capture confirm variable SEC_C_Q121
	if !_rc replace coping_spend = coping_spend + cond(SEC_C_Q121 < ., SEC_C_Q121, 0)

	* Monthly budget share (% of total monthly consumption expenditure)
	gen double coping_pct = .
	capture confirm variable exp_total_m
	if !_rc {
		replace coping_pct = (coping_spend / exp_total_m) * 100 if exp_total_m > 0 & exp_total_m < .
		replace coping_pct = 100 if coping_pct > 100 & coping_pct < .
	}

	lab var coping_spend "Monthly expenditure on alternative lighting & coping mechanisms"
	lab var coping_pct   "Share of monthly household budget spent on coping mechanisms (%)"


	*===========================================================================
	*  ENHANCEMENT 13: COMPREHENSIVE LIGHTING POINTS (INCANDESCENT, FLUOR, CFL, LED)
	*===========================================================================

	capture drop has_electric_lights has_solar_lights has_any_lights
	capture confirm variable has_lights
	if !_rc gen byte has_electric_lights = (has_lights == 1) if has_lights < .
	else    gen byte has_electric_lights = 0
	gen byte has_solar_lights = (solar_hh == 1)
	gen byte has_any_lights   = (has_electric_lights == 1 | has_solar_lights == 1)
	lab var has_electric_lights "Owns electric lighting points (incandescent, fluorescent, CFL, LED)"
	lab var has_solar_lights    "Owns standalone solar lighting points / lantern"
	lab var has_any_lights      "Owns any modern electric or solar lighting points"


	*===========================================================================
	*  ENHANCEMENT 14: COOKSTOVE TIME-USE & WEEKLY COOKING HOURS
	*===========================================================================

	preserve
		local fn_stoves = cond("$fn_cookstoves" != "", "$fn_cookstoves", "section_g_cookstoves_roster.dta")
		capture confirm file "$raw_hh/`fn_stoves'"
		if !_rc {
			use "$raw_hh/`fn_stoves'", clear
			capture confirm variable interview__id
			if _rc {
				capture confirm variable interview__key
				if !_rc clonevar interview__id = interview__key
			}
			* Daily cooking minutes: boiling water (Q21) + morning (Q22a) + afternoon (Q22b) + evening (Q22c)
			gen double daily_mins = cond(SEC_G_Q21 < ., SEC_G_Q21, 0) + ///
			                        cond(SEC_G_Q22a < ., SEC_G_Q22a, 0) + ///
			                        cond(SEC_G_Q22b < ., SEC_G_Q22b, 0) + ///
			                        cond(SEC_G_Q22c < ., SEC_G_Q22c, 0)
			* Weekly hours = (daily_mins / 60) * days used per week (Q19)
			gen double weekly_hrs = (daily_mins / 60) * cond(SEC_G_Q19 < ., SEC_G_Q19, 0)
			
			* Disaggregate by cookstove type
			gen double hr_3stone = weekly_hrs if SEC_G_Q05 == 1
			gen double hr_trad   = weekly_hrs if SEC_G_Q05 == 2
			gen double hr_ics    = weekly_hrs if SEC_G_Q05 == 3
			gen double hr_lpg    = weekly_hrs if SEC_G_Q05 == 5
			gen double hr_elec   = weekly_hrs if SEC_G_Q05 == 7
			
			bys interview__id: egen hr_3stone_hh = total(hr_3stone)
			bys interview__id: egen hr_trad_hh   = total(hr_trad)
			bys interview__id: egen hr_ics_hh    = total(hr_ics)
			bys interview__id: egen hr_lpg_hh    = total(hr_lpg)
			bys interview__id: egen hr_elec_hh   = total(hr_elec)
			
			keep interview__id hr_3stone_hh hr_trad_hh hr_ics_hh hr_lpg_hh hr_elec_hh
			duplicates drop
			save "$wip_hh/stove_time_use.dta", replace
		}
	restore
	capture merge 1:1 interview__id using "$wip_hh/stove_time_use.dta", nogen
	lab var hr_3stone_hh "Weekly cooking hours on 3-stone / open fire"
	lab var hr_trad_hh   "Weekly cooking hours on traditional/artisanal charcoal stove"
	lab var hr_ics_hh    "Weekly cooking hours on improved biomass cookstove (ICS)"
	lab var hr_lpg_hh    "Weekly cooking hours on LPG cookstove"
	lab var hr_elec_hh   "Weekly cooking hours on electric cookstove"


	*---------------------------------------------------------------------------
	* Save
	*---------------------------------------------------------------------------
	save "$wip_hh/$master_dta", replace
	di " 06_analytical_enhancements.do complete (Enhancements 1-14)"
