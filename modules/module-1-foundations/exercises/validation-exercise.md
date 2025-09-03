# Module 1: Environment Validation Exercise

## Objective

Validate that your Docker AI Agents Workshop environment is properly configured and all components are working correctly.

**Time Required:** 10-15 minutes

## Exercise Overview

This exercise will guide you through testing each component of the Docker AI platform to ensure everything is working before we start building agents.

## Part 1: Basic Docker Validation

### Step 1.1: Verify Docker Installation

Run the following commands and record the output:

```bash
docker --version
docker compose version
docker info
```

**Expected Results:**
- Docker version 24.0.0 or later
- Docker Compose version v2.20.0 or later
- Docker info shows system information without errors

**✅ Validation:** Docker is properly installed and running.

### Step 1.2: Test Docker Functionality

```bash
docker run hello-world
```

**Expected Result:** Should display "Hello from Docker!" message.

**✅ Validation:** Docker can run containers successfully.

## Part 2: Workshop Environment Validation

### Step 2.1: Navigate to Workshop Directory

```bash
cd docker-ai-agents-workshop
ls -la
```

**Expected Result:** Should show workshop directories including `modules/`, `examples/`, `scripts/`.

### Step 2.2: Run Environment Test

```bash
./scripts/test-environment.sh
```

**Expected Result:** All tests should pass with green checkmarks.

**✅ Validation:** Workshop environment is properly configured.

## Part 3: Docker AI Components Testing

### Step 3.1: Start Docker Model Runner

```bash
cd examples/basic-setup
docker compose up -d model-runner
```

Wait for the service to start, then test:

```bash
curl http://localhost:11434/api/tags
```

**Expected Result:** JSON response listing available models.

**✅ Validation:** Docker Model Runner is accessible.

### Step 3.2: Test Model Interaction

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:1b",
    "prompt": "Hello, how are you?",
    "stream": false
  }'
```

**Expected Result:** JSON response with generated text.

**✅ Validation:** Model can generate responses.

### Step 3.3: Start MCP Gateway

```bash
docker compose up -d mcp-gateway
```

Test the gateway:

```bash
curl http://localhost:3000/health
```

**Expected Result:** JSON response showing healthy status.

**✅ Validation:** MCP Gateway is running and healthy.

### Step 3.4: Test MCP Tool Access

```bash
curl -X POST http://localhost:3000/tools/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Docker AI platform",
    "limit": 3
  }'
```

**Expected Result:** JSON response with search results.

**✅ Validation:** MCP tools are accessible through the gateway.

## Part 4: Development Environment Testing

### Step 4.1: Test Docker Compose Watch (Optional)

Create a test file to monitor:

```bash
echo "console.log('Hello Workshop');" > test-app.js
```

Create a simple compose file with watch:

```yaml
# test-compose.yml
version: '3.8'
services:
  test-app:
    image: node:18-alpine
    working_dir: /app
    volumes:
      - .:/app
    command: node test-app.js
    develop:
      watch:
        - action: sync
          path: ./test-app.js
          target: /app/test-app.js
```

Run with watch:

```bash
docker compose -f test-compose.yml watch
```

In another terminal, modify the test file:

```bash
echo "console.log('Hello Workshop - Updated!');" > test-app.js
```

**Expected Result:** Should see the container restart and show updated output.

Stop the watch with `Ctrl+C` and clean up:

```bash
rm test-app.js test-compose.yml
```

**✅ Validation:** Docker Compose Watch is working for development.

## Part 5: Integration Testing

### Step 5.1: Test Complete Stack

Start all services:

```bash
docker compose up -d
```

Check all services are running:

```bash
docker compose ps
```

**Expected Result:** All services should show "Up" status.

### Step 5.2: Test Service Communication

Test that services can communicate:

```bash
# Test from within the network
docker compose exec model-runner curl http://mcp-gateway:3000/health
```

**Expected Result:** Should return health status from MCP Gateway.

**✅ Validation:** Services can communicate within Docker network.

## Part 6: Performance and Resource Testing

### Step 6.1: Check Resource Usage

```bash
docker stats --no-stream
```

**Expected Result:** Should show resource usage for running containers.

### Step 6.2: Test Model Performance

Time a model request:

```bash
time curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:1b",
    "prompt": "Explain Docker in one sentence.",
    "stream": false
  }'
```

**Expected Result:** Should complete within reasonable time (< 30 seconds for small model).

**✅ Validation:** Model performance is acceptable for workshop use.

## Troubleshooting Section

### Common Issues and Solutions

#### Issue: Port Already in Use

**Error:** `Error: port 11434 is already in use`

**Solution:**
```bash
# Find what's using the port
lsof -i :11434

# Stop conflicting service or change port in docker-compose.yml
```

#### Issue: Model Download Slow/Fails

**Error:** Model download timeout or failure

**Solution:**
```bash
# Use smaller model
docker compose exec model-runner ollama pull llama3.2:1b

# Or skip model download and use API-based models
```

#### Issue: MCP Gateway Not Responding

**Error:** `Connection refused` on port 3000

**Solution:**
```bash
# Check container logs
docker compose logs mcp-gateway

# Restart the service
docker compose restart mcp-gateway
```

#### Issue: Docker Compose Watch Not Working

**Error:** File changes not detected

**Solution:**
```bash
# Ensure you're using Docker Compose v2.20+
docker compose version

# Check file permissions
ls -la test-app.js
```

## Validation Checklist

Complete this checklist to confirm your environment is ready:

### Basic Setup
- [ ] Docker version 24.0.0+ installed
- [ ] Docker Compose v2.20.0+ available
- [ ] Docker Desktop running without errors
- [ ] Workshop repository cloned and accessible

### Docker AI Components
- [ ] Docker Model Runner starts successfully
- [ ] Model Runner API responds on port 11434
- [ ] Can generate text using local model
- [ ] MCP Gateway starts successfully
- [ ] MCP Gateway health check passes
- [ ] Can access MCP tools through gateway

### Development Environment
- [ ] Docker Compose Watch functionality works
- [ ] All services start with `docker compose up -d`
- [ ] Services can communicate within Docker network
- [ ] Resource usage is reasonable

### Performance
- [ ] Model responses complete within 30 seconds
- [ ] No memory or CPU warnings
- [ ] All containers remain stable

## Next Steps

Once all validations pass:

1. **Stop test services:**
   ```bash
   docker compose down
   ```

2. **Proceed to Module 2:** You're ready to build your first AI agent!

3. **Keep this reference:** Bookmark this validation exercise for troubleshooting later.

## Quick Reference Commands

```bash
# Start all services
docker compose up -d

# Check service status
docker compose ps

# View logs
docker compose logs [service-name]

# Stop all services
docker compose down

# Test environment
./scripts/test-environment.sh

# Reset if needed
./scripts/reset-environment.sh
```

## Success Criteria

Your environment is ready when:
- ✅ All validation checkpoints pass
- ✅ No error messages in service logs
- ✅ Model responses are generated successfully
- ✅ MCP tools are accessible
- ✅ Docker Compose Watch responds to file changes

**Congratulations!** Your Docker AI Agents Workshop environment is ready. You can now confidently proceed to building your first AI agent in Module 2.