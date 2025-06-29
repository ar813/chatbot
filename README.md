# 🧠 Python Teacher Chatbot

A friendly and beginner-focused AI chatbot built using **Chainlit**, **Agent SDK**, and **Gemini API**, designed to help users learn Python programming in the simplest and most supportive way.

---

## 📌 Features

* Conversational Python tutor powered by AI
* Friendly, simple, and supportive tone for beginners
* Teaches Python topics with code examples and explanations
* Built using Chainlit for interactive chat UI
* Uses Gemini 2.0 Flash model through OpenAI-compatible API

---

## 🚀 How It Works

1. User starts a conversation in the Chainlit chat UI.
2. The chatbot listens, analyzes, and responds using the Agent SDK and Gemini model.
3. Each response is beginner-friendly and includes examples, explanations, and gentle guidance.

---

## 🛠️ Technologies Used

* **Python** 🐍
* **Chainlit** – for chat UI and message handling
* **Gemini API** – through OpenAI-compatible endpoint
* **Agent SDK** – for defining agent, model, and runner
* **dotenv** – to load API keys securely from `.env`

---

## 🧑‍🏫 Agent Behavior

The chatbot acts as a Python teacher that:

* Explains everything in simple English
* Uses short and easy code examples
* Covers beginner topics (syntax, loops, functions, OOP, etc.)
* Encourages and motivates learners
* Never responds to non-Python questions

---

## 📦 Setup & Installation

Follow these steps to set up the project:

```bash
# Initialize a new uv project
uv init

# Create and activate a virtual environment
uv venv
.venv\Scripts\activate    # On Windows

# Install required packages
uv add chainlit
uv add openai_agents python-dotenv
```

Then run the chatbot:

```bash
uv run chainlit run main.py
```

Make sure your `.env` file contains:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```
