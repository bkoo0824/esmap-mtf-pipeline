
	**************************************************************************
	*  04_cooking_attributes.do                                              *
	*  Namibia MTF Pipeline — 6 MECS Cooking Attribute Tiers                *
	*                                                                        *
	*  Source logic: Namibia_electricityANDcooking.do (lines 2544–3067)     *
	*                                                                        *
	*  Attributes produced (each 0–5):                                       *
	*    cs_exp_tier    — Exposure (stove emission × ventilation)            *
	*    cs_efcy_tier   — Efficiency (ISO thermal efficiency by stove type)  *
	*    cs_conv_tier   — Convenience (fuel collection + prep time hr/wk)    *
	*    cs_sfty_tier   — Safety (burn/respiratory injury past 12 months)    *
	*    cs_affd_tier   — Affordability (fuel spend < 5% HH expenditure)     *
	*    cs_avbl_tier   — Availability (fuel supply reliability)              *
	*                                                                        *
	*  Auxiliary variables:                                                  *
	*    mainstove      — Main stove type (1–8, 555=other)                  *
	*    secondstove    — Second stove (stove stacking)                      *
	*    clean_stove    — Binary: owns clean-fuel stove                      *
	*    trad_stove     — Binary: owns traditional stove                     *
	*    cookingfuel_exp_tot_yr — Annual cooking fuel expenditure            *
	*    cs_fcol_fpre   — Weekly fuel collection + prep time (hr/wk)        *
	**************************************************************************

	use "$wip_hh/$master_dta", clear
	set more off

	label define tier 0 "Tier 0" 1 "Tier 1" 2 "Tier 2" 3 "Tier 3" 4 "Tier 4" 5 "Tier 5", replace

	** Defensive safeguard: Ensure all cooking variables exist in master
	foreach v in SEC_G_Q04 SEC_G_Q05 SEC_G_Q14 SEC_G_Q15__1 SEC_G_Q15__2 SEC_G_Q15__111 SEC_G_Q15__555 ///
	             SEC_G_Q16 SEC_G_Q17 SEC_G_Q23 SEC_G_Q28 ///
	             clean_stove ics trad_stove stove_stacking cs_fcol_fpre exp_total_yr fuel_exp_tot_yr {
		capture confirm var `v'
		if _rc gen `v' = .
	}
	forval i = 1/15 {
		capture confirm var SEC_G_Q16__`i'
		if _rc gen SEC_G_Q16__`i' = 0
	}
	foreach v in SEC_G_Q16__111 SEC_G_Q16__555 {
		capture confirm var `v'
		if _rc gen `v' = 0
	}


	*===========================================================================
	*  PART 0: STOVE TYPE CLASSIFICATION
	*===========================================================================

	capture drop mainstove
	gen mainstove = .
	replace mainstove = 1 if inlist(SEC_G_Q05, 1, 2)              // 3-stone / open fire
	replace mainstove = 2 if inlist(SEC_G_Q05, 3, 5, 22)          // traditional/locally built
	replace mainstove = 3 if inlist(SEC_G_Q05, 4, 6, 7, 8, 9, 20, 21)  // manufactured biomass ICS
	replace mainstove = 4 if inlist(SEC_G_Q05, 10, 11, 12, 13, 14, 23) // LPG/cooking gas
	replace mainstove = 5 if inlist(SEC_G_Q05, 19)                // electric stove
	replace mainstove = 6 if inlist(SEC_G_Q05, 17, 18)            // solar cooker
	replace mainstove = 7 if inlist(SEC_G_Q05, 15)                // biogas
	replace mainstove = 8 if inlist(SEC_G_Q05, 16)                // biofuel
	replace mainstove = 555 if inlist(SEC_G_Q05, 555)             // other

	* Correct misclassified gas stoves (fuel=gas and no other fuels used)
	tempvar q16_fuel_count
	egen `q16_fuel_count' = rowtotal(SEC_G_Q16__*)
	replace mainstove = 4 if mainstove != 4 & SEC_G_Q16__15 == 1 & `q16_fuel_count' == 1

	lab define mainstove ///
		1 "3-Stone / Open Fire"        ///
		2 "Traditional / Local Stove"  ///
		3 "Manufactured Biomass (ICS)" ///
		4 "LPG / Cooking Gas"          ///
		5 "Electric Stove"             ///
		6 "Solar Cooker"               ///
		7 "Biogas Stove"               ///
		8 "Biofuel Stove"              ///
		555 "Other Cookstove", replace
	lab val mainstove mainstove
	lab var mainstove "Type of Main Stove"

	capture drop electricstove
	gen electricstove = (mainstove == 5)
	lab var electricstove "Binary: electric stove as main stove"


	*===========================================================================
	*  A. EXPOSURE TIER
	*  ISO emission tier of stove × kitchen ventilation quality (ESMAP MTF standard methodology)
	*===========================================================================

	capture drop cs_emit_tier SEC_G_Q15 vent_strc vent_tier cs_exp_tier
	* Use time-weighted emission tier across all stoves from cookstoves roster
	capture confirm variable weighted_emit_tier
	if !_rc {
		gen cs_emit_tier = weighted_emit_tier
	}
	else {
		gen cs_emit_tier = .
	}
	* Fallback by mainstove group if unassigned
	replace cs_emit_tier = 0 if inlist(mainstove, 1, 2) & cs_emit_tier == .
	replace cs_emit_tier = 3 if mainstove == 3 & cs_emit_tier == .
	replace cs_emit_tier = 4 if inlist(mainstove, 4, 5, 6) & cs_emit_tier == .
	replace cs_emit_tier = 5 if inlist(mainstove, 7, 8) & cs_emit_tier == .
	replace cs_emit_tier = 0 if cs_emit_tier == .
	lab var cs_emit_tier "Stove ISO Emission Tier (0–5, time-weighted across stoves)"

	** Exhaust system (SEC_G_Q15)
	capture drop SEC_G_Q15
	gen SEC_G_Q15 = .
	replace SEC_G_Q15 = 1   if SEC_G_Q15__1 == 1
	replace SEC_G_Q15 = 2   if SEC_G_Q15__2 == 1
	replace SEC_G_Q15 = 111 if SEC_G_Q15__111 == 1
	replace SEC_G_Q15 = 555 if SEC_G_Q15__555 == 1

	** Openings / windows (SEC_G_Q28)
	replace SEC_G_Q28 = 1 if SEC_G_Q28 == 20

	** Ventilation structure
	gen vent_strc = .
	replace vent_strc = 5 if SEC_G_Q14 == 5 | inlist(mainstove, 4, 5, 6, 7, 8)
	replace vent_strc = 4 if SEC_G_Q14 == 4
	replace vent_strc = 3 if (inlist(SEC_G_Q14, 1, 2, 3)) & inlist(SEC_G_Q15, 1, 2)
	replace vent_strc = 2 if (inlist(SEC_G_Q14, 1, 2, 3)) & SEC_G_Q28 >= 2 & SEC_G_Q28 != 888 & SEC_G_Q28 != . & vent_strc == .
	replace vent_strc = 1 if (inlist(SEC_G_Q14, 1, 2, 3)) & SEC_G_Q28 == 1 & SEC_G_Q28 != 888 & vent_strc == .
	replace vent_strc = 0 if (inlist(SEC_G_Q14, 1, 2, 3)) & SEC_G_Q15 == 111 & SEC_G_Q28 == 0 & SEC_G_Q28 != 888 & vent_strc == .

	** Ventilation level
	gen vent_tier = .
	replace vent_tier = 2 if inlist(vent_strc, 0, 1, 2)
	replace vent_tier = 3 if inlist(vent_strc, 3)
	replace vent_tier = 5 if inlist(vent_strc, 4, 5)

	** Exposure tier
	gen cs_exp_tier = .
	replace cs_exp_tier = 5 if cs_emit_tier == 5
	replace cs_exp_tier = 5 if cs_emit_tier == 4 & inlist(vent_tier, 5)
	replace cs_exp_tier = 4 if cs_emit_tier == 4 & inlist(vent_tier, 2, 3)
	replace cs_exp_tier = 4 if cs_emit_tier == 3 & inlist(vent_tier, 5)
	replace cs_exp_tier = 3 if cs_emit_tier == 3 & inlist(vent_tier, 3)
	replace cs_exp_tier = 2 if cs_emit_tier == 3 & inlist(vent_tier, 2)
	replace cs_exp_tier = 3 if cs_emit_tier == 2 & inlist(vent_tier, 5)
	replace cs_exp_tier = 2 if cs_emit_tier == 2 & inlist(vent_tier, 3)
	replace cs_exp_tier = 1 if cs_emit_tier == 2 & inlist(vent_tier, 2)
	replace cs_exp_tier = 2 if cs_emit_tier == 1 & inlist(vent_tier, 5)
	replace cs_exp_tier = 1 if cs_emit_tier == 1 & inlist(vent_tier, 3)
	replace cs_exp_tier = 0 if cs_emit_tier == 1 & inlist(vent_tier, 2)
	replace cs_exp_tier = 1 if cs_emit_tier == 0 & inlist(vent_tier, 5)
	replace cs_exp_tier = 0 if cs_emit_tier == 0 & inlist(vent_tier, 2, 3)
	replace cs_exp_tier = cs_emit_tier if cs_exp_tier == . & vent_tier == .

	egen exp_traditional_mode = mode(cs_exp_tier) if inlist(mainstove, 2), min
	egen exp_manufacturedbio_mode = mode(cs_exp_tier) if inlist(mainstove, 3), min
	replace cs_exp_tier = exp_traditional_mode if inlist(mainstove, 2) & cs_exp_tier == .
	replace cs_exp_tier = exp_manufacturedbio_mode if inlist(mainstove, 3) & cs_exp_tier == .
	replace cs_exp_tier = 0 if inlist(mainstove, 1) & cs_exp_tier == .
	replace cs_exp_tier = 5 if inlist(mainstove, 4, 5, 6, 7, 8) & cs_exp_tier == .
	capture drop exp_traditional_mode exp_manufacturedbio_mode

	lab val cs_exp_tier tier
	lab var cs_exp_tier "Cooking: Exposure Tier (emission × ventilation)"


	*===========================================================================
	*  B. EFFICIENCY TIER
	*  ISO thermal efficiency by stove type (MTF standard)
	*===========================================================================

	capture drop cs_efcy_tier
	gen cs_efcy_tier = .
	replace cs_efcy_tier = 0 if inlist(mainstove, 1, 2)
	replace cs_efcy_tier = 3 if mainstove == 3
	replace cs_efcy_tier = 4 if mainstove == 4
	replace cs_efcy_tier = 5 if inlist(mainstove, 5, 6, 7, 8)
	lab val cs_efcy_tier tier
	lab var cs_efcy_tier "Cooking: Efficiency Tier (ISO thermal efficiency)"


	*===========================================================================
	*  C. CONVENIENCE TIER
	*  Weekly fuel collection + prep time (hr/wk) from cs_fcol_fpre
	*===========================================================================

	capture drop cs_conv_tier
	gen cs_conv_tier = .
	replace cs_conv_tier = 1 if cs_fcol_fpre >= 7   & cs_fcol_fpre != .
	replace cs_conv_tier = 2 if cs_fcol_fpre >= 3   & cs_fcol_fpre != . & cs_conv_tier == .
	replace cs_conv_tier = 3 if cs_fcol_fpre >= 1.5 & cs_fcol_fpre != . & cs_conv_tier == .
	replace cs_conv_tier = 4 if cs_fcol_fpre >= 0.5 & cs_fcol_fpre != . & cs_conv_tier == .
	replace cs_conv_tier = 5 if cs_fcol_fpre <  0.5 & cs_fcol_fpre != . & cs_conv_tier == .
	replace cs_conv_tier = 5 if inlist(mainstove, 4, 5, 6, 7, 8)
	replace cs_conv_tier = 5 if cs_conv_tier == .
	lab val cs_conv_tier tier
	lab var cs_conv_tier "Cooking: Convenience Tier (fuel time hr/wk)"


	*===========================================================================
	*  D. SAFETY TIER
	*  Based on SEC_G_Q23 injury severity (ESMAP MTF standard methodology)
	*===========================================================================

	capture drop cs_sfty_tier
	gen cs_sfty_tier = .
	replace cs_sfty_tier = 0 if SEC_G_Q23 == 1
	replace cs_sfty_tier = 2 if inlist(SEC_G_Q23, 2, 5, 7)
	replace cs_sfty_tier = 3 if inlist(SEC_G_Q23, 3, 4, 6)
	replace cs_sfty_tier = 5 if cs_sfty_tier == . & SEC_G_Q23 == 111
	replace cs_sfty_tier = 5 if cs_sfty_tier == .
	lab val cs_sfty_tier tier
	lab var cs_sfty_tier "Cooking: Safety Tier (injury severity past 12 months)"


	*===========================================================================
	*  E. AFFORDABILITY TIER
	*  Annual cooking fuel spend / total HH expenditure (MTF 5% threshold)
	*===========================================================================

	capture drop cookingfuel_exp_tot_yr cookfuel_share_yr cs_affd_tier
	gen cookingfuel_exp_tot_yr = fuel_exp_tot_yr
	* Electric cooking fuel expenditure derived from electricity billing

	gen cookfuel_share_yr = cookingfuel_exp_tot_yr / exp_total_yr if exp_total_yr != 0 & exp_total_yr != .
	gen cs_affd_tier = 2 if cookfuel_share_yr >= 0.05 & cookfuel_share_yr != .
	replace cs_affd_tier = 5 if cookfuel_share_yr < 0.05  & cookfuel_share_yr != .
	replace cs_affd_tier = 5 if cs_affd_tier == .
	lab val cs_affd_tier tier
	lab var cs_affd_tier "Cooking: Affordability Tier (fuel <5% HH exp)"


	*===========================================================================
	*  F. AVAILABILITY TIER
	*  Primary fuel availability from SEC_G_Q17 (ESMAP MTF standard methodology)
	*===========================================================================

	capture drop cs_avbl_tier
	gen cs_avbl_tier = .
	replace cs_avbl_tier = 2 if inlist(SEC_G_Q17, 4)
	replace cs_avbl_tier = 3 if inlist(SEC_G_Q17, 3)
	replace cs_avbl_tier = 4 if inlist(SEC_G_Q17, 2)
	replace cs_avbl_tier = 5 if inlist(SEC_G_Q17, 1)

	egen avl_threestone_mode = mode(cs_avbl_tier) if inlist(mainstove, 1), min
	replace cs_avbl_tier = avl_threestone_mode if inlist(mainstove, 1) & cs_avbl_tier == .
	egen avl_gas_mode = mode(cs_avbl_tier) if inlist(mainstove, 4), min
	replace cs_avbl_tier = avl_gas_mode if inlist(mainstove, 4) & cs_avbl_tier == .
	replace cs_avbl_tier = 5 if inlist(mainstove, 5, 6, 7, 8) & cs_avbl_tier == .
	replace cs_avbl_tier = 5 if cs_avbl_tier == .
	capture drop avl_threestone_mode avl_gas_mode

	lab val cs_avbl_tier tier
	lab var cs_avbl_tier "Cooking: Availability Tier (fuel supply reliability)"


	*---------------------------------------------------------------------------
	* Save
	*---------------------------------------------------------------------------
	save "$wip_hh/$master_dta", replace
	di " 04_cooking_attributes.do complete"
