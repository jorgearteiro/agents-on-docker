# Exercise 1: Build Your First Agent

**Duration:** 20 minutes  
**Objective:** Create a working Strands agent with Docker Model Runner integration

## Learning Goals

By completing this exercise, you will:
- ✅ Set up a complete agent project structure
- ✅ Implement a Strands agent with custom tools
- ✅ Configure Docker Compose for local model execution
- ✅ Test and validate agent functionality

## Scenario

You're building a "Personal Assistant" agent that can:
- Tell the current time in any timezone
- Perform basic calculations
- Save notes and reminders
- Search for information (mock implementation)

## Step 1: Project Setup (5 minutes)

### Create Project Directory

```bash
# Create your project directory
mkdir personal-assistant-agent
cd personal-assistant-agent

# Create necessary subdirectories
mkdir notes
```

### Create Dependencies File

Create `pyproject.toml`:

```toml
[project]
name = "personal-assistant-agent"
version = "0.1.0"
description = "A personal assistant AI agent built with Strands SDK"
dependencies = [
    "strands>=0.1.0",
    "strands-tools>=0.1.0",
    "pytz>=2023.3"
]

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
```

## Step 2: Implement the Agent (10 minutes)

Create `agent.py` with the following implementation:

```python
#!/usr/bin/env python3
"""
Personal Assistant Agent

A helpful AI assistant that can manage time, calculations, and notes.
This demonstrates core Strands SDK concepts with practical functionality.
"""

import os
from datetime import datetime
from strands import Agent, tool
from strands.models.openai import OpenAIModel
from strands_tools import current_time

# Configuration from environment
MODEL_RUNNER_URL = os.getenv("MODEL_RUNNER_URL", "http://model-runner.docker.internal/engines/llama.cpp/v1")
MODEL_RUNNER_MODEL = os.getenv("MODEL_RUNNER_MODEL", "ai/gemma3:1B-Q4_K_M")
USER_QUERY = os.getenv("USER_QUERY", "What time is it in New York and can you save a note that I have a meeting at 3 PM?")

@tool
def calculate(expression: str) -> str:
    """Perform basic mathematical calculations safely."""
    try:
        # Validate expression contains only safe characters
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return "❌ Error: Only basic math operations (+, -, *, /, parentheses) are allowed"
        
        # Evaluate the expression
        result = eval(expression)
        return f"🧮 Calculation: {expression} = {result}"
        
    except ZeroDivisionError:
        return "❌ Error: Division by zero is not allowed"
    except Exception as e:
        return f"❌ Calculation error: {str(e)}"

@tool
def save_note(title: str, content: str) -> str:
    """Save a note or reminder to a file."""
    try:
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{title.replace(' ', '_').lower()}.txt"
        filepath = f"/app/notes/{filename}"
        
        # Create note content with metadata
        note_content = f"""Title: {title}
Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Content:
{content}
"""
        
        # Save the note
        with open(filepath, "w") as f:
            f.write(note_content)
        
        return f"📝 Note saved successfully as '{filename}'"
        
    except Exception as e:
        return f"❌ Error saving note: {str(e)}"

@tool
def search_info(query: str) -> str:
    """Search for information about a topic (mock implementation for demo)."""
    # Mock search results for common queries
    mock_database = {
        "weather": "🌤️ Current weather information would be retrieved from a weather API in a real implementation.",
        "news": "📰 Latest news headlines would be fetched from a news API in a real implementation.",
        "stocks": "📈 Stock market data would be retrieved from a financial API in a real implementation.",
        "restaurants": "🍽️ Restaurant recommendations would be fetched from a places API in a real implementation.",
        "movies": "🎬 Movie information would be retrieved from a movie database API in a real implementation."
    }
    
    # Simple keyword matching
    query_lower = query.lower()
    for keyword, response in mock_database.items():
        if keyword in query_lower:
            return f"🔍 Search results for '{query}':\n{response}"
    
    return f"🔍 Search results for '{query}':\nThis is a mock search result. In a real implementation, this would query external APIs or databases to provide relevant information about {query}."

def main():
    """Main function to run the personal assistant agent."""
    print("🤖 Personal Assistant Agent Starting...")
    print(f"❓ User Query: {USER_QUERY}")
    print("=" * 60)
    
    # Initialize the model with Docker Model Runner
    model = OpenAIModel(
        client_args={
            "api_key": "sk-insecure",  # Dummy key for local models
            "base_url": MODEL_RUNNER_URL
        },
        model_id=MODEL_RUNNER_MODEL,
        params={
            "temperature": 0.2,  # Slightly creative but mostly deterministic
            "max_tokens": 600
        }
    )
    
    # Create the agent with tools and system prompt
    agent = Agent(
        model=model,
        tools=[current_time, calculate, save_note, search_info],
        system_prompt="""
You are a helpful Personal Assistant AI with access to several useful tools.

## Your Capabilities
- **Time Management**: Get current time in any timezone using current_time()
- **Calculations**: Perform math calculations using calculate()
- **Note Taking**: Save notes and reminders using save_note()
- **Information Search**: Search for information using search_info()

## Tool Usage Guidelines
- Use current_time(timezone='timezone_name') for time queries
- Use calculate('expression') for any math problems
- Use save_note('title', 'content') to save important information
- Use search_info('query') to find information about topics

## Response Style
- Be friendly and helpful
- Use emojis to make responses more engaging
- Always use tools when appropriate rather than guessing
- Provide clear, actionable information
- If saving notes, confirm what was saved

## Common Timezones
- US/Eastern, US/Central, US/Mountain, US/Pacific
- Europe/London, Europe/Paris, Europe/Berlin
- Asia/Tokyo, Asia/Shanghai, Australia/Sydney

Always call the appropriate tools to provide accurate, real-time information.
"""
    )
    
    try:
        print("🔄 Processing your request...")
        response = agent(USER_QUERY)
        print(f"\n✅ Assistant Response:\n{response}")
        
        # Show saved notes if any exist
        notes_dir = "/app/notes"
        if os.path.exists(notes_dir) and os.listdir(notes_dir):
            print(f"\n📋 Saved Notes:")
            for note_file in sorted(os.listdir(notes_dir)):
                print(f"  - {note_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting Tips:")
        print("  - Ensure Docker Desktop is running with AI features enabled")
        print("  - Check that the model is downloading: docker compose logs")
        print("  - Verify MODEL_RUNNER_URL is accessible")

if __name__ == "__main__":
    main()
```

## Step 3: Create Docker Configuration (3 minutes)

### Create Dockerfile

Create `Dockerfile`:

```dockerfile
# Use Python 3.12 slim for efficiency
FROM python:3.12-slim

# Prevent Python output buffering
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast package management
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY pyproject.toml ./
RUN uv pip install --system .

# Copy application code
COPY agent.py .

# Create notes directory
RUN mkdir -p /app/notes

# Run the agent
CMD ["python", "agent.py"]
```

### Create Docker Compose Configuration

Create `compose.yaml`:

```yaml
services:
  personal-assistant:
    build: .
    
    # Environment configuration
    environment:
      - USER_QUERY=What time is it in Tokyo? Also calculate 15 * 24 and save a note about my dentist appointment tomorrow at 2 PM.
    
    # Mount notes directory for persistence
    volumes:
      - ./notes:/app/notes
    
    # Docker AI Platform integration
    models:
      llm:
        endpoint_var: MODEL_RUNNER_URL
        model_var: MODEL_RUNNER_MODEL
    
    # Development configuration
    develop:
      watch:
        - action: sync+restart
          path: .
          target: /app
          ignore:
            - __pycache__/
            - notes/
        - action: rebuild
          path: ./pyproject.toml

# Model configuration
models:
  llm:
    model: ai/gemma3:1B-Q4_K_M
    context_size: 8192
```

## Step 4: Test Your Agent (2 minutes)

### Run the Agent

```bash
# Build and run the agent
docker compose up --build

# Check if notes were saved
ls -la notes/
```

### Test Different Queries

```bash
# Test with a different query
USER_QUERY="What's 25 * 4 + 10? Also tell me the time in London." docker compose up --build

# Test note-taking functionality
USER_QUERY="Save a note titled 'Shopping List' with content 'milk, bread, eggs, coffee'" docker compose up --build
```

## Validation

### Automatic Validation Script

Create `validate.py` to check your implementation:

```python
#!/usr/bin/env python3
"""
Validation script for Exercise 1: Build Your First Agent
"""

import os
import subprocess
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a required file exists."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ Missing {description}: {filepath}")
        return False

def check_file_content(filepath, required_content, description):
    """Check if file contains required content."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            if required_content in content:
                print(f"✅ {description}")
                return True
            else:
                print(f"❌ {description}")
                return False
    except FileNotFoundError:
        print(f"❌ File not found for {description}: {filepath}")
        return False

def run_docker_compose_check():
    """Check if Docker Compose configuration is valid."""
    try:
        result = subprocess.run(
            ["docker", "compose", "config"],
            capture_output=True,
            text=True,
            cwd="."
        )
        if result.returncode == 0:
            print("✅ Docker Compose configuration is valid")
            return True
        else:
            print(f"❌ Docker Compose configuration error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ Docker Compose not found. Please install Docker Desktop.")
        return False

def main():
    """Run all validation checks."""
    print("🔍 Validating Exercise 1: Build Your First Agent")
    print("=" * 50)
    
    checks_passed = 0
    total_checks = 0
    
    # Check required files exist
    required_files = [
        ("pyproject.toml", "Dependencies file"),
        ("agent.py", "Agent implementation"),
        ("Dockerfile", "Docker configuration"),
        ("compose.yaml", "Docker Compose configuration")
    ]
    
    for filepath, description in required_files:
        total_checks += 1
        if check_file_exists(filepath, description):
            checks_passed += 1
    
    # Check agent.py content
    agent_checks = [
        ("from strands import Agent, tool", "Strands imports"),
        ("@tool", "Tool decorator usage"),
        ("def calculate(", "Calculate tool implementation"),
        ("def save_note(", "Save note tool implementation"),
        ("def search_info(", "Search info tool implementation"),
        ("Agent(", "Agent instantiation")
    ]
    
    for content, description in agent_checks:
        total_checks += 1
        if check_file_content("agent.py", content, description):
            checks_passed += 1
    
    # Check Docker Compose configuration
    compose_checks = [
        ("models:", "Model configuration"),
        ("llm:", "Model service definition"),
        ("ai/gemma3:1B-Q4_K_M", "Model specification"),
        ("volumes:", "Volume mounting"),
        ("./notes:/app/notes", "Notes directory mounting")
    ]
    
    for content, description in compose_checks:
        total_checks += 1
        if check_file_content("compose.yaml", content, description):
            checks_passed += 1
    
    # Check Docker Compose validity
    total_checks += 1
    if run_docker_compose_check():
        checks_passed += 1
    
    # Check notes directory
    total_checks += 1
    if os.path.exists("notes"):
        print("✅ Notes directory exists")
        checks_passed += 1
    else:
        print("❌ Notes directory missing")
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Validation Results: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("🎉 Congratulations! Your agent implementation is complete and correct.")
        print("\n🚀 Next Steps:")
        print("  1. Run your agent: docker compose up --build")
        print("  2. Try different queries by modifying USER_QUERY")
        print("  3. Proceed to Exercise 2: Development Workflow")
        return True
    else:
        print("⚠️  Some checks failed. Please review the errors above and fix them.")
        print("\n💡 Common Issues:")
        print("  - Missing required files")
        print("  - Incorrect function names or decorators")
        print("  - Invalid Docker Compose syntax")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

### Run Validation

```bash
# Make validation script executable
chmod +x validate.py

# Run validation
python validate.py
```

## Expected Output

When you run your agent successfully, you should see output similar to:

```
🤖 Personal Assistant Agent Starting...
❓ User Query: What time is it in Tokyo? Also calculate 15 * 24 and save a note about my dentist appointment tomorrow at 2 PM.
============================================================
🔄 Processing your request...

✅ Assistant Response:
I'll help you with all three requests!

First, let me get the current time in Tokyo:
The current time in Tokyo is: 2024-01-15 14:30:22 JST

Now for the calculation:
🧮 Calculation: 15 * 24 = 360

And I'll save that note about your dentist appointment:
📝 Note saved successfully as '20240115_143022_dentist_appointment.txt'

Is there anything else you'd like me to help you with?

📋 Saved Notes:
  - 20240115_143022_dentist_appointment.txt
```

## Troubleshooting

### Common Issues and Solutions

#### 1. "Connection refused" to Model Runner

**Symptoms:**
```
Error: Connection refused to http://model-runner.docker.internal
```

**Solutions:**
- Ensure Docker Desktop is running with AI features enabled
- Wait for model download to complete (first run takes time)
- Check model status: `docker compose logs`

#### 2. "Module not found" errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'strands'
```

**Solutions:**
- Rebuild the container: `docker compose up --build`
- Check `pyproject.toml` syntax
- Clear Docker cache: `docker system prune -a`

#### 3. Notes not saving

**Symptoms:**
- Agent runs but no notes appear in `./notes/` directory

**Solutions:**
- Check volume mounting in `compose.yaml`
- Ensure `./notes` directory exists locally
- Verify container has write permissions

#### 4. Agent gives generic responses

**Symptoms:**
- Agent doesn't use tools or gives vague answers

**Solutions:**
- Check tool decorators are correct (`@tool`)
- Verify tools are added to agent's tools list
- Improve system prompt with clearer instructions

### Debug Commands

```bash
# Check Docker Compose configuration
docker compose config

# View detailed logs
docker compose logs --follow

# Test container without running agent
docker compose run personal-assistant bash

# Check if model is loaded
docker model ls
```

## Success Criteria

You've successfully completed this exercise when:

- ✅ All validation checks pass
- ✅ Agent responds to queries using appropriate tools
- ✅ Time queries return current time in specified timezone
- ✅ Calculations are performed correctly
- ✅ Notes are saved to the local `./notes/` directory
- ✅ Docker Compose Watch works for development

## Next Steps

Congratulations! You've built your first AI agent. Now you can:

1. **Experiment with different queries** to test all tools
2. **Try different models** by changing the model specification
3. **Add more tools** for additional functionality
4. **Proceed to Exercise 2** to learn development workflow optimization

Ready for the next challenge? Let's master the development workflow! 🚀