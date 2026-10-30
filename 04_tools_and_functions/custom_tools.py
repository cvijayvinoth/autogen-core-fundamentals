"""Custom typed asynchronous tools integrated with AutoGen AssistantAgent."""

import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()


async def fetch_salary_band(role: str, level: str) -> str:
    """Fetch base compensation range for a specific title and seniority level.

    Args:
        role: Job title (e.g., 'Python Developer').
        level: Seniority (e.g., 'Junior', 'Mid', 'Senior').
    """
    bands = {
        ("python developer", "junior"): "INR 6,00,000 - 9,00,000",
        ("python developer", "mid"): "INR 10,00,000 - 16,00,000",
        ("python developer", "senior"): "INR 18,00,000 - 28,00,000",
    }
    key = (role.lower().strip(), level.lower().strip())
    return bands.get(key, "Compensation band not found for given criteria.")


async def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found.")

    client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key=api_key)

    agent = AssistantAgent(
        name="compensation_agent",
        model_client=client,
        tools=[fetch_salary_band],
        system_message="You assist candidate inquiries on compensation using the fetch_salary_band tool.",
    )

    try:
        task = "What is the expected compensation range for a Junior Python Developer?"
        await Console(agent.run_stream(task=task))
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
