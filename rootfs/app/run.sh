#!/usr/bin/with-contenv bashio

# Start the Python Flask server
bashio::log.info "Starting Hyundai Bluelink Control Service..."

# Get config from add-on options
export BLUELINK_USERNAME=$(bashio::config 'username')
export BLUELINK_PASSWORD=$(bashio::config 'password')
export BLUELINK_PIN=$(bashio::config 'pin')
export BLUELINK_VEHICLE_ID=$(bashio::config 'vehicle_id')
export BLUELINK_REGION=$(bashio::config 'region')
export BLUELINK_BRAND=$(bashio::config 'brand')
export BLUELINK_PORT=$(bashio::config 'port')

bashio::log.info "Configuration loaded for user: ${BLUELINK_USERNAME}"

# Start the Flask API server
cd /app
python3 server.py
