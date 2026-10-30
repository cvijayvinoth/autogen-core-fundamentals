"""Day 1 Assignment: AssistantAgent HR Assistant writing a 5-line JD."""

import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()


async def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file.")

    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=api_key,
    )

    try:
        # Create AssistantAgent with system_message per problem statement
        hr_agent = AssistantAgent(
            name="hr_assistant",
            model_client=model_client,
            system_message="You are an HR assistant.",
        )

        # Unambiguous prompt requesting exactly 5 bulleted lines
        task = (
            "Write a job description for a Junior Python Developer. "
            "It must consist of exactly 5 bulleted lines, one sentence per bullet, "
            "with no introductory or concluding text."
        )

        await Console(hr_agent.run_stream(task=task))

    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())
