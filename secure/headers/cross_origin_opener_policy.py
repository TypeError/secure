# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy
# https://owasp.org/www-project-secure-headers/#cross-origin-opener-policy
#
# Cross-Origin-Opener-Policy by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/


from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class CrossOriginOpenerPolicy(BaseHeader):
    """
    Represents the `Cross-Origin-Opener-Policy` (COOP) HTTP header, which helps process-isolate your document
    to prevent attackers from accessing your global object through popups and reduce cross-origin attacks (XS-Leaks).

    Default header value: `same-origin`

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy
        - https://owasp.org/www-project-secure-headers/#cross-origin-opener-policy
    """

    header_name: str = HeaderName.CROSS_ORIGIN_OPENER_POLICY.value
    _directive: str = field(default=HeaderDefaultValue.CROSS_ORIGIN_OPENER_POLICY.value)

    @property
    def header_value(self) -> str:
        """Return the current `Cross-Origin-Opener-Policy` header value.

        Returns:
            The current COOP policy as a string.
        """
        return self._directive

    def set(self, value: str) -> CrossOriginOpenerPolicy:
        """
        Set a custom value for the `Cross-Origin-Opener-Policy` header.

        Args:
            value: Custom header value.

        Returns:
            The `CrossOriginOpenerPolicy` instance for method chaining.
        """
        self._directive = value
        return self

    def clear(self) -> CrossOriginOpenerPolicy:
        """
        Reset the `Cross-Origin-Opener-Policy` header to its default value.

        Returns:
            The `CrossOriginOpenerPolicy` instance for method chaining.
        """
        self._directive = HeaderDefaultValue.CROSS_ORIGIN_OPENER_POLICY.value
        return self

    def unsafe_none(self) -> CrossOriginOpenerPolicy:
        """
        Set the header to `'unsafe-none'`.

        This allows the document to be added to its opener’s browsing context group unless the opener has a COOP
        of `same-origin` or `same-origin-allow-popups` (this is the default value).

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy

        Returns:
            The `CrossOriginOpenerPolicy` instance for method chaining.
        """
        self._directive = "unsafe-none"
        return self

    def same_origin_allow_popups(self) -> CrossOriginOpenerPolicy:
        """
        Set the header to `'same-origin-allow-popups'`.

        This allows retaining references to newly opened windows or tabs that either don’t set COOP or opt out of isolation
        by setting a COOP of `unsafe-none`.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy

        Returns:
            The `CrossOriginOpenerPolicy` instance for method chaining.
        """
        self._directive = "same-origin-allow-popups"
        return self

    def same_origin(self) -> CrossOriginOpenerPolicy:
        """
        Set the header to `'same-origin'`.

        This isolates the browsing context exclusively to same-origin documents, preventing cross-origin documents from
        being loaded in the same context.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy

        Returns:
            The `CrossOriginOpenerPolicy` instance for method chaining.
        """
        self._directive = "same-origin"
        return self
