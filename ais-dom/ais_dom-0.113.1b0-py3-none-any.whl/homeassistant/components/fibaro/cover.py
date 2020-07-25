"""Support for Fibaro cover - curtains, rollershutters etc."""
import logging

from homeassistant.components.cover import (
    ATTR_POSITION,
    ATTR_TILT_POSITION,
    DOMAIN,
    CoverEntity,
)

from . import FIBARO_DEVICES, FibaroDevice

_LOGGER = logging.getLogger(__name__)


# Ais dom
async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Fibaro covers."""
    async_add_entities(
        [FibaroCover(device) for device in hass.data[FIBARO_DEVICES]["cover"]], True
    )


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Fibaro covers."""
    if discovery_info is None:
        return

    add_entities(
        [FibaroCover(device) for device in hass.data[FIBARO_DEVICES]["cover"]], True
    )


class FibaroCover(FibaroDevice, CoverEntity):
    """Representation a Fibaro Cover."""

    def __init__(self, fibaro_device):
        """Initialize the Vera device."""
        super().__init__(fibaro_device)
        self.entity_id = f"{DOMAIN}.{self.ha_id}"

    @staticmethod
    def bound(position):
        """Normalize the position."""
        if position is None:
            return None
        position = int(position)
        if position <= 5:
            return 0
        if position >= 95:
            return 100
        return position

    @property
    def current_cover_position(self):
        """Return current position of cover. 0 is closed, 100 is open."""
        return self.bound(self.level)

    @property
    def current_cover_tilt_position(self):
        """Return the current tilt position for venetian blinds."""
        return self.bound(self.level2)

    def set_cover_position(self, **kwargs):
        """Move the cover to a specific position."""
        self.set_level(kwargs.get(ATTR_POSITION))

    def set_cover_tilt_position(self, **kwargs):
        """Move the cover to a specific position."""
        self.set_level2(kwargs.get(ATTR_TILT_POSITION))

    @property
    def is_closed(self):
        """Return if the cover is closed."""
        if self.current_cover_position is None:
            return None
        return self.current_cover_position == 0

    def open_cover(self, **kwargs):
        """Open the cover."""
        self.action("open")

    def close_cover(self, **kwargs):
        """Close the cover."""
        self.action("close")

    def open_cover_tilt(self, **kwargs):
        """Open the cover tilt."""
        self.set_level2(100)

    def close_cover_tilt(self, **kwargs):
        """Close the cover."""
        self.set_level2(0)

    def stop_cover(self, **kwargs):
        """Stop the cover."""
        self.action("stop")
