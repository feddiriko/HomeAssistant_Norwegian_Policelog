import logging
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    _LOGGER.info("Police log integration setup via UI")
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
