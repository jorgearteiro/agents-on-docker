FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y build-essential cmake ninja-build git && \
    rm -rf /var/lib/apt/lists/*
RUN pip install uv

WORKDIR /app
COPY pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy \
    uv pip install --system .

COPY agent.py .

COPY <<EOF /entrypoint.sh
#!/bin/sh

if test -f /run/secrets/openai-api-key; then
    export OPENAI_API_KEY=\$(cat /run/secrets/openai-api-key)
fi

if test -n "\${OPENAI_API_KEY}"; then
    echo "Using OpenAI with \${OPENAI_MODEL_NAME}"
else
    echo "Using Docker Model Runner with \${MODEL_RUNNER_MODEL}"
    export OPENAI_BASE_URL=\${MODEL_RUNNER_URL}
    export OPENAI_API_KEY=sk-insecure
fi

exec python -u /app/agent.py
EOF

RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
