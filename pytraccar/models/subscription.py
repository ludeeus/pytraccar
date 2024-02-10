"""Model for the subscription."""
from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from .device import DeviceModel
    from .position import PositionModel
    from .reports_event import ReportsEventeModel


class SubscriptionStatus(StrEnum):
    """Model for the subscription status."""

    CONNECTED = "connected"
    CONNECTING = "connecting"
    DISCONNECTED = "disconnected"
    ERROR = "error"


class SubscriptionData(TypedDict):
    """Model for the subscription data.

    ref: https://www.traccar.org/traccar-api/
    """

    devices: list[DeviceModel] | None
    positions: list[PositionModel] | None
    events: list[ReportsEventeModel] | None
