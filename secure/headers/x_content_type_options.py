from __future__ import annotations  # type: ignore

from dataclasses import dataclass

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class XContentTypeOptions(BaseHeader):
    """Prevent MIME-sniffing

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options
    https://owasp.org/www-project-secure-headers/#x-content-type-options
    """

    header_name: str = HeaderName.X_CONTENT_TYPE_OPTIONS.value
    header_value: str = HeaderDefaultValue.X_CONTENT_TYPE_OPTIONS.value

    def set(self, value: str) -> XContentTypeOptions:
        """Set custom value for `X-Content-Type-Options` header

        :param value: custom header value
        :type value: str
        :return: XContentTypeOptions class
        :rtype: XContentTypeOptions
        """
        self.header_value = value
        return self
