from typing import List


class StrictTransportSecurity:
    """
    Ensure application communication is sent over HTTPS

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
    https://owasp.org/www-project-secure-headers/#http-strict-transport-security
    """

    def __init__(self) -> None:
        self.__policy: List[str] = []
        self.header = "Strict-Transport-Security"
        self.value = "max-age=63072000; includeSubdomains"

    def _build(self, directive: str) -> None:
        self.__policy.append(directive)
        self.value = "; ".join(self.__policy)

    def set(self, value: str) -> "StrictTransportSecurity":
        """Set custom value for `Strict-Transport-Security` header

        :param value: custom header value
        :type value: str
        :return: StrictTransportSecurity class
        :rtype: StrictTransportSecurity
        """
        self._build(value)
        return self

    def include_subdomains(self) -> "StrictTransportSecurity":
        """Include subdomains to HSTS policy [Optional]

        :return: [description]
        :rtype: [type]
        """
        self._build("includeSubDomains")
        return self

    def max_age(self, seconds: int) -> "StrictTransportSecurity":
        """Instruct the browser to remember HTTPS preference
        until time (seconds) expires.

        :param seconds: time in seconds
        :type seconds: str
        :return: StrictTransportSecurity class
        :rtype: StrictTransportSecurity
        """
        self._build(f"max-age={seconds}")
        return self

    def preload(self) -> "StrictTransportSecurity":
        """Instruct browser to always use HTTPS [Optional]

        Please see:
        https://hstspreload.org

        :return: StrictTransportSecurity class
        :rtype: StrictTransportSecurity
        """
        self._build("preload")
        return self
