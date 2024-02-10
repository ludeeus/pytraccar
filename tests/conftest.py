"""Test fixtures and configuration."""
import logging

import aiohttp
import pytest
import pytest_asyncio

from pytraccar import ApiClient
from tests.common import MockedRequests, MockResponse

logging.basicConfig(level=logging.ERROR)
logging.getLogger("pytraccar").setLevel(logging.DEBUG)

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
def mock_requests():
    """Return a new mock request instanse."""
    return MockedRequests()


@pytest.fixture
def mock_response():
    """Return a new mock response instanse."""
    return MockResponse()


@pytest_asyncio.fixture
async def client_session(mock_response, mock_requests):
    """Mock our the request part of the client session."""

    async def _mocked_request(*args, **kwargs):
        if len(args) > 2:
            mock_response.mock_endpoint = args[2].split("/api/")[-1]
            mock_requests.add({"method": args[1], "url": args[2], **kwargs})
        else:
            mock_response.mock_endpoint = args[1].split("/api/")[-1]
            mock_requests.add({"method": args[0], "url": args[1], **kwargs})
        return mock_response

    async with aiohttp.ClientSession() as session:
        mock_requests.clear()
        session._request = _mocked_request  # pylint: disable=protected-access
        yield session


@pytest_asyncio.fixture
async def api_client(client_session):
    """Fixture to provide a API Client."""
    yield ApiClient(
        host="127.0.0.1",
        port=1337,
        username="test",
        password="test",
        client_session=client_session,
    )
