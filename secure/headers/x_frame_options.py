from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class XFrameOptions(BaseHeader):
    """
    Represents the `X-Frame-Options` HTTP header, which protects against clickjacking by controlling
    whether the browser should allow rendering of a page in a <frame>, <iframe>, or <object>.

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
    """

    header_name: str = HeaderName.X_FRAME_OPTIONS.value
    _value: str = field(default=HeaderDefaultValue.X_FRAME_OPTIONS.value)

    @property
    def header_value(self) -> str:
        """Return the current `X-Frame-Options` header value."""
        return self._value

    def set(self, value: str) -> XFrameOptions:
        """
        Set a custom value for the `X-Frame-Options` header.

        Args:
            value: The custom header value.

        Returns:
            The `XFrameOptions` instance for method chaining.
        """
        self._value = value
        return self

    def clear(self) -> XFrameOptions:
        """
        Reset the `X-Frame-Options` header to its default value.

        Returns:
            The `XFrameOptions` instance for method chaining.
        """
        self._value = HeaderDefaultValue.X_FRAME_OPTIONS.value
        return self

    def deny(self) -> XFrameOptions:
        """
        Set the `X-Frame-Options` header to `deny`, which prevents any site from framing the page.

        Returns:
            The `XFrameOptions` instance for method chaining.
        """
        self._value = "deny"
        return self

    def sameorigin(self) -> XFrameOptions:
        """
        Set the `X-Frame-Options` header to `sameorigin`, which allows the page to be framed
        only by pages from the same origin.

        Returns:
            The `XFrameOptions` instance for method chaining.
        """
        self._value = "sameorigin"
        return self
