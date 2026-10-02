"""
Streamlit AI chatbot using the Groq API (free tier).

Setup:
    pip install streamlit groq
    Get a free key at https://console.groq.com/keys

Run (PowerShell, same window you run streamlit in):
    $env:GROQ_API_KEY="your_key"
    streamlit run app.py

(Or skip the env var and paste the key into the sidebar box.)
"""

import os
import streamlit as st
from groq import Groq

# Model names change over time; override with: $env:GROQ_MODEL="<name>"
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
SYSTEM_PROMPT = "You are a helpful, concise assistant."

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot (Groq)")

# --- API key: env var first, sidebar input as fallback ---
api_key = os.getenv("GROQ_API_KEY")
with st.sidebar:
    st.header("Settings")
    if not api_key:
        api_key = st.text_input("Groq API key", type="password")
    st.caption(f"Model: {MODEL}")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

if not api_key:
    st.info("Enter your Groq API key in the sidebar (or set GROQ_API_KEY) to start.")
    st.stop()

client = Groq(api_key=api_key)

# --- Chat history lives in session_state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Handle new input ---
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                )
            reply = response.choices[0].message.content or "(empty response)"
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"API error: {e}")
            st.session_state.messages.pop()  # drop the failed user turn