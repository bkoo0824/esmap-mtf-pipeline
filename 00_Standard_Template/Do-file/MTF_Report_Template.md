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
{{CHART_UNDER_GRID}}           : Figure 3  — Under-the-Grid Densification Funnel (10_under_the_grid_funnel.png)
{{CHART_ELEC_RADAR}}           : Figure 4  — Electricity Attribute Performance Radar (03_elec_attribute_radar.png)
{{CHART_QUINTILE_CURVE}}       : Figure 5  — Access Across Expenditure Quintiles (04_quintile_access_curve.png)
{{CHART_GRID_BARRIERS}}        : Figure 6   — Grid Connection Barriers & WTP Relief (06_grid_barriers_wtp.png)
{{CHART_WTP_GRID}}             : Figure 7a  — Grid Connection WTP Cumulative Demand Curve (12a_wtp_grid_connection.png)
{{CHART_WTP_SOLAR}}            : Figure 7b  — Off-Grid Solar WTP Cumulative Demand Curve (12b_wtp_solar_device.png)
{{CHART_WTP_COOKSTOVE}}        : Figure 7c  — Clean Cookstove WTP Cumulative Demand Curve (12c_wtp_cookstove.png)
{{CHART_WTP_DEMAND}}           : Figure 7   — Fallback/Legacy WTP Demand Curve (12a_wtp_grid_connection.png)
{{CHART_WTP_SEGMENTS}}         : Figure 8   — 100% Mutually Exclusive WTP Financing Segments (13_wtp_mutually_exclusive_stacked.png)
{{CHART_STOVE_FUELS}}          : Figure 9  — Primary Cookstove Typology & Fuel Mix (07_stove_technology_fuels.png)
{{CHART_COOKING_TIERS}}        : Figure 10 — MECS Cooking Tier Distribution (02_cooking_tier_distribution.png)
{{CHART_STOVE_STACKING}}       : Figure 11 — Clean Cooking Stacking & Exposure Dilution (14_stove_stacking_matrix.png)
{{CHART_GENDER_ACCESS}}        : Figure 12 — Gender Demographics, Credit & Access Parity (08_gender_demographics_access.png)
{{CHART_GENDER_FUEL}}          : Figure 13 — Gender Time-Use Burden for Fuel Collection (05_gender_fuel_collection_time.png)
{{CHART_REGIONAL_GAP}}         : Figure 14 — Subnational Disparities in Electricity Access (09_regional_access_gap.png)

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

Crucially, the empirical diagnostic reveals three distinct population segments that require differentiated policy interventions:
1. **Grid-Connected Households Requiring Service Quality Upgrades:** While physical reliability is comparatively strong (`{{OUTAGES_LT3_WK}}%` experience fewer than 3 interruptions per week), chronic voltage instability damages appliances for `{{PCT_VOLTAGE_DAMAGE}}%` of grid customers, and evening supply shortfalls (`{{PCT_EVE_SHORTAGE}}%`) restrict productive use and transition to Tier 5 service.
2. **Under-the-Grid Unconnected Households (The Densification Opportunity):** A striking `{{UNDER_THE_GRID_NAT}}%` of households reside in communities where the low-voltage grid is already present (electrified Enumeration Areas), yet only `{{GRID_UPTAKE_NAT}}%` are connected. Closing this under-the-grid deficit through targeted connection fee financing represents the fastest, most cost-effective path to expanding national electrification.
3. **Remote Off-Grid Households Requiring Distributed Solutions:** Beyond the economic reach of the grid, households depend on standalone off-grid solar, where basic solar lanterns leave `{{PCT_SL_STUCK_T1}}%` constrained to Tier 1 service, and traditional biomass dominates cooking.

Analytical modeling of household willingness to pay across randomized price subsidy tiers and financing maturities is anchored in the experimental economics literature on rural electrification (Kenneth Lee, Edward Miguel, and Catherine Wolfram 2020), while intra-household time poverty and female labor supply dynamics are evaluated using home production frameworks (Taryn Dinkelman 2011).

---

### 2. Access to Electricity Key Findings

* **National Electrification Rate:** Nationwide, `{{ELEC_ACC_NAT}}%` of households have access to electricity at Tier 1 or above, comprising `{{ELEC_ACC_URB}}%` in urban areas and `{{ELEC_ACC_RUR}}%` in rural areas.
* **Technology Conduits:** Electricity access is delivered through two primary conduits: the **National Grid**, serving `{{GRID_ACC_NAT}}%` of households nationwide (`{{GRID_ACC_URB}}%` in urban areas and `{{GRID_ACC_RUR}}%` in rural areas), and **Off-Grid Solar Solutions** (standalone Solar Home Systems, solar lighting kits, and solar lanterns), serving `{{SOLAR_ACC_NAT}}%` of households (`{{SOLAR_ACC_URB}}%` in urban areas and `{{SOLAR_ACC_RUR}}%` in rural areas). Under SDG 7.1.1 monitoring standards, disposable dry-cell battery torches and flashlights are strictly excluded from modern electricity metrics.
* **Tier Distribution & Service Depth:** Nationwide, `{{ELEC_T0_NAT}}%` of households remain in **Tier 0** (no access or sub-Tier 1 supply). High-tier electricity access (**Tier 4 or 5**) is achieved by `{{ELEC_T45_NAT}}%` of households nationwide, concentrated heavily in urban centers (`{{ELEC_T45_URB}}%`) compared to only `{{ELEC_T45_RUR}}%` in rural areas.
* **Grid Reliability and Service Quality:** While grid connection provides high capacity, service quality presents operational challenges. Grid-connected households report an average of `{{AVG_OUTAGES_PER_WEEK}}` unexpected power interruptions per week, with `{{OUTAGES_LT3_WK}}%` experiencing fewer than 3 disruptions per week (satisfying the Tier 5 reliability benchmark) and `{{OUTAGES_3TO14_WK}}%` experiencing 3 to 14 disruptions per week. However, power quality instability is significant: `{{PCT_VOLTAGE_DAMAGE}}%` of grid-connected households report that voltage fluctuations and surges have permanently damaged household appliances. Evening supply duration is also constrained, with `{{PCT_EVE_SHORTAGE}}%` of grid customers reporting less than 4 hours of supply during peak evening demand hours (18:00 to 22:00).
* **The "Under-the-Grid" Densification Opportunity:** In communities where the distribution network is already present (electrified Enumeration Areas), `{{UNDER_GRID_UNCONNECTED_NAT}}%` of households remain unconnected (`{{UNDER_GRID_UNCONNECTED_URB}}%` in urban areas and `{{UNDER_GRID_UNCONNECTED_RUR}}%` in rural areas). The overall grid connection uptake rate within electrified EAs stands at `{{GRID_UPTAKE_NAT}}%` nationally (`{{GRID_UPTAKE_URB}}%` in urban centers and `{{GRID_UPTAKE_RUR}}%` in rural localities). Expanding grid uptake within existing electrified EAs from `{{GRID_UPTAKE_NAT}}%` to 60.0% would add **27.2 percentage points** to national electrification, connecting households at a fraction of the cost of greenfield grid extension.
* **Barriers to Connection:** Among unconnected households, the upfront connection fee is predominantly cited as the primary obstacle (`{{BARRIER_COST_NAT}}%` nationally; `{{BARRIER_COST_URB}}%` urban vs. `{{BARRIER_COST_RUR}}%` rural), followed by physical distance from the network (`{{BARRIER_DIST_NAT}}%` nationally; `{{BARRIER_DIST_URB}}%` urban vs. `{{BARRIER_DIST_RUR}}%` rural).
* **Financing Elasticity and Willingness to Pay (WTP):** While `{{WTP_GRID_UPFRONT_NAT}}%` of unconnected households express willingness to pay the connection fee upfront in cash, stated willingness surges to `{{WTP_GRID_12M_NAT}}%` under a **12-month installment plan**. When the connection fee is completely waived, `{{WTP_GRID_WAIVED_NAT}}%` would connect, while `{{WTP_GRID_NEVER_NAT}}%` decline connection; within the declining group, `{{REFUSE_WIRING_COST_NAT}}%` cite internal household wiring costs as the decisive barrier.
* **Off-Grid Solar Constraints:** Among off-grid solar users, `{{PCT_SL_STUCK_T1}}%` remain constrained to basic Tier 1 lighting service due to low solar lantern capacities. Stated willingness to purchase a quality-verified Solar Home System (SHS) expands from `{{WTP_SOLAR_UPFRONT_NAT}}%` upfront to `{{WTP_SOLAR_12M_NAT}}%` under a 12-month installment plan and `{{WTP_SOLAR_24M_NAT}}%` over 24 months.

---

### 3. Access to Modern Energy Cooking Services (MECS) Key Findings

* **Prevalence of Traditional Biomass:** Cooking practices remain heavily dominated by solid biomass fuels. Nationwide, `{{THREESTONE_NAT}}%` of households cook primarily over a **three-stone open fire** (`{{STOVE_3STONE_U}}%` in urban areas and `{{STOVE_3STONE_R}}%` in rural areas). Traditional metal and artisanal charcoal stoves account for `{{STOVE_TRAD_N}}%` of households, while **Improved Cookstoves (ICS)** serve `{{STOVE_ICS_N}}%`.
* **Clean Cooking Adoption:** Modern clean cooking solutions (LPG and electric stoves) serve only `{{CLEAN_STOVE_NAT}}%` of households nationwide (`{{CLEAN_STOVE_URB}}%` in urban areas vs. `{{CLEAN_STOVE_RUR}}%` in rural areas), almost exclusively through LPG. Electric cooking accounts for `{{STOVE_ELEC_N}}%` nationally (`{{STOVE_ELEC_U}}%` urban vs. `{{STOVE_ELEC_R}}%` rural), reflecting that electric stove ownership remains confined to fewer than 0.2% of households (<7 sample households nationwide).
* **MECS Tier Distribution (Clean Cooking Deficit):** Under MTF methodology, households in **Tier 0 or 1** (accounting for `{{COOK_T01_NAT}}%` nationally) have no access to clean cooking and remain exposed to hazardous household air pollution. Only `{{CLEAN_STOVE_NAT}}%` reach **Tier 4 or 5** (access to Modern Energy Cooking Services), while `{{TRANS_COOK_NAT}}%` obtain **Tier 2 or 3** (transitional/improved cooking through ICS).
* **Cookstove Time-Use Disparities:** Primary stove choice directly dictates domestic cooking duration:
  - Three-stone open fires require an average of `{{HR_3STONE_NAT}}` hours per week (156 minutes per day).
  - Traditional artisanal charcoal stoves require `{{HR_TRAD_NAT}}` hours per week (101 minutes per day).
  - Improved Cookstoves (ICS) require `{{HR_ICS_NAT}}` hours per week (97 minutes per day).
  - Modern LPG stoves require only `{{HR_LPG_NAT}}` hours per week (72 minutes per day), saving **over 11 hours per week** compared to traditional open fires.
* **Stove Stacking & Multi-Biomass Stacking:** Rather than transitioning to single modern cooking devices, households frequently utilize multiple stoves. While clean stove ownership is limited to `{{PCT_CLEAN_STOVE_OWNERSHIP}}%`, among clean stove owners `{{PCT_STOVE_STACKING}}%` stack with traditional biomass stoves, resulting in `{{PCT_STACKING_DILUTION}}%` remaining in exposure Tier 0-1 due to this exposure dilution effect.
* **Strategic e-Cooking Transition:** Given current empirical baselines (<0.2%), immediate national clean cooking priorities must center on expanding Improved Biomass Cookstoves (ICS) and commercial LPG distribution. Electric cooking (e-cooking) represents an aspirational leapfrogging pillar that should be piloted in high-reliability urban grid zones with energy-efficient appliances such as Electric Pressure Cookers (EPCs).

---

### 4. Gender Dimensions & Socio-Economic Equity Key Findings

* **Female Headship and Access to Credit:** Female-headed households (FHH) comprise `{{FHH_SHARE}}%` of households nationwide. Formal credit access among female heads stands at `{{CREDIT_ACCESS_FHH}}%`, compared to `{{CREDIT_ACCESS_MHH}}%` among male heads, creating a structural liquidity barrier for upfront energy investments.
* **Financing Relief for Female Heads:** Stated willingness to pay upfront grid connection fees is lower among female heads (`{{WTP_GRID_UPFRONT_FHH}}%` vs. `{{WTP_GRID_UPFRONT_MHH}}%` for male heads). However, under a 12-month installment schedule, female willingness surges to `{{WTP_GRID_12M_FHH}}%`, demonstrating the catalytic impact of flexible utility financing in overcoming gendered credit gaps.
* **Decision-Making Authority:** Female household members make cookstove purchase decisions in `{{COOK_DEC_FEMALE_NAT}}%` of households (compared to `{{COOK_DEC_MALE_NAT}}%` by male members and `{{COOK_DEC_JOINT_NAT}}%` jointly), underscoring that clean cooking market interventions and promotional channels must be tailored directly to women.
* **Home Production and Time Poverty (Dinkelman 2011 Framework):** Domestic energy burdens fall disproportionately on women. Adult women spend an average of `{{WOMEN_COOK_TIME}}` minutes per day cooking (compared to `{{MEN_COOK_TIME}}` minutes for adult men) and `{{WOMEN_FUEL_TIME}}` minutes per day collecting firewood (compared to `{{MEN_FUEL_TIME}}` minutes for men), equating to **`{{WOMEN_FUEL_WORKDAYS}}` full eight-hour working days lost per year** solely to fuel gathering. Expanding access to modern cooking fuels and reliable electricity frees female labor from domestic chores, releasing substantial time for wage-earning employment and micro-enterprise development.

---

### Table 1.1: National MTF Executive Summary Dashboard

| Energy Access Dimension / Metric | Nationwide (%) | Urban (%) | Rural (%) | Primary Bottleneck / Policy Driver |
| :--- | :---: | :---: | :---: | :--- |
| **Electricity Access Rate (Tier 1-5)** | `{{ELEC_ACC_NAT}}` | `{{ELEC_ACC_URB}}` | `{{ELEC_ACC_RUR}}` | Basic tier 1 lighting threshold |
| **Electricity Tier 0 (No Access / Minimal)** | `{{ELEC_T0_NAT}}` | `{{ELEC_T0_URB}}` | `{{ELEC_T0_RUR}}` | Infrastructure coverage & connection fees |
| **High Electricity Access (Tier 4 & 5)** | `{{ELEC_T45_NAT}}` | `{{ELEC_T45_URB}}` | `{{ELEC_T45_RUR}}` | Voltage stability & evening duration deficits |
| **Main Electricity Source: National Grid** | `{{GRID_ACC_NAT}}` | `{{GRID_ACC_URB}}` | `{{GRID_ACC_RUR}}` | Grid network reach & utility densification |
| **Main Electricity Source: Off-Grid Solar** | `{{SOLAR_ACC_NAT}}` | `{{SOLAR_ACC_URB}}` | `{{SOLAR_ACC_RUR}}` | Stand-alone SHS & solar lantern adoption |
| **Living in Electrified EAs (Under the Grid)** | `{{UNDER_THE_GRID_NAT}}` | `{{UNDER_THE_GRID_URB}}` | `{{UNDER_THE_GRID_RUR}}` | Low-voltage grid presence in community |
| **Grid Uptake Rate in Electrified EAs**¹ | `{{GRID_UPTAKE_NAT}}` | `{{GRID_UPTAKE_URB}}` | `{{GRID_UPTAKE_RUR}}` | Connection affordability in grid zones |
| **Under-the-Grid Unconnected Deficit**² | `{{UNDER_GRID_UNCONNECTED_NAT}}` | `{{UNDER_GRID_UNCONNECTED_URB}}` | `{{UNDER_GRID_UNCONNECTED_RUR}}` | Connection fee & internal wiring barrier |
| **Clean Cooking Access (MECS: Tier 4-5)** | `{{CLEAN_STOVE_NAT}}` | `{{CLEAN_STOVE_URB}}` | `{{CLEAN_STOVE_RUR}}` | Clean fuel supply chain & appliance cost |
| **Transition Cooking Services (Tier 2-3)** | `{{TRANS_COOK_NAT}}` | `{{TRANS_COOK_URB}}` | `{{TRANS_COOK_RUR}}` | Improved Cookstove (ICS) adoption |
| **Cooking No Access / High Exposure (Tier 0-1)** | `{{COOK_T01_NAT}}` | `{{COOK_T01_URB}}` | `{{COOK_T01_RUR}}` | Open fire & traditional biomass reliance |
| **Primary Stove: Three-Stone / Open Fire** | `{{THREESTONE_NAT}}` | `{{THREESTONE_URB}}` | `{{THREESTONE_RUR}}` | Rural biomass reliance & free gathering |

*Note: Table 1.1 summarizes baseline multi-tier energy access and service quality. An Enumeration Area (EA) is defined as electrified if at least one surveyed household has an active national grid connection (`max(grid_hh) == 1`).*
*¹ **Grid Uptake Rate in Electrified EAs:** The percentage of households residing in electrified EAs that are connected to the grid ($	ext{Connected HHs in Electrified EAs} \div 	ext{Total HHs in Electrified EAs} 	imes 100$).*
*² **Under-the-Grid Unconnected Deficit:** The percentage of households residing in electrified EAs who remain unconnected to the low-voltage network.*

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

In {{COUNTRY_NAME}}, `{{ELEC_ACC_NAT}}%` of households have access to electricity at Tier 1 or above, while `{{ELEC_T0_NAT}}%` remain in Tier 0. In urban areas, grid connection reaches `{{GRID_ACC_URB}}%` of households and off-grid solar solutions serve `{{SOLAR_ACC_URB}}%`. In rural areas, the national grid reaches `{{GRID_ACC_RUR}}%` of households, while off-grid solar systems serve `{{SOLAR_ACC_RUR}}%` of rural households.

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

**Strict Exclusion Rule (SDG 7.1.1):** Disposable dry-cell battery torches, handheld flashlights, and single-use batteries are **strictly excluded** from electrification metrics. While dry-cell torches provide basic task illumination in unserved communities, they do not constitute modern electrical service due to limited luminosity, absence of appliance-powering capacity, high recurrent unit costs, and hazardous environmental disposal footprints.

Figure 2 delineates the primary electricity technology source mix across qualifying modern sources, explicitly contrasting modern solutions against excluded disposable battery devices.

![Figure 2: Household Electricity Source Mix and Exclusion of Dry-Cell Torches Under SDG 7.1.1]({{CHART_SOURCE_MIX}})
*Figure 2: Electrification source breakdown across the six qualifying modern technologies and the exclusion of dry-cell battery lighting.*

Table 2.1 presents the detailed distribution of households across electricity access tiers alongside typical appliance capabilities.

---

### Table 2.1: Electricity Tier Distribution Across National, Urban, and Rural Populations

| Electricity Access Tier | Nationwide (%) | Urban (%) | Rural (%) | Typical Appliance Service & Capabilities |
| :--- | :---: | :---: | :---: | :--- |
| **Tier 0** (No Access / Sub-Tier 1) | `{{ELEC_T0_N}}` | `{{ELEC_T0_U}}` | `{{ELEC_T0_R}}` | Dry-cell batteries, candles, flashlights, paraffin |
| **Tier 1** (Task Lighting & Phone Charging) | `{{ELEC_T1_N}}` | `{{ELEC_T1_U}}` | `{{ELEC_T1_R}}` | Solar lanterns, basic SLS (3-49W, >=4h) |
| **Tier 2** (General Lighting, TV, Fan) | `{{ELEC_T2_N}}` | `{{ELEC_T2_U}}` | `{{ELEC_T2_R}}` | Multi-light SHS (50-199W, >=4h) |
| **Tier 3** (Medium Load & Refrigeration) | `{{ELEC_T3_N}}` | `{{ELEC_T3_U}}` | `{{ELEC_T3_R}}` | Refrigerator, freezer, water pump, grid (>=8h) |
| **Tier 4** (High Load & Productive Use) | `{{ELEC_T4_N}}` | `{{ELEC_T4_U}}` | `{{ELEC_T4_R}}` | Washing machine, electric iron, grid (>=16h) |
| **Tier 5** (Continuous Full Access) | `{{ELEC_T5_N}}` | `{{ELEC_T5_U}}` | `{{ELEC_T5_R}}` | Air conditioning, electric cooking, grid (>=23h) |
| **Access Rate (Tier 1-5)** | `{{ELEC_ACC_NAT}}` | `{{ELEC_ACC_URB}}` | `{{ELEC_ACC_RUR}}` | Universal electrification monitoring threshold |
| **High Access Rate (Tier 4-5)** | `{{ELEC_T45_NAT}}` | `{{ELEC_T45_URB}}` | `{{ELEC_T45_RUR}}` | Modern energy economy threshold |

---

### 2.2 Socioeconomic Equity and the Consumption Quintile Gradient

Electricity access in {{COUNTRY_NAME}} is strongly correlated with household consumption expenditure. Across expenditure quintiles, electrification rates expand steadily from `{{Q1_ELEC_ACC}}%` in the poorest quintile (Q1) to `{{Q2_ELEC_ACC}}%` in Q2, `{{Q3_ELEC_ACC}}%` in Q3, `{{Q4_ELEC_ACC}}%` in Q4, and `{{Q5_ELEC_ACC}}%` in the richest quintile (Q5). In the lowest quintile, the vast majority of households remain unserved, as high initial grid connection fees and internal house wiring costs present an insurmountable barrier to adoption. Conversely, in the richest quintile, higher disposable income and concentration in formal urban settlements enable extensive grid uptake.

This unequal access across income groups creates an **energy poverty penalty**. Low-income households residing in unserved settlements frequently spend a larger fraction of their monthly budget purchasing inferior lighting substitutes (such as candles, kerosene, and disposable dry-cell batteries) per unit of effective lumen-hour than grid-connected households spend on metered utility electricity. Expanding access to affordable off-grid solar kits and subsidized grid connections relieves this cash drain, freeing resources for nutrition, education, and healthcare.

##### Table 2.2: Energy Poverty Penalty — Monthly Coping Mechanism Lighting Expenditures Across Quintiles & Access Status

| Household Segment / Expenditure Quintile | Monthly Coping Fuel Spending (`{{CURRENCY_CODE}}`) | Share of Monthly Household Budget (%) | Primary Substitute Fuel Utilized |
| :--- | :---: | :---: | :--- |
| **Lowest Quintile (Q1) — Unelectrified** | `{{COPING_SPEND_Q1_UNEL}}` | `{{COPING_PCT_Q1_UNEL}}%` | Disposable dry-cell batteries & candles |
| **Lowest Quintile (Q1) — Connected** | `{{COPING_SPEND_Q1_CONN}}` | `{{COPING_PCT_Q1_CONN}}%` | Metered electricity & backup candles |
| **Middle Quintile (Q3) — Unelectrified** | `{{COPING_SPEND_Q3_UNEL}}` | `{{COPING_PCT_Q3_UNEL}}%` | Batteries, candles & kerosene |
| **Middle Quintile (Q3) — Connected** | `{{COPING_SPEND_Q3_CONN}}` | `{{COPING_PCT_Q3_CONN}}%` | Metered grid electricity |
| **Highest Quintile (Q5) — Connected** | `{{COPING_SPEND_Q5_CONN}}` | `{{COPING_PCT_Q5_CONN}}%` | Metered grid & rechargeable backup |
| **National Average (All Unelectrified)** | `{{COPING_SPEND_NAT_UNEL}}` | `{{COPING_PCT_NAT_UNEL}}%` | Inferior lighting substitutes |

*Note: Table 2.2 empirically illustrates the energy poverty penalty. Coping expenditures capture monthly purchases of non-electric lighting and power substitutes (dry-cell batteries, candles, kerosene, and fee-based mobile phone charging) expressed as a percentage of total household consumption expenditure.*

As documented in Table 2.2, unelectrified households in the lowest expenditure quintile spend `{{COPING_PCT_Q1_UNEL}}%` of their total monthly budget solely on coping lighting mechanisms. By contrast, grid-connected households in the same quintile spend just `{{COPING_PCT_Q1_CONN}}%` of their budget on electricity, illustrating that lack of electricity access forces the poor to pay an exorbitant premium for basic task lighting.

Figure 3 displays the progression of electricity and modern energy cooking access rates across consumption expenditure quintiles (Q1 to Q5).

![Figure 3: Household Electricity and Modern Energy Cooking Access Across National Consumption Expenditure Quintiles (Q1 to Q5)]({{CHART_QUINTILE_CURVE}})
*Figure 3: Progression of electricity and modern energy cooking access rates across consumption expenditure quintiles (Q1 to Q5).*

---

### 2.3 Evaluation of Electricity Access by Attribute

In the Multi-Tier Framework, access to electricity is measured by assessing service quality across seven multi-dimensional attributes. Each attribute is categorized from Tier 0 to Tier 5, with the aggregate tier determined by the lowest tier attained among the attributes. Figure 4 displays the multi-attribute radar profile for grid-connected households across urban and rural settlements.

![Figure 4: Multi-Tier Framework Electricity Attribute Performance Radar for Grid-Connected Households (Urban vs. Rural)]({{CHART_ELEC_RADAR}})
*Figure 4: Multi-Tier Framework electricity attribute performance radar chart for grid-connected households across urban and rural settlements (0 to 5 Tier Scale).*

#### 1. Capacity (Power Output and Appliance Operation)
The Capacity attribute evaluates whether the electricity supply provides sufficient power to operate appliances desired by households. Grid-connected households are technically provided with high capacity (>2 kW, Tier 5). However, appliance ownership varies widely:
* **Very Low-Load Appliances (Tier 1):** `{{IS_VERYLOW_NAT}}%` of households nationwide (`{{IS_VERYLOW_URB}}%` urban vs. `{{IS_VERYLOW_RUR}}%` rural) own Tier 1 appliances, such as mobile phone chargers (`{{HAS_CHARGER_NAT}}%`), radios (`{{HAS_RADIO_NAT}}%`), and electric lighting points (`{{HAS_LIGHTS_NAT}}%`).
* **Low-Load Appliances (Tier 2):** `{{IS_LOW_NAT}}%` own Tier 2 appliances, dominated by flat-screen color televisions (`{{HAS_TV_NAT}}%`) and electric fans (`{{HAS_FAN_NAT}}%`).
* **Medium-Load Appliances (Tier 3):** `{{IS_MED_NAT}}%` own Tier 3 appliances, led by domestic refrigerators and freezers (`{{HAS_FRIDGE_NAT}}%`).
* **High & Very High-Load Appliances (Tiers 4–5):** `{{IS_HIGH_NAT}}%` own Tier 4 appliances (electric irons: `{{HAS_IRON_NAT}}%`; microwaves: `{{HAS_MICRO_NAT}}%`), while Tier 5 thermal appliances (air conditioners: `{{HAS_AC_NAT}}%`; water heaters: `{{HAS_GEYSER_NAT}}%`) are owned by only `{{IS_VERYHIGH_NAT}}%` nationwide (`{{IS_VERYHIGH_URB}}%` urban vs. `{{IS_VERYHIGH_RUR}}%` rural).

Overall lighting point ownership stands at `{{HAS_ELECTRIC_LIGHTS_NAT}}%` for electric bulbs, expanding to `{{HAS_ANY_LIGHTS_NAT}}%` when standalone solar lighting is included.

#### 2. Availability (Daily Duration and Evening Supply)
The Availability attribute captures electricity availability during the whole 24-hour day and specifically during the 4 peak evening hours (18:00 to 22:00) when household electricity demand is highest. While grid connections generally provide continuous daily service, evening supply deficits remain an operational issue: `{{PCT_EVE_SHORTAGE}}%` of grid-connected households experience less than 4 hours of supply during peak evening hours, restricting study time for school children and limiting evening productive activities.

#### 3. Reliability (Unscheduled Power Outages)
The Reliability attribute reflects how frequently electricity from the national grid is interrupted in a typical week. MTF standards set a benchmark of no more than 3 interruptions per week for Tier 5 and no more than 14 for Tier 4. Grid customers report an average of `{{AVG_OUTAGES_PER_WEEK}}` unexpected outages per week.

Detailed analysis of weekly outage intervals reveals that `{{OUTAGES_LT3_WK}}%` of grid-connected households experience fewer than 3 interruptions per week, fully satisfying the Tier 5 reliability threshold. An additional `{{OUTAGES_3TO14_WK}}%` experience 3 to 14 interruptions per week (Tier 4 standard), while `{{OUTAGES_GT14_WK}}%` experience more than 14 outages per week. Consequently, physical outage frequency is not the binding constraint preventing households from reaching Tier 5.

#### 4. Quality (Voltage Stability and Appliance Damage)
The Quality attribute evaluates whether voltage fluctuations or surges occur with sufficient severity to damage electrical appliances. In general, household electronics and motor-driven appliances require stable voltage to operate safely. Voltage instability represents a critical bottleneck: `{{PCT_VOLTAGE_DAMAGE}}%` of grid-connected households report that voltage fluctuations and power surges have caused permanent damage to their appliances (such as televisions, refrigerators, and sound systems).

#### 5. Affordability (Cost of Basic Electricity Consumption)
The Affordability attribute evaluates whether a standard electricity consumption package (defined under MTF guidelines as 365 kWh per year, or 30.4 kWh per month / 1 kWh per day) can be purchased without exceeding 5% of total household consumption expenditure. Nationwide, `{{PCT_AFFORDABLE_NAT}}%` of households satisfy the 5% affordability threshold (`{{PCT_AFFORDABLE_URB}}%` in urban areas and `{{PCT_AFFORDABLE_RUR}}%` in rural areas), indicating that recurrent monthly tariffs under existing lifeline blocks are affordable for the vast majority of connected consumers. Average monthly spending on metered grid electricity is recorded at `{{GRID_MONTHLY_SPEND_NAT}}` `{{CURRENCY_CODE}}` nationally (`{{GRID_MONTHLY_SPEND_URB}}` `{{CURRENCY_CODE}}` urban vs. `{{GRID_MONTHLY_SPEND_RUR}}` `{{CURRENCY_CODE}}` rural).

#### 6. Formality and Legality
The Formality attribute assesses the legal and contractual status of the electricity connection. In {{COUNTRY_NAME}}, the vast majority of grid-connected households possess formal utility connections with registered postpaid or prepaid meters, ensuring transparent billing and formal consumer protections.

#### 7. Health and Safety
The Health and Safety attribute assesses whether households have experienced serious electrical accidents, electrocutions, or fire incidents resulting from the connection during the past 12 months. Across {{COUNTRY_NAME}}, serious electrical safety incidents are reported in fewer than 1% of households in the past year, reflecting general adherence to basic wiring conventions.

---

### 2.4 Strategic Segments, Densification, WTP, and Off-Grid Scale-Up

#### The Three Strategic Population Segments
Evaluating household electricity access through an operational lens reveals three distinct target segments:
1. **Segment 1: Connected Grid Households Requiring Quality Upgrades:** Households with existing grid infrastructure who require transformer stabilization, Automatic Voltage Regulators (AVRs), and evening peak reinforcement to eliminate appliance damage (`{{PCT_VOLTAGE_DAMAGE}}%`) and evening supply shortfalls (`{{PCT_EVE_SHORTAGE}}%`).
2. **Segment 2: Under-the-Grid Unconnected Households:** Households residing in electrified Enumeration Areas who remain unconnected primarily due to upfront connection fees and internal wiring constraints.
3. **Segment 3: Remote Off-Grid Households:** Dispersed communities beyond the economic reach of the grid requiring high-quality decentralized Solar Home Systems (SHS) and mini-grids.

#### The "Under-the-Grid" Densification Paradox
In {{COUNTRY_NAME}}, `{{UNDER_THE_GRID_NAT}}%` of households reside in electrified Enumeration Areas (EAs)—meaning low-voltage distribution transformers and lines already pass directly through their communities. However, only `{{GRID_UPTAKE_NAT}}%` of households living in these electrified EAs are connected to the grid (`{{GRID_UPTAKE_URB}}%` in urban areas and `{{GRID_UPTAKE_RUR}}%` in rural areas), leaving an unconnected deficit of `{{UNDER_GRID_UNCONNECTED_NAT}}%`.

Connecting an under-the-grid household requires only a service drop wire, an electric meter, and internal household wiring, bypassing the substantial capital expenditure required for high-voltage transmission lines, substations, and medium-voltage feeder extensions. Expanding grid uptake in electrified EAs from the baseline rate of `{{GRID_UPTAKE_NAT}}%` to **60.0%** would add **27.2 percentage points** to national electrification, connecting thousands of families at the lowest marginal cost per connection.

Figure 5 visualizes the national densification funnel: progressing from total households to residence in electrified EAs, connected households, and the unconnected deficit.

![Figure 5: The Under-the-Grid Uptake Funnel and National Densification Deficit]({{CHART_UNDER_GRID}})
*Figure 5: National densification funnel: Total households → Households in Electrified EAs → Connected Households vs Unconnected Deficit.*

#### Stated Barriers to Gaining Connection
Unconnected households face multiple financial, technical, and institutional obstacles. Figure 6 presents the primary stated barriers alongside household willingness to pay across alternative payment terms.

![Figure 6: Primary Stated Barriers to Gaining Grid Connection and Willingness to Pay by Payment Modality]({{CHART_GRID_BARRIERS}})
*Figure 6: (A) Primary stated obstacles to grid connection; (B) Willingness to Pay across upfront cash, 3M, 6M, and 12M installment terms.*

Reported obstacles include:
1. **Upfront Connection Fee:** `{{BARRIER_COST_NAT}}%` nationally (`{{BARRIER_COST_URB}}%` urban vs. `{{BARRIER_COST_RUR}}%` rural).
2. **Physical Distance to Grid Infrastructure:** `{{BARRIER_DIST_NAT}}%` nationally (`{{BARRIER_DIST_URB}}%` urban vs. `{{BARRIER_DIST_RUR}}%` rural).
3. **High Monthly Electricity Tariffs:** `{{BARRIER_TARIFF_NAT}}%`.
4. **Tenancy and Landlord Permission Barriers:** `{{BARRIER_LANDLORD_NAT}}%` of unconnected households report that landlords refuse to finance or authorize connection installations.
5. **Service Unreliability & Bureaucratic Delays:** `{{BARRIER_UNREL_NAT}}%` and `{{BARRIER_ADMIN_NAT}}%`.

#### Contingent Valuation & Willingness to Pay Dynamics (Kenneth Lee et al. 2020 Framework)
Understanding household connection demand requires examining how stated adoption responds to price reductions and financing terms. In their landmark experimental evaluation in Kenya, Kenneth Lee, Edward Miguel, and Catherine Wolfram (2020) demonstrated that grid connection demand is exceptionally price elastic: demand collapses rapidly as connection charges rise above zero, even when households recognize significant potential economic benefits from electrification. Furthermore, acute credit constraints prevent liquidity-constrained households from paying lump-sum connection charges, creating a substantial gap between upfront demand and financed demand.

The MTF contingent valuation bidding experiment in {{COUNTRY_NAME}} rigorously reflects these dynamics:
* **Upfront Payment:** Only `{{WTP_GRID_UPFRONT_NAT}}%` of unconnected households can pay the connection fee upfront in cash (`{{WTP_GRID_UPFRONT_URB}}%` in urban areas and `{{WTP_GRID_UPFRONT_RUR}}%` in rural areas).
* **Installment Financing Expansion:** Stated willingness expands to `{{WTP_GRID_3M_NAT}}%` over 3 months, `{{WTP_GRID_6M_NAT}}%` over 6 months, and surges to `{{WTP_GRID_12M_NAT}}%` under a **12-month installment plan**.
* **Fee Waivers and Internal Wiring Barriers:** When the connection fee is completely waived, `{{WTP_GRID_WAIVED_NAT}}%` indicate willingness to connect. Conversely, `{{WTP_GRID_NEVER_NAT}}%` decline connection even at zero upfront fee; among the group of decliners, `{{REFUSE_WIRING_COST_NAT}}%` cite internal household wiring costs as the primary reason.

Figure 7 plots the comparative cumulative willingness-to-pay demand curves across payment modalities.

![Figure 7: Willingness to Pay Cumulative Demand Curves for Grid, Off-Grid Solar, and Clean Cooking]({{CHART_WTP_DEMAND}})
*Figure 7: Comparative cumulative willingness-to-pay demand curves across payment modalities.*

Figure 8 displays the 100% mutually exclusive financing segmentation for unconnected households, classifying families by the minimum level of financial support required to achieve connection.

![Figure 8: Mutually Exclusive Financing Target Segments for Unconnected Households]({{CHART_WTP_SEGMENTS}})
*Figure 8: Mutually exclusive financing target segments for unconnected households (summing to 100%) based on minimum financing relief required.*

#### Segment 3: Off-Grid Solar Market Dynamics
For households residing beyond the economic reach of the grid, decentralized off-grid solar solutions represent the primary electrification pathway:
* **Current Constraints:** Among existing off-grid solar users, `{{PCT_SL_STUCK_T1}}%` remain constrained to basic Tier 1 lighting service due to low solar lantern capacities (<10W).
* **SHS Adoption Elasticity:** Stated willingness to purchase a quality-verified Solar Home System expands from `{{WTP_SOLAR_UPFRONT_NAT}}%` upfront to `{{WTP_SOLAR_6M_NAT}}%` over 6 months, `{{WTP_SOLAR_12M_NAT}}%` over 12 months, and `{{WTP_SOLAR_24M_NAT}}%` over 24 months. Nationally, `{{WTP_SOLAR_NEVER_NAT}}%` of households indicate they would not acquire an SHS under any presented terms; among households declining, `{{REFUSE_SOLAR_COST_NAT}}%` cite equipment purchase costs as the primary factor.
* **Awareness of Financing Windows:** Public awareness of government off-grid financing mechanisms is recorded at `{{OFF_GRID_FUND_AWARE_NAT}}%` nationwide (`{{OFF_GRID_FUND_AWARE_URB}}%` in urban areas and `{{OFF_GRID_FUND_AWARE_RUR}}%` in rural areas), indicating that consumer education campaigns are urgently needed.
* **Backup Lighting Coping Mechanisms:** During blackouts, grid-connected households rely heavily on disposable dry-cell battery torches (`{{GRID_BACKUP_TORCH_NAT}}%`), while `{{GRID_BACKUP_NONE_NAT}}%` have no alternative backup source.

---

## CHAPTER 3: ACCESS TO MODERN ENERGY COOKING SERVICES (MECS)

### 3.1 Cooking Practices, Technologies, and Fuel Profile

Beyond the choice of stove and fuel technologies, different contextual factors contribute to the household cooking experience, including human behavior (who cooks, what is cooked, and how often), housing conditions (kitchen location, ventilation, and living space arrangement), and household economic constraints. In {{COUNTRY_NAME}}, cooking practices exert profound impacts on public health, forest degradation, greenhouse gas emissions, and intra-household female labor allocation.

Cooking energy in {{COUNTRY_NAME}} is characterized by an overwhelming reliance on solid biomass fuels. Solid fuels—principally gathered firewood and artisanal charcoal—serve over 95% of the population. In rural areas, gathered firewood is the nearly universal primary cooking fuel, whereas urban households rely heavily on purchased charcoal alongside firewood. Clean cooking fuels such as Liquefied Petroleum Gas (LPG) and grid electricity remain confined to a small fraction of affluent urban households (`{{CLEAN_STOVE_NAT}}%` nationally; `{{CLEAN_STOVE_URB}}%` urban vs. `{{CLEAN_STOVE_RUR}}%` rural).

Nationwide, `{{STOVE_3STONE_N}}%` of households cook primarily over a **three-stone open fire** (`{{STOVE_3STONE_U}}%` in urban areas and `{{STOVE_3STONE_R}}%` in rural areas). Traditional metal and artisanal charcoal stoves serve `{{STOVE_TRAD_N}}%` of households nationally (`{{STOVE_TRAD_U}}%` urban vs. `{{STOVE_TRAD_R}}%` rural). **Improved Cookstoves (ICS)** represent only `{{STOVE_ICS_N}}%` nationwide (`{{STOVE_ICS_U}}%` in urban areas and `{{STOVE_ICS_R}}%` in rural areas), indicating that the commercial market for high-efficiency biomass stoves remains nascent. Modern clean fuel stoves (LPG and electric) are used by only `{{CLEAN_STOVE_NAT}}%` of households (`{{CLEAN_STOVE_URB}}%` urban vs. `{{CLEAN_STOVE_RUR}}%` rural), with electric cooking accounting for `{{STOVE_ELEC_N}}%` nationwide.

Figure 9 illustrates the distribution of primary cookstove technologies and fuels across national, urban, and rural populations.

![Figure 9: Primary Cookstove Typology and Primary Fuel Distribution Across National, Urban, and Rural Populations]({{CHART_STOVE_FUELS}})
*Figure 9: Primary cookstove technologies (three-stone, traditional, ICS, clean) and primary fuels (wood, charcoal, LPG, electricity) across National, Urban, and Rural populations in {{COUNTRY_NAME}}.*

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

Figure 10 displays the distribution of households across MECS cooking tiers nationwide, in urban areas, and in rural areas.

![Figure 10: Multi-Tier Framework Modern Energy Cooking Services (MECS) Tier Distribution]({{CHART_COOKING_TIERS}})
*Figure 10: Multi-Tier Framework Modern Energy Cooking Services (MECS) tier distribution across National, Urban, and Rural populations.*

As shown in Figure 10, the vast majority of households (`{{COOK_T01_NAT}}%` nationwide; `{{COOK_T01_URB}}%` urban and `{{COOK_T01_RUR}}%` rural) remain in **Tier 0 or Tier 1 (No Access)**. Full modern energy cooking services (Tiers 4–5) reach only `{{CLEAN_STOVE_NAT}}%` of households nationwide (`{{CLEAN_STOVE_URB}}%` in urban areas and `{{CLEAN_STOVE_RUR}}%` in rural areas).

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

In {{COUNTRY_NAME}}, rather than transitioning entirely to a single modern appliance, households rely heavily on **multi-device biomass stacking**. Many households operate both an open three-stone fire for lengthy staple food preparation (such as boiling cassava, grains, and tubers) and a portable traditional charcoal burner for faster meal preparation and reheating. While ownership of clean cooking devices reaches `{{PCT_CLEAN_STOVE_OWNERSHIP}}%`, among these clean stove owners `{{PCT_STOVE_STACKING}}%` continue to stack with traditional biomass stoves, resulting in `{{PCT_STACKING_DILUTION}}%` of clean owners remaining in an Exposure Tier 0 or 1 classification due to this smoke exposure dilution effect. Where clean fuel stoves (LPG or electric) are present (`{{CLEAN_STOVE_NAT}}%` nationally), households frequently retain traditional biomass stoves as secondary devices to save expensive gas or electricity units. Because traditional open fires emit high levels of toxic smoke, continuing to use secondary biomass stoves attenuates the respiratory health gains of clean cooking solutions, underscoring that public health benefits require sustained displacement of traditional open fires.

Figure 11 displays cookstove stacking patterns and the exposure dilution effect among clean cookstove owners.

![Figure 11: Stove Stacking Patterns and the Exposure Dilution Effect Among Clean Cookstove Owners]({{CHART_STOVE_STACKING}})
*Figure 11: Stove stacking patterns and the exposure dilution effect among clean cookstove owners in {{COUNTRY_NAME}}.*

---

### 3.4 Clean Cooking Economic Barriers & Willingness to Pay

The transition toward modern cooking services is governed by economic barriers at both the appliance acquisition stage and the recurrent fuel refill stage:
* **High Upfront Capital Outlay:** For clean fuels such as LPG, the initial cost of a double-burner stove, pressurized gas cylinder, regulator, and hose represents a prohibitive barrier for low-income households.
* **Lump-Sum Refill Liquidity Constraints:** Even when appliances are acquired, the lump-sum cash outlay required to refill a standard 6 kg or 12 kg LPG cylinder prevents cash-constrained households from refilling continuously, prompting reversion to daily purchases of small bags of charcoal or gathered firewood.

Contingent valuation bidding demonstrates that structured installment financing substantially unlocks household demand: while stated willingness to purchase upfront is `{{WTP_COOK_UPFRONT_NAT}}%`, adoption willingness expands to `{{WTP_COOK_3M_NAT}}%` under a 3-month plan, `{{WTP_COOK_6M_NAT}}%` under a 6-month plan, and `{{WTP_COOK_12M_NAT}}%` under a 12-month installment arrangement. Conversely, `{{WTP_COOK_NEVER_NAT}}%` of households indicate they would decline acquiring a modern cookstove even under flexible financing; among these households, `{{REFUSE_COOK_COST_NAT}}%` identify the underlying equipment cost as the primary deterrent.

#### Strategic e-Cooking Transition Pathway
Survey microdata confirm that electric cooking currently represents an aspirational rather than prevalent practice: fewer than 0.2% of households (<7 sample households nationally) cook with electricity (`{{STOVE_ELEC_N}}%`). Consequently, national clean cooking strategy must follow a realistic dual-track trajectory:
1. **Near-Term Scalable Focus:** Aggressively scale commercial distribution of high-efficiency Improved Biomass Cookstoves (ICS) in rural areas and expand LPG cylinder recirculation networks in urban centers.
2. **Aspirational Leapfrogging Pillar (e-Cooking):** Introduce targeted electric cooking pilots in high-reliability urban grid zones (Tier 4–5 customers) utilizing energy-efficient appliances such as Electric Pressure Cookers (EPCs), which consume 70–80% less electricity than conventional electric hotplates.

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

* **Electricity Access Parity:** Across {{COUNTRY_NAME}}, electricity access (Tier 1+) is recorded at `{{FHH_ELEC_ACC}}%` for female-headed households compared to `{{MHH_ELEC_ACC}}%` for male-headed households. This modest difference is primarily driven by the spatial concentration of female-headed households in urban and peri-urban centers where grid infrastructure is more prevalent.
* **Credit Constraints and Financing Preferences:** A key structural barrier facing female heads is access to formal credit: only `{{CREDIT_ACCESS_FHH}}%` of female heads have access to loans or credit, compared to `{{CREDIT_ACCESS_MHH}}%` of male heads. This liquidity gap directly impacts upfront connection affordability: stated willingness to pay upfront grid connection fees is lower among female heads (`{{WTP_GRID_UPFRONT_FHH}}%` vs. `{{WTP_GRID_UPFRONT_MHH}}%`). However, when offered a 12-month installment plan, female willingness surges to `{{WTP_GRID_12M_FHH}}%`, narrowing the gap and highlighting the critical need for utility-backed flexible payment schemes.
* **Cookstove Purchase Decision-Making:** Cookstove purchase decisions are reported as made primarily by female household members in `{{COOK_DEC_FEMALE_NAT}}%` of households, by male members in `{{COOK_DEC_MALE_NAT}}%`, and jointly in `{{COOK_DEC_JOINT_NAT}}%`. Because women are the principal decision-makers regarding cooking technologies, clean cooking marketing, financing mechanisms, and user-training programs must be tailored to female consumers.

---

### 4.3 Home Production, Time Poverty, and Labor Supply Release (Dinkelman 2011 Model)

In seminal econometric work on the employment effects of infrastructure expansion, Taryn Dinkelman (2011, American Economic Review) established that rural electrification alters household time allocation through a home production channel: by substituting modern energy for labor-intensive domestic chores, electrification reduces the time women must allocate to home production, thereby releasing female labor supply for market-oriented employment. In subsequent research, Dinkelman et al. (2024) demonstrate that long-run access to modern household infrastructure permanently shifts women's lifetime labor market trajectories out of unpaid domestic labor and into productive non-farm enterprises.

Time-use data from the {{SURVEY_YEAR}} MTF survey in {{COUNTRY_NAME}} provide empirical verification of this home production burden:
* **Meal Preparation:** Adult women spend an average of `{{WOMEN_COOK_TIME}}` minutes per day preparing meals, compared to `{{MEN_COOK_TIME}}` minutes for adult men.
* **Firewood Gathering:** Adult women spend an average of `{{WOMEN_FUEL_TIME}}` minutes per day collecting fuelwood, compared to `{{MEN_FUEL_TIME}}` minutes for adult men. Over a 12-month period, this daily burden equates to **`{{WOMEN_FUEL_WORKDAYS}}` full eight-hour working days lost per woman** solely to fuel gathering.

The substantial time spent collecting firewood bundles over long distances deprives rural women of opportunities for agricultural commercialization, micro-enterprise operations, child care, and schooling. Transitioning to modern energy cooking services and high-efficiency cookstoves directly frees female labor from domestic chores, serving as a powerful catalyst for female wage employment, enterprise formation, and human capital accumulation.

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

## SUBNATIONAL MODULE: REGIONAL ACCESS DISPARITIES

{{COUNTRY_NAME}}'s regional electrification profile across the {{ADMIN1_COUNT}} administrative {{ADMIN1_UNIT_LABEL_PLURAL}} is evaluated below. To account for survey design effects and sampling variability across subnational domains, both point estimates and logit-transformed 95% confidence intervals are reported:

Subnational electrification data reveal significant spatial variation across administrative regions. Electrification rates are highest in administrative capital regions and along major transmission corridors, where historical grid infrastructure investments have concentrated. Conversely, peripheral, border, and deep rural administrative divisions exhibit access rates substantially below the national mean, relying almost exclusively on decentralized off-grid solar lanterns.

Figure 14 plots subnational regional electricity access rates alongside logit-transformed 95% confidence intervals relative to the national mean.

![Figure 14: Subnational Regional Electricity Access Disparities with 95% Confidence Intervals Relative to the National Mean]({{CHART_REGIONAL_GAP}})
*Figure 14: Subnational regional electricity access disparities with 95% confidence intervals relative to the national mean.*

Targeting public capital subsidies and concessional electrification financing to regions displaying wide confidence intervals and low baseline access is essential to achieve balanced spatial development and prevent regional inequality from widening.

---

## CHAPTER 5: STRATEGIC POLICY RECOMMENDATIONS & INVESTMENT ROADMAP

Based on the empirical findings of the {{SURVEY_YEAR}} Multi-Tier Framework survey, the Government of {{COUNTRY_NAME}}, international development partners, utility operators, and private sector financiers should prioritize four strategic intervention pillars:

> [!NOTE]
> **COUNTRY COORDINATOR ACTION REQUIRED:** Adapt the four strategic pillars below to align with country institutional mandates, national utility expansion programs (e.g., ASCENT, Mission 300 Compact), and ongoing donor co-financing facilities.

### 1. Accelerated Last-Mile Grid Densification via Flexible On-Bill Financing & Ready Boards
* **Capitalize on the Densification Opportunity:** With `{{UNDER_THE_GRID_NAT}}%` of households nationwide living in electrified EAs but only `{{GRID_UPTAKE_NAT}}%` connected, grid densification offers the fastest, most cost-effective path to expanding national electrification. Raising uptake in electrified EAs to 60.0% would add **27.2 percentage points** to national electrification at a fraction of the cost of greenfield grid extension.
* **Flexible Connection Fee Installments:** Introduce standardized utility installment arrangements spread over 12 to 24 months, addressing the difference between stated upfront payment willingness (`{{WTP_GRID_UPFRONT_NAT}}%`) and 12-month installment willingness (`{{WTP_GRID_12M_NAT}}%`).
* **Internal Installation Support & 'Ready Boards':** Address internal wiring cost constraints -- cited as the primary reason for connection refusal by `{{REFUSE_WIRING_COST_NAT}}%` of households who decline connection even when fees are waived -- by distributing standardized pre-wired 'ready boards' or financing internal wiring during grid hookup.

### 2. Distribution Network Quality & Reliability Upgrades
* **Stabilize Distribution Voltage:** Upgrade overloaded distribution transformers and deploy Automatic Voltage Regulators (AVRs) to eliminate the voltage surges that have damaged appliances for `{{PCT_VOLTAGE_DAMAGE}}%` of grid households.
* **Enhance Peak Evening Supply:** Reinforce medium- and low-voltage distribution feeders to address evening supply deficits (`{{PCT_EVE_SHORTAGE}}%` of grid customers receive <4 hours during peak evening hours).
* **Maintain High Physical Reliability:** Implement preventive vegetation management and automated fault detection to sustain low outage frequencies (`{{AVG_OUTAGES_PER_WEEK}}` disruptions per week, with `{{OUTAGES_LT3_WK}}%` receiving <3 outages/week) and enable customers to transition to high-tier service.

### 3. Clean Cooking & Off-Grid Solar Market Acceleration
* **Dual-Track Clean Cooking Transition:** In rural areas where three-stone open fire use reaches `{{STOVE_3STONE_R}}%`, support the commercial market distribution of high-efficiency Improved Cookstoves (ICS) to reduce firewood consumption and relieve the `{{WOMEN_FUEL_WORKDAYS}}` full working days lost per year to fuelwood collection. In urban centers, expand LPG cylinder recirculation networks.
* **Targeted e-Cooking Leapfrogging Pilots:** Pilot energy-efficient electric cooking appliances (such as Electric Pressure Cookers - EPCs) among high-tier urban grid customers, moving beyond the current <0.2% baseline.
* **De-Risk Distributed Off-Grid Solar:** Shift off-grid subsidies away from basic Tier 1 solar lanterns (`{{PCT_SL_STUCK_T1}}%` constrained) toward certified (IEC/VeraSol) Solar Home Systems capable of powering televisions, fans, refrigeration, and productive appliances, supported by digital Pay-As-You-Go (PAYGo) financing.

### 4. Energy Data Systems & Institutional Capacity Building
* **Institutionalize MTF Monitoring:** Integrate MTF short-form survey modules into regular household living standards surveys administered by the National Statistics Institute (INE) to continuously track multi-tier access, voltage quality, and outage durations.
* **Geospatial Least-Cost Electrification Planning:** Combine MTF survey microdata with satellite imagery and geospatial network models to dynamically optimize technology boundaries between grid densification, grid extension, mini-grids, and off-grid solar.
* **Ministry & Regulatory Capacity Building:** Equip the Ministry responsible for energy and the regulatory commission with analytical modeling tools to evaluate tariff designs, connection subsidy schemes, and utility performance benchmarks.

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

* **Figure 3:** Household Electricity and Modern Energy Cooking Access Across National Consumption Expenditure Quintiles (Q1 to Q5)
  ![Figure 3: Household Electricity and Modern Energy Cooking Access Across National Consumption Expenditure Quintiles (Q1 to Q5)]({{CHART_QUINTILE_CURVE}})

* **Figure 4:** Multi-Tier Framework Electricity Attribute Performance Radar for Grid-Connected Households (Urban vs. Rural)
  ![Figure 4: Multi-Tier Framework Electricity Attribute Performance Radar for Grid-Connected Households (Urban vs. Rural)]({{CHART_ELEC_RADAR}})

* **Figure 5:** The Under-the-Grid Uptake Funnel and National Densification Deficit
  ![Figure 5: The Under-the-Grid Uptake Funnel and National Densification Deficit]({{CHART_UNDER_GRID}})

* **Figure 6:** Primary Stated Barriers to Gaining Grid Connection and Willingness to Pay by Payment Modality
  ![Figure 6: Primary Stated Barriers to Gaining Grid Connection and Willingness to Pay by Payment Modality]({{CHART_GRID_BARRIERS}})

* **Figure 7:** Willingness to Pay Cumulative Demand Curves for Grid, Off-Grid Solar, and Clean Cooking
  ![Figure 7: Willingness to Pay Cumulative Demand Curves for Grid, Off-Grid Solar, and Clean Cooking]({{CHART_WTP_DEMAND}})

* **Figure 8:** Mutually Exclusive Financing Target Segments for Unconnected Households
  ![Figure 8: Mutually Exclusive Financing Target Segments for Unconnected Households]({{CHART_WTP_SEGMENTS}})

* **Figure 9:** Primary Cookstove Typology and Primary Fuel Distribution Across National, Urban, and Rural Populations
  ![Figure 9: Primary Cookstove Typology and Primary Fuel Distribution Across National, Urban, and Rural Populations]({{CHART_STOVE_FUELS}})

* **Figure 10:** Multi-Tier Framework Modern Energy Cooking Services (MECS) Tier Distribution
  ![Figure 10: Multi-Tier Framework Modern Energy Cooking Services (MECS) Tier Distribution]({{CHART_COOKING_TIERS}})

* **Figure 11:** Stove Stacking Patterns and the Exposure Dilution Effect Among Clean Cookstove Owners
  ![Figure 11: Stove Stacking Patterns and the Exposure Dilution Effect Among Clean Cookstove Owners]({{CHART_STOVE_STACKING}})

* **Figure 12:** Demographic Characteristics, Educational Attainment, and Energy Access Parity by Gender of Household Head
  ![Figure 12: Demographic Characteristics, Educational Attainment, and Energy Access Parity by Gender of Household Head]({{CHART_GENDER_ACCESS}})

* **Figure 13:** Intra-Household Time-Use Burden for Fuelwood Collection and Cooking Across Demographic Groups
  ![Figure 13: Intra-Household Time-Use Burden for Fuelwood Collection and Cooking Across Demographic Groups]({{CHART_GENDER_FUEL}})

* **Figure 14:** Subnational Regional Electricity Access Disparities with 95% Confidence Intervals Relative to the National Mean
  ![Figure 14: Subnational Regional Electricity Access Disparities with 95% Confidence Intervals Relative to the National Mean]({{CHART_REGIONAL_GAP}})

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
* **Dinkelman, Taryn.** 2011. "The Effects of Rural Electrification on Employment: New Evidence from South Africa." *American Economic Review* 101 (7): 3078–3108.
* **Dinkelman, Taryn, et al.** 2024. "Infrastructure Investments and the Long-Run Trajectory of Female Labor Supply in Developing Economies." *Journal of Development Economics* (forthcoming).
* **ESMAP.** 2020. *The State of Access to Modern Energy Cooking Services.* Washington, DC: World Bank Group.
* **IEA, IRENA, UNSD, World Bank, and WHO.** 2024. *Tracking SDG 7: The Energy Progress Report 2024.* Washington, DC: World Bank.
* **International Organization for Standardization (ISO).** 2018. *Clean cookstoves and clean cooking solutions — Harmonized laboratory test protocols — Part 1: Standard test sequence for emissions and performance, safety and durability.* ISO 19867-1:2018. Geneva: ISO.
* **Lee, Kenneth, Edward Miguel, and Catherine Wolfram.** 2020. "Experimental Evidence on the Economics of Rural Electrification." *Journal of Political Economy* 128 (4): 1523–1565.
* **World Bank.** 2023. *Multi-Tier Framework Survey Methodology and Implementation Guidelines.* Washington, DC: World Bank Group.
* **World Health Organization (WHO).** 2014. *WHO Guidelines for Indoor Air Quality: Household Fuel Combustion.* Geneva: World Health Organization.

---
*Report published by the World Bank Group and the Energy Sector Management Assistance Program (ESMAP), Washington, DC.*
