# Environment Setup Guide

## Prerequisites

Before starting the workshop, ensure you have the following installed:

- **Docker Desktop** (version 4.20 or later)
- **Git** (for cloning repositories)
- **Text Editor** (VS Code recommended)
- **Terminal/Command Line** access

### System Requirements

- **RAM**: Minimum 8GB, recommended 16GB
- **Storage**: At least 10GB free space
- **OS**: Windows 10/11, macOS 10.15+, or Linux
- **Internet**: Required for initial setup and model downloads

## Step 1: Verify Docker Installation

First, let's verify that Docker is properly installed and running.

### 1.1 Check Docker Version

Open your terminal and run:

```bash
docker --version
docker compose version
```

**Expected Output:**
```
Docker version 24.0.0 or later
Docker Compose version v2.20.0 or later
```

### 1.2 Verify Docker Desktop is Running

Check that Docker Desktop is running:

```bash
docker info
```

**Expected Output:** Should show Docker system information without errors.

**✅ Checkpoint 1:** Docker is installed and running correctly.

## Step 2: Clone Workshop Repository

### 2.1 Clone the Repository

```bash
git clone https://github.com/docker/docker-ai-agents-workshop.git
cd docker-ai-agents-workshop
```

### 2.2 Verify Repository Structure

```bash
ls -la
```

**Expected Output:** You should see directories like `modules/`, `templates/`, `examples/`, etc.

**✅ Checkpoint 2:** Workshop repository is cloned and accessible.

## Step 3: Run Environment Setup Script

### 3.1 Make Setup Script Executable

```bash
chmod +x scripts/setup-environment.sh
```

### 3.2 Run Setup Script

```bash
./scripts/setup-environment.sh
```

This script will:
- Create necessary directories
- Pull required Docker images
- Set up configuration files
- Initialize the workshop environment

**Expected Output:**
```
✅ Creating workshop directories...
✅ Pulling Docker images...
✅ Setting up configuration files...
✅ Environment setup complete!
```

**✅ Checkpoint 3:** Environment setup script completed successfully.

## Step 4: Validate Docker AI Components

### 4.1 Start Docker Model Runner

```bash
cd examples/basic-setup
docker compose up -d model-runner
```

### 4.2 Verify Model Runner is Running

```bash
docker compose ps
```

**Expected Output:**
```
NAME                    IMAGE                     STATUS
basic-setup-model-runner-1   docker/model-runner:latest   Up
```

### 4.3 Test Model Runner API

```bash
curl http://localhost:11434/api/tags
```

**Expected Output:** JSON response listing available models.

**✅ Checkpoint 4:** Docker Model Runner is running and accessible.

### 4.4 Start MCP Gateway

```bash
docker compose up -d mcp-gateway
```

### 4.5 Test MCP Gateway

```bash
curl http://localhost:3000/health
```

**Expected Output:**
```json
{"status": "healthy", "services": ["search", "filesystem"]}
```

**✅ Checkpoint 5:** MCP Gateway is running and healthy.

## Step 5: Test Complete Environment

### 5.1 Start All Services

```bash
docker compose up -d
```

### 5.2 Verify All Services

```bash
docker compose ps
```

**Expected Output:** All services should show "Up" status.

### 5.3 Run Environment Test

```bash
./scripts/test-environment.sh
```

This script tests:
- Docker Model Runner connectivity
- MCP Gateway health
- Basic agent functionality
- File system permissions

**Expected Output:**
```
✅ Docker Model Runner: OK
✅ MCP Gateway: OK
✅ Agent Container: OK
✅ File Permissions: OK
✅ All tests passed!
```

**✅ Checkpoint 6:** Complete environment is working correctly.

## Step 6: Explore Your Environment

### 6.1 View Running Containers

```bash
docker ps
```

### 6.2 Check Container Logs

```bash
docker compose logs model-runner
docker compose logs mcp-gateway
```

### 6.3 Access Container Shell (Optional)

```bash
docker compose exec model-runner sh
```

Type `exit` to leave the container shell.

**✅ Checkpoint 7:** You can navigate and inspect your Docker environment.

## Troubleshooting Guide

### Common Issues and Solutions

#### Issue: Docker Desktop Not Running

**Symptoms:**
- `docker: command not found`
- `Cannot connect to the Docker daemon`

**Solution:**
1. Start Docker Desktop application
2. Wait for Docker to fully initialize
3. Retry the commands

#### Issue: Port Already in Use

**Symptoms:**
- `Error: port 11434 is already in use`
- `Error: port 3000 is already in use`

**Solution:**
1. Check what's using the port:
   ```bash
   lsof -i :11434
   lsof -i :3000
   ```
2. Stop the conflicting service or change ports in `docker-compose.yml`

#### Issue: Model Download Fails

**Symptoms:**
- `Error pulling model`
- `Connection timeout`

**Solution:**
1. Check internet connection
2. Retry the setup script:
   ```bash
   ./scripts/setup-environment.sh --retry
   ```
3. Use alternative model if available

#### Issue: Permission Denied

**Symptoms:**
- `Permission denied` when running scripts
- `Cannot create directory`

**Solution:**
1. Make scripts executable:
   ```bash
   chmod +x scripts/*.sh
   ```
2. Check Docker permissions:
   ```bash
   docker run hello-world
   ```

#### Issue: Insufficient Resources

**Symptoms:**
- Containers keep restarting
- Out of memory errors

**Solution:**
1. Increase Docker Desktop memory allocation (8GB minimum)
2. Close other applications to free up resources
3. Use lighter models if available

### Getting Help

If you encounter issues not covered here:

1. **Check the logs:**
   ```bash
   docker compose logs
   ```

2. **Restart services:**
   ```bash
   docker compose down
   docker compose up -d
   ```

3. **Reset environment:**
   ```bash
   ./scripts/reset-environment.sh
   ./scripts/setup-environment.sh
   ```

4. **Ask for help:** Raise your hand or ask in the workshop chat.

## Environment Validation Checklist

Before proceeding to Module 2, ensure all checkpoints are completed:

- [ ] ✅ Checkpoint 1: Docker is installed and running
- [ ] ✅ Checkpoint 2: Workshop repository is cloned
- [ ] ✅ Checkpoint 3: Environment setup script completed
- [ ] ✅ Checkpoint 4: Docker Model Runner is running
- [ ] ✅ Checkpoint 5: MCP Gateway is running
- [ ] ✅ Checkpoint 6: Complete environment test passed
- [ ] ✅ Checkpoint 7: Can navigate Docker environment

## Next Steps

Congratulations! Your environment is ready. You can now proceed to **Module 2: Basic Agent Development** where you'll build your first AI agent using the Strands SDK.

## Quick Reference Commands

```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# View service status
docker compose ps

# View logs
docker compose logs [service-name]

# Test environment
./scripts/test-environment.sh

# Reset environment
./scripts/reset-environment.sh
```