import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
import aiohttp
import logging

from .const import DOMAIN  # Ensure DOMAIN is defined in your constants file

_LOGGER = logging.getLogger(__name__)

class YourComponentConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for your_component."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLLING

    async def validate_input(self, hass, data):
        """Validate the user input allows us to connect."""
        username = data[CONF_USERNAME]
        password = data[CONF_PASSWORD]
        domain = "http://ubertrac.co.za"  # Use your fixed domain here

        session = async_get_clientsession(hass)
        try:
            token = await get_jwt_token(session, domain, username, password)
            if not token:
                raise Exception("Failed to log in with provided credentials")
            return {"title": username}  # Use the username as entry title
        finally:
            await session.close()

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

        DATA_SCHEMA = vol.Schema({
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
        })

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
