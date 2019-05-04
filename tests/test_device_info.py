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

        testdeviceid = "111111111"
        testdevice = traccar.device_info[testdeviceid]

        assert isinstance(testdevice["address"], str)
        assert isinstance(testdevice["latitude"], float)
        assert isinstance(testdevice["longitude"], float)
        assert isinstance(testdevice["accuracy"], float)
        assert isinstance(testdevice["altitude"], float)
        assert isinstance(testdevice["course"], float)
        assert isinstance(testdevice["speed"], float)
        assert isinstance(testdevice["traccar_id"], int)
        assert isinstance(testdevice["device_id"], str)
        assert isinstance(testdevice["updated"], str)
        assert isinstance(testdevice["category"], str)
        assert isinstance(testdevice["battery"], float)
        assert isinstance(testdevice["motion"], bool)
        assert isinstance(testdevice["geofence"], str)
