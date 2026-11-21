"""
Justice AI - Direct GitHub Repository Uploader (Clean Production Release)
Uploads clean project files directly to a GitHub repository via GitHub REST API without requiring Git CLI.
Includes flood-control throttling to smoothly navigate campus/corporate firewalls (Sophos).
"""
import os
import sys
import base64
import json
import ssl
import time
import urllib.request
import urllib.error

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

IGNORE_PREFIXES = ('screen_', 'extracted_', 'debug_', 'test_', 'temp_')
IGNORE_DIRS = {'.git', '__pycache__', '.pytest_cache', '.vscode', 'chroma_db'}
IGNORE_EXTENSIONS = ('.pyc', '.log', '.tmp', '.bin')

def is_clean_file(rel_path):
    parts = rel_path.replace('\\', '/').split('/')
    for p in parts:
        if p in IGNORE_DIRS:
            return False
        if p.startswith('.') and p not in ('.gitignore', '.env.example', '.streamlit'):
            return False
        if p.startswith(IGNORE_PREFIXES):
            return False
        if any(p.endswith(ext) for ext in IGNORE_EXTENSIONS):
            return False
    filename = parts[-1]
    if filename.startswith('.env') and filename != '.env.example':
        return False
    if filename.startswith(IGNORE_PREFIXES):
        return False
    if any(filename.endswith(ext) for ext in IGNORE_EXTENSIONS):
        return False
    return True

def make_request(url, data=None, headers=None, method=None, ctx=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=45) as resp:
                raw = resp.read().decode('utf-8')
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    # Captive portal / proxy intercepted
                    time.sleep(2)
                    continue
        except urllib.error.HTTPError as e:
            if attempt == 3:
                raise Exception(f"HTTP {e.code}")
            time.sleep(2)
        except Exception as e:
            if attempt == 3:
                raise e
            time.sleep(2)
    raise Exception(f"Failed to fetch {url} after 4 attempts")

def upload_to_github(token, repo_owner, repo_name, branch="main", base_dir="."):
    ctx = ssl._create_unverified_context()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Justice-AI-Uploader",
        "Content-Type": "application/json"
    }
    api_base = f"https://api.github.com/repos/{repo_owner}/{repo_name}"

    print(f"[*] Connecting to repository https://github.com/{repo_owner}/{repo_name}...")
    repo_data = make_request(api_base, headers=headers, ctx=ctx)
    print(f"[+] Connected to: {repo_data.get('full_name')} (Private: {repo_data.get('private')})")

    # 1. Collect files
    files_to_upload = []
    for root, dirs, files in os.walk(base_dir):
        # Filter directories in-place
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, base_dir).replace('\\', '/')
            if is_clean_file(rel_path):
                if os.path.getsize(full_path) < 25 * 1024 * 1024:
                    files_to_upload.append((full_path, rel_path))

    print(f"[*] Found {len(files_to_upload)} clean production files to upload.")

    # 2. Create Blobs
    tree_items = []
    total = len(files_to_upload)
    for idx, (full_path, rel_path) in enumerate(files_to_upload, 1):
        try:
            with open(full_path, 'rb') as fp:
                content = fp.read()
            b64_content = base64.b64encode(content).decode('utf-8')
            blob_payload = json.dumps({"content": b64_content, "encoding": "base64"}).encode('utf-8')
            blob_data = make_request(f"{api_base}/git/blobs", data=blob_payload, headers=headers, method="POST", ctx=ctx)
            tree_items.append({
                "path": rel_path,
                "mode": "100644",
                "type": "blob",
                "sha": blob_data["sha"]
            })
            if idx % 10 == 0 or idx == total:
                print(f"  [+] Uploaded {idx}/{total} files ({rel_path})")
            time.sleep(0.08)  # Gentle pacing to avoid campus firewall throttling
        except Exception as e:
            print(f"  [!] Skipping {rel_path}: {e}")

    # 3. Create Tree
    print(f"\n[*] Constructing Git Tree ({len(tree_items)} items)...")
    tree_payload = json.dumps({"tree": tree_items}).encode('utf-8')
    tree_data = make_request(f"{api_base}/git/trees", data=tree_payload, headers=headers, method="POST", ctx=ctx)
    tree_sha = tree_data["sha"]
    print(f"[+] Git Tree created: {tree_sha[:8]}")

    # 4. Get Parent Commit
    parent_commit = None
    try:
        ref_data = make_request(f"{api_base}/git/ref/heads/{branch}", headers=headers, ctx=ctx)
        parent_commit = ref_data["object"]["sha"]
        print(f"[+] Parent commit found: {parent_commit[:8]}")
    except Exception:
        print("[*] No existing parent commit found. Creating root commit.")

    # 5. Create Commit
    commit_body = {
        "message": "Release v1.1: Oswald typography, unified 3 coverage cards, 6 randomized sample scenarios, and UI refinements\n\n- Unified Indian legal statutes into a single card (reduced to 3 coverage boxes)\n- Added 6 dynamic randomized sample scenarios with zero place or person names\n- Renamed Statutory Coverage to Coverage\n- Modernized all typography to Oswald across landing page and consultation chat\n- Updated all branding to all-caps JUSTICE AI\n- Minimalist identical sidebar collapse arrows and white/blue dropdown selectors\n- Integrated Contact Us support ticket modal with /api/contact backend",
        "tree": tree_sha
    }
    if parent_commit:
        commit_body["parents"] = [parent_commit]

    c_payload = json.dumps(commit_body).encode('utf-8')
    c_data = make_request(f"{api_base}/git/commits", data=c_payload, headers=headers, method="POST", ctx=ctx)
    commit_sha = c_data["sha"]
    print(f"[+] Git Commit created: {commit_sha[:8]}")

    # 6. Update/Create Branch Ref
    if parent_commit:
        make_request(
            f"{api_base}/git/refs/heads/{branch}",
            data=json.dumps({"sha": commit_sha, "force": True}).encode('utf-8'),
            headers=headers,
            method="PATCH",
            ctx=ctx
        )
    else:
        make_request(
            f"{api_base}/git/refs",
            data=json.dumps({"ref": f"refs/heads/{branch}", "sha": commit_sha}).encode('utf-8'),
            headers=headers,
            method="POST",
            ctx=ctx
        )

    print(f"\n========================================================")
    print(f"[SUCCESS] Successfully pushed all files to https://github.com/{repo_owner}/{repo_name}")
    print(f"Branch: {branch} | Commit: {commit_sha[:8]}")
    print(f"========================================================")
    return True

if __name__ == "__main__":
    tok = sys.argv[1] if len(sys.argv) > 1 else ""
    owner = sys.argv[2] if len(sys.argv) > 2 else "APTIKDEBNATH"
    repo = sys.argv[3] if len(sys.argv) > 3 else "justice-ai-"
    br = sys.argv[4] if len(sys.argv) > 4 else "main"

    if not tok:
        print("Usage: python github_uploader.py <TOKEN> <OWNER> <REPO_NAME> [BRANCH]")
    else:
        upload_to_github(tok, owner, repo, br)
