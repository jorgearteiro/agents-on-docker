# Basic Agent Example

Your first Strands SDK agent with local model integration.

## Learning Goals

- Understand Strands SDK agent structure
- Use Docker Model Runner for local AI models
- Implement basic tools (search, file operations)
- Set up development workflow with hot reload

## Quick Start

```bash
cd examples/basic-agent/agent-docker-v1
docker compose up --build
```

The agent will start and you can interact via console. Changes to `agent.py` will auto-reload.

## Key Files

- `agent.py` - Main agent implementation
- `compose.yaml` - Development setup with hot reload
- `Dockerfile` - Container configuration

## What's Next

After understanding this example, proceed to `../agent-with-mcp/` to learn external tool integration.