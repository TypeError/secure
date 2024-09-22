from __future__ import annotations  # type: ignore

from dataclasses import dataclass

from secure.headers.base_header import BaseHeader


@dataclass
class CustomHeader(BaseHeader):
    """
    Represents a custom HTTP header.

    This class allows users to create and manage custom HTTP headers
    with arbitrary names and values. It is useful for adding non-standard
    headers to HTTP responses or requests.
    """

    header_name: str
    _value: str

    def __init__(self, header: str, value: str) -> None:
        """
        Initialize the `CustomHeader` with a custom header name and value.

        Args:
            header: The name of the custom header (e.g., "X-Custom-Header").
            value: The value associated with the custom header.
        """
        self.header_name = header
        self._value = value

    @property
    def header_value(self) -> str:
        """
        Retrieve the current value of the custom header.

        Returns:
            str: The value of the custom header.
        """
        return self._value

    def set(self, value: str) -> CustomHeader:
        """
        Update the value of the custom header.

        This method allows the value of the custom header to be updated
        and supports method chaining.

        Args:
            value: The new value to set for the custom header.

        Returns:
            CustomHeader: The current instance, allowing for method chaining.
        """
        self._value = value
        return self
