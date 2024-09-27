# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
# https://owasp.org/www-project-secure-headers/#x-frame-options
#
# X-Frame-Options by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class XFrameOptions(BaseHeader):
    """
    Represents the `X-Frame-Options` HTTP header, which protects against clickjacking by controlling
    whether the browser should allow rendering of a page in a <frame>, <iframe>, or <object>.

    Default header value: `SAMEORIGIN`

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
        - https://owasp.org/www-project-secure-headers/#x-frame-options
    """

    header_name: str = HeaderName.X_FRAME_OPTIONS.value
    _value: str = field(default=HeaderDefaultValue.X_FRAME_OPTIONS.value)

    @property
    def header_value(self) -> str:
        """Return the current `X-Frame-Options` header value.

        Returns:
            The current `X-Frame-Options` header value as a string.
        """
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
        Set the `X-Frame-Options` header to `DENY`, which prevents any site from framing the page.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options

        Returns:
            The `XFrameOptions` instance for method chaining.
        """
        self._value = "DENY"
        return self

    def sameorigin(self) -> XFrameOptions:
        """
        Set the `X-Frame-Options` header to `SAMEORIGIN`, which allows the page to be framed
        only by pages from the same origin.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options

        Returns:
            The `XFrameOptions` instance for method chaining.
        """
        self._value = "SAMEORIGIN"
        return self
