# Multi-Agent vs. Single-Agent Architecture Comparison Report

## 1. System Architecture
* **Framework**: LangGraph / CrewAI Workflow
* **Router Agent**: Analyzes user intent and categorizes requests (`coverage`, `claims`, `enrollment`) to dispatch to the appropriate specialist.
* **Specialist Agents**:
  * `Coverage Specialist`: Focuses on policy text, benefit limits, and medical procedure coverage.
  * `Claims Specialist`: Interacts with structured claim databases, processing pipelines, and payment records.

---

## 2. Multi-Agent Evaluation on 5 Test Questions

| # | Question | Router Classification | Assigned Specialist | Multi-Agent Answer | Single-Agent Baseline Difference |
|---|---|---|---|---|---|
| 1 | "What is the status of claim C-2031?" | `claims` | Claims Specialist | Claim C-2031 is currently in Processing status for $450.00. | Cleaner trace with zero risk of running semantic doc search. |
| 2 | "Is physical therapy covered under the Silver plan?" | `coverage` | Coverage Specialist | Physical therapy is covered up to 20 visits/yr ($35 copay). This is not medical advice. | Context window isolated strictly to policy chunks. |
| 3 | "What is the deductible for the Gold plan?" | `coverage` | Coverage Specialist | The individual deductible for the Gold plan is $1,500. This is not medical advice. | Same answer, narrower specialist prompt overhead. |
| 4 | "Has claim C-9910 been approved?" | `claims` | Claims Specialist | Claim C-9910 has been Approved for $120.00. | Bypassed vector database tools completely. |
| 5 | "Are routine checkups covered without copay?" | `coverage` | Coverage Specialist | Standard preventive care is covered 100% with $0 copay. This is not medical advice. | Precise prompt instructions prevented medical hallucination. |

* **Routing Accuracy**: 5 / 5 (100% accuracy on intent routing).

---

## 3. When Is Multi-Agent Worth It?

* **Genuinely Different Domains (Coverage vs. Claims)**:
  * Multi-agent architecture provides tangible value when splitting specialized tooling, distinct system prompts, and different security permissions (e.g., claims database access vs. public policy vector embeddings). It prevents tool description confusion in large action spaces.
* **Simple / Single-Domain Questions**:
  * For single-domain lookup tasks, a single well-tooled ReAct agent is faster, simpler to maintain, and avoids inter-agent latency and coordination overhead.