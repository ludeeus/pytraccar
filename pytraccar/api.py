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

    @property
    def geofences(self):
        """Return the configured geofences if any."""
        return self._geofences

    @property
    def devices(self):
        """Return the devices if any."""
        return self._devices
