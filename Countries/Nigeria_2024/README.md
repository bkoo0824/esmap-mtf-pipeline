# MTF Nigeria 2024 Diagnostic Pipeline

## Survey Context
- **Country:** Federal Republic of Nigeria
- **Survey Year:** 2024
- **Currency:** Nigerian Naira (NGN)
- **Exchange Rate:** 1,580.0 NGN / USD
- **Sample Size:** 4,162 households across 210 EAs
- **Admin 1 Domains:** 37 Administrative Divisions (36 States + Federal Capital Territory)
- **Primary Sampling Unit (EA ID):** `SEC_A_Q07` (string identifier converted via `egen psu_id = group(SEC_A_Q07)`)
- **Locality Variable:** `SEC_A_Q05` (1 = Urban, 2 = Rural)
- **Sampling Weight:** Embedded `HHsampleweights`
- **Cookstove Question:** `SEC_G_Q05` (26 distinct categories mapped in `cookstove_calibration.csv`)

## Execution Instructions
1. Open Stata (version 16+ SE/MP).
2. Open `Nigeria_MTF_Master.do`.
3. Ensure your local username and OneDrive data path are configured in Section 1:
   ```stata
   if c(username) == "your_username" {
       global user "C:/Users/your_username/OneDrive - WBG/..."
   }
   ```
4. Run `Nigeria_MTF_Master.do`.
