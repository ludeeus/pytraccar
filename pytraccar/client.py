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
    """Class for interacting with the Traccar API."""

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
        """Get server information."""
        response: ServerModel = await self._call_api("server")
        return response

    async def get_devices(self) -> list[DeviceModel]:
        """Get all devices from the Traccar API."""
        response: list[DeviceModel] = await self._call_api("devices")
        return response

    async def get_geofences(self) -> list[GeofenceModel]:
        """Get all geofences from the Traccar API."""
        response: list[GeofenceModel] = await self._call_api("geofences")
        return response

    async def get_positions(self) -> list[PositionModel]:
        """Get all positions from the Traccar API."""
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
        """Get events."""
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
        """Subscribe to events."""

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
