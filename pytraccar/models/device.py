"""Model for the devices response."""
from __future__ import annotations

from typing import Any, TypedDict


class DeviceModel(TypedDict):
    """Model for the devices response.

    ref: https://www.traccar.org/api-reference/#tag/Devices/paths/~1devices/get

    WARNING!: The API documentation does not state that null is
    valid for any keys, but this is not the case.
    """

    id: int
    name: str
    uniqueId: str
    status: str
    disabled: bool
    lastUpdate: str | None
    positionId: int
    groupId: int
    phone: str | None
    model: str | None
    contact: str | None
    category: str | None
    attributes: dict[str, Any]
