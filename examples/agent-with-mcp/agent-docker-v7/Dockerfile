# Basic AI Agent Dockerfile
# This Dockerfile demonstrates best practices for containerizing Python AI agents
# with the Strands SDK and Docker Model Runner integration

# Use Python 3.12 slim image for smaller size and security
# Slim images contain only essential packages, reducing attack surface
FROM python:3.12-slim

# Prevent Python from buffering stdout/stderr
# This ensures logs appear immediately in Docker logs
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for Python packages
# - build-essential: C compiler for native extensions
# - cmake, ninja-build: Build tools for some AI libraries
# - git: Required for some pip installations
# Clean up apt cache to reduce image size
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    ninja-build \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv - a fast Python package installer
# uv is significantly faster than pip for dependency resolution and installation
RUN pip install uv

# Set working directory for the application
# All subsequent commands will run from this directory
WORKDIR /app

# Copy dependency specification and README first (for Docker layer caching)
# This allows Docker to cache the dependency installation step
# if pyproject.toml hasn't changed
COPY pyproject.toml README.md ./

# Install Python dependencies with optimizations
# --mount=type=cache: Cache downloaded packages between builds
# UV_COMPILE_BYTECODE=1: Pre-compile Python files for faster startup
# UV_LINK_MODE=copy: Copy packages instead of linking (more reliable in containers)
# --system: Install packages system-wide (no virtual environment needed in container)
RUN --mount=type=cache,target=/root/.cache/uv \
    UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy \
    uv pip install --system .

# Copy the agent code
# This is done after dependency installation to maximize Docker layer caching
COPY agent.py .

# Create entrypoint script using heredoc syntax
# This script handles automatic model detection and configuration
COPY <<EOF /entrypoint.sh
#!/bin/sh

# Docker Secrets Integration
# Check if OpenAI API key is provided via Docker secrets
# Docker secrets are mounted at /run/secrets/ and are more secure than environment variables
if test -f /run/secrets/openai-api-key; then
    export OPENAI_API_KEY=\$(cat /run/secrets/openai-api-key)
fi

# Automatic Model Detection Logic
# If OpenAI API key is available, use OpenAI models
# Otherwise, fall back to Docker Model Runner with local models
if test -n "\${OPENAI_API_KEY}"; then
    echo "🌐 Using OpenAI model: \${OPENAI_MODEL_NAME:-gpt-4o-mini}"
else
    echo "🏠 Using Docker Model Runner with local model: \${MODEL_RUNNER_MODEL:-ai/qwen3}"
    # Configure OpenAI client to use Docker Model Runner
    export OPENAI_BASE_URL=\${MODEL_RUNNER_URL}
    export OPENAI_API_KEY=sk-insecure  # Dummy key for local models
fi

# Execute the agent with unbuffered output (-u flag)
# exec replaces the shell process, ensuring proper signal handling
exec python -u /app/agent.py
EOF

# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the default command to run the entrypoint script
# This will be executed when the container starts
CMD ["/entrypoint.sh"]
