"""Base client tests."""

import asyncio

import aiohttp
import pytest

from pytraccar import (
    ApiClient,
    TraccarAuthenticationException,
    TraccarConnectionException,
    TraccarException,
    TraccarResponseException,
)
from tests.common import MockResponse


@pytest.mark.asyncio
async def test_base_api(api_client: ApiClient) -> None:
    """Test base API."""
    response = await api_client.get_server()
    assert response["bingKey"] == "string"


@pytest.mark.asyncio
async def test_base_api_unauthenticated(
    api_client: ApiClient, mock_response: MockResponse
) -> None:
    """Test unauthenticated base API."""
    mock_response.mock_status = 401
    with pytest.raises(TraccarAuthenticationException):
        await api_client.get_server()


@pytest.mark.asyncio
async def test_base_api_issue(
    api_client: ApiClient, mock_response: MockResponse
) -> None:
    """Test API issue."""
    mock_response.mock_status = 500
    with pytest.raises(TraccarResponseException):
        await api_client.get_server()


@pytest.mark.asyncio
async def test_base_api_timeout(
    api_client: ApiClient, mock_response: MockResponse
) -> None:
    """Test API issue."""
    mock_response.mock_raises = asyncio.TimeoutError
    with pytest.raises(TraccarConnectionException):
        await api_client.get_server()

    mock_response.mock_raises = aiohttp.ClientError
    with pytest.raises(TraccarConnectionException):
        await api_client.get_server()

    mock_response.mock_raises = TypeError
    with pytest.raises(TraccarException):
        await api_client.get_server()
