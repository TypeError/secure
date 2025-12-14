from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers._validation import normalize_header_value
from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class Server(BaseHeader):
    """
    Builder for the ``Server`` HTTP response header.

    Default header value: ``""``

    Notes:
        * The default is intentionally empty to avoid leaking server details.
        * Callers can override this value for compatibility with legacy tooling.

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server
        - https://owasp.org/www-project-secure-headers/
    """

    header_name: str = field(init=False, default=HeaderName.SERVER.value, repr=False)
    _default_value: str = field(init=False, default=HeaderDefaultValue.SERVER.value, repr=False)
    _value: str = field(default=HeaderDefaultValue.SERVER.value, repr=False)

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
        self._value = normalize_header_value(value, what="Server value")
        return self

    def value(self, value: str) -> Server:
        """Alias for :meth:`set` (kept for feature parity with other headers)."""
        return self.set(value)

    def clear(self) -> Server:
        """
        Reset the `Server` header value to its default (`NULL`).

        This method clears any custom value that has been set for the `Server` header
        and reverts it to the default, which is a more secure value that hides server details.

        Returns:
            Server: The current instance, allowing for method chaining.
        """
        self._value = self._default_value
        return self
