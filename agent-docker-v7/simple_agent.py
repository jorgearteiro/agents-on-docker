#!/usr/bin/env python3
import os
from pathlib import Path
from strands import Agent, tool
from strands.models.openai import OpenAIModel

# Simple configuration
MODEL_RUNNER_URL = os.getenv("MODEL_RUNNER_URL", "http://model-runner.docker.internal/engines/llama.cpp/v1")
MODEL_RUNNER_MODEL = os.getenv("MODEL_RUNNER_MODEL", "ai/qwen3")
QUESTION = os.getenv("QUESTION", "What is 25 * 4?")

@tool
def simple_search(query: str) -> str:
    """Search for information about a topic."""
    # Simple mock search - replace with real search if needed
    return f"Here is information about {query}: This is a mock search result for demonstration."

@tool
def save_file(filename: str, content: str) -> str:
    """Save content to a file."""
    out_dir = Path("/app/definitions")
    out_dir.mkdir(exist_ok=True)
    
    file_path = out_dir / filename
    with open(file_path, "w") as f:
        f.write(content)
    
    return f"Saved to {file_path}"

def main():
    # Simple model setup for local use
    model = OpenAIModel(
        client_args={
            "api_key": "sk-insecure",
            "base_url": MODEL_RUNNER_URL
        },
        model_id=MODEL_RUNNER_MODEL,
        params={
            "temperature": 0.1,
            "max_tokens": 200
        }
    )
    
    # Create agent with simple tools - NO MCP
    agent = Agent(
        model=model,
        tools=[simple_search, save_file],
        system_prompt="You are a helpful assistant. Use tools when needed and give short, direct answers."
    )
    
    print(f"Question: {QUESTION}")
    response = agent(QUESTION)
    print(f"Answer: {response}")

if __name__ == "__main__":
    main()
