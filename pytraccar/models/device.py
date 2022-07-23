"""Model for the devices response."""
from typing import Any, Optional

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
    last_update: Optional[str] = Field(alias="lastUpdate")
    position_id: int = Field(alias="positionId")
    group_id: int = Field(alias="groupId")
    phone: Optional[str]
    model: Optional[str]
    contact: Optional[str]
    category: Optional[str]
    geofence_ids: Optional[list[int]] = Field(alias="geofenceIds")
    attributes: dict[str, Any]
