"""
Update and fetch device information from Traccar.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import asyncio
import logging
import socket

import aiohttp
import async_timeout

_LOGGER = logging.getLogger(__name__)


class API(object):
    """A class for the Traccar API."""

    def __init__(self, loop, session, username, password, api_endpoint):
        """Initialize the class."""
        self._loop = loop
        self._auth = aiohttp.BasicAuth(username, password)
        self._api = api_endpoint
        self._session = session
        self._geofences = {}
        self._devices = []
        self._positions = []
        self._device_info = {}

    async def get_device_info(self):
        """Get the local installed version."""
        await self.get_geofences()
        await self.get_devices()
        await self.get_positions()
        devinfo = {}
        try:
            for dev in self._devices or []:
                for pos in self._positions or []:
                    if pos['deviceId'] == dev['id']:
                        devinfo[dev['id']] = {}
                        devinfo[dev['id']]['name'] = dev['name']
                        devinfo[dev['id']]['address'] = pos['address']
                        devinfo[dev['id']]['updated'] = pos['fixTime']
                        devinfo[dev['id']]['latitude'] = pos['latitude']
                        devinfo[dev['id']]['longitude'] = pos['longitude']
                        devinfo[dev['id']]['altitude'] = pos['altitude']
                        devinfo[dev['id']]['speed'] = pos['speed']
                        geofence =  self.geofences[dev['geofenceIds'][0]]
                        devinfo[dev['id']]['geofence'] = geofence
            self._device_info = devinfo
        except KeyError as error:
            _LOGGER.error('Error combining data from Traccar, %s', error)

    async def get_geofences(self):
        """Get the local installed version."""
        base_url = self._api + '/geofences'
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(base_url, auth=self._auth)
            data = await response.json()
            for geofence in data or []:
                self._geofences[geofence['id']] = geofence['name']
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error fetching data from Traccar, %s', error)

    async def get_devices(self):
        """Get the local installed version."""
        base_url = self._api + '/devices'
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(base_url, auth=self._auth)
            data = await response.json()
            self._devices = data
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error fetching data from Traccar, %s', error)

    async def get_positions(self):
        """Get the local installed version."""
        base_url = self._api + '/positions'
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(base_url, auth=self._auth)
            data = await response.json()
            self._positions = data
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error fetching data from Traccar, %s', error)

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
