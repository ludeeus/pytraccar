"""
Update and fetch device information from Traccar.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import asyncio
import logging
import socket

from datetime import datetime, timedelta

import aiohttp

from pytraccar.const import ATTRIBUTES, EVENT_INTERVAL, HEADERS

_LOGGER = logging.getLogger(__name__)


class API(object):  # pylint: disable=too-many-instance-attributes
    """A class for the Traccar API."""

    def __init__(self, loop, session, username, password, host, port=8082, ssl=False):
        """Initialize the class."""
        self._loop = loop
        self._auth = aiohttp.BasicAuth(username, password)
        schema = "https" if ssl else "http"
        self._api = "{}://{}:{}/api".format(schema, host, port)
        self._session = session
        self._authenticated = False
        self._connected = False
        self._geofences = {}
        self._devices = []
        self._events = []
        self._positions = []
        self._device_info = {}

    async def api(self, endpoint, params=None, test=False):
        """Comunicate with the API."""
        data = None
        url = "{}/{}".format(self._api, endpoint)
        try:
            response = await self._session.get(
                url,
                auth=self._auth,
                headers=HEADERS,
                params=params,
                timeout=aiohttp.ClientTimeout(total=10),
            )

            if response.status == 200:
                self._authenticated = True
                self._connected = True
                if not test:
                    data = await response.json()
            elif response.status == 401:
                self._authenticated = False
                self._connected = True

        except asyncio.TimeoutError as error:
            self._authenticated, self._connected = False, False
            if not test:
                _LOGGER.warning("Timeouterror connecting to Traccar, %s", error)
        except aiohttp.ClientError as error:
            self._authenticated, self._connected = False, False
            if not test:
                _LOGGER.warning("Error connecting to Traccar, %s", error)
        except socket.gaierror as error:
            self._authenticated, self._connected = False, False
            if not test:
                _LOGGER.warning("Error connecting to Traccar, %s", error)
        except TypeError as error:
            self._authenticated, self._connected = False, False
            if not test:
                _LOGGER.warning("Error connecting to Traccar, %s", error)
        except Exception as error:  # pylint: disable=broad-except
            self._authenticated, self._connected = False, False
            if not test:
                _LOGGER.warning("Error connecting to Traccar, %s", error)
        return data

    async def test_connection(self):
        """Test the connection."""
        await self.api("devices", test=True)

    async def get_device_info(self, custom_attributes=None):
        """Get device info"""
        await self.get_geofences()
        await self.get_devices()
        await self.get_positions()
        devinfo = {}
        try:  # pylint: disable=too-many-nested-blocks
            for dev in self._devices or []:
                for pos in self._positions or []:
                    if pos["deviceId"] == dev.get("id"):
                        uid = dev.get("uniqueId")
                        devinfo[uid] = {}
                        nested = pos.get("attributes", {})

                        for attribute in ATTRIBUTES["position"]:
                            key = ATTRIBUTES["position"][attribute]
                            devinfo[uid][attribute] = pos[key]

                        for attribute in ATTRIBUTES["device"]:
                            key = ATTRIBUTES["device"][attribute]
                            devinfo[uid][attribute] = dev[key]

                        devinfo[uid]["battery"] = nested.get("batteryLevel")
                        devinfo[uid]["motion"] = nested.get("motion")

                        if custom_attributes is not None:
                            for attr in custom_attributes:
                                if attr in nested:
                                    attrvalue = nested.get(attr)
                                    devinfo[uid][attr] = attrvalue
                        try:
                            geofence = self.geofences[dev["geofenceIds"][0]]
                        except IndexError:
                            geofence = None

                        devinfo[uid]["geofence"] = geofence
            if devinfo:
                self._device_info = devinfo
            else:
                self._device_info = self._device_info
            _LOGGER.debug(self._device_info)
        except KeyError as error:
            _LOGGER.error("Error combining data from Traccar, %s", error)

    async def get_geofences(self):
        """Get geofences."""
        data = await self.api("geofences")
        if self.connected and self.authenticated:
            for geofence in data or []:
                self._geofences[geofence["id"]] = geofence["name"]
        else:
            self._geofences = self._geofences
        _LOGGER.debug(self._geofences)

    async def get_devices(self):
        """Get devices."""
        data = await self.api("devices")
        if self.connected and self.authenticated:
            self._devices = data
        else:
            self._devices = self._devices
        _LOGGER.debug(self._devices)

    async def get_positions(self):
        """Get positions."""
        data = await self.api("positions")
        if self.connected and self.authenticated:
            self._positions = data
        else:
            self._positions = self._positions
        _LOGGER.debug(self._positions)

    async def get_events(
        self, device_ids, group_ids=None, from_time=None, to_time=None, event_types=None
    ):
        """Get events."""
        if to_time is None:
            to_time = datetime.utcnow()
        if from_time is None:
            from_time = to_time - timedelta(seconds=EVENT_INTERVAL)
        if event_types is None:
            event_types = ["allEvents"]

        get_params = []

        get_params.extend([("deviceId", value) for value in device_ids])
        if group_ids is not None:
            get_params.extend([("groupId", value) for value in group_ids])
        get_params.extend([("from", from_time.isoformat() + "Z")])
        get_params.extend([("to", to_time.isoformat() + "Z")])
        get_params.extend([("type", value) for value in event_types])

        data = await self.api("reports/events", get_params)

        if self.connected and self.authenticated:
            self._events = data
        else:
            self._events = self._events

        return self._events

    @property
    def events(self):
        """Return events."""
        return self._events

    @property
    def geofences(self):
        """Return the configured geofences if any."""
        return self._geofences

    @property
    def devices(self):
        """Return the devices if any."""
        return self._devices

    @property
    def positions(self):
        """Return the device positions if any."""
        return self._positions

    @property
    def device_info(self):
        """Return the device info if any."""
        return self._device_info

    @property
    def authenticated(self):
        """Return bool that indicate the success of the authentication."""
        return self._authenticated

    @property
    def connected(self):
        """Return bool that indicate the success of the connection."""
        return self._connected
