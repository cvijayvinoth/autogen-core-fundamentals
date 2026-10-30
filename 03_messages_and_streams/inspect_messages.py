"""Inspect raw message streams and event types from AutoGen AssistantAgent."""

import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()


async def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found.")

    client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key=api_key)

    agent = AssistantAgent(
        name="echo_assistant",
        model_client=client,
        system_message="You are a concise engineering assistant.",
    )

    try:
        stream = agent.run_stream(task="List 3 key principles of asynchronous Python programming.")
        print("--- Inspecting Stream Frames ---")
        async for item in stream:
            print(f"Type: {type(item).__name__} | Payload: {item}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
