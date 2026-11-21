"""
Justice AI - Unified Cloud Production Server (Render / Railway / Hugging Face)
Binds to the cloud-assigned $PORT environment variable automatically.
Serves the responsive editorial web interface and handles all /api/* requests.
"""

import http.server
import os
import sys

# Ensure core modules can be imported
sys.path.insert(0, os.path.dirname(__file__))

from core.api_handler import handle_api_request
import core.auth_db as auth_db

# Auto-detect cloud port or default to 3000
PORT = int(os.environ.get("PORT", sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].isdigit() else 3000))
BASE_DIR = os.path.dirname(__file__)
WEB_DIR = os.path.join(BASE_DIR, "web")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

class JusticeAIProductionHandler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def translate_path(self, path):
        clean_path = path.split("?", 1)[0].split("#", 1)[0]
        if clean_path.startswith("/assets/"):
            rel_path = clean_path[len("/assets/"):]
            return os.path.join(ASSETS_DIR, rel_path)
        else:
            rel_path = clean_path.lstrip("/")
            if not rel_path:
                rel_path = "index.html"
            return os.path.join(WEB_DIR, rel_path)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_OPTIONS(self):
        if self.path.startswith("/api/"):
            code, headers, data = handle_api_request("OPTIONS", self.path, self.headers, "")
            self.send_response(code)
            for k, v in headers.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Session-Token")
            self.send_header("Connection", "close")
            self.end_headers()

    def do_GET(self):
        if self.path.startswith("/api/"):
            code, headers, data = handle_api_request("GET", self.path, self.headers, "")
            self.send_response(code)
            for k, v in headers.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(data)
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/"):
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""
            code, headers, data = handle_api_request("POST", self.path, self.headers, post_data)
            self.send_response(code)
            for k, v in headers.items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_error(404, "Endpoint not found")

    def log_message(self, format, *args):
        print(f"[Cloud Server :{PORT}] - {args[0]} - {args[1]} {args[2]}")
        sys.stdout.flush()

if __name__ == "__main__":
    # Ensure database is initialized
    auth_db.init_db()
    
    httpd = http.server.ThreadingHTTPServer(("", PORT), JusticeAIProductionHandler)
    httpd.daemon_threads = True
    print(f"============================================================")
    print(f"  Justice AI Production Server LIVE on port {PORT}")
    print(f"  Serving client UI from {WEB_DIR}")
    print(f"  Ready for public traffic!")
    print(f"============================================================")
    sys.stdout.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server shutdown requested.")
