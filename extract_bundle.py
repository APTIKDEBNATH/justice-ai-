import json
import gzip
import base64
import re
import os

bundle_path = r'C:\Users\akdeb\.gemini\antigravity\brain\d7ff6692-5e23-4c7a-8b59-328e080306d4\.user_uploaded\media_1794813565377_74249ffc.html'
with open(bundle_path, 'r', encoding='utf-8') as f:
    html = f.read()

print("HTML size:", len(html))

# Look for script tag containing manifest
script_matches = re.findall(r'<script([^>]*)>([\s\S]*?)</script>', html)
print(f"Total script tags: {len(script_matches)}")

manifest_data = None
for i, (attrs, body) in enumerate(script_matches):
    print(f"Script {i}: attrs='{attrs.strip()}' length={len(body)}")
    if 'manifest' in attrs or 'manifest' in body[:100] or 'files' in body[:100] or '__bundler' in attrs:
        try:
            manifest_data = json.loads(body.strip())
            print(f"Successfully parsed JSON from script {i}")
            break
        except Exception as e:
            print(f"Script {i} not JSON: {e}")

if not manifest_data:
    for i, (attrs, body) in enumerate(script_matches):
        try:
            parsed = json.loads(body.strip())
            print(f"Script {i} is JSON!")
            manifest_data = parsed
            break
        except Exception:
            pass

if manifest_data:
    print("Keys in manifest:", list(manifest_data.keys()))
    # Let's inspect the files/screens
    files = manifest_data.get('files', manifest_data)
    if isinstance(files, dict):
        for k, v in files.items():
            print(f"File key: {k}, type: {type(v)}")
            if isinstance(v, dict):
                print(f"  details: {list(v.keys())}")
                if 'content' in v or 'data' in v:
                    content_val = v.get('content') or v.get('data')
                    encoding = v.get('encoding', '')
                    print(f"  encoding: {encoding}, content length: {len(str(content_val))}")
                    # Try decompressing if base64/gzip
                    if isinstance(content_val, str):
                        try:
                            decoded = base64.b64decode(content_val)
                            try:
                                decompressed = gzip.decompress(decoded).decode('utf-8')
                                print(f"  Decompressed length: {len(decompressed)}")
                                out_filename = f"extracted_{os.path.basename(k)}.html" if not k.endswith('.html') else f"extracted_{os.path.basename(k)}"
                                with open(out_filename, 'w', encoding='utf-8') as out_f:
                                    out_f.write(decompressed)
                                print(f"  Wrote decompressed to {out_filename}")
                            except Exception as gz_err:
                                print(f"  Gzip decompress error: {gz_err}")
                                with open(f"extracted_{os.path.basename(k)}.bin", 'wb') as out_f:
                                    out_f.write(decoded)
                        except Exception as b64_err:
                            print(f"  Base64 decode error: {b64_err}")
    elif isinstance(files, list):
        print(f"Files is list of length {len(files)}")
        for idx, item in enumerate(files):
            print(f"Item {idx}: {type(item)}")
            if isinstance(item, dict):
                print(f"  keys: {list(item.keys())}")
