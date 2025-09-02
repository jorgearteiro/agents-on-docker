# Agent Docker v7: Strands + MCP (Simplified)

Follows crew-ai patterns with proper secrets handling and automatic model detection.

## Key Improvements

- ✅ **Proper Secrets**: Docker secrets for API keys
- ✅ **Auto Model Detection**: No manual MODEL_TYPE switching
- ✅ **Simplified Dockerfile**: Logic in entrypoint like crew-ai
- ✅ **Minimal Code**: Only essential functionality

## Usage

### Local Model (Default)
```bash
docker compose up --build
```

### OpenAI Model
```bash
# Add your API key to secret file
echo "sk-your-key" > secret.openai-api-key
docker compose -f compose.yaml -f compose.openai.yaml up --build
```

## Architecture

```
Dockerfile Logic:
- If /run/secrets/openai-api-key exists → Use OpenAI
- Else → Use local model-runner

Agent Logic:
- Auto-detect model based on OPENAI_API_KEY
- Proper MCP context manager usage
- Minimal tool implementation
```

## Files

- `agent.py` - Minimal Strands agent (50 lines)
- `Dockerfile` - Proper secrets + entrypoint logic
- `compose.yaml` - Local model setup
- `compose.openai.yaml` - OpenAI overlay with secrets
