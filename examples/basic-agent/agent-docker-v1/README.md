# Basic AI Agent with Docker Model Runner (v1)

This example demonstrates the fundamentals of building and containerizing AI agents using the Strands SDK and Docker's AI platform. It's designed as an educational starting point that introduces core concepts without complexity.

## 🎯 Learning Objectives

By working through this example, you'll understand:

- **Strands Agent Architecture**: The three core components (model + tools + prompt)
- **Docker Model Runner**: Running AI models locally with OpenAI-compatible APIs
- **Container Development**: Building and running AI agents in Docker containers
- **Volume Mounting**: Persisting agent outputs between container runs
- **Environment Configuration**: Managing settings through environment variables

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Your Agent    │───▶│ Docker Model     │───▶│  Local AI Model │
│   (Python)      │    │ Runner Service   │    │  (Qwen, Llama)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│   Agent Tools   │
│ • Search        │
│ • File Save     │
└─────────────────┘
```

**Key Components:**
- **Agent Container**: Your Python application with Strands SDK
- **Docker Model Runner**: Provides OpenAI-compatible API for local models
- **Current Time Tool**: Built-in tool for getting time in different timezones
- **Docker Compose**: Orchestrates all services together

## 📁 Project Structure

```
agent-docker-v1/
├── agent.py              # Main agent implementation
├── Dockerfile            # Container build instructions
├── compose.yaml          # Docker Compose configuration
├── compose.openai.yaml   # OpenAI model overlay
├── pyproject.toml        # Python dependencies
├── .dockerignore         # Files to exclude from build
└── README.md            # This documentation
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop with AI features enabled
- Basic understanding of Python and Docker concepts

### 1. Run with Local Model (Recommended for Learning)

```bash
# Clone or navigate to this directory
cd agent-docker-v1

# Start the agent with local model
docker compose up --build
```

**What happens:**
1. Docker builds your agent container
2. Docker Model Runner starts with a local AI model (Gemma 3)
3. Your agent connects to the local model and asks for the current time in Sydney
4. Results are displayed in the terminal

### 2. Run with OpenAI Model (Optional)

```bash
# Create a file with your OpenAI API key
echo "sk-your-actual-api-key-here" > secret.openai-api-key

# Start with OpenAI overlay
docker compose -f compose.yaml -f compose.openai.yaml up --build
```

## 🔍 Understanding the Code

### Agent Implementation (`agent.py`)

The agent demonstrates the three pillars of Strands architecture:

#### 1. Model Configuration
```python
model = OpenAIModel(
    client_args={
        "api_key": "sk-insecure",  # Dummy key for local models
        "base_url": MODEL_RUNNER_URL  # Points to Docker Model Runner
    },
    model_id=MODEL_RUNNER_MODEL,  # Which model to use
    params={
        "temperature": 0.1,
        "max_tokens": 500
    }
)
```

#### 2. Tool Usage
```python
from strands_tools import current_time
```

#### 3. Agent Assembly
```python
agent = Agent(
    model=model,
    tools=[current_time],
    system_prompt="Call the tool once, then answer with the time. Do not call tools repeatedly."
)
```

### Docker Configuration

#### Dockerfile Breakdown
```dockerfile
FROM python:3.12-slim          # Lightweight Python base image
ENV PYTHONUNBUFFERED=1         # Ensure Python output appears in logs
RUN apt-get update && ...      # Install build dependencies
RUN pip install uv             # Fast Python package installer
WORKDIR /app                   # Set working directory
COPY pyproject.toml ./         # Copy dependency specification
RUN uv pip install --system . # Install Python dependencies
COPY agent.py .                # Copy agent code
```

#### Docker Compose Services
```yaml
services:
  agent:
    build: .                   # Build from local Dockerfile
    environment:               # Environment variables
      - QUESTION=what time it is in Sydney?
    models:                    # Docker AI model configuration
      llm:
        endpoint_var: MODEL_RUNNER_URL
        model_var: MODEL_RUNNER_MODEL
```

## 🛠️ Development Workflow

### Making Changes

The compose configuration includes Docker Compose Watch for development:

```yaml
develop:
  watch:
    - action: sync+restart    # Restart on code changes
      path: .
      target: /app
    - action: rebuild         # Rebuild on dependency changes
      path: ./pyproject.toml
```

**To develop with hot reload:**
```bash
docker compose watch
```

Now any changes to `agent.py` will automatically restart the container.

### Testing Different Questions

```bash
# Set a custom question
QUESTION="What is machine learning?" docker compose up --build

# Or modify the compose.yaml file directly
```

### Adding New Tools

1. Define a new tool function with the `@tool` decorator
2. Add comprehensive docstring (the AI model reads this!)
3. Add the tool to the agent's tools list
4. Test with `docker compose up --build`

Example:
```python
@tool
def calculate(expression: str) -> str:
    """Safely evaluate mathematical expressions."""
    try:
        result = eval(expression)  # Note: Use safe_eval in production
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_RUNNER_URL` | `http://model-runner.docker.internal/engines/llama.cpp/v1` | Docker Model Runner endpoint |
| `MODEL_RUNNER_MODEL` | `ai/gemma3:1B-Q4_K_M` | Model to use for inference |
| `QUESTION` | `"what time it is in Sydney?"` | Question for the agent to answer |

### Model Options

Edit the `models` section in `compose.yaml`:

```yaml
models:
  llm:
    model: ai/gemma3:1B-Q4_K_M    # Fast, small model
    # model: ai/llama3.2:3B-Q4_K_M  # Larger, more capable
    context_size: 8192
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. "Connection refused" or "Model Runner not accessible"

**Symptoms:**
```
Error: Connection refused to http://model-runner.docker.internal
```

**Solutions:**
- Ensure Docker Desktop is running with AI features enabled
- Check that the model is downloading: `docker compose logs`
- Verify Docker AI is available: `docker version` (look for AI features)
- Try restarting Docker Desktop

#### 2. "Model not found" or "Model loading failed"

**Symptoms:**
```
Error: Model ai/qwen3 not found
```

**Solutions:**
- Wait for model download to complete (first run takes time)
- Check available models: `docker model ls`
- Try a different model in `compose.yaml`
- Ensure sufficient disk space for model files

#### 3. "Permission denied" when saving files

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: '/app/definitions/output.txt'
```

**Solutions:**
- Check that the `./definitions` directory exists and is writable
- On Linux/Mac: `chmod 755 ./definitions`
- Ensure Docker has permission to mount the directory

#### 4. Python dependency errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'strands'
```

**Solutions:**
- Rebuild the container: `docker compose up --build`
- Check `pyproject.toml` for correct dependencies
- Clear Docker build cache: `docker system prune -a`

#### 5. Container exits immediately

**Symptoms:**
Container starts and stops without output

**Solutions:**
- Check logs: `docker compose logs agent`
- Verify Python syntax: `python agent.py` (locally)
- Ensure all required environment variables are set

### Debug Mode

For detailed debugging, modify the agent to include more logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug prints
print(f"Model URL: {MODEL_RUNNER_URL}")
print(f"Model ID: {MODEL_RUNNER_MODEL}")
```

### Getting Help

1. **Check logs**: `docker compose logs` shows all service output
2. **Inspect containers**: `docker compose ps` shows service status
3. **Test connectivity**: `docker compose exec agent ping model-runner.docker.internal`
4. **Validate configuration**: `docker compose config` shows resolved configuration

## 📚 Next Steps

After mastering this basic example:

1. **Explore agent-docker-v7**: Learn about MCP Gateway and external tool integration
2. **Add real tools**: Replace mock search with actual APIs
3. **Experiment with models**: Try different local models for various tasks
4. **Build custom tools**: Create domain-specific tools for your use case
5. **Production deployment**: Learn about scaling and monitoring agents

## 🔗 Related Resources

- [Strands SDK Documentation](https://docs.strands.ai)
- [Docker AI Platform Guide](https://docs.docker.com/ai)
- [Docker Model Runner Reference](https://docs.docker.com/ai/model-runner)
- [Docker Compose Watch Documentation](https://docs.docker.com/compose/file-watch)
