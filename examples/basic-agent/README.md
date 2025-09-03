# Enhanced Basic Agent (v1)

This is an enhanced version of the original agent-docker-v1 example, designed for educational purposes with comprehensive documentation and explanations.

## What You'll Learn

- Basic Strands SDK agent structure
- Docker Model Runner integration
- Simple tool creation and usage
- Docker Compose configuration
- Development workflow with hot reload

## Files Overview

- `agent.py` - Main agent implementation with educational comments
- `Dockerfile` - Container configuration with explanations
- `compose.yaml` - Docker Compose setup for local development
- `compose.watch.yaml` - Hot reload configuration for development
- `pyproject.toml` - Python dependencies and project configuration

## Key Features

- **Local Model Integration**: Uses Docker Model Runner for local AI models
- **Simple Tools**: Includes basic search and file operation tools
- **Hot Reload**: Docker Compose Watch for rapid development
- **Educational Comments**: Extensive inline documentation

## Quick Start

1. Navigate to this directory
2. Run `docker compose up --build`
3. Interact with the agent through the console
4. Make changes and see them reload automatically

## Architecture

```
Agent Container
├── Strands SDK Agent
├── Basic Tools (search, files)
├── Docker Model Runner Client
└── Local Model Integration
```

## Next Steps

After understanding this basic example, proceed to enhanced-agent-v7 to learn about external tool integration with MCP Gateway.