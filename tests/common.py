"""Common helpers for tests."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from aiohttp import WSMsgType


class WSMessage:
    """WSMessage."""

    def __init__(self, messagetype: WSMsgType, json: dict | None = None) -> None:
        """Initialize."""
        self.type = messagetype
        self._json = json

    def json(self) -> dict | None:
        """json."""
        return self._json


def load_response(filename: str) -> dict[str, Any]:
    """Load a response."""
    filename = f"{filename}.json" if "." not in filename else filename
    path = Path(
        Path.resolve(Path(__file__)).parent,
        "responses",
        filename.lower().replace("/", "_"),
    )
    with path.open(encoding="utf-8") as fptr:
        return json.loads(fptr.read())


class WSMessageHandler:
    """WSMessageHandler."""

    def __init__(self) -> None:
        """Initialize."""
        self.messages = []

    def add(self, msg: WSMessage) -> None:
        """Add."""
        self.messages.append(msg)

    def get(self) -> WSMessage:
        """Get."""
        return (
            self.messages.pop(0)
            if self.messages
            else WSMessage(messagetype=WSMsgType.CLOSED)
        )


@dataclass
class MockResponse:
    """Mock response class."""

    _count = 0

    mock_data: Any | None = None
    mock_data_list: list[Any] | None = None
    mock_endpoint: str = ""
    mock_headers: dict[str, str] | None = None
    mock_raises: BaseException | None = None
    mock_status: int = 200

    @property
    def status(self) -> int:
        """status."""
        return self.mock_status

    @property
    def reason(self) -> str:
        """Return the reason."""
        return "unknown"

    async def json(self, **_: Any) -> Any:
        """json."""
        if self.mock_raises is not None:
            raise self.mock_raises  # pylint: disable=raising-bad-type
        if self.mock_data_list:
            data = self.mock_data_list[self._count]
            self._count += 1
            return data
        if self.mock_data is not None:
            return self.mock_data
        return load_response(self.mock_endpoint)

    def release(self) -> None:
        """release."""

    def clear(self) -> None:
        """clear."""
        self.mock_data = None
        self.mock_endpoint = ""
        self.mock_headers = None
        self.mock_raises = None
        self.mock_status = 200

    async def wait_for_close(self) -> None:
        """wait_for_close."""


class MockedRequests:
    """Mock request class."""

    def __init__(self) -> None:
        """Initialize."""
        self._calls = []

    def add(self, url: str) -> None:
        """add."""
        self._calls.append(url)

    def clear(self) -> None:
        """clear."""
        self._calls.clear()

    def __repr__(self) -> str:
        """repr."""
        return f"<MockedRequests: {self._calls}>"

    @property
    def called(self) -> int:
        """count."""
        return len(self._calls)

    def has(self, string: str) -> bool:
        """has."""
        return bool([entry for entry in self._calls if string in entry])

    @property
    def last_request(self) -> MockResponse:
        """Last url."""
        return self._calls[-1]
