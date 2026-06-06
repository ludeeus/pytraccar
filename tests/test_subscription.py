"""Test subscription."""

from __future__ import annotations

import asyncio
from typing import Any, NoReturn
from unittest.mock import patch

import aiohttp
import pytest
from aiohttp import WSMsgType

from pytraccar import (
    ApiClient,
    SubscriptionStatus,
    TraccarConnectionException,
    TraccarException,
)
from tests.common import WSMessage, WSMessageHandler


@pytest.mark.parametrize(
    "messages",
    [
        [
            WSMessage(messagetype=WSMsgType.TEXT, json={}),
            WSMessage(messagetype=WSMsgType.TEXT, json=None),
        ],
        [
            WSMessage(messagetype=WSMsgType.TEXT, json={"devices": []}),
        ],
        [
            WSMessage(messagetype=WSMsgType.TEXT, json={"positions": []}),
        ],
        [
            WSMessage(messagetype=WSMsgType.TEXT, json={"events": []}),
        ],
        [
            WSMessage(messagetype=WSMsgType.TEXT, json={"devices": []}),
            WSMessage(messagetype=WSMsgType.TEXT, json={"positions": []}),
            WSMessage(messagetype=WSMsgType.TEXT, json={"events": []}),
        ],
        [
            WSMessage(messagetype=WSMsgType.TEXT, json={"events": [], "devices": []}),
        ],
    ],
)
@pytest.mark.asyncio
async def test_subscription_text_message(
    api_client: ApiClient,
    messages: list[WSMessage],
    mock_ws_messages: WSMessageHandler,
) -> None:
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

    async def _handler(data: Any) -> None:
        _handled.append(data)

    with pytest.raises(
        TraccarConnectionException,
        match="WebSocket connection closed unexpectedly",
    ):
        await api_client.subscribe(_handler)
    assert _handled == _expected_handled


@pytest.mark.parametrize(
    "message",
    [
        WSMessage(messagetype=WSMsgType.CLOSE),
        WSMessage(messagetype=WSMsgType.CLOSED),
        WSMessage(messagetype=WSMsgType.CLOSING),
        WSMessage(messagetype=WSMsgType.ERROR),
    ],
)
@pytest.mark.asyncio
async def test_subscription_stopping_message(
    api_client: ApiClient,
    message: WSMessage,
    mock_ws_messages: WSMessageHandler,
) -> None:
    """Test subscription stopping message."""
    _handled = []
    mock_ws_messages.add(message)

    async def _handler(data: Any) -> None:
        _handled.append(data)

    with pytest.raises(
        TraccarConnectionException,
        match=f"WebSocket connection closed with {message.type.name}",
    ):
        await api_client.subscribe(_handler)
    assert len(_handled) == 0


@pytest.mark.parametrize(
    "message",
    [
        WSMessage(messagetype=WSMsgType.CONTINUATION),
        WSMessage(messagetype=WSMsgType.BINARY),
        WSMessage(messagetype=WSMsgType.PING),
        WSMessage(messagetype=WSMsgType.PONG),
    ],
)
@pytest.mark.asyncio
async def test_subscription_unknown_type(
    api_client: ApiClient,
    message: WSMessage,
    mock_ws_messages: WSMessageHandler,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test subscription unknown type."""
    _handled = []
    mock_ws_messages.add(message)

    async def _handler(data: Any) -> None:
        _handled.append(data)

    assert f"Unexpected message type {message.type.name}" not in caplog.text

    with pytest.raises(
        TraccarConnectionException,
        match="WebSocket connection closed unexpectedly",
    ):
        await api_client.subscribe(_handler)

    assert len(_handled) == 0
    assert f"Unexpected message type {message.type.name}" in caplog.text


@pytest.mark.asyncio
async def test_subscription_bad_handler(
    api_client: ApiClient,
    mock_ws_messages: WSMessageHandler,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test subscription unknown type."""
    mock_ws_messages.add(WSMessage(messagetype=WSMsgType.TEXT, json={"devices": []}))

    async def _handler(_: Any) -> NoReturn:
        raise ValueError("Bad handler")

    with pytest.raises(
        TraccarConnectionException,
        match="WebSocket connection closed unexpectedly",
    ):
        await api_client.subscribe(_handler)

    assert "Exception while handling message: ValueError(Bad handler)" in caplog.text


@pytest.mark.asyncio
async def test_subscription_silent_close(
    api_client: ApiClient,
    mock_ws_messages: WSMessageHandler,
) -> None:
    """Test that a silent WebSocket close raises TraccarConnectionException.

    When the server closes the connection without sending a CLOSE frame
    (e.g. during a restart), aiohttp's async iterator exits without raising.
    The client must still surface this as a connection exception.
    """
    assert api_client.subscription_status == SubscriptionStatus.DISCONNECTED
    assert len(mock_ws_messages.messages) == 0

    async def _handler(_: Any) -> None:
        pass

    with pytest.raises(
        TraccarConnectionException,
        match="WebSocket connection closed unexpectedly",
    ):
        await api_client.subscribe(_handler)

    assert api_client.subscription_status == SubscriptionStatus.ERROR


@pytest.mark.parametrize(
    ("side_effect", "raises", "with_message"),
    [
        (
            KeyError("boom"),
            TraccarException,
            "Unexpected error",
        ),
        (
            asyncio.TimeoutError(),
            TraccarConnectionException,
            "Timeout error connecting to Traccar",
        ),
        (
            aiohttp.ClientError("boom"),
            TraccarConnectionException,
            "Could not communicate with Traccar",
        ),
        (
            TraccarConnectionException(),
            TraccarConnectionException,
            None,
        ),
    ],
)
@pytest.mark.asyncio
async def test_subscription_exceptions(
    api_client: ApiClient,
    side_effect: Exception,
    raises: Exception,
    with_message: str | None,
) -> None:
    """Test subscription exceptions."""
    assert api_client.subscription_status == SubscriptionStatus.DISCONNECTED
    with patch("aiohttp.ClientSession.ws_connect", side_effect=side_effect):
        if with_message is not None:
            with pytest.raises(raises, match=with_message):
                await api_client.subscribe(None)
        else:
            with pytest.raises(raises):
                await api_client.subscribe(None)

    assert api_client.subscription_status == SubscriptionStatus.ERROR


@pytest.mark.asyncio
async def test_subscription_cancelation(api_client: ApiClient) -> None:
    """Test subscription exceptions."""
    assert api_client.subscription_status == SubscriptionStatus.DISCONNECTED
    with patch(
        "aiohttp.ClientSession.ws_connect", side_effect=asyncio.CancelledError("boom")
    ):
        await api_client.subscribe(None)

    assert api_client.subscription_status == SubscriptionStatus.DISCONNECTED


@pytest.mark.asyncio
async def test_subscription_unsubscribe_graceful(
    api_client: ApiClient,
    mock_ws_messages: WSMessageHandler,
) -> None:
    """Test cancellation-based unsubscription is handled gracefully."""
    handler_block_seconds = 30
    started = asyncio.Event()
    mock_ws_messages.add(WSMessage(messagetype=WSMsgType.TEXT, json={"devices": []}))

    async def _handler(_message: Any) -> None:
        started.set()
        await asyncio.sleep(handler_block_seconds)

    subscribe_task = asyncio.create_task(api_client.subscribe(_handler))

    await asyncio.wait_for(started.wait(), timeout=1)

    subscribe_task.cancel()
    try:
        await asyncio.wait_for(subscribe_task, timeout=1)
    except asyncio.CancelledError:
        pytest.fail("Cancellation should be handled gracefully by subscribe()")

    assert api_client.subscription_status == SubscriptionStatus.DISCONNECTED
