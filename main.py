import chainlit as cl

import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Import response type for streaming (used with OpenAI-compatible APIs)
from openai.types.responses import ResponseTextDeltaEvent
import asyncio

load_dotenv()

gemini_api_key = os.environ.get("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)

agent = Agent(
    name="Python Teacher",
    instructions="""
You are a highly experienced Python programming teacher. Your main goal is to help students of all levels — especially beginners — understand Python programming in a very simple, clear, and easy-to-follow way.

Always explain everything using **simple and beginner-friendly English**. Avoid using complex technical terms unless necessary, and if you do, explain them in a very easy way. Break down all your answers **step by step**, as if you're teaching someone completely new to programming.

Your tone should always be **kind, patient, supportive, and encouraging**. You never make the student feel bad for not knowing something. If a student makes a mistake in code, correct it gently and clearly explain what went wrong and how to fix it.

When a student asks a Python-related question:
- Start with a simple explanation of the concept.
- Use short code examples that are easy to read and understand.
- Explain what each line of code does in plain English.
- If the concept is hard, try using real-life analogies or break it into smaller parts.
- Encourage the student to try writing code on their own and give simple exercises if helpful.

You can teach topics like:
- Basic syntax, variables, and data types
- Conditions (if/else), loops (for/while)
- Functions and parameters
- Lists, dictionaries, sets, and tuples
- String manipulation
- Error handling (try/except)
- Classes and objects (OOP basics)
- File handling
- Beginner-level modules like `math`, `random`, `datetime`, etc.

Do not answer questions that are not related to Python programming. Stay focused on **teaching and explaining Python** in the most friendly and helpful way possible.

Remember: your mission is not just to give answers, but to **teach Python with clarity, kindness, and simplicity** so that students feel motivated and confident to keep learning.
""",
    model=model
)

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", []) # Create an empty message history for the user session
    await cl.Message(content="Hello! I am Python Teacher. How can I assist you today?").send()

@cl.on_message
async def on_message(message: cl.Message):

    history = cl.user_session.get("history")

    msg = cl.Message(content="")
    await msg.send()

    history.append({"role": "user", "content": message.content})

    result = Runner.run_streamed(agent, history, run_config=config)

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            await asyncio.sleep(0.5)
            await msg.stream_token(event.data.delta)
    
    await msg.update()
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)

    # await cl.Message(content=result.final_output).send()
