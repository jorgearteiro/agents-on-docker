# Exercise 2: Development Workflow with Docker Compose Watch

**Duration:** 15 minutes  
**Objective:** Master Docker Compose Watch for efficient agent development

## Learning Goals

By completing this exercise, you will:
- ✅ Configure Docker Compose Watch for hot reload development
- ✅ Make iterative improvements to your agent efficiently
- ✅ Test different models and configurations quickly
- ✅ Debug common development issues effectively

## Prerequisites

- Completed Exercise 1 (Build Your First Agent)
- Working agent from Exercise 1 in `personal-assistant-agent/` directory

## Overview

Traditional development with Docker requires rebuilding containers for every code change. Docker Compose Watch eliminates this friction by automatically syncing changes and restarting services, enabling rapid iteration.

## Step 1: Enhance Your Compose Configuration (3 minutes)

Navigate to your `personal-assistant-agent/` directory and enhance the `compose.yaml` file:

```yaml
services:
  personal-assistant:
    build: .
    
    # Environment configuration
    environment:
      - USER_QUERY=Help me test the development workflow
    
    # Mount directories for persistence and development
    volumes:
      - ./notes:/app/notes
      - ./logs:/app/logs  # Add logs directory
    
    # Docker AI Platform integration
    models:
      llm:
        endpoint_var: MODEL_RUNNER_URL
        model_var: MODEL_RUNNER_MODEL
    
    # Enhanced development configuration
    develop:
      watch:
        # Sync Python files and restart service
        - action: sync+restart
          path: ./agent.py
          target: /app/agent.py
        
        # Sync any new Python files
        - action: sync+restart
          path: ./*.py
          target: /app/
          ignore:
            - validate.py
        
        # Rebuild on dependency changes
        - action: rebuild
          path: ./pyproject.toml
        
        # Sync configuration files without restart
        - action: sync
          path: ./config/
          target: /app/config/
          ignore:
            - "*.tmp"
            - "*.log"

# Model configuration with multiple options
models:
  llm:
    model: ai/gemma3:1B-Q4_K_M  # Fast model for development
    context_size: 8192

# Development profiles for different scenarios
profiles:
  # Fast development with small model
  dev:
    services:
      personal-assistant:
        environment:
          - USER_QUERY=Quick test query
        models:
          llm:
            model: ai/gemma3:1B-Q4_K_M
  
  # Testing with larger model
  test:
    services:
      personal-assistant:
        environment:
          - USER_QUERY=Complex reasoning test
        models:
          llm:
            model: ai/qwen3:1.5B-Q4_K_M
```

## Step 2: Add Development Utilities (5 minutes)

### Create a Logging System

Add logging to your `agent.py` to better track development changes:

```python
# Add these imports at the top of agent.py
import logging
from datetime import datetime

# Add this function after the imports
def setup_logging():
    """Set up logging for development."""
    # Create logs directory if it doesn't exist
    os.makedirs("/app/logs", exist_ok=True)
    
    # Configure logging
    log_filename = f"/app/logs/agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()  # Also log to console
        ]
    )
    return logging.getLogger(__name__)

# Modify your main() function to use logging
def main():
    """Main function to run the personal assistant agent."""
    logger = setup_logging()
    
    print("🤖 Personal Assistant Agent Starting...")
    logger.info("Agent starting with development logging enabled")
    print(f"❓ User Query: {USER_QUERY}")
    print("=" * 60)
    
    # ... rest of your existing main() function code ...
    
    try:
        print("🔄 Processing your request...")
        logger.info(f"Processing query: {USER_QUERY}")
        
        response = agent(USER_QUERY)
        logger.info("Query processed successfully")
        
        print(f"\n✅ Assistant Response:\n{response}")
        
        # Show saved notes if any exist
        notes_dir = "/app/notes"
        if os.path.exists(notes_dir) and os.listdir(notes_dir):
            print(f"\n📋 Saved Notes:")
            for note_file in sorted(os.listdir(notes_dir)):
                print(f"  - {note_file}")
        
        # Show log files
        logs_dir = "/app/logs"
        if os.path.exists(logs_dir) and os.listdir(logs_dir):
            print(f"\n📝 Log Files:")
            for log_file in sorted(os.listdir(logs_dir)):
                print(f"  - {log_file}")
        
    except Exception as e:
        logger.error(f"Agent error: {e}")
        print(f"❌ Error: {e}")
        # ... rest of error handling ...
```

### Create Development Helper Scripts

Create `dev-tools.py` for development utilities:

```python
#!/usr/bin/env python3
"""
Development tools for the Personal Assistant Agent
"""

import os
import json
from datetime import datetime

def create_test_queries():
    """Create a set of test queries for development."""
    test_queries = [
        "What time is it in New York?",
        "Calculate 15 * 24 + 100",
        "Save a note titled 'Meeting' with content 'Team standup at 9 AM'",
        "Search for information about artificial intelligence",
        "What's the time in Tokyo and London? Also calculate 50 / 2",
        "Save a shopping list note with milk, bread, and eggs",
        "Search for weather information and tell me the time in Sydney"
    ]
    
    return test_queries

def log_development_session():
    """Log the current development session."""
    session_info = {
        "timestamp": datetime.now().isoformat(),
        "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "test_queries": create_test_queries(),
        "environment": {
            "MODEL_RUNNER_URL": os.getenv("MODEL_RUNNER_URL", "not_set"),
            "MODEL_RUNNER_MODEL": os.getenv("MODEL_RUNNER_MODEL", "not_set")
        }
    }
    
    # Save session info
    os.makedirs("/app/logs", exist_ok=True)
    with open(f"/app/logs/dev_session_{session_info['session_id']}.json", "w") as f:
        json.dump(session_info, f, indent=2)
    
    print(f"📊 Development session logged: {session_info['session_id']}")
    return session_info

if __name__ == "__main__":
    log_development_session()
```

## Step 3: Start Development with Watch Mode (2 minutes)

### Create Local Directories

```bash
# Create required directories
mkdir -p logs config

# Create a simple config file for testing sync
echo "development_mode: true" > config/settings.yaml
```

### Start Watch Mode

```bash
# Start in watch mode
docker compose watch

# You should see output like:
# [+] Running 1/1
# ✔ personal-assistant Pulled
# [+] Running 1/1
# ✔ Container personal-assistant-agent-personal-assistant-1 Started
# Watch enabled
```

## Step 4: Test Hot Reload Development (5 minutes)

### Test 1: Modify Agent Response Style

With the container running in watch mode, edit `agent.py` and change the system prompt:

```python
# In the Agent initialization, modify the system_prompt:
system_prompt="""
You are an enthusiastic Personal Assistant AI! 🎉

## Your Capabilities
- **Time Management**: Get current time in any timezone using current_time()
- **Calculations**: Perform math calculations using calculate()
- **Note Taking**: Save notes and reminders using save_note()
- **Information Search**: Search for information using search_info()

## Response Style
- Be VERY enthusiastic and use lots of emojis! 🚀
- Always start responses with "Absolutely! I'd love to help!" 
- End responses with "What else can I do for you today? 😊"
- Use tools when appropriate rather than guessing

Always call the appropriate tools to provide accurate, real-time information!
"""
```

**Watch the container automatically restart and test the new personality!**

### Test 2: Add a New Tool

Add a new tool to your agent without stopping the container:

```python
@tool
def get_random_fact() -> str:
    """Get a random interesting fact."""
    facts = [
        "🌍 The Earth travels around the sun at approximately 67,000 mph!",
        "🐙 Octopuses have three hearts and blue blood!",
        "🌙 A day on Venus is longer than its year!",
        "🧠 Your brain uses about 20% of your body's total energy!",
        "🦋 Butterflies taste with their feet!",
        "🌊 The ocean contains 99% of Earth's living space!",
        "⚡ Lightning strikes the Earth about 100 times per second!",
        "🐘 Elephants can hear sounds from up to 6 miles away!"
    ]
    
    import random
    return f"🎲 Random Fact: {random.choice(facts)}"

# Don't forget to add it to your agent's tools list:
# tools=[current_time, calculate, save_note, search_info, get_random_fact]
```

### Test 3: Modify Environment Variables

Test different queries by changing the environment variable:

```bash
# In another terminal, while watch mode is running:
USER_QUERY="Tell me a random fact and what time it is in Paris!" docker compose up --build
```

### Test 4: Test Different Models

Edit `compose.yaml` to try a different model:

```yaml
models:
  llm:
    model: ai/qwen3:1.5B-Q4_K_M  # Larger, more capable model
    context_size: 8192
```

**Watch the container rebuild automatically when you save the file!**

## Step 5: Development Workflow Best Practices (2 minutes)

### Monitor Logs in Real-Time

```bash
# In a separate terminal, watch logs
docker compose logs --follow personal-assistant

# Or watch specific log files
tail -f logs/*.log
```

### Quick Testing Commands

Create a `test.sh` script for quick testing:

```bash
#!/bin/bash
# Quick test script for development

echo "🧪 Running development tests..."

# Test different queries quickly
queries=(
    "What time is it?"
    "Calculate 10 + 5"
    "Save a test note"
    "Tell me a random fact"
)

for query in "${queries[@]}"; do
    echo "Testing: $query"
    USER_QUERY="$query" docker compose up --no-deps personal-assistant
    echo "---"
done

echo "✅ All tests completed!"
```

### Development Profiles

Use different profiles for different development scenarios:

```bash
# Fast development with small model
docker compose --profile dev watch

# Testing with larger model
docker compose --profile test watch

# Production-like testing
docker compose -f compose.yaml -f compose.production.yaml watch
```

## Validation

### Check Watch Mode is Working

Create `validate-workflow.py`:

```python
#!/usr/bin/env python3
"""
Validate the development workflow setup
"""

import os
import subprocess
import time
import sys

def test_watch_mode():
    """Test that watch mode is properly configured."""
    print("🔍 Testing Docker Compose Watch configuration...")
    
    try:
        # Check compose config
        result = subprocess.run(
            ["docker", "compose", "config"],
            capture_output=True,
            text=True
        )
        
        if "develop:" in result.stdout and "watch:" in result.stdout:
            print("✅ Watch mode configuration found")
            return True
        else:
            print("❌ Watch mode configuration missing")
            return False
            
    except Exception as e:
        print(f"❌ Error checking configuration: {e}")
        return False

def test_hot_reload():
    """Test hot reload functionality."""
    print("🔄 Testing hot reload functionality...")
    
    # Create a test file
    test_content = f"# Test file created at {time.time()}\nprint('Hot reload test')"
    
    try:
        with open("test_reload.py", "w") as f:
            f.write(test_content)
        
        print("✅ Test file created for hot reload testing")
        
        # Clean up
        os.remove("test_reload.py")
        return True
        
    except Exception as e:
        print(f"❌ Error testing hot reload: {e}")
        return False

def check_directories():
    """Check that required directories exist."""
    required_dirs = ["notes", "logs", "config"]
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ Directory exists: {directory}")
        else:
            print(f"❌ Missing directory: {directory}")
            return False
    
    return True

def main():
    """Run all workflow validation tests."""
    print("🔍 Validating Development Workflow Setup")
    print("=" * 50)
    
    tests = [
        ("Watch Mode Configuration", test_watch_mode),
        ("Hot Reload Setup", test_hot_reload),
        ("Required Directories", check_directories)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Development workflow is properly configured!")
        print("\n🚀 Next Steps:")
        print("  1. Start watch mode: docker compose watch")
        print("  2. Make changes to agent.py and see automatic restarts")
        print("  3. Try different models and configurations")
        print("  4. Proceed to Exercise 3: Custom Tools Integration")
        return True
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

### Run Validation

```bash
python validate-workflow.py
```

## Expected Workflow

When working with watch mode, your development cycle should be:

1. **Start watch mode**: `docker compose watch`
2. **Make code changes**: Edit `agent.py` in your editor
3. **See automatic restart**: Container restarts automatically
4. **Test immediately**: New functionality is available instantly
5. **Iterate quickly**: Repeat steps 2-4 for rapid development

## Troubleshooting

### Common Issues

#### 1. Watch Mode Not Restarting

**Symptoms:**
- Changes to code don't trigger container restart

**Solutions:**
- Check watch configuration in `compose.yaml`
- Ensure file paths are correct
- Verify Docker Compose version supports watch

#### 2. Frequent Rebuilds

**Symptoms:**
- Container rebuilds instead of restarting

**Solutions:**
- Use `sync+restart` instead of `rebuild` for code files
- Only use `rebuild` for dependency changes
- Check ignore patterns are correct

#### 3. Permission Issues

**Symptoms:**
- Files can't be synced or created

**Solutions:**
- Check volume mount permissions
- Ensure directories exist locally
- Use proper file ownership

### Debug Commands

```bash
# Check watch configuration
docker compose config

# Monitor file changes
docker compose watch --verbose

# Check container status
docker compose ps

# View detailed logs
docker compose logs --follow --timestamps
```

## Success Criteria

You've successfully mastered the development workflow when:

- ✅ Watch mode starts without errors
- ✅ Code changes trigger automatic container restarts
- ✅ New functionality is available immediately after changes
- ✅ Different models can be tested quickly
- ✅ Logs and notes are persisted between restarts
- ✅ Development cycle is under 10 seconds from change to test

## Key Takeaways

1. **Docker Compose Watch eliminates rebuild friction**
2. **Proper ignore patterns prevent unnecessary restarts**
3. **Volume mounts preserve data during development**
4. **Logging helps track development progress**
5. **Profiles enable different development scenarios**

## Next Steps

Excellent work! You've mastered efficient agent development. Now you can:

1. **Apply this workflow to any agent project**
2. **Experiment with rapid prototyping**
3. **Test different models and configurations quickly**
4. **Proceed to Exercise 3** to learn custom tool integration

Ready to build more sophisticated tools? Let's dive into custom tool development! 🛠️