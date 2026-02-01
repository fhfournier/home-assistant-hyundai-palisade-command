ARG BUILD_FROM
FROM $BUILD_FROM

# Install Python
RUN apk add --no-cache python3 py3-pip

# Set working directory
WORKDIR /app

# Copy application
COPY rootfs/app/server.py /app/server.py

# Install Python dependencies with pip
RUN pip3 install --no-cache-dir \
    hyundai-kia-connect-api \
    cloudscraper \
    flask \
    requests

# Create data directory
RUN mkdir -p /data

# Expose port
EXPOSE 8099

# Start server
CMD ["python3", "/app/server.py"]
