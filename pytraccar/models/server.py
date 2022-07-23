"""Model for the server response."""
from typing import Any

from pydantic import BaseModel, Field


class ServerModel(BaseModel):
    """Model for the server response.

    ref: https://www.traccar.org/api-reference/#tag/Server/paths/~1server/get

    WARNING!: The API documentation does not state that null is
    valid for any keys, but this is not the case.
    """

    id: int
    registration: bool
    readonly: bool
    device_readonly: bool = Field(alias="deviceReadonly")
    limit_commands: bool = Field(alias="limitCommands")
    map: str | None
    bing_key: str | None = Field(alias="bingKey")
    map_url: str | None = Field(alias="mapUrl")
    poi_layer: str | None = Field(alias="poiLayer")
    latitude: float
    longitude: float
    zoom: int
    twelve_hour_format: bool = Field(alias="twelveHourFormat")
    version: str
    force_settings: bool = Field(alias="forceSettings")
    coordinate_format: str | None = Field(alias="coordinateFormat")
    attributes: dict[str, Any]
