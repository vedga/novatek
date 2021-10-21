"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components import sensor
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import DEVICE_CLASS_POWER, ELECTRIC_POTENTIAL_VOLT, ELECTRIC_CURRENT_AMPERE, POWER_WATT, ENERGY_WATT_HOUR, FREQUENCY_HERTZ
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import logging
import json

#from . import novatek
from . import DOMAIN

SENSORS = {
    'power': [DEVICE_CLASS_POWER, sensor.STATE_CLASS_MEASUREMENT, POWER_WATT, None],
    'frequency': [DEVICE_CLASS_POWER, None, FREQUENCY_HERTZ, None],
    'energy': [sensor.DEVICE_CLASS_ENERGY, sensor.STATE_CLASS_TOTAL, ENERGY_WATT_HOUR, None],
    'current': [sensor.DEVICE_CLASS_CURRENT, sensor.STATE_CLASS_MEASUREMENT, ELECTRIC_CURRENT_AMPERE, None],
    'voltage': [sensor.DEVICE_CLASS_VOLTAGE, sensor.STATE_CLASS_MEASUREMENT, ELECTRIC_POTENTIAL_VOLT, None]
}

TAG_ACTIVE = 'active'
TAG_FULL = 'full'

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, add_entities,
                               discovery_info=None):
    #_LOGGER.warning(f"novatek: called async_setup_platform()")

    if discovery_info is None:
        return

    #x = json.dumps(discovery_info)
    #_LOGGER.warning(f"novatek: discovery_info {x}")

    #y = json.dumps(config)
    #_LOGGER.warning(f"novatek: config {y}")

    registry = hass.data[DOMAIN]
    if registry is None:
        raise Exception("novatek: Registry must be exist at this point")

    device = registry.Get(discovery_info["name"])
    if device is None:
        raise Exception("novatek: Device must be exist at this point")

    add_entities([VoltageSensor(discovery_info["name"], device),
                  CurrentSensor(discovery_info["name"], device),
                  PowerSensor(discovery_info["name"], device, TAG_ACTIVE),
                  PowerSensor(discovery_info["name"], device, TAG_FULL),
                  EnergySensor(discovery_info["name"], device, TAG_ACTIVE),
                  EnergySensor(discovery_info["name"], device, TAG_FULL),
                  FrequencySensor(discovery_info["name"], device)])


class VoltageSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, name, device):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._device = device

    @property
    def unique_id(self) -> Optional[str]:
        return f"novatek_" + self._name + f"_voltage"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'novatek voltage value from device ' + self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_class(self):
        return SENSORS["voltage"][0] if "voltage" in SENSORS else None

    @property
    def state_class(self) -> str | None:
        return SENSORS["voltage"][1] if "voltage" in SENSORS else None

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return SENSORS["voltage"][2] if "voltage" in SENSORS else None

    @property
    def icon(self):
        return SENSORS["voltage"][3] if "voltage" in SENSORS else None

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        try:
            self._state = self._device.Voltage()
        except (ConnectionAbortedError, json.decoder.JSONDecodeError):
            self._device.Connect()
            self._state = self._device.Voltage()

class CurrentSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, name, device):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._device = device

    @property
    def unique_id(self) -> Optional[str]:
        return f"novatek_" + self._name + f"_current"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'novatek current value from device ' + self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_class(self):
        return SENSORS["current"][0] if "current" in SENSORS else None

    @property
    def state_class(self) -> str | None:
        return SENSORS["current"][1] if "current" in SENSORS else None

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return SENSORS["current"][2] if "current" in SENSORS else None

    @property
    def icon(self):
        return SENSORS["current"][3] if "current" in SENSORS else None

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        try:
            self._state = self._device.Current()
        except (ConnectionAbortedError, json.decoder.JSONDecodeError):
            self._device.Connect()
            self._state = self._device.Current()

class PowerSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, name, device, tag):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._device = device
        self._tag = tag

    @property
    def unique_id(self) -> Optional[str]:
        return f"novatek_" + self._name + f"_" + self._tag + f"_power"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'novatek ' + self._tag + ' power value from device ' + self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_class(self):
        return SENSORS["power"][0] if "power" in SENSORS else None

    @property
    def state_class(self) -> str | None:
        return SENSORS["power"][1] if "power" in SENSORS else None

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return SENSORS["power"][2] if "power" in SENSORS else None

    @property
    def icon(self):
        return SENSORS["power"][3] if "power" in SENSORS else None

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        try:
            if self._tag == TAG_ACTIVE:
                self._state = self._device.ActivePower()
            else:
                self._state = self._device.FullPower()
        except (ConnectionAbortedError, json.decoder.JSONDecodeError):
            self._device.Connect()
            if self._tag == TAG_ACTIVE:
                self._state = self._device.ActivePower()
            else:
                self._state = self._device.FullPower()

class EnergySensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, name, device, tag):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._device = device
        self._tag = tag

    @property
    def unique_id(self) -> Optional[str]:
        return f"novatek_" + self._name + f"_" + self._tag + f"_energy"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'novatek ' + self._tag + ' energy value from device ' + self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_class(self):
        return SENSORS["energy"][0] if "energy" in SENSORS else None

    @property
    def state_class(self) -> str | None:
        return SENSORS["energy"][1] if "energy" in SENSORS else None

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return SENSORS["energy"][2] if "energy" in SENSORS else None

    @property
    def icon(self):
        return SENSORS["energy"][3] if "energy" in SENSORS else None

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        try:
            if self._tag == TAG_ACTIVE:
                self._state = self._device.ActiveEnergy()
            else:
                self._state = self._device.FullEnergy()
        except (ConnectionAbortedError, json.decoder.JSONDecodeError):
            self._device.Connect()
            if self._tag == TAG_ACTIVE:
                self._state = self._device.ActiveEnergy()
            else:
                self._state = self._device.FullEnergy()

class FrequencySensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, name, device):
        """Initialize the sensor."""
        self._state = None
        self._name = name
        self._device = device

    @property
    def unique_id(self) -> Optional[str]:
        return f"novatek_" + self._name + f"_frequency"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'novatek frequency value from device ' + self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_class(self):
        return SENSORS["frequency"][0] if "frequency" in SENSORS else None

    @property
    def state_class(self) -> str | None:
        return SENSORS["frequency"][1] if "frequency" in SENSORS else None

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return SENSORS["frequency"][2] if "frequency" in SENSORS else None

    @property
    def icon(self):
        return SENSORS["frequency"][3] if "frequency" in SENSORS else None

    def update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        try:
            self._state = self._device.Frequency()
        except (ConnectionAbortedError, json.decoder.JSONDecodeError):
            self._device.Connect()
            self._state = self._device.Frequency()
