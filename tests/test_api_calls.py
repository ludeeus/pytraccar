"""Test API endpoint."""
import pytest

from pytraccar import ApiClient


@pytest.mark.asyncio
async def test_server(api_client: ApiClient) -> None:
    """Test /server endpoint."""
    response = await api_client.get_server()
    assert response["id"] == 0


@pytest.mark.asyncio
async def test_devices(api_client: ApiClient) -> None:
    """Test /devices endpoint."""
    response = await api_client.get_devices()
    assert isinstance(response, list)
    assert response[0]["id"] == 0


@pytest.mark.asyncio
async def test_geofences(api_client: ApiClient) -> None:
    """Test /geofences endpoint."""
    response = await api_client.get_geofences()
    assert isinstance(response, list)
    assert response[0]["id"] == 0


@pytest.mark.asyncio
async def test_positions(api_client: ApiClient) -> None:
    """Test /positions endpoint."""
    response = await api_client.get_positions()
    assert isinstance(response, list)
    assert response[0]["id"] == 0


@pytest.mark.asyncio
async def test_reports_events(api_client: ApiClient) -> None:
    """Test /reports/events endpoint."""
    response = await api_client.get_reports_events()
    assert isinstance(response, list)
    assert response[0]["id"] == 0
