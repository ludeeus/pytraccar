"""Custom exceptions for pytraccar.

These exceptions normalize errors from HTTP and WebSocket interactions with a
Traccar server, providing a consistent surface for consumers of the library.

Typical usage::

    try:
        await client.get_devices()
    except TraccarAuthenticationException:
        # Invalid/expired token or missing permission
        ...
    except TraccarResponseException:
        # Non-200 HTTP status other than 401
        ...
    except TraccarConnectionException:
        # Network errors, timeouts, or WebSocket issues
        ...
    except TraccarException:
        # Any other unexpected error from pytraccar
        ...
"""


class TraccarException(Exception):
    """Base class for all pytraccar exceptions.

    Raised for unexpected errors that occur during API calls or WebSocket
    interactions which do not fit more specific error categories.
    """


class TraccarAuthenticationException(TraccarException):
    """Authentication failed with the Traccar API.

    Raised when the API returns HTTP 401 Unauthorized (e.g., invalid or
    expired token, or insufficient permissions).
    """


class TraccarConnectionException(TraccarException):
    """Connectivity or transport error while communicating with Traccar.

    Raised for network issues, timeouts, ``aiohttp`` client errors, or
    WebSocket closures/errors.
    """


class TraccarResponseException(TraccarException):
    """Unexpected HTTP response from the Traccar API.

    Raised for non-200 responses other than 401 (which raises
    :class:`TraccarAuthenticationException`). Includes the status code and
    reason when available.
    """
