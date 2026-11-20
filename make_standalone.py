import re
import json

with open('debug_en_screen.html', 'r', encoding='utf-8') as f:
    text = f.read()

tmpl = re.search(r'<script type=[\"\']__bundler/template[\"\']>([\s\S]*?)</script>', text)
if tmpl:
    val = json.loads(tmpl.group(1).strip())
    # Replace internal asset uuids with Google Fonts URLs
    val = val.replace('1372f042-17a4-49a3-9598-f8fcf1b42acc', 'https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7SUc.woff2')
    val = val.replace('e6142bc3-9604-456f-8539-8134f75d52f7', 'https://fonts.gstatic.com/s/newsreader/v26/cY9VfjOCX1hbuyalUrK49dLac06G1ZGsZBtoBAbEJYQraA.woff2')
    val = val.replace('{{accent}}', '#1F4E79')
    val = val.replace('<x-dc>', '').replace('</x-dc>', '')
    val = val.replace('<sc-raw-select>', '<select>').replace('</sc-raw-select>', '</select>')
    val = val.replace('sc-camel-view-box', 'viewBox')
    
    with open('standalone_en.html', 'w', encoding='utf-8') as out:
        out.write(val)
    print("Wrote standalone_en.html, length:", len(val))
