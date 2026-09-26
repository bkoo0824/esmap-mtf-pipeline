"""
inject_report.py — MTF Namibia Automated Report Injector
==========================================================
Reads:
  - mtf_report_values.json  (key-value pairs from 07_export.do)
  - MTF_Report_Template.md  (Markdown with {{PLACEHOLDER}} tags)
  - MTF_Report_Template.docx (Word with {{PLACEHOLDER}} tags)
  - 5 PNG charts from visualize.py

Writes:
  - Output/streamlined/MTF_Liberia_Report.md
  - Output/streamlined/MTF_Liberia_Report.docx

Run after visualize.py:
  python3 scripts/inject_report.py

Requires: python-docx, Pillow
  pip install python-docx pillow
"""

import sys
import json
import re
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml import parse_xml, OxmlElement
    from docx.oxml.ns import nsdecls, qn
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False
    Document = Inches = Pt = RGBColor = WD_ALIGN_PARAGRAPH = WD_TABLE_ALIGNMENT = parse_xml = OxmlElement = nsdecls = qn = None
    print("[warn] python-docx not installed — Word injection skipped", file=sys.stderr)

# ─── PATHS ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR    = Path(__file__).parent
DO_FILE_DIR   = SCRIPT_DIR.parent
BASE_DIR      = DO_FILE_DIR.parent
OUTPUT_DIR    = BASE_DIR / "Output" / "streamlined" if (BASE_DIR / "Output" / "streamlined").exists() else BASE_DIR / "Output"
CHARTS_DIR    = OUTPUT_DIR / "charts"

JSON_PATH     = OUTPUT_DIR / "mtf_report_values.json"
MD_TEMPLATE   = DO_FILE_DIR / "MTF_Report_Template.md"
DOCX_TEMPLATE = DO_FILE_DIR / "MTF_Report_Template.docx"

MD_OUT        = OUTPUT_DIR / "MTF_Liberia_Report.md"
DOCX_OUT      = OUTPUT_DIR / "MTF_Liberia_Report.docx"

CHARTS = {
    "CHART_ELEC_TIERS"     : CHARTS_DIR / "01_elec_tier_distribution.png",
    "CHART_COOKING_TIERS"  : CHARTS_DIR / "02_cooking_tier_distribution.png",
    "CHART_ELEC_RADAR"     : CHARTS_DIR / "03_elec_attribute_radar.png",
    "CHART_QUINTILE_CURVE" : CHARTS_DIR / "04_quintile_access_curve.png",
    "CHART_GENDER_FUEL"    : CHARTS_DIR / "05_gender_fuel_collection_time.png",
    "CHART_GRID_BARRIERS"  : CHARTS_DIR / "06_grid_barriers_wtp.png",
    "CHART_STOVE_FUELS"    : CHARTS_DIR / "07_stove_technology_fuels.png",
    "CHART_GENDER_ACCESS"  : CHARTS_DIR / "08_gender_demographics_access.png",
    "CHART_REGIONAL_GAP"   : CHARTS_DIR / "09_regional_access_gap.png",
}


# ─── LOAD JSON VALUES ─────────────────────────────────────────────────────────
def load_values() -> dict:
    """Load JSON, normalise keys to {{KEY}} format, add chart paths."""
    if not JSON_PATH.exists():
        print(f"[ERROR] {JSON_PATH} not found.", file=sys.stderr)
        sys.exit(1)

    with open(JSON_PATH, encoding="utf-8") as f:
        raw_str = f.read().strip()
    raw_str = re.sub(r',\s*\}', '}', raw_str)
    raw = json.loads(raw_str)

    values = {}
    for k, v in raw.items():
        # Support keys with or without {{}}
        clean_key = k.strip("{} ")
        placeholder = f"{{{{{clean_key}}}}}"
        # Format numbers: 1 decimal place for percentages
        try:
            fv = float(v)
            values[placeholder] = f"{fv:.1f}"
        except (ValueError, TypeError):
            values[placeholder] = str(v)

    # Chart paths (for MD injection as image links)
    for k, p in CHARTS.items():
        values[f"{{{{{k}}}}}"] = str(p) if p.exists() else f"[chart not found: {p.name}]"

    return values


# ─── INJECT MARKDOWN ──────────────────────────────────────────────────────────
def inject_markdown(values: dict):
    if not MD_TEMPLATE.exists():
        print(f"[warn] {MD_TEMPLATE} not found — skipping MD injection", file=sys.stderr)
        return

    text = MD_TEMPLATE.read_text(encoding="utf-8")
    replaced = 0

    for placeholder, val in values.items():
        if placeholder in text:
            text = text.replace(placeholder, val)
            replaced += 1

    # Report remaining unfilled placeholders
    remaining = re.findall(r"\{\{[A-Z_0-9]+\}\}", text)
    if remaining:
        print(f"  [warn] {len(remaining)} unfilled placeholders in MD: {set(remaining)}")

    MD_OUT.write_text(text, encoding="utf-8")
    print(f"  ✓ Markdown report: {MD_OUT.name} ({replaced} values injected)")


# ─── INJECT WORD DOCUMENT ─────────────────────────────────────────────────────
# Color palette: World Bank ESMAP Standards
if HAS_DOCX:
    COLOR_NAVY     = RGBColor(0, 34, 68)       # #002244
    COLOR_ACCENT   = RGBColor(0, 119, 153)     # #007799
    COLOR_CHARCOAL = RGBColor(34, 34, 34)      # #222222
    COLOR_MUTED    = RGBColor(100, 100, 100)   # #666666
    COLOR_WHITE    = RGBColor(255, 255, 255)   # #FFFFFF
else:
    COLOR_NAVY = COLOR_ACCENT = COLOR_CHARCOAL = COLOR_MUTED = COLOR_WHITE = None

HEX_NAVY     = "002244"
HEX_ACCENT   = "007799"
HEX_LIGHT_BG = "F0F4F8"
HEX_ALT_ROW  = "F6F8FA"
HEX_BORDER   = "CCCCCC"


def _set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner padding for a table cell in twips."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def _set_cell_shading(cell, color_hex):
    """Set background color of a cell."""
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)


def _set_callout_borders(cell, border_color_hex=HEX_NAVY, border_size=24):
    """Left thick border, no other borders for callout box."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), str(border_size))
    left.set(qn('w:space'), '0')
    left.set(qn('w:color'), border_color_hex)
    tcBorders.append(left)
    for side in ['top', 'bottom', 'right']:
        b = OxmlElement(f'w:{side}')
        b.set(qn('w:val'), 'none')
        tcBorders.append(b)
    tcPr.append(tcBorders)


def _set_table_borders(table, border_color_hex=HEX_BORDER):
    """Set clean borders on a table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="{border_color_hex}"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{HEX_NAVY}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color_hex}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def _add_formatted_runs(paragraph, text, base_color=None, base_size=None):
    """Parse inline **bold**, *italic*, and `code` into formatted Word runs."""
    if not HAS_DOCX:
        return
    if base_color is None:
        base_color = COLOR_CHARCOAL
    if base_size is None:
        base_size = Pt(10.0)
    tokens = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)', text)
    for token in tokens:
        if not token:
            continue
        if token.startswith('**') and token.endswith('**'):
            run = paragraph.add_run(token[2:-2])
            run.bold = True
            run.font.color.rgb = base_color
            run.font.size = base_size
        elif token.startswith('*') and token.endswith('*'):
            run = paragraph.add_run(token[1:-1])
            run.italic = True
            run.font.color.rgb = base_color
            run.font.size = base_size
        elif token.startswith('`') and token.endswith('`'):
            run = paragraph.add_run(token[1:-1])
            run.bold = True
            run.font.name = 'Consolas'
            run.font.color.rgb = COLOR_NAVY
            run.font.size = Pt(base_size.pt - 0.5)
        else:
            run = paragraph.add_run(token)
            run.font.color.rgb = base_color
            run.font.size = base_size


def inject_docx_from_markdown(md_path: Path, docx_path: Path):
    """
    Renders the fully injected Markdown report directly into a publication-grade Word document (.docx).
    Follows World Bank ESMAP styling guidelines.
    """
    if not HAS_DOCX:
        print("[warn] python-docx not installed — Word report skipped", file=sys.stderr)
        return

    doc = Document()
    
    # 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.different_first_page_header_footer = True
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("ESMAP | Beyond Connections: Namibia Energy Access Diagnostic Report")
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = COLOR_MUTED
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Multi-Tier Framework (MTF) Household Survey — Republic of Namibia")
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = COLOR_MUTED

    md_content = md_path.read_text(encoding='utf-8')
    lines = md_content.splitlines()
    
    i = 0
    n = len(lines)
    
    while i < n:
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
            
        if line in ['---', '***', '___']:
            i += 1
            continue
            
        # Images: ![caption](path)
        img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line)
        if img_match:
            caption, img_path_str = img_match.groups()
            img_path = Path(img_path_str)
            if not img_path.exists():
                cand = BASE_DIR / img_path_str.lstrip('/')
                if cand.exists():
                    img_path = cand
            if img_path.exists():
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(12)
                p_img.paragraph_format.space_after = Pt(4)
                p_img.add_run().add_picture(str(img_path), width=Inches(5.6))
                
                p_cap = doc.add_paragraph()
                p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_cap.paragraph_format.space_before = Pt(2)
                p_cap.paragraph_format.space_after = Pt(14)
                c_run = p_cap.add_run(caption)
                c_run.italic = True
                c_run.font.size = Pt(9.5)
                c_run.font.color.rgb = COLOR_MUTED
            else:
                p_err = doc.add_paragraph(f"[Image not found: {img_path_str}]")
                p_err.runs[0].font.color.rgb = RGBColor(200, 0, 0)
            i += 1
            continue
            
        # Headings
        if line.startswith('# '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(line[2:].strip())
            run.bold = True
            run.font.size = Pt(22)
            run.font.color.rgb = COLOR_NAVY
            i += 1
            continue
            
        if line.startswith('## '):
            h_text = line[3:].strip()
            if h_text.startswith('CHAPTER') or h_text in ['EXECUTIVE SUMMARY', 'ACKNOWLEDGMENTS']:
                doc.add_page_break()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(h_text)
            run.bold = True
            run.font.size = Pt(15)
            run.font.color.rgb = COLOR_NAVY
            i += 1
            continue
            
        if line.startswith('### '):
            h_text = line[4:].strip()
            # Box Callout
            if h_text.startswith('Box '):
                box_title = h_text
                i += 1
                box_content = []
                while i < n and lines[i].strip() and not lines[i].strip().startswith('#') and not lines[i].strip().startswith('---'):
                    box_content.append(lines[i].strip())
                    i += 1
                
                tbl = doc.add_table(rows=1, cols=1)
                tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
                cell = tbl.cell(0, 0)
                cell.width = Inches(6.5)
                _set_cell_margins(cell, top=140, bottom=140, left=180, right=160)
                _set_cell_shading(cell, HEX_LIGHT_BG)
                _set_callout_borders(cell, border_color_hex=HEX_NAVY, border_size=28)
                
                cp = cell.paragraphs[0]
                cp.paragraph_format.space_before = Pt(2)
                cp.paragraph_format.space_after = Pt(4)
                bt_run = cp.add_run(box_title)
                bt_run.bold = True
                bt_run.font.size = Pt(11)
                bt_run.font.color.rgb = COLOR_NAVY
                
                for b_line in box_content:
                    bp = cell.add_paragraph()
                    bp.paragraph_format.space_before = Pt(2)
                    bp.paragraph_format.space_after = Pt(3)
                    if b_line.startswith('* ') or b_line.startswith('- '):
                        _add_formatted_runs(bp, "•  " + b_line[2:], base_color=COLOR_CHARCOAL, base_size=Pt(9.5))
                    else:
                        _add_formatted_runs(bp, b_line, base_color=COLOR_CHARCOAL, base_size=Pt(9.5))
                
                sp = doc.add_paragraph()
                sp.paragraph_format.space_before = Pt(0)
                sp.paragraph_format.space_after = Pt(6)
                continue
            
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(h_text)
            run.bold = True
            run.font.size = Pt(12.5)
            run.font.color.rgb = COLOR_ACCENT
            i += 1
            continue
            
        if line.startswith('#### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(line[5:].strip())
            run.bold = True
            run.font.size = Pt(11)
            run.font.color.rgb = COLOR_CHARCOAL
            i += 1
            continue

        # Tables: line starts with '|'
        if line.startswith('|') and '|' in line[1:]:
            table_lines = []
            while i < n and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            
            if len(table_lines) >= 2:
                header_cells = [c.strip() for c in table_lines[0].strip('|').split('|')]
                data_rows = []
                for t_line in table_lines[2:]:
                    cells = [c.strip() for c in t_line.strip('|').split('|')]
                    while len(cells) < len(header_cells):
                        cells.append("")
                    data_rows.append(cells[:len(header_cells)])
                
                tbl = doc.add_table(rows=len(data_rows) + 1, cols=len(header_cells))
                tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
                _set_table_borders(tbl)
                
                # Header
                hdr_row = tbl.rows[0]
                trPr = hdr_row._tr.get_or_add_trPr()
                trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
                
                for c_idx, text in enumerate(header_cells):
                    cell = hdr_row.cells[c_idx]
                    _set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
                    _set_cell_shading(cell, HEX_NAVY)
                    p = cell.paragraphs[0]
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.space_after = Pt(0)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
                    _add_formatted_runs(p, text, base_color=COLOR_WHITE, base_size=Pt(9.5))
                    for run in p.runs:
                        run.bold = True
                
                # Data Rows
                for r_idx, row_data in enumerate(data_rows):
                    row = tbl.rows[r_idx + 1]
                    bg_color = HEX_ALT_ROW if r_idx % 2 == 1 else "FFFFFF"
                    for c_idx, val in enumerate(row_data):
                        cell = row.cells[c_idx]
                        _set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
                        if bg_color != "FFFFFF":
                            _set_cell_shading(cell, bg_color)
                        p = cell.paragraphs[0]
                        p.paragraph_format.space_before = Pt(0)
                        p.paragraph_format.space_after = Pt(0)
                        if re.match(r'^-?\d+(\.\d+)?%?$', val) or val in ['—', '-', 'N/A']:
                            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        else:
                            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                        _add_formatted_runs(p, val, base_color=COLOR_CHARCOAL, base_size=Pt(9.0))
                
                sp = doc.add_paragraph()
                sp.paragraph_format.space_before = Pt(0)
                sp.paragraph_format.space_after = Pt(8)
            continue
            
        # Bullet list
        if line.startswith('* ') or line.startswith('- '):
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(3)
            _add_formatted_runs(p, line[2:].strip(), base_color=COLOR_CHARCOAL, base_size=Pt(10.0))
            i += 1
            continue
            
        # Numbered list
        num_match = re.match(r'^(\d+)\.\s+(.*)', line)
        if num_match:
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(3)
            _add_formatted_runs(p, num_match.group(2).strip(), base_color=COLOR_CHARCOAL, base_size=Pt(10.0))
            i += 1
            continue
            
        # Regular paragraph
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        
        # Math display $$...$$
        if line.startswith('$$') and line.endswith('$$'):
            math_text = line.strip('$').strip()
            clean_math = math_text.replace(r'\text{', '').replace('}', '').replace(r'\min', 'min')
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            m_run = p.add_run(clean_math)
            m_run.italic = True
            m_run.bold = True
            m_run.font.size = Pt(11)
            m_run.font.color.rgb = COLOR_NAVY
        else:
            _add_formatted_runs(p, line, base_color=COLOR_CHARCOAL, base_size=Pt(10.0))
            
        i += 1
        
    docx_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(docx_path))
    print(f"  ✓ Word report: {docx_path.name} (full publication layout)")


# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n  MTF Namibia — Automated Report Injection Pipeline")
    print(f"  =================================================")
    print(f"  JSON Values:  {JSON_PATH}")
    print(f"  MD Template:  {MD_TEMPLATE}")
    print(f"  MD Output:    {MD_OUT}")
    print(f"  DOCX Output:  {DOCX_OUT}")
    print()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    values = load_values()
    print(f"  Loaded {len(values)} placeholder values from JSON\n")

    # Step 1: Inject Markdown template
    inject_markdown(values)

    # Step 2: Render full publication Word document from injected Markdown
    inject_docx_from_markdown(MD_OUT, DOCX_OUT)

    print(f"\n  All reports successfully generated in: {OUTPUT_DIR}\n")

