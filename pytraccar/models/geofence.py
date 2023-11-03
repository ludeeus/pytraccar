"""Model for the geofence response."""
from typing import Any, Optional, TypedDict


class GeofenceModel(TypedDict):
    """Model for the geofence response.

    ref: https://www.traccar.org/api-reference/#tag/Geofences/paths/~1geofences/get

    WARNING!: The API documentation does not state that null is
    valid for any keys, but this is not the case.
    """

    id: int
    name: str
    description: Optional[str]
    area: str
    calendarId: str
    attributes: dict[str, Any]
