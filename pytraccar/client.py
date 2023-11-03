"""API client for Traccar servers."""
from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from logging import Logger, getLogger
from typing import Any

import aiohttp

from .exceptions import (
    TraccarAuthenticationException,
    TraccarConnectionException,
    TraccarException,
    TraccarResponseException,
)
from .models import (
    DeviceModel,
    GeofenceModel,
    PositionModel,
    ReportsEventeModel,
    ServerModel,
)

_LOGGER: Logger = getLogger(__package__)


class ApiClient:
    """
    Class for interacting with the Traccar API.
    """

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        client_session: aiohttp.ClientSession,
        *,
        port: int | None = None,
        ssl: bool = False,
        verify_ssl: bool = True,
        **kwargs: Any,
    ):
        """Initialize the API client."""
        self._authentication = aiohttp.BasicAuth(username, password)
        self._base_url = f"http{'s' if ssl else ''}://{host}:{port or 8082}/api"
        self._client_session = client_session
        self._verify_ssl = verify_ssl

    async def _call_api(
        self,
        endpoint: str,
        *,
        params: list[tuple[str, str | int]] | None = None,
    ) -> Any:
        """Call the API endpoint and return the response."""
        _LOGGER.debug("Calling API endpoint: %s with params: %s", endpoint, params)
        try:
            async with self._client_session.get(
                url=f"{self._base_url}/{endpoint}",
                auth=self._authentication,
                verify_ssl=self._verify_ssl,
                params=params,
                headers={
                    aiohttp.hdrs.CONTENT_TYPE: "application/json",
                    aiohttp.hdrs.ACCEPT: "application/json",
                },
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status == 401:
                    raise TraccarAuthenticationException("Unauthorized")
                if response.status == 200:
                    result = await response.json()
                    _LOGGER.debug("API response: %s", result)
                    return result

                raise TraccarResponseException(f"{response.status}: {response.reason}")
        except (TraccarAuthenticationException, TraccarResponseException):
            raise
        except asyncio.TimeoutError as exception:
            raise TraccarConnectionException("Timeouterror connecting to Traccar") from exception
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
        **kwargs: Any,
    ) -> list[ReportsEventeModel]:
        """Get events."""
        datetime_now = datetime.now(tz=timezone.utc).replace(tzinfo=None)
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
