#!/usr/bin/env python3
"""
Basic Strands AI Agent Example (v1)

This example demonstrates the fundamentals of building an AI agent using the Strands SDK
with Docker Model Runner for local model execution. This is the simplest possible agent
implementation that showcases core concepts without external dependencies.

Key Learning Objectives:
- Understanding Strands Agent architecture (model + tools + prompt)
- Using Docker Model Runner for local AI model execution
- Using tools for agent functionality
- Basic Docker containerization for AI agents
"""

#!/usr/bin/env python3

import os
from strands import Agent, tool
from strands.models.openai import OpenAIModel
from strands_tools import current_time

# Configuration from environment variables
MODEL_RUNNER_URL = os.getenv("MODEL_RUNNER_URL", "http://model-runner.docker.internal/engines/llama.cpp/v1")
MODEL_RUNNER_MODEL = os.getenv("MODEL_RUNNER_MODEL", "ai/gemma3:1B-Q4_K_M")
QUESTION = "what time it is in Sydney?"

def main():
    model = OpenAIModel(
        client_args={
            "api_key": "sk-insecure",
            "base_url": MODEL_RUNNER_URL
        },
        model_id=MODEL_RUNNER_MODEL,
        params={
            "temperature": 0.1,
            "max_tokens": 500
        }
    )
    
    agent = Agent(
        model=model,
        tools=[current_time],
        system_prompt="Call current_time(timezone='Australia/Sydney') once, then answer with the time. Do not call tools repeatedly."
    )
    
    print(f"🤖 Agent Question: {QUESTION}")
    print("🔄 Processing...")
    
    try:
        response = agent(QUESTION)
        print(f"✅ Agent Answer: {response}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
