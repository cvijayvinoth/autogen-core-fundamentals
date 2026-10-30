"""Comparing the effect of system messages: HR Assistant vs Technical Recruiter vs Legal."""

import asyncio
import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()


async def run_persona(persona_name: str, system_message: str, client: OpenAIChatCompletionClient) -> None:
    print(f"\n{'='*20} Testing Persona: {persona_name} {'='*20}")
    agent = AssistantAgent(
        name=persona_name,
        model_client=client,
        system_message=system_message,
    )
    task = "Write a 5-bullet job description for a Junior Python Developer."
    await Console(agent.run_stream(task=task))


async def main() -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file.")

    client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key=api_key)

    personas = [
        ("HR_Assistant", "You are an HR assistant focusing on company culture, collaboration, and foundational responsibilities."),
        ("Tech_Recruiter", "You are an aggressive technical recruiter focusing on marketable skills, tool stacks, and rapid placement."),
        ("Legal_Compliance", "You are a corporate employment lawyer emphasizing compliance, liability, intellectual property, and labor boundaries."),
    ]

    try:
        for name, prompt in personas:
            await run_persona(name, prompt, client)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
