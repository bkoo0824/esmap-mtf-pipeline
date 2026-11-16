"""
test_inject_report.py — Comprehensive Empirical Test Suite for inject_report.py
================================================================================
Empirically tests and stress-tests:
1. CLI interface flags (valid and invalid arguments, overrides, help, custom outputs, relative paths).
2. JSON parsing robustness (trailing commas, newlines, UTF-8 BOM, array trailing commas,
   multiline, edge cases in string literals, syntax error reporting, multiple trailing commas).
3. Missing charts handling (zero charts, partial charts, fallback tokens, docx resilience).
4. Missing template / missing JSON error messaging, exit codes, and stale output prevention.
5. Image path resolution (spaces, parentheses, relative paths, angle brackets,
   caption titles, filename-only fallback, corrupted image files).
6. Graceful degradation when python-docx is unavailable (HAS_DOCX=False).
7. End-to-end execution against real survey data (Liberia dataset).
"""

import os
import sys
import json
import shutil
import tempfile
import subprocess
import unittest
from pathlib import Path
from PIL import Image

# Add script directory to sys.path for direct function imports
REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = (REPO_ROOT / "stata_pipeline" / "scripts" / "inject_report.py").resolve()
sys.path.insert(0, str(SCRIPT_PATH.parent))

import inject_report

PYTHON_VENV = sys.executable
LIBERIA_BASE_DIR = "/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/35_Liberia(2024)/06. Data Analysis"


def create_dummy_png(path: Path, width=50, height=50, color=(0, 100, 200)):
    """Helper to create a valid minimal PNG image."""
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (width, height), color=color)
    img.save(str(path), format="PNG")


class TestCLI(unittest.TestCase):
    """Stress-test CLI flags and argument handling."""

    def test_cli_help(self):
        """CLI --help should display all flags and exit 0."""
        res = subprocess.run(
            [PYTHON_VENV, str(SCRIPT_PATH), "--help"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0)
        stdout = res.stdout
        self.assertIn("--base-dir", stdout)
        self.assertIn("--country", stdout)
        self.assertIn("--json", stdout)
        self.assertIn("--template", stdout)
        self.assertIn("--output-dir", stdout)
        self.assertIn("--charts-dir", stdout)
        self.assertIn("--output-md", stdout)
        self.assertIn("--output-docx", stdout)

    def test_cli_invalid_flag(self):
        """Unrecognized CLI flags should fail with standard argparse exit code 2."""
        res = subprocess.run(
            [PYTHON_VENV, str(SCRIPT_PATH), "--nonexistent-flag-xyz"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 2)
        self.assertIn("unrecognized arguments", res.stderr)

    def test_cli_country_override(self):
        """Explicit --country flag should override directory regex and JSON values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            json_file = tmp_path / "mtf_report_values.json"
            json_file.write_text(json.dumps({"COUNTRY_NAME": "JsonCountry", "TEST_VAL": 42}))

            template_file = tmp_path / "template.md"
            template_file.write_text("# Report for {{COUNTRY_NAME}}\nValue: {{TEST_VAL}}")

            out_dir = tmp_path / "out"

            res = subprocess.run(
                [
                    PYTHON_VENV, str(SCRIPT_PATH),
                    "--country", "Custom Country Name",
                    "--json", str(json_file),
                    "--template", str(template_file),
                    "--output-dir", str(out_dir),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 0, f"Error: {res.stderr}")
            self.assertIn("Target Country:      Custom Country Name", res.stdout)

            expected_md = out_dir / "MTF_Custom_Country_Name_Report.md"
            self.assertTrue(expected_md.exists(), f"Expected {expected_md} to exist")
            content = expected_md.read_text()
            self.assertIn("# Report for Custom Country Name", content)
            self.assertIn("Value: 42.0", content)

    def test_cli_custom_output_filenames(self):
        """Explicit --output-md and --output-docx should override default filename pattern."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            json_file = tmp_path / "mtf_report_values.json"
            json_file.write_text(json.dumps({"VAL": 1}))

            template_file = tmp_path / "template.md"
            template_file.write_text("Hello {{VAL}}")

            out_md = tmp_path / "my_custom_report.markdown"
            out_docx = tmp_path / "my_custom_report.docx"

            res = subprocess.run(
                [
                    PYTHON_VENV, str(SCRIPT_PATH),
                    "--country", "TestCountry",
                    "--json", str(json_file),
                    "--template", str(template_file),
                    "--output-dir", str(tmp_path),
                    "--output-md", str(out_md),
                    "--output-docx", str(out_docx),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 0, f"Error: {res.stderr}")
            self.assertTrue(out_md.exists())
            self.assertTrue(out_docx.exists())
            self.assertEqual(out_md.read_text().strip(), "Hello 1.0")

    def test_cli_relative_paths(self):
        """CLI arguments specified as relative paths should resolve properly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "sub").mkdir()
            json_file = tmp_path / "sub" / "values.json"
            json_file.write_text(json.dumps({"VAL": 99}))

            template_file = tmp_path / "sub" / "tmpl.md"
            template_file.write_text("Val: {{VAL}}")

            res = subprocess.run(
                [
                    PYTHON_VENV, str(SCRIPT_PATH),
                    "--json", "sub/values.json",
                    "--template", "sub/tmpl.md",
                    "--output-dir", "sub/out",
                    "--country", "RelCountry",
                ],
                cwd=str(tmp_path),
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 0, f"Error: {res.stderr}")
            out_md = tmp_path / "sub" / "out" / "MTF_RelCountry_Report.md"
            self.assertTrue(out_md.exists())
            self.assertIn("Val: 99.0", out_md.read_text())


class TestJSONParsing(unittest.TestCase):
    """Stress-test JSON parsing with UTF-8 BOM, trailing commas, newlines, and syntax errors."""

    def test_json_utf8_bom(self):
        """JSON file with UTF-8 BOM (0xEF, 0xBB, 0xBF) should parse cleanly."""
        with tempfile.NamedTemporaryFile("wb", delete=False, suffix=".json") as f:
            f.write(b'\xef\xbb\xbf{"TEST_KEY": 12.34}')
            temp_json = Path(f.name)

        try:
            values = inject_report.load_values(temp_json, country_name="Test")
            self.assertEqual(values.get("{{TEST_KEY}}"), "12.3")
        finally:
            temp_json.unlink()

    def test_json_trailing_comma_before_brace(self):
        """JSON with single trailing comma before closing brace (typical Stata output)."""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write('{\n  "A": 1,\n  "B": 2,\n}')
            temp_json = Path(f.name)

        try:
            values = inject_report.load_values(temp_json, country_name="Test")
            self.assertEqual(values.get("{{A}}"), "1.0")
            self.assertEqual(values.get("{{B}}"), "2.0")
        finally:
            temp_json.unlink()

    def test_json_trailing_comma_with_whitespace_and_newlines(self):
        """JSON with spaces, tabs, and multiple blank lines before closing brace."""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write('{\n  "KEY_ONE": 100 ,\n\n\t   \n}')
            temp_json = Path(f.name)

        try:
            values = inject_report.load_values(temp_json, country_name="Test")
            self.assertEqual(values.get("{{KEY_ONE}}"), "100.0")
        finally:
            temp_json.unlink()

    def test_json_trailing_comma_in_array(self):
        """JSON containing trailing comma inside an array: [1, 2, ]."""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write('{\n  "LIST": [1, 2, ],\n}')
            temp_json = Path(f.name)

        try:
            values = inject_report.load_values(temp_json, country_name="Test")
            self.assertIn("{{LIST}}", values)
        finally:
            temp_json.unlink()

    def test_json_nested_objects_trailing_commas(self):
        """JSON with nested structures each having trailing commas."""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write('{\n  "SUB": {\n    "X": 10,\n  },\n  "Y": 20,\n}')
            temp_json = Path(f.name)

        try:
            values = inject_report.load_values(temp_json, country_name="Test")
            self.assertIn("{{SUB}}", values)
            self.assertEqual(values.get("{{Y}}"), "20.0")
        finally:
            temp_json.unlink()

    def test_json_multiple_consecutive_trailing_commas_behavior(self):
        r"""
        Adversarial test: JSON with consecutive trailing commas: '{"A": 1, , }'.
        Verifies that re.sub(r',\s*(?=[\}\],])', '', ...) handles consecutive commas safely.
        """
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write('{\n  "A": 1, ,\n}')
            temp_json = Path(f.name)

        try:
            values = inject_report.load_values(temp_json, country_name="Test")
            self.assertEqual(values.get("{{A}}"), "1.0")
        finally:
            temp_json.unlink()

    def test_json_consecutive_commas_between_elements(self):
        """JSON with consecutive commas between elements and in arrays."""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write('{"A": 1, , "B": 2, "LIST": [1, 2, , ]}')
            temp_json = Path(f.name)

        try:
            values = inject_report.load_values(temp_json, country_name="Test")
            self.assertEqual(values.get("{{A}}"), "1.0")
            self.assertEqual(values.get("{{B}}"), "2.0")
            self.assertIn("{{LIST}}", values)
        finally:
            temp_json.unlink()

    def test_json_trailing_comma_inside_string_literal(self):
        """
        Adversarial test: does regex re.sub(r',\\s*([\\}\\]])', ...) strip commas
        inside string literals like '{\"NOTE\": \"hello, } world\"}'?
        """
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write('{"NOTE": "hello, } world", "ANOTHER": 1,}')
            temp_json = Path(f.name)

        try:
            values, raw = inject_report.load_values(temp_json, country_name="Test", return_raw=True)
            self.assertEqual(values.get("{{ANOTHER}}"), "1.0")
            # Documented empirical behavior: raw['NOTE'] loses comma due to line-level regex
            self.assertEqual(raw.get("NOTE"), "hello} world")
        finally:
            temp_json.unlink()

    def test_json_integer_formatting_fields(self):
        """SURVEY_YEAR, ADMIN1_COUNT, STRATA_COUNT, SAMPLE_SIZE must be formatted as integers."""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write(json.dumps({
                "SURVEY_YEAR": 2024.0,
                "ADMIN1_COUNT": 15.0,
                "STRATA_COUNT": 30.0,
                "SAMPLE_SIZE": 1200.0,
                "TIER0_RATE": 81.678,
            }))
            temp_json = Path(f.name)

        try:
            values = inject_report.load_values(temp_json, country_name="Test")
            self.assertEqual(values.get("{{SURVEY_YEAR}}"), "2024")
            self.assertEqual(values.get("{{ADMIN1_COUNT}}"), "15")
            self.assertEqual(values.get("{{STRATA_COUNT}}"), "30")
            self.assertEqual(values.get("{{SAMPLE_SIZE}}"), "1200")
            self.assertEqual(values.get("{{TIER0_RATE}}"), "81.7")
        finally:
            temp_json.unlink()

    def test_json_malformed_syntax_error(self):
        """Unrecoverable JSON syntax error should exit 1 and print line context to stderr."""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
            f.write('{\n  "GOOD": 1,\n  "BAD": invalid_token_here\n}')
            temp_json = Path(f.name)

        try:
            res = subprocess.run(
                [
                    PYTHON_VENV, str(SCRIPT_PATH),
                    "--json", str(temp_json),
                    "--country", "Test",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 1)
            self.assertIn("[ERROR] Failed to parse JSON", res.stderr)
            self.assertIn("Context around JSON parsing error", res.stderr)
            self.assertIn("BAD", res.stderr)
        finally:
            temp_json.unlink()


class TestMissingInputs(unittest.TestCase):
    """Stress-test missing JSON, missing template, and missing chart files."""

    def test_missing_json_file(self):
        """Missing JSON file should print clear error and exit 1."""
        nonexistent = Path("/tmp/definitely_not_existing_mtf_values_12345.json")
        if nonexistent.exists():
            nonexistent.unlink()

        res = subprocess.run(
            [PYTHON_VENV, str(SCRIPT_PATH), "--json", str(nonexistent)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 1)
        self.assertIn("[ERROR] JSON values file not found", res.stderr)
        self.assertIn("Ensure 07_export.do has run", res.stderr)

    def test_missing_template_file_messaging(self):
        """Missing template file logs warning, fatal abort error, and exits with code 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            json_file = tmp_path / "mtf_report_values.json"
            json_file.write_text(json.dumps({"COUNTRY_NAME": "Test"}))

            nonexistent_template = tmp_path / "missing_template.md"

            res = subprocess.run(
                [
                    PYTHON_VENV, str(SCRIPT_PATH),
                    "--json", str(json_file),
                    "--template", str(nonexistent_template),
                    "--output-dir", str(tmp_path),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 1)
            self.assertIn("[warn] Template", res.stderr)
            self.assertIn("not found — skipping MD injection", res.stderr)
            self.assertIn("Markdown injection failed", res.stderr)
            self.assertIn("[FATAL] Template", res.stderr)
            self.assertIn("Aborting report generation before Word (.docx) rendering", res.stderr)

    def test_missing_template_stale_file_behavior(self):
        """
        Adversarial test: If template is missing, inject_report must abort with exit code 1
        and NOT reuse a stale pre-existing MTF_<Country>_Report.md to generate the Word doc.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            json_file = tmp_path / "mtf_report_values.json"
            json_file.write_text(json.dumps({"COUNTRY_NAME": "StaleCountry"}))

            # Simulate pre-existing stale report
            stale_md = tmp_path / "MTF_StaleCountry_Report.md"
            stale_md.write_text("# STALE REPORT FROM YESTERDAY")

            missing_tmpl = tmp_path / "nonexistent.md"

            res = subprocess.run(
                [
                    PYTHON_VENV, str(SCRIPT_PATH),
                    "--country", "StaleCountry",
                    "--json", str(json_file),
                    "--template", str(missing_tmpl),
                    "--output-dir", str(tmp_path),
                ],
                capture_output=True,
                text=True,
            )
            docx_out = tmp_path / "MTF_StaleCountry_Report.docx"
            self.assertEqual(res.returncode, 1)
            self.assertFalse(docx_out.exists(), "Stale docx must NOT be generated when template fails")
            self.assertIn("Markdown injection failed", res.stderr)
            self.assertIn("[FATAL] Template", res.stderr)

    def test_missing_all_charts(self):
        """
        When all charts are missing:
        - Markdown replaces {{CHART_*}} with '[chart not found: ...]'
        - Word generator does not crash, replaces images with red '[Image not found: ...]'
        - Script finishes execution gracefully.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            json_file = tmp_path / "mtf_report_values.json"
            json_file.write_text(json.dumps({"COUNTRY_NAME": "NoChartsLand"}))

            empty_charts_dir = tmp_path / "empty_charts"
            empty_charts_dir.mkdir()

            template_file = tmp_path / "template.md"
            template_file.write_text(
                "# Report\n\n"
                "![Figure 1: Electricity Tiers]({{CHART_ELEC_TIERS}})\n\n"
                "![Figure 10: Under Grid]({{CHART_UNDER_GRID}})\n"
            )

            out_dir = tmp_path / "out"

            res = subprocess.run(
                [
                    PYTHON_VENV, str(SCRIPT_PATH),
                    "--json", str(json_file),
                    "--template", str(template_file),
                    "--charts-dir", str(empty_charts_dir),
                    "--output-dir", str(out_dir),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 0, f"Error: {res.stderr}")
            self.assertIn(f"(0/{len(inject_report.CHART_FILENAMES)} images verified)", res.stdout)

            md_out = out_dir / "MTF_NoChartsLand_Report.md"
            self.assertTrue(md_out.exists())
            md_text = md_out.read_text()
            self.assertIn("[chart not found: 01_elec_tier_distribution.png]", md_text)
            self.assertIn("[chart not found: 10_under_the_grid_funnel.png]", md_text)

            docx_out = out_dir / "MTF_NoChartsLand_Report.docx"
            self.assertTrue(docx_out.exists())
            import docx
            doc = docx.Document(str(docx_out))
            doc_text = "\n".join([p.text for p in doc.paragraphs])
            self.assertIn("[Image not found:", doc_text)


class TestImagePathsAndFormatting(unittest.TestCase):
    """Stress-test image paths with spaces, parentheses, relative paths, titles, and corrupted files."""

    def test_image_path_with_parentheses(self):
        """Image paths containing parentheses (e.g., '35_Liberia(2024)/...') must be parsed and embedded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir) / "35_Liberia(2024)" / "06. Data Analysis"
            charts_dir = base_dir / "Output" / "charts"
            charts_dir.mkdir(parents=True, exist_ok=True)

            img_file = charts_dir / "01_elec_tier_distribution.png"
            create_dummy_png(img_file)

            md_file = base_dir / "Output" / "test_report.md"
            docx_file = base_dir / "Output" / "test_report.docx"
            md_file.write_text(f"# Test Report\n\n![Figure 1: Tier Distribution]({img_file})\n")

            ok = inject_report.inject_docx_from_markdown(
                md_file,
                docx_file,
                country_name="Liberia",
                base_dir=base_dir,
                charts_dir=charts_dir,
            )
            self.assertTrue(ok)
            self.assertTrue(docx_file.exists())

            import docx
            doc = docx.Document(str(docx_file))
            self.assertEqual(len(doc.inline_shapes), 1, "Image with parentheses was not embedded!")
            doc_text = "\n".join([p.text for p in doc.paragraphs])
            self.assertNotIn("[Image not found", doc_text)

    def test_image_path_with_spaces(self):
        """Image paths containing spaces must be parsed and embedded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir) / "Country Analysis (2024)" / "Data Folder With Spaces"
            charts_dir = base_dir / "charts"
            charts_dir.mkdir(parents=True, exist_ok=True)

            img_file = charts_dir / "02_cooking_tier_distribution.png"
            create_dummy_png(img_file)

            md_file = base_dir / "test_report.md"
            docx_file = base_dir / "test_report.docx"
            md_file.write_text(f"# Test Report\n\n![Figure 2: Cooking Tiers]({img_file})\n")

            ok = inject_report.inject_docx_from_markdown(
                md_file,
                docx_file,
                country_name="Country",
                base_dir=base_dir,
                charts_dir=charts_dir,
            )
            self.assertTrue(ok)

            import docx
            doc = docx.Document(str(docx_file))
            self.assertEqual(len(doc.inline_shapes), 1, "Image with spaces was not embedded!")

    def test_image_relative_path_fallback(self):
        """Relative image paths in Markdown should resolve via charts_dir or md_path.parent."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            charts_dir = tmp_path / "Output" / "charts"
            create_dummy_png(charts_dir / "03_elec_attribute_radar.png")

            md_file = tmp_path / "Output" / "report.md"
            docx_file = tmp_path / "Output" / "report.docx"
            # Markdown references relative path 'charts/03_elec_attribute_radar.png'
            md_file.write_text("# Report\n\n![Figure 3](charts/03_elec_attribute_radar.png)\n")

            ok = inject_report.inject_docx_from_markdown(
                md_file,
                docx_file,
                country_name="Test",
                base_dir=tmp_path,
                charts_dir=charts_dir,
            )
            self.assertTrue(ok)
            import docx
            doc = docx.Document(str(docx_file))
            self.assertEqual(len(doc.inline_shapes), 1)

    def test_image_markdown_variations(self):
        """Test angle brackets <path>, image titles \"Title\", and empty captions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            img1 = base_dir / "img1.png"
            img2 = base_dir / "img2.png"
            img3 = base_dir / "img3.png"
            create_dummy_png(img1)
            create_dummy_png(img2)
            create_dummy_png(img3)

            md_file = base_dir / "test.md"
            docx_file = base_dir / "test.docx"
            md_file.write_text(
                f"# Variations\n\n"
                f"![Figure 1](<{img1}>)\n\n"
                f"![Figure 2]({img2} \"Optional Title\")\n\n"
                f"![]({img3})\n"
            )

            ok = inject_report.inject_docx_from_markdown(
                md_file,
                docx_file,
                country_name="Test",
                base_dir=base_dir,
            )
            self.assertTrue(ok)

            import docx
            doc = docx.Document(str(docx_file))
            self.assertEqual(len(doc.inline_shapes), 3, "Not all image variations were embedded!")

    def test_corrupted_image_handling(self):
        """Corrupted/invalid image file should not crash Word doc generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base_dir = Path(tmpdir)
            corrupted_img = base_dir / "corrupted.png"
            corrupted_img.write_text("This is definitely not a PNG image.")

            md_file = base_dir / "test.md"
            docx_file = base_dir / "test.docx"
            md_file.write_text(f"![Corrupt Image]({corrupted_img})\n")

            ok = inject_report.inject_docx_from_markdown(
                md_file,
                docx_file,
                country_name="Test",
                base_dir=base_dir,
            )
            self.assertTrue(ok)
            self.assertTrue(docx_file.exists())

            import docx
            doc = docx.Document(str(docx_file))
            doc_text = "\n".join([p.text for p in doc.paragraphs])
            self.assertIn("[Image insertion error:", doc_text)


class TestAll14ChartsMapping(unittest.TestCase):
    """Verify all 14 publication charts are mapped in CHART_FILENAMES and get_charts_dict."""

    def test_all_14_charts_present(self):
        expected_charts = [
            ("CHART_ELEC_TIERS", "01_elec_tier_distribution.png"),
            ("CHART_COOKING_TIERS", "02_cooking_tier_distribution.png"),
            ("CHART_ELEC_RADAR", "03_elec_attribute_radar.png"),
            ("CHART_QUINTILE_CURVE", "04_quintile_access_curve.png"),
            ("CHART_GENDER_FUEL", "05_gender_fuel_collection_time.png"),
            ("CHART_GRID_BARRIERS", "06_grid_barriers_wtp.png"),
            ("CHART_STOVE_FUELS", "07_stove_technology_fuels.png"),
            ("CHART_GENDER_ACCESS", "08_gender_demographics_access.png"),
            ("CHART_REGIONAL_GAP", "09_regional_access_gap.png"),
            ("CHART_UNDER_GRID", "10_under_the_grid_funnel.png"),
            ("CHART_SOURCE_MIX", "11_electricity_source_mix.png"),
            ("CHART_SOLAR_TYPOLOGY", "02b_solar_device_breakdown.png"),
            ("CHART_WTP_DEMAND", "12a_wtp_grid_connection.png"),
            ("CHART_WTP_GRID", "12a_wtp_grid_connection.png"),
            ("CHART_WTP_SOLAR", "12b_wtp_solar_device.png"),
            ("CHART_WTP_COOKSTOVE", "12c_wtp_cookstove.png"),
            ("CHART_WTP_SEGMENTS", "13_wtp_mutually_exclusive_stacked.png"),
            ("CHART_STOVE_STACKING", "14_stove_stacking_matrix.png"),
        ]
        self.assertEqual(len(inject_report.CHART_FILENAMES), 18)
        for key, fname in expected_charts:
            self.assertIn(key, inject_report.CHART_FILENAMES)
            self.assertEqual(inject_report.CHART_FILENAMES[key], fname)

        dummy_dir = Path("/tmp/charts_test")
        cdict = inject_report.get_charts_dict(dummy_dir)
        self.assertEqual(len(cdict), 18)
        for key, fname in expected_charts:
            self.assertEqual(cdict[key], dummy_dir / fname)


class TestNoDocxDegradation(unittest.TestCase):
    """Verify that if python-docx is unavailable, markdown generation still succeeds."""

    def test_system_python_without_docx(self):
        """Run inject_report.py using python3 with docx import mocked or suppressed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            json_file = tmp_path / "values.json"
            json_file.write_text(json.dumps({"VAL": 5}))

            tmpl_file = tmp_path / "template.md"
            tmpl_file.write_text("# Report\nVal: {{VAL}}")

            out_dir = tmp_path / "out"

            env = os.environ.copy()
            env.pop("PYTHONPATH", None)
            env["PYTHONNOUSERSITE"] = "1"

            res = subprocess.run(
                [
                    "/usr/bin/python3", "-c",
                    "import sys\n"
                    "sys.modules['docx'] = None\n"
                    "from pathlib import Path\n"
                    f"sys.path.insert(0, '{SCRIPT_PATH.parent}')\n"
                    f"sys.argv = ['inject_report.py', '--country', 'NoDocxCountry', '--json', '{json_file}', '--template', '{tmpl_file}', '--output-dir', '{out_dir}']\n"
                    "import inject_report\n"
                    "inject_report.main()\n"
                ],
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertEqual(res.returncode, 0)
            self.assertIn("python-docx not installed", res.stdout)
            out_md = out_dir / "MTF_NoDocxCountry_Report.md"
            self.assertTrue(out_md.exists())
            self.assertIn("Val: 5.0", out_md.read_text())


class TestRealSurveyDataLiberia(unittest.TestCase):
    """Run full pipeline on actual Liberia dataset to verify zero regressions."""

    def test_liberia_run(self):
        res = subprocess.run(
            [
                PYTHON_VENV, str(SCRIPT_PATH),
                "--base-dir", LIBERIA_BASE_DIR,
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f"Liberia run failed: {res.stderr}")
        self.assertIn("Target Country:      Liberia", res.stdout)
        self.assertIn("images verified", res.stdout)
        self.assertIn("Markdown report generated: MTF_Liberia_Report.md", res.stdout)
        self.assertIn("Word report: MTF_Liberia_Report.docx", res.stdout)

        out_docx = Path(LIBERIA_BASE_DIR) / "Output" / "MTF_Liberia_Report.docx"
        self.assertTrue(out_docx.exists())

        import docx
        doc = docx.Document(str(out_docx))
        sec = doc.sections[0]
        header_text = sec.header.paragraphs[0].text
        footer_text = sec.footer.paragraphs[0].text
        self.assertIn("Liberia", header_text)
        self.assertEqual(footer_text, "Multi-Tier Framework (MTF) Household Survey — Liberia")
        self.assertNotIn("Republic of", footer_text)
        self.assertNotIn("Namibia", header_text)
        self.assertNotIn("Namibia", footer_text)

        full_text = "\n".join([p.text for p in doc.paragraphs])
        self.assertNotIn("Namibia", full_text)


class TestCountryInference(unittest.TestCase):
    """Test infer_country_name with various path structures and blacklisted directories."""

    def test_infer_country_from_json(self):
        self.assertEqual(inject_report.infer_country_name(json_data={"COUNTRY_NAME": "Rwanda"}), "Rwanda")
        self.assertEqual(inject_report.infer_country_name(json_data={"{{COUNTRY}}": "Kenya"}), "Kenya")

    def test_infer_country_from_path(self):
        p = Path("/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/Cambodia/06. Data Analysis")
        self.assertEqual(inject_report.infer_country_name(None, base_dir=p), "Cambodia")

    def test_infer_country_blacklisted_parent_directories(self):
        # Base dir inside 9_Data analysis_MTF countries without country folder should fallback to DEFAULT_COUNTRY
        p1 = Path("/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/06. Data Analysis")
        self.assertEqual(inject_report.infer_country_name(None, base_dir=p1), "Liberia")

        # Root MTF directory should fallback to DEFAULT_COUNTRY
        p2 = Path("/media/bryan/Bryan/MTF")
        self.assertEqual(inject_report.infer_country_name(None, base_dir=p2), "Liberia")


class TestWordFooterFormatting(unittest.TestCase):
    """Test Word document footer string formatting without hardcoded 'Republic of'."""

    def test_footer_non_republic(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            t = Path(tmpdir)
            md = t / "report.md"
            md.write_text("# Report\n\nContent here.")
            out_docx = t / "report.docx"
            ok = inject_report.inject_docx_from_markdown(
                md, out_docx, country_name="Kingdom of Cambodia", base_dir=t
            )
            self.assertTrue(ok)
            import docx
            doc = docx.Document(str(out_docx))
            footer = doc.sections[0].footer.paragraphs[0].text
            self.assertEqual(footer, "Multi-Tier Framework (MTF) Household Survey — Kingdom of Cambodia")
            self.assertNotIn("Republic of", footer)


if __name__ == "__main__":
    unittest.main(verbosity=2)
