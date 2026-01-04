import logging
from homeassistant import config_entries
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

DOMAIN = "norwegian_policelog"

class PoliceLogConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=f"Police Log {user_input['district']}",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("district", default="Oslo"): str,
                    vol.Optional("municipality", default=""): str,
                }
            ),
        )
