from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class XContentTypeOptions(BaseHeader):
    """
    Represents the `X-Content-Type-Options` HTTP header, which prevents MIME-sniffing by browsers.

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options
        - https://owasp.org/www-project-secure-headers/#x-content-type-options
    """

    header_name: str = HeaderName.X_CONTENT_TYPE_OPTIONS.value
    _value: str = field(default=HeaderDefaultValue.X_CONTENT_TYPE_OPTIONS.value)

    @property
    def header_value(self) -> str:
        """Return the current `X-Content-Type-Options` header value."""
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

        This is the recommended value for preventing MIME-sniffing.

        Returns:
            The `XContentTypeOptions` instance for method chaining.
        """
        self._value = "nosniff"
        return self
