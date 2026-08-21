import uuid
import requests
import streamlit as st

st.set_page_config(page_title="Insurance Coverage Chatbot", page_icon="💬")

API_BASE_URL = "http://localhost:8000"

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("Settings")
    selected_plan = st.selectbox(
        "Select Insurance Plan",
        options=["Gold Plan", "Silver Plan", "Bronze Plan"]
    )
    if st.button("New conversation"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

st.title("Insurance Coverage Assistant")
st.caption(f"Session ID: {st.session_state.session_id} | Plan: {selected_plan}")

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User prompt
if prompt := st.chat_input("Ask a question about your coverage or claims..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        
        try:
            payload = {
                "session_id": st.session_state.session_id,
                "member_id": "mem_default",
                "message": prompt
            }
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{API_BASE_URL}/chat",
                    json=payload,
                    stream=True,
                    timeout=15
                )

            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        line_text = line.decode("utf-8")
                        if line_text.startswith("data: "):
                            token = line_text[6:]
                            full_response += token
                            placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                placeholder.error("Error: Received non-200 response from backend.")
        except requests.exceptions.Timeout:
            placeholder.error("Request timed out. Please try again.")
        except Exception as e:
            placeholder.error("Error connecting to server or stream interrupted.")