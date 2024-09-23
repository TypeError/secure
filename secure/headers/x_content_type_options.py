# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options
# https://owasp.org/www-project-secure-headers/#x-content-type-options
#
# X-Content-Type-Options by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class XContentTypeOptions(BaseHeader):
    """
    Represents the `X-Content-Type-Options` HTTP header, which prevents MIME-sniffing by browsers.

    Default header value: `nosniff`

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options
        - https://owasp.org/www-project-secure-headers/#x-content-type-options
    """

    header_name: str = HeaderName.X_CONTENT_TYPE_OPTIONS.value
    _value: str = field(default=HeaderDefaultValue.X_CONTENT_TYPE_OPTIONS.value)

    @property
    def header_value(self) -> str:
        """Return the current `X-Content-Type-Options` header value.

        Returns:
            The current `X-Content-Type-Options` header value as a string.
        """
        return self._value

    def set(self, value: str) -> XContentTypeOptions:
        """
        Set a custom value for the `X-Content-Type-Options` header.

        Args:
            value: The custom header value.

        Returns:
            The `XContentTypeOptions` instance for method chaining.
        """
        self._value = value
        return self

    def clear(self) -> XContentTypeOptions:
        """
        Reset the `X-Content-Type-Options` header to its default value.

        Returns:
            The `XContentTypeOptions` instance for method chaining.
        """
        self._value = HeaderDefaultValue.X_CONTENT_TYPE_OPTIONS.value
        return self

    def nosniff(self) -> XContentTypeOptions:
        """
        Set the `X-Content-Type-Options` header to `nosniff`.

        This value tells the browser to block requests for certain content types and prevents MIME-sniffing attacks.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options

        Returns:
            The `XContentTypeOptions` instance for method chaining.
        """
        self._value = "nosniff"
        return self
