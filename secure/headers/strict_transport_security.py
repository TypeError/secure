# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
# https://owasp.org/www-project-secure-headers/#http-strict-transport-security
#
# Strict-Transport-Security by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class StrictTransportSecurity(BaseHeader):
    """
    Represents the `Strict-Transport-Security` (HSTS) HTTP header, which ensures that the application
    communication is sent over HTTPS and helps prevent man-in-the-middle attacks.

    Default header value: `max-age=31536000`

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
        - https://owasp.org/www-project-secure-headers/#http-strict-transport-security
    """

    header_name: str = HeaderName.STRICT_TRANSPORT_SECURITY.value
    _directives: list[str] = field(default_factory=list)
    _default_value: str = HeaderDefaultValue.STRICT_TRANSPORT_SECURITY.value

    @property
    def header_value(self) -> str:
        """Return the current `Strict-Transport-Security` header value.

        Returns:
            The `Strict-Transport-Security` header as a string.
        """
        return "; ".join(self._directives) if self._directives else self._default_value

    def _build(self, directive: str) -> None:
        """Add a directive to the `Strict-Transport-Security` policy if not already present.

        Args:
            directive: The directive to add to the HSTS policy.
        """
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
        Clear all directives from the `Strict-Transport-Security` header and reset to the default value.

        Returns:
            The `StrictTransportSecurity` instance for method chaining.
        """
        self._directives.clear()
        return self

    def include_subdomains(self) -> StrictTransportSecurity:
        """
        Add the `includeSubDomains` directive, which ensures that the HSTS policy is applied
        to all subdomains of the domain.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security#includeSubDomains

        Returns:
            The `StrictTransportSecurity` instance for method chaining.
        """
        self._build("includeSubDomains")
        return self

    def max_age(self, seconds: int) -> StrictTransportSecurity:
        """
        Set the `max-age` directive, instructing the browser to enforce the HTTPS-only policy
        for the specified duration in seconds.

        Args:
            seconds: The number of seconds for which the HSTS policy will be applied.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security#max-age

        Returns:
            The `StrictTransportSecurity` instance for method chaining.
        """
        self._build(f"max-age={seconds}")
        return self

    def preload(self) -> StrictTransportSecurity:
        """
        Add the `preload` directive, indicating that the site should be included in the HSTS preload list,
        instructing browsers to always load the site over HTTPS.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security#preload
            https://hstspreload.org

        Returns:
            The `StrictTransportSecurity` instance for method chaining.
        """
        self._build("preload")
        return self
