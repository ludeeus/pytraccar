"""Model for the geofence response."""
from __future__ import annotations

from typing import Any, TypedDict


class GeofenceModel(TypedDict):
    """Model for the geofence response.

    ref: https://www.traccar.org/api-reference/#tag/Geofences/paths/~1geofences/get

    WARNING!: The API documentation does not state that null is
    valid for any keys, but this is not the case.
    """

    id: int
    name: str
    description: str | None
    area: str
    calendarId: str
    attributes: dict[str, Any]
