import re

for fname in ['extracted_84b9151d-6507-432e-9fe5-8568147d7a5a.html', 'extracted_e0db5695-1f51-461a-a8e9-e77a951bdd87.html']:
    print(f"\n=================== {fname} ===================")
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()
    
    title = re.search(r'<title>(.*?)</title>', html, re.I)
    print('Title:', title.group(1) if title else 'No title')
    
    # Check body classes and attributes
    body_tag = re.search(r'<body([^>]*)>', html, re.I)
    print('Body tag:', body_tag.group(0) if body_tag else 'None')
    
    # Extract headings
    headings = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', html, re.I | re.DOTALL)
    print('Headings:', [re.sub(r'<[^>]+>', '', h).strip() for h in headings[:15]])
    
    # Extract nav / buttons / links
    buttons = re.findall(r'<button[^>]*>(.*?)</button>', html, re.I | re.DOTALL)
    print(f'Buttons count: {len(buttons)}, sample: {[re.sub(r"<[^>]+>", "", b).strip() for b in buttons[:10]]}')
    
    # Look for layout structure
    print("\n--- Key Layout Elements ---")
    div_classes = set(re.findall(r'class=[\"\']([^\"\']+)[\"\']', html))
    # Filter interesting classes
    interesting = [c for c in div_classes if any(k in c.lower() for k in ['sidebar', 'header', 'chat', 'message', 'jurisdiction', 'card', 'nav', 'input', 'panel'])]
    print("Interesting classes:", interesting[:20])

