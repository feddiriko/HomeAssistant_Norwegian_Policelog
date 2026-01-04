import voluptuous as vol
from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv

DISTRICTS = [
    "Oslo", "Øst", "Innlandet", "SørØst", "Agder", "SørVest",
    "Vest", "MøreOgRomsdal", "Trøndelag", "Nordland", "Troms", "Finnmark"
]

class NorwegianPolicelogConfigFlow(config_entries.ConfigFlow, domain="norwegian_policelog"):
    """Config flow for Norwegian Policelog."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            districts = user_input.get("districts")
            if not districts:
                errors["base"] = "no_districts"
                return self.async_show_form(step_id="user", data_schema=self.get_schema(), errors=errors)

            # Filter invalid districts
            valid_districts = [d for d in districts if d in DISTRICTS]
            if not valid_districts:
                errors["base"] = "invalid_districts"
                return self.async_show_form(step_id="user", data_schema=self.get_schema(), errors=errors)

            return self.async_create_entry(
                title="Norwegian Policelog",
                data={"districts": valid_districts}
            )

        # Show the form
        return self.async_show_form(
            step_id="user",
            data_schema=self.get_schema(),
            errors=errors
        )

    @staticmethod
    def get_schema():
        """Return HA-compatible schema with multi-select."""
        return vol.Schema({
            vol.Required("districts", default=["Oslo"]): cv.multi_select(DISTRICTS)
        })
