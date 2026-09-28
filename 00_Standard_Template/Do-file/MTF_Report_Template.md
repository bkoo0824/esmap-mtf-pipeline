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
{{COUNTRY_NAME}}               : Full official name of client country (e.g. Liberia, Rwanda)
{{SURVEY_YEAR}}                : Survey implementation / fieldwork year (e.g. 2024)
{{CURRENCY_CODE}}              : ISO 3-letter local currency code (e.g. LRD, NAD, USD)
{{ADMIN1_COUNT}}               : Total count of Admin 1 subnational divisions (e.g. 15, 14)
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
{{CLEAN_STOVE_NAT}}            : Primary stove clean fuels (LPG/Electric) nationwide (%) [JSON: CLEAN_STOVE_NAT]
{{CLEAN_STOVE_URB}}            : Primary stove clean fuels (LPG/Electric) urban (%) [JSON: CLEAN_STOVE_URB]
{{CLEAN_STOVE_RUR}}            : Primary stove clean fuels (LPG/Electric) rural (%) [JSON: CLEAN_STOVE_RUR]
{{THREESTONE_NAT}}             : Primary stove three-stone fire / open flame nationwide (%) [JSON: THREESTONE_NAT]
{{THREESTONE_URB}}             : Primary stove three-stone fire / open flame urban (%) [JSON: THREESTONE_URB]
{{THREESTONE_RUR}}             : Primary stove three-stone fire / open flame rural (%) [JSON: THREESTONE_RUR]
{{UNDER_GRID_UNCONNECTED_NAT}} : Households in electrified EAs without connection nationwide (%) [JSON: UNDER_GRID_UNCONNECTED_NAT]
{{UNDER_GRID_UNCONNECTED_URB}} : Households in electrified EAs without connection urban (%) [JSON: UNDER_GRID_UNCONNECTED_URB]
{{UNDER_GRID_UNCONNECTED_RUR}} : Households in electrified EAs without connection rural (%) [JSON: UNDER_GRID_UNCONNECTED_RUR]
{{GRID_UPTAKE_NAT}}            : Grid connection uptake rate in electrified EAs nationwide (%) [JSON: GRID_UPTAKE_NAT]
{{GRID_UPTAKE_URB}}            : Grid connection uptake rate in electrified EAs urban (%) [JSON: GRID_UPTAKE_URB]
{{GRID_UPTAKE_RUR}}            : Grid connection uptake rate in electrified EAs rural (%) [JSON: GRID_UPTAKE_RUR]
{{AVG_OUTAGES_PER_WEEK}}       : Average weekly unexpected power outages for grid users [JSON: AVG_OUTAGES_PER_WEEK]
{{PCT_VOLTAGE_DAMAGE}}         : Grid households reporting appliance voltage surge damage (%) [JSON: PCT_VOLTAGE_DAMAGE]
{{PCT_EVE_SHORTAGE}}           : Grid households with evening supply deficit (<4h) (%) [JSON: PCT_EVE_SHORTAGE]
{{BARRIER_COST_NAT}}           : Primary barrier: upfront connection fee too high (%) [JSON: BARRIER_COST_NAT]
{{BARRIER_DIST_NAT}}           : Primary barrier: distance to low-voltage network (%) [JSON: BARRIER_DIST_NAT]
{{WTP_GRID_UPFRONT_NAT}}       : Stated WTP for grid connection upfront nationwide (%) [JSON: WTP_GRID_UPFRONT_NAT]
{{WTP_GRID_12M_NAT}}           : Stated WTP for grid connection over 12 months nationwide (%) [JSON: WTP_GRID_12M_NAT]
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
{{FHH_SHARE}}                  : Share of female-headed households nationwide (%) [Stata/JSON: FHH_SHARE]
{{HEAD_AGE_FHH}}               : Average age of female household heads (years) [JSON: HEAD_AGE_FHH]
{{HEAD_AGE_MHH}}               : Average age of male household heads (years) [JSON: HEAD_AGE_MHH]
{{HEAD_MARITAL_WIDOW_FHH}}     : Widowed rate among female household heads (%) [JSON: HEAD_MARITAL_WIDOW_FHH]
{{HEAD_MARITAL_WIDOW_MHH}}     : Widowed rate among male household heads (%) [JSON: HEAD_MARITAL_WIDOW_MHH]
{{WTP_GRID_UPFRONT_FHH}}       : Upfront grid connection WTP among female-headed HHs (%) [JSON: WTP_GRID_UPFRONT_FHH]
{{WTP_GRID_UPFRONT_MHH}}       : Upfront grid connection WTP among male-headed HHs (%) [JSON: WTP_GRID_UPFRONT_MHH]
{{WTP_GRID_12M_FHH}}           : 12-month installment grid WTP among female-headed HHs (%) [JSON: WTP_GRID_12M_FHH]
{{COOK_DEC_FEMALE_NAT}}        : Cookstove purchase decisions made by female members (%) [JSON: COOK_DEC_FEMALE_NAT]
{{COOK_DEC_MALE_NAT}}          : Cookstove purchase decisions made by male members (%) [JSON: COOK_DEC_MALE_NAT]
{{COOK_DEC_JOINT_NAT}}         : Cookstove purchase decisions made jointly (%) [JSON: COOK_DEC_JOINT_NAT]
{{WOMEN_COOK_TIME}}            : Mean daily cooking time for adult women (minutes/day) [JSON: WOMEN_COOK_TIME]
{{MEN_COOK_TIME}}              : Mean daily cooking time for adult men (minutes/day) [JSON: MEN_COOK_TIME]
{{WOMEN_FUEL_TIME}}            : Mean daily fuelwood gathering time for adult women (min/day) [JSON: WOMEN_FUEL_TIME]
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
{{STOVE_SOLAR_N/U/R}}                         : Solar cooker adoption National, Urban, Rural (%) [Stata/Fallback: STOVE_SOLAR_N / U / R]
{{STOVE_BIO_N/U/R}}                           : Biogas dedicated stove adoption National, Urban, Rural (%) [Stata/Fallback: STOVE_BIO_N / U / R]
{{STOVE_BIOFUEL_N/U/R}}                       : Biofuel / ethanol stove adoption National, Urban, Rural (%) [Stata/Fallback: STOVE_BIOFUEL_N / U / R]
{{STOVE_OTHER_N/U/R}}                         : Other / unspecified stove adoption National, Urban, Rural (%) [Stata/Fallback: STOVE_OTHER_N / U / R]

--------------------------------------------------------------------------------
6. CHAPTER 4: GENDER ANALYSIS & TABLE 4.1 PLACEHOLDERS
--------------------------------------------------------------------------------
{{MHH_SHARE}} / {{FHH_SHARE}}                  : Share of male / female-headed households (%) [Target Stata scalar: MHH_SHARE / FHH_SHARE]
{{HEAD_AGE_MHH}} / {{HEAD_AGE_FHH}}           : Average age of male / female head (years) [JSON: HEAD_AGE_MHH / HEAD_AGE_FHH]
{{HEAD_AGE_NAT}}                              : National average age of household head (years) [Target Stata scalar: HEAD_AGE_NAT]
{{HEAD_EDUC_NONE_MHH/FHH/NAT}}                : Head has no formal education for MHH, FHH, National (%) [JSON: MHH/FHH; Target Stata: NAT]
{{HEAD_EDUC_PRIM_MHH/FHH/NAT}}                : Head completed primary education for MHH, FHH, National (%) [JSON: MHH/FHH; Target Stata: NAT]
{{HEAD_EDUC_SEC_MHH/FHH/NAT}}                 : Head completed secondary education for MHH, FHH, National (%) [JSON: MHH/FHH; Target Stata: NAT]
{{HEAD_EDUC_HIGH_MHH/FHH/NAT}}                : Head completed higher education for MHH, FHH, National (%) [JSON: MHH/FHH; Target Stata: NAT]
{{HEAD_MARITAL_MARRIED_MHH/FHH/NAT}}          : Head is married / cohabiting for MHH, FHH, National (%) [JSON: MHH/FHH; Target Stata: NAT]
{{HEAD_MARITAL_WIDOW_MHH/FHH/NAT}}            : Head is widowed for MHH, FHH, National (%) [JSON: MHH/FHH; Target Stata: NAT]
{{HEAD_MARITAL_SINGLE_MHH/FHH}}               : Head is single / never married for MHH, FHH (%) [JSON: HEAD_MARITAL_SINGLE_MHH/FHH]
{{HEAD_MARITAL_DIVSEP_MHH/FHH}}               : Head is divorced / separated for MHH, FHH (%) [JSON: HEAD_MARITAL_DIVSEP_MHH/FHH]
{{CREDIT_ACCESS_MHH/FHH/NAT}}                 : Head has access to credit/loans for MHH, FHH, National (%) [JSON: MHH/FHH; Target Stata: NAT]
{{MHH_ELEC_ACC}} / {{FHH_ELEC_ACC}}           : Electricity access rate (Tier 1+) for MHH / FHH (%) [JSON: MHH_ELEC_ACC / FHH_ELEC_ACC]
{{MHH_MECS_ACC}} / {{FHH_MECS_ACC}}           : MECS cooking access rate for MHH / FHH (%) [JSON: MHH_MECS_ACC / FHH_MECS_ACC]
{{WTP_GRID_UPFRONT_MHH/FHH}}                  : Grid connection upfront WTP for MHH / FHH (%) [JSON: WTP_GRID_UPFRONT_MHH/FHH]
{{WTP_GRID_12M_MHH/FHH}}                      : Grid connection 12-month installment WTP for MHH / FHH (%) [JSON: WTP_GRID_12M_MHH/FHH]
{{WTP_SOLAR_UPFRONT_MHH/FHH}}                 : Solar Home System upfront WTP for MHH / FHH (%) [JSON: WTP_SOLAR_UPFRONT_MHH/FHH]
{{MEN_FUEL_TIME}}                             : Mean daily fuelwood gathering time for adult men (min/day) [JSON: MEN_FUEL_TIME]

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

<!-- [FILL IN: Country-Specific Acknowledgments
Instructions:
- Acknowledge ESMAP and co-financing facilities (e.g., SREP, GEAPP, OPEC Fund, AfDB, bilateral donors).
- Thank the host government, specifically the Ministry responsible for energy, the national utility, and regional distributors.
- Acknowledge the national bureau of statistics, field supervisors, enumerators, and the surveyed households.
- List the World Bank Task Team Leader(s) (TTLs) and core analytical authors.

Draft Example:
"This Energy Access Diagnostic Report presents the empirical findings of the {{SURVEY_YEAR}} Multi-Tier Framework (MTF) National Household Survey in {{COUNTRY_NAME}}. The World Bank Group and ESMAP express their sincere gratitude to the Government of {{COUNTRY_NAME}}, particularly the [Ministry of Energy], [National Power Utility], and [National Statistics Agency]. The team acknowledges the dedication of the national survey team, enumerators, and the thousands of households who generously shared their time. The report was prepared by a World Bank task team led by [Task Team Leader(s)], with analytical and modeling contributions from [Author Names]."
] -->

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

<!-- [FILL IN: Country-Specific Acronyms
Instructions:
- Insert country-specific power sector institutions, utilities, regulators, and national electrification programs.

Examples:
- [LEC] : Liberia Electricity Corporation (National Electric Utility)
- [RREA] : Rural and Renewable Energy Agency
- [LERC] : Liberia Electricity Regulatory Commission
- [ASCENT] : Accelerating Sustainable and Clean Energy Access Transformation
- [CFL] : Compact Fluorescent Lamp
- [LRD] : Liberian Dollar (Local Currency Unit)
] -->

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

This diagnostic report presents the comprehensive empirical findings of the **{{SURVEY_YEAR}} Multi-Tier Framework National Household Survey** in {{COUNTRY_NAME}}. The survey was administered using Computer-Assisted Personal Interviewing (CAPI) across a nationally representative sample covering all {{ADMIN1_COUNT}} administrative {{ADMIN1_UNIT_LABEL_PLURAL}} and {{STRATA_COUNT}} sampling strata. By evaluating the performance of electricity services across seven technical attributes and assessing cooking practices across six service dimensions, this diagnostic provides policymakers, utility managers, regulatory authorities, and international development financiers with an evidence-based roadmap to accelerate universal access under national electrification initiatives, regional programs such as the Accelerating Sustainable and Clean Energy Access Transformation (ASCENT) facility, and the World Bank / AfDB Mission 300 (M300) Africa Energy Compact.

---

### 2. Access to Electricity Key Findings

* **National Electrification Rate:** Nationwide, `{{ELEC_ACC_NAT}}%` of households have access to electricity at Tier 1 or above, comprising `{{ELEC_ACC_URB}}%` in urban areas and `{{ELEC_ACC_RUR}}%` in rural areas.
* **Technology Conduits:** Electricity access is delivered through two primary technological conduits: the **National Grid**, reaching `{{GRID_ACC_NAT}}%` of households nationwide (`{{GRID_ACC_URB}}%` in urban areas and `{{GRID_ACC_RUR}}%` in rural areas), and **Off-Grid Solar Solutions** (comprising standalone Solar Home Systems, multi-light solar kits, and portable solar lanterns), serving `{{SOLAR_ACC_NAT}}%` of households (`{{SOLAR_ACC_URB}}%` in urban areas and `{{SOLAR_ACC_RUR}}%` in rural areas). Under SDG 7.1.1 monitoring criteria, dry-cell battery torches and flashlights are strictly excluded from modern electricity metrics.
* **Tier Distribution & High Access:** Nationwide, `{{ELEC_T0_NAT}}%` of households remain in **Tier 0** (no access or sub-Tier 1 supply). Among electrified households, `{{ELEC_T45_NAT}}%` achieve **High Electricity Access (Tier 4 or 5)**, with high-tier access standing at `{{ELEC_T45_URB}}%` in urban areas and `{{ELEC_T45_RUR}}%` in rural areas.
* **Grid Performance & Reliability Deficits:** A physical connection to the national grid does not automatically translate into Tier 5 service. Grid-connected households experience an average of `{{AVG_OUTAGES_PER_WEEK}}` unexpected power interruptions per week. Power quality instability represents a severe bottleneck: `{{PCT_VOLTAGE_DAMAGE}}%` of grid-connected households report that voltage fluctuations and surges have permanently damaged electrical appliances. Furthermore, evening supply duration is constrained, with `{{PCT_EVE_SHORTAGE}}%` of grid customers reporting less than 4 hours of supply during peak evening demand hours (18:00 to 22:00).
* **The "Under-the-Grid" Densification Paradox:** A critical finding of the MTF diagnostic is that `{{UNDER_GRID_UNCONNECTED_NAT}}%` of households nationwide reside in electrified Enumeration Areas (EAs) within physical reach of existing low-voltage distribution lines but remain unconnected (`{{UNDER_GRID_UNCONNECTED_URB}}%` in urban areas and `{{UNDER_GRID_UNCONNECTED_RUR}}%` in rural areas). The overall grid connection uptake rate within electrified EAs stands at `{{GRID_UPTAKE_NAT}}%` nationally (`{{GRID_UPTAKE_URB}}%` in urban centers and `{{GRID_UPTAKE_RUR}}%` in rural localities). Last-mile densification represents the fastest and lowest-cost capital investment pathway for expanding national access.
* **Reported Barriers to Connection:** Among unconnected households, reported obstacles to connection include the upfront connection fee (`{{BARRIER_COST_NAT}}%` nationally; `{{BARRIER_COST_URB}}%` urban vs. `{{BARRIER_COST_RUR}}%` rural) and distance from the grid network (`{{BARRIER_DIST_NAT}}%` nationally; `{{BARRIER_DIST_URB}}%` urban vs. `{{BARRIER_DIST_RUR}}%` rural). Monthly electricity tariffs are cited as an obstacle by `{{BARRIER_TARIFF_NAT}}%`, while landlord tenancy constraints account for `{{BARRIER_LANDLORD_NAT}}%`.
* **Willingness to Pay (WTP) and Financing Elasticity:** Contingent valuation bidding experiments reveal that connection uptake is extraordinarily sensitive to payment terms. Among unconnected households, `{{WTP_GRID_UPFRONT_NAT}}%` indicate willingness to pay the connection fee upfront in cash (`{{WTP_GRID_UPFRONT_URB}}%` in urban areas and `{{WTP_GRID_UPFRONT_RUR}}%` in rural areas). Stated willingness expands to `{{WTP_GRID_3M_NAT}}%` under a 3-month plan, `{{WTP_GRID_6M_NAT}}%` under a 6-month plan, and `{{WTP_GRID_12M_NAT}}%` under a **12-month installment plan**. If the connection fee were waived, `{{WTP_GRID_WAIVED_NAT}}%` would connect, while `{{WTP_GRID_NEVER_NAT}}%` indicate they would decline; among this declining group, `{{REFUSE_WIRING_COST_NAT}}%` cite internal household wiring costs as the primary reason.
* **Off-Grid Solar Service Levels:** Standalone off-grid solar solutions provide vital energy access to communities located beyond the reach of the distribution network. Among off-grid solar users, `{{PCT_SL_STUCK_T1}}%` obtain Tier 1 service, reflecting system capacities configured primarily for basic lighting and task applications. Stated willingness to purchase a Solar Home System (SHS) expands from `{{WTP_SOLAR_UPFRONT_NAT}}%` upfront to `{{WTP_SOLAR_12M_NAT}}%` under a 12-month installment plan and `{{WTP_SOLAR_24M_NAT}}%` over 24 months, while `{{REFUSE_SOLAR_COST_NAT}}%` of households declining solar cite high equipment purchase costs.

---

### 3. Access to Modern Energy Cooking Services (MECS) Key Findings

* **Prevalence of Traditional Biomass:** `{{THREESTONE_NAT}}%` of households rely on the **three-stone open fire** as their primary cooking technology (`{{STOVE_3STONE_U}}%` in urban areas and `{{STOVE_3STONE_R}}%` in rural areas). Traditional metal stoves and basic charcoal burners account for `{{STOVE_TRAD_N}}%` nationally, while certified **Improved Cookstoves (ICS)** represent `{{STOVE_ICS_N}}%`.
* **Clean Cooking Adoption:** Clean cooking solutions (LPG and electric stoves) serve `{{CLEAN_STOVE_NAT}}%` of households nationwide (`{{CLEAN_STOVE_URB}}%` in urban areas vs. `{{CLEAN_STOVE_RUR}}%` in rural areas). Electric stoves represent `{{STOVE_ELEC_N}}%` of primary cooking nationwide (`{{STOVE_ELEC_U}}%` urban vs. `{{STOVE_ELEC_R}}%` rural).
* **MECS Tier Distribution:** Nationwide, `{{MECS_ACC_NAT}}%` of households meet the technical definition for Modern Energy Cooking Services (Tier 1 or above), with `{{COOK_T0_NAT}}%` in Tier 0. High-tier cooking service (Tiers 4-5) stands at `{{COOK_T5_URB}}%` in urban areas and `{{COOK_T5_RUR}}%` in rural areas, while transitional cooking (Tiers 2-3) reaches `{{TRANS_COOK_NAT}}%` nationally (`{{TRANS_COOK_URB}}%` urban and `{{TRANS_COOK_RUR}}%` rural).
* **Stove Stacking & Exposure Dilution:** While `{{PCT_CLEAN_STOVE_OWNERSHIP}}%` of households own clean cooking appliances, `{{PCT_STOVE_STACKING}}%` report concurrent use of multiple cookstoves and fuels (**stove stacking**); among clean stove owners, `{{PCT_STACKING_DILUTION}}%` remain in Exposure Tiers 0-1 due to the continued use of secondary biomass devices for long-duration boiling.

---

### 4. Gender Disparities and Intra-Household Drudgery

* **Demographic Differences:** Female-headed households (FHH) comprise `{{FHH_SHARE}}%` of households nationwide, while male-headed households (MHH) represent `{{MHH_SHARE}}%`. Female household heads average `{{HEAD_AGE_FHH}}` years of age, compared to `{{HEAD_AGE_MHH}}` years for male heads; `{{HEAD_MARITAL_WIDOW_FHH}}%` of female heads are widowed, compared to `{{HEAD_MARITAL_WIDOW_MHH}}%` of male heads.
* **Connection Financing & Credit Access:** Stated willingness to pay upfront grid connection fees is `{{WTP_GRID_UPFRONT_FHH}}%` for female-headed households and `{{WTP_GRID_UPFRONT_MHH}}%` for male-headed households, expanding to `{{WTP_GRID_12M_FHH}}%` and `{{WTP_GRID_12M_MHH}}%` respectively under a 12-month installment plan. Access to credit from formal financial institutions is reported by `{{CREDIT_ACCESS_FHH}}%` of female heads, compared to `{{CREDIT_ACCESS_MHH}}%` of male heads.
* **Cookstove Purchase Decision-Making:** Cookstove purchase decisions are reported as made primarily by female household members in `{{COOK_DEC_FEMALE_NAT}}%` of households, by male members in `{{COOK_DEC_MALE_NAT}}%`, and jointly in `{{COOK_DEC_JOINT_NAT}}%`.
* **Time Allocation for Domestic Energy:** Adult women spend an average of `{{WOMEN_COOK_TIME}}` minutes per day cooking (compared to `{{MEN_COOK_TIME}}` minutes for adult men) and `{{WOMEN_FUEL_TIME}}` minutes per day collecting fuel (compared to `{{MEN_FUEL_TIME}}` minutes for men), equating to **`{{WOMEN_FUEL_WORKDAYS}}` eight-hour working day equivalents per year** for fuel collection.

---

### Table 1.1: National MTF Executive Summary Dashboard

| Energy Access Dimension / Metric | Nationwide (%) | Urban (%) | Rural (%) | Primary Bottleneck / Policy Driver |
| :--- | :---: | :---: | :---: | :--- |
| **Electricity Access Rate (Tier 1-5)** | `{{ELEC_ACC_NAT}}` | `{{ELEC_ACC_URB}}` | `{{ELEC_ACC_RUR}}` | Basic tier 1 lighting threshold |
| **Electricity Tier 0 (No Access / Minimal)** | `{{ELEC_T0_NAT}}` | `{{ELEC_T0_URB}}` | `{{ELEC_T0_RUR}}` | Infrastructure coverage & connection fees |
| **High Electricity Access (Tier 4 & 5)** | `{{ELEC_T45_NAT}}` | `{{ELEC_T45_URB}}` | `{{ELEC_T45_RUR}}` | Voltage stability & evening duration deficits |
| **Main Electricity Source: National Grid** | `{{GRID_ACC_NAT}}` | `{{GRID_ACC_URB}}` | `{{GRID_ACC_RUR}}` | Grid network reach & utility densification |
| **Main Electricity Source: Off-Grid Solar** | `{{SOLAR_ACC_NAT}}` | `{{SOLAR_ACC_URB}}` | `{{SOLAR_ACC_RUR}}` | Stand-alone SHS & solar lantern adoption |
| **Modern Energy Cooking Services (MECS: Tier 1-5)** | `{{MECS_ACC_NAT}}` | `{{MECS_ACC_URB}}` | `{{MECS_ACC_RUR}}` | Clean fuel access & stove efficiency |
| **Transition Cooking Services (Tier 2-3)** | `{{TRANS_COOK_NAT}}` | `{{TRANS_COOK_URB}}` | `{{TRANS_COOK_RUR}}` | Improved Cookstove (ICS) adoption |
| **Cooking Tier 0 (Unimproved / High Exposure)** | `{{COOK_T0_NAT}}` | `{{COOK_T0_URB}}` | `{{COOK_T0_RUR}}` | Open fire cooking with poor ventilation |
| **Primary Stove: Clean Fuels (LPG/Electric)** | `{{CLEAN_STOVE_NAT}}` | `{{CLEAN_STOVE_URB}}` | `{{CLEAN_STOVE_RUR}}` | Urban grid tariffs & LPG supply chain |
| **Primary Stove: Three-Stone / Open Fire** | `{{THREESTONE_NAT}}` | `{{THREESTONE_URB}}` | `{{THREESTONE_RUR}}` | Rural biomass reliance & free gathering |
| **Under-the-Grid Unconnected Rate** | `{{UNDER_GRID_UNCONNECTED_NAT}}` | `{{UNDER_GRID_UNCONNECTED_URB}}` | `{{UNDER_GRID_UNCONNECTED_RUR}}` | Connection fee & internal wiring barrier |
| **Grid Uptake Rate in Electrified EAs** | `{{GRID_UPTAKE_NAT}}` | `{{GRID_UPTAKE_URB}}` | `{{GRID_UPTAKE_RUR}}` | Connection affordability in grid zones |

---

## CHAPTER 1: MEASURING ENERGY ACCESS IN {{COUNTRY_NAME}}

### 1.1 Country Context and Energy Sector Architecture

Modern energy services underpin macroeconomic resilience, agricultural productivity, educational outcomes, public healthcare delivery, and gender equality. In {{COUNTRY_NAME}}, expanding access to reliable and affordable power has been placed at the center of the national development agenda. However, power sector expansion takes place within a challenging physical and macroeconomic environment characterized by geographic dispersal, capital investment deficits, transmission bottlenecks, and currency volatility.

<!-- [FILL IN: Macroeconomic Context and Power Sector Architecture
Instructions:
- National macro context: Income classification (LIC / LMIC), geographic land area (km2), total population, GDP per capita (USD), poverty headcount rate, and consumption Gini index.
- Power sector governance: Responsible ministry, regulatory authority, national transmission/generation utility, and distribution entities (state-owned, private concessions, or municipal distributors).
- Generation mix and installed capacity: Total installed capacity (MW), generation profile (% hydro, % solar, % heavy fuel oil/diesel, % cross-border imports).
- Retail electricity tariffs: Average cost per kWh in USD and {{CURRENCY_CODE}}, lifeline tariff structure, and connection fee schedule.
- National development commitments: National electrification policy, Vision commitments, M300 Africa Energy Compact targets, and ongoing World Bank / donor operations (e.g., ASCENT Project).

Draft Example:
"With a population of approximately [X million] across [Y km2], {{COUNTRY_NAME}} is classified as a [lower-income / lower-middle-income] economy with a GDP per capita of [US$ Z]. The power sector operates under the policy direction of the [Ministry Name] and the economic regulation of [Regulatory Commission]. Bulk power generation and transmission are managed by the state utility [Utility Name], which operates [X MW] of installed capacity, dominated by [hydropower (X%) and thermal imports (Y%)]. Retail electricity tariffs average [US$ 0.XX per kWh], representing one of the [highest/lowest] tariff structures in the sub-region. Under the national [Electrification Strategy / Vision 2030], the Government has committed to achieving universal electricity access by 2030, supported by the World Bank's ASCENT regional program and the M300 Africa Energy Compact."
] -->

The governance of {{COUNTRY_NAME}}'s energy sector involves distinct institutional mandates across policy formulation, technical regulation, generation, transmission, and retail distribution. Sector policy is directed by the national Ministry responsible for energy, which establishes electrification roadmaps, renewable energy master plans, and national targets aligned with the United Nations Sustainable Development Goals. Technical and economic regulation is executed by the national energy regulatory authority, which oversees license issuance, tariff methodology determination, grid code enforcement, and service quality benchmarks.

Bulk power generation and high-voltage transmission are typically anchored by the national power utility. The generation asset base reflects the country's natural resource endowments, combining domestic hydropower resources, thermal heavy fuel oil or diesel plants, grid-connected solar photovoltaic installations, and cross-border regional power pool interconnectors. Retail distribution is managed either through centralized utility regional directorates, municipal electricity distributors, or public-private concessionaires operating licensed distribution service areas. In rural and peri-urban areas beyond the immediate reach of the transmission grid, dedicated rural electrification agencies coordinate decentralized mini-grids and off-grid solar initiatives.

Expanding energy access requires addressing the financial equilibrium of the power sector. Retail electricity tariffs must balance cost-reflectivity for utility financial viability against affordability for vulnerable and low-income consumer segments. Lifeline tariff blocks are commonly deployed to protect low-consumption residential consumers, while commercial and industrial tariffs provide cross-subsidies. High technical and commercial line losses, illegal connections, unmetered consumption, and bill collection challenges often constrain distribution utilities from financing last-mile service drops. Consequently, comprehensive diagnostic surveys such as the Multi-Tier Framework are vital to illuminate household demand elasticities, payment modalities, and service bottlenecks.

---

### 1.2 The Multi-Tier Framework (MTF) Global Methodology

Conventional global energy tracking has historically relied on binary indicators that record whether a household possesses a physical connection to an electricity grid or relies on clean cooking fuels. While binary metrics are straightforward to compile from standard census data, they fail to reflect the actual utility and reliability of energy services delivered to households. In many developing economies, households connected to the grid endure chronic power shedding, severe voltage drops that render appliances inoperable, and prolonged blackouts during evening peak hours. Such households cannot genuinely be considered to enjoy modern energy access.

To overcome these analytical limitations, the Energy Sector Management Assistance Program (ESMAP) and the World Bank developed the **Multi-Tier Framework (MTF)**. The MTF conceptualizes energy access not as a binary condition, but as a multi-dimensional continuum of service ranging from **Tier 0 (no access or sub-basic service)** to **Tier 5 (continuous, high-capacity, reliable, and safe modern energy)**.

Under MTF methodology, household electricity access is evaluated across **seven technical attributes**, while modern energy cooking services are assessed across **six operational dimensions**.

#### The Seven Attributes of Electricity Access
A household's aggregate electricity tier is determined by applying the **Minimum-Attribute Rule**, which establishes that the overall tier is equal to the lowest tier attained across any of the seven individual dimensions:

$$\text{Aggregate Electricity Tier} = \min\Big(\text{Capacity}, \text{Availability}, \text{Reliability}, \text{Quality}, \text{Affordability}, \text{Formality}, \text{Safety}\Big)$$

1. **Capacity:** Evaluates the power output (in watts) of the household's electricity source or the operational load of appliances that can be used simultaneously. Capacity thresholds range from Tier 0 (<3W) and Tier 1 (3–49W, task lighting and phone charging) up to Tier 4 (800–1,999W, heavy thermal appliances) and Tier 5 ($\ge$ 2,000W, air conditioning and electric cooking).
2. **Availability:** Measures the continuous duration of electricity supply delivered over a 24-hour cycle, with explicit evaluation of availability during the four peak evening hours (18:00 to 22:00). Tier 1 requires at least 4 hours per day (including 1 evening hour), while Tier 5 mandates at least 23 hours per day (including all 4 evening hours).
3. **Reliability:** Evaluates the frequency and predictability of unscheduled power outages experienced by grid-connected households. Tiers 4 and 5 impose strict caps on weekly interruptions, requiring no more than 14 outages per week for Tier 4 and no more than 3 outages per week for Tier 5.
4. **Quality:** Assesses whether voltage fluctuations, frequency swings, and power surges occur with sufficient severity to damage consumer electronic appliances. Tiers 4 and 5 require the complete absence of voltage-induced appliance damage.
5. **Affordability:** Determines whether a basic standard electricity consumption package (defined as 365 kWh per year, or 1 kWh per day) can be purchased without exceeding 5% of total household consumption expenditure.
6. **Formality:** Assesses the contractual and legal status of the connection, distinguishing between formal connections with registered utility meters (postpaid or prepaid) and informal, shared, or unregulated third-party hookups.
7. **Health and Safety:** Verifies the physical safety of household electrical installations, requiring the absence of electrical shocks, serious burn injuries, or electrical fire incidents during the preceding 12 months.

---

### Box 1: Minimum Requirements by Tier of Electricity Access

* **Tier 0 (No Access / Sub-Tier 1):** Electricity is unavailable or available for less than 4 hours per day (or less than 1 hour during evening peak hours). Households rely on candles, disposable dry-cell batteries, kerosene lamps, and open flames for lighting.
* **Tier 1 (Task Lighting & Phone Charging):** Peak capacity $\ge$ 3W; supply available $\ge$ 4 hours per day, including $\ge$ 1 hour during evening peak hours. Capable of powering task lighting and mobile phone charging (e.g., solar lanterns, basic solar lighting kits).
* **Tier 2 (General Lighting, Television, & Fan):** Peak capacity $\ge$ 50W; supply available $\ge$ 4 hours per day, including $\ge$ 2 hours during evening peak hours. Capable of operating multiple light points, television, and an electric fan (e.g., multi-light Solar Home Systems, entry-level mini-grids).
* **Tier 3 (Medium Load & Refrigeration):** Peak capacity $\ge$ 200W; supply available $\ge$ 8 hours per day, including $\ge$ 3 hours during evening peak hours. Enables domestic refrigeration, food processing, water pumping, and light productive applications. Standard 365 kWh annual consumption must meet the 5% affordability test.
* **Tier 4 (High Load & Productive Use):** Peak capacity $\ge$ 800W; supply available $\ge$ 16 hours per day, including all 4 evening peak hours. Capable of powering heavy thermal appliances (washing machines, electric irons, microwaves) with low weekly outage frequencies ($\le$ 14 disruptions/week), formal utility billing, and no appliance-damaging voltage swings.
* **Tier 5 (Continuous Full Modern Access):** Peak capacity $\ge$ 2,000W; supply available $\ge$ 23 hours per day, including all 4 evening peak hours. Capable of powering continuous commercial-grade loads, central air conditioning, space heating, and electric cooking with high reliability ($\le$ 3 disruptions/week), formal metering, and verified installation safety.

---

### Box 2: Typology of Off-Grid Solar Devices

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

The {{SURVEY_YEAR}} MTF Household Survey in {{COUNTRY_NAME}} was executed using a stratified two-stage cluster sampling design engineered to produce statistically robust, nationally representative estimates as well as disaggregated indicators across urban and rural domains. The primary sampling frame was derived from the most recent National Population and Housing Census administered by the National Statistics Agency.

In the first sampling stage, Primary Sampling Units (PSUs)—defined as census Enumeration Areas (EAs)—were selected with Probability Proportional to Size (PPS), where size was measured by the number of residential households recorded in the census frame. Sampling was independently stratified across `{{STRATA_COUNT}}` strata, formed by crossing all `{{ADMIN1_COUNT}}` administrative `{{ADMIN1_UNIT_LABEL_PLURAL}}` with geographic locality (urban vs. rural).

In the second sampling stage, a comprehensive household listing exercise was carried out in each selected EA immediately prior to data collection. A systematic random sample of households was drawn from the updated listing register. Household questionnaires were administered face-to-face by trained field enumerators using Computer-Assisted Personal Interviewing (CAPI) tablets programmed with real-time logical validation checks and spatial georeferencing.

To ensure that survey statistics accurately reflect national population parameters, calibrated sampling weights (`hh_wt`) were calculated. The base design weight for each sampled household is the inverse of its overall inclusion probability, computed as the product of the first-stage EA selection probability and the second-stage household selection probability:

$$w_{ij} = \frac{1}{P_{1i} \times P_{2ij}}$$

Sampling weights were subsequently adjusted for non-response at the EA level and calibrated against census population projections across administrative divisions. All econometric tabulations, tier allocations, and econometric models reported in this study apply these calibrated sampling weights.

---

## CHAPTER 2: ACCESS TO ELECTRICITY DIAGNOSTIC

### 2.1 Household Electrification by Technology and Locality

In {{COUNTRY_NAME}}, `{{ELEC_ACC_NAT}}%` of households have access to electricity at Tier 1 or above, while `{{ELEC_T0_NAT}}%` remain in Tier 0. In urban areas, grid connection reaches `{{GRID_ACC_URB}}%` of households and off-grid solar solutions serve `{{SOLAR_ACC_URB}}%`. In rural areas, the national grid reaches `{{GRID_ACC_RUR}}%` of households, while off-grid solar systems serve `{{SOLAR_ACC_RUR}}%` of rural households.

The national electrification profile reflects a diverse multi-source technological landscape. Under international monitoring guidelines established for SDG 7.1.1 and the Multi-Tier Framework, formal electricity access is defined across six qualifying modern technologies:
1. National central grid connections
2. Isolated mini-grids and micro-grids (solar, hydro, or hybrid diesel)
3. Standalone fossil-fuel generators (diesel or gasoline)
4. Solar Home Systems (SHS) and Solar Lighting Systems (SLS)
5. Rechargeable battery systems charged at external commercial charging stations
6. Standalone solar lanterns with task lighting and phone charging capabilities

**Strict Exclusion Rule (SDG 7.1.1):** Disposable dry-cell battery torches, handheld flashlights, and single-use batteries are **strictly excluded** from electrification metrics. While dry-cell torches provide basic task illumination in unserved communities, they do not constitute modern electrical service due to limited luminosity, absence of appliance-powering capacity, high recurrent unit costs, and hazardous environmental disposal footprints.

Figure 1 illustrates the distribution of households across Multi-Tier Framework electricity access tiers (Tier 0 to Tier 5) for national, urban, and rural populations.

![Figure 1: Multi-Tier Framework Electricity Access Tier Distribution Across National, Urban, and Rural Populations]({{CHART_ELEC_TIERS}})
*Figure 1: Distribution of households across Multi-Tier Framework electricity access tiers (Tier 0 to Tier 5) nationwide, in urban areas, and in rural areas.*

Figure 2 delineates the primary electricity technology source mix across the qualifying modern sources, explicitly contrasting modern solutions against excluded disposable battery devices.

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

Electricity access rates vary across household consumption expenditure quintiles: access stands at `{{Q1_ELEC_ACC}}%` in the lowest quintile (Q1), `{{Q2_ELEC_ACC}}%` in Q2, `{{Q3_ELEC_ACC}}%` in Q3, `{{Q4_ELEC_ACC}}%` in Q4, and `{{Q5_ELEC_ACC}}%` in the highest quintile (Q5). Modern energy cooking services access across the corresponding quintiles is `{{Q1_MECS_ACC}}%` in Q1, `{{Q2_MECS_ACC}}%` in Q2, `{{Q3_MECS_ACC}}%` in Q3, `{{Q4_MECS_ACC}}%` in Q4, and `{{Q5_MECS_ACC}}%` in Q5.

In the lowest expenditure quintile (Q1), `{{Q1_ELEC_ACC}}%` of households have electricity access, with unconnected households frequently citing upfront connection fees and wiring costs as primary obstacles. In the highest quintile (Q5), electricity access reaches `{{Q5_ELEC_ACC}}%`.

The consumption expenditure gradient illustrates the presence of an **energy poverty penalty**. Low-income households residing in unserved settlements frequently spend a larger fraction of their monthly budget purchasing inferior lighting substitutes (such as candles, kerosene, and disposable dry-cell batteries) per unit of effective lumen-hour than grid-connected households spend on metered utility electricity. Expanding access to affordable off-grid solar kits and subsidized grid connections relieves this cash drain, freeing resources for nutrition, education, and healthcare.

Figure 3 displays the progression of electricity and modern energy cooking access rates across consumption expenditure quintiles.

![Figure 3: Household Electricity and Modern Energy Cooking Access Across National Consumption Expenditure Quintiles (Q1 to Q5)]({{CHART_QUINTILE_CURVE}})
*Figure 3: Household energy access rates across national consumption expenditure quintiles (Q1 to Q5) for electricity and modern energy cooking services.*

---

### 2.3 In-Depth Evaluation of the Seven Attributes of Electricity Access

The Multi-Tier Framework evaluates electricity supply along seven operational attributes to identify binding bottlenecks that constrain service quality. Figure 4 displays the multi-attribute radar profile comparing grid customers, off-grid solar users, and unelectrified households.

![Figure 4: Multi-Tier Framework Electricity Attribute Performance Radar for Grid-Connected, Off-Grid Solar, and Non-Electrified Households]({{CHART_ELEC_RADAR}})
*Figure 4: Multi-Tier Framework electricity attribute performance radar chart for grid-connected, off-grid solar, and non-electrified households.*

#### 1. Capacity & Appliance Ownership
Grid-connected households are technically provided with high capacity (>2 kW, Tier 5). However, appliance ownership varies widely:
* **Very Low-Load Appliances:** `{{IS_VERYLOW_NAT}}%` of households nationwide (`{{IS_VERYLOW_URB}}%` urban vs. `{{IS_VERYLOW_RUR}}%` rural) own Tier 1 appliances, including mobile phone chargers (`{{HAS_CHARGER_NAT}}%`), radios (`{{HAS_RADIO_NAT}}%`), and electric lighting points (`{{HAS_LIGHTS_NAT}}%`).
* **Low-Load Appliances:** `{{IS_LOW_NAT}}%` own Tier 2 appliances, dominated by flat-screen color televisions (`{{HAS_TV_NAT}}%`) and electric fans (`{{HAS_FAN_NAT}}%`).
* **Medium-Load Appliances:** `{{IS_MED_NAT}}%` own Tier 3 appliances, led by domestic refrigerators and freezers (`{{HAS_FRIDGE_NAT}}%`).
* **High & Very High-Load Appliances:** `{{IS_HIGH_NAT}}%` own Tier 4 appliances, such as electric irons (`{{HAS_IRON_NAT}}%`), microwaves (`{{HAS_MICRO_NAT}}%`), and washing machines (`{{HAS_WASH_NAT}}%`). Tier 5 appliances (air conditioners: `{{HAS_AC_NAT}}%`; electric water heaters/geysers: `{{HAS_GEYSER_NAT}}%`) are owned by `{{IS_VERYHIGH_NAT}}%` nationwide (`{{IS_VERYHIGH_URB}}%` urban vs. `{{IS_VERYHIGH_RUR}}%` rural). Capacity limitations constrain `{{PCT_CAP_LIMITED}}%` of grid households from operating desired appliances simultaneously.

#### 2. Availability (Daily Duration & Evening Peak)
Continuous electricity availability is critical for household welfare and domestic enterprise. While urban grid connections provide extended daily hours, peak evening availability (18:00 to 22:00) represents an operational bottleneck: `{{PCT_EVE_SHORTAGE}}%` of grid-connected households experience evening supply deficits (<4 hours of supply), restricting study time for children and curtailing commercial activities.

#### 3. Reliability (Outage Frequency)
Reliability is a binding bottleneck for grid customers. Nationwide, grid households experience an average of `{{AVG_OUTAGES_PER_WEEK}}` unexpected power outages per week. Unscheduled disruptions are caused by transmission line trips, distribution transformer overloads in high-density informal settlements, vegetation encroachment on medium-voltage lines, and generation deficits during dry seasons.

#### 4. Quality (Voltage Stability)
Among grid-connected households, `{{PCT_VOLTAGE_DAMAGE}}%` report that voltage fluctuations and power surges have caused damage to household electrical appliances. Voltage drops below nominal operating levels prevent refrigerator compressors and water pumps from starting, while sudden high-voltage surges destroy sensitive consumer electronics.

#### 5. Affordability
Under MTF methodology, electricity is considered affordable if the annual cost of a standard 365 kWh package does not exceed 5% of total household consumption expenditure. Among grid-connected households, monthly electricity expenditure averages `{{GRID_MONTHLY_SPEND_NAT}}` `{{CURRENCY_CODE}}` nationally (`{{GRID_MONTHLY_SPEND_URB}}` `{{CURRENCY_CODE}}` in urban areas and `{{GRID_MONTHLY_SPEND_RUR}}` `{{CURRENCY_CODE}}` in rural areas).

#### 6. Formality
The majority of grid-connected households possess a formal connection with an official prepaid or postpaid meter from their authorized utility or municipality. Formal prepaid metering has expanded significantly, providing households with control over monthly spending while eliminating billing disputes. Informal connections, third-party resale through secondary sub-meters, and unmetered flat-rate arrangements are concentrated primarily in informal urban settlements.

#### 7. Health and Safety
Electricity safety is evaluated through reported incidents of electrical accidents, shocks, or fire hazards during the preceding 12 months. Across {{COUNTRY_NAME}}, safety incidents are reported in fewer than 1% of households in the past year, reflecting adherence to basic wiring conventions, though substandard informal drop lines in dense settlements pose persistent fire hazards.

---

### 2.4 Improving Electricity Access: Densification, WTP, and Off-Grid Scale-Up

#### The "Under-the-Grid" Densification Paradox
In {{COUNTRY_NAME}}, `{{UNDER_GRID_UNCONNECTED_NAT}}%` of households reside in electrified Enumeration Areas (EAs) without an active connection (`{{UNDER_GRID_UNCONNECTED_URB}}%` in urban areas and `{{UNDER_GRID_UNCONNECTED_RUR}}%` in rural areas). The overall grid uptake rate within electrified EAs is `{{GRID_UPTAKE_NAT}}%` nationally (`{{GRID_UPTAKE_URB}}%` in urban areas and `{{GRID_UPTAKE_RUR}}%` in rural areas).

An Enumeration Area is classified as electrified if at least one residential household possesses a functional connection to the national distribution grid (`max(grid_hh) == 1`). Households living within these EAs are physically "under the grid"—meaning that low-voltage distribution transformers and lines are already present within their immediate neighborhood.

Connecting an "under-the-grid" household requires only a service drop wire, a meter installation, and internal household wiring, bypassing the heavy capital expenditure required for high-voltage transmission lines, substation construction, and medium-voltage feeder extensions. Densification therefore represents the most cost-effective capital investment opportunity available to the national utility.

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

#### Contingent Valuation & Willingness to Pay (WTP) Dynamics
The MTF survey conducted a contingent valuation bidding experiment to evaluate household willingness to connect across structured financing terms. The analysis evaluates two distinct analytical perspectives:

1. **Cumulative Market Expansion (Demand Curves):** Shows the cumulative expansion of connected households as financing constraints are progressively relaxed.
2. **Mutually Exclusive Financing Target Segments (100% Partition):** Categorizes unconnected households into distinct policy target groups based on the minimum level of financial support required.

Figure 7a plots the cumulative willingness-to-pay demand curve for national grid connection among unconnected households.

![Figure 7a: Grid Connection Willingness to Pay Cumulative Demand Curve Across Financing Modalities]({{CHART_WTP_GRID}})
*Figure 7a: Grid connection willingness to pay cumulative demand curve across financing modalities (Upfront, 3-Month, 6-Month, 12-Month, and 100% Fee Waived).*

Contingent valuation bidding examines household connection willingness across payment structures:
* **Upfront Payment:** `{{WTP_GRID_UPFRONT_NAT}}%` of unconnected households express willingness to connect upfront (`{{WTP_GRID_UPFRONT_URB}}%` in urban areas and `{{WTP_GRID_UPFRONT_RUR}}%` in rural areas).
* **3-Month Installment Plan:** `{{WTP_GRID_3M_NAT}}%` express willingness to connect.
* **6-Month Installment Plan:** `{{WTP_GRID_6M_NAT}}%` express willingness to connect.
* **12-Month Installment Plan:** `{{WTP_GRID_12M_NAT}}%` express willingness to connect.
* **Waived Upfront Connection Fee:** `{{WTP_GRID_WAIVED_NAT}}%` indicate willingness to connect if the upfront fee is waived entirely.
* **Decline at Zero Upfront Fee:** Nationally, `{{WTP_GRID_NEVER_NAT}}%` of unconnected households indicate they would decline connection even at zero upfront fee; among this specific group of decliners, `{{REFUSE_WIRING_COST_NAT}}%` cite internal household wiring costs as the primary reason.

Figure 8 displays the 100% mutually exclusive financing segmentation for unconnected households.

![Figure 8: Mutually Exclusive Financing Target Segments for Unconnected Households]({{CHART_WTP_SEGMENTS}})
*Figure 8: Mutually exclusive financing target segments for unconnected households (summing to 100%) based on minimum financing relief required.*

#### Off-Grid Solar Market Dynamics
For households residing in remote, topographically complex, or sparsely populated settlements beyond the economic reach of grid extension, decentralized off-grid solar solutions represent the primary electrification pathway. Stated willingness to pay for a Solar Home System (SHS) across financing modalities is illustrated in Figure 7b:

![Figure 7b: Off-Grid Solar Device Willingness to Pay Cumulative Demand Curve Across Financing Modalities]({{CHART_WTP_SOLAR}})
*Figure 7b: Off-Grid Solar Home System willingness to pay cumulative demand curve across financing modalities (Upfront, 6-Month, 12-Month, and 24-Month PAYG).*

* **Upfront Payment:** `{{WTP_SOLAR_UPFRONT_NAT}}%` of households nationally.
* **6-Month Plan:** `{{WTP_SOLAR_6M_NAT}}%` of households nationally.
* **12-Month Plan:** `{{WTP_SOLAR_12M_NAT}}%` of households nationally.
* **24-Month Plan:** `{{WTP_SOLAR_24M_NAT}}%` of households nationally.
* **Decline Under Financing:** `{{WTP_SOLAR_NEVER_NAT}}%` of households indicate they would not acquire an SHS under any presented terms; among households declining, `{{REFUSE_SOLAR_COST_NAT}}%` cite equipment purchase costs as the primary factor.

<!-- [FILL IN: Off-Grid Solar Initiatives and Regulatory Framework
Instructions:
- If the country has active government or donor-supported off-grid solar initiatives (e.g., Results-Based Financing [RBF], credit facilities, solar market acceleration projects), summarize them here.
- Detail whether import duties and VAT are waived on certified solar products (IEC/VeraSol).
- If the survey measured public awareness of a specific off-grid fund, report the awareness metric `{{OFF_GRID_FUND_AWARE_NAT}}%` here. If no program exists, delete this block.

Draft Example:
"To accelerate electrification in remote areas beyond the national grid, the Government and development partners established the [Program Name], a [US$ XX million] Results-Based Financing facility designed to de-risk private solar distributors and subsidize tier-qualifying Solar Home Systems. However, public awareness of this financing window remains limited, with only `{{OFF_GRID_FUND_AWARE_NAT}}%` of households nationwide (`{{OFF_GRID_FUND_AWARE_URB}}%` urban vs. `{{OFF_GRID_FUND_AWARE_RUR}}%` rural) reporting familiarity with the initiative."
] -->

Public awareness of government off-grid financing mechanisms is recorded at `{{OFF_GRID_FUND_AWARE_NAT}}%` nationwide (`{{OFF_GRID_FUND_AWARE_URB}}%` in urban areas and `{{OFF_GRID_FUND_AWARE_RUR}}%` in rural areas).

#### Backup Lighting Coping Mechanisms for Grid Households
During unscheduled blackouts and load-shedding intervals, grid-connected households utilize alternative lighting coping mechanisms:
* **Candles:** `{{GRID_BACKUP_CANDLE_NAT}}%` (`{{GRID_BACKUP_CANDLE_URB}}%` urban vs. `{{GRID_BACKUP_CANDLE_RUR}}%` rural).
* **Dry-Cell Torches / Handheld Flashlights:** `{{GRID_BACKUP_TORCH_NAT}}%`.
* **Off-Grid Solar Lanterns & Systems:** `{{GRID_BACKUP_SOLAR_NAT}}%`.
* **No Alternative Backup Source:** `{{GRID_BACKUP_NONE_NAT}}%`.

---

## CHAPTER 3: ACCESS TO MODERN ENERGY COOKING SERVICES (MECS)

### 3.1 Cookstove Typology and Primary Fuel Profile

The cooking energy profile in {{COUNTRY_NAME}} reflects primary cookstove technologies and fuel options across urban and rural environments. Household cooking practices exert profound impacts on public health, forest degradation, greenhouse gas emissions, and female labor allocation.

Nationwide, `{{STOVE_3STONE_N}}%` of households cook primarily over three-stone open fires (`{{STOVE_3STONE_U}}%` in urban areas and `{{STOVE_3STONE_R}}%` in rural areas). Traditional metal and charcoal stoves serve `{{STOVE_TRAD_N}}%` of households nationally (`{{STOVE_TRAD_U}}%` urban vs. `{{STOVE_TRAD_R}}%` rural). Certified Improved Cookstoves (ICS) account for `{{STOVE_ICS_N}}%` nationwide (`{{STOVE_ICS_U}}%` in urban areas and `{{STOVE_ICS_R}}%` in rural areas). Clean cooking solutions (LPG and electric stoves) are used as primary cooking technology by `{{CLEAN_STOVE_NAT}}%` of households nationally (`{{CLEAN_STOVE_URB}}%` urban vs. `{{CLEAN_STOVE_RUR}}%` rural), with electric cooking representing `{{STOVE_ELEC_N}}%` nationally (`{{STOVE_ELEC_U}}%` urban vs. `{{STOVE_ELEC_R}}%` rural).

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

### 3.2 Evaluation of Access Using the Multi-Tier Framework

Access to Modern Energy Cooking Services (MECS) is measured across a six-tier spectrum (Tier 0 to Tier 5) based on six underlying attributes. Figure 10 displays the distribution of households across MECS cooking tiers nationwide, in urban areas, and in rural areas.

![Figure 10: Multi-Tier Framework Modern Energy Cooking Services (MECS) Tier Distribution]({{CHART_COOKING_TIERS}})
*Figure 10: Multi-Tier Framework Modern Energy Cooking Services (MECS) tier distribution across National, Urban, and Rural populations.*

The six attributes of modern energy cooking services are evaluated in depth below:

1. **Cooking Exposure:** Indoor air pollution from cooking fuels generates high concentrations of fine particulate matter ($PM_{2.5}$) and carbon monoxide ($CO$). Exposure is determined by stove emissions, cooking duration, kitchen location (outdoor, detached shelter, or indoor dwelling), and ventilation quality (presence of chimneys, exhaust hoods, or multiple windows). Nationwide, `{{COOK_T0_NAT}}%` of households remain in Cooking Tier 0 primarily because biomass is burned in enclosed or poorly ventilated cooking spaces.
2. **Cookstove Efficiency:** Traditional open fires and uninsulated artisanal burners exhibit thermal efficiency below 10% (Tier 0), wasting biomass and increasing fuel gathering requirements. Certified improved cookstoves achieve efficiencies of 20% to 35% (Tiers 2–3), while modern LPG burners and electric induction stoves reach efficiencies of 40% to 85%+ (Tiers 4–5).
3. **Convenience (Fuel Collection & Preparation Time):** In rural communities where firewood is gathered from communal forests and agricultural fields, households spend over 5.5 hours per week collecting fuel. Stove preparation and fire tending impose additional domestic labor requirements.
4. **Safety:** Evaluates past burn injuries, scalding accidents, and house fires. Serious burn injuries requiring medical hospitalization are reported in fewer than 2% of households, although child exposure to open flames remains a major hazard.
5. **Affordability:** Under MTF guidelines, cooking energy is deemed affordable if fuel expenditures do not exceed 5% of total household consumption expenditure. While rural households who gather firewood for free incur zero cash expenditures, urban households purchasing charcoal or commercial LPG spend significant portions of their disposable cash income on cooking fuel.
6. **Fuel Availability:** Year-round fuel availability is relatively stable for gathered rural firewood, but urban clean fuel users experience occasional LPG cylinder stock-outs and delivery bottlenecks.

---

### 3.3 Stove Stacking and the Exposure Dilution Effect

Stove stacking -- the concurrent use of multiple cookstoves and fuels -- is observed in `{{PCT_STOVE_STACKING}}%` of households in {{COUNTRY_NAME}}. Where clean cooking appliances (LPG or electric) are present (`{{PCT_CLEAN_STOVE_OWNERSHIP}}%` nationally), households may utilize secondary traditional stoves alongside clean devices to accommodate cooking habits, large cooking vessels, or fuel availability.

Because secondary biomass stoves emit smoke during cooking, secondary use of traditional stoves can attenuate the indoor air quality gains of clean cooking appliances: in {{COUNTRY_NAME}}, `{{PCT_STACKING_DILUTION}}%` of clean stove owners remain in Cooking Exposure Tiers 0 or 1.

The exposure dilution phenomenon is rooted in the non-linear dose-response relationship between $PM_{2.5}$ exposure and cardiopulmonary health outcomes defined by the World Health Organization. As illustrated by epidemiological exposure curves, breathing even modest quantities of biomass smoke from a secondary stove dilutes over 70% of the health benefits of clean cooking. Achieving full health gains requires complete displacement of traditional open fires.

Figure 11 displays cookstove stacking patterns and the resulting exposure dilution trapping clean cooking households in low exposure tiers.

![Figure 11: Stove Stacking Patterns and the Exposure Dilution Effect Among Clean Cookstove Owners]({{CHART_STOVE_STACKING}})
*Figure 11: Cookstove stacking patterns and the exposure dilution effect among clean cookstove owners in {{COUNTRY_NAME}}.*

---

### 3.4 Clean Cooking Economic Barriers & Transition Levers

The transition toward modern cooking services is governed by economic barriers at both the appliance acquisition stage and the recurrent fuel refill stage. For clean fuels such as LPG, the high initial capital outlay for a double-burner stove, pressurized gas cylinder, regulator, and safety hose represents a major hurdle for low-income households. Even when appliances are acquired, the lump-sum cash cost of a full 6 kg or 12 kg cylinder refill prevents cash-constrained households from refilling cylinders continuously, prompting reversion to daily charcoal purchases.

<!-- [FILL IN: Clean Cooking Strategy and Market Architecture
Instructions:
- Describe the national clean cooking strategy, biomass regulation, LPG cylinder recirculation models (CRM), and cookstove standards.
- Note any active clean cooking subsidy programs, carbon finance initiatives, or tax exemptions on clean cookstoves and LPG equipment.

Draft Example:
"The Government of {{COUNTRY_NAME}} has prioritized the transition to clean cooking through the [National Clean Cooking Strategy], targeting [X%] modern energy cooking access by 2030. Key reform priorities include transitioning urban centers from raw charcoal to LPG via the Cylinder Recirculation Model (CRM) and expanding high-tier biomass gasifier cookstoves in rural communities. However, progress has been constrained by fragmented supply chains, high upfront cylinder deposit costs, and the absence of national cookstove emissions standards."
] -->

To overcome refill cash constraints, modern distribution models such as Pay-As-You-Cook smart LPG meters and mobile money micro-payments are emerging internationally, allowing consumers to purchase gas in daily increments matching their cash flow.

Figure 7c plots household willingness to pay for improved and clean cooking appliances across structured installment modalities:

![Figure 7c: Clean Cookstove Willingness to Pay Cumulative Demand Curve Across Financing Modalities]({{CHART_WTP_COOKSTOVE}})
*Figure 7c: Clean cookstove willingness to pay cumulative demand curve across financing modalities (Upfront, 3-Month, 6-Month, and 12-Month Installments).*

Contingent valuation for clean cookstoves indicates that stated adoption expands from `{{WTP_COOK_UPFRONT_NAT}}%` under upfront cash payment to `{{WTP_COOK_3M_NAT}}%` under a 3-month plan, `{{WTP_COOK_6M_NAT}}%` under a 6-month plan, and `{{WTP_COOK_12M_NAT}}%` under a 12-month installment plan.

---

## CHAPTER 4: GENDER ANALYSIS AND INTRA-HOUSEHOLD DRUDGERY

### 4.1 Demographic & Socioeconomic Profile by Gender of Household Head

In {{COUNTRY_NAME}}, `{{MHH_SHARE}}%` of households are headed by men (MHH) and `{{FHH_SHARE}}%` are headed by women (FHH). Survey indicators disaggregated by gender of household head provide insight into comparative demographic profiles, educational attainment, credit access, and energy uptake.

Female household heads average `{{HEAD_AGE_FHH}}` years of age, compared to `{{HEAD_AGE_MHH}}` years for male household heads. Regarding marital status, `{{HEAD_MARITAL_WIDOW_FHH}}%` of female heads and `{{HEAD_MARITAL_WIDOW_MHH}}%` of male heads are widowed, while `{{HEAD_MARITAL_MARRIED_FHH}}%` of female heads and `{{HEAD_MARITAL_MARRIED_MHH}}%` of male heads are married or cohabiting. Educational attainment distributions indicate that `{{HEAD_EDUC_NONE_FHH}}%` of female heads and `{{HEAD_EDUC_NONE_MHH}}%` of male heads report no formal schooling; primary education completion is `{{HEAD_EDUC_PRIM_FHH}}%` for female heads and `{{HEAD_EDUC_PRIM_MHH}}%` for male heads; secondary completion is `{{HEAD_EDUC_SEC_FHH}}%` for female heads and `{{HEAD_EDUC_SEC_MHH}}%` for male heads; and higher education completion stands at `{{HEAD_EDUC_HIGH_FHH}}%` for female heads and `{{HEAD_EDUC_HIGH_MHH}}%` for male heads. Access to loans or credit from formal financial institutions is reported by `{{CREDIT_ACCESS_FHH}}%` of female heads, compared to `{{CREDIT_ACCESS_MHH}}%` of male heads.

Figure 12 displays comparative demographic profiles, educational attainment, credit access, and electricity access parity across female- and male-headed households.

![Figure 12: Demographic Characteristics, Educational Attainment, and Energy Access Parity by Gender of Household Head]({{CHART_GENDER_ACCESS}})
*Figure 12: Demographic characteristics, educational attainment, and energy access parity by gender of household head in {{COUNTRY_NAME}}.*

Table 4.1 presents the complete demographic and socioeconomic profile across household headship.

---

### Table 4.1: Demographic and Socioeconomic Profile by Gender of Household Head

| Indicator / Characteristic | Male-Headed (MHH) | Female-Headed (FHH) | National Average |
| :--- | :---: | :---: | :---: |
| **Share of Total Households (%)** | `{{MHH_SHARE}}` | `{{FHH_SHARE}}` | `100.0` |
| **Average Age of Household Head (Years)** | `{{HEAD_AGE_MHH}}` | `{{HEAD_AGE_FHH}}` | `{{HEAD_AGE_NAT}}` |
| **Head Has No Formal Schooling (%)** | `{{HEAD_EDUC_NONE_MHH}}` | `{{HEAD_EDUC_NONE_FHH}}` | `{{HEAD_EDUC_NONE_NAT}}` |
| **Head Completed Primary Education (%)** | `{{HEAD_EDUC_PRIM_MHH}}` | `{{HEAD_EDUC_PRIM_FHH}}` | `{{HEAD_EDUC_PRIM_NAT}}` |
| **Head Completed Secondary Education (%)** | `{{HEAD_EDUC_SEC_MHH}}` | `{{HEAD_EDUC_SEC_FHH}}` | `{{HEAD_EDUC_SEC_NAT}}` |
| **Head Completed Higher Education (%)** | `{{HEAD_EDUC_HIGH_MHH}}` | `{{HEAD_EDUC_HIGH_FHH}}` | `{{HEAD_EDUC_HIGH_NAT}}` |
| **Head Is Married / Cohabiting (%)** | `{{HEAD_MARITAL_MARRIED_MHH}}` | `{{HEAD_MARITAL_MARRIED_FHH}}` | `{{HEAD_MARITAL_MARRIED_NAT}}` |
| **Head Is Widowed (%)** | `{{HEAD_MARITAL_WIDOW_MHH}}` | `{{HEAD_MARITAL_WIDOW_FHH}}` | `{{HEAD_MARITAL_WIDOW_NAT}}` |
| **Head Has Access to Loans / Credit (%)** | `{{CREDIT_ACCESS_MHH}}` | `{{CREDIT_ACCESS_FHH}}` | `{{CREDIT_ACCESS_NAT}}` |
| **Electricity Access Rate (Tier 1-5, %)** | `{{MHH_ELEC_ACC}}` | `{{FHH_ELEC_ACC}}` | `{{ELEC_ACC_NAT}}` |
| **WTP Grid Connection Upfront (%)** | `{{WTP_GRID_UPFRONT_MHH}}` | `{{WTP_GRID_UPFRONT_FHH}}` | `{{WTP_GRID_UPFRONT_NAT}}` |
| **WTP Grid Connection (12-Mo. Plan, %)** | `{{WTP_GRID_12M_MHH}}` | `{{WTP_GRID_12M_FHH}}` | `{{WTP_GRID_12M_NAT}}` |

---

### 4.2 Energy Access and Willingness to Pay by Gender of Household Head

* **Electricity Access:** Electricity access (Tier 1 or above) stands at `{{FHH_ELEC_ACC}}%` for female-headed households and `{{MHH_ELEC_ACC}}%` for male-headed households. Modern cooking services access (Tier 1 or above) is `{{FHH_MECS_ACC}}%` among female-headed households and `{{MHH_MECS_ACC}}%` among male-headed households.
* **Grid Connection Financing Preferences:** Stated willingness to pay grid connection fees upfront is `{{WTP_GRID_UPFRONT_FHH}}%` among female heads and `{{WTP_GRID_UPFRONT_MHH}}%` among male heads. Under a 12-month installment schedule, stated willingness to connect is `{{WTP_GRID_12M_FHH}}%` for female heads and `{{WTP_GRID_12M_MHH}}%` for male heads. For off-grid solar systems, upfront purchase willingness is `{{WTP_SOLAR_UPFRONT_FHH}}%` among female heads and `{{WTP_SOLAR_UPFRONT_MHH}}%` among male heads.
* **Cookstove Purchase Decision-Making:** Cookstove purchase decisions are reported as made primarily by female household members in `{{COOK_DEC_FEMALE_NAT}}%` of households, by male members in `{{COOK_DEC_MALE_NAT}}%`, and jointly in `{{COOK_DEC_JOINT_NAT}}%`.

---

### 4.3 Intra-Household Time Poverty and Fuelwood Drudgery

Time-use data from the MTF survey document daily domestic labor allocations across adult household members:

* **Daily Cooking Time:** Adult women spend an average of `{{WOMEN_COOK_TIME}}` minutes per day on meal preparation, compared to `{{MEN_COOK_TIME}}` minutes per day for adult men.
* **Fuelwood Collection:** Daily time spent collecting firewood averages `{{WOMEN_FUEL_TIME}}` minutes for adult women, compared to `{{MEN_FUEL_TIME}}` minutes for adult men.
* **Annual Time Allocation:** Over a 12-month period, fuel collection time equates to **`{{WOMEN_FUEL_WORKDAYS}}` eight-hour working day equivalents** per woman.

The economic valuation of drudgery illustrates the immense opportunity cost imposed on rural women. Spending dozens of full working days per year collecting heavy firewood bundles directly reduces time available for agricultural production, market trade, micro-enterprise operations, child literacy support, and personal rest. Furthermore, the physical exertion of hauling 20–30 kg wood loads over long distances leads to chronic spinal, neck, and joint injuries.

Figure 13 illustrates the intra-household time-use burden for meal preparation and firewood collection across adult women, adult men, and children.

![Figure 13: Intra-Household Time-Use Burden for Fuelwood Collection and Cooking Across Demographic Groups]({{CHART_GENDER_FUEL}})
*Figure 13: Intra-household time-use burden for fuelwood collection and cooking across demographic groups in {{COUNTRY_NAME}}.*

---

### 4.4 Gender-Informed Energy Interventions

<!-- [FILL IN: Gender-Informed Energy Policies and Programs
Instructions:
- Describe any existing gender action plans within the Ministry of Energy or national utility.
- Note female employment targets, women-led clean energy entrepreneurship networks, or targeted connection subsidies for vulnerable female-headed households.

Draft Example:
"In alignment with the [National Gender Policy], the [Ministry Name] has integrated gender-responsive targets into national electrification operations. Priorities include establishing dedicated credit windows for female energy entrepreneurs, training women as certified solar technicians and mini-grid operators, and offering subsidized connection vouchers for low-income female-headed households."
] -->

Integrating gender considerations into national energy planning requires addressing both access to energy infrastructure and women's economic participation across the energy supply chain. Because women bear the primary responsibility for cooking and fuel gathering while making `{{COOK_DEC_FEMALE_NAT}}%` of cookstove purchasing decisions, clean cooking market interventions must be designed in direct consultation with women's cooperatives, community savings associations, and female entrepreneurs.

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

Based on the empirical findings of the {{SURVEY_YEAR}} Multi-Tier Framework survey, the Government of {{COUNTRY_NAME}}, international development partners, utility operators, and private sector financiers should prioritize six strategic intervention pillars:

### 1. Accelerate Last-Mile Grid Densification via Flexible On-Bill Financing & Ready Boards
* **Target the "Under-the-Grid" Population:** With `{{UNDER_GRID_UNCONNECTED_NAT}}%` of households nationwide residing in electrified EAs without a connection, grid densification offers the fastest, most cost-effective path to expanding national electrification.
* **Flexible Connection Fee Installments:** Introduce standardized utility installment arrangements spread over 12 to 24 months, addressing the difference between stated upfront payment willingness (`{{WTP_GRID_UPFRONT_NAT}}%`) and 12-month installment willingness (`{{WTP_GRID_12M_NAT}}%`).
* **Internal Installation Support & 'Ready Boards':** Address internal wiring cost constraints -- cited as the primary reason for connection refusal by `{{REFUSE_WIRING_COST_NAT}}%` of households who decline connection even when fees are waived -- by distributing standardized pre-wired 'ready boards' or financing internal wiring during grid hookup.

### 2. Distribution Network Quality & Reliability Upgrades
* **Stabilize Distribution Voltage:** Upgrade overloaded distribution transformers and deploy Automatic Voltage Regulators (AVRs) to eliminate the voltage surges that have damaged appliances for `{{PCT_VOLTAGE_DAMAGE}}%` of grid households.
* **Mitigate Outage Frequencies:** Implement automated fault isolation, feeder automation, and preventive vegetation clearing to reduce the average `{{AVG_OUTAGES_PER_WEEK}}` weekly disruptions, enabling households to achieve Tier 4 and Tier 5 service levels.

### 3. De-Risk Distributed Off-Grid Solar & Digital PAYGo Financing
* **Promote Quality-Verified Solar Home Systems:** Shift off-grid subsidies away from basic Tier 1 solar lanterns toward certified (IEC/VeraSol) Solar Home Systems capable of powering televisions, fans, refrigeration, and productive appliances.
* **Incorporate PAYGo Digital Financing:** Partner with mobile network operators and financial institutions to expand Pay-As-You-Go (PAYGo) mobile money financing, addressing upfront liquidity constraints.
* **Expand Public Awareness:** Address the `{{OFF_GRID_FUND_AWARE_NAT}}%` national awareness rate of off-grid financing mechanisms through targeted community outreach and local radio campaigns.

### 4. Implement a Dual-Track Clean Cooking Transition Strategy
* **Urban Clean Cooking & e-Cooking Transition:** Where urban grid infrastructure is present (`{{GRID_ACC_URB}}%` grid connection rate in urban areas), evaluate programs supporting energy-efficient electric cooking appliances (such as electric pressure cookers) alongside clean cooking fuels to reduce urban charcoal and biomass consumption.
* **Rural Biomass Efficiency & Improved Cookstoves (ICS):** In rural areas where three-stone open fire use is `{{STOVE_3STONE_R}}%`, support distribution and adoption of certified high-efficiency improved biomass cookstoves to reduce fuelwood consumption and ease the `{{WOMEN_FUEL_WORKDAYS}}` eight-hour working day equivalents per year associated with fuel collection.
* **Mitigate Stove Stacking:** Deploy public awareness campaigns regarding the exposure dilution effect, demonstrating that continued secondary use of traditional fires attenuates clean cooking health benefits.

### 5. Institutionalize Gender-Targeted Energy Interventions
* **Targeted Connection Subsidies for Vulnerable Households:** Provide connection fee relief, flexible installment plans, or subsidized connection vouchers for female-headed households (`{{FHH_SHARE}}%`).
* **Gender-Informed Program Design:** Align clean cooking program design, outreach, and payment options with household decision patterns, reflecting that female household members make cookstove purchase decisions in `{{COOK_DEC_FEMALE_NAT}}%` of households (with male decision-making at `{{COOK_DEC_MALE_NAT}}%` and joint decisions at `{{COOK_DEC_JOINT_NAT}}%`).

### 6. Institutionalize Geospatial Planning and MTF Monitoring Systems
* **Multi-Tier Performance Monitoring:** Embed MTF indicator tracking within the national Ministry responsible for energy to monitor service delivery, voltage quality, and outage durations over time.
* **Least-Cost Geospatial Electrification Planning:** Integrate MTF survey microdata with satellite imagery and geospatial network models to determine optimal technology boundaries between grid extension, mini-grids, and off-grid solar.

<!-- [FILL IN: Institutional Implementation Roadmap Matrix
Instructions:
- Populate the specific government ministries, state utilities, regulatory commissions, and donor projects responsible for executing each of the six strategic policy imperatives.
] -->

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

<!-- [FILL IN: Sampling Frame Details
Instructions:
- Provide the name and year of the national population census used to construct the Master Sampling Frame.
- Specify the number of surveyed Enumeration Areas (EAs) and final surveyed household sample size.

Draft Example:
"The {{SURVEY_YEAR}} MTF Household Survey sampling frame was constructed from the [Year] National Population and Housing Census provided by the [National Statistics Agency]. A total of [N] Enumeration Areas were selected across all {{ADMIN1_COUNT}} administrative {{ADMIN1_UNIT_LABEL_PLURAL}}, yielding a final calibrated sample of [N,NNN] households."
] -->

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

* **Figure 4:** Multi-Tier Framework Electricity Attribute Performance Radar for Grid-Connected, Off-Grid Solar, and Non-Electrified Households
  ![Figure 4: Multi-Tier Framework Electricity Attribute Performance Radar for Grid-Connected, Off-Grid Solar, and Non-Electrified Households]({{CHART_ELEC_RADAR}})

* **Figure 5:** The Under-the-Grid Uptake Funnel and National Densification Deficit
  ![Figure 5: The Under-the-Grid Uptake Funnel and National Densification Deficit]({{CHART_UNDER_GRID}})

* **Figure 6:** Primary Stated Barriers to Gaining Grid Connection and Willingness to Pay by Payment Modality
  ![Figure 6: Primary Stated Barriers to Gaining Grid Connection and Willingness to Pay by Payment Modality]({{CHART_GRID_BARRIERS}})

* **Figure 7a:** Grid Connection Willingness to Pay Cumulative Demand Curve Across Financing Modalities
  ![Figure 7a: Grid Connection Willingness to Pay Cumulative Demand Curve Across Financing Modalities]({{CHART_WTP_GRID}})

* **Figure 7b:** Off-Grid Solar Home System Willingness to Pay Cumulative Demand Curve Across Financing Modalities
  ![Figure 7b: Off-Grid Solar Home System Willingness to Pay Cumulative Demand Curve Across Financing Modalities]({{CHART_WTP_SOLAR}})

* **Figure 7c:** Clean Cookstove Willingness to Pay Cumulative Demand Curve Across Financing Modalities
  ![Figure 7c: Clean Cookstove Willingness to Pay Cumulative Demand Curve Across Financing Modalities]({{CHART_WTP_COOKSTOVE}})

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
* **ESMAP.** 2020. *The State of Access to Modern Energy Cooking Services.* Washington, DC: World Bank Group.
* **IEA, IRENA, UNSD, World Bank, and WHO.** 2024. *Tracking SDG 7: The Energy Progress Report 2024.* Washington, DC: World Bank.
* **International Organization for Standardization (ISO).** 2018. *Clean cookstoves and clean cooking solutions — Harmonized laboratory test protocols — Part 1: Standard test sequence for emissions and performance, safety and durability.* ISO 19867-1:2018. Geneva: ISO.
* **World Bank.** 2023. *Multi-Tier Framework Survey Methodology and Implementation Guidelines.* Washington, DC: World Bank Group.
* **World Health Organization (WHO).** 2014. *WHO Guidelines for Indoor Air Quality: Household Fuel Combustion.* Geneva: World Health Organization.

---
*Report published by the World Bank Group and the Energy Sector Management Assistance Program (ESMAP), Washington, DC.*
