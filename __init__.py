import aiohttp
import asyncio
import logging

from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_DOMAIN
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

DOMAIN = "your_component"

async def async_setup(hass, config):
    """Set up your integration."""
    conf = config[DOMAIN]
    username = conf[CONF_USERNAME]
    password = conf[CONF_PASSWORD]
    domain = conf[CONF_DOMAIN]

    session = async_get_clientsession(hass)
    token = await get_jwt_token(session, domain, username, password)
    hass.data[DOMAIN] = {'token': token}

    hass.async_create_task(
        hass.helpers.discovery.load_platform('sensor', DOMAIN, {}, config)
    )
    
    return True

async def get_jwt_token(session, domain, username, password):
    """Log in asynchronously and return the JWT token."""
    login_url = f"{domain}/api/auth/login"
    login_credentials = {"username": username, "password": password}
    headers = {"Content-Type": "application/json"}

    async with session.post(login_url, json=login_credentials, headers=headers) as response:
        response_data = await response.json()
        if response.status_code == 200:
            return response_data['token']
        else:
            _LOGGER.error(f"Failed to login, status code: {response.status_code}, message: {response_data}")
            return None
