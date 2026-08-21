import json
import sqlite3
from typing import Any, Dict
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Coverage-Claims-Server")

def vector_lookup(question: str) -> str:
    """Internal lookup simulating Day 10 vector retrieval."""
    return "Coverage Details: Physical therapy covered up to 20 visits per year with a $35 copay on Silver plan."

def plans_db_lookup(plan_id: str) -> Dict[str, Any]:
    """Internal lookup against Day 4 structured plans database."""
    return {
        "plan_id": plan_id,
        "plan_name": f"{plan_id.capitalize()} Plan",
        "copay": 20.0,
        "deductible": 1500.0,
        "coinsurance": "10%"
    }

@mcp.tool()
def check_coverage(plan_id: str, procedure: str) -> str:
    """Check insurance coverage details, copays, and limits for a procedure."""
    plan_info = plans_db_lookup(plan_id)
    policy_info = vector_lookup(procedure)
    
    result = {
        "plan": plan_info,
        "procedure": procedure,
        "policy_context": policy_info,
        "is_covered": True
    }
    return json.dumps(result)

@mcp.tool()
def get_claim_status(claim_id: str) -> str:
    """Get the current processing status and details for an insurance claim."""
    result = {
        "claim_id": claim_id,
        "status": "Processing",
        "amount": 450.0,
        "date_filed": "2026-08-10"
    }
    return json.dumps(result)

if __name__ == "__main__":
    mcp.run()