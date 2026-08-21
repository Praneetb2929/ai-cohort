# Server-Sent Events (SSE) Streaming Notes

## Implementation Architecture
* **FastAPI Backend**: Uses `StreamingResponse` with `media_type="text/event-stream"` to push SSE data tokens in the standard format (`data: <token>\n\n`).
* **Streamlit Frontend**: Consumes SSE streams using `requests.post(..., stream=True)` and iterates chunks via `response.iter_lines()`, updating a placeholder (`st.empty()`) in real time with a typewriter effect.

## Error Handling, Timeouts & Dropped Connections
* **Initial Response Spinner**: A UI spinner displays until the initial token arrives to reassure the user.
* **Stream Timeouts**: The client enforces an explicit `timeout=15` seconds. If the LLM service hangs before starting generation, `requests.exceptions.Timeout` triggers a user-friendly error message.
* **Mid-Stream Disconnects**: If network transport is terminated abruptly mid-stream, `response.iter_lines()` raises an exception which is caught gracefully, retaining the partial context while notifying the user to retry.