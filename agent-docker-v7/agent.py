#!/usr/bin/env python3
import os
from pathlib import Path
from mcp.client.sse import sse_client
from strands import Agent, tool
from strands.tools.mcp import MCPClient
from strands.models.openai import OpenAIModel

# Configuration
MODEL_RUNNER_URL = os.getenv("MODEL_RUNNER_URL", "http://model-runner.docker.internal/engines/llama.cpp/v1")
MODEL_RUNNER_MODEL = os.getenv("MODEL_RUNNER_MODEL", "ai/qwen3")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://mcp-gateway:8811/sse")
QUESTION = os.getenv("QUESTION", "Define Zorgon")

@tool
def save_definition(word: str, definition: str) -> str:
    """Save a word's definition to a text file."""
    out_dir = Path("/app/definitions")
    out_dir.mkdir(exist_ok=True)
    
    file_path = out_dir / f"{word}.txt"
    with open(file_path, "w") as f:
        f.write(definition.strip() + "\n")
    
    # Change the return value to be the desired final response
    return f"The definition for '{word}' has been found and saved. Mission Completed! Stop"

def get_model():
    """Auto-detect model based on environment."""
    if OPENAI_API_KEY and OPENAI_API_KEY != "sk-insecure":
        return OpenAIModel(
            client_args={"api_key": OPENAI_API_KEY},
            model_id=OPENAI_MODEL_NAME
        )
    else:
        return OpenAIModel(
            client_args={
                "api_key": "sk-insecure",
                "base_url": MODEL_RUNNER_URL
            },
            model_id=MODEL_RUNNER_MODEL,
            params={
                "temperature": 0.0,
                "max_tokens": 512
            }
        )

def main():
    model = get_model()
    mcp_client = MCPClient(lambda: sse_client(MCP_SERVER_URL))
    
    with mcp_client:
        mcp_tools = mcp_client.list_tools_sync()
        agent = Agent(
            model=model,
            tools=mcp_tools + [save_definition],
            system_prompt=f"""You are a helpful assistant. Your task is to define a term by searching for it, saving the definition, and then confirming completion.

## Example:

Question: "What is photosynthesis?"

Thought: The user is asking for the definition of "photosynthesis". I will use the search tool one time to find it.
Tool Call: `search(query="photosynthesis")`
Thought: I have the definition from the search result. I will now save it using the save_definition tool.
Tool Call: `save_definition("Photosynthesis", "The process by which green plants use sunlight to synthesize foods from carbon dioxide and water.")`
Thought: The definition has been saved successfully. I will now inform the user that the task is complete.
STOP! EXIT!
---

## Your Turn:

Question: {QUESTION}"""
        )
        
        print(f"Processing: {QUESTION}")
        response = agent(QUESTION)
        print(f"Response: {response}")

if __name__ == "__main__":
    main()
