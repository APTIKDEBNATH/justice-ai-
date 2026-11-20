"""
Justice AI - Standalone Web Server
Serves the pure HTML5/CSS3 Justice AI interface with real-time legal intelligence backend.
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from typing import Dict, Any

from modules.legal_chat import process_chat_message
from core.legal_formatter import format_assistant_response_data
from core.llm import LLMProvider

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(__file__), "web")

class JusticeAIHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            
            try:
                data = json.loads(post_data)
                query = data.get("query", "")
                jurisdiction = data.get("jurisdiction", "AUTO")
                category = data.get("category", "General")
                language = data.get("language", "en")

                llm = LLMProvider(provider="offline")
                raw_ans, eff_jur, statutes = process_chat_message(
                    user_query=query,
                    chat_history=[],
                    selected_jurisdiction=jurisdiction,
                    legal_domain=category,
                    llm=llm
                )

                card = format_assistant_response_data(
                    raw_response=raw_ans,
                    jurisdiction=eff_jur,
                    legal_domain=category,
                    retrieved_statutes=statutes,
                    language=language
                )

                response_payload = {
                    "status": "success",
                    "jurisdiction": eff_jur,
                    "card": card
                }
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(response_payload, ensure_ascii=False).encode("utf-8"))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint not found")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), JusticeAIHandler) as httpd:
        print(f"Justice AI Standalone Web Interface running at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")
