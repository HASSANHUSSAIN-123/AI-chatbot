# Built and Deployed by Hassan Hussain
# AI Chatbot

A simple chatbot with a browser interface, built in Python. You type a message, it goes to an AI model through the Groq API, and the reply appears in the chat window.

## What I built

A working chatbot that does the full loop from start to finish:

1. Accepts a message from the user
2. Sends it to an AI model through an API
3. Receives the response
4. Displays it in a chat interface

It also remembers the conversation while the app is open, so follow-up questions work. There's a "Clear chat" button to reset, a sidebar box for pasting an API key, and readable error messages instead of crashes. Everything lives in one file, `app.py`.

## Technology used

- **Python**: the whole app
- **Streamlit**: the chat interface (`st.chat_input`, `st.chat_message`) and session state for chat history
- **Groq API**: free-tier access to the AI model, with the official `groq` Python SDK
- **Model**: `openai/gpt-oss-120b` by default (configurable)
- **Git and GitHub**: version control and hosting the code

## How to run it

You need Python 3.9+ and a free Groq API key from https://console.groq.com/keys.

```bash
# 1. Clone the repo
git clone https://github.com/HASSANHUSSAIN-123/AI-chatbot.git
cd AI-chatbot

# 2. (Optional) create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1        # Windows PowerShell
# source venv/bin/activate       # Mac/Linux

# 3. Install dependencies
pip install streamlit groq
```

Set your API key. On Windows PowerShell:

```powershell
$env:GROQ_API_KEY="your_key_here"
```

On Mac/Linux: `export GROQ_API_KEY="your_key_here"`. You can also skip this and paste the key into the sidebar once the app is running.

Then start the app:

```bash
streamlit run app.py
```

It opens at http://localhost:8501.

To use a different model, set `GROQ_MODEL` before running, for example `$env:GROQ_MODEL="openai/gpt-oss-20b"`.

## API integration approach

- **Key handling:** the app reads `GROQ_API_KEY` from the environment first and falls back to a password field in the sidebar. The key is never written into the code, and `.env` and `venv/` are in `.gitignore`.
- **Request flow:** each time the user sends a message, the app builds a list that starts with a system prompt followed by the full chat history, then calls `client.chat.completions.create(...)`. Sending the whole history on every request is what lets the model follow the conversation.
- **State:** Streamlit reruns the script on every interaction, so the history is stored in `st.session_state.messages` to survive reruns.
- **Response:** the reply text is read from `response.choices[0].message.content`, shown in the chat and added to the history.
- **Error handling:** the API call is wrapped in `try/except`. If it fails, the app shows the error and removes the failed message from history so the next request stays valid.
- **Configurable model:** the model name comes from an environment variable with a default, because providers retire models over time.

## What I learned

- **API basics:** how to authenticate, structure a chat request (system, user and assistant roles) and read the response.
- **Keys are a real security issue:** keep them out of code and out of Git, and use environment variables and `.gitignore`. A placeholder key like `gsk_your_new_key` gives a 401, so check the actual key value before assuming the code is wrong.
- **Read the status code:** a 401 meant a bad key, and a 404 `model_not_found` meant the model had been retired or wasn't available on my account. Each error pointed to a different fix.
- **Providers change:** model names get deprecated, so the model should be configurable instead of hardcoded.
- **Streamlit reruns the script on every interaction,** so anything that needs to persist has to go in `st.session_state`.
- **Git workflow:** creating a repo, connecting a remote, and resolving a rejected push by merging remote changes before pushing.
- **Debugging by isolating:** testing the API call on its own in the terminal, outside Streamlit, quickly showed whether the problem was the key or the app.

## What I would improve next

- **Stream responses** word by word so replies feel faster
- **Model dropdown** in the sidebar, loaded from Groq's models endpoint so it never goes stale
- **Persistent history** saved to a file or database so chats survive a restart
- **Editable system prompt** to switch the bot between roles like tutor, coding helper or translator
- **Token and history limits** so long chats don't hit context limits or waste tokens
- **Rate limit handling** with a friendly message and automatic retry
- **Deployment** on Streamlit Community Cloud with the key stored in secrets
- **Tests** for the API wrapper and error handling
