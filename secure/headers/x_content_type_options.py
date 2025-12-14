# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options
# https://owasp.org/www-project-secure-headers/#x-content-type-options
#
# X-Content-Type-Options by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers._validation import normalize_header_value
from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class XContentTypeOptions(BaseHeader):
    """
    Builder for the `X-Content-Type-Options` HTTP header.

    Default header value: `nosniff`

    Notes:
        * The only standardized directive is `nosniff`; other values are allowed but discouraged.

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options
        - https://owasp.org/www-project-secure-headers/#x-content-type-options
    """

    header_name: str = field(init=False, default=HeaderName.X_CONTENT_TYPE_OPTIONS.value, repr=False)
    _default_value: str = field(init=False, default=HeaderDefaultValue.X_CONTENT_TYPE_OPTIONS.value, repr=False)
    _value: str = field(default=HeaderDefaultValue.X_CONTENT_TYPE_OPTIONS.value, repr=False)

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
        self._value = normalize_header_value(value, what="X-Content-Type-Options value")
        return self

    def value(self, value: str) -> XContentTypeOptions:
        """Alias for :meth:`set` to match other headers."""
        return self.set(value)

    def clear(self) -> XContentTypeOptions:
        """
        Reset the `X-Content-Type-Options` header to its default value.

        Returns:
            The `XContentTypeOptions` instance for method chaining.
        """
        self._value = self._default_value
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
