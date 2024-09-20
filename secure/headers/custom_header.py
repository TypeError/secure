from __future__ import annotations  # type: ignore

from dataclasses import dataclass

from secure.headers.base_header import BaseHeader


@dataclass
class CustomHeader(BaseHeader):
    """
    Represents a custom HTTP header.

    Allows users to set custom headers with arbitrary names and values.
    """

    header_name: str
    _value: str

    def __init__(self, header: str, value: str) -> None:
        """
        Initialize the custom header with a name and value.

        Args:
            header: The name of the custom header.
            value: The value for the custom header.
        """
        self.header_name = header
        self._value = value

    @property
    def header_value(self) -> str:
        """Return the current custom header value."""
        return self._value

    def set(self, value: str) -> CustomHeader:
        """
        Set a new value for the custom header.

        Args:
            value: The new value for the header.

        Returns:
            The `CustomHeader` instance for method chaining.
        """
        self._value = value
        return self
