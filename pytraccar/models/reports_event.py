"""Model for the reports/events response."""
from typing import Any

from pydantic import BaseModel, Field


class ReportsEventeModel(BaseModel):
    """Model for the reports/events response.

    ref: https://www.traccar.org/api-reference/#tag/Reports/paths/~1reports~1events/get

    WARNING!: The API documentation does not state that null is
    valid for any keys, but this is not the case.
    """

    id: int
    type: str
    event_time: str = Field(alias="eventTime")
    device_id: int = Field(alias="deviceId")
    position_id: int = Field(alias="positionId")
    geofence_id: int = Field(alias="geofenceId")
    maintenance_id: int = Field(alias="maintenanceId")
    attributes: dict[str, Any]
