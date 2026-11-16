"""
test_adversarial_m2_challenger_1.py — Empirical Challenger Test Suite for Milestone M2

Tests MTF_Report_Template.md and inject_report.py against:
1. Sequential Figure Numbering (Body & Annex 3: Figures 1..14)
2. Neutral Phrasing & Bias Scan (No directional claims, no hardcoded adjectives)
3. Currency Standardization (No '(local currency)', proper {{CURRENCY_CODE}})
4. Geographic Leaks ('Namibia' scan in template and Liberia output)
5. Injected Document Integrity on Liberia Survey Data (14/14 charts, 0 unfilled {{CHART_*}}, valid images)
6. Table Column Alignment & Structural Integrity
7. Consistency between in-text references, body figure embeds, and Annex 3
"""

import os
import re
import sys
import unittest
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "stata_pipeline" / "MTF_Report_Template.md"
INJECT_SCRIPT = REPO_ROOT / "stata_pipeline" / "scripts" / "inject_report.py"
LIBERIA_BASE_DIR = Path("/media/bryan/Bryan/MTF/9_Data analysis_MTF countries/35_Liberia(2024)/06. Data Analysis")
LIBERIA_MD_OUTPUT = LIBERIA_BASE_DIR / "Output" / "MTF_Liberia_Report.md"
PYTHON_VENV = sys.executable


class TestAdversarialFigureNumbering(unittest.TestCase):
    """Verifies strict monotonic sequence of figures 1 through 14 in body and Annex 3."""

    def setUp(self):
        self.assertTrue(TEMPLATE_PATH.exists(), f"Template not found at {TEMPLATE_PATH}")
        self.content = TEMPLATE_PATH.read_text(encoding="utf-8")
        # Split into body and annexes
        annex_marker = "## TECHNICAL ANNEXES"
        self.assertIn(annex_marker, self.content, "Missing TECHNICAL ANNEXES header")
        self.body, self.annex = self.content.split(annex_marker, 1)

    def test_body_figure_sequence(self):
        """Assert all figures in body follow strictly monotonic sequence: 1 through 13."""
        body_figs = [int(m) for m in re.findall(r'!\[Figure (\d+):', self.body)]
        self.assertEqual(
            body_figs,
            list(range(1, 14)),
            f"Body figures are not strictly monotonic 1..13: got {body_figs}"
        )

    def test_annex_figure_sequence(self):
        """Assert all figures in Annex 3 follow strictly monotonic sequence: 1 through 13."""
        annex_figs = [int(m) for m in re.findall(r'!\[Figure (\d+):', self.annex)]
        self.assertEqual(
            annex_figs,
            list(range(1, 14)),
            f"Annex figures are not strictly monotonic 1..13: got {annex_figs}"
        )

    def test_figure_syntax_validity(self):
        """Assert all figure image embeds use valid Markdown image syntax with chart token."""
        embeds = re.findall(r'!\[Figure (\d+): ([^\]]+)\]\(\{\{([^}]+)\}\}\)', self.content)
        self.assertEqual(len(embeds), 26, f"Expected 26 figure embeds (13 body + 13 annex), found {len(embeds)}")
        
        # Verify chart token mapping between body and annex
        body_embeds = embeds[:13]
        annex_embeds = embeds[13:]
        for (b_num, b_cap, b_tok), (a_num, a_cap, a_tok) in zip(body_embeds, annex_embeds):
            self.assertEqual(b_num, a_num, f"Figure number mismatch: {b_num} vs {a_num}")
            self.assertEqual(b_tok, a_tok, f"Figure token mismatch for Fig {b_num}: {b_tok} vs {a_tok}")

    def test_in_text_figure_citations_match_embedded_figures(self):
        """Assert that in-text mentions like 'Figure N' correlate with the actual figure subject."""
        # Check specific key citations
        self.assertIn("Figure 1 illustrates the distribution of households across Multi-Tier Framework electricity access tiers", self.body)
        self.assertIn("Figure 2 delineates the primary electricity technology source mix", self.body)
        self.assertIn("Figure 3 displays the progression of electricity and modern energy cooking access rates across consumption expenditure quintiles", self.body)
        self.assertIn("Figure 4 visualizes the national densification funnel", self.body)
        self.assertIn("Figure 5 presents the primary stated barriers", self.body)
        self.assertIn("Figure 6 plots the comparative cumulative willingness-to-pay demand curves", self.body)
        self.assertIn("cumulative willingness-to-pay demand curves in Figure 7", self.body)
        self.assertIn("Figure 8 illustrates the distribution of primary cookstove technologies", self.body)
        self.assertIn("Figure 9 displays the distribution of households across MECS cooking tiers", self.body)
        self.assertIn("Figure 10 displays cookstove stacking patterns", self.body)
        self.assertIn("contingent valuation demand curves in Figure 11", self.body)
        self.assertIn("Figure 12 displays comparative demographic profiles", self.body)
        self.assertIn("Figure 13 illustrates the intra-household time-use burden", self.body)


class TestAdversarialNeutralPhrasingAndBias(unittest.TestCase):
    """Scans template narrative for biased or hardcoded directional assertions."""

    def setUp(self):
        self.content = TEMPLATE_PATH.read_text(encoding="utf-8")
        # Strip comments
        narrative = re.sub(r'<!--.*?-->', '', self.content, flags=re.DOTALL)
        self.narrative = narrative

    def test_prohibited_age_comparisons(self):
        """Assert no hardcoded 'older' or 'younger' claims exist in narrative."""
        self.assertFalse(
            re.search(r'\bolder\b', self.narrative, re.IGNORECASE),
            "Found prohibited directional word 'older' in template narrative"
        )
        self.assertFalse(
            re.search(r'\byounger\b', self.narrative, re.IGNORECASE),
            "Found prohibited directional word 'younger' in template narrative"
        )

    def test_prohibited_directional_adjectives(self):
        """Assert no 'substantially lower' or 'substantially higher' claims."""
        self.assertFalse(
            re.search(r'substantially\s+lower', self.narrative, re.IGNORECASE),
            "Found 'substantially lower' in template narrative"
        )
        self.assertFalse(
            re.search(r'substantially\s+higher', self.narrative, re.IGNORECASE),
            "Found 'substantially higher' in template narrative"
        )

    def test_no_widespread_for_low_rates(self):
        """Assert 'widespread' is not used inappropriately."""
        self.assertFalse(
            re.search(r'\bwidespread\b', self.narrative, re.IGNORECASE),
            "Found word 'widespread' in template narrative"
        )

    def test_no_alarmist_adverbs(self):
        """Assert absence of alarmist or emotional framing."""
        for word in ['alarmingly', 'overwhelmingly', 'dramatically lower', 'drastically lower']:
            self.assertFalse(
                re.search(rf'\b{word}\b', self.narrative, re.IGNORECASE),
                f"Found non-neutral word '{word}' in template narrative"
            )

    def test_decliner_conditional_subpopulation_framing(self):
        """Assert that connection decline reasons explicitly condition on the subpopulation of decliners."""
        # Must contain explicit phrasing explaining that wiring cost applies AMONG decliners
        matches = re.findall(r'declining group|group of decliners|among households declining', self.narrative, re.IGNORECASE)
        self.assertGreaterEqual(
            len(matches), 3,
            "Expected at least 3 conditioned references to decliner subpopulations"
        )


class TestAdversarialCurrencyStandardization(unittest.TestCase):
    """Verifies that currency placeholders strictly conform to {{CURRENCY_CODE}}."""

    def setUp(self):
        self.content = TEMPLATE_PATH.read_text(encoding="utf-8")

    def test_no_local_currency_literal(self):
        """Assert that literal '(local currency)' does NOT exist anywhere in template."""
        self.assertNotIn(
            "(local currency)",
            self.content,
            "Found '(local currency)' literal in template"
        )

    def test_currency_code_placeholder_used(self):
        """Assert {{CURRENCY_CODE}} is properly declared and utilized."""
        self.assertIn("{{CURRENCY_CODE}}", self.content, "Missing {{CURRENCY_CODE}} placeholder in template")
        # Check spending mentions
        self.assertIn("`{{GRID_MONTHLY_SPEND_NAT}}` `{{CURRENCY_CODE}}`", self.content)


class TestAdversarialNamibiaLeaks(unittest.TestCase):
    """Verifies that 'Namibia' does not leak into the generic template or output."""

    def setUp(self):
        self.content = TEMPLATE_PATH.read_text(encoding="utf-8")
        narrative = re.sub(r'<!--.*?-->', '', self.content, flags=re.DOTALL)
        self.narrative = narrative

    def test_no_namibia_in_template_narrative(self):
        """Assert 'Namibia' is absent from template narrative."""
        self.assertNotIn("namibia", self.narrative.lower(), "Found 'Namibia' in template narrative")

    def test_no_namibia_in_liberia_markdown_output(self):
        """Assert 'Namibia' is absent from generated Liberia markdown output."""
        if LIBERIA_MD_OUTPUT.exists():
            out_content = LIBERIA_MD_OUTPUT.read_text(encoding="utf-8")
            self.assertNotIn("namibia", out_content.lower(), "Found 'Namibia' in Liberia markdown report")


class TestAdversarialInjectedDocumentIntegrity(unittest.TestCase):
    """Executes inject_report.py and validates complete artifact integrity."""

    @classmethod
    def setUpClass(cls):
        cmd = [
            PYTHON_VENV,
            str(INJECT_SCRIPT),
            "--base-dir", str(LIBERIA_BASE_DIR)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        assert res.returncode == 0, f"inject_report.py failed:\n{res.stderr}\n{res.stdout}"
        cls.injection_stdout = res.stdout
        cls.md_text = LIBERIA_MD_OUTPUT.read_text(encoding="utf-8")

    def test_zero_unfilled_chart_placeholders(self):
        """Assert 0 unfilled {{CHART_*}} tokens exist in generated report."""
        unfilled_charts = re.findall(r'\{\{CHART_[^}]+\}\}', self.md_text)
        self.assertEqual(unfilled_charts, [], f"Unfilled chart tokens found: {unfilled_charts}")

    def test_all_14_charts_embedded_and_files_exist(self):
        """Assert all 13 chart image files are referenced and exist on disk with non-zero size."""
        img_refs = re.findall(r'!\[Figure \d+: [^\]]+\]\((.+?\.(?:png|jpg|jpeg|svg))\)', self.md_text)
        self.assertEqual(len(img_refs), 26, f"Expected 26 images in report (13 body + 13 annex), found {len(img_refs)}")
        
        unique_paths = set(img_refs)
        self.assertEqual(len(unique_paths), 13, f"Expected exactly 13 unique chart paths, found {len(unique_paths)}")
        
        for p_str in unique_paths:
            p = Path(p_str)
            self.assertTrue(p.exists(), f"Referenced chart does not exist on disk: {p}")
            self.assertGreater(p.stat().st_size, 1000, f"Chart image file is suspiciously small (<1KB): {p}")

    def test_docx_report_generated_and_healthy(self):
        """Assert that MTF_Liberia_Report.docx is generated and has substantial size (>800KB)."""
        docx_path = LIBERIA_BASE_DIR / "Output" / "MTF_Liberia_Report.docx"
        self.assertTrue(docx_path.exists(), "MTF_Liberia_Report.docx was not generated")
        self.assertGreater(docx_path.stat().st_size, 800_000, "Docx file size is smaller than expected 800KB")

    def test_table_column_alignment(self):
        """Assert that Table 1.1, Table 2.1, Table 3.1, and Table 4.1 have uniform column counts."""
        # Find tables by header rows
        table_regex = re.compile(r'(\|.+?\|\n\|(?:\s*:?---+:?\s*\|)+\n(?:\|.+?\|\n)+)')
        tables = table_regex.findall(self.md_text)
        self.assertGreaterEqual(len(tables), 4, f"Expected at least 4 markdown tables, found {len(tables)}")
        
        for idx, tbl in enumerate(tables, 1):
            lines = [l.strip() for l in tbl.strip().splitlines() if l.strip()]
            header_cols = len([c for c in lines[0].split('|')[1:-1]])
            for row_num, line in enumerate(lines[2:], 3):
                row_cols = len([c for c in line.split('|')[1:-1]])
                self.assertEqual(
                    row_cols, header_cols,
                    f"Table {idx} row {row_num} has {row_cols} columns, expected {header_cols}: '{line}'"
                )


if __name__ == "__main__":
    unittest.main()
