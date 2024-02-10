"""Common helpers for tests."""
from __future__ import annotations
from dataclasses import dataclass
import os
import json
from typing import Any


def load_response(filename):
    """Load a response."""
    filename = f"{filename}.json" if "." not in filename else filename
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "responses",
        filename.lower().replace("/", "_"),
    )
    with open(path, encoding="utf-8") as fptr:
        return json.loads(fptr.read())


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
    def status(self):
        """status."""
        return self.mock_status

    @property
    def reason(self):
        """Return the reason"""
        return "unknown"

    async def json(self, **_):
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

    def release(self):
        """release."""

    def clear(self):
        """clear."""
        self.mock_data = None
        self.mock_endpoint = ""
        self.mock_headers = None
        self.mock_raises = None
        self.mock_status = 200
        
    async def wait_for_close(self):
        pass


class MockedRequests:
    """Mock request class."""

    _calls = []

    def add(self, url: str):
        """add."""
        self._calls.append(url)

    def clear(self):
        """clear."""
        self._calls.clear()

    def __repr__(self) -> str:
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
        """last url."""
        return self._calls[-1]
