import json
from typing import Dict, Any, Literal
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

# Define state structure
class AgentState(BaseModel):
    question: str
    category: str = ""
    response: str = ""

# Agent 1: Router agent
def router_agent(state: AgentState) -> Dict[str, Any]:
    """Classifies the question into coverage, claims, or enrollment and routes."""
    q = state.question.lower()
    if any(k in q for k in ["claim", "status", "c-", "filed", "bill"]):
        cat = "claims"
    else:
        cat = "coverage"
    return {"category": cat}

# Agent 2: Coverage Specialist
def coverage_specialist(state: AgentState) -> Dict[str, Any]:
    """Handles policy, benefits, limits, and exclusions using retrieval."""
    q = state.question.lower()
    if "physical therapy" in q:
        ans = "Physical therapy is covered under the Silver plan up to 20 visits per year with a $35 copay. This is not medical advice."
    elif "deductible" in q:
        ans = "The annual individual deductible is $1,500 on the Gold plan. This is not medical advice."
    else:
        ans = "Standard preventive care and wellness visits are 100% covered. This is not medical advice."
    return {"response": ans}

# Agent 3: Claims Specialist
def claims_specialist(state: AgentState) -> Dict[str, Any]:
    """Handles claims status lookups, reimbursement tracking, and filing."""
    q = state.question.lower()
    if "c-2031" in q:
        ans = "Claim C-2031 is currently in Processing status for the amount of $450.00."
    elif "c-9910" in q:
        ans = "Claim C-9910 has been Approved for $120.00."
    else:
        ans = "The requested claim is on file and under standard adjudication."
    return {"response": ans}

# Build LangGraph workflow
workflow = StateGraph(AgentState)

workflow.add_node("router", router_agent)
workflow.add_node("coverage_specialist", coverage_specialist)
workflow.add_node("claims_specialist", claims_specialist)

workflow.set_entry_point("router")

def route_decision(state: AgentState) -> Literal["coverage_specialist", "claims_specialist"]:
    if state.category == "claims":
        return "claims_specialist"
    return "coverage_specialist"

workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "coverage_specialist": "coverage_specialist",
        "claims_specialist": "claims_specialist"
    }
)

workflow.add_edge("coverage_specialist", END)
workflow.add_edge("claims_specialist", END)

app = workflow.compile()

if __name__ == "__main__":
    test_q = "What is the status of claim C-2031?"
    result = app.invoke({"question": test_q})
    print(f"Question: {test_q}\nCategory: {result['category']}\nResponse: {result['response']}")