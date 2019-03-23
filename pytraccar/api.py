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

    async def get_device_info(self, custom_attributes=None):
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
                        devinfo[unique_id]['traccar_id'] = dev.get('id')
                        devinfo[unique_id]['device_id'] = dev.get('name')
                        devinfo[unique_id]['address'] = pos.get('address')
                        devinfo[unique_id]['updated'] = dev.get('lastUpdate')
                        devinfo[unique_id]['category'] = dev.get('category')
                        devinfo[unique_id]['latitude'] = pos.get('latitude')
                        devinfo[unique_id]['longitude'] = pos.get('longitude')
                        devinfo[unique_id]['altitude'] = pos.get('altitude')
                        devinfo[unique_id]['course'] = pos.get('course')
                        devinfo[unique_id]['speed'] = pos.get('speed')
                        devattr = pos.get('attributes', {})
                        battery_level = devattr.get('batteryLevel')
                        motion = devattr.get('motion')
                        devinfo[unique_id]['battery'] = battery_level
                        devinfo[unique_id]['motion'] = motion
                        if custom_attributes is not None:
                            for attr in custom_attributes:
                                if attr in devattr:
                                    attrvalue = devattr.get(attr)
                                    devinfo[unique_id][attr] = attrvalue
                        try:
                            geofence = self.geofences[dev['geofenceIds'][0]]
                        except IndexError:
                            geofence = None
                        devinfo[unique_id]['geofence'] = geofence
            self._device_info = devinfo
            _LOGGER.debug(self._device_info)
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
            _LOGGER.debug(self._geofences)
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
            _LOGGER.debug(self._devices)
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
            _LOGGER.debug(self._positions)
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error fetching data from Traccar, %s', error)

    async def get_events(self, device_ids, group_ids=None,
                         from_time=None, to_time=None,
                         event_types=None):
        """Get the local installed version."""
        default_interval = 30
        if to_time is None:
            to_time = datetime.utcnow()
        if from_time is None:
            from_time = to_time - timedelta(seconds=default_interval)
        if event_types is None:
            event_types = ['allEvents']
        base_url = self._api + '/reports/events'
        get_params = []
        get_params.extend([('deviceId', value) for value in device_ids])
        if group_ids is not None:
            get_params.extend([('groupId', value) for value in group_ids])
        get_params.extend([('from', from_time.isoformat() + 'Z')])
        get_params.extend([('to', to_time.isoformat() + 'Z')])
        get_params.extend([('type', value) for value in event_types])
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(base_url,
                                                   auth=self._auth,
                                                   headers=HEADERS,
                                                   params=get_params)
            data = await response.json()
            return data
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
