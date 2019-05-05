"""Communication tests."""
import json

import aiohttp
import pytest

from pytraccar.api import API
from pytraccar.const import HEADERS

from .const import TEST_HOST, TEST_PASS, TEST_PORT, TEST_USER
from .fixtrues import positions_response


@pytest.mark.asyncio
async def test_positions(aresponses, event_loop, positions_response):
    """Test positions."""
    aresponses.add(
        "example.com:7728",
        "/api/positions",
        "get",
        aresponses.Response(
            text=json.dumps(positions_response), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        traccar = API(event_loop, session, TEST_USER, TEST_PASS, TEST_HOST, TEST_PORT)
        await traccar.get_positions()
        for position in traccar.positions:
            assert isinstance(position["id"], int)
            assert isinstance(position["attributes"], dict)
            assert isinstance(position["deviceId"], int)
            assert isinstance(position["serverTime"], str)
            assert isinstance(position["latitude"], float)
            assert isinstance(position["longitude"], float)
            assert isinstance(position["address"], str)
