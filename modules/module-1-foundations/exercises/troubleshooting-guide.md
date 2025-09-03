# Module 1: Troubleshooting Guide

## Overview

This guide provides solutions to common issues you might encounter during Module 1 environment setup and validation.

## Quick Diagnosis

Run this command first to get an overview of your system:

```bash
./scripts/diagnose-environment.sh
```

If the script doesn't exist, create it with:

```bash
cat > scripts/diagnose-environment.sh << 'EOF'
#!/bin/bash

echo "=== Docker AI Agents Workshop - Environment Diagnosis ==="
echo ""

echo "System Information:"
echo "- OS: $(uname -s)"
echo "- Architecture: $(uname -m)"
echo "- Date: $(date)"
echo ""

echo "Docker Information:"
docker --version 2>/dev/null || echo "❌ Docker not found"
docker compose version 2>/dev/null || echo "❌ Docker Compose not found"
echo ""

echo "Docker Status:"
if docker info >/dev/null 2>&1; then
    echo "✅ Docker is running"
    echo "- Containers: $(docker ps -q | wc -l) running"
    echo "- Images: $(docker images -q | wc -l) available"
else
    echo "❌ Docker is not running"
fi
echo ""

echo "Port Status:"
for port in 11434 3000; do
    if lsof -i :$port >/dev/null 2>&1; then
        echo "⚠️  Port $port is in use"
    else
        echo "✅ Port $port is available"
    fi
done
echo ""

echo "Disk Space:"
df -h . | tail -1
echo ""

echo "Memory Usage:"
free -h 2>/dev/null || vm_stat | head -5
EOF

chmod +x scripts/diagnose-environment.sh
```

## Common Issues and Solutions

### 1. Docker Installation Issues

#### Issue: "docker: command not found"

**Cause:** Docker is not installed or not in PATH.

**Solution:**
1. **Install Docker Desktop:**
   - **Windows/Mac:** Download from [docker.com](https://www.docker.com/products/docker-desktop)
   - **Linux:** Follow [official installation guide](https://docs.docker.com/engine/install/)

2. **Verify installation:**
   ```bash
   docker --version
   ```

3. **Add to PATH if needed (Linux):**
   ```bash
   export PATH=$PATH:/usr/local/bin
   echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
   ```

#### Issue: "Cannot connect to the Docker daemon"

**Cause:** Docker Desktop is not running.

**Solution:**
1. **Start Docker Desktop:**
   - **Windows/Mac:** Launch Docker Desktop application
   - **Linux:** Start Docker service:
     ```bash
     sudo systemctl start docker
     sudo systemctl enable docker
     ```

2. **Verify Docker is running:**
   ```bash
   docker info
   ```

3. **Check Docker Desktop status:**
   - Look for Docker whale icon in system tray
   - Should show "Docker Desktop is running"

#### Issue: "permission denied while trying to connect to Docker daemon"

**Cause:** User doesn't have permission to access Docker (Linux).

**Solution:**
1. **Add user to docker group:**
   ```bash
   sudo usermod -aG docker $USER
   ```

2. **Log out and log back in, or run:**
   ```bash
   newgrp docker
   ```

3. **Test access:**
   ```bash
   docker run hello-world
   ```

### 2. Port Conflicts

#### Issue: "Port 11434 is already in use"

**Cause:** Another service is using the Model Runner port.

**Solution:**
1. **Find what's using the port:**
   ```bash
   lsof -i :11434
   # or on Windows:
   netstat -ano | findstr :11434
   ```

2. **Stop the conflicting service:**
   ```bash
   # If it's another Docker container:
   docker stop $(docker ps -q --filter "publish=11434")
   
   # If it's a system service, stop it appropriately
   ```

3. **Or change the port in docker-compose.yml:**
   ```yaml
   services:
     model-runner:
       ports:
         - "11435:11434"  # Use different external port
   ```

#### Issue: "Port 3000 is already in use"

**Cause:** Another service is using the MCP Gateway port.

**Solution:**
1. **Find and stop the conflicting service:**
   ```bash
   lsof -i :3000
   # Common culprits: Node.js dev servers, React apps
   ```

2. **Or change the MCP Gateway port:**
   ```yaml
   services:
     mcp-gateway:
       ports:
         - "3001:3000"  # Use different external port
   ```

### 3. Model Download Issues

#### Issue: "Model download failed" or "Connection timeout"

**Cause:** Network issues or insufficient disk space.

**Solution:**
1. **Check internet connection:**
   ```bash
   ping google.com
   ```

2. **Check disk space:**
   ```bash
   df -h
   ```

3. **Retry with smaller model:**
   ```bash
   docker compose exec model-runner ollama pull llama3.2:1b
   ```

4. **Use manual download:**
   ```bash
   # Download directly
   docker compose exec model-runner ollama pull llama3.2:1b --verbose
   ```

5. **Skip model download and use API:**
   - Modify compose file to use OpenAI API instead
   - See Module 4 for cloud model configuration

#### Issue: "Model loading is slow"

**Cause:** Insufficient RAM or CPU resources.

**Solution:**
1. **Increase Docker Desktop resources:**
   - Open Docker Desktop Settings
   - Go to Resources → Advanced
   - Increase Memory to 8GB minimum
   - Increase CPU cores to 4 minimum

2. **Use smaller model:**
   ```bash
   docker compose exec model-runner ollama pull llama3.2:1b
   ```

3. **Close other applications to free resources**

### 4. MCP Gateway Issues

#### Issue: "MCP Gateway health check failed"

**Cause:** Gateway service not starting properly.

**Solution:**
1. **Check container logs:**
   ```bash
   docker compose logs mcp-gateway
   ```

2. **Common fixes:**
   ```bash
   # Restart the service
   docker compose restart mcp-gateway
   
   # Rebuild if needed
   docker compose up -d --force-recreate mcp-gateway
   ```

3. **Verify configuration:**
   ```bash
   # Check environment variables
   docker compose exec mcp-gateway env | grep MCP
   ```

#### Issue: "MCP tools not responding"

**Cause:** Tool servers not properly configured.

**Solution:**
1. **Check available tools:**
   ```bash
   curl http://localhost:3000/tools
   ```

2. **Test individual tools:**
   ```bash
   curl -X POST http://localhost:3000/tools/search \
     -H "Content-Type: application/json" \
     -d '{"query": "test", "limit": 1}'
   ```

3. **Restart with clean state:**
   ```bash
   docker compose down
   docker compose up -d
   ```

### 5. Docker Compose Issues

#### Issue: "docker-compose: command not found"

**Cause:** Using old Docker Compose v1 syntax.

**Solution:**
1. **Use Docker Compose v2 syntax:**
   ```bash
   # Instead of: docker-compose up
   docker compose up
   ```

2. **Update Docker Desktop to latest version**

#### Issue: "Service 'X' failed to build"

**Cause:** Build context or Dockerfile issues.

**Solution:**
1. **Check build logs:**
   ```bash
   docker compose build --no-cache
   ```

2. **Pull pre-built images instead:**
   ```bash
   docker compose pull
   docker compose up -d
   ```

### 6. File Permission Issues

#### Issue: "Permission denied" when accessing files

**Cause:** File ownership or permission problems.

**Solution:**
1. **Fix file permissions:**
   ```bash
   chmod +x scripts/*.sh
   ```

2. **Fix ownership (Linux/Mac):**
   ```bash
   sudo chown -R $USER:$USER .
   ```

3. **For Windows with WSL:**
   ```bash
   # Ensure files are in WSL filesystem, not Windows mount
   cp -r /mnt/c/path/to/workshop ~/workshop
   cd ~/workshop
   ```

### 7. Resource Issues

#### Issue: "Out of memory" or containers keep restarting

**Cause:** Insufficient system resources.

**Solution:**
1. **Increase Docker Desktop memory:**
   - Settings → Resources → Advanced
   - Set Memory to 8GB minimum

2. **Close other applications**

3. **Use resource limits:**
   ```yaml
   services:
     model-runner:
       deploy:
         resources:
           limits:
             memory: 4G
           reservations:
             memory: 2G
   ```

#### Issue: "No space left on device"

**Cause:** Insufficient disk space.

**Solution:**
1. **Clean up Docker:**
   ```bash
   docker system prune -a
   docker volume prune
   ```

2. **Check disk usage:**
   ```bash
   df -h
   docker system df
   ```

3. **Free up space and retry**

### 8. Network Issues

#### Issue: "Services can't communicate"

**Cause:** Network configuration problems.

**Solution:**
1. **Check network:**
   ```bash
   docker network ls
   docker network inspect workshop-network
   ```

2. **Recreate network:**
   ```bash
   docker compose down
   docker network rm workshop-network
   docker compose up -d
   ```

3. **Test connectivity:**
   ```bash
   docker compose exec model-runner ping mcp-gateway
   ```

### 9. Environment-Specific Issues

#### Windows-Specific Issues

**Issue: Line ending problems**
```bash
# Fix line endings
git config --global core.autocrlf true
```

**Issue: Path problems**
```bash
# Use WSL2 for better compatibility
wsl --set-default-version 2
```

#### macOS-Specific Issues

**Issue: Docker Desktop not starting**
```bash
# Reset Docker Desktop
# Docker Desktop → Troubleshoot → Reset to factory defaults
```

#### Linux-Specific Issues

**Issue: Docker service not starting**
```bash
sudo systemctl status docker
sudo systemctl start docker
```

## Advanced Troubleshooting

### Complete Environment Reset

If all else fails, reset everything:

```bash
# Stop all containers
docker compose down

# Remove all workshop containers
docker container prune -f

# Remove all workshop images
docker image prune -a -f

# Remove all volumes
docker volume prune -f

# Remove all networks
docker network prune -f

# Re-run setup
./scripts/setup-environment.sh
```

### Debug Mode

Run services in debug mode:

```bash
# Start with verbose logging
docker compose up --verbose

# Or start individual services
docker compose up model-runner --no-deps
```

### Container Shell Access

Access container for debugging:

```bash
# Access model runner
docker compose exec model-runner sh

# Access MCP gateway
docker compose exec mcp-gateway sh

# Check processes
docker compose exec model-runner ps aux
```

## Getting Help

### Self-Help Checklist

Before asking for help, try:

1. ✅ Run the diagnosis script
2. ✅ Check container logs: `docker compose logs`
3. ✅ Verify all ports are available
4. ✅ Ensure sufficient disk space and memory
5. ✅ Try restarting Docker Desktop
6. ✅ Try the complete environment reset

### When to Ask for Help

Ask for assistance if:
- Error persists after trying solutions above
- System-specific issues not covered here
- Hardware compatibility problems
- Network/firewall restrictions

### Information to Provide

When asking for help, include:
- Output of `./scripts/diagnose-environment.sh`
- Specific error messages
- Operating system and version
- Docker Desktop version
- Steps you've already tried

## Prevention Tips

### Best Practices

1. **Keep Docker Desktop updated**
2. **Allocate sufficient resources (8GB RAM minimum)**
3. **Regularly clean up Docker resources**
4. **Use stable internet connection for downloads**
5. **Close unnecessary applications during workshop**

### Regular Maintenance

```bash
# Weekly cleanup
docker system prune -f
docker volume prune -f

# Check resource usage
docker system df
```

This troubleshooting guide should help you resolve most common issues. Remember, the workshop is designed to be resilient, so don't hesitate to reset and start fresh if needed!