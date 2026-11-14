# MTF Guinea-Bissau 2024 Diagnostic Pipeline

## Survey Context
- **Country:** Republic of Guinea-Bissau
- **Survey Year:** 2024
- **Currency:** West African CFA Franc (XOF)
- **Exchange Rate:** 605.0 XOF / USD
- **Sample Size:** 3,510 households
- **Admin 1 Domains:** 9 Regions (Bafata, Biombo, Bissau, Bolama, Cacheu, Gabu, Oio, Quinara, Tombali)
- **Locality Variable:** `SEC_A_Q05` (1 = Urban, 2 = Rural)
- **Sampling Strata:** `strata_id` (18 strata: Region × Locality)
- **Primary Sampling Unit (EA):** `SEC_A_Q06` / `psu_id`
- **Sampling Weight:** `hh_wt`

## Key Harmonization Features
1. **Defensive Education Mapping (`00_country_harmonization.do`)**:
   - `SEC_A1_Q8` mapped to ISCED 4-category standard (0: None, 1: Primary, 2: Secondary, 3: Higher).
   - Includes runtime assertion halting execution if secondary/higher education has 0 observations.
2. **Missing Expenditure Codes**:
   - Positive code `888` ("Don't know") in `SEC_C_Q25` recoded to missing `.`.
3. **Cookstove Open-Text Reclassification**:
   - 28 artisanal charcoal braziers (`fogareiro`, `fugão a carvão`) in `SEC_G_Q05_oth` reclassified to Code 2 (Traditional Stove).
4. **Appliance Recoding**:
   - Open-text `"Rádio"` in `SEC_C_Q125_oth` mapped to `has_radio = 1`.

## Execution Instructions
1. Open Stata (version 16+ SE/MP).
2. Open `Guinea-Bissau_MTF_Master.do`.
3. Ensure your local username and data path are configured in Section 1.
4. Run `Guinea-Bissau_MTF_Master.do`.
