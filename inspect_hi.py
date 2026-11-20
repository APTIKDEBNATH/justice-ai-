import re
import json

with open('extracted_e0db5695-1f51-461a-a8e9-e77a951bdd87.html', 'r', encoding='utf-8') as f:
    text = f.read()

template_m = re.search(r'<script type=[\"\']__bundler/template[\"\']>([\s\S]*?)</script>', text)
if template_m:
    tmpl = json.loads(template_m.group(1).strip())
    with open('debug_hi_template.html', 'w', encoding='utf-8') as out:
        out.write(tmpl)
    print("Saved debug_hi_template.html with length", len(tmpl))
else:
    print("No template found in hi screen")
