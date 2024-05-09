class XContentTypeOptions:
    """Prevent MIME-sniffing

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options
    https://owasp.org/www-project-secure-headers/#x-content-type-options
    """

    def __init__(self) -> None:
        self.header = "X-Content-Type-Options"
        self.value = "nosniff"

    def set(self, value: str) -> "XContentTypeOptions":
        """Set custom value for `X-Content-Type-Options` header

        :param value: custom header value
        :type value: str
        :return: XContentTypeOptions class
        :rtype: XContentTypeOptions
        """
        self.value = value
        return self
