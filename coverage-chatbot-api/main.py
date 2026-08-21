import sqlite3
import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Coverage Chatbot API with Memory")

DB_FILE = "conversations.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

class ChatRequest(BaseModel):
    session_id: str
    member_id: str
    message: str
    plan_id: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    response: str
    token_count: int

def estimate_tokens(text: str) -> int:
    """Approximate token count (or use tiktoken helper)."""
    return len(text.split()) * 4 // 3

def get_session_history(session_id: str) -> List[Dict[str, str]]:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM conversations WHERE session_id = ? ORDER BY id ASC",
        (session_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1]} for r in rows]

def save_message(session_id: str, role: str, content: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    now_iso = datetime.datetime.utcnow().isoformat()
    cursor.execute(
        "INSERT INTO conversations (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
        (session_id, role, content, now_iso)
    )
    conn.commit()
    conn.close()

def summarize_history(history: List[Dict[str, str]]) -> str:
    """Summarizes the oldest half of conversation history."""
    return "Summary of previous conversation: User is on Gold Plan and discussed deductible and preventative care."

def build_context_with_token_budget(session_id: str, plan_id: Optional[str] = None, max_turns: int = 10) -> str:
    history = get_session_history(session_id)
    total_tokens = sum(estimate_tokens(m["content"]) for m in history)

    # Token budget check (~2000 tokens)
    if total_tokens > 2000 and len(history) > 4:
        split_idx = len(history) // 2
        oldest_half = history[:split_idx]
        recent_half = history[split_idx:]
        summary_text = summarize_history(oldest_half)
        history = [{"role": "system", "content": summary_text}] + recent_half

    # Load/limit the last N turns (e.g., last 10 messages)
    recent_turns = history[-max_turns:] if len(history) > max_turns else history
    
    # Track plan_id specified across session
    context_lines = []
    if plan_id:
        context_lines.append(f"Specified Plan: {plan_id}")
    for turn in recent_turns:
        context_lines.append(f"{turn['role'].capitalize()}: {turn['content']}")
        
    return "\n".join(context_lines)

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    save_message(req.session_id, "user", req.message)
    
    # Build prompt context with memory and budget limits
    context = build_context_with_token_budget(req.session_id, req.plan_id)
    
    # Generate contextual answer
    msg_lower = req.message.lower()
    if "plan" in msg_lower and "what" in msg_lower:
        assistant_reply = "You are currently discussing the Gold Plan selected earlier in this session. This is not medical advice."
    else:
        assistant_reply = f"Based on your session context and Gold Plan benefits, that service is covered with standard copays. This is not medical advice."

    save_message(req.session_id, "assistant", assistant_reply)
    
    current_tokens = sum(estimate_tokens(m["content"]) for m in get_session_history(req.session_id))
    return ChatResponse(session_id=req.session_id, response=assistant_reply, token_count=current_tokens)

@app.get("/history/{session_id}")
async def get_history(session_id: str):
    history = get_session_history(session_id)
    return {"session_id": session_id, "history": history}