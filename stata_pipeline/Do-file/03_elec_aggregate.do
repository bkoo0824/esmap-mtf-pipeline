
	**************************************************************************
	*  03_elec_aggregate.do                                                  *
	*  Namibia MTF Pipeline — Aggregate Electricity Tier & Technology Type  *
	*                                                                        *
	*  Produces:                                                             *
	*    elc_aggr_tier    — Aggregate electricity tier (0–5)                 *
	*    elec_access      — Binary: household has electricity access (T1+)   *
	*    elec_tech_type   — Technology category (1–7)                        *
	**************************************************************************

	use "$wip_hh/$master_dta", clear
	set more off


		*===========================================================================
	*  Aggregate Electricity Tier
	*  = min across all 7 attribute tiers
	*  Note: reliability, quality, formality only apply to grid/mini-grid.
	*  For off-grid HHs those attributes are missing (.) → excluded from rmin.
	*===========================================================================

	gen elc_rel_tier_adj  = elc_rel_tier
	gen elc_qual_tier_adj = elc_qual_tier
	gen elc_leg_tier_adj  = elc_leg_tier

	* Aggregate = minimum across all applicable attribute tiers
	* Native Stata rmin() ignores missing values (.) for non-grid technologies
	egen elc_aggr_tier = rmin( ///
		elc_cap_tier      ///    A. Capacity
		elc_avbl_tier     ///    B. Availability (day+evening)
		elc_rel_tier      ///    C. Reliability  (grid/mini only)
		elc_qual_tier     ///    D. Quality       (grid/mini only)
		elc_affrd_tier    ///    G. Affordability
		elc_leg_tier      ///    E. Formality     (grid/mini only)
		elc_sft_tier      ///    F. Safety
	)
	label define tier 0 "Tier 0" 1 "Tier 1" 2 "Tier 2" 3 "Tier 3" 4 "Tier 4" 5 "Tier 5", replace
	lab val elc_aggr_tier tier
	lab var elc_aggr_tier "Electricity: Aggregate Tier (min of 7 attributes)"


	*===========================================================================
	*  Binary electricity access indicator (Tier 1+)
	*===========================================================================

	gen elec_access = (elc_aggr_tier >= 1) if elc_aggr_tier != .
	lab define elec_access 0 "No Access (Tier 0)" 1 "Has Access (Tier 1+)", replace
	lab val elec_access elec_access
	lab var elec_access "Electricity Access (Tier 1 or above)"


	*===========================================================================
	*  Technology type category (for disaggregation and alignment analysis)
	*===========================================================================

	gen elec_tech_type = .
	replace elec_tech_type = 1 if SEC_C_Q162 == 1    // National Grid
	replace elec_tech_type = 2 if SEC_C_Q162 == 2    // Mini-Grid
	replace elec_tech_type = 3 if SEC_C_Q162 == 3    // Generator
	replace elec_tech_type = 4 if SEC_C_Q162 == 6    // Solar Home System (SHS)
	replace elec_tech_type = 5 if SEC_C_Q162 == 5    // Solar Lighting System (SLS)
	replace elec_tech_type = 6 if SEC_C_Q162 == 4    // Solar Lantern (SL)
	replace elec_tech_type = 7 if SEC_C_Q162 == 7    // Rechargeable Battery
	replace elec_tech_type = 8 if inlist(SEC_C_Q162, 8, 111) // No Access / Dry-cell

	lab define elec_tech_type ///
		1 "National Grid"       ///
		2 "Mini-Grid"           ///
		3 "Generator"           ///
		4 "Solar Home System"   ///
		5 "Solar Lighting System" ///
		6 "Solar Lantern"       ///
		7 "Rechargeable Battery" ///
		8 "No Electricity / Dry-cell", replace
	lab val elec_tech_type elec_tech_type
	lab var elec_tech_type "Primary Electricity Technology"

	capture drop grid_hh solar_hh elc_t45
	gen byte grid_hh  = (elec_tech_type == 1)
	gen byte solar_hh = inlist(elec_tech_type, 4, 5, 6)
	gen byte elc_t45  = inlist(elc_aggr_tier, 4, 5)
	lab var grid_hh  "Connected to National Grid"
	lab var solar_hh "Uses Off-Grid Solar Solution"
	lab var elc_t45  "High Electricity Access (Tier 4 or 5)"

	*---------------------------------------------------------------------------
	* Save
	*---------------------------------------------------------------------------
	save "$wip_hh/$master_dta", replace
	di " 03_elec_aggregate.do complete"
