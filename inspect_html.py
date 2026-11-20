import re

with open('extracted_84b9151d-6507-432e-9fe5-8568147d7a5a.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the large manifest script
text_no_manifest = re.sub(r'<script[^>]*type=[\"\']__bundler/manifest[\"\'][^>]*>[\s\S]*?</script>', '<!-- MANIFEST REMOVED -->', text)
print("Length without manifest:", len(text_no_manifest))
with open('debug_en_screen.html', 'w', encoding='utf-8') as out:
    out.write(text_no_manifest)

print("Saved debug_en_screen.html")
