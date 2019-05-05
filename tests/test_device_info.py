"""Communication tests."""
import json

import aiohttp
import pytest

from pytraccar.api import API
from pytraccar.const import HEADERS

from .const import TEST_HOST, TEST_PASS, TEST_PORT, TEST_USER
from .fixtrues import positions_response, geofence_response, devices_response


@pytest.mark.asyncio
async def test_device_info(
    aresponses, event_loop, positions_response, geofence_response, devices_response
):
    """Test positions."""
    aresponses.add(
        "example.com:7728",
        "/api/positions",
        "get",
        aresponses.Response(
            text=json.dumps(positions_response), status=200, headers=HEADERS
        ),
    )
    aresponses.add(
        "example.com:7728",
        "/api/geofences",
        "get",
        aresponses.Response(
            text=json.dumps(geofence_response), status=200, headers=HEADERS
        ),
    )
    aresponses.add(
        "example.com:7728",
        "/api/devices",
        "get",
        aresponses.Response(
            text=json.dumps(devices_response), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        traccar = API(event_loop, session, TEST_USER, TEST_PASS, TEST_HOST, TEST_PORT)
        await traccar.get_device_info()
        assert isinstance(traccar.device_info, dict)
        assert len(traccar.device_info) == 2

        for device in traccar.device_info:
            assert isinstance(traccar.device_info[device]["address"], str)
            assert isinstance(traccar.device_info[device]["latitude"], float)
            assert isinstance(traccar.device_info[device]["longitude"], float)
            assert isinstance(traccar.device_info[device]["accuracy"], float)
            assert isinstance(traccar.device_info[device]["altitude"], float)
            assert isinstance(traccar.device_info[device]["course"], float)
            assert isinstance(traccar.device_info[device]["speed"], float)
            assert isinstance(traccar.device_info[device]["traccar_id"], int)
            assert isinstance(traccar.device_info[device]["device_id"], str)
            assert isinstance(traccar.device_info[device]["updated"], str)
            assert isinstance(traccar.device_info[device]["category"], str)
            assert isinstance(traccar.device_info[device]["battery"], float)
            assert isinstance(traccar.device_info[device]["motion"], bool)
            assert isinstance(traccar.device_info[device]["geofence"], str)
