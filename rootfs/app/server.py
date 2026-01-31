"""
Flask API Server for Hyundai Bluelink Control
Runs as a Home Assistant Add-on
"""

import os
import sys
import json
import logging
from flask import Flask, jsonify, request
import requests
import cloudscraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Monkey patch for Cloudflare bypass
class PatchedSession(cloudscraper.CloudScraper):
    def request(self, method, url, *args, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        response = super().request(method, url, *args, **kwargs)
        if response.status_code == 403:
            logger.warning("403 Forbidden - Cloudflare might be blocking")
        return response

requests.Session = PatchedSession

# Import after patching
from hyundai_kia_connect_api import VehicleManager
from hyundai_kia_connect_api import const
from hyundai_kia_connect_api import ClimateRequestOptions

# Flask app
app = Flask(__name__)

# Load configuration from Home Assistant options.json
def load_config():
    """Load configuration from Home Assistant add-on options"""
    config_file = '/data/options.json'
    
    # Fallback to environment variables (for testing)
    if not os.path.exists(config_file):
        logger.warning(f"{config_file} not found, using environment variables")
        return {
            'username': os.environ.get('BLUELINK_USERNAME'),
            'password': os.environ.get('BLUELINK_PASSWORD'),
            'pin': os.environ.get('BLUELINK_PIN'),
            'vehicle_id': os.environ.get('BLUELINK_VEHICLE_ID'),
            'region': os.environ.get('BLUELINK_REGION', 'Canada'),
            'brand': os.environ.get('BLUELINK_BRAND', 'Hyundai'),
            'port': int(os.environ.get('BLUELINK_PORT', 8099))
        }
    
    # Load from options.json
    with open(config_file, 'r') as f:
        options = json.load(f)
    
    return {
        'username': options.get('username'),
        'password': options.get('password'),
        'pin': options.get('pin'),
        'vehicle_id': options.get('vehicle_id'),
        'region': options.get('region', 'Canada'),
        'brand': options.get('brand', 'Hyundai'),
        'port': int(options.get('port', 8099))
    }

CONFIG = load_config()

# Validate config
if not all([CONFIG['username'], CONFIG['password'], CONFIG['vehicle_id']]):
    logger.error("Missing required configuration. Please configure the add-on.")
    sys.exit(1)

logger.info(f"Configuration loaded for {CONFIG['username']}")

# Global vehicle manager (cached)
_vm_cache = None

def get_vehicle_manager():
    """Get or create VehicleManager instance"""
    global _vm_cache
    
    if _vm_cache is not None:
        return _vm_cache
    
    try:
        # Map region string to ID
        region_map = {
            'US': const.REGION_USA,
            'Canada': const.REGION_CANADA,
            'Europe': const.REGION_EUROPE
        }
        region_str = region_map.get(CONFIG['region'], const.REGION_CANADA)
        region_id = next(k for k, v in const.REGIONS.items() if v == region_str)
        
        # Map brand string to ID
        brand_map = {
            'Hyundai': const.BRAND_HYUNDAI,
            'Kia': const.BRAND_KIA
        }
        brand_str = brand_map.get(CONFIG['brand'], const.BRAND_HYUNDAI)
        brand_id = next(k for k, v in const.BRANDS.items() if v == brand_str)
        
    except StopIteration:
        logger.error("Could not find Region ID or Brand ID")
        return None
    
    vm = VehicleManager(
        region=region_id,
        brand=brand_id,
        username=CONFIG['username'],
        password=CONFIG['password'],
        pin=CONFIG['pin']
    )
    
    try:
        vm.check_and_refresh_token()
        vm.update_all_vehicles_with_cached_state()
        _vm_cache = vm
        logger.info("VehicleManager initialized successfully")
        return vm
    except Exception as e:
        logger.error(f"Failed to initialize VehicleManager: {e}")
        return None


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'hyundai-bluelink'}), 200


@app.route('/status', methods=['GET'])
def get_status():
    """Get vehicle status"""
    vm = get_vehicle_manager()
    if not vm:
        return jsonify({'error': 'Failed to connect to vehicle service'}), 500
    
    try:
        vm.update_all_vehicles_with_cached_state()
        vehicle = vm.vehicles.get(CONFIG['vehicle_id'])
        
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        return jsonify({
            'name': vehicle.name,
            'model': vehicle.model,
            'odometer': vehicle.odometer,
            'is_locked': vehicle.is_locked,
            'is_engine_running': vehicle.engine_is_running,
            'air_temperature': vehicle.air_temperature,
            'last_updated_at': str(vehicle.last_updated_at)
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/start', methods=['POST'])
def start_car():
    """Start the car with climate control"""
    vm = get_vehicle_manager()
    if not vm:
        return jsonify({'error': 'Failed to connect to vehicle service'}), 500
    
    try:
        logger.info("Starting vehicle...")
        
        options = ClimateRequestOptions(
            set_temp=30,
            duration=10,
            defrost=True,
            climate=True,
            heating=1,
            front_left_seat=8,
            front_right_seat=8,
            steering_wheel=1
        )
        
        vm.start_climate(CONFIG['vehicle_id'], options)
        logger.info("✅ Vehicle started successfully")
        
        return jsonify({'status': 'success', 'action': 'start'}), 200
        
    except Exception as e:
        logger.error(f"Error starting vehicle: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/stop', methods=['POST'])
def stop_car():
    """Stop the car"""
    vm = get_vehicle_manager()
    if not vm:
        return jsonify({'error': 'Failed to connect to vehicle service'}), 500
    
    try:
        logger.info("Stopping vehicle...")
        vm.stop_climate(CONFIG['vehicle_id'])
        logger.info("✅ Vehicle stopped successfully")
        
        return jsonify({'status': 'success', 'action': 'stop'}), 200
        
    except Exception as e:
        logger.error(f"Error stopping vehicle: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/lock', methods=['POST'])
def lock_car():
    """Lock the car"""
    vm = get_vehicle_manager()
    if not vm:
        return jsonify({'error': 'Failed to connect to vehicle service'}), 500
    
    try:
        logger.info("Locking vehicle...")
        vm.lock(CONFIG['vehicle_id'])
        logger.info("✅ Vehicle locked successfully")
        
        return jsonify({'status': 'success', 'action': 'lock'}), 200
        
    except Exception as e:
        logger.error(f"Error locking vehicle: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/unlock', methods=['POST'])
def unlock_car():
    """Unlock the car"""
    vm = get_vehicle_manager()
    if not vm:
        return jsonify({'error': 'Failed to connect to vehicle service'}), 500
    
    try:
        logger.info("Unlocking vehicle...")
        vm.unlock(CONFIG['vehicle_id'])
        logger.info("✅ Vehicle unlocked successfully")
        
        return jsonify({'status': 'success', 'action': 'unlock'}), 200
        
    except Exception as e:
        logger.error(f"Error unlocking vehicle: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    logger.info(f"Starting Flask server on port {CONFIG['port']}...")
    app.run(host='0.0.0.0', port=CONFIG['port'], debug=False)
