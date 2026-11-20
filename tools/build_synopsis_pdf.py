import os
import re
import shutil
import subprocess
import html
import pypdf

def clean_latex_to_html(text):
    text = text.replace(r'$\ge$', '&ge;').replace(r'$\le$', '&le;')
    text = text.replace(r'$\ge', '&ge; ').replace(r'$\le', '&le; ')
    text = text.replace(r'$\le', '&le; ')
    text = text.replace(r'$\tau = 0.35$', '&tau; = 0.35').replace(r'$\tau$', '&tau;')
    text = text.replace(r'$\mu$', '&mu;').replace(r'$\sigma$', '&sigma;')
    text = text.replace(r'$D_{statutory}$', '<i>D<sub>statutory</sub></i>')
    text = text.replace(r'$Q_{user}$', '<i>Q<sub>user</sub></i>')
    text = text.replace(r'$sim(v_q, v_d)$', '<i>sim</i>(<b>v</b><sub>q</sub>, <b>v</b><sub>d</sub>)')
    text = text.replace(r'$$', '')
    text = re.sub(r'\$([^\$]+)\$', r'<i>\1</i>', text)
    text = text.replace(r'\$', '$')
    return text

def format_inline(text):
    text = clean_latex_to_html(text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*\*([^*]+)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    return text

def parse_markdown_table(lines, start_idx):
    table_lines = [lines[start_idx].strip()]
    idx = start_idx + 2
    while idx < len(lines) and lines[idx].strip().startswith('|'):
        table_lines.append(lines[idx].strip())
        idx += 1

    headers = [c.strip() for c in table_lines[0].split('|')[1:-1]]
    html_out = ['<div class="table-container"><table class="report-table"><thead><tr>']
    for h in headers:
        html_out.append(f'<th>{format_inline(h)}</th>')
    html_out.append('</tr></thead><tbody>')

    for r in table_lines[1:]:
        cells = [c.strip() for c in r.split('|')[1:-1]]
        if len(cells) < len(headers):
            cells += [''] * (len(headers) - len(cells))
        html_out.append('<tr>')
        for c in cells[:len(headers)]:
            html_out.append(f'<td>{format_inline(c)}</td>')
        html_out.append('</tr>')

    html_out.append('</tbody></table></div>')
    return ''.join(html_out), idx

def markdown_to_html(md_path, font_pt=9.8, line_h=1.42, fig_scale=65):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    lines = md_text.split('\n')
    html_parts = []
    
    in_code = False
    code_lines = []
    in_list = False
    list_type = None
    in_cover = True
    cover_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Cover page end detection
        if in_cover and (line.strip() == r'\newpage' or line.strip() == '## 1. Title of the Project'):
            in_cover = False
            html_parts.append('<div class="cover-page">')
            ci = 0
            while ci < len(cover_lines):
                cl = cover_lines[ci]
                cl_s = cl.strip()
                if not cl_s:
                    ci += 1
                    continue
                if cl_s.startswith('# LOVELY PROFESSIONAL UNIVERSITY'):
                    html_parts.append('<div class="cover-uni">LOVELY PROFESSIONAL UNIVERSITY</div>')
                elif cl_s.startswith('### Phagwara, Punjab'):
                    html_parts.append('<div class="cover-loc">Phagwara, Punjab</div>')
                elif cl_s.startswith('### Department of Computer Science'):
                    html_parts.append('<div class="cover-dept">Department of Computer Science and Engineering</div>')
                elif cl_s in ['---', '***']:
                    html_parts.append('<div class="cover-divider"></div>')
                elif cl_s.startswith('# PROJECT SYNOPSIS'):
                    html_parts.append('<div class="cover-synopsis-badge">PROJECT SYNOPSIS</div>')
                elif cl_s.startswith('## “Justice AI'):
                    title_text = cl_s.replace('##', '').strip()
                    html_parts.append(f'<div class="cover-project-title">{format_inline(title_text)}</div>')
                elif 'Submitted in partial fulfillment' in cl_s or 'Bachelor of Technology' in cl_s:
                    html_parts.append(f'<div class="cover-degree-note">{format_inline(cl_s)}</div>')
                elif cl_s.startswith('### Submitted By:'):
                    html_parts.append('<div class="cover-section-head">Submitted By:</div>')
                elif cl_s.startswith('### Under the Guidance of:'):
                    html_parts.append('<div class="cover-section-head">Under the Guidance of:</div>')
                elif cl_s.startswith('|') and ci + 1 < len(cover_lines) and re.match(r'\|[-:| ]+\|', cover_lines[ci+1].strip()):
                    tbl_html, new_ci = parse_markdown_table(cover_lines, ci)
                    html_parts.append(f'<div class="cover-table-wrap">{tbl_html}</div>')
                    ci = new_ci
                    continue
                else:
                    html_parts.append(f'<div class="cover-text">{format_inline(cl_s)}</div>')
                ci += 1

            html_parts.append('</div>')
            # Notice: Single page-break triggered by .cover-page style; no duplicate div!
            if line.strip() == r'\newpage':
                i += 1
                continue

        if in_cover:
            cover_lines.append(line)
            i += 1
            continue

        # Code block handling
        if line.startswith('```'):
            if in_code:
                in_code = False
                code_content = html.escape('\n'.join(code_lines))
                html_parts.append(f'<pre class="code-block"><code>{code_content}</code></pre>')
                code_lines = []
            else:
                if in_list:
                    html_parts.append(f'</{list_type}>')
                    in_list = False
                in_code = True
                code_lines = []
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # Image Detection
        img_match = re.match(r'!\[([^\]]*)\]\(([^)]+)\)', line.strip())
        if img_match:
            if in_list:
                html_parts.append(f'</{list_type}>')
                in_list = False
            caption, img_rel_path = img_match.group(1), img_match.group(2)
            img_full_path = os.path.abspath(img_rel_path) if not os.path.isabs(img_rel_path) else img_rel_path
            if not os.path.exists(img_full_path):
                img_full_path = os.path.join(r"c:\Users\akdeb\Desktop\experiments\LEGAL CHATBOT", img_rel_path)
            file_url = f"file:///{img_full_path.replace(os.sep, '/')}"
            html_parts.append(f'''
            <div class="figure-container">
                <img src="{file_url}" alt="{caption}" class="report-figure-img" />
                <div class="figure-caption">{format_inline(caption)}</div>
            </div>
            ''')
            i += 1
            continue

        # Table detection
        if line.strip().startswith('|') and i + 1 < len(lines) and re.match(r'\|[-:| ]+\|', lines[i+1].strip()):
            if in_list:
                html_parts.append(f'</{list_type}>')
                in_list = False
            tbl_html, i = parse_markdown_table(lines, i)
            html_parts.append(tbl_html)
            continue

        # Horizontal Rule
        if line.strip() in ['---', '***', '___']:
            if in_list:
                html_parts.append(f'</{list_type}>')
                in_list = False
            html_parts.append('<hr class="report-hr" />')
            i += 1
            continue

        # Headings
        sline = line.strip()
        if not sline:
            if in_list:
                html_parts.append(f'</{list_type}>')
                in_list = False
            i += 1
            continue

        if sline.startswith('## '):
            if in_list:
                html_parts.append(f'</{list_type}>')
                in_list = False
            heading_text = sline[3:].strip()
            html_parts.append(f'<h2 class="report-h2">{format_inline(heading_text)}</h2>')
            i += 1
            continue

        if sline.startswith('### '):
            if in_list:
                html_parts.append(f'</{list_type}>')
                in_list = False
            heading_text = sline[4:].strip()
            html_parts.append(f'<h3 class="report-h3">{format_inline(heading_text)}</h3>')
            i += 1
            continue

        if sline.startswith('#### '):
            if in_list:
                html_parts.append(f'</{list_type}>')
                in_list = False
            heading_text = sline[5:].strip()
            html_parts.append(f'<h4 class="report-h4">{format_inline(heading_text)}</h4>')
            i += 1
            continue

        # Blockquote
        if sline.startswith('> '):
            if in_list:
                html_parts.append(f'</{list_type}>')
                in_list = False
            b_text = sline[2:].strip()
            html_parts.append(f'<blockquote class="report-quote">{format_inline(b_text)}</blockquote>')
            i += 1
            continue

        # Bullet list
        if re.match(r'^[\*\-]\s+', sline):
            item_text = re.sub(r'^[\*\-]\s+', '', sline)
            if not in_list or list_type != 'ul':
                if in_list:
                    html_parts.append(f'</{list_type}>')
                html_parts.append('<ul class="report-ul">')
                in_list = True
                list_type = 'ul'
            html_parts.append(f'<li>{format_inline(item_text)}</li>')
            i += 1
            continue

        # Numbered list
        if re.match(r'^\d+\.\s+', sline):
            item_text = re.sub(r'^\d+\.\s+', '', sline)
            if not in_list or list_type != 'ol':
                if in_list:
                    html_parts.append(f'</{list_type}>')
                html_parts.append('<ol class="report-ol">')
                in_list = True
                list_type = 'ol'
            html_parts.append(f'<li>{format_inline(item_text)}</li>')
            i += 1
            continue

        # Regular Paragraph
        if in_list:
            html_parts.append(f'</{list_type}>')
            in_list = False

        html_parts.append(f'<p class="report-p">{format_inline(sline)}</p>')
        i += 1

    if in_list:
        html_parts.append(f'</{list_type}>')

    full_body = '\n'.join(html_parts)

    css = f"""
@page {{
    size: A4 portrait;
    margin: 11mm 13mm 12mm 13mm;
    @top-right {{
        content: "Justice AI · LPU CSE Synopsis";
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
        font-size: 7.5pt;
        color: #718096;
    }}
    @bottom-center {{
        content: counter(page);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
        font-size: 8.0pt;
        color: #718096;
    }}
}}

* {{
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: {font_pt}pt;
    line-height: {line_h};
    color: #1a202c;
    background: #ffffff;
    margin: 0;
    padding: 0;
    text-rendering: optimizeLegibility;
}}

/* Cover Page - Exactly Page 1, No blank overflow */
.cover-page {{
    min-height: 86vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 15px 15px 20px 15px;
    box-sizing: border-box;
    page-break-after: always;
    break-after: page;
}}

.cover-uni {{
    font-size: 21pt;
    font-weight: 800;
    letter-spacing: 0.5px;
    color: #0d3b66;
    margin-bottom: 2px;
    text-transform: uppercase;
}}

.cover-loc {{
    font-size: 11.5pt;
    color: #4a5568;
    margin-bottom: 4px;
    font-weight: 500;
}}

.cover-dept {{
    font-size: 13pt;
    font-weight: 700;
    color: #2b6cb0;
    margin-bottom: 12px;
}}

.cover-divider {{
    width: 65%;
    height: 1.5px;
    background: linear-gradient(90deg, rgba(13,59,102,0) 0%, rgba(13,59,102,0.8) 50%, rgba(13,59,102,0) 100%);
    margin: 8px auto 14px auto;
}}

.cover-synopsis-badge {{
    font-size: 17pt;
    font-weight: 800;
    color: #0d3b66;
    letter-spacing: 2px;
    margin-bottom: 8px;
}}

.cover-project-title {{
    font-size: 14pt;
    font-weight: 700;
    line-height: 1.35;
    color: #1a202c;
    max-width: 90%;
    margin: 0 auto 10px auto;
}}

.cover-degree-note {{
    font-size: 9.5pt;
    color: #4a5568;
    font-style: italic;
    line-height: 1.4;
    margin-bottom: 10px;
}}

.cover-section-head {{
    font-size: 11pt;
    font-weight: 700;
    color: #0d3b66;
    margin-top: 8px;
    margin-bottom: 2px;
}}

.cover-text {{
    font-size: 9.5pt;
    color: #2d3748;
    line-height: 1.4;
    margin-bottom: 2px;
}}

.cover-table-wrap {{
    width: 88%;
    margin: 6px auto 10px auto;
}}

.cover-table-wrap .report-table th {{
    font-size: 8.0pt;
    padding: 4px 6px;
    text-align: center;
}}

.cover-table-wrap .report-table td {{
    font-size: 8.0pt;
    padding: 3.5px 6px;
    text-align: center;
}}

/* Headings */
.report-h2 {{
    font-size: 12.5pt;
    font-weight: 700;
    color: #0d3b66;
    margin-top: 14px;
    margin-bottom: 5px;
    padding-bottom: 2px;
    border-bottom: 1px solid #e2e8f0;
    page-break-after: avoid;
    break-after: avoid;
}}

.report-h3 {{
    font-size: 10.8pt;
    font-weight: 600;
    color: #2b6cb0;
    margin-top: 10px;
    margin-bottom: 4px;
    page-break-after: avoid;
    break-after: avoid;
}}

.report-h4 {{
    font-size: 9.8pt;
    font-weight: 600;
    color: #2d3748;
    margin-top: 7px;
    margin-bottom: 2px;
    page-break-after: avoid;
    break-after: avoid;
}}

/* Paragraphs & Text */
.report-p {{
    font-size: {font_pt}pt;
    line-height: {line_h};
    margin-top: 0;
    margin-bottom: 4.5px;
    text-align: justify;
    text-justify: inter-word;
}}

.report-ul, .report-ol {{
    margin-top: 0;
    margin-bottom: 5px;
    padding-left: 20px;
}}

.report-ul li, .report-ol li {{
    font-size: {font_pt}pt;
    line-height: {line_h};
    margin-bottom: 2.5px;
    text-align: justify;
}}

.report-quote {{
    border-left: 3px solid #3182ce;
    background-color: #ebf8ff;
    padding: 5px 10px;
    margin: 6px 0 8px 0;
    font-size: 9.0pt;
    color: #2c5282;
    border-radius: 0 3px 3px 0;
}}

.report-hr {{
    border: none;
    height: 1px;
    background-color: #e2e8f0;
    margin: 10px 0;
}}

code {{
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    font-size: 8.5pt;
    background-color: #edf2f7;
    color: #9b2c2c;
    padding: 1px 3px;
    border-radius: 2px;
}}

/* Figures / Charts */
.figure-container {{
    width: 100%;
    margin: 8px auto 10px auto;
    text-align: center;
    page-break-inside: avoid;
    break-inside: avoid;
}}

.report-figure-img {{
    max-width: {fig_scale}%;
    max-height: 200px;
    height: auto;
    object-fit: contain;
    border-radius: 4px;
    border: 1px solid #cbd5e0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}}

.figure-caption {{
    font-size: 8.0pt;
    font-style: italic;
    color: #4a5568;
    margin-top: 3px;
    text-align: center;
}}

/* Code Blocks */
.code-block {{
    background-color: #f7fafc;
    border: 1px solid #cbd5e0;
    border-radius: 4px;
    padding: 8px;
    overflow-x: auto;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    font-size: 6.5pt;
    line-height: 1.18;
    color: #2d3748;
    white-space: pre;
    page-break-inside: avoid;
    break-inside: avoid;
    margin: 8px 0;
}}

.code-block code {{
    background-color: transparent;
    color: inherit;
    padding: 0;
    font-size: inherit;
}}

/* Tables */
.table-container {{
    width: 100%;
    margin: 7px 0;
    page-break-inside: auto;
    break-inside: auto;
}}

.report-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 7.8pt;
    line-height: 1.35;
}}

.report-table tr {{
    page-break-inside: avoid;
    break-inside: avoid;
}}

.report-table th {{
    background-color: #0d3b66;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 5px 7px;
    border: 1px solid #0d3b66;
}}

.report-table td {{
    padding: 4px 7px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
}}

.report-table tr:nth-child(even) td {{
    background-color: #f8fafc;
}}

@media print {{
    body {{
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }}
    .cover-page {{
        page-break-after: always;
        break-after: page;
    }}
}}
"""

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Justice AI - Academic Project Synopsis Report</title>
<style>
{css}
</style>
</head>
<body>
{full_body}
</body>
</html>"""

    return full_html

def compile_pdf(html_path, pdf_path):
    chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    cmd = [
        chrome, '--headless=new', '--disable-gpu', '--no-sandbox',
        '--run-all-compositor-stages-before-draw',
        f'--print-to-pdf={os.path.abspath(pdf_path)}',
        f'file:///{os.path.abspath(html_path)}'
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        print(f"PDF Successfully Generated! Size: {os.path.getsize(pdf_path)} bytes")
        return True
    else:
        print("Error compiling PDF:")
        print("STDOUT:", res.stdout)
        print("STDERR:", res.stderr)
        return False

if __name__ == "__main__":
    md_file = r"c:\Users\akdeb\Desktop\experiments\LEGAL CHATBOT\JUSTICE_AI_PROJECT_SYNOPSIS_REPORT.md"
    html_file = r"c:\Users\akdeb\Desktop\experiments\LEGAL CHATBOT\JUSTICE_AI_PROJECT_SYNOPSIS_REPORT.html"
    pdf_file_workspace = r"c:\Users\akdeb\Desktop\experiments\LEGAL CHATBOT\JUSTICE_AI_PROJECT_SYNOPSIS_REPORT.pdf"
    pdf_file_artifact = r"C:\Users\akdeb\.gemini\antigravity\brain\d7ff6692-5e23-4c7a-8b59-328e080306d4\JUSTICE_AI_PROJECT_SYNOPSIS_REPORT.pdf"

    html_content = markdown_to_html(md_file, font_pt=10.0, line_h=1.44, fig_scale=65)
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Wrote HTML: {html_file}")

    if compile_pdf(html_file, pdf_file_workspace):
        shutil.copyfile(pdf_file_workspace, pdf_file_artifact)
        print(f"Copied PDF to Artifacts: {pdf_file_artifact}")

        reader = pypdf.PdfReader(pdf_file_workspace)
        print(f"FINAL COMPRESSED PDF TOTAL PAGES: {len(reader.pages)}")
        for idx, page in enumerate(reader.pages):
            chars = len(page.extract_text().strip())
            print(f"  Page {idx+1}: {chars} characters")
