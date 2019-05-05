"""Communication tests."""
import json

import aiohttp
import pytest

from pytraccar.api import API
from pytraccar.const import HEADERS

from .const import TEST_HOST, TEST_PASS, TEST_PORT, TEST_USER
from .fixtrues import event_response


@pytest.mark.asyncio
async def test_events(aresponses, event_loop, event_response):
    """Test events."""
    aresponses.add(
        "example.com:7728",
        "/api/reports/events",
        "get",
        aresponses.Response(
            text=json.dumps(event_response), status=200, headers=HEADERS
        ),
    )

    async with aiohttp.ClientSession(loop=event_loop) as session:
        traccar = API(event_loop, session, TEST_USER, TEST_PASS, TEST_HOST, TEST_PORT)
        await traccar.get_events([1, 2])
        assert isinstance(traccar.events, list)

        for event in traccar.events:
            assert isinstance(event["id"], int)
            assert isinstance(event["attributes"], dict)
            assert isinstance(event["deviceId"], int)
            assert isinstance(event["type"], str)
            assert isinstance(event["serverTime"], str)
            assert isinstance(event["positionId"], int)
            assert isinstance(event["geofenceId"], int)
            assert isinstance(event["maintenanceId"], int)
