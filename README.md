# Built and Deployed by Hassan Hussain
 AI Assistant — Streamlit AI Chatbot

A modern AI chatbot with text and voice conversation built using Python, Streamlit, Groq, and Whisper.

The application provides a simple ChatGPT-style interface where users can have multiple conversations, send text messages, record voice messages, and optionally listen to AI responses using the browser's built-in text-to-speech functionality.

# Features

# AI text chat

Send messages through a ChatGPT-style interface.

Receive responses powered by a Groq-hosted language model.

# Voice input

Record voice directly inside the Streamlit application.

Audio is transcribed using Groq's Whisper model.

Transcribed speech is automatically processed as a user message.

# Voice output

AI responses can be spoken aloud using the browser's built-in SpeechSynthesis API.

No additional text-to-speech package is required.

# Multiple conversations

Create separate chats.

Switch between previous conversations.

Automatically generate chat titles from the first message.

Delete individual conversations.

# Conversation context

Recent messages are sent to the AI model to maintain conversational context.

The application keeps up to 30 recent messages when generating a response.

# Secure API-key configuration

Supports environment variables.

Supports Streamlit secrets.

API keys are never requested directly inside the application.

# Input validation

Prevents empty messages.

Limits messages to 4,000 characters.

# Responsive Streamlit interface

Sidebar for chat history and settings.

Text and voice input.

Online/offline API status indicator.

 Demo

The application provides an interface similar to:

┌─────────────────────────────────────────────────────────────┐
│  AI Assistant                                             │
│ Text and voice conversation powered by Groq                │
│                                                             │
│ ● API Connected                                             │
│                                                             │
│ User: Explain machine learning                             │
│                                                             │
│ AI: Machine learning is a branch of AI that...             │
│                                                             │
│                                                             │
│ Type your message...                         🎙️             │
└─────────────────────────────────────────────────────────────┘

# Sidebar:
├── + New Chat
├── History
│   ├── Explain machine learning
│   ├── Python project
│   └── Voice conversation
├──  Enable voice output
└── Developed by Hassan Hussain

# Technologies Used
Technology	Purpose
Python	Application programming language
Streamlit	Web application and UI
Groq API	AI model inference
GPT-OSS 120B	Default conversational AI model
Whisper Large V3 Turbo	Speech-to-text transcription
JavaScript SpeechSynthesis	Browser-based text-to-speech
Hashlib	Chat/audio identifiers and hashing
OS Environment Variables	API configuration
# Project Structure

A simple project structure can be used:

ai-chatbot/
│
├── app.py
├── requirements.txt
├── README.md
│
└── .streamlit/
    └── secrets.toml


Where:

app.py — Main Streamlit application.

requirements.txt — Python dependencies.

README.md — Project documentation.

.streamlit/secrets.toml — Optional location for the Groq API key.

 Getting Started
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY


Replace YOUR_USERNAME and YOUR_REPOSITORY with your GitHub username and repository name.

2. Create a virtual environment
Windows
python -m venv venv
venv\Scripts\activate

macOS / Linux
python3 -m venv venv
source venv/bin/activate

3. Install dependencies

Create a requirements.txt file containing:

streamlit
groq


Then install the dependencies:

pip install -r requirements.txt

4. Configure your Groq API key

The application supports two configuration methods.

Option A — Environment variable

Windows PowerShell:

$env:GROQ_API_KEY="your_api_key_here"


macOS / Linux:

export GROQ_API_KEY="your_api_key_here"

Option B — Streamlit secrets

Create:

.streamlit/secrets.toml


Add:

GROQ_API_KEY = "your_api_key_here"


Do not commit your API key to GitHub.

Add the following to .gitignore:

.streamlit/secrets.toml
venv/
__pycache__/
*.pyc
.env

▶️ Running the Application

Start the Streamlit application with:

streamlit run app.py


Streamlit will provide a local URL, usually:

http://localhost:8501


Open the URL in your browser and start chatting.

⚙️ Configuration

The application uses the following configuration values:

CHAT_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)

WHISPER_MODEL = "whisper-large-v3-turbo"

MAX_MESSAGE_LENGTH = 4000

MAX_HISTORY_MESSAGES = 30

Change the AI model

You can override the default model using the GROQ_MODEL environment variable:

export GROQ_MODEL="your-model-name"


On Windows PowerShell:

$env:GROQ_MODEL="your-model-name"

🎙️ Voice Chat

The application supports voice messages through Streamlit's audio input component.

The process works as follows:

User records audio
        ↓
Streamlit captures audio
        ↓
Audio is sent to Groq
        ↓
Whisper transcribes the audio
        ↓
Transcribed text becomes a user message
        ↓
AI generates a response
        ↓
Browser optionally speaks the response


The transcription model configured by default is:

WHISPER_MODEL = "whisper-large-v3-turbo"

🔊 Voice Output

Voice output uses the browser's native:

SpeechSynthesis API


This means the application does not require an additional TTS service.

Users can enable or disable voice output from the sidebar:

🔊 Enable voice output


The browser must support the Web Speech API for voice output to work.

🧠 Conversation Memory

Chat messages are stored in Streamlit's session state.

Each conversation follows this structure:

{
    "title": "Chat title",
    "messages": [
        {
            "role": "user",
            "content": "Hello"
        },
        {
            "role": "assistant",
            "content": "Hi! How can I help?"
        }
    ]
}


When generating a response, the application sends the system prompt along with the most recent conversation messages.

recent_messages = current_chat["messages"][-30:]


This helps maintain conversational context while preventing the request from growing indefinitely.

# Chat Management

The application supports:

New Chat

Creates a new conversation with a unique chat ID.

Chat History

Previous conversations appear in the sidebar.

Automatic Titles

The first user message is used to generate a short conversation title.

For example:

User:
How do I learn Python?

Chat title:
How do I learn Python?

Delete Chat

Individual conversations can be removed from the sidebar.

# Security

The application is designed so that the Groq API key is loaded from configuration rather than entered by users.

Supported sources:

GROQ_API_KEY environment variable
        OR
.streamlit/secrets.toml


Never place a real API key directly inside your Python source code.

❌ Avoid
API_KEY = "gsk_XXXXXXXXXXXXXXXX"

✅ Use
API_KEY = os.getenv("GROQ_API_KEY")


or Streamlit secrets.

Also make sure sensitive files are included in .gitignore.

⚠️ Important Notes
Session-based storage

Chat history is currently stored in:

st.session_state


This means conversations are temporary and tied to the current Streamlit session.

If persistent chat history is required, the application could be extended with a database such as:

SQLite

PostgreSQL

MongoDB

Supabase

Browser voice support

Voice output depends on browser support for the Web Speech API.

The exact voice used can vary depending on the operating system and browser.

API usage

AI responses and voice transcription require access to the configured Groq API.

API availability, model availability, rate limits, and pricing can change over time.

🐛 Troubleshooting
Groq API key not found

Make sure GROQ_API_KEY is configured.

For Streamlit secrets:

GROQ_API_KEY = "your_api_key_here"


Then restart the Streamlit application.

Voice transcription fails

Check that:

Your browser allows microphone access.

An audio recording was successfully created.

Your Groq API key is valid.

The configured Whisper model is available to your account.

Your internet connection is working.

AI response fails

Check:

1. GROQ_API_KEY
2. GROQ_MODEL
3. Internet connection
4. Groq API availability
5. Model availability


The application displays the API error returned by the client to help with debugging.

🚀 Future Improvements

Possible improvements include:

💾 Persistent database-backed chat history

👤 User authentication

🌙 Dark/light theme controls

📤 Export conversations

📥 Import conversations

📝 Markdown file uploads

📄 PDF/document chat

🔎 Web search integration

🧠 Long-term memory

🎨 Custom model selection

🌍 Multi-language voice interaction

🗣️ Custom voice selection

⚡ Streaming AI responses

📊 Usage and token statistics

🔒 Improved authentication and access control

☁️ Cloud deployment

☁️ Deployment

The application can be deployed to a platform that supports Streamlit applications.

Before deployment, configure the API key using the platform's secret/environment-variable system rather than putting it into the source code.

For example:

GROQ_API_KEY = your_api_key


After deployment, verify that:

The application can access the Groq API.

The microphone works in the deployed browser environment.

Voice output works in the user's browser.

API secrets are not exposed to the frontend.

📄 License

You can add a license appropriate for your project.

For example, if you choose the MIT License, add a LICENSE file containing the MIT License terms.

👨‍💻 Author

Hassan Hussain

Built with:

Python
Streamlit
Groq
Whisper
JavaScript

⭐ Contributing

Contributions, suggestions, and improvements are welcome.

To contribute:

git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

git checkout -b feature/my-feature

# Make your changes

git add .
git commit -m "Add new feature"
git push origin feature/my-feature


Then open a pull request on GitHub.

📌 Summary

This project is a lightweight AI assistant that combines:

                 ┌──────────────────┐
                 │   Streamlit UI   │
                 └────────┬─────────┘
                          │
             ┌────────────┴────────────┐
             │                         │
        Text Input                Voice Input
             │                         │
             │                    Whisper STT
             │                         │
             └────────────┬────────────┘
                          │
                    Groq AI Model
                          │
                    AI Response
                          │
             ┌────────────┴────────────┐
             │                         │
          Text UI              Browser TTS
             │                         │
             └────────────┬────────────┘
                          │
                    User Experience


It provides a straightforward foundation for building a more advanced AI assistant with persistent memory, authentication, document processing, web search, and other capabilities.
