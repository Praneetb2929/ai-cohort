# Chaos Engineering & Fault Tolerance Test Report

## 1. System Resilience Architecture
* **MCP Integration**: Uses `mcp_server.py` tool bindings (`check_coverage`, `get_claim_status`).
* **Memory Wiring**: Wires conversation memory store to retain `selected_plan` (e.g. Gold Plan) across turns.
* **Timeout Boundary**: Wrapped in `asyncio.wait_for(..., timeout=10)`.
* **Retry Policy**: Maximum 1 retry allowed for transient network/tool failures.
* **Graceful Degradation**: Catches all exceptions and falls back cleanly without returning raw 500 crashes to the member:
  > *"I'm having trouble accessing that right now, please contact member support."*

---

## 2. Chaos Injection Scenarios

### Test 1: Simulated Tool Exception / Broken Dependency
* **Failure Injected**: Renamed `get_claim_status` in the backend service to simulate runtime failure.
* **Workflow Trajectory**:
  1. Router categorized request as `claims`.
  2. Claims Specialist attempted execution of `get_claim_status`.
  3. Encountered `AttributeError` / invocation fault.
  4. Performed retry 1/1.
  5. Caught terminal exception in `try/except` block.
  6. Returned graceful fallback message.
* **User-Facing Output**: *"I'm having trouble accessing that right now, please contact member support."*
* **Status**: Passed (0 crashes, 0 unhandled 500 errors).

---

### Test 2: Simulated Tool Latency Timeout
* **Failure Injected**: Injected a 15-second artificial sleep inside `check_coverage` (exceeding the 10s ceiling).
* **Workflow Trajectory**:
  1. Router categorized request as `coverage`.
  2. Coverage Specialist invoked MCP tool.
  3. `asyncio.wait_for` timed out at 10.0 seconds.
  4. Attempted 1 retry which timed out.
  5. Fallback handler caught `asyncio.TimeoutError`.
* **User-Facing Output**: *"I'm having trouble accessing that right now, please contact member support."*
* **Status**: Passed (Timeout caught gracefully within budget).