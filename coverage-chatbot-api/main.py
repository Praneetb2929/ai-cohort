import time
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Coverage Chatbot API")

# In-memory session store: session_id -> list of messages
session_store: Dict[str, List[Dict[str, str]]] = {}

class ChatRequest(BaseModel):
    session_id: str
    member_id: str
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    duration_ms: float

def mock_retrieve_and_answer(message: str) -> str:
    """Simulates retrieve() and generate_answer() / tool-calling pipeline."""
    msg_lower = message.lower()
    if "copay" in msg_lower:
        return "Your copay for primary care visits is $20 under the Gold plan. This is not medical advice."
    elif "deductible" in msg_lower:
        return "Your remaining annual individual deductible is $500. This is not medical advice."
    elif "maternity" in msg_lower or "covered" in msg_lower:
        return "Maternity care services are covered subject to your plan deductible and copays. This is not medical advice."
    return "Thank you for reaching out. Please verify with member services for further details. This is not medical advice."

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    start_time = time.time()
    
    # Initialize history list if session is new
    if req.session_id not in session_store:
        session_store[req.session_id] = []
    
    # Record user message
    session_store[req.session_id].append({"role": "user", "content": req.message})
    
    # Error handling around LLM pipeline execution
    try:
        assistant_reply = mock_retrieve_and_answer(req.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request through the language model."
        )
    
    # Record assistant response
    session_store[req.session_id].append({"role": "assistant", "content": assistant_reply})
    
    duration = (time.time() - start_time) * 1000
    print(f"[TIMING] Session {req.session_id} - Processing time: {duration:.2f}ms")
    
    return ChatResponse(
        session_id=req.session_id,
        response=assistant_reply,
        duration_ms=duration
    )

@app.get("/history/{session_id}")
async def get_history(session_id: str):
    if session_id not in session_store:
        return {"session_id": session_id, "history": []}
    return {"session_id": session_id, "history": session_store[session_id]}