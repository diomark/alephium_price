"""Platform for Alephium Price sensor component."""
import logging

from homeassistant.helpers.entity_platform import async_get_platforms

from . import DOMAIN
from .sensor import AlephiumPriceCoordinator, AlephiumPriceSensor

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Alephium Price sensor."""
    coordinator = AlephiumPriceCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    
    async_add_entities([AlephiumPriceSensor(coordinator)], True) 