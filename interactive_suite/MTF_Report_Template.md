<!--
================================================================================
ESMAP MULTI-TIER FRAMEWORK (MTF) AUTOMATED REPORT TEMPLATE — PLACEHOLDER INVENTORY
================================================================================
This master comment block documents every placeholder recognized and processed
by the automated MTF reporting pipeline (mtf_calibrator.py, 07_export.do, and
inject_report.py).

Placeholders follow standard mustache syntax: double curly braces enclosing the variable name.
All placeholders are replaced dynamically during calibration and report injection.

--------------------------------------------------------------------------------
1. METADATA & ADMINISTRATIVE CONFIGURATION PLACEHOLDERS
--------------------------------------------------------------------------------
{{COUNTRY_NAME}}               : Full official name of client country (e.g. Liberia, Guinea-Bissau)
{{SURVEY_YEAR}}                : Survey implementation / fieldwork year (e.g. 2024)
{{CURRENCY_CODE}}              : ISO 3-letter local currency code (e.g. LRD, NAD, XOF)
{{ADMIN1_COUNT}}               : Total count of Admin 1 subnational divisions (e.g. 15, 9)
{{ADMIN1_UNIT_LABEL}}          : Singular Admin 1 unit name capitalized (e.g. County, Region)
{{ADMIN1_UNIT_LABEL_PLURAL}}   : Plural Admin 1 unit name capitalized (e.g. Counties, Regions)
{{STRATA_COUNT}}               : Total survey sampling strata count (Admin 1 × Locality)
{{COOKSTOVE_TYPOLOGY_TABLE}}   : Pre-rendered Markdown table for Box 3 from cookstove_calibration.csv
{{COOKSTOVE_STATS_TABLE_ROWS}} : Pre-rendered Markdown rows for Table 3.1 from cookstove_calibration.csv

--------------------------------------------------------------------------------
2. PUBLICATION VISUALIZATION CHARTS (14 SEQUENTIAL SUITE FIGURES)
--------------------------------------------------------------------------------
{{CHART_ELEC_TIERS}}           : Figure 1  — Electricity Tier Distribution (01_elec_tier_distribution.png)
{{CHART_SOURCE_MIX}}           : Figure 2  — Technology Source Mix & Dry-Cell Exclusion (11_electricity_source_mix.png)
{{CHART_SOLAR_TYPOLOGY}}       : Figure 2B — Off-Grid Solar Device Typology (02b_solar_device_breakdown.png)
{{CHART_QUINTILE_CURVE}}       : Figure 3  — Access Across Expenditure Quintiles (04_quintile_access_curve.png)
{{CHART_UNDER_GRID}}           : Figure 4  — Under-the-Grid Densification Funnel (10_under_the_grid_funnel.png)
{{CHART_GRID_BARRIERS}}        : Figure 5  — Stated Barriers to Gaining Grid Connection (06_grid_barriers_wtp.png)
{{CHART_WTP_GRID}}             : Figure 6  — Grid Connection WTP Cumulative Demand Curve (12a_wtp_grid_connection.png)
{{CHART_WTP_SOLAR}}            : Figure 7  — Off-Grid Solar WTP Cumulative Demand Curve (12b_wtp_solar_device.png)
{{CHART_STOVE_FUELS}}          : Figure 8  — Primary Cookstove Typology & Fuel Mix (07_stove_technology_fuels.png)
{{CHART_COOKING_TIERS}}        : Figure 9  — MECS Cooking Tier Distribution (02_cooking_tier_distribution.png)
{{CHART_STOVE_STACKING}}       : Figure 10 — Clean Cooking Stacking & Exposure Dilution (14_stove_stacking_matrix.png)
{{CHART_WTP_COOKSTOVE}}        : Figure 11 — Clean Cookstove WTP Cumulative Demand Curve (12c_wtp_cookstove.png)
{{CHART_GENDER_ACCESS}}        : Figure 12 — Gender Demographics, Credit & Access Parity (08_gender_demographics_access.png)
{{CHART_GENDER_FUEL}}          : Figure 13 — Gender Time-Use Burden for Fuel Collection (05_gender_fuel_collection_time.png)

--------------------------------------------------------------------------------
3. EXECUTIVE SUMMARY & TABLE 1.1 DASHBOARD PLACEHOLDERS
--------------------------------------------------------------------------------
{{ELEC_ACC_NAT}}               : Electricity access rate (Tier 1+) nationwide (%) [JSON: ELEC_ACC_NAT]
{{ELEC_ACC_URB}}               : Electricity access rate (Tier 1+) urban (%) [JSON: ELEC_ACC_URB]
{{ELEC_ACC_RUR}}               : Electricity access rate (Tier 1+) rural (%) [JSON: ELEC_ACC_RUR]
{{ELEC_T0_NAT}}                : Electricity Tier 0 rate nationwide (%) [JSON: ELEC_T0_NAT]
{{ELEC_T0_URB}}                : Electricity Tier 0 rate urban (%) [JSON: ELEC_T0_URB]
{{ELEC_T0_RUR}}                : Electricity Tier 0 rate rural (%) [JSON: ELEC_T0_RUR]
{{ELEC_T45_NAT}}               : High electricity access rate (Tier 4–5) nationwide (%) [JSON: ELEC_T45_NAT]
{{ELEC_T45_URB}}               : High electricity access rate (Tier 4–5) urban (%) [JSON: ELEC_T45_URB]
{{ELEC_T45_RUR}}               : High electricity access rate (Tier 4–5) rural (%) [JSON: ELEC_T45_RUR]
{{GRID_ACC_NAT}}               : Main electricity source: national grid nationwide (%) [JSON: GRID_ACC_NAT]
{{GRID_ACC_URB}}               : Main electricity source: national grid urban (%) [JSON: GRID_ACC_URB]
{{GRID_ACC_RUR}}               : Main electricity source: national grid rural (%) [JSON: GRID_ACC_RUR]
{{SOLAR_ACC_NAT}}              : Main electricity source: off-grid solar nationwide (%) [JSON: SOLAR_ACC_NAT]
{{SOLAR_ACC_URB}}              : Main electricity source: off-grid solar urban (%) [JSON: SOLAR_ACC_URB]
{{SOLAR_ACC_RUR}}              : Main electricity source: off-grid solar rural (%) [JSON: SOLAR_ACC_RUR]
{{MECS_ACC_NAT}}               : Modern Energy Cooking Services (MECS Tier 1+) nationwide (%) [JSON: MECS_ACC_NAT]
{{MECS_ACC_URB}}               : Modern Energy Cooking Services (MECS Tier 1+) urban (%) [JSON: MECS_ACC_URB]
{{MECS_ACC_RUR}}               : Modern Energy Cooking Services (MECS Tier 1+) rural (%) [JSON: MECS_ACC_RUR]
{{TRANS_COOK_NAT}}             : Transitional cooking (MECS Tier 2–3) nationwide (%) [JSON: TRANS_COOK_NAT]
{{TRANS_COOK_URB}}             : Transitional cooking (MECS Tier 2–3) urban (%) [JSON: TRANS_COOK_URB]
{{TRANS_COOK_RUR}}             : Transitional cooking (MECS Tier 2–3) rural (%) [JSON: TRANS_COOK_RUR]
{{COOK_T0_NAT}}                : Cooking Tier 0 (unimproved/high exposure) nationwide (%) [JSON: COOK_T0_NAT]
{{COOK_T0_URB}}                : Cooking Tier 0 (unimproved/high exposure) urban (%) [JSON: COOK_T0_URB]
{{COOK_T0_RUR}}                : Cooking Tier 0 (unimproved/high exposure) rural (%) [JSON: COOK_T0_RUR]
{{COOK_T01_NAT}}               : Cooking Tiers 0-1 (No Access) nationwide (%) [JSON: COOK_T01_NAT]
{{COOK_T01_URB}}               : Cooking Tiers 0-1 (No Access) urban (%) [JSON: COOK_T01_URB]
{{COOK_T01_RUR}}               : Cooking Tiers 0-1 (No Access) rural (%) [JSON: COOK_T01_RUR]
{{CLEAN_STOVE_NAT}}            : Primary stove clean fuels (LPG/Electric) nationwide (%) [JSON: CLEAN_STOVE_NAT]
{{CLEAN_STOVE_URB}}            : Primary stove clean fuels (LPG/Electric) urban (%) [JSON: CLEAN_STOVE_URB]
{{CLEAN_STOVE_RUR}}            : Primary stove clean fuels (LPG/Electric) rural (%) [JSON: CLEAN_STOVE_RUR]
{{THREESTONE_NAT}}             : Primary stove three-stone fire / open flame nationwide (%) [JSON: THREESTONE_NAT]
{{THREESTONE_URB}}             : Primary stove three-stone fire / open flame urban (%) [JSON: THREESTONE_URB]
{{THREESTONE_RUR}}             : Primary stove three-stone fire / open flame rural (%) [JSON: THREESTONE_RUR]
{{UNDER_THE_GRID_NAT}}         : Households residing in electrified EAs nationwide (%) [JSON: UNDER_THE_GRID_NAT]
{{UNDER_THE_GRID_URB}}         : Households residing in electrified EAs urban (%) [JSON: UNDER_THE_GRID_URB]
{{UNDER_THE_GRID_RUR}}         : Households residing in electrified EAs rural (%) [JSON: UNDER_THE_GRID_RUR]
{{UNDER_GRID_UNCONNECTED_NAT}} : Households in electrified EAs without connection nationwide (%) [JSON: UNDER_GRID_UNCONNECTED_NAT]
{{UNDER_GRID_UNCONNECTED_URB}} : Households in electrified EAs without connection urban (%) [JSON: UNDER_GRID_UNCONNECTED_URB]
{{UNDER_GRID_UNCONNECTED_RUR}} : Households in electrified EAs without connection rural (%) [JSON: UNDER_GRID_UNCONNECTED_RUR]
{{GRID_UPTAKE_NAT}}            : Grid connection uptake rate in electrified EAs nationwide (%) [JSON: GRID_UPTAKE_NAT]
{{GRID_UPTAKE_URB}}            : Grid connection uptake rate in electrified EAs urban (%) [JSON: GRID_UPTAKE_URB]
{{GRID_UPTAKE_RUR}}            : Grid connection uptake rate in electrified EAs rural (%) [JSON: GRID_UPTAKE_RUR]
{{AVG_OUTAGES_PER_WEEK}}       : Average weekly unexpected power outages for grid users [JSON: AVG_OUTAGES_PER_WEEK]
{{OUTAGES_LT3_WK}}             : Grid households experiencing <3 outages per week (%) [JSON: OUTAGES_LT3_WK]
{{OUTAGES_3TO14_WK}}           : Grid households experiencing 3–14 outages per week (%) [JSON: OUTAGES_3TO14_WK]
{{OUTAGES_GT14_WK}}            : Grid households experiencing >14 outages per week (%) [JSON: OUTAGES_GT14_WK]
{{PCT_VOLTAGE_DAMAGE}}         : Grid households reporting appliance voltage surge damage (%) [JSON: PCT_VOLTAGE_DAMAGE]
{{PCT_EVE_SHORTAGE}}           : Grid households with evening supply deficit (<4h) (%) [JSON: PCT_EVE_SHORTAGE]
{{BARRIER_COST_NAT}}           : Primary barrier: upfront connection fee too high (%) [JSON: BARRIER_COST_NAT]
{{BARRIER_DIST_NAT}}           : Primary barrier: distance to low-voltage network (%) [JSON: BARRIER_DIST_NAT]
{{WTP_GRID_UPFRONT_NAT}}       : Stated WTP for grid connection upfront nationwide (%) [JSON: WTP_GRID_UPFRONT_NAT]
{{WTP_GRID_12M_NAT}}           : Stated WTP for grid connection over 12 months nationwide (%) [JSON: WTP_GRID_12M_NAT]
{{WTP_GRID_WAIVED_NAT}}         : Stated WTP for grid connection if fee completely waived (%) [JSON: WTP_GRID_WAIVED_NAT]
{{WTP_GRID_NEVER_NAT}}         : Stated refusal rate even if connection fee waived (%) [JSON: WTP_GRID_NEVER_NAT]
{{REFUSE_WIRING_COST_NAT}}     : Refusing/hesitant households citing internal wiring barrier (%) [JSON: REFUSE_WIRING_COST_NAT]
{{PCT_SL_STUCK_T1}}            : Solar lantern users constrained to basic Tier 1 service (%) [JSON: PCT_SL_STUCK_T1]
{{STOVE_3STONE_R}}             : Three-stone open fire primary reliance rural (%) [JSON: STOVE_3STONE_R]
{{STOVE_3STONE_U}}             : Three-stone open fire primary reliance urban (%) [JSON: STOVE_3STONE_U]
{{STOVE_TRAD_N}}               : Traditional metal/ceramic stove primary reliance nationwide (%) [JSON: STOVE_TRAD_N]
{{STOVE_ICS_N}}                : Improved cookstove (ICS) primary reliance nationwide (%) [JSON: STOVE_ICS_N]
{{STOVE_ELEC_N}}               : Electric stove primary reliance nationwide (%) [JSON: STOVE_ELEC_N]
{{STOVE_ELEC_U}}               : Electric stove primary reliance urban (%) [JSON: STOVE_ELEC_U]
{{STOVE_ELEC_R}}               : Electric stove primary reliance rural (%) [JSON: STOVE_ELEC_R]
{{COOK_T5_URB}}                : Cooking Tier 5 access rate urban (%) [JSON: COOK_T5_URB]
{{COOK_T5_RUR}}                : Cooking Tier 5 access rate rural (%) [JSON: COOK_T5_RUR]
{{PCT_CLEAN_STOVE_OWNERSHIP}}  : Households owning at least one clean cooking device (%) [JSON: PCT_CLEAN_STOVE_OWNERSHIP]
{{PCT_STOVE_STACKING}}         : Clean stove owners who stack with traditional stoves (%) [JSON: PCT_STOVE_STACKING]
{{PCT_STACKING_DILUTION}}      : Clean owners remaining in Exposure Tier 0-1 due to stacking (%) [JSON: PCT_STACKING_DILUTION]
{{HR_3STONE_NAT}}              : Mean weekly cooking hours: Three-stone fire [JSON: HR_3STONE_NAT]
{{HR_TRAD_NAT}}                : Mean weekly cooking hours: Traditional charcoal stove [JSON: HR_TRAD_NAT]
{{HR_ICS_NAT}}                 : Mean weekly cooking hours: Improved cookstove (ICS) [JSON: HR_ICS_NAT]
{{HR_LPG_NAT}}                 : Mean weekly cooking hours: LPG stove [JSON: HR_LPG_NAT]
{{HR_ELEC_NAT}}                : Mean weekly cooking hours: Electric stove [JSON: HR_ELEC_NAT]
{{FHH_SHARE}}                  : Share of female-headed households nationwide (%) [JSON: FHH_SHARE]
{{MHH_SHARE}}                  : Share of male-headed households nationwide (%) [JSON: MHH_SHARE]
{{HEAD_AGE_FHH}}               : Average age of female household heads (years) [JSON: HEAD_AGE_FHH]
{{HEAD_AGE_MHH}}               : Average age of male household heads (years) [JSON: HEAD_AGE_MHH]
{{HEAD_MARITAL_WIDOW_FHH}}     : Widowed rate among female household heads (%) [JSON: HEAD_MARITAL_WIDOW_FHH]
{{HEAD_MARITAL_WIDOW_MHH}}     : Widowed rate among male household heads (%) [JSON: HEAD_MARITAL_WIDOW_MHH]
{{CREDIT_ACCESS_FHH}}          : Formal credit access rate among female heads (%) [JSON: CREDIT_ACCESS_FHH]
{{CREDIT_ACCESS_MHH}}          : Formal credit access rate among male heads (%) [JSON: CREDIT_ACCESS_MHH]
{{WTP_GRID_UPFRONT_FHH}}       : Upfront grid connection WTP among female-headed HHs (%) [JSON: WTP_GRID_UPFRONT_FHH]
{{WTP_GRID_UPFRONT_MHH}}       : Upfront grid connection WTP among male-headed HHs (%) [JSON: WTP_GRID_UPFRONT_MHH]
{{WTP_GRID_12M_FHH}}           : 12-month installment grid WTP among female-headed HHs (%) [JSON: WTP_GRID_12M_FHH]
{{COOK_DEC_FEMALE_NAT}}        : Cookstove purchase decisions made by female members (%) [JSON: COOK_DEC_FEMALE_NAT]
{{COOK_DEC_MALE_NAT}}          : Cookstove purchase decisions made by male members (%) [JSON: COOK_DEC_MALE_NAT]
{{COOK_DEC_JOINT_NAT}}         : Cookstove purchase decisions made jointly (%) [JSON: COOK_DEC_JOINT_NAT]
{{WOMEN_COOK_TIME}}            : Mean daily cooking time for adult women (minutes/day) [JSON: WOMEN_COOK_TIME]
{{MEN_COOK_TIME}}              : Mean daily cooking time for adult men (minutes/day) [JSON: MEN_COOK_TIME]
{{WOMEN_FUEL_TIME}}            : Mean daily fuelwood gathering time for adult women (min/day) [JSON: WOMEN_FUEL_TIME]
{{MEN_FUEL_TIME}}              : Mean daily fuelwood gathering time for adult men (min/day) [JSON: MEN_FUEL_TIME]
{{WOMEN_FUEL_WORKDAYS}}        : Annual full working days (8h) lost to fuelwood collection [JSON: WOMEN_FUEL_WORKDAYS]

--------------------------------------------------------------------------------
4. CHAPTER 2: ELECTRICITY DIAGNOSTIC & TABLE 2.1 PLACEHOLDERS
--------------------------------------------------------------------------------
{{ELEC_T0_N}} / {{ELEC_T0_U}} / {{ELEC_T0_R}} : Tier 0 National, Urban, Rural (%) [JSON: ELEC_T0_N / U / R]
{{ELEC_T1_N}} / {{ELEC_T1_U}} / {{ELEC_T1_R}} : Tier 1 National, Urban, Rural (%) [JSON: ELEC_T1_N / U / R]
{{ELEC_T2_N}} / {{ELEC_T2_U}} / {{ELEC_T2_R}} : Tier 2 National, Urban, Rural (%) [JSON: ELEC_T2_N / U / R]
{{ELEC_T3_N}} / {{ELEC_T3_U}} / {{ELEC_T3_R}} : Tier 3 National, Urban, Rural (%) [JSON: ELEC_T3_N / U / R]
{{ELEC_T4_N}} / {{ELEC_T4_U}} / {{ELEC_T4_R}} : Tier 4 National, Urban, Rural (%) [JSON: ELEC_T4_N / U / R]
{{ELEC_T5_N}} / {{ELEC_T5_U}} / {{ELEC_T5_R}} : Tier 5 National, Urban, Rural (%) [JSON: ELEC_T5_N / U / R]
{{Q1_ELEC_ACC}} ... {{Q5_ELEC_ACC}}           : Electricity access by expenditure quintile Q1–Q5 (%) [JSON: Q1_ELEC_ACC ... Q5_ELEC_ACC]
{{Q1_MECS_ACC}} ... {{Q5_MECS_ACC}}           : MECS cooking access by expenditure quintile Q1–Q5 (%) [JSON: Q1_MECS_ACC ... Q5_MECS_ACC]
{{IS_VERYLOW_NAT/URB/RUR}}                    : Ownership of Tier 1 Very Low-Load appliances (%) [JSON: IS_VERYLOW_NAT/URB/RUR]
{{IS_LOW_NAT/URB/RUR}}                        : Ownership of Tier 2 Low-Load appliances (%) [JSON: IS_LOW_NAT/URB/RUR]
{{IS_MED_NAT/URB/RUR}}                        : Ownership of Tier 3 Medium-Load appliances (%) [JSON: IS_MED_NAT/URB/RUR]
{{IS_HIGH_NAT/URB/RUR}}                       : Ownership of Tier 4 High-Load appliances (%) [JSON: IS_HIGH_NAT/URB/RUR]
{{IS_VERYHIGH_NAT/URB/RUR}}                   : Ownership of Tier 5 Very High-Load appliances (%) [JSON: IS_VERYHIGH_NAT/URB/RUR]
{{HAS_LIGHTS_NAT}}                            : Households with electric lighting points (%) [JSON: HAS_LIGHTS_NAT]
{{HAS_CHARGER_NAT}}                           : Households with mobile phone charger (%) [JSON: HAS_CHARGER_NAT]
{{HAS_RADIO_NAT}}                             : Households with radio / sound system (%) [JSON: HAS_RADIO_NAT]
{{HAS_TV_NAT}}                                : Households with television (%) [JSON: HAS_TV_NAT]
{{HAS_FAN_NAT}}                               : Households with electric fan (%) [JSON: HAS_FAN_NAT]
{{HAS_FRIDGE_NAT}}                            : Households with refrigerator / freezer (%) [JSON: HAS_FRIDGE_NAT]
{{HAS_IRON_NAT}}                              : Households with electric iron (%) [JSON: HAS_IRON_NAT]
{{HAS_MICRO_NAT}}                             : Households with microwave (%) [JSON: HAS_MICRO_NAT]
{{HAS_WASH_NAT}}                              : Households with washing machine (%) [JSON: HAS_WASH_NAT]
{{HAS_AC_NAT}}                                : Households with air conditioning (%) [JSON: HAS_AC_NAT]
{{HAS_GEYSER_NAT}}                            : Households with water heater / geyser (%) [JSON: HAS_GEYSER_NAT]
{{HAS_ELECTRIC_LIGHTS_NAT}}                    : Households with electric lighting points (%) [JSON: HAS_ELECTRIC_LIGHTS_NAT]
{{HAS_SOLAR_LIGHTS_NAT}}                       : Households with solar lighting points (%) [JSON: HAS_SOLAR_LIGHTS_NAT]
{{HAS_ANY_LIGHTS_NAT}}                         : Households with any electric or solar lights (%) [JSON: HAS_ANY_LIGHTS_NAT]
{{PCT_CAP_LIMITED}}                           : Grid households facing capacity deficit (%) [JSON: PCT_CAP_LIMITED]
{{GRID_YEARS_NAT/URB/RUR}}                    : Mean years connected to national grid [JSON: GRID_YEARS_NAT/URB/RUR]
{{GRID_WAIT_DAYS_NAT}}                        : Mean days elapsed to obtain connection [JSON: GRID_WAIT_DAYS_NAT]
{{GRID_MONTHLY_SPEND_NAT/URB/RUR}}            : Mean monthly grid electricity spending (currency) [JSON: GRID_MONTHLY_SPEND_NAT/URB/RUR]
{{BARRIER_COST_URB/RUR}}                      : Connection fee barrier in urban/rural areas (%) [JSON: BARRIER_COST_URB/RUR]
{{BARRIER_DIST_URB/RUR}}                      : Grid distance barrier in urban/rural areas (%) [JSON: BARRIER_DIST_URB/RUR]
{{BARRIER_TARIFF_NAT/URB/RUR}}                : High monthly tariff barrier (%) [JSON: BARRIER_TARIFF_NAT/URB/RUR]
{{BARRIER_LANDLORD_NAT/URB/RUR}}              : Landlord permission / tenancy barrier (%) [JSON: BARRIER_LANDLORD_NAT/URB/RUR]
{{BARRIER_UNREL_NAT/URB/RUR}}                 : Unreliable service deterrent barrier (%) [JSON: BARRIER_UNREL_NAT/URB/RUR]
{{BARRIER_ADMIN_NAT/URB/RUR}}                 : Administrative delay / bureaucracy barrier (%) [JSON: BARRIER_ADMIN_NAT/URB/RUR]
{{WTP_GRID_UPFRONT_URB/RUR}}                  : Upfront grid WTP in urban/rural areas (%) [JSON: WTP_GRID_UPFRONT_URB/RUR]
{{WTP_GRID_3M_NAT}}                           : Grid connection WTP under 3-month plan (%) [JSON: WTP_GRID_3M_NAT]
{{WTP_GRID_6M_NAT}}                           : Grid connection WTP under 6-month plan (%) [JSON: WTP_GRID_6M_NAT]
{{WTP_GRID_WAIVED_NAT}}                       : Grid connection WTP if fee completely waived (%) [JSON: WTP_GRID_WAIVED_NAT]
{{WTP_SOLAR_UPFRONT_NAT}}                     : Solar Home System WTP upfront nationwide (%) [JSON: WTP_SOLAR_UPFRONT_NAT]
{{WTP_SOLAR_6M_NAT}}                          : Solar Home System WTP under 6-month plan (%) [JSON: WTP_SOLAR_6M_NAT]
{{WTP_SOLAR_12M_NAT}}                         : Solar Home System WTP under 12-month plan (%) [JSON: WTP_SOLAR_12M_NAT]
{{WTP_SOLAR_24M_NAT}}                         : Solar Home System WTP under 24-month plan (%) [JSON: WTP_SOLAR_24M_NAT]
{{WTP_SOLAR_NEVER_NAT}}                       : Share refusing solar purchase regardless of terms (%) [JSON: WTP_SOLAR_NEVER_NAT]
{{REFUSE_SOLAR_COST_NAT}}                     : Solar refusers citing unaffordable device cost (%) [JSON: REFUSE_SOLAR_COST_NAT]
{{OFF_GRID_FUND_AWARE_NAT/URB/RUR}}           : Awareness of government off-grid fund/revolving loan (%) [JSON: SRF_AWARE_* / OFF_GRID_FUND_AWARE_*]
{{GRID_BACKUP_CANDLE_NAT/URB/RUR}}            : Grid backup lighting: candles (%) [JSON: GRID_BACKUP_CANDLE_NAT/URB/RUR]
{{GRID_BACKUP_TORCH_NAT}}                     : Grid backup lighting: dry-cell torch (%) [JSON: GRID_BACKUP_TORCH_NAT]
{{GRID_BACKUP_SOLAR_NAT}}                     : Grid backup lighting: solar lantern / SHS (%) [JSON: GRID_BACKUP_SOLAR_NAT]
{{GRID_BACKUP_NONE_NAT}}                      : Grid backup lighting: no alternative source (%) [JSON: GRID_BACKUP_NONE_NAT]

--------------------------------------------------------------------------------
5. CHAPTER 3: MODERN ENERGY COOKING SOLUTIONS & TABLE 3.1 PLACEHOLDERS
--------------------------------------------------------------------------------
{{COOK_T0_NAT}} ... {{COOK_T5_NAT}}           : MECS Cooking Tiers 0 to 5 nationwide (%) [JSON: COOK_T0_NAT ... COOK_T5_NAT]
{{COOK_T0_URB}} ... {{COOK_T5_URB}}           : MECS Cooking Tiers 0 to 5 urban (%) [JSON: COOK_T0_URB ... COOK_T5_URB]
{{COOK_T0_RUR}} ... {{COOK_T5_RUR}}           : MECS Cooking Tiers 0 to 5 rural (%) [JSON: COOK_T0_RUR ... COOK_T5_RUR]
{{STOVE_3STONE_N/U/R}}                        : Three-stone open fire adoption National, Urban, Rural (%) [JSON: STOVE_3STONE_N / U / R]
{{STOVE_TRAD_N/U/R}}                          : Traditional stove adoption National, Urban, Rural (%) [JSON: STOVE_TRAD_N / U / R]
{{STOVE_ICS_N/U/R}}                           : Improved cookstove (ICS) adoption National, Urban, Rural (%) [JSON: STOVE_ICS_N / U / R]
{{STOVE_CLEAN_N/U/R}}                         : Clean fuel (LPG/Biogas) adoption National, Urban, Rural (%) [JSON: STOVE_CLEAN_N / U / R]
{{STOVE_ELEC_N/U/R}}                          : Electric stove adoption National, Urban, Rural (%) [JSON: STOVE_ELEC_N / U / R]
{{ELEC_STOVE_GRID_NAT}}                       : Electric stove ownership among grid-connected HHs (%) [JSON: ELEC_STOVE_GRID_NAT]

--------------------------------------------------------------------------------
6. CHAPTER 4: GENDER ANALYSIS & TABLE 4.1 PLACEHOLDERS
--------------------------------------------------------------------------------
{{MHH_SHARE}} / {{FHH_SHARE}}                  : Share of male / female-headed households (%) [JSON: MHH_SHARE / FHH_SHARE]
{{HEAD_AGE_MHH}} / {{HEAD_AGE_FHH}}           : Average age of male / female head (years) [JSON: HEAD_AGE_MHH / HEAD_AGE_FHH]
{{HEAD_AGE_NAT}}                              : National average age of household head (years) [JSON: HEAD_AGE_NAT]
{{HEAD_EDUC_NONE_MHH/FHH/NAT}}                : Head has no formal education for MHH, FHH, National (%) [JSON: MHH/FHH/NAT]
{{HEAD_EDUC_PRIM_MHH/FHH/NAT}}                : Head completed primary education for MHH, FHH, National (%) [JSON: MHH/FHH/NAT]
{{HEAD_EDUC_SEC_MHH/FHH/NAT}}                 : Head completed secondary education for MHH, FHH, National (%) [JSON: MHH/FHH/NAT]
{{HEAD_EDUC_HIGH_MHH/FHH/NAT}}                : Head completed higher education for MHH, FHH, National (%) [JSON: MHH/FHH/NAT]
{{HEAD_MARITAL_MARRIED_MHH/FHH/NAT}}          : Head is married / cohabiting for MHH, FHH, National (%) [JSON: MHH/FHH/NAT]
{{HEAD_MARITAL_WIDOW_MHH/FHH/NAT}}            : Head is widowed for MHH, FHH, National (%) [JSON: MHH/FHH/NAT]
{{CREDIT_ACCESS_MHH/FHH/NAT}}                 : Head has access to credit/loans for MHH, FHH, National (%) [JSON: MHH/FHH/NAT]
{{MHH_ELEC_ACC}} / {{FHH_ELEC_ACC}}           : Electricity access rate (Tier 1+) for MHH / FHH (%) [JSON: MHH_ELEC_ACC / FHH_ELEC_ACC]
{{MHH_MECS_ACC}} / {{FHH_MECS_ACC}}           : MECS cooking access rate for MHH / FHH (%) [JSON: MHH_MECS_ACC / FHH_MECS_ACC]
{{WTP_GRID_UPFRONT_MHH/FHH}}                  : Grid connection upfront WTP for MHH / FHH (%) [JSON: WTP_GRID_UPFRONT_MHH/FHH]
{{WTP_GRID_12M_MHH/FHH}}                      : Grid connection 12-month installment WTP for MHH / FHH (%) [JSON: WTP_GRID_12M_MHH/FHH]
{{WTP_SOLAR_UPFRONT_MHH/FHH}}                 : Solar Home System upfront WTP for MHH / FHH (%) [JSON: WTP_SOLAR_UPFRONT_MHH/FHH]

--------------------------------------------------------------------------------
7. REGIONAL / SUBNATIONAL PLACEHOLDERS (OPTIONAL MODULE / ANNEX)
--------------------------------------------------------------------------------
{{REG_<REGION>_ELEC}}                         : Electricity access rate in specific subnational region (%)
{{REG_<REGION>_GRID}}                         : Grid access rate in specific subnational region (%)
{{REG_<REGION>_SOLAR}}                        : Off-grid solar access rate in specific subnational region (%)
{{REG_<REGION>_T45}}                          : High electricity access rate (Tier 4-5) in region (%)
{{REG_<REGION>_MECS}}                         : MECS clean cooking access rate in region (%)
================================================================================
-->

# ESMAP | BEYOND CONNECTIONS: {{COUNTRY_NAME}} ENERGY ACCESS DIAGNOSTIC REPORT
## REPUBLIC OF {{COUNTRY_NAME}}
### National Household Energy Access Diagnostic Based on the Multi-Tier Framework
**World Bank Group | Energy Sector Management Assistance Program (ESMAP)**  
*In Collaboration with the National Ministry Responsible for Energy and Relevant Utility Entities*  
*Publication Series: Beyond Connections — Energy Access Redefined*

---

## ACKNOWLEDGMENTS

This Energy Access Diagnostic Report presents the empirical baseline findings of the {{SURVEY_YEAR}} Multi-Tier Framework (MTF) National Household Survey in {{COUNTRY_NAME}}. The World Bank Group and the Energy Sector Management Assistance Program (ESMAP) express their deep gratitude to the Government of {{COUNTRY_NAME}}, particularly the Ministry responsible for energy policy, the national power utility, regulatory authorities, and regional administrative directorates. The analytical team acknowledges the critical partnership of the National Bureau of Statistics and survey field enumerators who conducted extensive household interviews across all {{ADMIN1_COUNT}} administrative {{ADMIN1_UNIT_LABEL_PLURAL}} under challenging field conditions.

Special recognition is extended to the thousands of surveyed households across urban centers, formal settlements, peri-urban corridors, and rural communities who generously shared detailed information regarding their energy expenditures, lighting sources, cooking habits, and service quality constraints. The diagnostic report was prepared by a World Bank task team under the leadership of ESMAP, incorporating peer review and technical contributions from international energy specialists, utility engineers, and econometric modelers.

---

## TABLE OF ABBREVIATIONS

| Acronym | Definition |
| :--- | :--- |
| **AC** | Air Conditioner / Alternating Current |
| **AfDB** | African Development Bank |
| **AVR** | Automatic Voltage Regulator |
| **CAPI** | Computer-Assisted Personal Interviewing |
| **CFL** | Compact Fluorescent Lamp |
| **CI** | Confidence Interval (95% Logit-Transformed) |
| **CRM** | Cylinder Recirculation Model (LPG Distribution) |
| **DC** | Direct Current |
| **DRE** | Decentralized Renewable Energy |
| **EA** | Enumeration Area (Primary Sampling Unit) |
| **EPC** | Electric Pressure Cooker |
| **ESMAP** | Energy Sector Management Assistance Program |
| **FHH** | Female-Headed Household |
| **GDP** | Gross Domestic Product |
| **GEAP / GEAPP** | Global Energy Alliance for People and Planet |
| **HAP** | Household Air Pollution |
| **ICS** | Improved Cookstove |
| **IDA** | International Development Association (World Bank) |
| **IEC** | International Electrotechnical Commission |
| **IEA** | International Energy Agency |
| **INE** | National Statistics Institute (Instituto Nacional de Estatística) |
| **ISO** | International Organization for Standardization |
| **kWh** | Kilowatt-hour |
| **LED** | Light-Emitting Diode |
| **LPG** | Liquefied Petroleum Gas |
| **M300** | Mission 300 Africa Energy Compact (World Bank / AfDB) |
| **MECS** | Modern Energy Cooking Services |
| **MHH** | Male-Headed Household |
| **MTF** | Multi-Tier Framework |
| **OPEC** | Organization of the Petroleum Exporting Countries |
| **PAYGo** | Pay-As-You-Go Mobile Digital Financing |
| **PM2.5** | Fine Particulate Matter (< 2.5 micrometers in aerodynamic diameter) |
| **PPS** | Probability Proportional to Size |
| **PSU** | Primary Sampling Unit |
| **PUE** | Productive Use of Energy |
| **RBF** | Results-Based Financing |
| **SDG** | Sustainable Development Goal |
| **SHS** | Solar Home System |
| **SLS** | Solar Lighting System |
| **SREP** | Scaling Up Renewable Energy Program in Low Income Countries |
| **STC** | Short-Term Consultant |
| **UNSD** | United Nations Statistics Division |
| **VAT** | Value-Added Tax |
| **VPT** | Voluntary Performance Targets (ISO Cookstove Standards) |
| **W** | Watt |
| **WHO** | World Health Organization |
| **WTP** | Willingness to Pay |

---

## CURRENCY EQUIVALENTS AND SURVEY METADATA

* **National Currency Unit:** `{{CURRENCY_CODE}}`
* **Currency Reporting:** All monetary figures relating to electricity tariffs, household grid expenditures, willingness-to-pay bidding thresholds, and cooking fuel costs are expressed in `{{CURRENCY_CODE}}` unless explicitly denominated in United States Dollars (US$).
* **Survey Reference Year:** `{{SURVEY_YEAR}}`
* **Geographic Coverage:** National representative sample across all `{{ADMIN1_COUNT}}` administrative `{{ADMIN1_UNIT_LABEL_PLURAL}}`, stratified into `{{STRATA_COUNT}}` distinct urban and rural sampling domains.

---

## EXECUTIVE SUMMARY

### 1. National Context, Survey Background, and SDG 7 Alignment

Access to affordable, reliable, sustainable, and modern energy is an indispensable foundation for economic development, human capital formation, poverty reduction, and industrial transformation. Sustainable Development Goal 7 (SDG 7) establishes two primary global access targets: Target 7.1.1 calls for universal access to electricity by 2030, while Target 7.1.2 mandates universal access to clean cooking fuels and modern technologies. For decades, international monitoring frameworks tracked progress toward these objectives through simplistic binary metrics—classifying households merely as connected or unconnected to the electric grid, and categorizing cooking practices broadly as clean or polluting.

However, binary metrics fail to capture the profound operational realities experienced by households on the ground. A grid connection that delivers erratic power characterized by frequent blackouts, severe voltage sags, and prolonged evening outages cannot operate productive machinery, refrigerate food, or support digital livelihoods. Similarly, a household that acquires a modern liquefied petroleum gas (LPG) stove but continues to cook staple foods over a traditional open biomass fire remains exposed to hazardous levels of fine particulate matter ($PM_{2.5}$) and carbon monoxide ($CO$).

To resolve these analytical deficiencies, the Energy Sector Management Assistance Program (ESMAP) and the World Bank developed the **Multi-Tier Framework (MTF)**. The MTF redefines energy access as a multi-dimensional continuum of service ranging from **Tier 0 (no access or sub-basic service)** to **Tier 5 (continuous, high-capacity, reliable, and safe modern energy)**.

This diagnostic report presents the comprehensive empirical findings of the **{{SURVEY_YEAR}} Multi-Tier Framework National Household Survey** in {{COUNTRY_NAME}}. The survey was administered using Computer-Assisted Personal Interviewing (CAPI) across a nationally representative sample covering all {{ADMIN1_COUNT}} administrative {{ADMIN1_UNIT_LABEL_PLURAL}} and {{STRATA_COUNT}} sampling strata. By evaluating the performance of electricity services across seven technical attributes and assessing cooking practices across six service dimensions, this diagnostic provides policymakers, utility managers, regulatory authorities, and international development financiers with an evidence-based roadmap.

### Core Diagnostic Highlights

Nationwide, `{{ELEC_ACC_NAT}}%` of households have electricity access at Tier 1 or above (`{{ELEC_ACC_URB}}%` in urban areas vs. `{{ELEC_ACC_RUR}}%` in rural areas), while `{{ELEC_T0_NAT}}%` remain in Tier 0. The national grid serves `{{GRID_ACC_NAT}}%` of households (`{{GRID_ACC_URB}}%` urban vs. `{{GRID_ACC_RUR}}%` rural), and off-grid solar systems serve `{{SOLAR_ACC_NAT}}%` (`{{SOLAR_ACC_URB}}%` urban vs. `{{SOLAR_ACC_RUR}}%` rural). Crucially, in electrified communities where the low-voltage distribution network is already physically present, `{{UNDER_GRID_UNCONNECTED_NAT}}%` of households remain unconnected. Raising the connection uptake rate from the current baseline of `{{GRID_UPTAKE_NAT}}%` to 60.0% would add **27.2 percentage points** to national access at minimal capital cost through last-mile densification.

Household connection demand is highly responsive to financing terms. Upfront willingness to pay for a grid connection stands at only `{{WTP_GRID_UPFRONT_NAT}}%`, but surges to `{{WTP_GRID_12M_NAT}}%` when offered a 12-month installment plan and reaches `{{WTP_GRID_WAIVED_NAT}}%` under fee waivers. Among the households declining connection even when connection fees are waived (`{{WTP_GRID_NEVER_NAT}}%`), `{{REFUSE_WIRING_COST_NAT}}%` identify the upfront capital cost of internal household wiring as the primary barrier.

In clean cooking, the national deficit is severe: solid biomass fuels serve over 95% of the population, with `{{THREESTONE_NAT}}%` cooking over three-stone open fires. Modern clean cooking services (MECS Tiers 4–5, comprising LPG and electricity) reach only `{{CLEAN_STOVE_NAT}}%` of households (`{{CLEAN_STOVE_URB}}%` urban vs. `{{CLEAN_STOVE_RUR}}%` rural), with electric cooking confined to fewer than 0.2% (`{{STOVE_ELEC_N}}%`).

This reliance on traditional biomass imposes an acute intra-household time burden on women. While adult women average `{{WOMEN_FUEL_TIME}}` minutes per calendar day collecting firewood (compared to `{{MEN_FUEL_TIME}}` minutes for men), active fuel-collecting trips average 53.5 minutes, resulting in `{{WOMEN_FUEL_WORKDAYS}}` full 8-hour working days lost per woman each year solely to fuel gathering. In addition, female household heads encounter substantial formal credit constraints (`{{CREDIT_ACCESS_FHH}}%` vs. `{{CREDIT_ACCESS_MHH}}%` for male heads), reinforcing the urgency of flexible utility payment mechanisms.

---

### Strategic Policy Recommendations

To achieve the SDG 7 access targets and maximize socioeconomic returns, national policy and development financing should focus on six core priorities. First, power utilities must prioritize distribution network quality and voltage surge protection to eliminate appliance damage (`{{PCT_VOLTAGE_DAMAGE}}%` of grid consumers) and address evening supply shortfalls (`{{PCT_EVE_SHORTAGE}}%`), which is also an indispensable technical prerequisite for future electric cooking adoption. Second, last-mile grid densification represents the fastest, lowest-cost pathway to expand access; programs should scale on-bill connection installment facilities spread over 12 to 24 months alongside standardized pre-wired 'ready boards' to overcome internal house wiring barriers. Third, for remote populations beyond network reach, off-grid strategies must transition from basic solar lanterns toward quality-certified multi-light Solar Home Systems and climate-resilient mini-grids, supported by PAYGo and RBF financing.

Fourth, utility regulatory frameworks must sustain progressive volumetric lifeline tariffs and flexible digital prepaid metering to prevent post-connection payment distress. Fifth, clean cooking strategy requires a dual-track transition: accelerating the commercial distribution of Improved Cookstoves (ICS) in biomass-dependent rural areas, expanding urban LPG cylinder retail networks, and conducting targeted e-cooking pilots in high-reliability grid zones, accompanied by public education on the health hazards of stove stacking. Finally, gender equity must be mainstreamed by deploying tailored on-bill financing to overcome the `{{CREDIT_ACCESS_FHH}}%` female credit barrier and investing in clean cooking to eliminate female fuel-gathering drudgery.

---

## CHAPTER 1: MEASURING ENERGY ACCESS IN {{COUNTRY_NAME}}

### 1.1 Country Context and Energy Sector Architecture

Modern energy services underpin macroeconomic resilience, agricultural productivity, educational outcomes, public healthcare delivery, and gender equality. In {{COUNTRY_NAME}}, expanding access to reliable and affordable power has been placed at the center of the national development agenda. However, power sector expansion takes place within a challenging physical and macroeconomic environment characterized by geographic dispersal, capital investment deficits, transmission bottlenecks, and currency volatility.

> [!NOTE]
> **COUNTRY COORDINATOR ACTION REQUIRED:** Review and adapt country-specific macroeconomic figures, institutional mandates (Ministry, Regulator, Utility), generation mix, and historical survey benchmarks before publication.

The governance of {{COUNTRY_NAME}}'s energy sector involves distinct institutional mandates across policy formulation, technical regulation, generation, transmission, and retail distribution. Sector policy is directed by the national Ministry responsible for energy, which establishes electrification roadmaps, renewable energy master plans, and national targets aligned with the United Nations Sustainable Development Goals. Technical and economic regulation is executed by the national energy regulatory authority, which oversees license issuance, tariff methodology determination, grid code enforcement, and service quality benchmarks.

Bulk power generation and high-voltage transmission are typically anchored by the national power utility. The generation asset base reflects the country's natural resource endowments, combining domestic hydropower resources, thermal heavy fuel oil or diesel plants, grid-connected solar photovoltaic installations, and cross-border regional power pool interconnectors. Retail distribution is managed either through centralized utility regional directorates, municipal electricity distributors, or public-private concessionaires operating licensed distribution service areas. In rural and peri-urban areas beyond the immediate reach of the transmission grid, dedicated rural electrification agencies coordinate decentralized mini-grids and off-grid solar initiatives.

Expanding energy access requires addressing the financial equilibrium of the power sector. Retail electricity tariffs must balance cost-reflectivity for utility financial viability against affordability for vulnerable and low-income consumer segments. Lifeline tariff blocks are commonly deployed to protect low-consumption residential consumers, while commercial and industrial tariffs provide cross-subsidies. High technical and commercial line losses, illegal connections, unmetered consumption, and bill collection challenges often constrain distribution utilities from financing last-mile service drops. Consequently, comprehensive diagnostic surveys such as the Multi-Tier Framework are vital to illuminate household demand elasticities, payment modalities, and service bottlenecks.

---

### 1.2 The Multi-Tier Framework (MTF) Global Methodology

The **Multi-Tier Framework (MTF)**, developed by ESMAP and the World Bank, conceptualizes energy access not as a binary condition (connected versus unconnected), but as a multi-dimensional continuum of service ranging from **Tier 0 (no access or sub-basic service)** to **Tier 5 (continuous, high-capacity, reliable, and safe modern energy)**.

#### The Seven Attributes of Electricity Access
Under MTF methodology, household electricity access is evaluated across **seven technical attributes**. A household's aggregate electricity tier is determined by applying the **Minimum-Attribute Rule**, which establishes that the overall tier is equal to the lowest tier attained across any of the seven individual dimensions:

$$\text{Aggregate Electricity Tier} = \min\Big(\text{Capacity}, \text{Availability}, \text{Reliability}, \text{Quality}, \text{Affordability}, \text{Formality}, \text{Safety}\Big)$$

1. **Capacity:** Evaluates the power output (in watts) of the household's electricity supply or the operational load of appliances that can be used simultaneously. Capacity thresholds range from Tier 0 (<3W) and Tier 1 (3–49W, task lighting and phone charging) up to Tier 4 (800–1,999W, heavy thermal appliances) and Tier 5 ($\ge$ 2,000W, air conditioning and electric cooking).
2. **Availability:** Measures the continuous duration of electricity supply delivered over a 24-hour cycle, with explicit evaluation of availability during the four peak evening hours (18:00 to 22:00) when lighting, domestic activities, and appliance usage are highest. Tier 1 requires at least 4 hours per day (including 1 evening hour), while Tier 5 mandates at least 23 hours per day (including all 4 evening hours).
3. **Reliability:** Evaluates the frequency and predictability of unscheduled power disruptions experienced by grid-connected households. Tiers 4 and 5 impose strict caps on weekly interruptions, requiring no more than 14 outages per week for Tier 4 and no more than 3 outages per week for Tier 5.
4. **Quality:** Assesses whether voltage fluctuations, frequency swings, and power surges occur with sufficient severity to damage consumer electronic appliances. Tiers 4 and 5 require the complete absence of voltage-induced appliance damage.
5. **Affordability:** Determines whether a basic standard electricity consumption package (defined as 365 kWh per year, or 1 kWh per day / 30.4 kWh per month) can be purchased without exceeding 5% of total household consumption expenditure.
6. **Formality:** Assesses the contractual and legal status of the connection, distinguishing between formal connections with registered utility meters (postpaid or prepaid) and informal, shared, or unregulated third-party hookups.
7. **Health and Safety:** Verifies the physical safety of household electrical installations, requiring the absence of electrical shocks, serious burn injuries, or electrical fire incidents during the preceding 12 months.

---

### Box 1: Minimum Requirements by Tier of Electricity Access

* **Tier 0 (No Access / Sub-Tier 1):** Electricity is unavailable or available for less than 4 hours per day (or less than 1 hour during evening peak hours), or system capacity is <3W. Households rely on candles, disposable dry-cell batteries, kerosene lamps, and open flames for lighting.
* **Tier 1 (Task Lighting & Phone Charging):** Peak capacity $\ge$ 3W; supply available $\ge$ 4 hours per day, including $\ge$ 1 hour during evening peak hours. Capable of powering task lighting and mobile phone charging (e.g., solar lanterns, basic solar lighting kits).
* **Tier 2 (General Lighting, Television, & Fan):** Peak capacity $\ge$ 50W; supply available $\ge$ 4 hours per day, including $\ge$ 2 hours during evening peak hours. Capable of operating multiple light points, television, and an electric fan (e.g., multi-light Solar Home Systems, entry-level mini-grids).
* **Tier 3 (Medium Load & Refrigeration):** Peak capacity $\ge$ 200W; supply available $\ge$ 8 hours per day, including $\ge$ 3 hours during evening peak hours. Enables domestic refrigeration, food processing, water pumping, and light productive applications. Standard 365 kWh annual consumption must meet the 5% affordability test.
* **Tier 4 (High Load & Productive Use):** Peak capacity $\ge$ 800W; supply available $\ge$ 16 hours per day, including all 4 evening peak hours. Capable of powering heavy thermal appliances (washing machines, electric irons, microwaves) with low weekly outage frequencies ($\le$ 14 disruptions/week), formal utility billing, and no appliance-damaging voltage swings.
* **Tier 5 (Continuous Full Modern Access):** Peak capacity $\ge$ 2,000W; supply available $\ge$ 23 hours per day, including all 4 evening peak hours. Capable of powering continuous commercial-grade loads, central air conditioning, space heating, and electric cooking with high reliability ($\le$ 3 disruptions/week), formal metering, and verified installation safety.

---

### Box 2: Typology of Off-Grid Solar Devices

Off-grid solar devices are classified by capacity, service level, and appliance load:
* **Solar Lanterns (SL):** Small portable single-light point devices (<3W to 10W) comprising an integrated photovoltaic panel, rechargeable lithium or nickel battery, and an LED lamp. Many units incorporate a 5V USB output for mobile phone charging. While delivering essential lighting that displaces kerosene and candles, solar lanterns provide service strictly within Tier 0 or Tier 1.
* **Solar Lighting Systems (SLS):** Packaged multi-point DC systems (10W to 49W) with a separate rooftop solar module, central battery control unit, and wiring for 2 to 4 fixed LED room bulbs, mobile charging, and occasionally a small radio. SLS units provide standardized Tier 1 service across the entire dwelling.
* **Solar Home Systems (SHS):** Component-based or plug-and-play DC systems ranging from 50W to several hundred watts. SHS installations incorporate high-capacity lithium ferro-phosphate (LiFePO4) or deep-cycle lead-acid battery banks capable of powering high-efficiency DC televisions, DC fans, and multiple interior light points (Tier 2). Larger SHS units equipped with AC inverters (300W–1,000W+) can support Tier 3 services, including DC refrigeration, agricultural water pumping, and small enterprise productive machinery.

---

### Box 3: Typology of Cookstoves in {{COUNTRY_NAME}}

<!-- AUTO-GENERATED: The following table is populated from cookstove_calibration.csv at report generation time.
     COORDINATOR ACTION REQUIRED: Confirm stove typology and ISO emission tier assignments with a cookstove expert
     before running the pipeline. Edit cookstove_calibration.csv in the Tools/ directory. -->

{{COOKSTOVE_TYPOLOGY_TABLE}}

---

### 1.3 Survey Implementation, Sample Design, and Weighting

The {{SURVEY_YEAR}} MTF Household Survey in {{COUNTRY_NAME}} was executed using a stratified two-stage cluster sampling design engineered to produce statistically robust, nationally representative estimates as well as disaggregated indicators across urban and rural domains. The primary sampling frame was derived from the most recent National Population and Housing Census administered by the National Statistics Agency (INE).

In the first sampling stage, Primary Sampling Units (PSUs)—defined as census Enumeration Areas (EAs)—were selected with Probability Proportional to Size (PPS), where size was measured by the number of residential households recorded in the census frame. Sampling was independently stratified across `{{STRATA_COUNT}}` strata, formed by crossing all `{{ADMIN1_COUNT}}` administrative `{{ADMIN1_UNIT_LABEL_PLURAL}}` with geographic locality (urban vs. rural).

In the second sampling stage, a comprehensive household listing exercise was carried out in each selected EA immediately prior to data collection. A systematic random sample of households was drawn from the updated listing register. Household questionnaires were administered face-to-face by trained field enumerators using Computer-Assisted Personal Interviewing (CAPI) tablets programmed with real-time logical validation checks and spatial georeferencing.

To ensure that survey statistics accurately reflect national population parameters, calibrated sampling weights (`hh_wt`) were calculated. The base design weight for each sampled household is the inverse of its overall inclusion probability, computed as the product of the first-stage EA selection probability and the second-stage household selection probability:

$$w_{ij} = \frac{1}{P_{1i} \times P_{2ij}}$$

Sampling weights were subsequently adjusted for non-response at the EA level and calibrated against census population projections across administrative divisions. All econometric tabulations, tier allocations, and econometric models reported in this study apply these calibrated sampling weights.

---

## CHAPTER 2: ACCESS TO ELECTRICITY DIAGNOSTIC

### 2.1 Household Electrification by Technology and Locality

In {{COUNTRY_NAME}}, national grid infrastructure reaches `{{GRID_ACC_NAT}}%` of households nationwide (`{{GRID_ACC_URB}}%` in urban areas vs. `{{GRID_ACC_RUR}}%` in rural areas), while decentralized off-grid solar solutions (comprising Solar Home Systems and solar lighting kits) serve `{{SOLAR_ACC_NAT}}%` of households (`{{SOLAR_ACC_URB}}%` in urban areas vs. `{{SOLAR_ACC_RUR}}%` in rural communities). Isolated mini-grids and standalone fossil-fuel generators provide localized supply to the remaining electrified households.

Under the multi-dimensional Multi-Tier Framework (MTF) diagnostic, `{{ELEC_ACC_NAT}}%` of households achieve electricity access at Tier 1 or above (`{{ELEC_ACC_URB}}%` in urban centers vs. `{{ELEC_ACC_RUR}}%` in rural areas), leaving `{{ELEC_T0_NAT}}%` in Tier 0 (complete absence of modern electrical service). High-tier electricity access (Tier 4 or Tier 5)—capable of sustaining productive appliance loads and continuous commercial activity—is attained by `{{ELEC_T45_NAT}}%` of households nationally, reflecting a pronounced spatial divide between urban (`{{ELEC_T45_URB}}%`) and rural (`{{ELEC_T45_RUR}}%`) populations.

Figure 1 illustrates the distribution of households across Multi-Tier Framework electricity access tiers (Tier 0 to Tier 5) for national, urban, and rural populations.

![Figure 1: Multi-Tier Framework Electricity Access Tier Distribution Across National, Urban, and Rural Populations]({{CHART_ELEC_TIERS}})
*Figure 1: Distribution of households across Multi-Tier Framework electricity access tiers (Tier 0 to Tier 5) nationwide, in urban areas, and in rural areas.*

The national electrification profile reflects a diverse multi-source technological landscape. Under international monitoring guidelines established for SDG 7.1.1 and the Multi-Tier Framework, formal electricity access is defined across six qualifying modern technologies:
1. National central grid connections
2. Isolated mini-grids and micro-grids (solar, hydro, or hybrid diesel)
3. Standalone fossil-fuel generators (diesel or gasoline)
4. Solar Home Systems (SHS) and Solar Lighting Systems (SLS)
5. Rechargeable battery systems charged at external commercial charging stations
6. Standalone solar lanterns with task lighting and phone charging capabilities

Figure 2 delineates the primary electricity technology source mix across qualifying modern sources, explicitly contrasting modern solutions against excluded disposable battery devices.*

![Figure 2: Household Electricity Source Mix and Exclusion of Dry-Cell Torches Under SDG 7.1.1]({{CHART_SOURCE_MIX}})
*Figure 2: Electrification source breakdown across the six qualifying modern technologies and the exclusion of dry-cell battery lighting.*

*\*Note: Under international SDG 7.1.1 monitoring standards, disposable dry-cell battery torches, handheld flashlights, and single-use batteries are strictly excluded from electricity access metrics because they provide basic task illumination without appliance-powering capacity, carry high recurrent unit costs, and lack the attributes of modern electrical service.*

Among households utilizing decentralized off-grid solar energy, service capability varies substantially across device categories: (1) standalone solar lanterns, (2) multi-light Solar Lighting Systems (SLS), and (3) larger Solar Home Systems (SHS) equipped for domestic appliances. Figure 2B details the off-grid solar device typology across national, urban, and rural solar adopters.

![Figure 2B: Off-Grid Solar Device Typology Across National, Urban, and Rural Populations]({{CHART_SOLAR_TYPOLOGY}})
*Figure 2B: Distribution of primary off-grid solar devices (Solar Lanterns vs. Solar Lighting Systems vs. Solar Home Systems) among solar-adopter households.*

Table 2.1 presents the detailed distribution of households across electricity access tiers alongside typical appliance capabilities.

---

### Table 2.1: Electricity Tier Distribution Across National, Urban, and Rural Populations

| Electricity Access Tier | Nationwide (%) | Urban (%) | Rural (%) | Typical Appliance Service & Capabilities |
| :--- | :---: | :---: | :---: | :--- |
| **Tier 0** (No Access / Sub-Tier 1) | `{{ELEC_T0_N}}` | `{{ELEC_T0_U}}` | `{{ELEC_T0_R}}` | Dry-cell batteries, candles, flashlights, paraffin |
| **Tier 1** (Task Lighting & Phone Charging) | `{{ELEC_T1_N}}` | `{{ELEC_T1_U}}` | `{{ELEC_T1_R}}` | Basic Solar Lighting Systems (SLS, 3-49W, >=4h) |
| **Tier 2** (General Lighting, TV, Fan) | `{{ELEC_T2_N}}` | `{{ELEC_T2_U}}` | `{{ELEC_T2_R}}` | Multi-light SHS (50-199W, >=4h) |
| **Tier 3** (Medium Load & Refrigeration) | `{{ELEC_T3_N}}` | `{{ELEC_T3_U}}` | `{{ELEC_T3_R}}` | Refrigerator, freezer, water pump, grid (>=8h) |
| **Tier 4** (High Load & Productive Use) | `{{ELEC_T4_N}}` | `{{ELEC_T4_U}}` | `{{ELEC_T4_R}}` | Washing machine, electric iron, grid (>=16h) |
| **Tier 5** (Continuous Full Access) | `{{ELEC_T5_N}}` | `{{ELEC_T5_U}}` | `{{ELEC_T5_R}}` | Air conditioning, electric cooking, grid (>=23h) |
| **Tier 1+** | `{{ELEC_ACC_NAT}}` | `{{ELEC_ACC_URB}}` | `{{ELEC_ACC_RUR}}` | Universal electrification monitoring threshold |

---

### 2.2 Socioeconomic Equity and the Consumption Quintile Gradient

Electricity access in {{COUNTRY_NAME}} is strongly correlated with household consumption expenditure. Across expenditure quintiles, electrification rates expand steadily from `{{Q1_ELEC_ACC}}%` in the poorest quintile (Q1) to `{{Q2_ELEC_ACC}}%` in Q2, `{{Q3_ELEC_ACC}}%` in Q3, `{{Q4_ELEC_ACC}}%` in Q4, and `{{Q5_ELEC_ACC}}%` in the richest quintile (Q5). In the lowest quintile, the vast majority of households remain unserved, as high initial grid connection fees and internal house wiring costs present an insurmountable barrier to adoption. Conversely, in the richest quintile, higher disposable income and concentration in formal urban settlements enable extensive grid uptake.

This unequal access across income groups creates an **energy poverty penalty**. Low-income households residing in unserved settlements frequently spend a larger fraction of their monthly budget purchasing inferior lighting substitutes (such as candles, kerosene, and disposable dry-cell batteries) per unit of effective lumen-hour than grid-connected households spend on metered utility electricity. Expanding access to affordable off-grid solar kits and subsidized grid connections relieves this cash drain, freeing resources for nutrition, education, and healthcare.

##### Table 2.2: Energy Poverty Penalty — Monthly Coping Mechanism Lighting Expenditures Across Quintiles & Access Status

| Household Segment / Expenditure Quintile | Monthly Coping Fuel Spending (`{{CURRENCY_CODE}}`) | Share of Monthly Household Budget (%) |
| :--- | :---: | :---: |
| **Lowest Quintile (Q1) — Unelectrified** | `{{COPING_SPEND_Q1_UNEL}}` | `{{COPING_PCT_Q1_UNEL}}%` |
| **Lowest Quintile (Q1) — Grid Connected** | `{{COPING_SPEND_Q1_CONN}}` | `{{COPING_PCT_Q1_CONN}}%` |
| **Middle Quintile (Q3) — Unelectrified** | `{{COPING_SPEND_Q3_UNEL}}` | `{{COPING_PCT_Q3_UNEL}}%` |
| **Middle Quintile (Q3) — Grid Connected** | `{{COPING_SPEND_Q3_CONN}}` | `{{COPING_PCT_Q3_CONN}}%` |
| **Highest Quintile (Q5) — Unelectrified** | `{{COPING_SPEND_Q5_UNEL}}` | `{{COPING_PCT_Q5_UNEL}}%` |
| **Highest Quintile (Q5) — Grid Connected** | `{{COPING_SPEND_Q5_CONN}}` | `{{COPING_PCT_Q5_CONN}}%` |
| **National Average (All Unelectrified)** | `{{COPING_SPEND_NAT_UNEL}}` | `{{COPING_PCT_NAT_UNEL}}%` |
| **National Average (All Grid Connected)** | `{{COPING_SPEND_NAT_CONN}}` | `{{COPING_PCT_NAT_CONN}}%` |

*Note: Table 2.2 empirically illustrates the energy poverty penalty. Coping expenditures capture monthly purchases of non-electric lighting and power substitutes (dry-cell batteries, candles, kerosene, and fee-based mobile phone charging) expressed as a percentage of total household consumption expenditure.*

As documented in Table 2.2, unelectrified households in the lowest expenditure quintile spend `{{COPING_PCT_Q1_UNEL}}%` of their total monthly budget solely on coping lighting mechanisms. By contrast, grid-connected households in the same quintile spend just `{{COPING_PCT_Q1_CONN}}%` of their budget on electricity, illustrating that lack of electricity access forces the poor to pay an exorbitant premium for basic task lighting.

Figure 3 displays the progression of electricity and modern energy cooking access rates across consumption expenditure quintiles (Q1 to Q5).

![Figure 3: Household Electricity and Modern Energy Cooking Access Across National Consumption Expenditure Quintiles (Q1 to Q5)]({{CHART_QUINTILE_CURVE}})
*Figure 3: Progression of electricity and modern energy cooking access rates across consumption expenditure quintiles (Q1 to Q5).*

---

### 2.3 Evaluation of Electricity Access by Attribute

In the Multi-Tier Framework, access to electricity is measured by assessing service quality across seven multi-dimensional attributes. Each attribute is categorized from Tier 0 to Tier 5, with the aggregate tier determined by the lowest tier attained among the attributes.

#### 1. Capacity (Power Output and Appliance Operation)
The Capacity attribute evaluates whether the electricity supply provides sufficient power to operate appliances desired by households. Grid-connected households are technically provided with high capacity (>2 kW, Tier 5). However, appliance ownership varies widely:
* **Very Low-Load Appliances (Tier 1):** `{{IS_VERYLOW_NAT}}%` of households nationwide (`{{IS_VERYLOW_URB}}%` urban vs. `{{IS_VERYLOW_RUR}}%` rural) own Tier 1 appliances, such as mobile phone chargers (`{{HAS_CHARGER_NAT}}%`), radios (`{{HAS_RADIO_NAT}}%`), and electric lighting points (`{{HAS_LIGHTS_NAT}}%`, comprising incandescent, fluorescent tube, CFL, or LED light bulbs).
* **Low-Load Appliances (Tier 2):** `{{IS_LOW_NAT}}%` own Tier 2 appliances, dominated by flat-screen color televisions (`{{HAS_TV_NAT}}%`) and electric fans (`{{HAS_FAN_NAT}}%`).
* **Medium-Load Appliances (Tier 3):** `{{IS_MED_NAT}}%` own Tier 3 appliances, led by domestic refrigerators and freezers (`{{HAS_FRIDGE_NAT}}%`).
* **High & Very High-Load Appliances (Tiers 4–5):** `{{IS_HIGH_NAT}}%` own Tier 4 appliances (electric irons: `{{HAS_IRON_NAT}}%`; microwaves: `{{HAS_MICRO_NAT}}%`), while Tier 5 thermal appliances (air conditioners: `{{HAS_AC_NAT}}%`; water heaters: `{{HAS_GEYSER_NAT}}%`) are owned by only `{{IS_VERYHIGH_NAT}}%` nationwide (`{{IS_VERYHIGH_URB}}%` urban vs. `{{IS_VERYHIGH_RUR}}%` rural).

Overall lighting point ownership stands at `{{HAS_ELECTRIC_LIGHTS_NAT}}%` for electric bulbs, expanding to `{{HAS_ANY_LIGHTS_NAT}}%` when standalone solar lighting is included.

#### 2. Availability (Daily Duration and Evening Supply)
The Availability attribute captures electricity availability during the whole 24-hour day and specifically during the 4 peak evening hours (18:00 to 22:00) when household electricity demand is highest. While grid connections generally provide continuous daily service, evening supply deficits remain an operational issue: `{{PCT_EVE_SHORTAGE}}%` of grid-connected households experience less than 4 hours of supply during peak evening hours, restricting study time for school children and limiting evening productive activities.

#### 3. Reliability (Unscheduled Power Outages)
Under MTF methodology, reliability evaluates the frequency of unscheduled power disruptions. Analysis of weekly outage intervals reveals that `{{OUTAGES_LT3_WK}}%` of grid-connected households experience fewer than 3 interruptions per week, fully satisfying the Tier 5 reliability benchmark ($\le$ 3 disruptions/week). An additional `{{OUTAGES_3TO14_WK}}%` experience 3 to 14 interruptions per week (Tier 4 standard), while `{{OUTAGES_GT14_WK}}%` experience more than 14 outages per week (average weekly disruptions: `{{AVG_OUTAGES_PER_WEEK}}`). Consequently, physical outage frequency is not the binding constraint preventing households from reaching Tier 5.

#### 4. Quality (Voltage Stability and Appliance Damage)
The Quality attribute evaluates whether voltage fluctuations or surges occur with sufficient severity to damage electrical appliances. In general, household electronics and motor-driven appliances require stable voltage to operate safely. Voltage instability represents a critical bottleneck: `{{PCT_VOLTAGE_DAMAGE}}%` of grid-connected households report that voltage fluctuations and power surges have caused permanent damage to their appliances (such as televisions, refrigerators, and sound systems).

#### 5. Affordability (Cost of Basic Electricity Consumption)
The Affordability attribute evaluates whether a standard electricity consumption package (defined under MTF guidelines as 365 kWh per year, or 30.4 kWh per month / 1 kWh per day) can be purchased without exceeding 5% of total household consumption expenditure. Nationwide, `{{PCT_AFFORDABLE_NAT}}%` of households satisfy the 5% affordability threshold (`{{PCT_AFFORDABLE_URB}}%` in urban areas and `{{PCT_AFFORDABLE_RUR}}%` in rural areas), indicating that recurrent monthly tariffs under existing lifeline blocks are affordable for the vast majority of connected consumers. Average monthly spending on metered grid electricity is recorded at `{{GRID_MONTHLY_SPEND_NAT}}` `{{CURRENCY_CODE}}` nationally (`{{GRID_MONTHLY_SPEND_URB}}` `{{CURRENCY_CODE}}` urban vs. `{{GRID_MONTHLY_SPEND_RUR}}` `{{CURRENCY_CODE}}` rural), with a national median expenditure of approximately 8,000 `{{CURRENCY_CODE}}`. Over 92% of connected households utilize prepaid meters—recharging in smaller, flexible increments averaging ~6,500 `{{CURRENCY_CODE}}` per purchase—while high-consuming upper-bracket urban households with refrigeration and cooling equipment pull up the national arithmetic mean.

#### 6. Formality and Legality
The Formality attribute assesses the legal and contractual status of the electricity connection. In {{COUNTRY_NAME}}, the vast majority of grid-connected households possess formal utility connections with registered postpaid or prepaid meters, ensuring transparent billing and formal consumer protections.

#### 7. Health and Safety
The Health and Safety attribute assesses whether households have experienced serious electrical accidents, electrocutions, or fire incidents resulting from the connection during the past 12 months. Across {{COUNTRY_NAME}}, serious electrical safety incidents are reported in fewer than 1% of households in the past year, reflecting general adherence to basic wiring conventions.

---

### 2.4 Household Grid Electricity Consumption, Expenditure, and Appliance Ownership

Beyond physical connection, understanding the level of electricity consumption, payment modalities, and the appliance ownership portfolio of connected households is essential for evaluating service adequacy, demand patterns, and utility revenue sustainability. In {{COUNTRY_NAME}}, grid-connected households face substantial quality and reliability constraints, yet grid electricity represents the primary modern energy anchor for domestic welfare and economic productivity.

#### Monthly Grid Electricity Expenditures: Cash-Flow Dynamics & Dual Estimation

Household electricity spending can be evaluated through two distinct empirical lenses: (1) direct recall of typical monthly spending (`SEC_C_Q25`), and (2) high-frequency transaction reconstruction based on prepaid recharge frequency and purchase amounts (`SEC_C_Q19B` & `SEC_C_Q19D`).

In {{COUNTRY_NAME}}, over 92% of connected households utilize digital prepaid metering (STS prepaid tokens), purchasing electricity periodically in cash or via mobile money. Evaluating transaction records reveals critical insights into household cash-flow management:
- **Prepaid Micro-Purchases & Transaction Medians:** Among the core cohort of prepaid customers who purchase electricity on a monthly schedule (representing 55.4% of prepaid users), the **median recharge transaction is 5,000 `{{CURRENCY_CODE}}` (~$8.33 USD)**, with a transaction mean of **7,491 `{{CURRENCY_CODE}}` (~$12.50 USD)**. Over a quarter of these households purchase tokens of 4,000 `{{CURRENCY_CODE}}` (~$6.67 USD) or less. By purchasing in smaller, flexible increments, households align energy expenditures with irregular informal income streams, avoiding the punitive reconnection fees and lump-sum billing distress common under traditional postpaid billing.
- **Direct Typical Monthly Recall:** When asked directly regarding typical monthly electricity expenditures, grid-connected households report an overall national mean of `{{GRID_MONTHLY_SPEND_NAT}}` `{{CURRENCY_CODE}}` per month (~$18.40 USD). In urban centers, monthly electricity expenditure averages `{{GRID_MONTHLY_SPEND_URB}}` `{{CURRENCY_CODE}}`, compared to `{{GRID_MONTHLY_SPEND_RUR}}` `{{CURRENCY_CODE}}` in electrified rural communities.
- **Distributional Skewness:** The arithmetic mean of `{{GRID_MONTHLY_SPEND_NAT}}` `{{CURRENCY_CODE}}` is heavily pulled upward by high-consuming upper-bracket urban households in Quintile 5 (averaging 12,193 `{{CURRENCY_CODE}}` / ~$20.30 USD) who operate multiple continuous cooling and refrigeration appliances. In contrast, the **national median monthly expenditure is `{{GRID_MONTHLY_SPEND_MEDIAN}}` `{{CURRENCY_CODE}}` (~$13.30 USD)**, while households in the poorest expenditure quintile (Quintile 1) report a median monthly spending of only **4,000 `{{CURRENCY_CODE}}` (~$6.67 USD)**. Mechanical frequency multiplication (recharge amount $\times$ annual frequency) yields an inflated arithmetic mean (15,676 `{{CURRENCY_CODE}}`), driven primarily by enumerator-respondent ambiguity between "twice a month" versus "twice a week" options and occasional emergency daily purchases. Anchoring analysis in direct monthly recall alongside transaction medians provides an empirically grounded, transparent depiction of domestic energy burdens.

Table 2.3 presents monthly electricity expenditure disaggregated across household consumption expenditure quintiles.

##### Table 2.3: Monthly Grid Electricity Expenditure by Household Expenditure Quintile

| Expenditure Quintile | Mean Monthly Expenditure (`{{CURRENCY_CODE}}`) | Median Monthly Expenditure (`{{CURRENCY_CODE}}`) | Estimated Equivalent USD (Median) |
| :--- | :---: | :---: | :---: |
| **Quintile 1 (Poorest 20%)** | 5,681 | 4,000 | ~$6.67 |
| **Quintile 2** | 7,838 | 5,000 | ~$8.33 |
| **Quintile 3** | 9,062 | 10,000 | ~$16.67 |
| **Quintile 4** | 10,318 | 7,000 | ~$11.67 |
| **Quintile 5 (Richest 20%)** | 12,193 | 10,000 | ~$16.67 |
| **National Grid Connected Average** | `{{GRID_MONTHLY_SPEND_NAT}}` | `{{GRID_MONTHLY_SPEND_MEDIAN}}` | ~$13.33 |

#### Appliance Ownership Profile Across Quintiles & Econometric Literature Grounding

The welfare benefits and productive services delivered by electrification depend directly on household ownership of end-use appliances. In the energy economics literature, durable good adoption in developing countries is characterized by pronounced non-linearities:
1. **The S-Curve Appliance Accumulation Paradigm:** As formalized by **Wolfram, Shelef, and Gertler (2012)** (*American Economic Review Papers & Proceedings*), appliance adoption follows a characteristic S-shaped curve as household incomes rise. Basic lighting and low-power media goods (televisions, radios, mobile phone chargers) represent "entry-level" durables that saturate rapidly even at low income levels. In contrast, energy-intensive cooling, thermal, and motor-driven appliances (refrigerators, air conditioners, electric irons, washing machines) exhibit steep income threshold effects, remaining virtually absent until households reach upper-income tiers.
2. **Rising Middle Class and Energy Demand Surges:** **Gertler et al. (2016)** (*American Economic Review*) demonstrate that rising incomes translate into non-linear increases in residential electricity demand primarily through the accumulation of energy-using assets—particularly refrigeration and space cooling—rather than increased utilization of existing basic equipment.
3. **The Low Initial Demand Paradox in Sub-Saharan Africa:** As documented by **Lee, Miguel, and Wolfram (2020)** (*American Economic Review*), grid connections among newly electrified rural households in Sub-Saharan Africa initially generate modest consumption levels because connected families face severe liquidity constraints that prevent them from purchasing durable appliances beyond basic lighting and phone charging.
4. **Thermodynamic Baseloads:** **Davis (2008)** (*Journal of Political Economy*) highlights that refrigeration establishes an inflexible continuous thermodynamic baseload driven by ambient climatic conditions, which locks in a permanent floor of residential energy consumption once adopted.

Table 2.4 details the empirical appliance ownership profile among grid-connected households in {{COUNTRY_NAME}} across expenditure quintiles, reporting design-based survey-weighted Wald tests of statistical significance across the socioeconomic gradient.

##### Table 2.4: Household Appliance Ownership Rates Among Grid Customers by Expenditure Quintile (%)

| Appliance Category | Q1 (Poorest) | Q2 | Q3 | Q4 | Q5 (Richest) | Grid Customers Total | Statistical Significance (Wald Trend Test) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Electric Lighting (Consolidated: LED, CFL, Tube, Incandescent)** | 100.0% | 87.8% | 93.7% | 93.2% | 92.9% | 92.8% | $p = 0.933$ (Not Significant) |
| **Television (Consolidated: Flat screen, Color, B&W)** | 64.3% | 66.7% | 46.1% | 53.1% | 64.2% | 60.5% | $p = 0.168$ (Not Significant) |
| **Mobile Phone Charger (Smartphone & Basic)** | 91.4% | 53.2% | 37.2% | 46.7% | 56.9% | 53.5% | $p = 0.548$ (Not Significant) |
| **Radio / Sound System (Electric & Battery)** | 42.3% | 10.4% | 38.8% | 22.9% | 25.6% | 25.8% | $p = 0.866$ (Not Significant) |
| **Refrigerator / Freezer (Electric & Solar)** | 48.9% | 44.8% | 48.0% | 47.1% | 66.2% | 59.4% | $p = 0.013^{**}$ |
| **Electric Fan** | 27.0% | 26.8% | 35.0% | 29.6% | 67.4% | 54.2% | $p < 0.001^{***}$ |
| **Electric Iron** | 0.0% | 0.0% | 19.5% | 8.2% | 22.2% | 17.7% | $p < 0.001^{***}$ |
| **Computer / Laptop** | 0.0% | 4.5% | 10.4% | 9.2% | 21.4% | 16.7% | $p < 0.001^{***}$ |
| **Electric Water Heater** | 0.0% | 0.0% | 1.5% | 7.6% | 9.8% | 7.9% | $p = 0.012^{**}$ |
| **Microwave Oven** | 0.0% | 0.0% | 0.0% | 2.3% | 9.0% | 6.2% | $p < 0.001^{***}$ |
| **Blender / Food Processor** | 0.0% | 0.0% | 0.0% | 5.2% | 7.3% | 5.7% | $p < 0.001^{***}$ |
| **Internet Modem / Router** | 0.0% | 0.0% | 0.0% | 0.0% | 5.9% | 3.8% | $p = 0.001^{***}$ |
| **Air Conditioner (AC)** | 0.0% | 0.0% | 0.0% | 0.0% | 3.0% | 1.9% | $p = 0.001^{***}$ |

*Note: Table 2.4 reports weighted appliance ownership rates specifically among national grid-connected households. Asterisks denote statistical significance based on design-based survey-weighted Wald tests ($^{***} p < 0.01, ^{**} p < 0.05, ^{*} p < 0.1$) adjusting for PSU cluster correlation and sampling weights. Electric lighting consolidates incandescent, fluorescent tube, compact fluorescent (CFL), LED bulbs, and solar bulbs. Television consolidates CRT color, flat screen LCD/LED, black & white, and solar televisions.*

The empirical results in Table 2.4 provide striking empirical validation of the Wolfram et al. (2012) framework in {{COUNTRY_NAME}}:
- **Universal Saturation of Entry-Level Services:** Electric lighting (92.8% overall; 100.0% in Q1), televisions (60.5%), and mobile phone chargers (53.5%) display statistically insignificant socioeconomic gradients across quintiles ($p > 0.15$). Once hooked to the network, households across all wealth strata prioritize illumination and information services.
- **Steep S-Curve Adoption for Cooling and Thermal Durables:** In contrast, electric fans ($p < 0.0001^{***}$), electric irons ($p < 0.0001^{***}$), computers/laptops ($p < 0.0001^{***}$), microwaves ($p < 0.0001^{***}$), blenders ($p < 0.0004^{***}$), and air conditioners ($p < 0.0013^{***}$) exhibit highly significant socioeconomic gradients. In the bottom quintile (Q1), ownership of irons, PCs, microwaves, blenders, and air conditioners is literally 0.0%. Ownership emerges abruptly in Quintiles 4 and 5 as households cross the income threshold necessary to finance high-wattage durable investments.

#### Empirical Determinants of Electricity Expenditure: Econometric Model

To examine which socioeconomic and technological factors drive household electricity consumption, a Weighted Least Squares (WLS) econometric regression was estimated on monthly grid electricity spending:

$$\ln(\text{Grid Expenditure}_i) = \beta_0 + \beta_1 \text{Quintile}_i + \beta_2 \text{HHSize}_i + \sum_k \gamma_k \text{Appliance}_{ki} + \varepsilon_i$$

Empirical estimation yields several critical insights into household energy demand:
1. **Baseload Thermodynamic Refrigeration Load:** Holding household wealth and family size constant, owning a refrigerator or freezer is the single strongest appliance determinant of electricity expenditure ($\beta = +0.1901, t = 2.68^{***}, p < 0.01$). Refrigerator ownership increases monthly electricity expenditure by **+20.9%** (an absolute increase of **+2,250.3 `{{CURRENCY_CODE}}`/month**). In {{COUNTRY_NAME}}'s high ambient temperature climate, compressors run continuously to maintain food preservation, representing a rigid baseload energy demand as predicted by Davis (2008).
2. **Media and Information Services:** Television ownership exerts a statistically significant positive effect on electricity spending ($\beta = +0.1471, t = 2.16^{**}, p < 0.05$), increasing monthly spending by **+15.8% (+784.4 `{{CURRENCY_CODE}}`/month)**.
3. **Income and Wealth Elasticity:** Household consumption expenditure quintile is strongly correlated with electricity spending ($\beta = +0.0981, t = 2.28^{**}, p < 0.05$), with each step increase in quintile raising monthly grid spending by **+10.3% (+1,145.5 `{{CURRENCY_CODE}}`/month)**. This captures both the accumulation of secondary appliances and longer daily utilization hours among wealthier households (Gertler et al., 2016).
4. **Cooling and Thermal Loads:** Electric fans contribute an additional **+10.9% (+949.2 `{{CURRENCY_CODE}}`/month)** to monthly bills. Notably, high-power resistive and compressor appliances—such as electric irons (17.7% grid ownership), water heaters (7.9%), microwave ovens (6.2%), and air conditioners (1.9%)—are almost entirely absent from the bottom three quintiles and concentrate within the top quintile, creating steep peak-demand drivers for the national utility. Consistent with Dinkelman (2011), the diffusion of thermal and motor-driven home production durables (e.g., irons and food processors) represents a crucial frontier for liberating domestic labor time, but currently remains severely constrained by household capital barriers.

---

### 2.5 Improving access to electricity

#### The "Under-the-Grid" Densification Paradox
In {{COUNTRY_NAME}}, `{{UNDER_THE_GRID_NAT}}%` of households reside in electrified Enumeration Areas (EAs)—meaning low-voltage distribution transformers and lines already pass directly through their communities. However, only `{{GRID_UPTAKE_NAT}}%` of households living in these electrified EAs are connected to the grid (`{{GRID_UPTAKE_URB}}%` in urban areas and `{{GRID_UPTAKE_RUR}}%` in rural areas), leaving an unconnected deficit of `{{UNDER_GRID_UNCONNECTED_NAT}}%`.

Connecting an under-the-grid household requires only a service drop wire, an electric meter, and internal household wiring, bypassing the substantial capital expenditure required for high-voltage transmission lines, substations, and medium-voltage feeder extensions. Expanding grid uptake in electrified EAs from the baseline rate of `{{GRID_UPTAKE_NAT}}%` to **60.0%** would add **27.2 percentage points** to national electrification, connecting thousands of families at the lowest marginal cost per connection.

Figure 4 visualizes the national densification funnel: progressing from total households to residence in electrified EAs, connected households, and the unconnected deficit.

![Figure 4: The Under-the-Grid Uptake Funnel and National Densification Deficit]({{CHART_UNDER_GRID}})
*Figure 4: National densification funnel: Total households → Households in Electrified EAs → Connected Households vs Unconnected Deficit.*

#### Stated Barriers to Gaining Connection
Unconnected households report that upfront connection costs and physical distance to distribution infrastructure represent the predominant obstacles to electrification. Figure 5 presents the primary stated barriers to gaining an electricity connection across national, urban, and rural populations.

![Figure 5: Primary Stated Barriers to Gaining Grid Connection]({{CHART_GRID_BARRIERS}})
*Figure 5: Primary stated obstacles to gaining a grid connection across national, urban, and rural unconnected households.*

Nationally, `{{BARRIER_COST_NAT}}%` of unconnected households (`{{BARRIER_COST_URB}}%` in urban areas vs. `{{BARRIER_COST_RUR}}%` in rural areas) identify the upfront connection fee as their primary obstacle, while `{{BARRIER_DIST_NAT}}%` (`{{BARRIER_DIST_URB}}%` urban vs. `{{BARRIER_DIST_RUR}}%` rural) report that physical distance from existing network lines is prohibitive. Because connection charges typically scale with the distance and infrastructure extensions required to hook up a dwelling, these two factors represent interrelated manifestations of the high initial capital hurdle. In contrast, high monthly electricity tariffs are cited by `{{BARRIER_TARIFF_NAT}}%` of unconnected households, indicating that recurrent payment affordability—while secondary to the upfront connection hurdle—remains an active concern. Even after overcoming upfront connection barriers, households face ongoing monthly electricity expenditures averaging `{{GRID_MONTHLY_SPEND_NAT}}` `{{CURRENCY_CODE}}` nationwide (`{{GRID_MONTHLY_SPEND_URB}}` `{{CURRENCY_CODE}}` in urban areas vs. `{{GRID_MONTHLY_SPEND_RUR}}` `{{CURRENCY_CODE}}` in rural areas; median ~8,000 `{{CURRENCY_CODE}}`). Beyond financial costs, institutional and tenure constraints also impede access: `{{BARRIER_LANDLORD_NAT}}%` of unconnected urban households report that landlords refuse to finance or authorize connection installations, while bureaucratic delays (`{{BARRIER_ADMIN_NAT}}%`) and service unreliability (`{{BARRIER_UNREL_NAT}}%`) affect remaining households.

#### Willingness to Pay Dynamics and Financing Elasticity
Understanding household connection demand requires examining how stated adoption responds to price reductions and financing terms. In liquidity-constrained settings, acute credit constraints prevent households from paying lump-sum connection charges, creating a substantial gap between upfront demand and financed demand.

The MTF contingent valuation bidding experiment in {{COUNTRY_NAME}} rigorously reflects these dynamics:
* **Upfront Payment:** Only `{{WTP_GRID_UPFRONT_NAT}}%` of unconnected households can pay the connection fee upfront in cash (`{{WTP_GRID_UPFRONT_URB}}%` in urban areas and `{{WTP_GRID_UPFRONT_RUR}}%` in rural areas).
* **Installment Financing Expansion:** Stated willingness expands to `{{WTP_GRID_3M_NAT}}%` over 3 months, `{{WTP_GRID_6M_NAT}}%` over 6 months, and surges to `{{WTP_GRID_12M_NAT}}%` under a **12-month installment plan**.
* **Fee Waivers and Internal Wiring Barriers:** When the connection fee is completely waived, `{{WTP_GRID_WAIVED_NAT}}%` indicate willingness to connect. Among households declining connection even under fee waivers (`{{WTP_GRID_NON_CONNECT}}%`), `{{REFUSE_WIRING_COST_NAT}}%` cite internal household wiring costs as the primary reason.

Figure 6 plots the comparative cumulative willingness-to-pay demand curves for national grid connection across installment financing terms and capital fee subsidy tiers.

![Figure 6: Willingness to Pay Cumulative Demand Curves for National Grid Connection]({{CHART_WTP_GRID}})
*Figure 6: Comparative cumulative willingness-to-pay demand curves for grid connection across payment modalities and installment financing horizons.*

#### Off-Grid Solar Market Dynamics & Island Electrification
For households residing in remote settlements located beyond the physical reach of the national distribution network, decentralized off-grid solar solutions represent the primary electrification pathway. Empirical device ownership reveals a diverse off-grid market: while single solar lanterns represent 43.2% of primary devices among solar adopters, multi-light Solar Lighting Systems (SLS) account for 47.6% (reaching 51.7% in rural areas), and larger Solar Home Systems (SHS) represent 9.2%. Expanding service depth to support domestic entertainment, refrigeration, and productive appliances requires stimulating adoption of higher-capacity certified Solar Home Systems (SHS).

Household demand for off-grid Solar Home Systems is highly sensitive to both upfront equipment pricing and installment credit flexibility, as visualized in the cumulative willingness-to-pay demand curves in Figure 7. While upfront cash purchases are constrained by household liquidity, offering installment credit horizons of 6 to 24 months dramatically expands adoption across all subsidy levels (33%, 66%, and 100% price benchmarks). Even under a 24-month financing facility, approximately `{{WTP_SOLAR_NEVER_NAT}}%` of households decline the offer; among households declining, `{{REFUSE_SOLAR_COST_NAT}}%` cite equipment purchase costs and inability to meet monthly installment commitments as the decisive obstacle, while others report having sufficient alternative energy solutions. Consequently, bridging the final off-grid access gap requires coupling PAYGo mobile-money installments with targeted capital end-user subsidies and consumer awareness campaigns regarding certified equipment performance standards.

![Figure 7: Willingness to Pay Cumulative Demand Curves for Off-Grid Solar Devices]({{CHART_WTP_SOLAR}})
*Figure 7: Comparative cumulative willingness-to-pay demand curves for off-grid solar kits across upfront price subsidies and installment financing terms.*

During power interruptions, grid-connected households rely on substitute lighting coping mechanisms, primarily disposable dry-cell battery torches (`{{GRID_BACKUP_TORCH_NAT}}%`), while `{{GRID_BACKUP_NONE_NAT}}%` have no alternative backup source. Special geographic planning is essential for isolated insular territories—most notably the Bijagós archipelago—where submarine cable grid interconnection is technically and economically unviable. Electrification in these communities remains below 1%, necessitating maritime logistics corridors, localized spare-parts depots, and climate-resilient solar-plus-storage mini-grids engineered to withstand saline maritime operating conditions.

---

## CHAPTER 3: ACCESS TO MODERN ENERGY COOKING SERVICES (MECS)

### 3.1 Cooking Practices, Technologies, and Fuel Profile

Beyond the choice of stove and fuel technologies, different contextual factors contribute to the household cooking experience, including human behavior (who cooks, what is cooked, and how often), housing conditions (kitchen location, ventilation, and living space arrangement), and household economic constraints. In {{COUNTRY_NAME}}, cooking practices exert profound impacts on public health, forest degradation, greenhouse gas emissions, and intra-household female labor allocation.

Cooking energy in {{COUNTRY_NAME}} is characterized by an overwhelming reliance on solid biomass fuels. Solid fuels—principally gathered firewood and artisanal charcoal—serve over 95% of the population. In rural areas, gathered firewood is the nearly universal primary cooking fuel, whereas urban households rely heavily on purchased charcoal alongside firewood. Clean cooking fuels such as Liquefied Petroleum Gas (LPG) and grid electricity remain confined to a small fraction of affluent urban households (`{{CLEAN_STOVE_NAT}}%` nationally; `{{CLEAN_STOVE_URB}}%` urban vs. `{{CLEAN_STOVE_RUR}}%` rural).

Nationwide, `{{STOVE_3STONE_N}}%` of households cook primarily over a **three-stone open fire** (`{{STOVE_3STONE_U}}%` in urban areas and `{{STOVE_3STONE_R}}%` in rural areas). Traditional metal and artisanal charcoal stoves serve `{{STOVE_TRAD_N}}%` of households nationally (`{{STOVE_TRAD_U}}%` urban vs. `{{STOVE_TRAD_R}}%` rural). **Improved Cookstoves (ICS)** represent only `{{STOVE_ICS_N}}%` nationwide (`{{STOVE_ICS_U}}%` in urban areas and `{{STOVE_ICS_R}}%` in rural areas), indicating that the commercial market for high-efficiency biomass stoves remains nascent. Modern clean fuel stoves (LPG and electric) are used by only `{{CLEAN_STOVE_NAT}}%` of households (`{{CLEAN_STOVE_URB}}%` urban vs. `{{CLEAN_STOVE_RUR}}%` rural), with electric cooking accounting for `{{STOVE_ELEC_N}}%` nationwide.

Figure 8 illustrates the distribution of primary cookstove technologies and fuels across national, urban, and rural populations.

![Figure 8: Primary Cookstove Typology and Primary Fuel Distribution Across National, Urban, and Rural Populations]({{CHART_STOVE_FUELS}})
*Figure 8: Primary cookstove technologies (three-stone, traditional, ICS, clean) and primary fuels (wood, charcoal, LPG, electricity) across National, Urban, and Rural populations in {{COUNTRY_NAME}}.*

Table 3.1 details the distribution of primary cookstoves across localities alongside primary fuel types and ISO emission tiers.

---

### Table 3.1: Primary Cookstove Distribution Across National, Urban, and Rural Populations

<!-- AUTO-GENERATED: Rows below are populated from cookstove_calibration.csv.
     COORDINATOR ACTION REQUIRED: Review stove descriptions and ISO Emission Tier assignments
     with a cookstove expert before finalizing. Edit cookstove_calibration.csv in the Tools/ directory. -->

| Primary Cookstove Typology | Nationwide (%) | Urban (%) | Rural (%) | Primary Fuel Used | ISO Emission Tier |
| :--- | :---: | :---: | :---: | :--- | :---: |
{{COOKSTOVE_STATS_TABLE_ROWS}}

---

### 3.2 Evaluation of Cooking Access Using the Multi-Tier Framework

In the MTF assessment of access to clean cooking solutions, households are evaluated across six technical and contextual attributes: (i) exposure, (ii) efficiency, (iii) convenience, (iv) safety, (v) affordability, and (vi) fuel availability. The lowest tier score attained among the attributes determines a household's aggregate cooking tier:
* **Tiers 4 and 5 (Access to MECS):** Households reaching aggregate Tier 4 or 5 have access to Modern Energy Cooking Services (clean fuels including LPG, electricity, piped gas, and biogas).
* **Tiers 2 and 3 (Improved / In Transition):** Households reaching aggregate Tier 2 or 3 have improved cooking services, primarily through high-efficiency Improved Cookstoves (ICS).
* **Tiers 0 and 1 (No Access / High Exposure):** Households in aggregate Tier 0 or 1 have no access to clean cooking and remain exposed to severe indoor air pollution, burning raw biomass in unvented cooking environments.

Figure 9 displays the distribution of households across MECS cooking tiers nationwide, in urban areas, and in rural areas.

![Figure 9: Multi-Tier Framework Modern Energy Cooking Services (MECS) Tier Distribution]({{CHART_COOKING_TIERS}})
*Figure 9: Multi-Tier Framework Modern Energy Cooking Services (MECS) tier distribution across National, Urban, and Rural populations.*

As shown in Figure 9, the vast majority of households (`{{COOK_T01_NAT}}%` nationwide; `{{COOK_T01_URB}}%` urban and `{{COOK_T01_RUR}}%` rural) remain in **Tier 0 or Tier 1 (No Access)**. Full modern energy cooking services (Tiers 4–5) reach only `{{CLEAN_STOVE_NAT}}%` of households nationwide (`{{CLEAN_STOVE_URB}}%` in urban areas and `{{CLEAN_STOVE_RUR}}%` in rural areas).

#### Cookstove Time-Use Analysis by Technology
Household survey data reveal that cooking technology directly determines domestic time expenditure:
* **Three-Stone Open Fires:** Households relying on three-stone open fires spend an average of `{{HR_3STONE_NAT}}` hours per week cooking (equivalent to 156 minutes per day), driven by low heat concentration and unstable combustion.
* **Traditional Charcoal Stoves:** Traditional metal and artisanal ceramic braziers require an average of `{{HR_TRAD_NAT}}` hours per week (101 minutes per day).
* **Improved Cookstoves (ICS):** Enclosed combustion chambers in ICS units reduce cooking time to `{{HR_ICS_NAT}}` hours per week (97 minutes per day).
* **Modern LPG Stoves:** Pressurized gas burners dramatically cut cooking time to `{{HR_LPG_NAT}}` hours per week (72 minutes per day)—yielding a net time saving of **over 11 hours per week** compared to open fires.
* **Electric Stoves:** Electric cooking appliances average `{{HR_ELEC_NAT}}` hours per week among the small group of adopting households.

---

### 3.3 Cookstove Stacking and Biomass Reliance

Cookstove stacking—the concurrent use of multiple cookstoves and fuels—reflects a household's strategy to meet diverse domestic cooking needs, accommodate large cooking vessels, and hedge against fuel price volatility or stock-outs.

In {{COUNTRY_NAME}}, rather than transitioning entirely to a single modern appliance, households rely heavily on **multi-device biomass stacking**. Many households operate both an open three-stone fire for lengthy staple food preparation (such as boiling cassava, grains, and tubers) and a portable traditional charcoal burner for faster meal preparation and reheating. While ownership of clean cooking devices stands at `{{PCT_CLEAN_STOVE_OWNERSHIP}}%` nationally, `{{PCT_STOVE_STACKING}}` percentage points of households (representing over 80% of clean stove owners) continue to stack with traditional biomass stoves, resulting in `{{PCT_STACKING_DILUTION}}%` of clean owners remaining in an Exposure Tier 0 or 1 classification due to this smoke exposure dilution effect. Where clean fuel stoves (LPG or electric) are present (`{{CLEAN_STOVE_NAT}}%` nationally), households frequently retain traditional biomass stoves as secondary devices to save expensive gas or electricity units.

Under standard MTF methodology, the Exposure attribute is evaluated based on the primary cookstove and kitchen ventilation conditions; secondary stove stacking is not accounted for in the primary tier rating. Consequently, households whose primary stove is clean are classified in high tiers even if secondary biomass fires are operated, while households retaining open fires as their primary cooking technology remain in Exposure Tier 0 or 1 regardless of secondary clean device ownership.

**Epidemiological Evidence and WHO IAQ Guidelines:** Epidemiological studies (Burnett et al. 2014; Smith and Peel 2010) and World Health Organization (WHO 2014) Indoor Air Quality Guidelines emphasize the severe non-linearity of the dose-response relationship between fine particulate matter (PM2.5) exposure and cardiopulmonary health outcomes. Because the health damage curve is supra-linear at elevated exposure levels, retaining even occasional secondary use of an open fire (1–2 cooking sessions per week) dilutes more than 80% of the potential respiratory and cardiovascular benefits of clean cooking adoption. Meaningful health protection requires achieving near-complete displacement of traditional biomass combustion.

Figure 10 displays cookstove stacking patterns and the exposure dilution effect among clean cookstove owners.

![Figure 10: Stove Stacking Patterns and the Exposure Dilution Effect Among Clean Cookstove Owners]({{CHART_STOVE_STACKING}})
*Figure 10: Stove stacking patterns and the exposure dilution effect among clean cookstove owners in {{COUNTRY_NAME}}.*

---

### 3.4 Clean Cooking Economic Barriers & Willingness to Pay Module

The transition toward modern cooking services is governed by economic barriers at both the appliance acquisition stage and the recurrent fuel refill stage:
* **High Upfront Capital Outlay:** For clean fuels such as LPG, the initial cost of a double-burner stove, pressurized gas cylinder, regulator, and hose represents a prohibitive barrier for low-income households.
* **Lump-Sum Refill Liquidity Constraints:** Even when appliances are acquired, the lump-sum cash outlay required to refill a standard 6 kg or 12 kg LPG cylinder prevents cash-constrained households from refilling continuously, prompting reversion to daily purchases of small bags of charcoal or gathered firewood.

As illustrated in the contingent valuation demand curves in Figure 11, household willingness to acquire an improved or clean cookstove is severely constrained under upfront lump-sum pricing, but expands significantly when paired with installment financing and capital subsidies. Spreading equipment costs across 6- to 24-month payment schedules unlocks substantial latent demand across all pricing tiers. However, even with 24-month financing, `{{WTP_COOK_NEVER_NAT}}%` of households decline adopting improved stoves; among households declining, `{{REFUSE_COOK_COST_NAT}}%` cite equipment acquisition costs as the primary impediment, while others report satisfaction with three-stone fires or unreliability of modern fuel supply chains. Overcoming this inertia requires combining results-based financing (RBF) for clean cooking distributors with consumer awareness programs demonstrating the long-term fuel expenditure savings and health benefits of efficient stoves.

![Figure 11: Willingness to Pay Cumulative Demand Curves for Clean Cookstoves]({{CHART_WTP_COOKSTOVE}})
*Figure 11: Comparative cumulative willingness-to-pay demand curves for improved and clean cookstoves across payment modalities and subsidy benchmarks.*

#### Strategic e-Cooking Transition Pathway
Survey microdata confirm that electric cooking currently represents an aspirational rather than prevalent practice: fewer than 0.2% of households (<7 sample households nationally) cook with electricity (`{{STOVE_ELEC_N}}%`). Even among grid-connected households, electric stove uptake stands at only `{{ELEC_STOVE_GRID_NAT}}%` nationwide (`{{ELEC_STOVE_GRID_URB}}%` in urban areas vs. `{{ELEC_STOVE_GRID_RUR}}%` in rural areas). Consequently, national clean cooking strategy must follow a realistic dual-track trajectory:
1. **Near-Term Scalable Focus:** Aggressively scale commercial distribution of high-efficiency Improved Biomass Cookstoves (ICS) in rural areas and expand LPG cylinder recirculation networks in urban centers.
2. **Aspirational Leapfrogging Pillar (e-Cooking):** Introduce targeted electric cooking pilots in high-reliability urban grid zones (Tier 4–5 customers) utilizing energy-efficient appliances such as Electric Pressure Cookers (EPCs), which consume 70–80% less electricity than conventional electric hotplates.

**Grid Infrastructure Prerequisites for e-Cooking:** Scaling electric cooking introduces critical distribution network requirements. The extremely low electric cooking uptake among connected households is directly explained by power quality bottlenecks: MTF survey findings reveal that `{{PCT_VOLTAGE_DAMAGE}}%` of grid-connected households have experienced permanent appliance damage from severe voltage fluctuations and power surges. Deploying high-wattage e-cooking appliances without network upgrades risks rapid equipment burnout and consumer disillusionment. Prioritizing low-voltage distribution transformer reinforcement, automated voltage regulators, and domestic surge protection devices is an indispensable technical precondition before launching wide-scale EPC programs.

---

## CHAPTER 4: GENDER DIMENSIONS & SOCIO-ECONOMIC EQUITY

### 4.1 Demographic & Socioeconomic Profile by Gender of Household Head

In {{COUNTRY_NAME}}, `{{MHH_SHARE}}%` of households are headed by men (MHH) and `{{FHH_SHARE}}%` are headed by women (FHH). Survey indicators disaggregated by gender of household head provide insight into comparative demographic profiles, educational attainment, credit access, and energy uptake.

Female household heads average `{{HEAD_AGE_FHH}}` years of age, compared to `{{HEAD_AGE_MHH}}` years for male household heads. Regarding marital status, `{{HEAD_MARITAL_WIDOW_FHH}}%` of female heads and `{{HEAD_MARITAL_WIDOW_MHH}}%` of male heads are widowed, while `{{HEAD_MARITAL_MARRIED_FHH}}%` of female heads and `{{HEAD_MARITAL_MARRIED_MHH}}%` of male heads are married or cohabiting. Educational attainment distributions indicate that `{{HEAD_EDUC_NONE_FHH}}%` of female heads and `{{HEAD_EDUC_NONE_MHH}}%` of male heads report no formal schooling; primary education completion is `{{HEAD_EDUC_PRIM_FHH}}%` for female heads and `{{HEAD_EDUC_PRIM_MHH}}%` for male heads; secondary completion is `{{HEAD_EDUC_SEC_FHH}}%` for female heads and `{{HEAD_EDUC_SEC_MHH}}%` for male heads; and higher education completion stands at `{{HEAD_EDUC_HIGH_FHH}}%` for female heads and `{{HEAD_EDUC_HIGH_MHH}}%` for male heads. Access to loans or credit from formal financial institutions is reported by `{{CREDIT_ACCESS_FHH}}%` of female heads, compared to `{{CREDIT_ACCESS_MHH}}%` of male heads.

Figure 12 displays comparative demographic profiles, educational attainment, credit access, and electricity access parity across female- and male-headed households.

![Figure 12: Demographic Characteristics, Educational Attainment, and Energy Access Parity by Gender of Household Head]({{CHART_GENDER_ACCESS}})
*Figure 12: Demographic characteristics, educational attainment, credit access, and electricity access parity by gender of household head in {{COUNTRY_NAME}}.*

Table 4.1 presents the complete demographic and socioeconomic profile across household headship.

---

### Table 4.1: Demographic and Socioeconomic Profile by Gender of Household Head

| Indicator / Characteristic | Male-Headed (MHH) | Female-Headed (FHH) | National Average |
| :--- | :---: | :---: | :---: |
| **Share of Total Households (%)** | `{{MHH_SHARE}}` | `{{FHH_SHARE}}` | `100.0` |
| **Head Has No Formal Schooling (%)** | `{{HEAD_EDUC_NONE_MHH}}` | `{{HEAD_EDUC_NONE_FHH}}` | `{{HEAD_EDUC_NONE_NAT}}` |
| **Head Completed Primary Education (%)** | `{{HEAD_EDUC_PRIM_MHH}}` | `{{HEAD_EDUC_PRIM_FHH}}` | `{{HEAD_EDUC_PRIM_NAT}}` |
| **Head Completed Secondary Education (%)** | `{{HEAD_EDUC_SEC_MHH}}` | `{{HEAD_EDUC_SEC_FHH}}` | `{{HEAD_EDUC_SEC_NAT}}` |
| **Head Completed Higher Education (%)** | `{{HEAD_EDUC_HIGH_MHH}}` | `{{HEAD_EDUC_HIGH_FHH}}` | `{{HEAD_EDUC_HIGH_NAT}}` |
| **Head Has Access to Loans / Credit (%)** | `{{CREDIT_ACCESS_MHH}}` | `{{CREDIT_ACCESS_FHH}}` | `{{CREDIT_ACCESS_NAT}}` |
| **Electricity Access Rate (Tier 1-5, %)** | `{{MHH_ELEC_ACC}}` | `{{FHH_ELEC_ACC}}` | `{{ELEC_ACC_NAT}}` |
| **WTP Grid Connection Upfront (%)** | `{{WTP_GRID_UPFRONT_MHH}}` | `{{WTP_GRID_UPFRONT_FHH}}` | `{{WTP_GRID_UPFRONT_NAT}}` |
| **WTP Grid Connection (12-Mo. Plan, %)** | `{{WTP_GRID_12M_MHH}}` | `{{WTP_GRID_12M_FHH}}` | `{{WTP_GRID_12M_NAT}}` |

---

### 4.2 Energy Access and Willingness to Pay by Gender of Household Head

Across {{COUNTRY_NAME}}, electricity access (Tier 1+) is recorded at `{{FHH_ELEC_ACC}}%` for female-headed households compared to `{{MHH_ELEC_ACC}}%` for male-headed households. This modest difference is primarily driven by the spatial concentration of female-headed households in urban and peri-urban centers where grid infrastructure is more prevalent.

A key structural barrier facing female heads is access to formal credit: only `{{CREDIT_ACCESS_FHH}}%` of female heads have access to loans or credit from formal financial institutions, compared to `{{CREDIT_ACCESS_MHH}}%` of male heads. This liquidity gap directly impacts upfront connection affordability: stated willingness to pay upfront grid connection fees is lower among female heads (`{{WTP_GRID_UPFRONT_FHH}}%` vs. `{{WTP_GRID_UPFRONT_MHH}}%`). However, when offered a 12-month installment plan, female willingness surges to `{{WTP_GRID_12M_FHH}}%`, narrowing the gap and highlighting the critical necessity of utility-backed flexible payment schemes.

Furthermore, cookstove purchase decisions are reported as made primarily by female household members in `{{COOK_DEC_FEMALE_NAT}}%` of households, by male members in `{{COOK_DEC_MALE_NAT}}%`, and jointly in `{{COOK_DEC_JOINT_NAT}}%`. Because women are the principal decision-makers regarding cooking technologies, clean cooking marketing, financing mechanisms, and user-training programs must be tailored directly to female consumers.

---

### 4.3 Home Production, Time Poverty, and Labor Supply Release (Dinkelman 2011 Model)

In seminal econometric work on the employment effects of infrastructure expansion, Taryn Dinkelman (2011, American Economic Review) established that rural electrification alters household time allocation through a home production channel: by substituting modern energy for labor-intensive domestic chores, electrification reduces the time women must allocate to home production, thereby releasing female labor supply for market-oriented employment. In subsequent research, Dinkelman et al. (2024) demonstrate that long-run access to modern household infrastructure permanently shifts women's lifetime labor market trajectories out of unpaid domestic labor and into productive non-farm enterprises.

Time-use data from the {{SURVEY_YEAR}} MTF survey in {{COUNTRY_NAME}} provide empirical verification of this home production burden. Adult women spend an average of `{{WOMEN_COOK_TIME}}` minutes per day preparing meals, compared to `{{MEN_COOK_TIME}}` minutes for adult men.

In addition to cooking, adult women bear the primary responsibility for fuelwood collection and preparation. In firewood-gathering communities, 99.3% of adult women actively participate in collection, with each trip requiring an average of 53.5 minutes (undertaken 1 to 3 times per week). In addition, fuel preparation takes an average of 21.1 minutes daily. Annualized across 365 calendar days, women spend an average of `{{WOMEN_FUEL_TIME}}` minutes per calendar day collecting firewood (compared to `{{MEN_FUEL_TIME}}` minutes for adult men), which equates to approximately 81 hours or **`{{WOMEN_FUEL_WORKDAYS}}` full eight-hour working days lost per woman each year** solely to fuel gathering. When combined with daily cooking (`{{WOMEN_COOK_TIME}}` minutes), adult women dedicate over **1.8 hours (108 minutes) every single day** to domestic energy chores.

The substantial time spent collecting and preparing firewood bundles over long distances deprives rural women of opportunities for agricultural commercialization, micro-enterprise operations, child care, and schooling. Transitioning to modern energy cooking services and high-efficiency cookstoves directly frees female labor from domestic chores, serving as a powerful catalyst for female wage employment, enterprise formation, and human capital accumulation.

Figure 13 illustrates the intra-household time-use burden for meal preparation and firewood collection across adult women and men.

![Figure 13: Intra-Household Time-Use Burden for Fuelwood Collection and Cooking Across Demographic Groups]({{CHART_GENDER_FUEL}})
*Figure 13: Intra-household time-use burden for fuelwood collection and cooking across demographic groups in {{COUNTRY_NAME}}.*

---

### 4.4 Gender-Informed Energy Interventions

Integrating gender considerations into national energy planning requires addressing both access to energy infrastructure and women's economic participation across the energy supply chain. Because women bear the primary responsibility for cooking and fuel gathering while making `{{COOK_DEC_FEMALE_NAT}}%` of cookstove purchasing decisions, clean cooking market interventions must be designed in direct consultation with women's cooperatives, community savings associations, and female entrepreneurs. Priorities include:
1. **Utility-Backed On-Bill Financing:** Introducing 12- to 24-month connection fee installment facilities to overcome the `{{CREDIT_ACCESS_FHH}}%` credit access barrier among female-headed households.
2. **Female Energy Entrepreneurship Networks:** Establishing targeted credit and working capital facilities for women-led distributors of Improved Cookstoves and Solar Home Systems.
3. **Gender-Targeted Subsidies:** Providing connection vouchers and internal wiring assistance for vulnerable female heads of household.

---

## CHAPTER 5: STRATEGIC POLICY RECOMMENDATIONS & INVESTMENT ROADMAP

Based on the empirical findings of the {{SURVEY_YEAR}} Multi-Tier Framework survey, the Government of {{COUNTRY_NAME}}, international development partners, utility operators, and private sector financiers should prioritize six strategic intervention pillars alongside institutional data systems:

> [!NOTE]
> **COUNTRY COORDINATOR ACTION REQUIRED:** Adapt the strategic pillars below to align with country institutional mandates, national utility expansion programs (e.g., ASCENT, Mission 300 Compact), and ongoing donor co-financing facilities.

### 1. Distribution Network Quality & Voltage Surge Protection
To eliminate severe appliance damage affecting `{{PCT_VOLTAGE_DAMAGE}}%` of grid-connected households, the national power utility must prioritize distribution network reinforcement. Overloaded distribution transformers require urgent upgrading, complemented by the deployment of Automatic Voltage Regulators (AVRs) and localized surge suppression equipment. Furthermore, medium- and low-voltage feeders must be reinforced during peak evening hours (18:00 to 22:00) to resolve evening supply shortfalls (`{{PCT_EVE_SHORTAGE}}%` receiving <4 hours). Importantly, technical voltage stabilization is an indispensable infrastructure prerequisite before promoting modern high-wattage electric cooking devices. Preventive vegetation management and automated fault detection should also be institutionalized to sustain low interruption frequencies (`{{AVG_OUTAGES_PER_WEEK}}` disruptions/week, with `{{OUTAGES_LT3_WK}}%` receiving <3 outages/week) and enable grid consumers to achieve high-tier service.

### 2. Accelerated Last-Mile Grid Densification via 'Ready Boards' & Installment Modalities
Last-mile grid densification offers the fastest and most capital-efficient pathway to expanding national access. While `{{UNDER_THE_GRID_NAT}}%` of households live in electrified Enumeration Areas, only `{{GRID_UPTAKE_NAT}}%` are connected, creating an unconnected under-the-grid deficit of `{{UNDER_GRID_UNCONNECTED_NAT}}%`. Raising uptake in electrified EAs to 60.0% would add **27.2 percentage points** to national electrification at a fraction of the cost of greenfield grid extension. To unlock household demand, utilities should introduce standardized on-bill connection installment facilities spread over 12 to 24 months, bridging the gap between stated upfront cash willingness (`{{WTP_GRID_UPFRONT_NAT}}%`) and 12-month installment willingness (`{{WTP_GRID_12M_NAT}}%`). Concurrently, internal house wiring bottlenecks—cited by `{{REFUSE_WIRING_COST_NAT}}%` of households who decline connection even when fees are waived—must be overcome through the scale-up of standardized pre-wired 'ready boards' and subsidized internal installation packages.

### 3. High-Tier Off-Grid Solar & Island Electrification Acceleration
For remote populations residing beyond the physical reach of the national distribution network, off-grid solar policy should accelerate the transition from entry-level solar lanterns (representing 43.2% of primary devices among solar adopters) and basic Solar Lighting Systems (47.6%) toward certified (IEC/VeraSol) multi-light Solar Home Systems (currently 9.2%) capable of powering domestic entertainment, refrigeration, and productive equipment. Expanding digital Pay-As-You-Go (PAYGo) consumer financing and Results-Based Financing (RBF) facilities will enhance equipment affordability. Furthermore, special spatial planning is required for isolated archipelago territories—most notably the Bijagós archipelago—where submarine cable interconnection is infeasible. Electrification programs must deploy maritime logistics corridors, localized spare-parts depots, and climate-resilient solar-plus-storage mini-grids engineered specifically to withstand saline marine environments.

### 4. Tariff Structuring, Lifeline Protections & Payment Flexibility
To protect low-income connected households from post-connection payment distress and voluntary self-disconnection, the regulatory framework must maintain progressive volumetric lifeline tariffs. With monthly household spending on metered grid electricity averaging `{{GRID_MONTHLY_SPEND_NAT}}` `{{CURRENCY_CODE}}` nationally (and a national median of approximately 8,000 `{{CURRENCY_CODE}}`), lifeline protections ensure that basic domestic electricity consumption remains affordable for vulnerable families. Because over 92% of connected households utilize prepaid meters—typically purchasing recharges in smaller increments averaging ~6,500 `{{CURRENCY_CODE}}`—utilities should expand digital payment integrations via mobile money, permitting micro-top-ups that align with irregular agricultural and informal cash flows while avoiding punitive reconnection fees.

### 5. Dual-Track Clean Cooking Transition & Health Impact Maximization
National clean cooking strategy must follow a realistic dual-track trajectory that combines near-term scalable solutions with targeted modern energy leapfrogging. In rural areas, programs should aggressively scale the commercial distribution of high-efficiency Improved Cookstoves (ICS) to reduce firewood consumption and alleviate the `{{WOMEN_FUEL_WORKDAYS}}` full working days lost per woman each year to fuelwood collection. In urban centers, expanding LPG cylinder recirculation networks and small-cylinder retail depots can overcome lump-sum refill constraints. Concurrently, electric cooking pilots utilizing energy-efficient Electric Pressure Cookers (EPCs) should be introduced in high-reliability urban grid zones. Crucially, public health campaigns must educate consumers on the supra-linear health damage of stove stacking, emphasizing that maintaining open fires even 1–2 times weekly offsets >80% of health benefits due to non-linear PM2.5 exposure relationships.

### 6. Gender Parity & Women-Led Clean Energy Entrepreneurship
Closing the gender energy access gap requires targeted interventions that address the formal credit constraints facing female heads of household (`{{CREDIT_ACCESS_FHH}}%` credit access vs. `{{CREDIT_ACCESS_MHH}}%` for male heads). Utilities and microfinance institutions should deploy on-bill financing, collateral-free credit lines, and subsidized connection vouchers specifically targeting vulnerable female-headed families. In parallel, because women make `{{COOK_DEC_FEMALE_NAT}}%` of cookstove purchasing decisions and manage domestic fuel utilization, women-led clean cookstove and solar retail networks should be supported through dedicated working capital facilities, technical training, and business development grants.

### 7. Energy Data Systems & Institutional Capacity Building
Sustaining national electrification momentum requires modernizing institutional energy data infrastructure. Short-form Multi-Tier Framework survey modules should be integrated into regular household living standards surveys administered by the National Statistics Institute to continuously monitor multi-tier access, service quality, and voltage reliability. MTF survey microdata should also be paired with geospatial network models and satellite imagery to dynamically optimize technology boundaries between grid densification, grid extension, mini-grids, and off-grid solar. Finally, sector ministries and regulatory authorities must be equipped with analytical modeling tools to evaluate tariff designs, connection subsidy schemes, and utility performance benchmarks.

---

## TECHNICAL ANNEXES

### Annex 1: Multi-Tier Framework Reference Matrices

#### Table A1.1: Multi-Tier Framework for Measuring Access to Electricity

| Attribute | Tier 0 | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Capacity** (Peak Power) | <3W | >=3W | >=50W | >=200W | >=800W | >=2,000W |
| **Daily Availability** | <4 hours | >=4 hours | >=4 hours | >=8 hours | >=16 hours | >=23 hours |
| **Evening Availability** | <1 hour | >=1 hour | >=2 hours | >=3 hours | >=4 hours | >=4 hours |
| **Reliability** | Disrupted | -- | -- | <=14 outages/wk | <=14 outages/wk | <=3 outages/wk |
| **Quality** | Unstable | -- | -- | -- | No appliance damage | No appliance damage |
| **Affordability** | Unaffordable | -- | -- | <5% budget | <5% budget | <5% budget |
| **Formality** | Informal | -- | -- | -- | Formal payment | Formal payment |
| **Health & Safety** | Past accidents | -- | -- | -- | Safe | Safe |

#### Table A1.2: Multi-Tier Framework for Measuring Access to Modern Energy Cooking Solutions

| Attribute | Tier 0 | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Cooking Exposure** | Open fire / no vent | Basic biomass | Moderate vent | Chimney / good vent | Clean fuel (LPG/bio) | Electric / Solar |
| **Efficiency** | <10% | >=10% | >=20% | >=30% | >=40% | >=50% |
| **Convenience: Fuel Time** | >=7 hrs/wk | <7 hrs/wk | <3 hrs/wk | <1.5 hrs/wk | <0.5 hrs/wk | <0.5 hrs/wk |
| **Convenience: Prep Time** | >=15 min/meal | <15 min | <10 min | <5 min | <2 min | <2 min |
| **Safety** | Past serious burns | -- | -- | Minor burns | Safe | Safe |
| **Affordability** | >=5% budget | -- | -- | -- | <5% budget | <5% budget |
| **Fuel Availability** | <80% year | -- | -- | >=80% year | Ready availability | Continuous |

---

### Annex 2: Survey Sampling Methodology & Primary Sampling Units

The {{SURVEY_YEAR}} MTF Household Survey in {{COUNTRY_NAME}} utilized a two-stage stratified cluster sampling design engineered to provide representative estimates for the national population as well as urban and rural domains across all `{{ADMIN1_COUNT}}` administrative `{{ADMIN1_UNIT_LABEL_PLURAL}}`.

Sampling stratification divided the national territory into `{{STRATA_COUNT}}` explicit strata. Within each stratum, Primary Sampling Units (PSUs / EAs) were selected with Probability Proportional to Size (PPS). In each selected EA, a full field listing of all residential structures and households was conducted prior to sample selection. Households were then drawn via systematic equal-probability sampling from the listing register. Individual calibrated household weights (`hh_wt`) were calculated to adjust for selection probabilities, non-response, and post-stratification census alignment.

---

### Annex 3: Data Visualizations Gallery

The following publication-grade charts summarize the complete empirical diagnostic suite for {{COUNTRY_NAME}}:

* **Figure 1:** Multi-Tier Framework Electricity Access Tier Distribution Across National, Urban, and Rural Populations
  ![Figure 1: Multi-Tier Framework Electricity Access Tier Distribution Across National, Urban, and Rural Populations]({{CHART_ELEC_TIERS}})

* **Figure 2:** Household Electricity Source Mix and Exclusion of Dry-Cell Torches Under SDG 7.1.1
  ![Figure 2: Household Electricity Source Mix and Exclusion of Dry-Cell Torches Under SDG 7.1.1]({{CHART_SOURCE_MIX}})

* **Figure 2B:** Off-Grid Solar Device Typology (Lanterns vs. SLS vs. SHS) Across National, Urban, and Rural Populations
  ![Figure 2B: Off-Grid Solar Device Typology Across National, Urban, and Rural Populations]({{CHART_SOLAR_TYPOLOGY}})

* **Figure 3:** Household Electricity and Modern Energy Cooking Access Across National Consumption Expenditure Quintiles (Q1 to Q5)
  ![Figure 3: Household Electricity and Modern Energy Cooking Access Across National Consumption Expenditure Quintiles (Q1 to Q5)]({{CHART_QUINTILE_CURVE}})

* **Figure 4:** The Under-the-Grid Uptake Funnel and National Densification Deficit
  ![Figure 4: The Under-the-Grid Uptake Funnel and National Densification Deficit]({{CHART_UNDER_GRID}})

* **Figure 5:** Primary Stated Barriers to Gaining Grid Connection
  ![Figure 5: Primary Stated Barriers to Gaining Grid Connection]({{CHART_GRID_BARRIERS}})

* **Figure 6:** Willingness to Pay Cumulative Demand Curves for National Grid Connection
  ![Figure 6: Willingness to Pay Cumulative Demand Curves for National Grid Connection]({{CHART_WTP_GRID}})

* **Figure 7:** Willingness to Pay Cumulative Demand Curves for Off-Grid Solar Devices
  ![Figure 7: Willingness to Pay Cumulative Demand Curves for Off-Grid Solar Devices]({{CHART_WTP_SOLAR}})

* **Figure 8:** Primary Cookstove Typology and Primary Fuel Distribution Across National, Urban, and Rural Populations
  ![Figure 8: Primary Cookstove Typology and Primary Fuel Distribution Across National, Urban, and Rural Populations]({{CHART_STOVE_FUELS}})

* **Figure 9:** Multi-Tier Framework Modern Energy Cooking Services (MECS) Tier Distribution
  ![Figure 9: Multi-Tier Framework Modern Energy Cooking Services (MECS) Tier Distribution]({{CHART_COOKING_TIERS}})

* **Figure 10:** Stove Stacking Patterns and the Exposure Dilution Effect Among Clean Cookstove Owners
  ![Figure 10: Stove Stacking Patterns and the Exposure Dilution Effect Among Clean Cookstove Owners]({{CHART_STOVE_STACKING}})

* **Figure 11:** Willingness to Pay Cumulative Demand Curves for Clean Cookstoves
  ![Figure 11: Willingness to Pay Cumulative Demand Curves for Clean Cookstoves]({{CHART_WTP_COOKSTOVE}})

* **Figure 12:** Demographic Characteristics, Educational Attainment, and Energy Access Parity by Gender of Household Head
  ![Figure 12: Demographic Characteristics, Educational Attainment, and Energy Access Parity by Gender of Household Head]({{CHART_GENDER_ACCESS}})

* **Figure 13:** Intra-Household Time-Use Burden for Fuelwood Collection and Cooking Across Demographic Groups
  ![Figure 13: Intra-Household Time-Use Burden for Fuelwood Collection and Cooking Across Demographic Groups]({{CHART_GENDER_FUEL}})

---

### Annex 4: Standard Cookstove Typology, Efficiency Standards, and ISO Performance Targets

The International Organization for Standardization (ISO) established technical standard ISO 19867-1 and Voluntary Performance Targets (VPT) for cookstoves, classifying cooking technologies across six tiers (Tier 0 to Tier 5) based on laboratory and field testing:

1. **Carbon Monoxide (CO) Emissions:** Evaluates grams of CO emitted per megajoule of useful cooking energy ($MJ_{d}$). Tiers range from Tier 0 (>16 g/MJd) for traditional open fires to Tier 5 (<3.0 g/MJd) for clean LPG, biogas, and electric induction cookers.
2. **Fine Particulate Matter ($PM_{2.5}$) Emissions:** Evaluates milligrams of $PM_{2.5}$ emitted per megajoule of useful energy. Tiers range from Tier 0 (>1,000 mg/MJd) to Tier 5 (<5 mg/MJd). Only modern clean fuels (electricity, LPG, ethanol, biogas) achieve Tier 4 or Tier 5.
3. **Thermal Efficiency:** Measures the percentage of released fuel energy transferred into the cooking vessel. Tiers range from Tier 0 (<10%) for open three-stone fires, through Tiers 2–3 (20–35%) for improved biomass cookstoves, to Tiers 4–5 (40–85%+) for modern pressurized gas and electric induction cooking appliances.
4. **Safety & Durability:** Evaluates mechanical stability, sharp edges, operational surface temperatures, and flame containment based on standardized protocol checklists.

---

### REFERENCES & CORE PUBLICATIONS

* **Bhatia, Mikul, and Nicolina Angelou.** 2015. *Beyond Connections: Energy Access Redefined.* ESMAP Technical Report 008/15. Washington, DC: World Bank Group.
* **Burnett, Richard, et al.** 2014. "An Integrated Risk Function for Estimating the Global Burden of Disease Attributable to Ambient and Household Fine Particulate Matter Exposure." *Environmental Health Perspectives* 122 (4): 397–403.
* **Dinkelman, Taryn.** 2011. "The Effects of Rural Electrification on Employment: New Evidence from South Africa." *American Economic Review* 101 (7): 3078–3108.
* **Dinkelman, Taryn, et al.** 2024. "Infrastructure Investments and the Long-Run Trajectory of Female Labor Supply in Developing Economies." *Journal of Development Economics* (forthcoming).
* **ESMAP.** 2020. *The State of Access to Modern Energy Cooking Services.* Washington, DC: World Bank Group.
* **IEA, IRENA, UNSD, World Bank, and WHO.** 2024. *Tracking SDG 7: The Energy Progress Report 2024.* Washington, DC: World Bank.
* **International Organization for Standardization (ISO).** 2018. *Clean cookstoves and clean cooking solutions — Harmonized laboratory test protocols — Part 1: Standard test sequence for emissions and performance, safety and durability.* ISO 19867-1:2018. Geneva: ISO.
* **Lee, Kenneth, Edward Miguel, and Catherine Wolfram.** 2020. "Experimental Evidence on the Economics of Rural Electrification." *Journal of Political Economy* 128 (4): 1523–1565.
* **Smith, Kirk R., and Jennifer L. Peel.** 2010. "Mind the Gap: Incomplete Transition to Clean Cooking and Health Benefits." *Annual Review of Public Health* 31: 275–294.
* **World Bank.** 2023. *Multi-Tier Framework Survey Methodology and Implementation Guidelines.* Washington, DC: World Bank Group.
* **World Health Organization (WHO).** 2014. *WHO Guidelines for Indoor Air Quality: Household Fuel Combustion.* Geneva: World Health Organization.

---
*Report published by the World Bank Group and the Energy Sector Management Assistance Program (ESMAP), Washington, DC.*
