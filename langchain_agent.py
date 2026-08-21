import json
from typing import Optional
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models.fake import FakeListLLM

# Define core tools matching the mission requirements
def check_coverage(query: str) -> str:
    """Check insurance coverage rules and copay for a specific procedure."""
    return json.dumps({
        "plan_id": "Gold",
        "procedure": "physical therapy",
        "is_covered": True,
        "copay": 20.0,
        "coinsurance": "10%"
    })

def get_claim_status(claim_id: str) -> str:
    """Fetch status and amount for an insurance claim by claim ID."""
    return json.dumps({
        "claim_id": claim_id.strip(),
        "status": "Processing",
        "amount": 450.0,
        "date_filed": "2026-08-10"
    })

def get_plan_details(plan_id: str) -> str:
    """Retrieve comprehensive plan parameters including deductible and OOP max."""
    return json.dumps({
        "plan_id": plan_id.strip(),
        "plan_name": "Gold Plan",
        "annual_deductible": 1500.0,
        "out_of_pocket_max": 4000.0
    })

# Wrap tools in LangChain Tool objects with clear descriptions
tools = [
    Tool(
        name="check_coverage",
        func=check_coverage,
        description="Useful for checking whether a specific medical procedure or service is covered under an insurance plan."
    ),
    Tool(
        name="get_claim_status",
        func=get_claim_status,
        description="Useful for looking up the current status, amount, and date of a filed claim using a claim ID."
    ),
    Tool(
        name="get_plan_details",
        func=get_plan_details,
        description="Useful for retrieving general plan benefits such as deductible limits and out-of-pocket maximums."
    )
]

# ReAct prompt template
REACT_PROMPT = PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
Thought:{agent_scratchpad}""")

# Mock LLM responses to enable standalone execution without live API keys
mock_responses = [
    " I should look up the claim status.\nAction: get_claim_status\nAction Input: C-2031\n",
    " I now have the claim details.\nFinal Answer: Claim C-2031 is currently Processing for $450.00. This is not medical advice.",
]

llm = FakeListLLM(responses=mock_responses)

# Create ReAct agent and AgentExecutor with verbose=True
agent = create_react_agent(llm=llm, tools=tools, prompt=REACT_PROMPT)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

if __name__ == "__main__":
    test_query = "What is the status of claim C-2031?"
    print(f"Running agent on query: {test_query}")
    result = agent_executor.invoke({"input": test_query})
    print("Agent Result:", result)