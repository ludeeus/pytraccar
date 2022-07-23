"""Test API endpoint."""
import pytest

from pytraccar import (
    ApiClient,
    PositionModel,
    ServerModel,
    DeviceModel,
    GeofenceModel,
    ReportsEventeModel,
)


@pytest.mark.asyncio
async def test_server(api_client: ApiClient):
    """Test /server endpoint."""
    response = await api_client.get_server()
    assert isinstance(response, ServerModel)
    assert response.id == 0


@pytest.mark.asyncio
async def test_devices(api_client: ApiClient):
    """Test /devices endpoint."""
    response = await api_client.get_devices()
    assert isinstance(response, list)
    assert isinstance(response[0], DeviceModel)
    assert response[0].id == 0


@pytest.mark.asyncio
async def test_geofences(api_client: ApiClient):
    """Test /geofences endpoint."""
    response = await api_client.get_geofences()
    assert isinstance(response, list)
    assert isinstance(response[0], GeofenceModel)
    assert response[0].id == 0


@pytest.mark.asyncio
async def test_positions(api_client: ApiClient):
    """Test /positions endpoint."""
    response = await api_client.get_positions()
    assert isinstance(response, list)
    assert isinstance(response[0], PositionModel)
    assert response[0].id == 0


@pytest.mark.asyncio
async def test_reports_events(api_client: ApiClient):
    """Test /reports/events endpoint."""
    response = await api_client.get_reports_events()
    assert isinstance(response, list)
    assert isinstance(response[0], ReportsEventeModel)
    assert response[0].id == 0
