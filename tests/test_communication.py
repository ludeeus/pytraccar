"""Communication tests."""
import aiohttp
import pytest
from pytraccar.api import API
from pytraccar.const import HEADERS

from .const import TEST_USER, TEST_PASS, TEST_HOST, TEST_PORT


@pytest.mark.asyncio
async def test_connection(aresponses, event_loop):
    """Test connection stable."""
    aresponses.add(
        "example.com:7728",
        "/api/devices",
        "get",
        aresponses.Response(status=200, headers=HEADERS),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        traccar = API(event_loop, session, TEST_USER, TEST_PASS, TEST_HOST, TEST_PORT)
        await traccar.test_connection()
        assert traccar.connected


@pytest.mark.asyncio
async def test_connection_failed(aresponses, event_loop):
    """Test connection stable."""
    aresponses.add(
        "example.com:7728",
        "/api/devices",
        "get",
        aresponses.Response(status=404, headers=HEADERS),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        traccar = API(event_loop, session, TEST_USER, TEST_PASS, TEST_HOST, TEST_PORT)
        await traccar.test_connection()
        assert not traccar.connected


@pytest.mark.asyncio
async def test_authentication(aresponses, event_loop):
    """Test pypi stable."""
    aresponses.add(
        "example.com:7728",
        "/api/devices",
        "get",
        aresponses.Response(status=200, headers=HEADERS),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        traccar = API(event_loop, session, TEST_USER, TEST_PASS, TEST_HOST, TEST_PORT)
        await traccar.test_connection()
        assert traccar.authenticated


@pytest.mark.asyncio
async def test_authentication_failed(aresponses, event_loop):
    """Test pypi stable."""
    aresponses.add(
        "example.com:7728",
        "/api/devices",
        "get",
        aresponses.Response(status=401, headers=HEADERS),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        traccar = API(event_loop, session, TEST_USER, TEST_PASS, TEST_HOST, TEST_PORT)
        await traccar.test_connection()
        assert not traccar.authenticated
