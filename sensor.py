"""Sensor platform for Alephium Price."""
import asyncio
import logging
from datetime import timedelta
import aiohttp
import async_timeout

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    API_ENDPOINT,
    UPDATE_INTERVAL,
    ATTR_PRICE,
    ATTR_PRICE_YESTERDAY,
    ATTR_VOLUME_YESTERDAY,
    ATTR_SYMBOL,
    ATTR_NAME,
    ATTR_BLOCKCHAIN,
    ATTR_DATA_SOURCE,
    ATTR_LAST_UPDATED,
    ATTR_COLOR,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Alephium Price sensor based on a config entry."""
    coordinator = AlephiumPriceCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([AlephiumPriceSensor(coordinator)], True)


class AlephiumPriceCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Alephium price data."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the data coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self.session = aiohttp.ClientSession()

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            async with async_timeout.timeout(10):
                response = await self.session.get(API_ENDPOINT)
                data = await response.json()
                return {
                    ATTR_PRICE: data.get("Price", 0),
                    ATTR_PRICE_YESTERDAY: data.get("PriceYesterday", 0),
                    ATTR_VOLUME_YESTERDAY: data.get("VolumeYesterdayUSD", 0),
                    ATTR_SYMBOL: data.get("Symbol", "ALPH"),
                    ATTR_NAME: data.get("Name", "Alephium"),
                    ATTR_BLOCKCHAIN: data.get("Blockchain", "Alephium"),
                    ATTR_DATA_SOURCE: data.get("Source", "diadata.org"),
                    ATTR_LAST_UPDATED: data.get("Time", ""),
                }
        except (asyncio.TimeoutError, aiohttp.ClientError) as error:
            raise UpdateFailed(f"Error fetching data: {error}") from error


def get_price_change_color(current_price, yesterday_price):
    """Calculate color based on price change percentage.
    
    - Blue to red gradient when price decreased (red at 2% decrease)
    - Blue to green gradient when price increased (green at 2% increase)
    """
    if not current_price or not yesterday_price or yesterday_price == 0:
        return "#0000FF"  # Default blue
    
    # Calculate percentage change
    percent_change = ((current_price - yesterday_price) / yesterday_price) * 100
    
    # Clamp the change to max +/- 2%
    clamped_change = max(min(percent_change, 2), -2)
    
    if percent_change < 0:
        # Negative change: blue to red gradient
        # Map from -2% to 0% to a 0-1 scale
        intensity = min(abs(clamped_change) / 2, 1)
        # Generate color: As intensity increases, move from blue to red
        red = int(255 * intensity)
        blue = int(255 * (1 - intensity))
        return f"#{red:02x}00{blue:02x}"
    else:
        # Positive change: blue to green gradient
        # Map from 0% to 2% to a 0-1 scale
        intensity = min(clamped_change / 2, 1)
        # Generate color: As intensity increases, move from blue to green
        green = int(255 * intensity)
        blue = int(255 * (1 - intensity))
        return f"#00{green:02x}{blue:02x}"


class AlephiumPriceSensor(SensorEntity):
    """Representation of a Alephium Price sensor."""

    def __init__(self, coordinator: AlephiumPriceCoordinator) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}_price"
        self._attr_name = "Alephium Price"
        self._attr_icon = "mdi:currency-usd"
        self._attr_native_unit_of_measurement = "USD"
        self._attr_suggested_display_precision = 3

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get(ATTR_PRICE)
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
            
        current_price = self.coordinator.data.get(ATTR_PRICE, 0)
        yesterday_price = self.coordinator.data.get(ATTR_PRICE_YESTERDAY, 0)
        
        return {
            ATTR_PRICE_YESTERDAY: yesterday_price,
            ATTR_VOLUME_YESTERDAY: self.coordinator.data.get(ATTR_VOLUME_YESTERDAY),
            ATTR_SYMBOL: self.coordinator.data.get(ATTR_SYMBOL),
            ATTR_NAME: self.coordinator.data.get(ATTR_NAME),
            ATTR_BLOCKCHAIN: self.coordinator.data.get(ATTR_BLOCKCHAIN),
            ATTR_DATA_SOURCE: self.coordinator.data.get(ATTR_DATA_SOURCE),
            ATTR_LAST_UPDATED: self.coordinator.data.get(ATTR_LAST_UPDATED),
            ATTR_COLOR: get_price_change_color(current_price, yesterday_price),
        }

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self) -> None:
        """Update the entity."""
        await self.coordinator.async_request_refresh() 