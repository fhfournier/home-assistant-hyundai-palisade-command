# Use UV for fast Python dependency installation
FROM ghcr.io/astral-sh/uv:python3.12-alpine

# Install system dependencies
RUN apk add --no-cache \
    libstdc++ \
    ca-certificates

# Set working directory
WORKDIR /app

# Copy project configuration
COPY pyproject.toml /app/pyproject.toml

# Copy application files
COPY rootfs/app/server.py /app/server.py

# Sync dependencies using UV (creates .venv and installs everything)
RUN uv sync --no-dev --frozen

# Create data directory for Home Assistant config
RUN mkdir -p /data

# Expose port
EXPOSE 8099

# Launch server using UV run (uses the .venv created by uv sync)
CMD ["uv", "run", "python", "server.py"]
