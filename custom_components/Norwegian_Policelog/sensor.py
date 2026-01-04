import logging
import urllib.parse
from datetime import datetime, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)

async def async_setup_entry(hass, config_entry, async_add_entities):
    district = config_entry.data.get("district")
    municipality = config_entry.data.get("municipality", "").strip()

    district_encoded = urllib.parse.quote(district)
    municipality_encoded = urllib.parse.quote(municipality) if municipality else ""

    api_url = f"https://api.politiet.no/politiloggen/v1/message?Districts={district_encoded}"
    if municipality_encoded:
        api_url += f"&Municipalities={municipality_encoded}"

    async_add_entities(
        [PoliceLogSensor(hass, api_url, district, municipality)],
        update_before_add=True,
    )


class PoliceLogSensor(SensorEntity):
    _attr_icon = "mdi:police-station"

    def __init__(self, hass, api_url, district, municipality):
        self.hass = hass
        self._api_url = api_url
        self._district = district
        self._municipality = municipality
        self._last_event_id = None
        self._event = None

        name = f"Police Log {district}"
        if municipality:
            name += f" {municipality}"

        self._attr_name = name
        self._attr_unique_id = (
            f"policelog_{district}_{municipality}".lower().replace(" ", "_")
        )

    @property
    def native_value(self):
        """Short state (ALWAYS < 255 chars)"""
        if not self._event:
            return "No data"
        return self._event.get("published", "Updated")

    @property
    def extra_state_attributes(self):
        if not self._event:
            return {}

        return {
            "text": self._event.get("text"),
            "published": self._event.get("published"),
            "id": self._event.get("id"),
            "district": self._district,
            "municipality": self._municipality,
            "last_updated": datetime.utcnow().isoformat(),
        }

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        session = async_get_clientsession(self.hass)

        try:
            async with session.get(self._api_url, timeout=10) as resp:
                resp.raise_for_status()
                data = await resp.json()

            event = data.get("data")
            if not event:
                _LOGGER.debug("No police log data returned")
                return

            event_id = event.get("id")
            if event_id != self._last_event_id:
                self._last_event_id = event_id
                self._event = event
                _LOGGER.debug("New police log event received")

        except Exception as err:
            _LOGGER.error("Failed to update police log: %s", err)
