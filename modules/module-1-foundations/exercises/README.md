# Module 1 Exercises

## Overview

Module 1 exercises focus on setting up and validating your Docker AI Agents Workshop environment. These hands-on exercises ensure you have a working development environment before building your first AI agent.

## Exercise Files

- **[setup-guide.md](setup-guide.md)** - Complete step-by-step environment setup
- **[validation-exercise.md](validation-exercise.md)** - Interactive validation and testing
- **[troubleshooting-guide.md](troubleshooting-guide.md)** - Solutions for common issues

## Exercise 1.1: Environment Setup and Validation

**Objective:** Set up and validate your workshop environment

**Time:** 20-25 minutes

**Prerequisites:**
- Docker Desktop installed
- Git installed
- Terminal/command line access
- 8GB+ RAM available

### Quick Start

1. **Follow the setup guide:** [setup-guide.md](setup-guide.md)
2. **Run validation exercise:** [validation-exercise.md](validation-exercise.md)
3. **If issues arise:** [troubleshooting-guide.md](troubleshooting-guide.md)

### Key Steps
1. Verify Docker installation and system requirements
2. Clone workshop repository and run setup script
3. Start Docker AI platform components (Model Runner, MCP Gateway)
4. Validate all services are running and accessible
5. Test basic AI functionality and tool integration
6. Verify development environment (Docker Compose Watch)

### Success Criteria
- [ ] Docker Desktop is running without errors
- [ ] All required Docker images are pulled and available
- [ ] Workshop directory structure is created correctly
- [ ] Docker Model Runner responds on port 11434
- [ ] MCP Gateway is healthy on port 3000
- [ ] Basic model generation works
- [ ] MCP tools are accessible
- [ ] Docker Compose Watch responds to file changes
- [ ] All validation tests pass

## Exercise 1.2: Explore Docker AI Components

**Objective:** Understand Docker AI platform components through hands-on exploration

**Time:** 15-20 minutes

**Prerequisites:** Completed Exercise 1.1 successfully

### Learning Goals
- Understand the role of each Docker AI component
- Learn how components communicate and work together
- Practice using Docker commands for AI development
- Explore configuration options and customization

### Key Activities

#### Part A: Docker Model Runner Deep Dive
1. **Examine Model Runner configuration:**
   ```bash
   cd examples/basic-setup
   cat docker-compose.yml | grep -A 10 model-runner
   ```

2. **Test different models:**
   ```bash
   # List available models
   curl http://localhost:11434/api/tags
   
   # Test model generation
   curl -X POST http://localhost:11434/api/generate \
     -H "Content-Type: application/json" \
     -d '{"model": "llama3.2:1b", "prompt": "Explain Docker AI in one sentence."}'
   ```

3. **Monitor resource usage:**
   ```bash
   docker stats model-runner
   ```

#### Part B: MCP Gateway Exploration
1. **Check MCP Gateway health and configuration:**
   ```bash
   curl http://localhost:3000/health
   curl http://localhost:3000/tools
   ```

2. **Test MCP tools:**
   ```bash
   # Test search tool
   curl -X POST http://localhost:3000/tools/search \
     -H "Content-Type: application/json" \
     -d '{"query": "Docker containers", "limit": 3}'
   
   # Test filesystem tool
   curl -X POST http://localhost:3000/tools/filesystem \
     -H "Content-Type: application/json" \
     -d '{"action": "list", "path": "/workspace"}'
   ```

3. **Examine security features:**
   ```bash
   docker compose logs mcp-gateway | grep -i security
   ```

#### Part C: Docker Compose Watch Testing
1. **Create a test application:**
   ```bash
   echo 'console.log("Hello Workshop v1");' > test-watch.js
   ```

2. **Set up watch configuration:**
   ```yaml
   # Add to docker-compose.yml
   test-app:
     image: node:18-alpine
     working_dir: /app
     volumes:
       - .:/app
     command: node test-watch.js
     develop:
       watch:
         - action: sync
           path: ./test-watch.js
           target: /app/test-watch.js
   ```

3. **Test hot reload:**
   ```bash
   docker compose watch test-app
   # In another terminal, modify test-watch.js
   echo 'console.log("Hello Workshop v2 - Updated!");' > test-watch.js
   ```

### Validation Checklist
- [ ] Can identify each Docker AI component and its purpose
- [ ] Successfully tested Model Runner with different prompts
- [ ] Accessed and used MCP Gateway tools
- [ ] Understand security isolation provided by MCP Gateway
- [ ] Successfully demonstrated Docker Compose Watch hot reload
- [ ] Can monitor resource usage and container logs
- [ ] Understand how components communicate within Docker network

## Exercise 1.3: Component Integration Testing (Optional)

**Objective:** Test how Docker AI components work together in a complete workflow

**Time:** 10 minutes

**Prerequisites:** Completed Exercises 1.1 and 1.2

### Integration Scenarios

1. **Model + MCP Tool Chain:**
   - Use Model Runner to generate a search query
   - Pass query to MCP Gateway search tool
   - Process search results

2. **Development Workflow:**
   - Make code changes
   - Watch automatic container updates
   - Test updated functionality immediately

3. **Resource Sharing:**
   - Run multiple agent instances
   - Share Model Runner across instances
   - Verify efficient resource utilization

### Success Criteria
- [ ] Components work together seamlessly
- [ ] Development workflow is smooth and efficient
- [ ] Resource sharing works as expected
- [ ] Ready to build first AI agent in Module 2

## Troubleshooting

If you encounter any issues during these exercises:

1. **First:** Check [troubleshooting-guide.md](troubleshooting-guide.md)
2. **Run diagnostics:** `./scripts/diagnose-environment.sh`
3. **Reset if needed:** `./scripts/reset-environment.sh`
4. **Ask for help:** Raise your hand or use workshop chat

## Next Steps

Once you've completed all Module 1 exercises:

1. **Verify completion:** All validation checkboxes should be checked
2. **Clean up test files:** Remove any temporary files created
3. **Keep services running:** Leave Docker AI services running for Module 2
4. **Proceed to Module 2:** Ready to build your first AI agent!

## Quick Reference

```bash
# Start all services
cd examples/basic-setup && docker compose up -d

# Check service status
docker compose ps

# Test Model Runner
curl http://localhost:11434/api/tags

# Test MCP Gateway
curl http://localhost:3000/health

# View logs
docker compose logs [service-name]

# Stop services
docker compose down
```