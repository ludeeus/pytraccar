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
HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json'}


class API(object):
    """A class for the Traccar API."""

    def __init__(self, loop, session, username, password,
                 host, port=8082, ssl=False):
        """Initialize the class."""
        self._loop = loop
        self._auth = aiohttp.BasicAuth(username, password)
        schema = 'https' if ssl else 'http'
        self._api = schema + '://' + host + ':' + str(port) + '/api'
        self._session = session
        self._authenticated = False
        self._geofences = {}
        self._devices = []
        self._positions = []
        self._device_info = {}

    async def test_connection(self):
        """Get the local installed version."""
        base_url = self._api + '/devices'
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(base_url,
                                                   auth=self._auth,
                                                   headers=HEADERS)
            if response.status == 200:
                self._authenticated = True
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error connecting to Traccar, %s', error)

    async def get_device_info(self):
        """Get the local installed version."""
        await self.get_geofences()
        await self.get_devices()
        await self.get_positions()
        devinfo = {}
        try:
            for dev in self._devices or []:
                for pos in self._positions or []:
                    if pos['deviceId'] == dev.get('id'):
                        unique_id = dev.get('uniqueId')
                        devinfo[unique_id] = {}
                        devinfo[unique_id]['device_id'] = dev.get('id')
                        devinfo[unique_id]['device_id'] = dev.get('name')
                        devinfo[unique_id]['address'] = pos.get('address')
                        devinfo[unique_id]['updated'] = dev.get('lastUpdate')
                        devinfo[unique_id]['category'] = dev.get('category')
                        devinfo[unique_id]['latitude'] = pos.get('latitude')
                        devinfo[unique_id]['longitude'] = pos.get('longitude')
                        devinfo[unique_id]['altitude'] = pos.get('altitude')
                        devinfo[unique_id]['speed'] = pos.get('speed')
                        devattr = pos.get('attributes', {})
                        battery_level = devattr.get('batteryLevel')
                        motion = devattr.get('motion')
                        devinfo[unique_id]['battery'] = battery_level
                        devinfo[unique_id]['motion'] = motion
                        try:
                            geofence = self.geofences[dev['geofenceIds'][0]]
                        except IndexError:
                            geofence = None
                        devinfo[unique_id]['geofence'] = geofence
            self._device_info = devinfo
        except KeyError as error:
            _LOGGER.error('Error combining data from Traccar, %s', error)

    async def get_geofences(self):
        """Get the local installed version."""
        base_url = self._api + '/geofences'
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(base_url,
                                                   auth=self._auth,
                                                   headers=HEADERS)
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
                response = await self._session.get(base_url,
                                                   auth=self._auth,
                                                   headers=HEADERS)
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
                response = await self._session.get(base_url,
                                                   auth=self._auth,
                                                   headers=HEADERS)
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

    @property
    def authenticated(self):
        """Return bool that indicate the success of the authentication."""
        return self._authenticated
