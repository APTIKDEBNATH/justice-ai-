import json
import gzip
import base64
import re
import os

def unpack_bundler(filename, prefix=""):
    print(f"\n--- Checking {filename} ---")
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # Look for manifest
    scripts = re.findall(r'<script([^>]*)>([\s\S]*?)</script>', html)
    manifest = None
    for attrs, body in scripts:
        if '__bundler/manifest' in attrs or '"mime"' in body[:200] or '"compressed"' in body[:200]:
            try:
                manifest = json.loads(body.strip())
                break
            except Exception as e:
                pass
    
    if not manifest:
        print(f"No manifest found in {filename}.")
        return

    print(f"Found manifest in {filename} with {len(manifest)} entries:")
    for k, v in manifest.items():
        mime = v.get('mime', 'unknown')
        compressed = v.get('compressed', False)
        data = v.get('data', '')
        print(f"  Entry: {k} | mime: {mime} | compressed: {compressed} | data len: {len(data)}")
        
        raw = base64.b64decode(data)
        if compressed:
            try:
                raw = gzip.decompress(raw)
            except Exception as e:
                print(f"    Gzip error: {e}")
        
        # Save output
        ext = ".html" if "html" in mime else (".css" if "css" in mime else (".js" if "javascript" in mime else ".bin"))
        clean_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', k)
        out_name = f"{prefix}_{clean_name}{ext}" if not clean_name.endswith(ext) else f"{prefix}_{clean_name}"
        
        try:
            text_content = raw.decode('utf-8')
            with open(out_name, 'w', encoding='utf-8') as out_f:
                out_f.write(text_content)
            print(f"    Saved text file: {out_name} (len {len(text_content)})")
            # If it's HTML, check if it's another bundler
            if '<script' in text_content and '__bundler/manifest' in text_content:
                unpack_bundler(out_name, prefix=prefix + "_nested")
        except UnicodeDecodeError:
            with open(out_name, 'wb') as out_f:
                out_f.write(raw)
            print(f"    Saved binary file: {out_name} (len {len(raw)})")

unpack_bundler('extracted_84b9151d-6507-432e-9fe5-8568147d7a5a.html', prefix="screen_en")
unpack_bundler('extracted_e0db5695-1f51-461a-a8e9-e77a951bdd87.html', prefix="screen_hi")
