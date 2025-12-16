# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options
# https://owasp.org/www-project-secure-headers/#x-frame-options
#
# X-Frame-Options by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers._validation import normalize_header_value
from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class XFrameOptions(BaseHeader):
    """
    Builder for the `X-Frame-Options` HTTP response header.

    Default header value: `SAMEORIGIN`

    Notes:
        * Consider CSP `frame-ancestors` for richer framing controls.
        * This header is only processed when sent as an HTTP response header.

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options
        - https://owasp.org/www-project-secure-headers/#x-frame-options
    """

    header_name: str = field(init=False, default=HeaderName.X_FRAME_OPTIONS.value, repr=False)
    _default_value: str = field(init=False, default=HeaderDefaultValue.X_FRAME_OPTIONS.value, repr=False)
    _value: str = field(default=HeaderDefaultValue.X_FRAME_OPTIONS.value, repr=False)

    @property
    def header_value(self) -> str:
        """Return the current `X-Frame-Options` header value."""
        return self._value

    # ---------------------------------------------------------------------
    # Escape hatches
    # ---------------------------------------------------------------------

    def value(self, value: str) -> XFrameOptions:
        """Set a custom header value.

        Use this when you already have a fully-formed header value and want to bypass
        directive helpers.

        Notes:
            This method rejects CR/LF characters to avoid header injection. Any further
            validation/normalization belongs in `Secure.validate_and_normalize_headers(...)`.

        Args:
            value: The complete header value.

        Returns:
            The `XFrameOptions` instance for method chaining.
        """
        self._value = normalize_header_value(value, what="X-Frame-Options value")
        return self

    def set(self, value: str) -> XFrameOptions:
        """Alias for `value(...)` (backwards-compatible)."""
        return self.value(value)

    def custom(self, value: str) -> XFrameOptions:
        """Alias for `value(...)`."""
        return self.value(value)

    def clear(self) -> XFrameOptions:
        """Reset the `X-Frame-Options` header to its default value (`SAMEORIGIN`)."""
        self._value = self._default_value
        return self

    # ---------------------------------------------------------------------
    # Directives
    # ---------------------------------------------------------------------

    def deny(self) -> XFrameOptions:
        """Set the directive to `DENY`.

        The page cannot be displayed in a frame, regardless of the site attempting to do so.
        """
        self._value = "DENY"
        return self

    def sameorigin(self) -> XFrameOptions:
        """Set the directive to `SAMEORIGIN`.

        The page can only be displayed if all ancestor frames have the same origin as the page.
        """
        self._value = "SAMEORIGIN"
        return self

    def allow_from(self, origin: str) -> XFrameOptions:
        """Set the (obsolete) `ALLOW-FROM <origin>` directive.

        Warning:
            This is an obsolete directive. Modern browsers that encounter response headers
            with this directive will ignore the header completely. Use CSP `frame-ancestors`
            instead.

        Args:
            origin: An origin value (for example, `https://example.com`).

        Returns:
            The `XFrameOptions` instance for method chaining.
        """
        # Keep construction minimal; validity of the origin is out-of-scope for this module.
        return self.value(f"ALLOW-FROM {origin.strip()}")
