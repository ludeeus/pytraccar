"""Test fixtures and configuration."""

import logging
from typing import Any, AsyncGenerator

import aiohttp
import pytest
import pytest_asyncio

from pytraccar import ApiClient
from tests.common import MockedRequests, MockResponse, WSMessageHandler

logging.basicConfig(level=logging.ERROR)
logging.getLogger("pytraccar").setLevel(logging.DEBUG)

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
def mock_requests() -> MockedRequests:
    """Return a new mock request instance."""
    return MockedRequests()


@pytest.fixture
def mock_response() -> MockResponse:
    """Return a new mock response instance."""
    return MockResponse()


@pytest.fixture
def mock_ws_messages() -> WSMessageHandler:
    """Return a new mock ws instance."""
    return WSMessageHandler()


@pytest_asyncio.fixture
async def client_session(
    mock_response: MockResponse,
    mock_requests: MockedRequests,
    mock_ws_messages: WSMessageHandler,
) -> AsyncGenerator[aiohttp.ClientSession, None]:
    """Mock our the request part of the client session."""

    class MockedWSContext:
        @property
        def closed(self) -> bool:
            return len(mock_ws_messages.messages) == 0

        async def receive(self) -> Any:
            return mock_ws_messages.get()

    async def _mocked_ws_connect(*_: Any, **__: Any) -> Any:
        return MockedWSContext()

    async def _mocked_request(*args: Any, **kwargs: Any) -> Any:
        if len(args) > 2:
            mock_response.mock_endpoint = args[2].split("/api/")[-1]
            mock_requests.add({"method": args[1], "url": args[2], **kwargs})
        else:
            mock_response.mock_endpoint = args[1].split("/api/")[-1]
            mock_requests.add({"method": args[0], "url": args[1], **kwargs})
        return mock_response

    async with aiohttp.ClientSession() as session:
        mock_requests.clear()
        session._request = _mocked_request  # noqa: SLF001
        session._ws_connect = _mocked_ws_connect  # noqa: SLF001
        yield session


@pytest_asyncio.fixture
async def api_client(
    client_session: AsyncGenerator[aiohttp.ClientSession, None],
) -> AsyncGenerator[ApiClient, None]:
    """Fixture to provide a API Client."""
    yield ApiClient(
        host="127.0.0.1",
        port=1337,
        username="test",
        password="test",  # noqa: S106
        client_session=client_session,
    )
