
	**************************************************************************
	*  05_cooking_aggregate.do                                               *
	*  Namibia MTF Pipeline — Aggregate MECS Cooking Tier & Stove Type      *
	*                                                                        *
	*  Produces:                                                             *
	*    cs_aggr_tier     — Aggregate MECS tier (min of 6 attributes)        *
	*    mecs_access      — Binary: household has cooking access (Tier 1+)   *
	*    stove_primary_type — Stove category for disaggregation (1–5)       *
	**************************************************************************

	use "$wip_hh/$master_dta", clear
	set more off

	label define tier 0 "Tier 0" 1 "Tier 1" 2 "Tier 2" 3 "Tier 3" 4 "Tier 4" 5 "Tier 5", replace


	*===========================================================================
	*  Aggregate MECS Cooking Tier
	*  Operational MECS standard (Kat line 3750): min of Exposure, Convenience, Safety, Availability
	*===========================================================================

	capture drop cs_aggr_tier cs_aggr_tier_6attr
	egen cs_aggr_tier = rmin(cs_exp_tier cs_conv_tier cs_sfty_tier cs_avbl_tier)
	lab val cs_aggr_tier tier
	lab var cs_aggr_tier "Cooking MECS: Aggregate Tier (min of 4 operational attributes)"

	egen cs_aggr_tier_6attr = rmin(cs_exp_tier cs_efcy_tier cs_conv_tier cs_sfty_tier cs_affd_tier cs_avbl_tier)
	lab val cs_aggr_tier_6attr tier
	lab var cs_aggr_tier_6attr "Cooking MECS: Full 6-Attribute Tier"


	*===========================================================================
	*  Binary MECS access indicator (Tier 1+)
	*===========================================================================

	capture drop mecs_access mecs_modern mecs_trans
	gen mecs_access = (cs_aggr_tier >= 1) if cs_aggr_tier != .
	lab define mecs_access 0 "No MECS Access (Tier 0)" 1 "MECS Access (Tier 1+)", replace
	lab val mecs_access mecs_access
	lab var mecs_access "MECS Cooking Access (Tier 1 or above)"

	* Modern Energy Cooking Services (Tier 4–5)
	gen mecs_modern = (cs_aggr_tier >= 4) if cs_aggr_tier != .
	lab var mecs_modern "MECS Modern (Tier 4–5): clean fuel stove"

	* Transitional cooking (Tier 2–3)
	gen mecs_trans = inlist(cs_aggr_tier, 2, 3) if cs_aggr_tier != .
	lab var mecs_trans "MECS Transitional (Tier 2–3): ICS or improved fuel"


	*===========================================================================
	*  Stove primary type for disaggregated analysis
	*===========================================================================

	gen stove_primary_type = .
	replace stove_primary_type = 1 if inlist(mainstove, 1)           // Three-stone / open fire
	replace stove_primary_type = 2 if inlist(mainstove, 2, 3)        // Traditional / ICS biomass
	replace stove_primary_type = 3 if mainstove == 4                  // LPG / Cooking gas
	replace stove_primary_type = 4 if inlist(mainstove, 7, 8)        // Biogas / biofuel
	replace stove_primary_type = 5 if inlist(mainstove, 5, 6)        // Electric / solar cooker

	lab define stove_primary_type ///
		1 "Three-stone / Open Fire"    ///
		2 "Traditional / Biomass ICS"  ///
		3 "LPG / Cooking Gas"          ///
		4 "Biogas / Biofuel"           ///
		5 "Electric / Solar Cooker", replace
	lab val stove_primary_type stove_primary_type
	lab var stove_primary_type "Primary Cookstove Category"


	*---------------------------------------------------------------------------
	* Save
	*---------------------------------------------------------------------------
	save "$wip_hh/$master_dta", replace
	di " 05_cooking_aggregate.do complete"
