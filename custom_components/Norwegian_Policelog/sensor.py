import logging
import requests
from datetime import timedelta, datetime
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
import urllib.parse

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)

async def async_setup_entry(hass, config_entry, async_add_entities):
    district = config_entry.data.get("district", "SørVest")
    municipality = config_entry.data.get("municipality", "").strip()

    district_encoded = urllib.parse.quote(district)
    municipality_encoded = urllib.parse.quote(municipality) if municipality else ""

    api_url = f"https://api.politiet.no/politiloggen/v1/message?Districts={district_encoded}"
    if municipality_encoded:
        api_url += f"&Municipalities={municipality_encoded}"

    async_add_entities([PoliceLogSensor(api_url, district, municipality)], True)


class PoliceLogSensor(Entity):
    def __init__(self, api_url, district, municipality=None):
        self._api_url = api_url
        self._district = district
        self._municipality = municipality
        self._name = f"Police Log {district} {municipality}" if municipality else f"Police Log {district}"
        self._state = None
        self._data = None
        self._icon = "mdi:police-station"
        self._last_event_id = None
        self._last_updated = None

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        base = f"policelog_{self._district.lower()}"
        if self._municipality:
            base += f"_{self._municipality.lower()}"
        return base.replace(" ", "_")

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return self._icon

    @property
    def extra_state_attributes(self):
        return {
            "log_text": self._data.get("text") if self._data else "No data",
            "published": self._data.get("published") if self._data else None,
            "last_updated": self._last_updated,
        }

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        try:
            response = requests.get(self._api_url, timeout=10)
            response.raise_for_status()
            result = response.json()

            if result and isinstance(result.get("data"), dict):
                event = result["data"]
                event_id = event.get("id")

                if event_id and event_id != self._last_event_id:
                    self._last_event_id = event_id
                    self._data = event
                    self._state = event.get("text", "No information")
                    self._last_updated = datetime.utcnow().isoformat()
                    _LOGGER.debug("New police log event received")
                else:
                    _LOGGER.debug("No new event found")
            else:
                _LOGGER.warning("Invalid or empty response from API")
        except requests.RequestException as e:
            _LOGGER.error("Failed to fetch data: %s", e)
