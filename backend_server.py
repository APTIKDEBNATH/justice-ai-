"""
Justice AI - Dedicated Multithreaded Backend REST API Server
Runs on http://localhost:5000
Provides statutory search, multi-jurisdictional ML classification, and legal RAG inference.
"""

import http.server
import sys
from core.api_handler import handle_api_request

PORT = 5000

class JusticeAIBackendHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_OPTIONS(self):
        code, headers, data = handle_api_request("OPTIONS", self.path, self.headers, "")
        self.send_response(code)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        code, headers, data = handle_api_request("GET", self.path, self.headers, "")
        self.send_response(code)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""
        code, headers, data = handle_api_request("POST", self.path, self.headers, post_data)
        self.send_response(code)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        print(f"[Backend API :5000] - {args[0]} - {args[1]} {args[2]}")
        sys.stdout.flush()


if __name__ == "__main__":
    httpd = http.server.ThreadingHTTPServer(("", PORT), JusticeAIBackendHandler)
    httpd.daemon_threads = True
    print(f"Justice AI Backend API Server active on http://localhost:{PORT}")
    sys.stdout.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Backend server stopped.")
