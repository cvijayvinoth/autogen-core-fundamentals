# Microsoft AutoGen (v0.4+) — Fundamentals & Agent Orchestration

A structured reference repository tracking core architectural concepts, implementations, and hands-on labs for Microsoft AutoGen v0.4+. This repository covers foundational agent construction, asynchronous event streaming, runtime message architectures, and tool integration.

---

## Architecture Overview

```
                                      +-------------------------------+
                                      |   OpenAIChatCompletionClient   |
                                      +---------------+---------------+
                                                      |
                                                      v
+------------------+                    +-------------+---------------+
|   User Prompt    | -----------------> |       AssistantAgent        |
+------------------+                    | (System Prompt, State, Tools)
                                        +-------------+---------------+
                                                      |
                                                      v
                                        +-------------+---------------+
                                        |      Console UI Stream      |
                                        +-----------------------------+
```

AutoGen v0.4+ transitions from legacy sequential loops to an asynchronous, message-driven runtime (`autogen-core` and `autogen-agentchat`). Core components include:

- **Asynchronous Execution (`asyncio`)**: Agent operations, stream handling, and tool execution operate natively inside asynchronous event loops.
- **Stateless Model Clients**: Model clients (`OpenAIChatCompletionClient`) maintain isolated connection pooling and must be explicitly opened and closed during application teardown.
- **Typed Message Passing**: Communication across agents, tools, and UI streams relies on strongly-typed message schemas (`TextMessage`, `ToolCallRequestMessage`, `ToolCallResultMessage`).

---

## Repository Structure

```
.
├── 01_intro_and_model_clients/
│   └── client_setup.py          # Direct model client initialization and teardown
├── 02_first_agent_hr/
│   ├── hr_agent.py              # Single AssistantAgent implementation (Day 1 Lab)
│   └── test_system_prompts.py   # Comparing HR vs Recruiter vs Legal system messages
├── 03_messages_and_streams/
│   └── inspect_messages.py      # Deconstructing runtime stream frames and message types
├── 04_tools_and_functions/
│   ├── basic_tools.py           # Registering standard Python functions as agent tools
│   └── custom_tools.py          # Type-annotated custom tools with docstring schemas
├── env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Environment Setup

### 1. Prerequisites

- Python 3.10 – 3.12 (Python 3.13 requires compatible wheels for binary dependencies)
- OpenAI API key with access to standard completion endpoints

### 2. Virtual Environment Configuration

#### On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

*(If script execution is disabled on Windows, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

### 3. Dependency Installation

Install the required packages:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Secret Configuration

Copy the example environment template and add your credentials:

```bash
cp env.example .env
```

Set your key inside `.env`:
```env
OPENAI_API_KEY=your_actual_api_key_here
```

---

## Module Summaries & Concepts

### 1. Configuring the LLM (`OpenAIChatCompletionClient`)
Unlike legacy architectures where configurations were passed as raw dictionaries (`llm_config`), v0.4 uses dedicated client instances.

```python
from autogen_ext.models.openai import OpenAIChatCompletionClient

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=api_key,
)
```

### 2. Building an Agent (`AssistantAgent`)
Agents are instantiated with a name, a model client, and a system message that frames the persona and boundary conditions.

```python
from autogen_agentchat.agents import AssistantAgent

hr_agent = AssistantAgent(
    name="hr_assistant",
    model_client=model_client,
    system_message="You are an HR assistant.",
)
```

### 3. Prompt Engineering & Deterministic Output
Large Language Models interpret ambiguous constraints unpredictably (e.g., "write 5 lines" can result in 5 paragraphs, 5 sentences, or 5 markdown sections). Concrete operational instructions ensure structural compliance:

```python
task = (
    "Write a job description for a Junior Python Developer. "
    "Output must consist of exactly 5 bullet points, one sentence per bullet. "
    "Do not include intro, titles, or concluding remarks."
)
```

### 4. Message Streaming & Observation
AutoGen v0.4 outputs tokens and states via streaming generators. `Console` provides real-time streaming directly to `stdout`.

```python
from autogen_agentchat.ui import Console

await Console(hr_agent.run_stream(task=task))
```

### 5. Custom Tools with Python
Tools are defined as standard, type-annotated Python functions. AutoGen reads type signatures and docstrings to generate JSON schema definitions for the model's function-calling engine.

```python
async def fetch_salary_band(role: str, level: str) -> str:
    """Fetch base compensation range for a specific title and seniority level.

    Args:
        role: Job title (e.g., 'Python Developer').
        level: Seniority (e.g., 'Junior', 'Mid', 'Senior').
    """
    bands = {
        ("python developer", "junior"): "INR 6,00,000 - 9,00,000",
        ("python developer", "senior"): "INR 18,00,000 - 28,00,000",
    }
    return bands.get((role.lower(), level.lower()), "Role not mapped.")
```

---

## Lab Execution: Day 1 HR Assistant

Run the Day 1 baseline task:

```bash
python 02_first_agent_hr/hr_agent.py
```

### Expected Behavior
1. The script loads environment configurations from `.env`.
2. Asynchronous client session initializes.
3. The `AssistantAgent` streams a strictly formatted, 5-bullet job description directly to the terminal without hanging on script exit.

---

## Best Practices & Troubleshooting

| Issue | Root Cause | Resolution |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'autogen_agentchat'` | Terminal executed system/Windows Store Python instead of environment binary. | Run via `python -m pip install ...` inside activated venv, or use `python` instead of `python3` on Windows. |
| Process hangs indefinitely after completing | Client connection pool left open. | Wrap execution logic in `try ... finally` and ensure `await model_client.close()` is executed. |
| Agent ignores output constraints | Imprecise natural language prompt. | Explicitly define the format (e.g., *"exactly 5 markdown list items, single line each"*). |
| `ValueError: OPENAI_API_KEY not found` | `.env` file absent from runtime working directory or environment variable missing. | Verify `.env` location matches the directory where `load_dotenv()` runs, or set directly via terminal session. |
