import warnings


class XXSSProtection:
    """
    Enable browser Cross-Site Scripting filters

    **Deprecated**

    Recommended to utilize `Content-Security-Policy`
    instead of the legacy `X-XSS-Protection` header.

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection
    https://owasp.org/www-project-secure-headers/#x-xss-protection
    """

    def __init__(self) -> None:
        self.header = "X-XSS-Protection"
        self.value = "0"

    def set(self, value: str) -> "XXSSProtection":
        """Set custom value for `X-XSS-Protection` header

        :param value: custom header value
        :type value: str
        :return: XXSSProtection class
        :rtype: XXSSProtection
        """
        warnings.warn(
            "Recommended to utilize Content-Security-Policy",
            DeprecationWarning,
        )
        self.value = value
        return self
