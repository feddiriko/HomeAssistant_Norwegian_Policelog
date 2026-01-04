"""Norwegian Policelog integration."""
from homeassistant.core import HomeAssistant

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up Norwegian Policelog from a config entry."""
    hass.data.setdefault("norwegian_policelog", {})
    hass.data["norwegian_policelog"][entry.entry_id] = entry.data

    # Await the forwarding so HA knows setup is complete
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, ["sensor"])
    hass.data["norwegian_policelog"].pop(entry.entry_id, None)
    return True
