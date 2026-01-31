# Hyundai Bluelink Control Add-on

![Logo](https://brands.home-assistant.io/hyundai_bluelink/icon.png)

Control your Hyundai or Kia vehicle directly from Home Assistant!

## About

This add-on provides a REST API server that allows you to control your Hyundai Bluelink or Kia UVO connected vehicle:

- 🚗 **Remote Start/Stop** with climate control
- 🔒 **Lock/Unlock** doors
- 📊 **Vehicle Status** (odometer, temperature, lock status, etc.)
- 🔄 **Auto-refresh** vehicle data

## Installation

### Step 1: Add this repository to Home Assistant

1. Navigate to **Settings** > **Add-ons** > **Add-on Store**
2. Click the **⋮** menu (top right) > **Repositories**
3. Add this repository URL (once you host it on GitHub)
4. Click **Add** > **Close**

### Step 2: Install the Add-on

1. Find **Hyundai Bluelink Control** in the add-on store
2. Click **Install**
3. Wait for installation to complete

### Step 3: Configure

1. Go to the **Configuration** tab
2. Fill in your credentials:
   - **username**: Your Bluelink/UVO email
   - **password**: Your Bluelink/UVO password
   - **pin**: Your 4-digit PIN
   - **vehicle_id**: Your vehicle ID (get from status command)
   - **region**: US, Canada, or Europe
   - **brand**: Hyundai or Kia
   - **port**: 8099 (default)

3. Save the configuration

### Step 4: Start the Add-on

1. Go to the **Info** tab
2. Click **Start**
3. Enable **Start on boot** (optional)
4. Check the **Logs** tab to verify it's running

## Configuration

Example configuration:

```yaml
username: "your-email@example.com"
password: "your-password"
pin: "1234"
vehicle_id: "your-vehicle-id"
region: "Canada"
brand: "Hyundai"
port: 8099
```

## Getting Your Vehicle ID

You need to get your vehicle ID first. You can use the original Python script to get it:

```bash
uv run src/026_homeassistant_car/control.py status
```

Look for the key in the JSON response (e.g., `KYCcaLX6zxRlJkuYt545bA==`).

## Home Assistant Integration

Once the add-on is running, add this to your `configuration.yaml`:

```yaml
rest_command:
  car_start:
    url: "http://localhost:8099/start"
    method: POST

  car_stop:
    url: "http://localhost:8099/stop"
    method: POST

  car_lock:
    url: "http://localhost:8099/lock"
    method: POST

  car_unlock:
    url: "http://localhost:8099/unlock"
    method: POST

sensor:
  - platform: rest
    name: "Vehicle Status"
    resource: "http://localhost:8099/status"
    scan_interval: 1800 # 30 minutes
    json_attributes:
      - name
      - model
      - odometer
      - is_locked
      - is_engine_running
      - air_temperature
    value_template: "{{ value_json.model }}"
```

Restart Home Assistant after adding the configuration.

## Dashboard

Add this card to your dashboard:

```yaml
type: entities
title: 🚗 My Hyundai
entities:
  - entity: sensor.vehicle_status
  - type: button
    name: Start Car
    action_name: START
    tap_action:
      action: call-service
      service: rest_command.car_start
  - type: button
    name: Stop Car
    action_name: STOP
    tap_action:
      action: call-service
      service: rest_command.car_stop
  - type: button
    name: Lock
    action_name: LOCK
    tap_action:
      action: call-service
      service: rest_command.car_lock
  - type: button
    name: Unlock
    action_name: UNLOCK
    tap_action:
      action: call-service
      service: rest_command.car_unlock
```

## API Endpoints

The add-on exposes the following REST API endpoints:

- `GET /health` - Health check
- `GET /status` - Get vehicle status
- `POST /start` - Start vehicle with climate
- `POST /stop` - Stop vehicle
- `POST /lock` - Lock doors
- `POST /unlock` - Unlock doors

## Support

For issues and questions, please open an issue on GitHub.

## Credits

This add-on uses the [hyundai-kia-connect-api](https://github.com/Hyundai-Kia-Connect/hyundai_kia_connect_api) library.
