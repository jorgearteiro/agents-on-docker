#!/usr/bin/env python3
"""
Advanced Strands AI Agent with MCP Gateway Integration (v7)

This example demonstrates advanced AI agent capabilities using the Model Context Protocol (MCP)
Gateway for secure external tool integration. It showcases:

- MCP Gateway integration for secure external API access
- Automatic model detection (local vs cloud)
- Docker secrets management for API keys
- Real external tool usage (search, file operations, etc.)
- Production-ready error handling and logging

Key Learning Objectives:
- Understanding MCP Gateway architecture and security benefits
- Integrating external tools securely through MCP
- Managing secrets in containerized environments
- Building production-ready agents with proper error handling
"""

import os
from pathlib import Path
from mcp.client.sse import sse_client
from strands import Agent, tool
from strands.tools.mcp import MCPClient
from strands.models.openai import OpenAIModel

# Configuration from environment variables
# These are set by Docker Compose and the entrypoint script

# Docker Model Runner configuration for local AI models
MODEL_RUNNER_URL = os.getenv("MODEL_RUNNER_URL", "http://model-runner.docker.internal/engines/llama.cpp/v1")
MODEL_RUNNER_MODEL = os.getenv("MODEL_RUNNER_MODEL", "ai/gemma3:1B-Q4_K_M")

# OpenAI configuration for cloud models
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Set by entrypoint from Docker secrets

# MCP Gateway configuration
# The MCP Gateway provides secure access to external tools and APIs
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://mcp-gateway:8811/sse")

# Default question for the agent to process
QUESTION = os.getenv("QUESTION", "Define Zorgon")

@tool
def save_definition(word: str, definition: str) -> str:
    """
    Save a word's definition to a text file in the agent's workspace.
    
    This tool demonstrates how to create custom tools that work alongside
    MCP-provided external tools. It handles file operations within the
    containerized environment with proper error handling.
    
    Args:
        word (str): The word being defined
        definition (str): The definition text to save
        
    Returns:
        str: Confirmation message indicating successful save
        
    Docker Integration Notes:
    - Files are saved to /app/definitions (mounted as Docker volume)
    - Directory is created automatically if it doesn't exist
    - Files persist between container restarts due to volume mounting
    - Proper error handling for file system operations
    """
    try:
        # Create output directory - this maps to a Docker volume
        out_dir = Path("/app/definitions")
        out_dir.mkdir(exist_ok=True)
        
        # Create filename from word (sanitize for filesystem)
        safe_word = "".join(c for c in word if c.isalnum() or c in (' ', '-', '_')).strip()
        file_path = out_dir / f"{safe_word}.txt"
        
        # Write definition to file with proper formatting
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"Definition of '{word}':\n")
            f.write("=" * (len(word) + 15) + "\n\n")
            f.write(definition.strip() + "\n")
        
        return f"✅ The definition for '{word}' has been found and saved to {file_path.name}. Mission Completed!"
        
    except Exception as e:
        return f"❌ Error saving definition for '{word}': {str(e)}"

def get_model():
    """
    Auto-detect and configure the appropriate AI model based on environment.
    
    This function demonstrates automatic model selection based on available
    credentials and configuration. It supports both local models via Docker
    Model Runner and cloud models via OpenAI API.
    
    Returns:
        OpenAIModel: Configured model instance ready for use
        
    Model Selection Logic:
    1. If OPENAI_API_KEY is available and valid → Use OpenAI cloud models
    2. Otherwise → Use Docker Model Runner with local models
    
    Security Notes:
    - API keys are loaded from Docker secrets (more secure than env vars)
    - Local models use dummy API key for compatibility
    - Model selection is logged for debugging
    """
    
    # Check if we have a valid OpenAI API key (not the dummy key used for local models)
    if OPENAI_API_KEY and OPENAI_API_KEY != "sk-insecure":
        print(f"🌐 Configuring OpenAI model: {OPENAI_MODEL_NAME}")
        return OpenAIModel(
            client_args={
                "api_key": OPENAI_API_KEY  # Real API key from Docker secrets
            },
            model_id=OPENAI_MODEL_NAME,
            params={
                "temperature": 0.1,  # Slightly creative but focused
                "max_tokens": 1000   # Allow longer responses for definitions
            }
        )
    else:
        print(f"🏠 Configuring local model via Docker Model Runner: {MODEL_RUNNER_MODEL}")
        return OpenAIModel(
            client_args={
                "api_key": "sk-insecure",      # Dummy key for local models
                "base_url": MODEL_RUNNER_URL   # Docker Model Runner endpoint
            },
            model_id=MODEL_RUNNER_MODEL,
            params={
                "temperature": 0.1,  # Consistent behavior
                "max_tokens": 1000   # Allow longer responses
            }
        )

def main():
    """
    Main function demonstrating advanced Strands agent with MCP Gateway integration.
    
    This function showcases:
    1. Automatic model detection and configuration
    2. MCP Gateway connection and tool discovery
    3. Agent creation with both MCP and custom tools
    4. Proper error handling and resource management
    5. Context manager usage for MCP client lifecycle
    """
    
    print("🚀 Starting Advanced Strands Agent with MCP Gateway Integration")
    print("=" * 60)
    
    try:
        # Step 1: Configure the AI model (local or cloud)
        model = get_model()
        
        # Step 2: Initialize MCP Gateway connection
        # MCP Gateway provides secure access to external tools and APIs
        print(f"🔗 Connecting to MCP Gateway at: {MCP_SERVER_URL}")
        mcp_client = MCPClient(lambda: sse_client(MCP_SERVER_URL))
        
        # Step 3: Use context manager for proper resource management
        # This ensures MCP connection is properly closed even if errors occur
        with mcp_client:
            print("✅ MCP Gateway connection established")
            
            # Step 4: Discover available tools from MCP Gateway
            # MCP Gateway can provide search, file operations, API access, etc.
            mcp_tools = mcp_client.list_tools_sync()
                       
            # Step 5: Create agent with combined tool set
            # Combine MCP-provided external tools with custom local tools
            all_tools = mcp_tools + [save_definition]
            print(f"🤖 Creating agent with {len(all_tools)} total tools")
            
            agent = Agent(
                model=model,
                tools=all_tools,
                system_prompt=f"""You are an intelligent research assistant with access to external tools through MCP Gateway.

Your task is to research and define terms by:
1. Using the search tool to find accurate, comprehensive information
2. Synthesizing the information into a clear, well-structured definition
3. Saving the definition using the save_definition tool
4. Confirming completion to the user

## Example Workflow:

Question: "What is photosynthesis?"

1. Search for information: search(query="photosynthesis definition biology")
2. Analyze and synthesize the results
3. Save the definition: save_definition("Photosynthesis", "comprehensive definition here")
4. Confirm completion

## Your Task:
Question: {QUESTION}

Please research this term and provide a comprehensive definition."""
            )
            
            # Step 6: Execute the agent task
            print(f"📝 Processing question: {QUESTION}")
            print("🔄 Agent is working...")
            
            response = agent(QUESTION)
            
            print("\n" + "=" * 60)
            print("🎯 Agent Response:")
            print(response)
            print("=" * 60)
            
    except Exception as e:
        print(f"❌ Error during agent execution: {str(e)}")
        print("💡 Troubleshooting tips:")
        print("   - Check that MCP Gateway is running and accessible")
        print("   - Verify Docker Model Runner is available (for local models)")
        print("   - Ensure API keys are properly configured (for cloud models)")
        print("   - Check network connectivity between services")
        raise

if __name__ == "__main__":
    main()
