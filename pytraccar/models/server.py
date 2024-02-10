"""Model for the server response."""
from __future__ import annotations

from typing import Any, TypedDict


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
    map: str | None
    bingKey: str | None
    mapUrl: str | None
    poiLayer: str | None
    latitude: float
    longitude: float
    zoom: int
    twelveHourFormat: bool
    version: str
    forceSettings: bool
    coordinateFormat: str | None
    attributes: dict[str, Any]
    openIdEnabled: bool
    openIdForce: bool
