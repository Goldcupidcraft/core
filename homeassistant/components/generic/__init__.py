Skip to content
Search or jump to…
Pull requests
Issues
Marketplace
Explore
 
@Goldcupidcraft 
home-assistant
/
core
Public
Code
Issues
1.6k
Pull requests
488
Actions
Projects
2
Security
Insights
core/homeassistant/components/generic/__init__.py /
@davet2001
davet2001 Remove invalid unique id from generic camera (#70568)
…
Latest commit d00d823 on 28 Apr
 History
 4 contributors
@bdraco@davet2001@Swamp-Ig@slovdahl
 48 lines (32 sloc)  1.62 KB

"""The generic component."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er

DOMAIN = "generic"
PLATFORMS = [Platform.CAMERA]


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def _async_migrate_unique_ids(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Migrate entities to the new unique id."""

    @callback
    def _async_migrator(entity_entry: er.RegistryEntry) -> dict[str, Any] | None:
        if entity_entry.unique_id == entry.entry_id:
            # Already correct, nothing to do
            return None
        # There is only one entity, and its unique id
        # should always be the same as the config entry entry_id
        return {"new_unique_id": entry.entry_id}

    await er.async_migrate_entries(hass, entry.entry_id, _async_migrator)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up generic IP camera from a config entry."""

    await _async_migrate_unique_ids(hass, entry)
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
Footer
© 2022 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
Release 2022.6.7 · home-assistant/corecore/__init__.py at 2022.6.7 · home-assistant/core
