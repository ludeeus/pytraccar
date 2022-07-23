"""Custom exceptions for pytraccar."""


class TraccarException(Exception):
    """Base class for all pytraccar exceptions."""


class TraccarAuthenticationException(TraccarException):
    """Exception for authentication errors."""


class TraccarConnectionException(TraccarException):
    """Exception for connection errors."""


class TraccarResponseException(TraccarException):
    """Exception for response errors."""
