"""
Justice AI - Unified REST API Request Handler
Provides centralized, authenticated routing for auth, conversations, and legal RAG inference.
Used by both backend_server.py (:5000) and frontend_server.py (:3000).
"""

import json
import urllib.parse
from typing import Tuple, Dict, Any, Optional

from core.auth_db import (
    register_user, authenticate_user, get_user_by_token, delete_session,
    get_user_conversations, create_conversation, get_conversation_details,
    save_chat_turn, delete_conversation
)
from core.autonomous_reasoner import reason_legally
from core.legal_formatter import LEGAL_CATEGORIES, CLEAN_REGIONS, REGION_LANGUAGES

def extract_token_from_headers(headers) -> Optional[str]:
    # Check Authorization: Bearer <token>
    auth_header = headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:].strip()
    # Check X-Session-Token
    token = headers.get("X-Session-Token", "")
    if token:
        return token.strip()
    return None

def handle_api_request(method: str, path: str, headers: Any, post_data: str) -> Tuple[int, Dict[str, str], bytes]:
    """
    Dispatches API calls and returns (status_code, headers_dict, response_bytes).
    """
    parsed_url = urllib.parse.urlparse(path)
    clean_path = parsed_url.path
    query_params = urllib.parse.parse_qs(parsed_url.query)

    response_headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS, DELETE",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Session-Token",
        "Connection": "close"
    }

    if method == "OPTIONS":
        return 200, response_headers, b""

    # ---------------- GET ENDPOINTS ----------------
    if method == "GET":
        if clean_path in ("/api/health", "/"):
            payload = {
                "status": "online",
                "service": "Justice AI Global Legal Intelligence API",
                "version": "2.2.0",
                "features": ["multi-tenant-auth", "per-user-conversations", "statutory-rag", "ml-classifier"]
            }
            return 200, response_headers, json.dumps(payload, indent=2).encode("utf-8")

        elif clean_path == "/api/taxonomy":
            payload = {
                "regions": CLEAN_REGIONS,
                "categories": LEGAL_CATEGORIES,
                "languages": REGION_LANGUAGES
            }
            return 200, response_headers, json.dumps(payload, indent=2).encode("utf-8")

        elif clean_path == "/api/auth/me":
            token = extract_token_from_headers(headers) or query_params.get("token", [None])[0]
            user = get_user_by_token(token)
            if user:
                return 200, response_headers, json.dumps({"status": "success", "user": user}).encode("utf-8")
            return 401, response_headers, json.dumps({"status": "error", "message": "Unauthorized or session expired"}).encode("utf-8")

        elif clean_path == "/api/conversations":
            token = extract_token_from_headers(headers) or query_params.get("token", [None])[0]
            user = get_user_by_token(token)
            if not user:
                return 401, response_headers, json.dumps({"status": "error", "message": "Unauthorized"}).encode("utf-8")

            convs = get_user_conversations(user["id"])
            return 200, response_headers, json.dumps({"status": "success", "conversations": convs}).encode("utf-8")

        elif clean_path == "/api/conversations/detail":
            token = extract_token_from_headers(headers) or query_params.get("token", [None])[0]
            user = get_user_by_token(token)
            if not user:
                return 401, response_headers, json.dumps({"status": "error", "message": "Unauthorized"}).encode("utf-8")

            conv_id = query_params.get("id", [None])[0]
            if not conv_id:
                return 400, response_headers, json.dumps({"status": "error", "message": "Missing conversation id"}).encode("utf-8")

            details = get_conversation_details(user["id"], conv_id)
            if not details:
                return 404, response_headers, json.dumps({"status": "error", "message": "Conversation not found"}).encode("utf-8")

            return 200, response_headers, json.dumps({"status": "success", "data": details}).encode("utf-8")

    # ---------------- POST ENDPOINTS ----------------
    elif method == "POST":
        try:
            body = json.loads(post_data) if post_data else {}
        except Exception:
            body = {}

        if clean_path == "/api/auth/register":
            username = body.get("username", "")
            password = body.get("password", "")
            name = body.get("name", "")
            ok, user, token, err = register_user(username, password, name)
            if ok:
                return 200, response_headers, json.dumps({
                    "status": "success",
                    "user": user,
                    "token": token,
                    "message": "Account created successfully"
                }).encode("utf-8")
            return 400, response_headers, json.dumps({"status": "error", "message": err}).encode("utf-8")

        elif clean_path == "/api/auth/login":
            username = body.get("username", "")
            password = body.get("password", "")
            ok, user, token, err = authenticate_user(username, password)
            if ok:
                return 200, response_headers, json.dumps({
                    "status": "success",
                    "user": user,
                    "token": token,
                    "message": "Signed in successfully"
                }).encode("utf-8")
            return 401, response_headers, json.dumps({"status": "error", "message": err}).encode("utf-8")

        elif clean_path == "/api/auth/logout":
            token = extract_token_from_headers(headers) or body.get("token")
            if token:
                delete_session(token)
            return 200, response_headers, json.dumps({"status": "success", "message": "Logged out"}).encode("utf-8")

        elif clean_path == "/api/conversations/new":
            token = extract_token_from_headers(headers) or body.get("token")
            user = get_user_by_token(token)
            if not user:
                return 401, response_headers, json.dumps({"status": "error", "message": "Unauthorized"}).encode("utf-8")

            title = body.get("title", "New legal question")
            jur = body.get("jurisdiction", "AUTO")
            cat = body.get("category", "General")
            conv = create_conversation(user["id"], title, jur, cat)
            return 200, response_headers, json.dumps({"status": "success", "conversation": conv}).encode("utf-8")

        elif clean_path == "/api/conversations/delete":
            token = extract_token_from_headers(headers) or body.get("token")
            user = get_user_by_token(token)
            if not user:
                return 401, response_headers, json.dumps({"status": "error", "message": "Unauthorized"}).encode("utf-8")

            conv_id = body.get("id") or query_params.get("id", [None])[0]
            if not conv_id:
                return 400, response_headers, json.dumps({"status": "error", "message": "Missing conversation id"}).encode("utf-8")

            success = delete_conversation(user["id"], conv_id)
            return 200, response_headers, json.dumps({"status": "success" if success else "not_found"}).encode("utf-8")

        elif clean_path == "/api/conversations/claim_guest":
            token = extract_token_from_headers(headers) or body.get("token")
            user = get_user_by_token(token)
            if not user:
                return 401, response_headers, json.dumps({"status": "error", "message": "Unauthorized"}).encode("utf-8")

            turns = body.get("turns", [])
            if not turns:
                return 200, response_headers, json.dumps({"status": "success", "message": "No guest turns to claim"}).encode("utf-8")

            first_query = turns[0].get("query", "Guest Legal Inquiry")
            first_jur = turns[0].get("jurisdiction", "AUTO")
            first_cat = turns[0].get("category", "General")
            conv = create_conversation(user["id"], first_query[:35], first_jur, first_cat)

            for t in turns:
                q = t.get("query", "")
                c = t.get("card", {})
                b = c.get("body_text", "")
                j = t.get("jurisdiction", first_jur)
                cat = t.get("category", first_cat)
                save_chat_turn(user["id"], conv["id"], q, b, c, j, cat)

            return 200, response_headers, json.dumps({
                "status": "success",
                "conversation": conv,
                "message": f"Successfully migrated {len(turns)} guest consultation turn(s)"
            }).encode("utf-8")

        elif clean_path == "/api/chat":
            token = extract_token_from_headers(headers) or body.get("token")
            user = get_user_by_token(token) if token else None

            query = body.get("query", "").strip()
            jurisdiction = body.get("jurisdiction", "AUTO")
            category = body.get("category", "General")
            language = body.get("language", "en")
            conv_id = body.get("conversation_id")

            if not query:
                return 400, response_headers, json.dumps({"status": "error", "message": "Query cannot be empty"}).encode("utf-8")

            # Process with Autonomous Legal Reasoning Agent & ChromaDB Vector Search
            reasoning_result = reason_legally(query, jurisdiction, category, language)
            eff_jur = reasoning_result["jurisdiction"]
            eff_cat = reasoning_result["category"]
            eff_lang = reasoning_result["language"]
            card = reasoning_result["card"]

            # If user is authenticated, persist to database under their account
            if user:
                if not conv_id:
                    new_c = create_conversation(user["id"], query[:35], jurisdiction, category)
                    conv_id = new_c["id"]
                try:
                    save_chat_turn(user["id"], conv_id, query, card["body_text"], card, eff_jur, eff_cat)
                except Exception as e:
                    print(f"[api_handler] Error saving turn: {e}")
            else:
                conv_id = conv_id or "guest_session"

            payload = {
                "status": "success",
                "conversation_id": conv_id,
                "is_guest": user is None,
                "jurisdiction": eff_jur,
                "category": eff_cat,
                "language": eff_lang,
                "card": card
            }
            return 200, response_headers, json.dumps(payload, ensure_ascii=False).encode("utf-8")

    return 404, response_headers, json.dumps({"status": "error", "message": "Not found"}).encode("utf-8")
