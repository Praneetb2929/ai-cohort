# MCP Server Local Integration & Verification Log

## 1. Server Configuration & Manifest
* **Server Implementation**: `mcp_server.py` using FastMCP / MCP Python SDK (`mcp`).
* **Transport**: Standard I/O (`stdio`).
* **Exposed Tools**:
  1. `check_coverage(plan_id, procedure)`: Calls internal `vector_lookup()` and queries SQLite `plans` table.
  2. `get_claim_status(claim_id)`: Fetches status and amounts for submitted claims.

---

## 2. Client Registration (`claude_desktop_config.json` / `cline_mcp_settings.json`)

```json
{
  "mcpServers": {
    "coverage-server": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_server.py"]
    }
  }
}