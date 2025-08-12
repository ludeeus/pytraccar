"""API client for Traccar servers."""

from __future__ import annotations

import asyncio
from contextlib import suppress
from datetime import UTC, datetime, timedelta
from logging import Logger, getLogger
from typing import TYPE_CHECKING, Any

import aiohttp

from .exceptions import (
    TraccarAuthenticationException,
    TraccarConnectionException,
    TraccarException,
    TraccarResponseException,
)
from .models import (
    SubscriptionData,
    SubscriptionStatus,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from .models import (
        DeviceModel,
        GeofenceModel,
        PositionModel,
        ReportsEventeModel,
        ServerModel,
    )


_LOGGER: Logger = getLogger(__package__)


class ApiClient:
    """Class for interacting with the Traccar API.

    :param host: Traccar server hostname or IP (without scheme). Used to build
        the base URL.
    :type host: str
    :param token: Traccar API access token. Sent as ``Authorization: Bearer
        <token>`` with every request.
    :type token: str
    :param client_session: Existing ``aiohttp`` session used for HTTP and
        WebSocket communication. This client does not manage the session
        lifecycle.
    :type client_session: aiohttp.ClientSession
    :param port: Port for the Traccar API. Defaults to ``8082`` if not
        provided.
    :type port: int | None
    :param ssl: Use HTTPS when ``True``; HTTP when ``False``. Defaults to
        ``False``.
    :type ssl: bool
    :param verify_ssl: Verify TLS certificates for HTTPS/WebSocket
        connections. Relevant when ``ssl`` is ``True``. Defaults to ``True``.
    :type verify_ssl: bool
    :param ws_heartbeat: Heartbeat interval (seconds) for the WebSocket used by
        :meth:`subscribe` method. Defaults to ``120``.
    :type ws_heartbeat: int

    Note:
        Base URL: ``http[s]://{host}:{port or 8082}/api``.
        Extra keyword arguments are accepted but ignored for forward
        compatibility.

    """

    def __init__(
        self,
        host: str,
        token: str,
        client_session: aiohttp.ClientSession,
        *,
        port: int | None = None,
        ssl: bool = False,
        verify_ssl: bool = True,
        ws_heartbeat: int = 120,
        **_: Any,
    ) -> None:
        """Initialize the API client."""
        self._base_url = f"http{'s' if ssl else ''}://{host}:{port or 8082}/api"
        self._client_session = client_session
        self._token = token
        self._verify_ssl = verify_ssl
        self._subscription_status = SubscriptionStatus.DISCONNECTED
        self._ws_heartbeat = ws_heartbeat

    @property
    def subscription_status(self) -> SubscriptionStatus:
        """Return the current subscription status."""
        return self._subscription_status

    async def _call_api(
        self,
        endpoint: str,
        method: str = "GET",
        *,
        params: list[tuple[str, str | int]] | None = None,
        headers: dict[str, str] | None = None,
        data: Any | None = None,
        **_: Any,
    ) -> Any:
        """Call the API endpoint and return the response."""
        try:
            async with self._client_session.request(
                method=method,
                url=f"{self._base_url}/{endpoint}",
                ssl=self._verify_ssl,
                params=params,
                data=data,
                headers={
                    aiohttp.hdrs.ACCEPT: "application/json",
                    aiohttp.hdrs.AUTHORIZATION: f"Bearer {self._token}",
                    aiohttp.hdrs.CONTENT_TYPE: "application/json",
                    **(headers or {}),
                },
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status == 401:
                    raise TraccarAuthenticationException("Unauthorized")
                if response.status == 200:
                    return await response.json()

                raise TraccarResponseException(f"{response.status}: {response.reason}")
        except (TraccarAuthenticationException, TraccarResponseException):
            raise
        except TimeoutError as exception:
            raise TraccarConnectionException(
                "Timeouterror connecting to Traccar"
            ) from exception
        except (aiohttp.ClientError, asyncio.CancelledError) as exception:
            raise TraccarConnectionException(
                f"Could not communicate with Traccar - {exception}"
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise TraccarException(f"Unexpected error - {exception}") from exception

    async def get_server(self) -> ServerModel:
        """Get server information.

        :return: Server information from Traccar.
        :rtype: ServerModel
        :raises TraccarAuthenticationException: If authentication fails (401).
        :raises TraccarResponseException: For non-200 HTTP responses.
        :raises TraccarConnectionException: On connectivity/timeouts/client errors.
        :raises TraccarException: For unexpected errors.
        """
        response: ServerModel = await self._call_api("server")
        return response

    async def get_devices(self) -> list[DeviceModel]:
        """Get all devices from the Traccar API.

        :return: A list of devices.
        :rtype: list[DeviceModel]
        :raises TraccarAuthenticationException: If authentication fails (401).
        :raises TraccarResponseException: For non-200 HTTP responses.
        :raises TraccarConnectionException: On connectivity/timeouts/client errors.
        :raises TraccarException: For unexpected errors.
        """
        response: list[DeviceModel] = await self._call_api("devices")
        return response

    async def get_geofences(self) -> list[GeofenceModel]:
        """Get all geofences from the Traccar API.

        :return: A list of geofences.
        :rtype: list[GeofenceModel]
        :raises TraccarAuthenticationException: If authentication fails (401).
        :raises TraccarResponseException: For non-200 HTTP responses.
        :raises TraccarConnectionException: On connectivity/timeouts/client errors.
        :raises TraccarException: For unexpected errors.
        """
        response: list[GeofenceModel] = await self._call_api("geofences")
        return response

    async def get_positions(self) -> list[PositionModel]:
        """Get all positions from the Traccar API.

        :return: A list of positions.
        :rtype: list[PositionModel]
        :raises TraccarAuthenticationException: If authentication fails (401).
        :raises TraccarResponseException: For non-200 HTTP responses.
        :raises TraccarConnectionException: On connectivity/timeouts/client errors.
        :raises TraccarException: For unexpected errors.
        """
        response: list[PositionModel] = await self._call_api("positions")
        return response

    async def get_reports_events(
        self,
        *,
        devices: list[int] | None = None,
        groups: list[int] | None = None,
        event_types: list[str] | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        **_: Any,
    ) -> list[ReportsEventeModel]:
        """Get events.

        :param devices: Device IDs to filter by.
        :type devices: list[int] | None
        :param groups: Group IDs to filter by.
        :type groups: list[int] | None
        :param event_types: Event type names to filter by.
        :type event_types: list[str] | None
        :param start_time: Start time inclusive. If naive, treated as UTC.
        :type start_time: datetime | None
        :param end_time: End time inclusive. If naive, treated as UTC.
        :type end_time: datetime | None
        :return: A list of events matching the filters.
        :rtype: list[ReportsEventeModel]
        :raises TraccarAuthenticationException: If authentication fails (401).
        :raises TraccarResponseException: For non-200 HTTP responses.
        :raises TraccarConnectionException: On connectivity/timeouts/client errors.
        :raises TraccarException: For unexpected errors.
        """
        datetime_now = datetime.now(tz=UTC).replace(tzinfo=None)
        start_time = start_time or datetime_now
        end_time = end_time or datetime_now - timedelta(hours=30)
        response: list[ReportsEventeModel] = await self._call_api(
            "reports/events",
            params=[
                ("to", start_time.isoformat() + "Z"),
                ("from", end_time.isoformat() + "Z"),
                *[("deviceId", device) for device in devices or []],
                *[("groupId", group) for group in groups or []],
                *[("type", value) for value in event_types or ""],
            ],
        )
        return response

    async def subscribe(
        self, callback: Callable[[SubscriptionData], Awaitable[None]]
    ) -> None:
        """Subscribe to events via WebSocket and invoke the callback for each message.

        :param callback: Coroutine called with incoming payloads. The payload is a
            mapping with optional keys ``devices``, ``events``, and ``positions``.
        :type callback: Callable[[SubscriptionData], Awaitable[None]]
        :raises TraccarConnectionException: When the WebSocket closes/errors or on
            connectivity/timeouts/client errors.
        :raises TraccarException: For unexpected errors, including a failed session
            setup prior to opening the WebSocket.
        """

        async def _subscriber() -> None:
            self._subscription_status = SubscriptionStatus.CONNECTING
            async with self._client_session.ws_connect(
                url=f"{self._base_url}/socket",
                verify_ssl=self._verify_ssl,
                heartbeat=self._ws_heartbeat,
            ) as ws:
                self._subscription_status = SubscriptionStatus.CONNECTED
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        if not (data := msg.json()):
                            # Ignore empty messages
                            continue
                        try:
                            await callback(
                                {
                                    "devices": None,
                                    "events": None,
                                    "positions": None,
                                    **data,
                                }
                            )
                        except Exception as exception:
                            _LOGGER.exception(
                                "Exception while handling message: %s(%s)",
                                exception.__class__.__name__,
                                exception,
                            )
                    elif msg.type in (
                        aiohttp.WSMsgType.CLOSE,
                        aiohttp.WSMsgType.CLOSED,
                        aiohttp.WSMsgType.CLOSING,
                        aiohttp.WSMsgType.ERROR,
                    ):
                        raise TraccarConnectionException(
                            f"WebSocket connection closed with {msg.type.name}"
                        )
                    else:
                        _LOGGER.warning("Unexpected message type %s", msg.type.name)

        try:
            # https://www.traccar.org/api-reference/#tag/Session/paths/~1session/post
            await self._call_api(
                f"session?token={self._token}",
                method="GET",
                headers={
                    aiohttp.hdrs.CONTENT_TYPE: "application/x-www-form-urlencoded",
                },
            )
            await _subscriber()
        except asyncio.CancelledError:
            self._subscription_status = SubscriptionStatus.DISCONNECTED
        except Exception as exception:  # pylint: disable=broad-except
            self._subscription_status = SubscriptionStatus.ERROR
            if isinstance(exception, TraccarConnectionException):
                raise
            if isinstance(exception, asyncio.TimeoutError):
                raise TraccarConnectionException(
                    "Timeout error connecting to Traccar"
                ) from exception
            if isinstance(exception, aiohttp.ClientError):
                raise TraccarConnectionException(
                    "Could not communicate with Traccar"
                ) from exception
            raise TraccarException("Unexpected error") from exception
        finally:
            # Close the session if we can
            # https://www.traccar.org/api-reference/#tag/Session/paths/~1session/delete
            with suppress(TraccarException):
                await self._call_api(
                    "session",
                    method="DELETE",
                    headers={},
                )
