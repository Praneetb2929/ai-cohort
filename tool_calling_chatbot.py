import json
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

# Pydantic response models
class CoverageResponse(BaseModel):
    plan_id: str
    procedure: str
    is_covered: bool
    copay: float
    coinsurance: str

class ClaimStatusResponse(BaseModel):
    claim_id: str
    status: str
    amount: float
    date_filed: str

class PlanDetailsResponse(BaseModel):
    plan_id: str
    plan_name: str
    annual_deductible: float
    out_of_pocket_max: float

class OutOfPocketEstimateResponse(BaseModel):
    procedure: str
    plan_id: str
    estimated_cost: float

# Tool implementations
def check_coverage(plan_id: str, procedure: str) -> Dict[str, Any]:
    """Check if a procedure is covered under a plan."""
    res = CoverageResponse(
        plan_id=plan_id,
        procedure=procedure,
        is_covered=True,
        copay=20.0,
        coinsurance="10%"
    )
    return res.model_dump()

def get_claim_status(claim_id: str) -> Dict[str, Any]:
    """Fetch status for an insurance claim."""
    res = ClaimStatusResponse(
        claim_id=claim_id,
        status="Processing",
        amount=450.0,
        date_filed="2026-08-10"
    )
    return res.model_dump()

def get_plan_details(plan_id: str) -> Dict[str, Any]:
    """Fetch structured benefits and limits for a plan."""
    res = PlanDetailsResponse(
        plan_id=plan_id,
        plan_name="Gold Plan",
        annual_deductible=1500.0,
        out_of_pocket_max=4000.0
    )
    return res.model_dump()

def estimate_out_of_pocket_cost(procedure: str, plan_id: str) -> Dict[str, Any]:
    """Estimate out-of-pocket patient costs."""
    res = OutOfPocketEstimateResponse(
        procedure=procedure,
        plan_id=plan_id,
        estimated_cost=150.0
    )
    return res.model_dump()

# Tool schemas definition
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_coverage",
            "description": "Check coverage rules and copay for a procedure",
            "parameters": {
                "type": "object",
                "properties": {
                    "plan_id": {"type": "string"},
                    "procedure": {"type": "string"}
                },
                "required": ["plan_id", "procedure"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_claim_status",
            "description": "Get current status of a claim by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "claim_id": {"type": "string"}
                },
                "required": ["claim_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_plan_details",
            "description": "Retrieve comprehensive plan parameters",
            "parameters": {
                "type": "object",
                "properties": {
                    "plan_id": {"type": "string"}
                },
                "required": ["plan_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "estimate_out_of_pocket_cost",
            "description": "Estimate out-of-pocket cost for a medical procedure",
            "parameters": {
                "type": "object",
                "properties": {
                    "procedure": {"type": "string"},
                    "plan_id": {"type": "string"}
                },
                "required": ["procedure", "plan_id"]
            }
        }
    }
]

def execute_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    tool_map = {
        "check_coverage": check_coverage,
        "get_claim_status": get_claim_status,
        "get_plan_details": get_plan_details,
        "estimate_out_of_pocket_cost": estimate_out_of_pocket_cost,
    }
    if tool_name in tool_map:
        return tool_map[tool_name](**args)
    raise ValueError(f"Tool {tool_name} not found")