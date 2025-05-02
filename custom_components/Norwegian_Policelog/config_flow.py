import logging
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

class PoliceLogConfigFlow(config_entries.ConfigFlow, domain="norwegian_policelog"):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            district = user_input["district"]
            municipality = user_input["municipality"]

            return self.async_create_entry(
                title=f"Police Log {district}",
                data={
                    "district": district,
                    "municipality": municipality
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("district", default="SørVest"): cv.string,
                vol.Optional("municipality", default=""): cv.string,
            })
        )
