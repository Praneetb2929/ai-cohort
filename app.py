import uuid
import requests
import streamlit as st

st.set_page_config(page_title="Insurance Coverage Chatbot", page_icon="💬")

API_BASE_URL = "http://localhost:8000"

# Initialize session_id via uuid4() in st.session_state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Initialize message history list in st.session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar controls
with st.sidebar:
    st.title("Settings")
    # Plan selector dropdown populated from standard plans table
    selected_plan = st.selectbox(
        "Select Insurance Plan",
        options=["Gold Plan", "Silver Plan", "Bronze Plan"]
    )
    
    # "New conversation" button to reset session_id and clear history
    if st.button("New conversation"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

st.title("Insurance Coverage Assistant")
st.caption(f"Session ID: {st.session_state.session_id} | Plan: {selected_plan}")

# Render conversation thread from history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input field
if prompt := st.chat_input("Ask a question about your coverage or claims..."):
    # Append & render user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Post message to /chat endpoint
    with st.chat_message("assistant"):
        try:
            payload = {
                "session_id": st.session_state.session_id,
                "member_id": "mem_default",
                "message": prompt
            }
            resp = requests.post(f"{API_BASE_URL}/chat", json=payload, timeout=10)
            if resp.status_code == 200:
                answer = resp.json().get("response", "")
            else:
                answer = "Error: Backend returned a non-200 status code."
        except Exception:
            answer = "Error connecting to backend service. Please ensure the API is running at http://localhost:8000."
        
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})