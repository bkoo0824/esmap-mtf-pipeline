# test_engine_parity.py — Stata vs Python MTF Dual-Engine Parity Test Suite
# ==============================================================================
# Verifies that the open-source Python analytical engine (mtf_engine.py) produces
# econometric indicators strictly matching Stata reference values within numerical
# tolerance (delta <= 0.15 percentage points).
# ==============================================================================

import os
import json
import unittest
from pathlib import Path

class TestEngineParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Locate Stata output JSON and Python output JSON
        cls.repo_root = Path(__file__).resolve().parent.parent
        cls.stata_json = Path("/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/37_Guinea-Bissau/Output/mtf_report_values.json")
        cls.py_json = Path("/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/37_Guinea-Bissau/Output/mtf_report_values_py.json")

        if not cls.stata_json.exists():
            # Fallback path if working on different clone
            cls.stata_json = cls.repo_root / "Output" / "mtf_report_values.json"

    def test_json_files_exist(self):
        """Verify that Stata and Python output JSON files exist for parity comparison."""
        self.assertTrue(self.stata_json.exists(), f"Stata JSON missing at {self.stata_json}")
        self.assertTrue(self.py_json.exists(), f"Python JSON missing at {self.py_json}")

    def test_numerical_parity_across_common_indicators(self):
        """Assert numerical parity between Stata and Python for all common indicators."""
        with open(self.stata_json, "r", encoding="utf-8") as f1:
            stata_data = json.load(f1)
        with open(self.py_json, "r", encoding="utf-8") as f2:
            py_data = json.load(f2)

        common_keys = sorted(list(set(stata_data.keys()) & set(py_data.keys())))
        self.assertGreaterEqual(len(common_keys), 40, f"Expected at least 40 common indicators, got {len(common_keys)}")

        mismatches = []
        for k in common_keys:
            s_val = stata_data[k]
            p_val = py_data[k]
            if isinstance(s_val, (int, float)) and isinstance(p_val, (int, float)):
                delta = abs(s_val - p_val)
                # Max tolerance: 0.15 percentage points to account for float precision and rounding
                if delta > 0.15:
                    mismatches.append(f"{k}: Stata={s_val}, Python={p_val}, Delta={delta:.3f}")

        self.assertEqual(len(mismatches), 0, "Dual-engine parity failure! Diverging indicators:\n" + "\n".join(mismatches))

    def test_core_access_rates_match(self):
        """Specifically assert core electrification and clean cooking access rates match Stata."""
        with open(self.stata_json, "r", encoding="utf-8") as f1:
            stata_data = json.load(f1)
        with open(self.py_json, "r", encoding="utf-8") as f2:
            py_data = json.load(f2)

        core_tokens = [
            "{{ELEC_ACC_NAT}}", "{{ELEC_ACC_URB}}", "{{ELEC_ACC_RUR}}",
            "{{COOK_MECS_NAT}}", "{{COOK_MECS_URB}}", "{{COOK_MECS_RUR}}",
            "{{UNDER_THE_GRID_NAT}}", "{{GRID_UPTAKE_NAT}}", "{{PCT_STACKING_DILUTION}}"
        ]

        for token in core_tokens:
            if token in stata_data and token in py_data:
                s = stata_data[token]
                p = py_data[token]
                self.assertAlmostEqual(s, p, delta=0.1, msg=f"Parity mismatch on {token}: Stata={s}, Python={p}")

if __name__ == "__main__":
    unittest.main()
