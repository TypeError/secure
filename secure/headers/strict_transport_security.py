from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class StrictTransportSecurity(BaseHeader):
    """
    Ensure application communication is sent over HTTPS

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
    https://owasp.org/www-project-secure-headers/#http-strict-transport-security
    """

    _policy: list[str] = field(default_factory=list)
    header_name: str = HeaderName.STRICT_TRANSPORT_SECURITY.value
    header_value: str = HeaderDefaultValue.STRICT_TRANSPORT_SECURITY.value

    def _build(self, directive: str) -> None:
        self._policy.append(directive)
        self.header_value = "; ".join(self._policy)

    def set(self, value: str) -> StrictTransportSecurity:
        """Set custom value for `Strict-Transport-Security` header

        :param value: custom header value
        :type value: str
        :return: StrictTransportSecurity class
        :rtype: StrictTransportSecurity
        """
        self._build(value)
        return self

    def include_subdomains(self) -> StrictTransportSecurity:
        """Include subdomains to HSTS policy [Optional]

        :return: [description]
        :rtype: [type]
        """
        self._build("includeSubDomains")
        return self

    def max_age(self, seconds: int) -> StrictTransportSecurity:
        """Instruct the browser to remember HTTPS preference
        until time (seconds) expires.

        :param seconds: time in seconds
        :type seconds: str
        :return: StrictTransportSecurity class
        :rtype: StrictTransportSecurity
        """
        self._build(f"max-age={seconds}")
        return self

    def preload(self) -> StrictTransportSecurity:
        """Instruct browser to always use HTTPS [Optional]

        Please see:
        https://hstspreload.org

        :return: StrictTransportSecurity class
        :rtype: StrictTransportSecurity
        """
        self._build("preload")
        return self
