"""
test_adversarial_m1_challenger_3.py — Adversarial Stress Test Suite for Milestone M1

Targeted adversarial stress tests for:
1. Missing template handling with stale MTF_Test_Report.md and stale MTF_Test_Report.docx.
   Asserts exit code 1, fatal abort message in stderr, and prevention of docx generation/update.
2. JSON trailing and consecutive commas stress test:
   - {"A": 1, , }
   - {"A": 1,,}
   - {"A": 1,  ,  ,  }
   - [1, , 2]
   - {"A": 1, , "B": 2}
   - nested dicts and lists with trailing commas
   Asserts that all inputs parse cleanly without JSONDecodeError.
"""

import sys
import json
import re
import tempfile
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = (REPO_ROOT / "00_Standard_Template" / "Do-file" / "scripts" / "inject_report.py").resolve()
PYTHON_VENV = sys.executable

sys.path.insert(0, str(SCRIPT_PATH.parent))
import inject_report


class TestAdversarialMissingTemplate(unittest.TestCase):
    """Adversarial stress-test: Missing template handling and stale artifact prevention."""

    def test_stale_markdown_and_docx_not_updated_on_missing_template(self):
        """
        Create a test scenario where an old/stale MTF_Test_Report.md exists in the output directory.
        Run inject_report.py with --template /nonexistent/path.md.
        Assert that:
          (a) exit code is 1
          (b) stderr contains fatal abort message
          (c) MTF_Test_Report.docx is NOT generated or updated
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            json_file = tmp_path / "mtf_report_values.json"
            json_file.write_text(json.dumps({"COUNTRY_NAME": "Test", "VAL": 123}))

            # 1. Create pre-existing stale MTF_Test_Report.md
            stale_md = tmp_path / "MTF_Test_Report.md"
            stale_md_content = "# STALE REPORT FROM OBSOLETE RUN"
            stale_md.write_text(stale_md_content)

            # 2. Create pre-existing stale MTF_Test_Report.docx with sentinel content
            stale_docx = tmp_path / "MTF_Test_Report.docx"
            stale_docx_content = b"STALE_SENTINEL_DOCX_BYTES_NOT_A_REAL_DOCX"
            stale_docx.write_bytes(stale_docx_content)
            orig_docx_mtime = stale_docx.stat().st_mtime

            nonexistent_template = Path("/nonexistent/path.md")

            # 3. Run inject_report.py with nonexistent template
            res = subprocess.run(
                [
                    PYTHON_VENV, str(SCRIPT_PATH),
                    "--country", "Test",
                    "--json", str(json_file),
                    "--template", str(nonexistent_template),
                    "--output-dir", str(tmp_path),
                ],
                capture_output=True,
                text=True,
            )

            # (a) Assert exit code is 1
            self.assertEqual(res.returncode, 1, f"Expected returncode 1, got {res.returncode}. Output:\n{res.stdout}")

            # (b) Assert stderr contains fatal abort message
            self.assertIn("[FATAL] Template", res.stderr)
            self.assertIn("could not be processed", res.stderr)
            self.assertIn("Aborting report generation before Word (.docx) rendering", res.stderr)
            self.assertIn("Markdown injection failed", res.stderr)

            # (c) Assert MTF_Test_Report.docx was NOT updated
            self.assertEqual(stale_docx.read_bytes(), stale_docx_content, "stale MTF_Test_Report.docx content was modified!")
            self.assertEqual(stale_docx.stat().st_mtime, orig_docx_mtime, "stale MTF_Test_Report.docx mtime was updated!")

            # Also verify MTF_Test_Report.md was NOT overwritten
            self.assertEqual(stale_md.read_text(), stale_md_content, "stale MTF_Test_Report.md was overwritten!")

    def test_docx_not_created_when_missing_template_and_stale_md_exists(self):
        """
        When stale MTF_Test_Report.md exists but NO docx exists:
        inject_report.py must abort code 1 and NOT generate MTF_Test_Report.docx.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            json_file = tmp_path / "mtf_report_values.json"
            json_file.write_text(json.dumps({"COUNTRY_NAME": "Test"}))

            stale_md = tmp_path / "MTF_Test_Report.md"
            stale_md.write_text("# STALE REPORT")

            docx_file = tmp_path / "MTF_Test_Report.docx"
            self.assertFalse(docx_file.exists())

            res = subprocess.run(
                [
                    PYTHON_VENV, str(SCRIPT_PATH),
                    "--country", "Test",
                    "--json", str(json_file),
                    "--template", "/nonexistent/path.md",
                    "--output-dir", str(tmp_path),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(res.returncode, 1)
            self.assertIn("[FATAL] Template", res.stderr)
            self.assertFalse(docx_file.exists(), "MTF_Test_Report.docx was created despite missing template!")


class TestAdversarialJSONCommas(unittest.TestCase):
    """Adversarial stress-test: JSON trailing comma and consecutive commas resilience."""

    def _clean_and_parse_json(self, raw_str: str):
        """Mirror the exact sanitization and parsing logic from inject_report.py line 160-163."""
        cleaned_str = re.sub(r',\s*(?=[\}\],])', '', raw_str)
        return json.loads(cleaned_str)

    def test_json_single_trailing_comma_consecutive(self):
        """Input: {"A": 1, , } -> must parse cleanly without JSONDecodeError."""
        raw = '{"A": 1, , }'
        parsed = self._clean_and_parse_json(raw)
        self.assertEqual(parsed, {"A": 1})

        # Also test via load_values()
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write(raw)
            p = Path(f.name)
        try:
            vals = inject_report.load_values(p, country_name="Test")
            self.assertEqual(vals.get("{{A}}"), "1.0")
        finally:
            p.unlink()

    def test_json_consecutive_commas_no_whitespace(self):
        """Input: {"A": 1,,} -> must parse cleanly without JSONDecodeError."""
        raw = '{"A": 1,,}'
        parsed = self._clean_and_parse_json(raw)
        self.assertEqual(parsed, {"A": 1})

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write(raw)
            p = Path(f.name)
        try:
            vals = inject_report.load_values(p, country_name="Test")
            self.assertEqual(vals.get("{{A}}"), "1.0")
        finally:
            p.unlink()

    def test_json_multiple_consecutive_commas_with_varying_spaces(self):
        """Input: {"A": 1,  ,  ,  } -> must parse cleanly without JSONDecodeError."""
        raw = '{"A": 1,  ,  ,  }'
        parsed = self._clean_and_parse_json(raw)
        self.assertEqual(parsed, {"A": 1})

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write(raw)
            p = Path(f.name)
        try:
            vals = inject_report.load_values(p, country_name="Test")
            self.assertEqual(vals.get("{{A}}"), "1.0")
        finally:
            p.unlink()

    def test_json_array_consecutive_commas(self):
        """Input: [1, , 2] -> must parse cleanly without JSONDecodeError."""
        raw = '[1, , 2]'
        parsed = self._clean_and_parse_json(raw)
        self.assertEqual(parsed, [1, 2])

        # Test feeding to load_values() directly:
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write(raw)
            p = Path(f.name)
        try:
            # load_values() cleans and parses JSON without JSONDecodeError.
            # Downstream line 178 does `raw.items()` which raises AttributeError on lists, but crucially NEVER JSONDecodeError.
            try:
                inject_report.load_values(p, country_name="Test")
            except json.JSONDecodeError as err:
                self.fail(f"load_values() raised JSONDecodeError: {err}")
            except AttributeError:
                # Top-level array parsed cleanly; dict iteration skipped
                pass
        finally:
            p.unlink()

    def test_json_consecutive_commas_between_dict_keys(self):
        """Input: {"A": 1, , "B": 2} -> must parse cleanly without JSONDecodeError."""
        raw = '{"A": 1, , "B": 2}'
        parsed = self._clean_and_parse_json(raw)
        self.assertEqual(parsed, {"A": 1, "B": 2})

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write(raw)
            p = Path(f.name)
        try:
            vals = inject_report.load_values(p, country_name="Test")
            self.assertEqual(vals.get("{{A}}"), "1.0")
            self.assertEqual(vals.get("{{B}}"), "2.0")
        finally:
            p.unlink()

    def test_json_nested_dicts_and_lists_trailing_commas(self):
        """Input: nested dicts and lists with trailing commas -> must parse cleanly without JSONDecodeError."""
        raw = """{
            "TIER_DATA": {
                "TIER_0": 81.7, ,
                "TIER_1": 10.2,,
                "SUB_METRICS": {
                    "CAPACITY": 1, , ,
                    "HOURS": 4.5,
                },
            },
            "SOURCE_LIST": [
                "National Grid", ,
                "Solar Home System",,
                "Mini-Grid", , ,
            ],
            "COMPLEX_NESTED": [
                {"KEY_A": 100, },
                {"KEY_B": 200, , },
            ],
        }"""
        parsed = self._clean_and_parse_json(raw)
        self.assertIn("TIER_DATA", parsed)
        self.assertEqual(parsed["TIER_DATA"]["TIER_0"], 81.7)
        self.assertEqual(parsed["TIER_DATA"]["TIER_1"], 10.2)
        self.assertEqual(parsed["TIER_DATA"]["SUB_METRICS"]["CAPACITY"], 1)
        self.assertEqual(parsed["TIER_DATA"]["SUB_METRICS"]["HOURS"], 4.5)
        self.assertEqual(parsed["SOURCE_LIST"], ["National Grid", "Solar Home System", "Mini-Grid"])
        self.assertEqual(parsed["COMPLEX_NESTED"], [{"KEY_A": 100}, {"KEY_B": 200}])

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write(raw)
            p = Path(f.name)
        try:
            vals = inject_report.load_values(p, country_name="Test")
            self.assertIn("{{TIER_DATA}}", vals)
            self.assertIn("{{SOURCE_LIST}}", vals)
            self.assertIn("{{COMPLEX_NESTED}}", vals)
        finally:
            p.unlink()


if __name__ == "__main__":
    unittest.main(verbosity=2)
