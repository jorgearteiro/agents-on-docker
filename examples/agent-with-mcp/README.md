# Enhanced Advanced Agent (v7)

This is agent showcasing MCP Gateway integration and advanced Docker AI features.

## What You'll Learn

- MCP Gateway setup and security benefits
- Docker secrets management for API keys
- External tool integration patterns
- Advanced agent architecture
- Production-ready configurations

## Files Overview

- `agent.py` - Advanced agent with MCP integration
- `simple_agent.py` - Simplified version for comparison
- `Dockerfile` - Optimized container with security practices
- `compose.yaml` - Local development with MCP Gateway
- `compose.openai.yaml` - Cloud model overlay with secrets
- `pyproject.toml` - Enhanced dependencies

## Key Features

- **MCP Gateway Integration**: Secure external tool access
- **Docker Secrets**: Proper API key management
- **Model Flexibility**: Automatic local/cloud model detection
- **Enhanced Security**: Container security best practices
- **Production Ready**: Monitoring and error handling

## Quick Start

1. Navigate to this directory
2. Set up secrets: `echo "your-api-key" | docker secret create openai_api_key -`
3. Run with local models: `docker compose up --build`
4. Or run with OpenAI: `docker compose -f compose.yaml -f compose.openai.yaml up --build`

## Architecture

```
Agent Container
├── Strands SDK Agent
├── MCP Gateway Client
├── Docker Model Runner Client
├── External Tools via MCP
└── Secrets Management
```

## Security Features

- API keys stored as Docker secrets
- MCP Gateway provides secure tool isolation
- Minimal container attack surface
- Proper secret rotation support

## Next Steps

Use this example as a foundation for building production-ready AI agents with external tool integration.