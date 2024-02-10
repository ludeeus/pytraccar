"""Test subscription."""
import asyncio
from unittest.mock import patch
from aiohttp import WSMsgType
import aiohttp
import pytest

from pytraccar import (
    ApiClient,
    TraccarConnectionException,
    TraccarException,
    SubscriptionStatus,
)
from tests.common import WSMessage


@pytest.mark.parametrize(
    "messages",
    (
        [
            WSMessage(type=WSMsgType.TEXT, json={}),
            WSMessage(type=WSMsgType.TEXT, json=None),
        ],
        [
            WSMessage(type=WSMsgType.TEXT, json={"devices": []}),
        ],
        [
            WSMessage(type=WSMsgType.TEXT, json={"positions": []}),
        ],
        [
            WSMessage(type=WSMsgType.TEXT, json={"events": []}),
        ],
        [
            WSMessage(type=WSMsgType.TEXT, json={"devices": []}),
            WSMessage(type=WSMsgType.TEXT, json={"positions": []}),
            WSMessage(type=WSMsgType.TEXT, json={"events": []}),
        ],
        [
            WSMessage(
                type=WSMsgType.TEXT, json={"events": [], "devices": [], "events": []}
            ),
        ],
    ),
)
@pytest.mark.asyncio
async def test_subscription_text_message(
    api_client: ApiClient,
    messages: list[WSMessage],
    mock_ws_messages,
):
    """Test subscription text message."""
    _handled = []
    _expected_handled = []
    for message in messages:
        mock_ws_messages.add(message)
        if message.type == WSMsgType.TEXT and (data := message.json()):
            _expected_handled.append(
                {
                    "devices": None,
                    "events": None,
                    "positions": None,
                    **data,
                }
            )

    async def _handler(data):
        _handled.append(data)

    await api_client.subscribe(_handler)
    assert _handled == _expected_handled


@pytest.mark.parametrize(
    "message",
    (
        WSMessage(type=WSMsgType.CLOSE),
        WSMessage(type=WSMsgType.CLOSED),
        WSMessage(type=WSMsgType.ERROR),
    ),
)
@pytest.mark.asyncio
async def test_subscription_stopping_message(
    api_client: ApiClient,
    message: WSMessage,
    mock_ws_messages,
):
    """Test subscription stopping message."""
    _handled = []
    mock_ws_messages.add(message)

    async def _handler(data):
        _handled.append(data)

    with pytest.raises(
        TraccarConnectionException,
        match=f"WebSocket connection closed with {message.type.name}",
    ):
        await api_client.subscribe(_handler)
    assert len(_handled) == 0


@pytest.mark.parametrize(
    "message",
    (
        WSMessage(type=WSMsgType.CONTINUATION),
        WSMessage(type=WSMsgType.BINARY),
        WSMessage(type=WSMsgType.PING),
        WSMessage(type=WSMsgType.PONG),
        WSMessage(type=WSMsgType.CLOSING),
    ),
)
@pytest.mark.asyncio
async def test_subscription_unknown_type(
    api_client: ApiClient,
    message: WSMessage,
    mock_ws_messages,
    caplog: pytest.LogCaptureFixture,
):
    """Test subscription unknown type."""
    _handled = []
    mock_ws_messages.add(message)

    async def _handler(data):
        _handled.append(data)

    assert f"Unexpected message type {message.type.name}" not in caplog.text

    await api_client.subscribe(_handler)

    assert len(_handled) == 0
    assert f"Unexpected message type {message.type.name}" in caplog.text


@pytest.mark.asyncio
async def test_subscription_bad_handler(
    api_client: ApiClient,
    mock_ws_messages,
    caplog: pytest.LogCaptureFixture,
):
    """Test subscription unknown type."""
    mock_ws_messages.add(WSMessage(type=WSMsgType.TEXT, json={"devices": []}))

    async def _handler(data):
        raise ValueError("Bad handler")

    await api_client.subscribe(_handler)

    assert "Exception while handling message: ValueError(Bad handler)" in caplog.text


@pytest.mark.parametrize(
    ("side_effect", "raises", "with_message"),
    (
        (
            KeyError("boom"),
            TraccarException,
            "Unexpected error - 'boom'",
        ),
        (
            asyncio.TimeoutError(),
            TraccarConnectionException,
            "Timeout error connecting to Traccar",
        ),
        (
            asyncio.CancelledError("boom"),
            TraccarConnectionException,
            "Subscription cancelled",
        ),
        (
            aiohttp.ClientError("boom"),
            TraccarConnectionException,
            "Could not communicate with Traccar - boom",
        ),
        (
            TraccarConnectionException(),
            TraccarConnectionException,
            "",
        ),
    ),
)
@pytest.mark.asyncio
async def test_subscription_exceptions(
    api_client: ApiClient,
    side_effect: Exception,
    raises: Exception,
    with_message: str,
):
    """Test subscription exceptions."""
    assert api_client.subscription_status == SubscriptionStatus.DISCONNECTED
    with patch("aiohttp.ClientSession.ws_connect", side_effect=side_effect):
        with pytest.raises(
            raises,
            match=with_message,
        ):
            await api_client.subscribe(None)

    assert api_client.subscription_status == SubscriptionStatus.ERROR
