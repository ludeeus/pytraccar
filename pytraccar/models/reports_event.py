"""Model for the reports/events response."""
from __future__ import annotations

from typing import Any, TypedDict


class ReportsEventeModel(TypedDict):
    """Model for the reports/events response.

    ref: https://www.traccar.org/api-reference/#tag/Reports/paths/~1reports~1events/get

    WARNING!: The API documentation does not state that null is
    valid for any keys, but this is not the case.
    """

    id: int
    type: str
    eventTime: str
    deviceId: int
    positionId: int
    geofenceId: int
    maintenanceId: int
    attributes: dict[str, Any]
