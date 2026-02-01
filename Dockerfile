ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python and UV
RUN apk add --no-cache \
    python3 \
    py3-pip \
    libstdc++ \
    ca-certificates \
    && pip3 install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml /app/pyproject.toml
COPY rootfs/app/server.py /app/server.py

# Install dependencies with UV
RUN uv pip install --system --no-cache \
    hyundai-kia-connect-api \
    cloudscraper \
    flask \
    requests

# Create data directory for Home Assistant config
RUN mkdir -p /data

# Expose port
EXPOSE 8099

# Launch server
CMD ["python3", "/app/server.py"]
