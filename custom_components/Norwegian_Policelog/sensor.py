import asyncio
from datetime import timedelta
import logging

import aiohttp
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = timedelta(seconds=120)
API_URL = "https://api.politiet.no/politiloggen/v1/message"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    districts = entry.data.get("districts", [])
    coordinator = NorwegianPolicelogCoordinator(hass, districts)
    await coordinator.async_config_entry_first_refresh()

    sensors = [NorwegianPolicelogSensor(coordinator, district) for district in districts]
    async_add_entities(sensors)

class NorwegianPolicelogCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, districts):
        super().__init__(
            hass,
            _LOGGER,
            name="Norwegian Policelog",
            update_interval=UPDATE_INTERVAL
        )
        self.districts = districts
        self.data = {district: None for district in districts}

    async def _async_update_data(self):
        async with aiohttp.ClientSession() as session:
            for district in self.districts:
                params = {"Districts": district}
                try:
                    async with session.get(API_URL, params=params) as resp:
                        if resp.status != 200:
                            raise UpdateFailed(f"Error fetching data: {resp.status}")
                        result = await resp.json()
                        text = result.get("data", {}).get("text", "")
                        # truncate to 200 chars
                        if len(text) > 200:
                            text = text[:200]
                        self.data[district] = text
                except Exception as err:
                    raise UpdateFailed(f"Error fetching data for {district}: {err}")
        return self.data

class NorwegianPolicelogSensor(Entity):
    def __init__(self, coordinator: NorwegianPolicelogCoordinator, district: str):
        self.coordinator = coordinator
        self.district = district
        self._attr_name = f"Norwegian Policelog {district}"
        self._attr_unique_id = f"norwegian_policelog_{district.lower()}"
        self._attr_icon = "mdi:police-badge"  # <-- set your MDI icon here

    @property
    def state(self):
        return self.coordinator.data.get(self.district)

    @property
    def available(self):
        return self.coordinator.data.get(self.district) is not None

    async def async_update(self):
        await self.coordinator.async_request_refresh()
