from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers._validation import normalize_header_value
from secure.headers.base_header import BaseHeader


@dataclass
class CustomHeader(BaseHeader):
    """
    Wrapper for an arbitrary HTTP header.

    Default header value: provided by the caller at initialization.

    Notes:
        * Header names and values are normalized via ``normalize_header_value`` to
          prevent header injection.
        * This class keeps parity with other builders via ``value``, ``set``, and
          escape-hatch helpers so it plugs into the fluent API.

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers
    """

    header_name: str
    _value: str = field(repr=False)

    def __init__(self, header: str, value: str) -> None:
        """
        Initialize a custom header name and value.

        Args:
            header: The header name (for example, ``"X-Custom-Header"``).
            value: The header value to emit.
        """
        self.header_name = normalize_header_value(header, what="custom header name")
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
        self._value = normalize_header_value(value, what="custom header value")
        return self

    def value(self, value: str) -> CustomHeader:
        """
        Alias for :meth:`set`, provided for parity with other headers.
        """
        return self.set(value)
