from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class Server(BaseHeader):
    """
    Represents the `Server` HTTP header, which provides information about the software used by the server.

    By default, the `Server` header is set to a generic value to hide specific server details.
    """

    header_name: str = HeaderName.SERVER.value
    _value: str = field(default=HeaderDefaultValue.SERVER.value)

    @property
    def header_value(self) -> str:
        """Return the current `Server` header value."""
        return self._value

    def set(self, value: str) -> Server:
        """
        Set a custom value for the `Server` header.

        Args:
            value: The custom value for the `Server` header.

        Returns:
            The `Server` instance for method chaining.
        """
        self._value = value
        return self

    def clear(self) -> Server:
        """
        Reset the `Server` header value to its default.

        Returns:
            The `Server` instance for method chaining.
        """
        self._value = HeaderDefaultValue.SERVER.value
        return self
