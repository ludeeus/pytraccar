"""Model for the server response."""
from typing import Any, Optional, TypedDict


class ServerModel(TypedDict):
    """Model for the server response.

    ref: https://www.traccar.org/api-reference/#tag/Server/paths/~1server/get

    WARNING!: The API documentation does not state that null is
    valid for any keys, but this is not the case.
    """

    id: int
    registration: bool
    readonly: bool
    deviceReadonly: bool
    limitCommands: bool
    map: Optional[str]
    bingKey: Optional[str]
    mapUrl: Optional[str]
    poiLayer: Optional[str]
    latitude: float
    longitude: float
    zoom: int
    twelveHourFormat: bool
    version: str
    forceSettings: bool
    coordinateFormat: Optional[str]
    attributes: dict[str, Any]
    openIdEnabled: bool
    openIdForce: bool
