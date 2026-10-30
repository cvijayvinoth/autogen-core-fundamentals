"""Demonstrates tool registration with AssistantAgent using Python type annotations."""

import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()


def calculate_experience_score(years_experience: float, target_level: str) -> str:
    """Calculate candidate fit score based on years of experience and role level.

    Args:
        years_experience: Number of years working with relevant tech.
        target_level: Target position level ('junior', 'mid', 'senior').
    """
    thresholds = {"junior": 1.0, "mid": 3.0, "senior": 5.0}
    required = thresholds.get(target_level.lower(), 2.0)
    if years_experience >= required:
        return f"Qualified: Candidate has {years_experience}y (Required: {required}y)."
    return f"Below Minimum: Candidate has {years_experience}y (Required: {required}y)."


async def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found.")

    client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key=api_key)

    agent = AssistantAgent(
        name="screening_agent",
        model_client=client,
        tools=[calculate_experience_score],
        system_message="You are a technical screening agent. Use your tool to evaluate candidate qualifications.",
    )

    try:
        task = "Evaluate a candidate with 1.5 years of experience applying for a junior Python role."
        await Console(agent.run_stream(task=task))
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
