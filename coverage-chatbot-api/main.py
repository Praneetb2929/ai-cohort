import time
import hashlib
import sqlite3
import datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, status, Request
from pydantic import BaseModel
from token_utils import count_tokens, estimate_cost

app = FastAPI(title="Coverage Chatbot API with Caching & Rate Limiting")

DB_FILE = "conversations.db"

# In-memory stores
general_cache: Dict[str, str] = {}
rate_limit_store: Dict[str, list] = {}  # member_id -> list of timestamps

RATE_LIMIT_PER_MINUTE = 20

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TEXT
        )
    """)
    # Token usage logging table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS token_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            timestamp TEXT,
            input_tokens INTEGER,
            output_tokens INTEGER,
            estimated_cost REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

class ChatRequest(BaseModel):
    session_id: str
    member_id: str
    message: str
    plan_id: Optional[str] = "Gold"

class ChatResponse(BaseModel):
    session_id: str
    response: str
    cached: bool = False
    input_tokens: int
    output_tokens: int
    estimated_cost: float

def check_rate_limit(member_id: str):
    """Enforces request cap per member per minute."""
    now = time.time()
    timestamps = rate_limit_store.get(member_id, [])
    # Keep only requests from the last 60 seconds
    timestamps = [t for t in timestamps if now - t < 60]
    if len(timestamps) >= RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Maximum 20 requests per minute per member."
        )
    timestamps.append(now)
    rate_limit_store[member_id] = timestamps

def get_cache_key(message: str) -> Optional[str]:
    """Generates hash for general questions; returns None for member-specific data."""
    msg_lower = message.strip().lower()
    # Member-specific inquiries must NEVER be cached
    if any(k in msg_lower for k in ["claim", "c-", "member", "status", "bill", "my deductible"]):
        return None
    return hashlib.sha256(msg_lower.encode("utf-8")).hexdigest()

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # 1. Rate Limiting Check
    check_rate_limit(req.member_id)
    
    input_tokens = count_tokens(req.message)
    now_iso = datetime.datetime.utcnow().isoformat()
    cache_key = get_cache_key(req.message)

    # 2. Check General Question Cache
    if cache_key and cache_key in general_cache:
        cached_response = general_cache[cache_key]
        output_tokens = count_tokens(cached_response)
        return ChatResponse(
            session_id=req.session_id,
            response=cached_response,
            cached=True,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=0.0
        )

    # 3. Simulate RAG / Generation
    msg_lower = req.message.lower()
    if "copay" in msg_lower:
        assistant_reply = "Your primary care visit copay is $20 under the Gold plan. This is not medical advice."
    elif "maternity" in msg_lower:
        assistant_reply = "Maternity care is covered under comprehensive benefits subject to plan deductible. This is not medical advice."
    elif "c-2031" in msg_lower or "claim" in msg_lower:
        assistant_reply = "Claim C-2031 is currently in Processing status for $450.00."
    else:
        assistant_reply = "Standard preventive care is covered 100% with $0 copay. This is not medical advice."

    output_tokens = count_tokens(assistant_reply)
    cost = estimate_cost(input_tokens, output_tokens)

    # 4. Save to Cache if general question
    if cache_key:
        general_cache[cache_key] = assistant_reply

    # 5. Log Token Usage to SQLite
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO token_usage (session_id, timestamp, input_tokens, output_tokens, estimated_cost) VALUES (?, ?, ?, ?, ?)",
        (req.session_id, now_iso, input_tokens, output_tokens, cost)
    )
    cursor.execute(
        "INSERT INTO conversations (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
        (req.session_id, "user", req.message, now_iso)
    )
    cursor.execute(
        "INSERT INTO conversations (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
        (req.session_id, "assistant", assistant_reply, now_iso)
    )
    conn.commit()
    conn.close()

    return ChatResponse(
        session_id=req.session_id,
        response=assistant_reply,
        cached=False,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        estimated_cost=cost
    )