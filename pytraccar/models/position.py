"""Model for the position response."""
from typing import Any, Optional, TypedDict


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
    geofenceIds: Optional[list[int]]
    longitude: float
    altitude: int
    speed: int
    course: int
    address: Optional[str]
    accuracy: int
    network: Optional[dict[str, Any]]
    attributes: dict[str, Any]
