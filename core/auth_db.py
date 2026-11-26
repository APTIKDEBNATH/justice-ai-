"""
Justice AI - User Authentication & Conversation Persistence Engine
Manages multi-tenant user authentication, secure credential hashing,
session tokens, and isolated per-user conversation storage using SQLite.
"""

import sqlite3
import os
import hashlib
import uuid
import json
import time
from typing import Dict, List, Optional, Tuple, Any

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "justice_ai.db")

def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    if not salt:
        salt = os.urandom(16).hex()
    pwd_hash = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return pwd_hash, salt

def init_db():
    conn = get_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                jurisdiction TEXT DEFAULT 'AUTO',
                category TEXT DEFAULT 'General',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                card_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS shared_chats (
                id TEXT PRIMARY KEY,
                payload_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    conn.close()
    _seed_demo_user()

def _seed_demo_user():
    """Seeds a sample demo account for immediate testing."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username = 'demo';")
        if not cur.fetchone():
            pwd_hash, salt = hash_password("password123")
            cur.execute("""
                INSERT INTO users (username, password_hash, salt, name)
                VALUES ('demo', ?, ?, 'Demo Counsel');
            """, (pwd_hash, salt))
            user_id = cur.lastrowid
            
            # Seed sample conversation 1
            conv1_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO conversations (id, user_id, title, jurisdiction, category)
                VALUES (?, ?, 'Landlord termination notice', 'DE', 'Tenancy: Eviction & Termination Notice');
            """, (conv1_id, user_id))

            c1_card = {
                "headline": "In most cases, yes. A landlord needs a legitimate reason to end an open-ended residential lease.",
                "body_text": "Typical valid reasons are genuine personal use of the home (Eigenbedarf) or a serious breach by the tenant, and the reason must be stated in the written notice. The landlord's notice period starts at three months and gets longer the more years you have lived there.",
                "tag_label": "Germany · Tenancy: Eviction & Termination Notice",
                "verified_label": "Answered from official sources",
                "sources_label": "SOURCES",
                "sources": [
                    {"title": "BGB § 573 · Ordinary termination by the landlord", "domain": "gesetze-im-internet.de", "url": "https://www.gesetze-im-internet.de/bgb/__573.html"},
                    {"title": "BGB § 573c · Notice periods", "domain": "gesetze-im-internet.de", "url": "https://www.gesetze-im-internet.de/bgb/__573c.html"}
                ],
                "confidence_label": "Retrieval confidence",
                "confidence_level": "High",
                "confidence_percentage": 90,
                "disclaimer": "General legal information, not formal legal advice. Consult a licensed legal practitioner in your jurisdiction.",
                "chips": ["What if I have lived here over 8 years?", "Can I object to the termination?", "Find a tenant association"]
            }

            cur.execute("""
                INSERT INTO messages (conversation_id, role, content, card_json)
                VALUES (?, 'user', 'My landlord in Germany sent me a termination letter. Does he need a reason?', NULL);
            """, (conv1_id,))
            cur.execute("""
                INSERT INTO messages (conversation_id, role, content, card_json)
                VALUES (?, 'assistant', ?, ?);
            """, (conv1_id, c1_card["body_text"], json.dumps(c1_card)))

            # Seed sample conversation 2
            conv2_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO conversations (id, user_id, title, jurisdiction, category)
                VALUES (?, ?, 'Defective online product refund', 'IN', 'Consumer Protection & Defective Goods');
            """, (conv2_id, user_id))

            c2_card = {
                "headline": "You have the statutory right to file a consumer complaint for repair, replacement, or a full refund.",
                "body_text": "First, send a written complaint to the seller and save all proof of order, payment, and defect. If unresolved, an electronic complaint can be lodged before the District Consumer Commission via the official e-Daakhil portal within 2 years.",
                "tag_label": "India · Consumer Protection & Defective Goods",
                "verified_label": "Answered from official sources",
                "sources_label": "SOURCES",
                "sources": [
                    {"title": "Consumer Protection Act, 2019 · Section 39", "domain": "indiacode.nic.in", "url": "https://www.indiacode.nic.in/handle/123456789/15256"}
                ],
                "confidence_label": "Retrieval confidence",
                "confidence_level": "High",
                "confidence_percentage": 88,
                "disclaimer": "General legal information, not formal legal advice.",
                "chips": ["Draft formal notice to seller", "How to file on e-Daakhil?"]
            }

            cur.execute("""
                INSERT INTO messages (conversation_id, role, content, card_json)
                VALUES (?, 'user', 'I ordered a phone online that arrived defective. Seller refuses refund. What are my rights?', NULL);
            """, (conv2_id,))
            cur.execute("""
                INSERT INTO messages (conversation_id, role, content, card_json)
                VALUES (?, 'assistant', ?, ?);
            """, (conv2_id, c2_card["body_text"], json.dumps(c2_card)))

            conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"[auth_db] Seed error: {e}")
    finally:
        conn.close()

def register_user(username: str, password: str, name: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str], Optional[str]]:
    username = username.strip().lower()
    name = name.strip()
    if not username or len(username) < 3:
        return False, None, None, "Username must be at least 3 characters."
    if not password or len(password) < 4:
        return False, None, None, "Password must be at least 4 characters."
    if not name:
        name = username.capitalize()

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username = ?;", (username,))
        if cur.fetchone():
            return False, None, None, "Username already exists. Please sign in or choose another."

        pwd_hash, salt = hash_password(password)
        cur.execute("""
            INSERT INTO users (username, password_hash, salt, name)
            VALUES (?, ?, ?, ?);
        """, (username, pwd_hash, salt, name))
        user_id = cur.lastrowid
        token = str(uuid.uuid4())
        cur.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?);", (token, user_id))
        conn.commit()

        user_dict = {"id": user_id, "username": username, "name": name}
        return True, user_dict, token, None
    except Exception as e:
        conn.rollback()
        return False, None, None, f"Database error: {str(e)}"
    finally:
        conn.close()

def authenticate_user(username: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str], Optional[str]]:
    username = username.strip().lower()
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, username, password_hash, salt, name FROM users WHERE username = ?;", (username,))
        row = cur.fetchone()
        if not row:
            return False, None, None, "Invalid username or password."

        user_id = row["id"]
        salt = row["salt"]
        stored_hash = row["password_hash"]
        calc_hash, _ = hash_password(password, salt)

        if calc_hash != stored_hash:
            return False, None, None, "Invalid username or password."

        token = str(uuid.uuid4())
        cur.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?);", (token, user_id))
        conn.commit()

        user_dict = {"id": user_id, "username": row["username"], "name": row["name"]}
        return True, user_dict, token, None
    except Exception as e:
        return False, None, None, f"Authentication error: {str(e)}"
    finally:
        conn.close()

def get_user_by_token(token: str) -> Optional[Dict[str, Any]]:
    if not token:
        return None
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT u.id, u.username, u.name 
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.token = ?;
        """, (token,))
        row = cur.fetchone()
        if row:
            return {"id": row["id"], "username": row["username"], "name": row["name"]}
        return None
    finally:
        conn.close()

def delete_session(token: str):
    if not token:
        return
    conn = get_connection()
    try:
        with conn:
            conn.execute("DELETE FROM sessions WHERE token = ?;", (token,))
    finally:
        conn.close()

def get_user_conversations(user_id: int) -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, title, jurisdiction, category, updated_at, created_at
            FROM conversations
            WHERE user_id = ?
            ORDER BY updated_at DESC;
        """, (user_id,))
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def create_conversation(user_id: int, title: str = "New legal question", jurisdiction: str = "AUTO", category: str = "General") -> Dict[str, Any]:
    conv_id = str(uuid.uuid4())
    conn = get_connection()
    try:
        with conn:
            conn.execute("""
                INSERT INTO conversations (id, user_id, title, jurisdiction, category)
                VALUES (?, ?, ?, ?, ?);
            """, (conv_id, user_id, title, jurisdiction, category))
        return {
            "id": conv_id,
            "user_id": user_id,
            "title": title,
            "jurisdiction": jurisdiction,
            "category": category
        }
    finally:
        conn.close()

def get_conversation_details(user_id: int, conversation_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, title, jurisdiction, category, updated_at
            FROM conversations
            WHERE id = ? AND user_id = ?;
        """, (conversation_id, user_id))
        conv = cur.fetchone()
        if not conv:
            return None

        cur.execute("""
            SELECT role, content, card_json, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC;
        """, (conversation_id,))
        raw_msgs = cur.fetchall()

        messages = []
        for m in raw_msgs:
            msg_obj = {
                "role": m["role"],
                "content": m["content"]
            }
            if m["card_json"]:
                try:
                    msg_obj["card"] = json.loads(m["card_json"])
                except Exception:
                    msg_obj["card"] = None
            messages.append(msg_obj)

        return {
            "conversation": dict(conv),
            "messages": messages
        }
    finally:
        conn.close()

def save_chat_turn(user_id: int, conversation_id: str, query: str, response_text: str, card_data: Optional[Dict[str, Any]], jurisdiction: str, category: str):
    conn = get_connection()
    try:
        cur = conn.cursor()
        # Verify ownership
        cur.execute("SELECT id, title FROM conversations WHERE id = ? AND user_id = ?;", (conversation_id, user_id))
        conv = cur.fetchone()
        
        # If conversation doesn't exist, create it
        if not conv:
            title = query[:40] + ("..." if len(query) > 40 else "")
            cur.execute("""
                INSERT INTO conversations (id, user_id, title, jurisdiction, category)
                VALUES (?, ?, ?, ?, ?);
            """, (conversation_id, user_id, title, jurisdiction, category))
        else:
            # If title is generic default, update title to the first user question
            if conv["title"] in ("New legal question", "New Question", "Untitled"):
                new_title = query[:40] + ("..." if len(query) > 40 else "")
                cur.execute("""
                    UPDATE conversations 
                    SET title = ?, jurisdiction = ?, category = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?;
                """, (new_title, jurisdiction, category, conversation_id))
            else:
                cur.execute("""
                    UPDATE conversations 
                    SET jurisdiction = ?, category = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?;
                """, (jurisdiction, category, conversation_id))

        # Insert user message
        cur.execute("""
            INSERT INTO messages (conversation_id, role, content, card_json)
            VALUES (?, 'user', ?, NULL);
        """, (conversation_id, query))

        # Insert assistant message
        card_json = json.dumps(card_data, ensure_ascii=False) if card_data else None
        cur.execute("""
            INSERT INTO messages (conversation_id, role, content, card_json)
            VALUES (?, 'assistant', ?, ?);
        """, (conversation_id, response_text, card_json))

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"[auth_db] Save turn error: {e}")
        raise e
    finally:
        conn.close()

def delete_conversation(user_id: int, conversation_id: str) -> bool:
    conn = get_connection()
    try:
        with conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM conversations WHERE id = ? AND user_id = ?;", (conversation_id, user_id))
            return cur.rowcount > 0
    finally:
        conn.close()

def save_shared_chat(payload: Dict[str, Any]) -> str:
    """Stores a shared conversation snapshot and returns its short share ID."""
    share_id = uuid.uuid4().hex[:10]
    conn = get_connection()
    try:
        with conn:
            conn.execute(
                "INSERT INTO shared_chats (id, payload_json) VALUES (?, ?);",
                (share_id, json.dumps(payload, ensure_ascii=False))
            )
        return share_id
    finally:
        conn.close()

def get_shared_chat(share_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a shared conversation snapshot by its share ID."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT payload_json FROM shared_chats WHERE id = ?;", (share_id,))
        row = cur.fetchone()
        if not row:
            return None
        return json.loads(row["payload_json"])
    finally:
        conn.close()

# Auto-initialize database tables on import
init_db()
