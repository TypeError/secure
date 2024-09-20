from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class StrictTransportSecurity(BaseHeader):
    """
    Represents the `Strict-Transport-Security` (HSTS) HTTP header, which ensures that the application
    communication is sent over HTTPS and prevents man-in-the-middle attacks.

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
        - https://owasp.org/www-project-secure-headers/#http-strict-transport-security
    """

    header_name: str = HeaderName.STRICT_TRANSPORT_SECURITY.value
    _directives: list[str] = field(default_factory=list)
    _default_value: str = HeaderDefaultValue.STRICT_TRANSPORT_SECURITY.value

    @property
    def header_value(self) -> str:
        """Return the current `Strict-Transport-Security` header value."""
        return "; ".join(self._directives) if self._directives else self._default_value

    def _build(self, directive: str) -> None:
        """Add a directive to the `Strict-Transport-Security` policy if not already present."""
        if directive not in self._directives:
            self._directives.append(directive)

    def set(self, value: str) -> StrictTransportSecurity:
        """
        Set a custom value for the `Strict-Transport-Security` header, replacing any existing directives.

        Args:
            value: The custom header value.

        Returns:
            The `StrictTransportSecurity` instance for method chaining.
        """
        self._directives = [value]
        return self

    def clear(self) -> StrictTransportSecurity:
        """
        Clear the current directives and reset to the default value.

        Returns:
            The `StrictTransportSecurity` instance for method chaining.
        """
        self._directives.clear()
        return self

    def include_subdomains(self) -> StrictTransportSecurity:
        """
        Include all subdomains in the HSTS policy.

        Returns:
            The `StrictTransportSecurity` instance for method chaining.
        """
        self._build("includeSubDomains")
        return self

    def max_age(self, seconds: int) -> StrictTransportSecurity:
        """
        Set the `max-age` directive, instructing the browser to remember the HTTPS preference
        for the specified time (in seconds).

        Args:
            seconds: The duration in seconds for which the HSTS policy is enforced.

        Returns:
            The `StrictTransportSecurity` instance for method chaining.
        """
        self._build(f"max-age={seconds}")
        return self

    def preload(self) -> StrictTransportSecurity:
        """
        Add the `preload` directive, indicating that the site should always be loaded over HTTPS
        and included in the HSTS preload list.

        Returns:
            The `StrictTransportSecurity` instance for method chaining.
        """
        self._build("preload")
        return self
