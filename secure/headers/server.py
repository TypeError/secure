from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class Server(BaseHeader):
    """
    Represents the `Server` HTTP header, which provides information about the software used by the server.

    Header default value: `""`

    By default, the `Server` header is set to an empty value to obscure specific server details
    and enhance security by avoiding unnecessary exposure of server information.
    """

    header_name: str = HeaderName.SERVER.value
    _value: str = field(default=HeaderDefaultValue.SERVER.value)

    @property
    def header_value(self) -> str:
        """
        Retrieve the current value of the `Server` header.

        Returns:
            str: The current value of the `Server` header.
        """
        return self._value

    def set(self, value: str) -> Server:
        """
        Set a custom value for the `Server` header.

        This allows you to override the default `Server` header value with a custom value
        that will be included in HTTP responses.

        Args:
            value: The custom value to set for the `Server` header.

        Returns:
            Server: The current instance, allowing for method chaining.
        """
        self._value = value
        return self

    def clear(self) -> Server:
        """
        Reset the `Server` header value to its default (`NULL`).

        This method clears any custom value that has been set for the `Server` header
        and reverts it to the default, which is a more secure value that hides server details.

        Returns:
            Server: The current instance, allowing for method chaining.
        """
        self._value = HeaderDefaultValue.SERVER.value
        return self
