"""
Update and fetch device information from Traccar.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""


class API(object):
    """A class for the Traccar API."""

    def __init__(self, loop, session):
        """Initialize the class."""
        self._loop = loop
        self._session = session

    async def dummy(self):
        """Get the local installed version."""
        print("For now this is just a placeholder")

    @property
    def test(self):
        """Return sample text."""
        return "For now this is just a placeholder."
