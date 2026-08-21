import uuid
import streamlit as st
from response_cards import ClaimStatusCard, CoverageSummaryCard

st.set_page_config(page_title="Insurance Coverage Chatbot", page_icon="💬")

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

def render_message_payload(msg: dict):
    st.markdown(msg.get("content", ""))
    
    # Render ClaimStatusCard UI
    if msg.get("claim_card"):
        card = ClaimStatusCard(**msg["claim_card"])
        with st.container(border=True):
            st.markdown(f"### 📋 Claim Status: `{card.claim_id}`")
            col1, col2, col3 = st.columns(3)
            col1.metric("Status", card.status)
            col2.metric("Billed Amount", f"${card.amount:,.2f}")
            col3.metric("Service Date", card.date)

    # Render CoverageSummaryCard UI
    if msg.get("coverage_card"):
        card = CoverageSummaryCard(**msg["coverage_card"])
        with st.container(border=True):
            st.markdown(f"### 🛡️ Coverage Details: **{card.plan_name}**")
            col1, col2, col3 = st.columns(3)
            col1.metric("Covered", "Yes ✅" if card.covered else "No ❌")
            col2.metric("Copay", f"${card.copay:.2f}")
            col3.metric("Deductible", f"${card.deductible:,.2f}")

    # Render Citations / Policy Sources Expander
    if msg.get("citations"):
        with st.expander("📚 Policy Sources"):
            for citation in msg["citations"]:
                st.markdown(f"- **[{citation.get('id', 'chunk')}]** *{citation.get('source_file', 'doc')}* (Section: `{citation.get('section', 'general')}`): {citation.get('text', '')}")

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        render_message_payload(msg)

# Chat input
if prompt := st.chat_input("Ask a question about your coverage or claims..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_lower = prompt.lower()
        
        # Test routing and mock responses
        if "c-2031" in p_lower or "claim" in p_lower:
            ans_text = "Here is the current processing status of your claim:"
            claim_data = {
                "claim_id": "C-2031",
                "status": "Processing",
                "amount": 450.00,
                "date": "2026-08-10"
            }
            msg_payload = {"role": "assistant", "content": ans_text, "claim_card": claim_data}
        elif "gold" in p_lower or "deductible" in p_lower:
            ans_text = "Here is your coverage summary for primary care visits:"
            cov_data = {
                "plan_name": "Gold Plan",
                "deductible": 1500.00,
                "copay": 20.00,
                "covered": True
            }
            msg_payload = {"role": "assistant", "content": ans_text, "coverage_card": cov_data}
        else:
            ans_text = "Physical therapy is covered under the Silver plan up to 20 visits per year [1]. This is not medical advice."
            citations = [
                {
                    "id": "chunk_002",
                    "source_file": "policy_guidelines.txt",
                    "section": "coverage",
                    "text": "Physical therapy covered up to 20 visits per calendar year with $35 copay."
                }
            ]
            msg_payload = {"role": "assistant", "content": ans_text, "citations": citations}

        render_message_payload(msg_payload)
        st.session_state.messages.append(msg_payload)