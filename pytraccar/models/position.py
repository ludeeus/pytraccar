"""Model for the position response."""
from __future__ import annotations

from typing import Any, TypedDict


class PositionModel(TypedDict):
    """Model for the position response.

    ref: https://www.traccar.org/api-reference/#tag/Devices/paths/~1devices/get

    WARNING!: The API documentation does not state that null is
    valid for any keys, but this is not the case.
    """

    id: int
    deviceId: int
    protocol: str
    deviceTime: str
    fixTime: str
    serverTime: str
    outdated: bool
    valid: bool
    latitude: float
    geofenceIds: list[int] | None
    longitude: float
    altitude: int
    speed: int
    course: int
    address: str | None
    accuracy: int
    network: dict[str, Any] | None
    attributes: dict[str, Any]
