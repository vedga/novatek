"""Novatek-Electro devices integration."""
import logging
from datetime import timedelta

import voluptuous as vol
from homeassistant.components.binary_sensor import DEVICE_CLASSES
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_DEVICES, \
    CONF_NAME, CONF_DEVICE_CLASS, EVENT_HOMEASSISTANT_STOP, CONF_MODE, \
    CONF_SCAN_INTERVAL, CONF_FORCE_UPDATE, CONF_EXCLUDE, CONF_SENSORS, \
    CONF_TIMEOUT, CONF_PAYLOAD_OFF
from homeassistant.core import ServiceCall
from homeassistant.helpers import config_validation as cv, discovery
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import HomeAssistantType

from .registry import NovatekRegistry
from . import novatek

DOMAIN = 'novatek'

CONF_DEBUG = 'debug'

_LOGGER = logging.getLogger(__name__)


CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_DEVICES): {
            cv.string: vol.Schema({
                vol.Required(CONF_HOST): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
                vol.Optional(CONF_NAME): cv.string,
                vol.Optional(CONF_DEVICE_CLASS): vol.Any(str, list),
                vol.Optional(CONF_FORCE_UPDATE): cv.boolean
            }, extra=vol.ALLOW_EXTRA),
        },
        vol.Optional(CONF_SCAN_INTERVAL): cv.time_period,
        vol.Optional(CONF_FORCE_UPDATE): cv.ensure_list,
        vol.Optional(CONF_SENSORS): cv.ensure_list,
        vol.Optional(CONF_DEBUG, default=False): cv.boolean
    }, extra=vol.ALLOW_EXTRA),
}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass: HomeAssistantType, hass_config: dict):
    # Device registry
    hass.data[DOMAIN] = registry = NovatekRegistry()

    config = hass_config[DOMAIN]

    # init debug if needed
    if config[CONF_DEBUG]:
        info = await hass.helpers.system_info.async_get_system_info()
        info.pop('installation_type', None)  # fix HA v0.109.6
        info.pop('timezone')
        _LOGGER.debug(f"SysInfo: {info}")

    # create sensors
    if CONF_DEVICES in config:
        for k, v in config[CONF_DEVICES].items():
            v['name'] = k
            device = await hass.async_add_executor_job(lambda: novatek.NovatekElectro(v[CONF_HOST],v[CONF_PASSWORD]))
            registry.Add(k, device)
            hass.async_create_task(discovery.async_load_platform(
                hass, 'sensor', DOMAIN, v, hass_config))

    return True
