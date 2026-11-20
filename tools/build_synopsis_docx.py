import os
import re
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def clean_latex(text):
    text = text.replace(r'$\ge$', '≥').replace(r'$\le$', '≤')
    text = text.replace(r'$\ge', '≥ ').replace(r'$\le', '≤ ')
    text = text.replace(r'$\tau = 0.35$', 'τ = 0.35').replace(r'$\tau$', 'τ')
    text = text.replace(r'$\mu$', 'μ').replace(r'$\sigma$', 'σ')
    text = text.replace(r'$D_{statutory}$', 'D_statutory')
    text = text.replace(r'$Q_{user}$', 'Q_user')
    text = text.replace(r'$sim(v_q, v_d)$', 'sim(v_q, v_d)')
    text = text.replace(r'$$', '')
    text = re.sub(r'\$([^\$]+)\$', r'\1', text)
    text = text.replace(r'\$', '$')
    return text

def add_styled_run(p, text, bold=False, italic=False, code=False, color=None, font_size=11, font_name="Calibri"):
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    if code:
        run.font.name = "Consolas"
        run.font.size = Pt(font_size - 1)
        run.font.color.rgb = RGBColor(160, 40, 40)
    else:
        run.font.name = font_name
        run.font.size = Pt(font_size)
        if color:
            run.font.color.rgb = color
    return run

def add_formatted_paragraph(p, text, font_size=11, base_color=None, font_name="Calibri"):
    text = clean_latex(text)
    tokens = re.split(r'(\*\*\*[^*]+\*\*\*|\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)', text)
    for token in tokens:
        if not token:
            continue
        if token.startswith('***') and token.endswith('***'):
            add_styled_run(p, token[3:-3], bold=True, italic=True, color=base_color, font_size=font_size, font_name=font_name)
        elif token.startswith('**') and token.endswith('**'):
            add_styled_run(p, token[2:-2], bold=True, color=base_color, font_size=font_size, font_name=font_name)
        elif token.startswith('*') and token.endswith('*'):
            add_styled_run(p, token[1:-1], italic=True, color=base_color, font_size=font_size, font_name=font_name)
        elif token.startswith('`') and token.endswith('`'):
            add_styled_run(p, token[1:-1], code=True, font_size=font_size)
        else:
            add_styled_run(p, token, color=base_color, font_size=font_size, font_name=font_name)

def markdown_to_docx(md_path, docx_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    doc = docx.Document()

    # Page Margins
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
        hrun = hp.add_run("Project Synopsis · Justice AI | LPU CSE")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(128, 128, 128)

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Lovely Professional University · Department of Computer Science & Engineering")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(128, 128, 128)

    NAVY = RGBColor(27, 54, 93)      # #1B365D
    SLATE = RGBColor(46, 64, 83)     # #2E4053
    CHARCOAL = RGBColor(34, 34, 34)  # #222222
    DARK_GRAY = RGBColor(80, 80, 80)

    lines = md_text.split('\n')
    i = 0
    in_code_block = False
    code_lines = []
    in_cover_page = True

    while i < len(lines):
        line = lines[i]

        # Check for cover page delimiter
        if in_cover_page and (line.strip() == r'\newpage' or line.strip() == '## 1. Title of the Project'):
            in_cover_page = False
            doc.add_page_break()
            if line.strip() == r'\newpage':
                i += 1
                continue

        # Code block handling
        if line.startswith('```'):
            if in_code_block:
                table = doc.add_table(rows=1, cols=1)
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                cell = table.cell(0, 0)
                set_cell_background(cell, "F4F6F7")
                set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
                set_table_borders(table, color="D0D5DD", sz="6", val="single")
                cp = cell.paragraphs[0]
                cp.paragraph_format.space_before = Pt(0)
                cp.paragraph_format.space_after = Pt(0)
                cp.paragraph_format.line_spacing = 1.05
                code_text = '\n'.join(code_lines)
                c_run = cp.add_run(code_text)
                c_run.font.name = "Consolas"
                c_run.font.size = Pt(8.0)
                c_run.font.color.rgb = RGBColor(40, 40, 40)
                doc.add_paragraph()
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
                code_lines = []
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Image Detection
        img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line.strip())
        if img_match:
            caption, img_rel_path = img_match.group(1), img_match.group(2)
            img_full_path = os.path.abspath(img_rel_path) if not os.path.isabs(img_rel_path) else img_rel_path
            if not os.path.exists(img_full_path):
                img_full_path = os.path.join(r"c:\Users\akdeb\Desktop\experiments\LEGAL CHATBOT", img_rel_path)
            if os.path.exists(img_full_path):
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(12)
                p_img.paragraph_format.space_after = Pt(4)
                p_img.paragraph_format.keep_with_next = True
                run_img = p_img.add_run()
                run_img.add_picture(img_full_path, width=Inches(5.8))
                if caption:
                    p_cap = doc.add_paragraph()
                    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_cap.paragraph_format.space_before = Pt(2)
                    p_cap.paragraph_format.space_after = Pt(10)
                    run_cap = p_cap.add_run(caption)
                    run_cap.font.name = "Calibri"
                    run_cap.font.size = Pt(9.5)
                    run_cap.font.italic = True
                    run_cap.font.color.rgb = RGBColor(100, 100, 100)
            i += 1
            continue

        # Markdown Table Detection
        if line.strip().startswith('|') and i + 1 < len(lines) and re.match(r'\|[-:| ]+\|', lines[i+1].strip()):
            table_lines = [line.strip()]
            i += 2
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1

            headers = [c.strip() for c in table_lines[0].split('|')[1:-1]]
            rows_data = []
            for r in table_lines[1:]:
                cells = [c.strip() for c in r.split('|')[1:-1]]
                if len(cells) < len(headers):
                    cells += [''] * (len(headers) - len(cells))
                rows_data.append(cells[:len(headers)])

            num_cols = len(headers)
            num_rows = len(rows_data) + 1
            table = doc.add_table(rows=num_rows, cols=num_cols)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            set_table_borders(table, color="D3D3D3", sz="4", val="single")

            # Header Row
            hdr_cells = table.rows[0].cells
            for col_idx, h_text in enumerate(headers):
                cell = hdr_cells[col_idx]
                set_cell_background(cell, "1B365D")
                set_cell_margins(cell, top=140, bottom=140, left=150, right=150)
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                add_formatted_paragraph(p, f"**{h_text}**", font_size=10, base_color=RGBColor(255, 255, 255))

            # Data Rows
            for row_idx, r_data in enumerate(rows_data):
                row_cells = table.rows[row_idx + 1].cells
                bg_color = "F8F9FA" if row_idx % 2 == 1 else "FFFFFF"
                for col_idx, c_text in enumerate(r_data):
                    cell = row_cells[col_idx]
                    set_cell_background(cell, bg_color)
                    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
                    cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
                    p = cell.paragraphs[0]
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.line_spacing = 1.15
                    add_formatted_paragraph(p, c_text, font_size=9.5, base_color=CHARCOAL)

            doc.add_paragraph()
            continue

        # Horizontal Rule
        if line.strip() in ['---', '***', '___']:
            if not in_cover_page:
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.space_after = Pt(6)
                p_border = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="1" w:color="CCCCCC"/></w:pBdr>')
                p._p.get_or_add_pPr().append(p_border)
            i += 1
            continue

        # Cover Page Formatting
        if in_cover_page:
            sline = line.strip()
            if not sline:
                i += 1
                continue
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.2

            if sline.startswith('# LOVELY PROFESSIONAL UNIVERSITY'):
                p.paragraph_format.space_before = Pt(18)
                p.paragraph_format.space_after = Pt(6)
                run = p.add_run("LOVELY PROFESSIONAL UNIVERSITY")
                run.bold = True
                run.font.name = "Calibri"
                run.font.size = Pt(20)
                run.font.color.rgb = NAVY
            elif sline.startswith('### Phagwara, Punjab'):
                run = p.add_run("Phagwara, Punjab")
                run.font.name = "Calibri"
                run.font.size = Pt(13)
                run.font.color.rgb = DARK_GRAY
            elif sline.startswith('### Department of Computer Science'):
                p.paragraph_format.space_after = Pt(16)
                run = p.add_run("Department of Computer Science and Engineering")
                run.bold = True
                run.font.name = "Calibri"
                run.font.size = Pt(14)
                run.font.color.rgb = SLATE
            elif sline.startswith('# PROJECT SYNOPSIS'):
                p.paragraph_format.space_before = Pt(16)
                p.paragraph_format.space_after = Pt(12)
                run = p.add_run("PROJECT SYNOPSIS")
                run.bold = True
                run.font.name = "Calibri"
                run.font.size = Pt(18)
                run.font.color.rgb = NAVY
            elif sline.startswith('## “Justice AI'):
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.space_after = Pt(16)
                clean_title = sline.replace('##', '').strip().strip('“').strip('”').strip('"')
                run = p.add_run(f'“{clean_title}”')
                run.bold = True
                run.font.name = "Calibri"
                run.font.size = Pt(15)
                run.font.color.rgb = CHARCOAL
            elif 'Submitted in partial fulfillment' in sline or 'Bachelor of Technology' in sline:
                add_formatted_paragraph(p, sline, font_size=11, base_color=DARK_GRAY)
            elif sline.startswith('### Submitted By:') or sline.startswith('### Under the Guidance of:'):
                p.paragraph_format.space_before = Pt(14)
                p.paragraph_format.space_after = Pt(4)
                run = p.add_run(sline.replace('###', '').strip())
                run.bold = True
                run.font.name = "Calibri"
                run.font.size = Pt(12)
                run.font.color.rgb = NAVY
            else:
                add_formatted_paragraph(p, sline, font_size=11, base_color=CHARCOAL)

            i += 1
            continue

        # Main Document Headings
        sline = line.strip()
        if not sline:
            i += 1
            continue

        if sline.startswith('## '):
            heading_text = sline[3:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(heading_text)
            run.bold = True
            run.font.name = "Calibri"
            run.font.size = Pt(15)
            run.font.color.rgb = NAVY
            i += 1
            continue

        if sline.startswith('### '):
            heading_text = sline[4:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(heading_text)
            run.bold = True
            run.font.name = "Calibri"
            run.font.size = Pt(12.5)
            run.font.color.rgb = SLATE
            i += 1
            continue

        if sline.startswith('#### '):
            heading_text = sline[5:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            run = p.add_run(heading_text)
            run.bold = True
            run.font.name = "Calibri"
            run.font.size = Pt(11.5)
            run.font.color.rgb = CHARCOAL
            i += 1
            continue

        # Blockquotes
        if sline.startswith('> '):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.4)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            add_formatted_paragraph(p, sline[2:].strip(), font_size=10.5, base_color=DARK_GRAY)
            i += 1
            continue

        # Bullet List Items
        if re.match(r'^[\*\-]\s+', sline):
            item_text = re.sub(r'^[\*\-]\s+', '', sline)
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            add_formatted_paragraph(p, item_text, font_size=11, base_color=CHARCOAL)
            i += 1
            continue

        # Numbered List Items
        if re.match(r'^\d+\.\s+', sline):
            num_match = re.match(r'^(\d+\.)\s+(.+)$', sline)
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.3)
            p.paragraph_format.first_line_indent = Inches(-0.3)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            if num_match:
                prefix, body = num_match.group(1), num_match.group(2)
                run = p.add_run(f"{prefix} ")
                run.bold = True
                run.font.name = "Calibri"
                run.font.size = Pt(11)
                run.font.color.rgb = NAVY
                add_formatted_paragraph(p, body, font_size=11, base_color=CHARCOAL)
            else:
                add_formatted_paragraph(p, sline, font_size=11, base_color=CHARCOAL)
            i += 1
            continue

        # Standard Paragraph
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        add_formatted_paragraph(p, sline, font_size=11, base_color=CHARCOAL)
        i += 1

    doc.save(docx_path)
    print(f"Successfully generated DOCX: {docx_path}")

if __name__ == "__main__":
    md_file = r"c:\Users\akdeb\Desktop\experiments\LEGAL CHATBOT\JUSTICE_AI_PROJECT_SYNOPSIS_REPORT.md"
    docx_file_workspace = r"c:\Users\akdeb\Desktop\experiments\LEGAL CHATBOT\JUSTICE_AI_PROJECT_SYNOPSIS_REPORT.docx"
    docx_file_artifact = r"C:\Users\akdeb\.gemini\antigravity\brain\d7ff6692-5e23-4c7a-8b59-328e080306d4\JUSTICE_AI_PROJECT_SYNOPSIS_REPORT.docx"

    markdown_to_docx(md_file, docx_file_workspace)
    shutil.copyfile(docx_file_workspace, docx_file_artifact)
    print(f"Copied DOCX to artifact: {docx_file_artifact}")
