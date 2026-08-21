import json
import asyncio
from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel
import mcp_server  # Reference MCP tools and mcp_server

# Fallback constant
FALLBACK_RESPONSE = "I'm having trouble accessing that right now, please contact member support."

class AgentState(BaseModel):
    session_id: str = "default_session"
    question: str
    selected_plan: Optional[str] = "Gold"
    category: str = ""
    response: str = ""

# Mock Day 20 Memory Store Loader
def get_memory_context(session_id: str) -> Dict[str, Any]:
    return {"selected_plan": "Gold", "history_summary": "User enrolled in Gold Plan"}

# Async MCP Tool Execution with Timeout, Retry (max 1), and Fallback
async def execute_mcp_tool_with_resilience(tool_func, *args, **kwargs) -> str:
    retries = 1
    for attempt in range(retries + 1):
        try:
            # Enforce 10s timeout using asyncio.wait_for
            result = await asyncio.wait_for(asyncio.to_thread(tool_func, *args, **kwargs), timeout=10)
            return result
        except Exception as e:
            if attempt < retries:
                await asyncio.sleep(0.5)
                continue
            return FALLBACK_RESPONSE

# Router Agent
def router_agent(state: AgentState) -> Dict[str, Any]:
    q = state.question.lower()
    if any(k in q for k in ["claim", "status", "c-", "filed"]):
        cat = "claims"
    else:
        cat = "coverage"
    return {"category": cat}

# Coverage Specialist using MCP check_coverage
def coverage_specialist(state: AgentState) -> Dict[str, Any]:
    memory = get_memory_context(state.session_id)
    plan = state.selected_plan or memory.get("selected_plan", "Gold")
    
    try:
        raw_res = asyncio.run(
            execute_mcp_tool_with_resilience(mcp_server.check_coverage, plan_id=plan, procedure=state.question)
        )
        if raw_res == FALLBACK_RESPONSE:
            return {"response": FALLBACK_RESPONSE}
        data = json.loads(raw_res)
        return {"response": f"Coverage info for {data['plan']['plan_name']}: {data['policy_context']} This is not medical advice."}
    except Exception:
        return {"response": FALLBACK_RESPONSE}

# Claims Specialist using MCP get_claim_status
def claims_specialist(state: AgentState) -> Dict[str, Any]:
    try:
        raw_res = asyncio.run(
            execute_mcp_tool_with_resilience(mcp_server.get_claim_status, claim_id="C-2031")
        )
        if raw_res == FALLBACK_RESPONSE:
            return {"response": FALLBACK_RESPONSE}
        data = json.loads(raw_res)
        return {"response": f"Claim {data['claim_id']} status is {data['status']} with amount ${data['amount']}."}
    except Exception:
        return {"response": FALLBACK_RESPONSE}

def run_workflow(question: str, session_id: str = "test_sess") -> str:
    state = AgentState(question=question, session_id=session_id)
    cat = router_agent(state)["category"]
    state.category = cat
    if cat == "claims":
        return claims_specialist(state)["response"]
    return coverage_specialist(state)["response"]

if __name__ == "__main__":
    print(run_workflow("What is the status of claim C-2031?"))