# Generic Agents

A collection of AI agent implementations demonstrating various patterns and integrations with different LLM SDKs and frameworks.

## Overview

This repository contains multiple agent implementations showcasing:
- **Multi-SDK Support**: Integration with OpenAI, Google Gemini, LiteLLM, LangChain, and LlamaIndex
- **Agent Patterns**: Action planning, routing, evaluation, memory, RAG, and parallel execution
- **Custom Endpoints**: Support for OpenAI-compatible APIs (e.g., Nebius Token Factory)

## Features

### LLM SDK Integrations

- **OpenAI**: Direct OpenAI API integration (`action_planning_openai.py`)
- **Google Gemini**: Gemini API integration (`action_planning_agent_gemini.py`)
- **LiteLLM**: Unified LLM interface supporting multiple providers (`action_planning_litellm.py`)
- **LangChain**: LangChain framework integration (`action_planning_langchain.py`)
- **LlamaIndex**: LlamaIndex framework integration (`action_planning_llamaindex.py`)

### Agent Types

1. **Action Planning Agent**: Extracts actionable steps from user prompts based on provided knowledge
2. **Augmented Prompt Agent**: Uses persona-based system prompts for specialized responses
3. **Evaluation Agent**: Iteratively evaluates and refines agent responses
4. **Routing Agent**: Routes user queries to specialized agents using embedding similarity
5. **Memory Agent**: Maintains conversation context across multiple turns and sessions
6. **RAG Agent**: Retrieval-Augmented Generation with knowledge base integration
7. **Orchestrator Agent**: Coordinates multiple specialized worker agents
8. **Parallel Execution Agents**: Runs multiple agents concurrently for contract analysis

## Setup

### Prerequisites

- Python 3.8+
- API keys for your chosen LLM provider(s)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/anjanas/generic-agents.git
cd generic-agents
```

2. Install dependencies:
```bash
pip install openai google-generativeai litellm langchain langchain-openai llama-index python-dotenv pydantic numpy pandas
```

3. Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
# Add other API keys as needed
```

## Usage

### Action Planning Agent Examples

Each SDK implementation follows a similar pattern:

```python
from action_planning_openai import ActionPlanningAgent
from dotenv import load_dotenv
import os

load_dotenv()

knowledge = """
# Your knowledge base here
"""

agent = ActionPlanningAgent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    knowledge=knowledge
)

steps = agent.extract_steps_from_prompt("How do I make scrambled eggs?")
print(steps)
```

### Using Custom Endpoints

For OpenAI-compatible endpoints (e.g., Nebius Token Factory):

```python
agent = ActionPlanningAgent(
    openai_api_key=os.getenv("API_KEY"),
    knowledge=knowledge,
    model_name="gpt-5-nano",
    api_base="https://api.tokenfactory.nebius.com/v1/"
)
```

## Project Structure

```
generic-agents/
├── action_planning_openai.py      # OpenAI SDK implementation
├── action_planning_agent_gemini.py # Google Gemini SDK implementation
├── action_planning_litellm.py     # LiteLLM implementation
├── action_planning_langchain.py   # LangChain implementation
├── action_planning_llamaindex.py  # LlamaIndex implementation
├── agent_with_memory.py           # Memory-enabled agent
├── augmented_prompt_agent.py      # Persona-based agent
├── evaluation_agent.py            # Evaluation and refinement agent
├── routing_agent.py               # Agent routing system
├── rag_knowledge_prompt_agent.py  # RAG implementation
├── orchestrator-agent.py          # Multi-agent orchestration
├── parallelExecutionAgents.py     # Parallel agent execution
├── evaluatorOptimizer.py          # Recipe optimization example
├── lib/                            # Shared utilities
│   ├── llm.py
│   ├── memory.py
│   ├── messages.py
│   ├── state_machine.py
│   └── tooling.py
└── README.md
```

## Key Concepts

### Knowledge-Augmented Prompts
Agents use structured knowledge bases to provide accurate, domain-specific responses.

### Multi-Agent Systems
- **Orchestration**: Central coordinator managing specialized workers
- **Routing**: Intelligent routing based on query similarity
- **Parallel Execution**: Concurrent agent execution for efficiency

### Memory Management
Agents maintain conversation context using state machines and short-term memory systems.

### RAG (Retrieval-Augmented Generation)
Combines external knowledge retrieval with LLM generation for enhanced accuracy.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

This repository demonstrates various agent patterns and LLM SDK integrations for educational purposes.

