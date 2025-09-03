# Agent with MCP Example

Advanced agent showcasing external tool integration and production patterns.

## Learning Goals

- Integrate external tools via MCP Gateway
- Manage secrets with Docker secrets
- Understand production security patterns
- Configure flexible model selection (local/cloud)

## Quick Start

### Local Models
```bash
cd examples/agent-with-mcp/agent-docker-v7
docker compose up --build
```

### With OpenAI (requires API key)
```bash
echo "your-api-key" | docker secret create openai_api_key -
docker compose -f compose.yaml -f compose.openai.yaml up --build
```

## Key Differences from Basic Agent

- **MCP Gateway**: Secure external tool access
- **Docker Secrets**: Proper API key management  
- **Model Flexibility**: Auto-detects local vs cloud models
- **Production Ready**: Enhanced error handling and monitoring

## Key Files

- `agent.py` - Advanced agent with MCP integration
- `compose.yaml` - Local development with MCP Gateway
- `compose.openai.yaml` - Cloud model overlay with secrets

## Security Features

- API keys stored as Docker secrets (never in code)
- MCP Gateway provides tool isolation
- Minimal container attack surface