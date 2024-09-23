# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
# https://owasp.org/www-project-secure-headers/#referrer-policy
#
# Referrer-Policy by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class ReferrerPolicy(BaseHeader):
    """
    Represents the `Referrer-Policy` HTTP header, which controls how much referrer information is sent with requests.

    Default header value: `strict-origin-when-cross-origin`

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
        - https://owasp.org/www-project-secure-headers/#referrer-policy
    """

    header_name: str = HeaderName.REFERRER_POLICY.value
    _directives: list[str] = field(default_factory=list)
    _default_value: str = HeaderDefaultValue.REFERRER_POLICY.value

    @property
    def header_value(self) -> str:
        """Return the current `Referrer-Policy` header value.

        Returns:
            The current Referrer-Policy header value as a string.
        """
        return ", ".join(self._directives) if self._directives else self._default_value

    def _build(self, directive: str) -> None:
        """Add a directive to the `Referrer-Policy` header if it is not already added."""
        if directive not in self._directives:
            self._directives.append(directive)

    def set(self, value: str) -> ReferrerPolicy:
        """
        Set a custom value for the `Referrer-Policy` header.

        Args:
            value: Custom header value.

        Returns:
            The `ReferrerPolicy` instance for method chaining.
        """
        self._build(value)
        return self

    def clear(self) -> ReferrerPolicy:
        """
        Clear all directives from the `Referrer-Policy` header.

        Returns:
            The `ReferrerPolicy` instance for method chaining.
        """
        self._directives.clear()
        return self

    def no_referrer(self) -> ReferrerPolicy:
        """
        Set the policy to `no-referrer`, meaning the `Referer` header will not be sent.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy/no-referrer

        Returns:
            The `ReferrerPolicy` instance for method chaining.
        """
        return self.set("no-referrer")

    def no_referrer_when_downgrade(self) -> ReferrerPolicy:
        """
        Set the policy to `no-referrer-when-downgrade`, meaning the `Referer` header will not be sent when moving from
        HTTPS to HTTP.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy/no-referrer-when-downgrade

        Returns:
            The `ReferrerPolicy` instance for method chaining.
        """
        return self.set("no-referrer-when-downgrade")

    def origin(self) -> ReferrerPolicy:
        """
        Set the policy to `origin`, meaning the `Referer` header will contain only the origin of the URL.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy/origin

        Returns:
            The `ReferrerPolicy` instance for method chaining.
        """
        return self.set("origin")

    def origin_when_cross_origin(self) -> ReferrerPolicy:
        """
        Set the policy to `origin-when-cross-origin`, meaning the `Referer` header will contain the full URL for
        same-origin requests, but only the origin for cross-origin requests.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy/origin-when-cross-origin

        Returns:
            The `ReferrerPolicy` instance for method chaining.
        """
        return self.set("origin-when-cross-origin")

    def same_origin(self) -> ReferrerPolicy:
        """
        Set the policy to `same-origin`, meaning the `Referer` header will only be sent for same-origin requests.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy/same-origin

        Returns:
            The `ReferrerPolicy` instance for method chaining.
        """
        return self.set("same-origin")

    def strict_origin(self) -> ReferrerPolicy:
        """
        Set the policy to `strict-origin`, meaning the `Referer` header will only be sent for same-origin requests,
        and not for cross-origin requests.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy/strict-origin

        Returns:
            The `ReferrerPolicy` instance for method chaining.
        """
        return self.set("strict-origin")

    def strict_origin_when_cross_origin(self) -> ReferrerPolicy:
        """
        Set the policy to `strict-origin-when-cross-origin`, meaning the `Referer` header will contain the origin for
        cross-origin requests and only the full URL for same-origin requests.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy/strict-origin-when-cross-origin

        Returns:
            The `ReferrerPolicy` instance for method chaining.
        """
        return self.set("strict-origin-when-cross-origin")

    def unsafe_url(self) -> ReferrerPolicy:
        """
        Set the policy to `unsafe-url`, meaning the `Referer` header will contain the full URL for both same-origin
        and cross-origin requests, regardless of security.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy/unsafe-url

        Returns:
            The `ReferrerPolicy` instance for method chaining.
        """
        return self.set("unsafe-url")
