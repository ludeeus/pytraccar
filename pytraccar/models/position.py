"""Model for the position response."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class PositionModel(BaseModel):
    """Model for the position response.

    ref: https://www.traccar.org/api-reference/#tag/Devices/paths/~1devices/get

    WARNING!: The API documentation does not state that null is
    valid for any keys, but this is not the case.
    """

    id: int
    device_id: int = Field(alias="deviceId")
    protocol: str
    device_time: str = Field(alias="deviceTime")
    fix_time: str = Field(alias="fixTime")
    server_time: str = Field(alias="serverTime")
    outdated: bool
    valid: bool
    latitude: float
    longitude: float
    altitude: int
    speed: int
    course: int
    address: str | None
    accuracy: int
    network: dict[str, Any] | None
    attributes: dict[str, Any]