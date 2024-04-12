import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD, CONF_DOMAIN
import aiohttp
import logging

from .const import DOMAIN  # Make sure to define your domain as a constant in a const.py or similar

_LOGGER = logging.getLogger(__name__)

class YourComponentConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for your_component."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLLING

    async def validate_input(self, hass, data):
        """Validate the user input allows us to connect.

        Data has the keys from DATA_SCHEMA with values provided by the user.
        """
        # Replace this with your method to validate input
        username = data[CONF_USERNAME]
        password = data[CONF_PASSWORD]
        domain = data[CONF_DOMAIN]

        session = aiohttp.ClientSession()
        token = await get_jwt_token(session, domain, username, password)
        session.close()

        if not token:
            raise Exception("Failed to log in with provided credentials")

        return {"title": "Your Component"}

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)

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

        # This is the schema for the form shown in the UI
        DATA_SCHEMA = vol.Schema({
            vol.Required(CONF_DOMAIN): str,
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options."""

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(CONF_DOMAIN): str,
                vol.Optional(CONF_USERNAME): str,
                vol.Optional(CONF_PASSWORD): str,
            })
        )
