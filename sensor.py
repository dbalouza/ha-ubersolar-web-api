from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_DEVICE_ID

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    token = hass.data[DOMAIN]['token']
    device_id = hass.data[DOMAIN]['device_id']
    async_add_entities([YourCustomSensor(token, device_id)], True)

class YourCustomSensor(Entity):
    def __init__(self, token, device_id):
        """Initialize the sensor."""
        self._state = None
        self.token = token
        self.device_id = device_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Device {self.device_id} Sensor"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor."""
        self._state = await fetch_telemetry_data(self.token, self.device_id)
