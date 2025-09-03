# Exercise 2: Docker Secrets Management for Secure API Access

**Duration:** 15 minutes  
**Objective:** Implement secure credential management using Docker secrets for cloud model access

## Overview

In this exercise, you'll learn how to securely manage API keys using Docker secrets instead of environment variables. You'll configure the agent to use OpenAI's API while keeping credentials secure and following production best practices.

## Prerequisites

- Completed Exercise 1
- OpenAI API key (or willingness to use dummy key for learning)
- Understanding of Docker Compose

## Step 1: Understanding Security Risks

First, let's understand why Docker secrets are more secure than environment variables:

### Environment Variables (Less Secure)
```bash
# ❌ Visible in process lists
ps aux | grep -i openai

# ❌ Stored in container metadata
docker inspect container_name | grep -i api

# ❌ Logged in various places
docker compose logs | grep -i key
```

### Docker Secrets (More Secure)
- Encrypted at rest and in transit
- Only available to authorized services
- Mounted as files, not environment variables
- Support automatic rotation

## Step 2: Create Docker Secrets

Let's create a Docker secret for the OpenAI API key:

```bash
# Option 1: Create from command line (for testing)
echo "sk-test-dummy-key-for-learning" | docker secret create openai_api_key -

# Option 2: Create from file (recommended for production)
# echo "your-real-api-key-here" > openai-key.txt
# docker secret create openai_api_key ./openai-key.txt
# rm openai-key.txt  # Remove the file after creating secret

# Verify the secret was created
docker secret ls
```

**Expected output:**
```
ID                          NAME              DRIVER    CREATED         UPDATED
abc123def456                openai_api_key              2 minutes ago   2 minutes ago
```

## Step 3: Create Enhanced Compose Configuration

Create a new compose file that uses Docker secrets:

```bash
# Create a new compose file for secrets demo
cat > compose.secrets.yaml << 'EOF'
services:
  # Enhanced AI Agent with Secrets Management
  agent:
    build: .
    
    # Mount Docker secrets
    secrets:
      - openai_api_key
    
    environment:
      # MCP Gateway connection
      - MCP_SERVER_URL=http://mcp-gateway:8811/sse
      
      # Research question
      - QUESTION=Define Machine Learning
      
      # Secret file path (not the actual key!)
      - OPENAI_API_KEY_FILE=/run/secrets/openai_api_key
    
    volumes:
      - ./definitions:/app/definitions
    
    depends_on:
      - mcp-gateway
    
    # Docker AI Platform Integration
    models:
      llm:
        endpoint_var: MODEL_RUNNER_URL
        model_var: MODEL_RUNNER_MODEL

  # MCP Gateway Service
  mcp-gateway:
    image: docker/mcp-gateway:latest
    use_api_socket: true
    command:
      - --transport=sse
      - --servers=duckduckgo
      - --tools=search

# Docker Secrets Configuration
secrets:
  openai_api_key:
    external: true  # Use existing secret created above

# Docker AI Model Configuration
models:
  llm:
    model: ai/gemma3:1B-Q4_K_M
    context_size: 8192
EOF
```

## Step 4: Enhance Agent Code for Secrets

Create an enhanced version of the agent that can load secrets securely:

```bash
# Create enhanced agent with secrets support
cat > agent-secrets.py << 'EOF'
#!/usr/bin/env python3
"""
Enhanced Strands AI Agent with Docker Secrets Management
Demonstrates secure credential handling in containerized environments
"""

import os
from pathlib import Path
from mcp.client.sse import sse_client
from strands import Agent, tool
from strands.tools.mcp import MCPClient
from strands.models.openai import OpenAIModel

# Configuration from environment variables
MODEL_RUNNER_URL = os.getenv("MODEL_RUNNER_URL", "http://model-runner.docker.internal/engines/llama.cpp/v1")
MODEL_RUNNER_MODEL = os.getenv("MODEL_RUNNER_MODEL", "ai/gemma3:1B-Q4_K_M")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://mcp-gateway:8811/sse")
QUESTION = os.getenv("QUESTION", "Define Machine Learning")

def load_secret(secret_name):
    """
    Securely load a Docker secret from the mounted file system.
    
    Docker secrets are mounted as files in /run/secrets/ directory.
    This is more secure than environment variables because:
    - Files are only readable by the container process
    - Not visible in process lists or container metadata
    - Can be rotated without container restart
    
    Args:
        secret_name (str): Name of the secret to load
        
    Returns:
        str: Secret value or None if not found
    """
    secret_path = f"/run/secrets/{secret_name}"
    try:
        with open(secret_path, 'r') as f:
            value = f.read().strip()
            if value:
                print(f"✅ Successfully loaded secret: {secret_name}")
                return value
            else:
                print(f"⚠️  Secret file is empty: {secret_name}")
                return None
    except FileNotFoundError:
        print(f"⚠️  Secret file not found: {secret_path}")
        return None
    except Exception as e:
        print(f"❌ Error loading secret {secret_name}: {e}")
        return None

def load_api_key():
    """
    Load OpenAI API key with fallback strategy.
    
    Priority order:
    1. Docker secret file (most secure)
    2. Environment variable (fallback for development)
    3. None (use local models)
    
    Returns:
        str: API key or None
    """
    # Try Docker secret first (production)
    api_key = load_secret('openai_api_key')
    if api_key and api_key != "sk-test-dummy-key-for-learning":
        return api_key
    
    # Fallback to environment variable (development)
    env_key = os.getenv('OPENAI_API_KEY')
    if env_key and env_key != "sk-insecure":
        print("⚠️  Using API key from environment variable (less secure)")
        return env_key
    
    print("ℹ️  No valid API key found, will use local models")
    return None

@tool
def save_research(topic: str, research_content: str) -> str:
    """
    Save research content to a file with enhanced formatting.
    
    Args:
        topic (str): The research topic
        research_content (str): The researched content to save
        
    Returns:
        str: Confirmation message
    """
    try:
        out_dir = Path("/app/definitions")
        out_dir.mkdir(exist_ok=True)
        
        # Create safe filename
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
        file_path = out_dir / f"{safe_topic}.md"
        
        # Write with enhanced formatting
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {topic}\n\n")
            f.write(f"**Research Date:** {Path().cwd()}\n")
            f.write(f"**Generated by:** Enhanced AI Agent with MCP Gateway\n\n")
            f.write("## Content\n\n")
            f.write(research_content.strip() + "\n\n")
            f.write("---\n")
            f.write("*This content was researched using external tools via MCP Gateway*\n")
        
        return f"✅ Research on '{topic}' saved to {file_path.name}"
        
    except Exception as e:
        return f"❌ Error saving research: {str(e)}"

def get_model():
    """
    Configure AI model with secure credential handling.
    
    Returns:
        OpenAIModel: Configured model instance
    """
    api_key = load_api_key()
    
    if api_key:
        print(f"🌐 Configuring OpenAI model: {OPENAI_MODEL_NAME}")
        return OpenAIModel(
            client_args={"api_key": api_key},
            model_id=OPENAI_MODEL_NAME,
            params={
                "temperature": 0.1,
                "max_tokens": 1500
            }
        )
    else:
        print(f"🏠 Configuring local model: {MODEL_RUNNER_MODEL}")
        return OpenAIModel(
            client_args={
                "api_key": "sk-insecure",
                "base_url": MODEL_RUNNER_URL
            },
            model_id=MODEL_RUNNER_MODEL,
            params={
                "temperature": 0.1,
                "max_tokens": 1500
            }
        )

def main():
    """Main function with enhanced security and error handling."""
    
    print("🔐 Starting Enhanced Agent with Docker Secrets Management")
    print("=" * 65)
    
    try:
        # Step 1: Configure model with secure credentials
        model = get_model()
        
        # Step 2: Connect to MCP Gateway
        print(f"🔗 Connecting to MCP Gateway: {MCP_SERVER_URL}")
        mcp_client = MCPClient(lambda: sse_client(MCP_SERVER_URL))
        
        with mcp_client:
            print("✅ MCP Gateway connection established")
            
            # Step 3: Discover tools
            mcp_tools = mcp_client.list_tools_sync()
            print(f"🛠️  Discovered {len(mcp_tools)} MCP tools")
            
            # Step 4: Create agent with all tools
            all_tools = mcp_tools + [save_research]
            
            agent = Agent(
                model=model,
                tools=all_tools,
                system_prompt=f"""You are a research assistant with secure access to external tools.

Your task is to research topics thoroughly and provide comprehensive, well-structured information.

Research Process:
1. Use the search tool to find current, accurate information
2. Analyze and synthesize multiple sources
3. Create a comprehensive summary with key points
4. Save the research using the save_research tool

Current Task: Research and explain "{QUESTION}"

Provide a detailed explanation that covers:
- Definition and core concepts
- Key applications or examples
- Current trends or developments
- Why it's important or relevant

Be thorough but concise, and ensure accuracy."""
            )
            
            # Step 5: Execute research task
            print(f"🔍 Researching: {QUESTION}")
            response = agent(QUESTION)
            
            print("\n" + "=" * 65)
            print("📋 Research Complete:")
            print(response)
            print("=" * 65)
            
    except Exception as e:
        print(f"❌ Error during execution: {str(e)}")
        print("\n💡 Troubleshooting checklist:")
        print("   ✓ MCP Gateway is running and accessible")
        print("   ✓ Docker secrets are properly configured")
        print("   ✓ API keys are valid (if using cloud models)")
        print("   ✓ Network connectivity between services")
        raise

if __name__ == "__main__":
    main()
EOF
```

## Step 5: Update Dockerfile for Secrets

Create an enhanced Dockerfile that handles the new agent:

```bash
# Create Dockerfile that can use either agent version
cat > Dockerfile.secrets << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY pyproject.toml .

# Install Python dependencies
RUN pip install -e .

# Copy application code
COPY agent.py .
COPY agent-secrets.py .

# Create definitions directory
RUN mkdir -p /app/definitions

# Default to enhanced agent with secrets
CMD ["python3", "agent-secrets.py"]
EOF
```

## Step 6: Test with Docker Secrets

Now let's test the enhanced configuration:

```bash
# Build with the new Dockerfile
docker compose -f compose.secrets.yaml build --build-arg DOCKERFILE=Dockerfile.secrets

# Start services with secrets
docker compose -f compose.secrets.yaml up
```

**Expected behavior:**
- Agent loads API key from Docker secret
- Falls back to local model if secret is dummy key
- Enhanced research output with better formatting
- Secure credential handling throughout

## Step 7: Verify Secret Security

Let's verify that secrets are handled securely:

```bash
# Check that API key is not in environment variables
docker compose -f compose.secrets.yaml exec agent env | grep -i api

# Check that secret is mounted as file
docker compose -f compose.secrets.yaml exec agent ls -la /run/secrets/

# Verify secret content (should show the dummy key)
docker compose -f compose.secrets.yaml exec agent cat /run/secrets/openai_api_key
```

**What you should see:**
- No API key in environment variables
- Secret file mounted in `/run/secrets/`
- File contains the secret value
- Proper file permissions (readable only by container process)

## Step 8: Test Secret Rotation

Demonstrate how to rotate secrets without container restart:

```bash
# Update the secret with a new value
echo "sk-new-dummy-key-rotated" | docker secret create openai_api_key_v2 -

# Update compose file to use new secret
sed -i 's/openai_api_key/openai_api_key_v2/g' compose.secrets.yaml

# Restart services to pick up new secret
docker compose -f compose.secrets.yaml up --force-recreate
```

## Validation Checkpoint

✅ **Verify your secrets implementation:**

1. **Secret Creation**: `docker secret ls` shows your created secret
2. **Secure Loading**: Agent loads API key from `/run/secrets/` not environment
3. **Fallback Behavior**: Agent gracefully handles missing or invalid secrets
4. **File Permissions**: Secret files have proper access controls
5. **No Leakage**: API keys don't appear in logs or environment variables

## Troubleshooting

### Issue: Secret not found

**Symptoms:**
```
⚠️  Secret file not found: /run/secrets/openai_api_key
```

**Solutions:**
1. Verify secret exists: `docker secret ls`
2. Check compose file has `secrets:` section for service
3. Ensure secret is listed in global `secrets:` section

### Issue: Permission denied reading secret

**Symptoms:**
```
❌ Error loading secret openai_api_key: Permission denied
```

**Solutions:**
1. Check container user permissions
2. Verify secret file permissions: `docker compose exec agent ls -la /run/secrets/`
3. Ensure proper Docker daemon configuration

### Issue: Secret contains wrong value

**Symptoms:**
- Agent uses local model despite having secret
- API authentication failures

**Solutions:**
1. Check secret content: `docker compose exec agent cat /run/secrets/openai_api_key`
2. Recreate secret with correct value
3. Verify secret name matches in compose file

## Understanding What Happened

In this exercise, you:

1. **Created Docker Secrets** - Secure credential storage mechanism
2. **Enhanced Agent Code** - Added secure secret loading functionality
3. **Updated Configuration** - Modified Docker Compose to use secrets
4. **Tested Security** - Verified credentials are not exposed
5. **Implemented Fallbacks** - Graceful handling of missing credentials

## Key Security Benefits

- **Encryption**: Secrets encrypted at rest and in transit
- **Access Control**: Only authorized containers can access secrets
- **No Environment Exposure**: Credentials not visible in process lists
- **Rotation Support**: Secrets can be updated without code changes
- **Audit Trail**: Secret access can be logged and monitored

## Production Considerations

For production deployments:

1. **External Secret Management**: Use AWS Secrets Manager, Azure Key Vault, etc.
2. **Automatic Rotation**: Implement automated secret rotation
3. **Monitoring**: Log and monitor secret access
4. **Backup**: Ensure secrets are included in backup strategies
5. **Compliance**: Meet regulatory requirements for credential management

## Next Steps

In Exercise 3, you'll learn how to create custom tools that work alongside MCP-provided tools, building a complete toolkit for your AI agents.

---

**Exercise Complete!** 🔐

You've successfully implemented secure credential management using Docker secrets, providing a foundation for production-ready AI agent deployments.