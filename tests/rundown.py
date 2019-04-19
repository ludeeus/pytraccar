"""Test all methods"""
import asyncio
import aiohttp
import pytest
from pytraccar.api import API

HOST = '0.0.0.0'
USERNAME = 'test'
PASSWORD = 'test'

LOOP = asyncio.get_event_loop()


@pytest.mark.asyncio
async def test_connection():
    """Test connection."""
    async with aiohttp.ClientSession() as session:
        traccar = API(LOOP, session, USERNAME, PASSWORD, HOST)
        await traccar.test_connection()
        assert not traccar.authenticated
        assert not traccar.connected


@pytest.mark.asyncio
async def test_get_geofences():
    """Test get_geofences."""
    async with aiohttp.ClientSession() as session:
        traccar = API(LOOP, session, USERNAME, PASSWORD, HOST)
        await traccar.get_device_info()
        assert not traccar.authenticated
        assert not traccar.connected
        assert traccar.geofences == {}


@pytest.mark.asyncio
async def test_get_devices():
    """Test get_devices."""
    async with aiohttp.ClientSession() as session:
        traccar = API(LOOP, session, USERNAME, PASSWORD, HOST)
        await traccar.get_devices()
        assert not traccar.authenticated
        assert not traccar.connected
        assert traccar.devices == []


@pytest.mark.asyncio
async def test_get_positions():
    """Test get_positions."""
    async with aiohttp.ClientSession() as session:
        traccar = API(LOOP, session, USERNAME, PASSWORD, HOST)
        await traccar.get_positions()
        assert not traccar.authenticated
        assert not traccar.connected
        assert traccar.positions == []


@pytest.mark.asyncio
async def test_get_events():
    """Test get_events."""
    async with aiohttp.ClientSession() as session:
        traccar = API(LOOP, session, USERNAME, PASSWORD, HOST)
        deviceids = [123, 123, 123, 'test']
        await traccar.get_events(deviceids)
        assert not traccar.authenticated
        assert not traccar.connected
        assert traccar.events == {}


@pytest.mark.asyncio
async def test_get_device_info():
    """Test get_device_info."""
    async with aiohttp.ClientSession() as session:
        traccar = API(LOOP, session, USERNAME, PASSWORD, HOST)
        await traccar.get_device_info()
        assert not traccar.authenticated
        assert not traccar.connected
        assert traccar.devices == []
        assert traccar.positions == []
        assert traccar.geofences == {}
