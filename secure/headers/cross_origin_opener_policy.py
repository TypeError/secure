# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy
# https://owasp.org/www-project-secure-headers/#cross-origin-opener-policy
#
# Cross-Origin-Opener-Policy by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field
from typing import Final, Literal

from secure.headers._validation import normalize_header_value
from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName

COOPDirective = Literal[
    "unsafe-none",
    "same-origin-allow-popups",
    "same-origin",
    "noopener-allow-popups",
]

# Library default (secure-header libs often default to isolation).
# Note: per MDN/spec behavior, if the header is absent, the effective default is "unsafe-none".
DEFAULT_VALUE: Final[str] = HeaderDefaultValue.CROSS_ORIGIN_OPENER_POLICY.value


@dataclass
class CrossOriginOpenerPolicy(BaseHeader):
    """
    Builder for the ``Cross-Origin-Opener-Policy`` (COOP) HTTP response header.

    COOP lets a page opt into a dedicated browsing context group or share like with
    its opener, helping protect against XS-Leaks.

    Default header value: ``same-origin``

    Notes:
        * If this header is absent, browsers behave as if ``unsafe-none`` were set.
        * Use the fluent helpers to pick MDN-defined directives; ``value(...)`` is
          provided as an escape hatch.

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy
        - https://owasp.org/www-project-secure-headers/#cross-origin-opener-policy
    """

    header_name: str = field(init=False, default=HeaderName.CROSS_ORIGIN_OPENER_POLICY.value, repr=False)
    _default_value: str = field(init=False, default=DEFAULT_VALUE, repr=False)
    _directive: str = field(default=DEFAULT_VALUE, repr=False)

    @property
    def header_value(self) -> str:
        """Return the current `Cross-Origin-Opener-Policy` header value."""
        return self._directive

    # ---------------------------------------------------------------------
    # Escape hatches
    # ---------------------------------------------------------------------

    def value(self, directive: str) -> CrossOriginOpenerPolicy:
        """
        Set a custom value for the `Cross-Origin-Opener-Policy` header.

        This is an escape hatch. Prefer the explicit directive helpers when possible.

        Safety:
            Rejects CR/LF to avoid header-splitting. Additional validation (obs-text, etc.)
            remains the responsibility of `Secure.validate_and_normalize_headers(...)`.

        Args:
            directive: Custom header value (usually one of the COOP directives).

        Returns:
            The `CrossOriginOpenerPolicy` instance for method chaining.
        """
        v = normalize_header_value(directive, what="Cross-Origin-Opener-Policy value")
        self._directive = v
        return self

    def custom(self, directive: str) -> CrossOriginOpenerPolicy:
        """Alias for :meth:`value`."""
        return self.value(directive)

    def set(self, value: str) -> CrossOriginOpenerPolicy:
        """
        Backwards-compatible alias for :meth:`value`.

        Prefer :meth:`value` or :meth:`custom` in v2+ for consistency.
        """
        return self.value(value)

    def clear(self) -> CrossOriginOpenerPolicy:
        """
        Reset the `Cross-Origin-Opener-Policy` header to the library default value.

        Returns:
            The `CrossOriginOpenerPolicy` instance for method chaining.
        """
        self._directive = self._default_value
        return self

    # ---------------------------------------------------------------------
    # Directive helpers (fluent API)
    # ---------------------------------------------------------------------

    def unsafe_none(self) -> CrossOriginOpenerPolicy:
        """
        Set the header to `'unsafe-none'`.

        This opts out of COOP-based isolation.

        Returns:
            The `CrossOriginOpenerPolicy` instance for method chaining.
        """
        self._directive = "unsafe-none"
        return self

    def same_origin_allow_popups(self) -> CrossOriginOpenerPolicy:
        """
        Set the header to `'same-origin-allow-popups'`.

        Similar to `same-origin`, but allows opening documents with COOP `unsafe-none`
        in the same browsing context group for `Window.open()` integrations.

        Returns:
            The `CrossOriginOpenerPolicy` instance for method chaining.
        """
        self._directive = "same-origin-allow-popups"
        return self

    def same_origin(self) -> CrossOriginOpenerPolicy:
        """
        Set the header to `'same-origin'`.

        Restricts browsing context group sharing to same-origin documents that also
        use `same-origin`. Commonly used as part of cross-origin isolation.

        Returns:
            The `CrossOriginOpenerPolicy` instance for method chaining.
        """
        self._directive = "same-origin"
        return self

    def noopener_allow_popups(self) -> CrossOriginOpenerPolicy:
        """
        Set the header to `'noopener-allow-popups'`.

        This severs opener relationships while still allowing popups, and is used to
        isolate documents even from same-origin openers in some workflows.

        Returns:
            The `CrossOriginOpenerPolicy` instance for method chaining.
        """
        self._directive = "noopener-allow-popups"
        return self
