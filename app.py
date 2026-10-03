import os
import json
import hashlib
import html

import streamlit as st
from groq import Groq


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CONFIGURATION
# ============================================================

CHAT_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)

WHISPER_MODEL = "whisper-large-v3-turbo"

MAX_MESSAGE_LENGTH = 4000
MAX_HISTORY_MESSAGES = 30


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are a helpful, intelligent, friendly AI assistant.

PERSONALITY:
- Be friendly and professional.
- Give clear and practical answers.
- Keep answers concise when the question is simple.
- Give detailed step-by-step explanations when the user needs them.
- Do not unnecessarily repeat information.
- Use Markdown formatting when useful.

ACCURACY:
- Never intentionally invent facts.
- If you are unsure about something, clearly say so.
- Distinguish facts from assumptions.
- For programming questions, provide working and easy-to-follow code.

CONVERSATION:
- Use previous messages in the current conversation as context.
- Remember relevant information from earlier messages in the same chat.
- Do not forget the current topic unless the user starts a new conversation.

PROGRAMMING:
- Prefer complete, copy-paste-ready solutions.
- Explain important changes simply.
- When fixing code, preserve working features unless there is a good reason to change them.

STYLE:
- Answer directly.
- Avoid unnecessary disclaimers.
- Use headings, bullets, tables, and code blocks when they improve readability.
"""


# ============================================================
# API KEY
# ============================================================

def get_api_key():
    """
    Get Groq API key from:
    1. Environment variable
    2. Streamlit secrets
    """

    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        return api_key

    try:
        api_key = st.secrets.get("GROQ_API_KEY")
        if api_key:
            return api_key
    except Exception:
        pass

    return None


API_KEY = get_api_key()


# ============================================================
# GROQ CLIENT
# ============================================================

if API_KEY:
    client = Groq(api_key=API_KEY)
else:
    client = None


# ============================================================
# SESSION STATE
# ============================================================

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None

if "voice_output" not in st.session_state:
    st.session_state.voice_output = True


# ============================================================
# CHAT MANAGEMENT
# ============================================================

def create_new_chat():
    """Create a new empty conversation."""

    chat_id = hashlib.sha256(
        os.urandom(32)
    ).hexdigest()[:12]

    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": []
    }

    st.session_state.current_chat_id = chat_id


def get_current_chat():
    """Return current chat."""

    chat_id = st.session_state.current_chat_id

    if chat_id is None:
        create_new_chat()
        chat_id = st.session_state.current_chat_id

    return st.session_state.chats[chat_id]


def generate_chat_title(text):
    """Generate a simple title from first user message."""

    text = text.strip()

    if not text:
        return "New Chat"

    # Remove new lines
    text = text.replace("\n", " ")

    # Keep title short
    if len(text) > 35:
        text = text[:35].rstrip() + "..."

    return text


def delete_current_chat():
    """Delete current conversation."""

    chat_id = st.session_state.current_chat_id

    if chat_id in st.session_state.chats:
        del st.session_state.chats[chat_id]

    st.session_state.current_chat_id = None

    # Create a fresh chat
    create_new_chat()


# Create first chat
if not st.session_state.chats:
    create_new_chat()

if st.session_state.current_chat_id not in st.session_state.chats:
    create_new_chat()


current_chat = get_current_chat()


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */
    .main {
        padding-top: 1rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.2);
    }

    /* Chat history buttons */
    section[data-testid="stSidebar"] button {
        border-radius: 8px;
    }

    /* Header */
    .app-header {
        padding: 10px 0 20px 0;
    }

    .app-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .app-subtitle {
        color: #888;
        font-size: 0.95rem;
    }

    /* Status */
    .status-online {
        color: #22c55e;
        font-weight: 600;
    }

    .status-offline {
        color: #ef4444;
        font-weight: 600;
    }

    /* Voice section */
    .voice-label {
        text-align: center;
        font-size: 0.75rem;
        color: #888;
        margin-top: 5px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #777;
        font-size: 0.75rem;
        padding-top: 25px;
        padding-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("Chats")

    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "New Chat",
        use_container_width=True,
        type="primary"
    ):
        create_new_chat()
        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------------

    st.markdown("###  History")

    chat_items = list(st.session_state.chats.items())

    if not chat_items:

        st.caption("No conversations yet.")

    else:

        # Newest/current chats first
        chat_items.reverse()

        for chat_id, chat in chat_items:

            title = chat["title"]

            if len(title) > 32:
                title = title[:32] + "..."

            is_current = (
                chat_id == st.session_state.current_chat_id
            )

            button_text = (
                f" {title}"
                if is_current
                else f" {title}"
            )

            if st.button(
                button_text,
                key=f"chat_{chat_id}",
                use_container_width=True
            ):

                st.session_state.current_chat_id = chat_id
                st.session_state.last_audio_hash = None
                st.rerun()

    st.divider()

    # --------------------------------------------------------
    # CURRENT CHAT ACTIONS
    # --------------------------------------------------------

    st.markdown("###  Current Chat")

    if st.button(
        "🗑️ Delete Current Chat",
        use_container_width=True
    ):

        delete_current_chat()
        st.rerun()

    # --------------------------------------------------------
    # VOICE OUTPUT
    # --------------------------------------------------------

    st.session_state.voice_output = st.checkbox(
        "🔊 Enable voice output",
        value=st.session_state.voice_output
    )

    st.divider()

    st.caption(
        "Chats are stored in the current Streamlit session."
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <div class="app-header">
        <div class="app-title">🤖 AI Assistant</div>
        <div class="app-subtitle">
            Text and voice conversation powered by Groq
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# API STATUS
# ============================================================

if client:

    st.markdown(
        '<span class="status-online">● API Connected</span>',
        unsafe_allow_html=True
    )

else:

    st.error(
        """
        **Groq API key not found.**

        Set `GROQ_API_KEY` in your environment or
        `.streamlit/secrets.toml`.

        The API key is intentionally not requested inside the app.
        """
    )


st.divider()


# ============================================================
# DISPLAY CURRENT CHAT
# ============================================================

for message in current_chat["messages"]:

    role = message["role"]
    content = message["content"]

    with st.chat_message(role):

        st.markdown(content)


# ============================================================
# FUNCTIONS
# ============================================================

def validate_message(message):
    """Validate user input."""

    if not message:
        return False, "Please enter a message."

    message = message.strip()

    if len(message) > MAX_MESSAGE_LENGTH:
        return (
            False,
            f"Message is too long. Maximum is "
            f"{MAX_MESSAGE_LENGTH} characters."
        )

    return True, ""


def transcribe_audio(audio_bytes):
    """
    Send recorded audio to Groq Whisper
    and return the transcription.
    """

    if not client:
        raise RuntimeError(
            "Groq API key is not configured."
        )

    if not audio_bytes:
        raise ValueError(
            "No audio was recorded."
        )

    # Groq accepts webm/wav/etc.
    audio_file = (
        "voice_message.webm",
        audio_bytes
    )

    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model=WHISPER_MODEL,
        response_format="json",
        temperature=0.0,
    )

    text = transcription.text.strip()

    if not text:
        raise ValueError(
            "I couldn't detect any speech in the recording."
        )

    return text


def get_ai_response():

    if not client:
        raise RuntimeError(
            "Groq API key is not configured."
        )

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Keep recent context
    recent_messages = current_chat["messages"][
        -MAX_HISTORY_MESSAGES:
    ]

    messages.extend(recent_messages)

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=2048,
    )

    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError(
            "The AI returned an empty response."
        )

    return answer.strip()


def speak_text(text):
    """
    Browser-based voice output.

    Uses the browser's built-in SpeechSynthesis API,
    so no extra TTS package is required.
    """

    if not text:
        return

    # Safely encode text for JavaScript
    safe_text = json.dumps(text)

    speech_html = f"""
    <script>
        const text = {safe_text};

        if ('speechSynthesis' in window) {{

            window.speechSynthesis.cancel();

            const utterance =
                new SpeechSynthesisUtterance(text);

            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;

            window.speechSynthesis.speak(utterance);
        }}
    </script>
    """

    st.components.v1.html(
        speech_html,
        height=0
    )


# ============================================================
# INPUT AREA
# ============================================================

st.markdown("###")


# Two-column input:
# LEFT  = typing
# RIGHT = microphone

text_column, voice_column = st.columns(
    [0.88, 0.12],
    vertical_alignment="bottom"
)


# ------------------------------------------------------------
# TEXT INPUT
# ------------------------------------------------------------

with text_column:

    text_prompt = st.chat_input(
        "Type your message..."
    )


# ------------------------------------------------------------
# VOICE INPUT
# ------------------------------------------------------------

with voice_column:

    audio_value = st.audio_input(
        "🎙️",
        sample_rate=16000,
        key="voice_recorder",
        label_visibility="collapsed",
    )


# ============================================================
# HANDLE TEXT MESSAGE
# ============================================================

if text_prompt is not None:

    valid, error_message = validate_message(
        text_prompt
    )

    if not valid:

        st.warning(error_message)

    elif not client:

        st.error(
            "Groq API key is not configured."
        )

    else:

        user_message = text_prompt.strip()

        # Add user message
        current_chat["messages"].append(
            {
                "role": "user",
                "content": user_message
            }
        )

        # Set title from first message
        if current_chat["title"] == "New Chat":

            current_chat["title"] = generate_chat_title(
                user_message
            )

        # Display user message
        with st.chat_message("user"):

            st.markdown(user_message)

        # Generate AI response
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    answer = get_ai_response()

                    st.markdown(answer)

                    current_chat["messages"].append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                except Exception as error:

                    error_text = str(error)

                    st.error(
                        f"❌ Failed to get AI response:\n\n"
                        f"{error_text}"
                    )

        # Rerun so sidebar title updates
        st.rerun()


# ============================================================
# HANDLE VOICE MESSAGE
# ============================================================

if audio_value is not None:

    try:

        audio_bytes = audio_value.getvalue()

        # Create unique hash for this recording
        audio_hash = hashlib.sha256(
            audio_bytes
        ).hexdigest()

        # IMPORTANT:
        # Streamlit reruns the script after recording.
        # This prevents the same recording from being
        # transcribed multiple times.
        if (
            audio_hash
            != st.session_state.last_audio_hash
        ):

            st.session_state.last_audio_hash = audio_hash

            if not client:

                st.error(
                    "Groq API key is not configured."
                )

            elif len(audio_bytes) == 0:

                st.warning(
                    "No audio was recorded."
                )

            else:

                # ------------------------------------------------
                # TRANSCRIBE
                # ------------------------------------------------

                with st.spinner(
                    "🎙️ Transcribing your voice..."
                ):

                    try:

                        voice_text = transcribe_audio(
                            audio_bytes
                        )

                    except Exception as error:

                        st.error(
                            "❌ Voice transcription failed.\n\n"
                            f"{str(error)}"
                        )

                        voice_text = None

                # ------------------------------------------------
                # SEND TRANSCRIPTION TO AI
                # ------------------------------------------------

                if voice_text:

                    valid, error_message = (
                        validate_message(voice_text)
                    )

                    if not valid:

                        st.warning(error_message)

                    else:

                        # Show transcribed user message
                        with st.chat_message("user"):

                            st.markdown(
                                f"🎙️ **Voice message**\n\n"
                                f"{voice_text}"
                            )

                        # Save user message
                        current_chat["messages"].append(
                            {
                                "role": "user",
                                "content": voice_text
                            }
                        )

                        # Set chat title
                        if current_chat["title"] == "New Chat":

                            current_chat["title"] = (
                                generate_chat_title(
                                    voice_text
                                )
                            )

                        # ------------------------------------------------
                        # AI RESPONSE
                        # ------------------------------------------------

                        with st.chat_message(
                            "assistant"
                        ):

                            with st.spinner(
                                "🤖 Thinking..."
                            ):

                                try:

                                    answer = (
                                        get_ai_response()
                                    )

                                    st.markdown(
                                        answer
                                    )

                                    # Save response
                                    current_chat[
                                        "messages"
                                    ].append(
                                        {
                                            "role": "assistant",
                                            "content": answer
                                        }
                                    )

                                    # Voice output
                                    if (
                                        st.session_state
                                        .voice_output
                                    ):

                                        speak_text(
                                            answer
                                        )

                                except Exception as error:

                                    st.error(
                                        "❌ AI response failed.\n\n"
                                        f"{str(error)}"
                                    )

                        # Update sidebar
                        st.rerun()

    except Exception as error:

        st.error(
            "❌ Something went wrong while "
            "processing the voice message.\n\n"
            f"{str(error)}"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        AI Assistant • Groq • Whisper Speech-to-Text
    </div>
    """,
    unsafe_allow_html=True,
)