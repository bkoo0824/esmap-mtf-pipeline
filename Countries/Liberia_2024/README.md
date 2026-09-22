# MTF Liberia 2024 Diagnostic Pipeline

## Survey Context
- **Country:** Republic of Liberia
- **Survey Year:** 2024
- **Currency:** Liberian Dollar (LRD)
- **Exchange Rate:** 192.5 LRD / USD
- **Sample Size:** 4,500+ households
- **Admin 1 Domains:** 15 Counties (Bomi, Bong, Gbarpolu, Grand Bassa, Grand Cape Mount, Grand Gedeh, Grand Kru, Lofa, Margibi, Maryland, Montserrado, Nimba, River Cess, River Gee, Sinoe)
- **Primary Sampling Unit (EA):** `SEC_A_Q05`
- **Locality Variable:** `SEC_A_Q06` (1 = Urban, 2 = Rural)
- **Sampling Weight:** Embedded `HH_weights`

## Execution Instructions
1. Open Stata (version 16+ SE/MP).
2. Open `Liberia_MTF_Master.do`.
3. Ensure your local username and OneDrive data path are configured in Section 1:
   ```stata
   if c(username) == "your_username" {
       global user "C:/Users/your_username/OneDrive - WBG/..."
   }
   ```
4. Run `Liberia_MTF_Master.do`.
