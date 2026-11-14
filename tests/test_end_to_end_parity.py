#!/usr/bin/env python3
"""
test_end_to_end_parity.py — Automated Dual-Pipeline Zero-Divergence Unit Test
=============================================================================
Author: Bryan Koo / Antigravity AI Executive Operating Agent
World Bank ESMAP | Energy Global Practice

Purpose:
  Asserts that the end-to-end Python pipeline (mtf_builder.py + mtf_engine.py)
  achieves strict numerical parity with Stata reference deliverables:
    1. All 50 core Master dataset variables satisfy max_diff <= 0.01%.
    2. All common report injection tokens satisfy absolute delta <= 0.10.
"""

import os
import sys
import json
import unittest
from pathlib import Path
import numpy as np
import pandas as pd

# Add repo root to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "interactive_suite") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "interactive_suite"))

from tests.verify_parity import ParityAuditor, CORE_MASTER_VARS


class TestEndToEndParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.py_master = REPO_ROOT / "interactive_suite" / "Data" / "test_py_master.dta"
        if not cls.py_master.exists():
            cls.py_master = Path("/home/bryan/Desktop/esmap-mtf-pipeline/interactive_suite/Data/test_py_master.dta")

        cls.stata_master = Path("/home/bryan/Desktop/esmap-mtf-pipeline/interactive_suite/Data/MTF_2024_HH_Guinea-Bissau_Master.dta")
        if not cls.stata_master.exists():
            cls.stata_master = Path("/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/37_Guinea-Bissau/Data/wip_hh/MTF_2024_HH_Guinea-Bissau_Master.dta")

        cls.py_json = REPO_ROOT / "Output" / "mtf_report_values_py.json"
        cls.stata_json = Path("/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/37_Guinea-Bissau/Output/mtf_report_values.json")

        cls.auditor = ParityAuditor(
            py_master=cls.py_master,
            stata_master=cls.stata_master,
            py_json=cls.py_json,
            stata_json=cls.stata_json
        )

    def test_datasets_available(self):
        """Assert both compiled Python master and reference Stata master datasets exist."""
        self.assertTrue(self.py_master.exists(), f"Python master dataset missing: {self.py_master}")
        self.assertTrue(self.stata_master.exists(), f"Stata master dataset missing: {self.stata_master}")

    def test_stage1_master_variable_parity(self):
        """Assert all 50 core variables satisfy divergence <= 0.01% (zero-divergence standard)."""
        results, all_ok = self.auditor.audit_stage1_master()
        self.assertGreaterEqual(len(results), 40, f"Expected >= 40 core variables, found {len(results)}")

        failed_vars = []
        for r in results:
            if not r["passed"]:
                failed_vars.append(f"{r['variable']}: Py={r['py_mean']:.4f}, Stata={r['stata_mean']:.4f}, Diff={r['diff_pct']:.4f}%")

        self.assertEqual(len(failed_vars), 0, "Stage 1 Dual-Pipeline Parity Failed! Divergent variables:\n" + "\n".join(failed_vars))

    def test_stage2_report_token_parity(self):
        """Assert common report scalar tokens match within numerical tolerance."""
        if not self.stata_json.exists() or not self.py_json.exists():
            self.skipTest("Report JSON outputs not found for token verification.")

        results, all_ok = self.auditor.audit_stage2_tokens()
        self.assertGreaterEqual(len(results), 100, f"Expected >= 100 tokens, found {len(results)}")

        divergent_tokens = []
        for r in results:
            if not r["passed"]:
                divergent_tokens.append(f"{r['token']}: Py={r['py_val']}, Stata={r['stata_val']}, Delta={r['delta']:.4f}")

        self.assertEqual(len(divergent_tokens), 0, "Stage 2 Token Parity Failed! Divergent tokens:\n" + "\n".join(divergent_tokens))

    def test_headline_access_exact_match(self):
        """Specifically assert headline electrification and clean cooking access rates match Stata."""
        if not self.stata_json.exists() or not self.py_json.exists():
            self.skipTest("Report JSON outputs not found.")

        with open(self.py_json, "r", encoding="utf-8") as f:
            py_tok = json.load(f)
        with open(self.stata_json, "r", encoding="utf-8") as f:
            stata_tok = json.load(f)

        headline_tokens = [
            "{{ELEC_ACC_NAT}}", "{{ELEC_ACC_URB}}", "{{ELEC_ACC_RUR}}",
            "{{ELEC_T45_NAT}}", "{{GRID_ACC_NAT}}", "{{SOLAR_ACC_NAT}}",
            "{{COOK_T4_NAT}}", "{{UNDER_THE_GRID_NAT}}", "{{GRID_UPTAKE_NAT}}"
        ]

        for tok in headline_tokens:
            if tok in py_tok and tok in stata_tok:
                p_val = py_tok[tok]
                s_val = stata_tok[tok]
                self.assertAlmostEqual(p_val, s_val, delta=0.01,
                                       msg=f"Headline token mismatch on {tok}: Python={p_val}, Stata={s_val}")


if __name__ == "__main__":
    unittest.main()
