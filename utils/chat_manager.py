import streamlit as st

def initialize_chat():
    """Initialize chatbot session history."""

    if "financial_chat_history" not in st.session_state:
        st.session_state.financial_chat_history = []


def clear_chat():
    """Clear conversation history."""

    st.session_state.financial_chat_history = []


