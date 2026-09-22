<!-- ============================================================
     MTF REGIONAL ANALYSIS MODULE — OPTIONAL APPENDIX
     ============================================================
     INSTRUCTIONS FOR COORDINATOR:
     This module provides the Admin 1 level disaggregated electricity
     access analysis. Insert this content into the main report ONLY
     if the client explicitly requests regional disaggregation.

     WHERE TO INSERT: Paste this content inside Section 2.2 of
     MTF_Report_Template.md, replacing the "OPTIONAL REGIONAL MODULE"
     comment block.

     AUTO-CALIBRATION: When running mtf_calibrator.py with the
     --include-regional flag, this module is auto-populated with the
     country's detected Admin 1 units and injected automatically.
     ============================================================ -->

### Regional Electrification Divide Across {{ADMIN1_COUNT}} Administrative {{ADMIN1_UNIT_LABEL_PLURAL}}

{{COUNTRY_NAME}}'s regional electrification profile reveals extreme unevenness across the {{ADMIN1_COUNT}} administrative {{ADMIN1_UNIT_LABEL_PLURAL}}. To account for survey design effects and sampling variability across subnational domains, both point estimates and logit-transformed 95% confidence intervals are evaluated:

<!-- [AUTO-GENERATED: The following bullet points are populated by mtf_calibrator.py based on the
     detected Admin 1 units and their electrification rates. Coordinator should review groupings
     (high-access vs. low-access) and update the narrative after seeing the actual data.] -->

{{REGIONAL_NARRATIVE_BULLETS}}

![Figure 9: Regional Access Gap]({{CHART_REGIONAL_GAP}})
*Figure 9: Subnational electricity access rates and technology mix across {{COUNTRY_NAME}}'s {{ADMIN1_COUNT}} administrative {{ADMIN1_UNIT_LABEL_PLURAL}} with logit-transformed 95% survey confidence intervals.*

##### Table 2.2: Subnational Energy Access Indicators with 95% Survey Confidence Intervals

| Administrative {{ADMIN1_UNIT_LABEL}} | Total Electricity Access (%) [95% CI] | National Grid Access (%) [95% CI] | Off-Grid Solar (%) [95% CI] | High Access Tier 4-5 (%) [95% CI] | Modern Cooking (MECS) (%) [95% CI] |
|:---|:---:|:---:|:---:|:---:|:---:|
{{REGIONAL_TABLE_ROWS}}

<!-- [FILL IN: Review Table 2.2 values after running the Stata pipeline and confirm 95% CI estimates.
     The placeholders above are populated from the 07_export.do scalar scalars by inject_report.py.
     If confidence intervals are very wide for small Admin 1 units, consider adding a footnote explaining
     small-sample caveats.] -->
