"""Module 1: Direct OpenAIChatCompletionClient initialization and lifecycle management."""

import asyncio
import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage

load_dotenv()


async def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment or .env file.")

    # Initialize client
    client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=api_key,
    )

    try:
        response = await client.create([UserMessage(content="Hello! Confirm connection.", source="user")])
        print("Model Response:", response.content)
    finally:
        # Crucial: always close client to avoid hanging connections
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
