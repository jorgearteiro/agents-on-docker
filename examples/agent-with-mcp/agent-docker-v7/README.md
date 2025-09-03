# Advanced AI Agent with MCP Gateway Integration (v7)

This example demonstrates production-ready AI agent development using the Strands SDK with Model Context Protocol (MCP) Gateway for secure external tool integration. It builds upon the basic v1 example by adding real external capabilities through Docker's MCP Gateway.

## 🎯 Learning Objectives

By working through this example, you'll understand:

- **MCP Gateway Architecture**: Secure external tool integration patterns
- **Docker Secrets Management**: Production-ready credential handling
- **Automatic Model Detection**: Seamless switching between local and cloud models
- **External Tool Integration**: Real search, file operations, and API access
- **Production Patterns**: Error handling, logging, and resource management

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Your Agent    │───▶│ Docker Model     │───▶│  Local AI Model │
│   (Python)      │    │ Runner Service   │    │  (Qwen, Llama)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   MCP Gateway   │───▶│  External APIs   │───▶│ • DuckDuckGo    │
│   (Security)    │    │  & Services      │    │ • File System   │
└─────────────────┘    └──────────────────┘    │ • Web APIs      │
         │                                      └─────────────────┘
         ▼
┌─────────────────┐
│ Docker Secrets  │
│ • API Keys      │
│ • Credentials   │
└─────────────────┘
```

**Key Components:**
- **Agent Container**: Your Python application with Strands SDK and MCP integration
- **MCP Gateway**: Secure proxy for external tool access with credential management
- **Docker Model Runner**: Local AI model execution with OpenAI-compatible API
- **Docker Secrets**: Secure credential storage and injection
- **External Tools**: Real search, file operations, and API integrations

## 🔒 MCP Gateway Security Benefits

The Model Context Protocol (MCP) Gateway provides several critical security advantages:

### 1. **Credential Isolation**
- API keys and secrets are managed centrally by the gateway
- Agent code never directly handles sensitive credentials
- Automatic credential rotation and management capabilities

### 2. **Network Security**
- All external API calls are routed through the secure gateway
- Network access is controlled and monitored
- Rate limiting and abuse prevention built-in

### 3. **Tool Sandboxing**
- External tools are validated and sandboxed
- Malicious or unexpected tool behavior is contained
- Audit logging of all external tool usage

### 4. **Access Control**
- Fine-grained permissions for different tools and APIs
- Role-based access control for different agent types
- Centralized policy management

## 📁 Project Structure

```
agent-docker-v7/
├── agent.py              # Advanced agent with MCP integration
├── simple_agent.py       # Fallback agent without MCP (for comparison)
├── Dockerfile            # Container with secrets support
├── compose.yaml          # Docker Compose with MCP Gateway
├── compose.openai.yaml   # OpenAI model overlay with secrets
├── pyproject.toml        # Python dependencies including MCP
├── .dockerignore         # Build optimization
└── README.md            # This comprehensive documentation
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop with AI features enabled
- Understanding of basic Docker concepts (recommended: complete v1 example first)
- Optional: OpenAI API key for cloud model testing

### 1. Run with Local Model + MCP Gateway (Recommended)

```bash
# Navigate to this directory
cd agent-docker-v7

# Start the complete stack
docker compose up --build
```

**What happens:**
1. Docker builds your agent container with MCP support
2. MCP Gateway starts and configures external tools (DuckDuckGo search)
3. Docker Model Runner starts with a local AI model
4. Your agent connects to both services and processes the default question
5. Agent uses real search through MCP Gateway to find information
6. Results are saved to `./definitions/` directory

### 2. Run with OpenAI Model + MCP Gateway

```bash
# Create a file with your OpenAI API key
echo "sk-your-actual-api-key-here" > secret.openai-api-key

# Start with OpenAI overlay
docker compose -f compose.yaml -f compose.openai.yaml up --build
```

### 3. Development Mode with Hot Reload

```bash
# Start with automatic restart on code changes
docker compose watch
```

## 🔍 Understanding MCP Integration

### MCP Client Setup

The agent establishes a connection to MCP Gateway using Server-Sent Events (SSE):

```python
from mcp.client.sse import sse_client
from strands.tools.mcp import MCPClient

# Create MCP client with SSE transport
mcp_client = MCPClient(lambda: sse_client(MCP_SERVER_URL))

# Use context manager for proper resource management
with mcp_client:
    # Discover available tools from MCP Gateway
    mcp_tools = mcp_client.list_tools_sync()
    
    # Create agent with MCP tools + custom tools
    agent = Agent(
        model=model,
        tools=mcp_tools + [save_definition],
        system_prompt="..."
    )
```

### Available MCP Tools

The MCP Gateway in this example provides:

| Tool | Description | Security Features |
|------|-------------|-------------------|
| `search` | DuckDuckGo web search | Rate limited, content filtered |
| `read_file` | File system access | Sandboxed to allowed directories |
| `write_file` | File creation/modification | Permission-controlled writes |

### Custom Tool Integration

You can combine MCP tools with custom tools seamlessly:

```python
@tool
def save_definition(word: str, definition: str) -> str:
    """Custom tool that works alongside MCP tools."""
    # Your custom logic here
    return f"Saved definition for {word}"

# Combine MCP and custom tools
all_tools = mcp_tools + [save_definition]
agent = Agent(model=model, tools=all_tools, ...)
```

## 🔧 Configuration and Environment Variables

### Core Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_SERVER_URL` | `http://mcp-gateway:8811/sse` | MCP Gateway endpoint |
| `MODEL_RUNNER_URL` | `http://model-runner.docker.internal/...` | Local model endpoint |
| `MODEL_RUNNER_MODEL` | `ai/qwen3` | Local model identifier |
| `OPENAI_MODEL_NAME` | `gpt-4o-mini` | OpenAI model for cloud usage |
| `QUESTION` | `"Define Zorgon"` | Question for the agent |

### MCP Gateway Configuration

The MCP Gateway is configured in `compose.yaml`:

```yaml
mcp-gateway:
  image: docker/mcp-gateway:latest
  use_api_socket: true  # Enable Docker API access
  command:
    - --transport=sse   # Use Server-Sent Events
    - --servers=duckduckgo  # Enable DuckDuckGo search
    - --tools=search    # Expose search tools
```

### Docker Secrets Configuration

Secrets are defined in `compose.openai.yaml`:

```yaml
secrets:
  openai-api-key:
    file: secret.openai-api-key  # Read from local file

services:
  agent:
    secrets:
      - openai-api-key  # Mount secret in container
```

## 🛠️ Development Workflow

### Making Changes to Agent Logic

1. Edit `agent.py` with your changes
2. If using `docker compose watch`, changes auto-restart the container
3. Otherwise, restart with `docker compose up --build`

### Adding New MCP Tools

1. Configure additional MCP servers in `compose.yaml`:
```yaml
mcp-gateway:
  command:
    - --transport=sse
    - --servers=duckduckgo,github,slack  # Add more servers
    - --tools=search,github_api,slack_api
```

2. The agent will automatically discover and use new tools

### Testing Different Questions

```bash
# Test with environment variable
QUESTION="What is quantum computing?" docker compose up --build

# Or modify compose.yaml directly
environment:
  - QUESTION=What is machine learning?
```

### Adding Custom Tools

```python
@tool
def custom_calculator(expression: str) -> str:
    """Safely evaluate mathematical expressions."""
    # Implementation here
    return result

# Add to agent tools list
agent = Agent(
    model=model,
    tools=mcp_tools + [save_definition, custom_calculator],
    system_prompt="..."
)
```

## 🐛 Troubleshooting

### MCP Gateway Issues

#### 1. "MCP Gateway connection failed"

**Symptoms:**
```
Error: Connection refused to http://mcp-gateway:8811/sse
```

**Solutions:**
- Check MCP Gateway logs: `docker compose logs mcp-gateway`
- Verify gateway is running: `docker compose ps`
- Ensure proper service dependencies in compose.yaml
- Check Docker network connectivity

#### 2. "No MCP tools discovered"

**Symptoms:**
```
Discovered 0 MCP tools
```

**Solutions:**
- Verify MCP Gateway configuration in compose.yaml
- Check that servers are properly specified: `--servers=duckduckgo`
- Ensure tools are exposed: `--tools=search`
- Review MCP Gateway startup logs for errors

#### 3. "MCP tool execution failed"

**Symptoms:**
```
Error executing search tool: Permission denied
```

**Solutions:**
- Check MCP Gateway permissions and configuration
- Verify external API connectivity (e.g., DuckDuckGo accessibility)
- Review rate limiting and quota restrictions
- Check Docker API socket permissions (`use_api_socket: true`)

### Docker Secrets Issues

#### 4. "OpenAI API key not found"

**Symptoms:**
```
Using Docker Model Runner (expected OpenAI)
```

**Solutions:**
- Verify secret file exists: `ls -la secret.openai-api-key`
- Check file permissions: `chmod 600 secret.openai-api-key`
- Ensure compose.openai.yaml is included in command
- Verify secret mounting in container: `docker compose exec agent ls -la /run/secrets/`

#### 5. "Invalid API key format"

**Symptoms:**
```
OpenAI API error: Invalid API key
```

**Solutions:**
- Verify API key format starts with `sk-`
- Check for extra whitespace: `cat secret.openai-api-key | wc -c`
- Ensure file contains only the API key (no newlines)
- Test API key directly with OpenAI API

### Model and Performance Issues

#### 6. "Model loading timeout"

**Symptoms:**
```
Timeout waiting for model to load
```

**Solutions:**
- Increase Docker resources (CPU, memory)
- Try a smaller model: `ai/gemma3:1B-Q4_K_M`
- Check available disk space for model downloads
- Monitor model loading: `docker compose logs -f`

#### 7. "Agent responses are slow"

**Solutions:**
- Use faster local models (1B-3B parameters)
- Increase `max_tokens` limit if responses are truncated
- Consider switching to OpenAI for faster responses
- Monitor resource usage: `docker stats`

### Debug Mode

Enable detailed logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug information
print(f"MCP Gateway URL: {MCP_SERVER_URL}")
print(f"Available tools: {[tool.name for tool in mcp_tools]}")
```

## 🔄 Comparison with v1 Example

| Feature | v1 (Basic) | v7 (Advanced) |
|---------|------------|---------------|
| **External Tools** | Mock search only | Real search via MCP Gateway |
| **Security** | Basic environment variables | Docker secrets + MCP Gateway |
| **Tool Discovery** | Static tool list | Dynamic MCP tool discovery |
| **Error Handling** | Basic try/catch | Comprehensive error management |
| **Production Ready** | Learning/demo | Production patterns |
| **Complexity** | Minimal | Moderate |

## 📚 Next Steps

After mastering this advanced example:

1. **Explore Custom MCP Servers**: Build your own MCP servers for domain-specific tools
2. **Multi-Agent Systems**: Coordinate multiple agents through MCP Gateway
3. **Production Deployment**: Learn about scaling, monitoring, and maintenance
4. **Advanced Security**: Implement custom authentication and authorization
5. **Tool Development**: Create sophisticated tools for your specific use cases

## 🔗 Related Resources

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Docker MCP Gateway Documentation](https://docs.docker.com/ai/mcp-gateway/)
- [Strands SDK MCP Integration Guide](https://docs.strands.ai/mcp)
- [Docker Secrets Management](https://docs.docker.com/engine/swarm/secrets/)
- [Production AI Agent Patterns](https://docs.docker.com/ai/best-practices/)
