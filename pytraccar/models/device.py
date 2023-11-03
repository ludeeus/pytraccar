"""Model for the devices response."""
from typing import Any, Optional, TypedDict


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
    lastUpdate: Optional[str]
    positionId: int
    groupId: int
    phone: Optional[str]
    model: Optional[str]
    contact: Optional[str]
    category: Optional[str]
    attributes: dict[str, Any]
