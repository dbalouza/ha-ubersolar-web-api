import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
import aiohttp
import logging

from .const import DOMAIN  # Ensure DOMAIN is defined in your constants

_LOGGER = logging.getLogger(__name__)

class YourComponentConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for your_component."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLLING

    async def validate_input(self, hass, data):
        """Validate the user input allows us to connect."""
        username = data['username']
        password = data['password']
        device_id = data['device_id']
        domain = "http://ubertrac.co.za"  # Static domain

        # Use an aiohttp session from Home Assistant's session pool
        session = hass.helpers.aiohttp_client.async_get_clientsession()

        # Assuming get_jwt_token is adjusted to be an async function
        try:
            token = await get_jwt_token(session, domain, username, password)
            if not token:
                raise Exception("Failed to log in with provided credentials")
            # Optionally validate the device ID here if necessary
            return {"title": username, "device_id": device_id}  # Use the username and device_id as entry title
        finally:
            await session.close()

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        errors = {}

        if user_input is not None:
            try:
                info = await self.validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except Exception as e:
                _LOGGER.error(f"Exception: {e}")
                errors['base'] = 'auth'

        DATA_SCHEMA = vol.Schema({
            vol.Required('username'): str,
            vol.Required('password'): str,
            vol.Required('device_id'): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

# If you have options flow
@callback
def async_get_options_flow(config_entry):
    return OptionsFlow(config_entry)

class OptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional('device_id', default=options.get('device_id')): str,
            })
        )
