import aiohttp
import asyncio
import logging

from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.exceptions import PlatformNotReady

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ubertrac api"

async def async_setup(hass, config):
    """Set up your integration based on configuration.yaml."""
    conf = config[DOMAIN]
    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD)
    device_id = conf.get('device_id')

    if not username or not password or not device_id:
        _LOGGER.error("Username, password, and device ID are required.")
        return False

    # Fixed domain as per your new setup
    domain = "http://ubertrac.co.za"

    session = async_get_clientsession(hass)
    token = await get_jwt_token(session, domain, username, password)
    if not token:
        raise PlatformNotReady("Failed to retrieve JWT token.")

    # Storing token and device ID for use in other components like sensors
    hass.data[DOMAIN] = {
        'token': token,
        'device_id': device_id
    }

    # Load the sensor platform and pass the token and device_id
    hass.async_create_task(
        hass.helpers.discovery.load_platform('sensor', DOMAIN, {
            'token': token, 'device_id': device_id
        }, config)
    )
    
    return True

async def get_jwt_token(session, domain, username, password):
    """Log in asynchronously and return the JWT token."""
    login_url = f"{domain}/api/auth/login"
    login_credentials = {"username": username, "password": password}
    headers = {"Content-Type": "application/json"}

    async with session.post(login_url, json=login_credentials, headers=headers) as response:
        if response.status == 200:
            response_data = await response.json()
            return response_data.get('token')
        else:
            response_data = await response.json()
            _LOGGER.error(f"Failed to login, status code: {response.status}, message: {response_data}")
            return None
