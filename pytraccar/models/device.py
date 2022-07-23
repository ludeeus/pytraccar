"""Model for the devices response."""
from typing import Any

from pydantic import BaseModel, Field


class DeviceModel(BaseModel):
    """Model for the devices response.

    ref: https://www.traccar.org/api-reference/#tag/Devices/paths/~1devices/get

    WARNING!: The API documentation does not state that null is
    valid for any keys, but this is not the case.
    """

    id: int
    name: str
    unique_id: str = Field(alias="uniqueId")
    status: str
    disabled: bool
    last_update: str | None = Field(alias="lastUpdate")
    position_id: int = Field(alias="positionId")
    group_id: int = Field(alias="groupId")
    phone: str | None
    model: str | None
    contact: str | None
    category: str | None
    geofence_ids: list[int] | None = Field(alias="geofenceIds")
    attributes: dict[str, Any]
