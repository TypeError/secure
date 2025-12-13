# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Resource-Policy
# https://owasp.org/www-project-secure-headers/#cross-origin-resource-policy
#
# Cross-Origin-Resource-Policy by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, Literal

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName

CorpDirective = Literal["same-site", "same-origin", "cross-origin"]

_ALLOWED: Final[frozenset[str]] = frozenset({"same-site", "same-origin", "cross-origin"})


@dataclass
class CrossOriginResourcePolicy(BaseHeader):
    """
    Represents the `Cross-Origin-Resource-Policy` (CORP) HTTP response header.

    CORP expresses the *resource owner's policy* for what sites/origins may load
    this resource. MDN documents three directives:

    - `same-site`: resources may be loaded only from the same site
    - `same-origin`: resources may be loaded only from the same origin
    - `cross-origin`: resources may be loaded by any origin/website

    Library default header value: `same-origin`

    Minimal example:
        corp = CrossOriginResourcePolicy().same_origin()
        print(corp.header_name)   # 'Cross-Origin-Resource-Policy'
        print(corp.header_value)  # 'same-origin'

    With `Secure`:
        # secure = Secure(corp=CrossOriginResourcePolicy().same_site())

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Resource-Policy
        - https://resourcepolicy.fyi/  (more examples)
        - https://owasp.org/www-project-secure-headers/#cross-origin-resource-policy
    """

    # Always emit the canonical header name for this module.
    header_name: str = field(init=False, default=HeaderName.CROSS_ORIGIN_RESOURCE_POLICY.value)

    # Library default (recommended) value.
    _value: str = field(default_factory=lambda: HeaderDefaultValue.CROSS_ORIGIN_RESOURCE_POLICY.value)

    @property
    def header_value(self) -> str:
        """Return the current header value."""
        return self._value

    def clear(self) -> CrossOriginResourcePolicy:
        """
        Reset this header to the library default value.

        Returns:
            The `CrossOriginResourcePolicy` instance for method chaining.
        """
        self._value = HeaderDefaultValue.CROSS_ORIGIN_RESOURCE_POLICY.value
        return self

    def value(self, value: str | CorpDirective) -> CrossOriginResourcePolicy:
        """
        Set the header value.

        This is the preferred "escape hatch" API. For known CORP directives, the
        stored value is canonicalized to the standard lowercase token.

        Args:
            value:
                Typically one of `same-origin`, `same-site`, or `cross-origin`.
                Other values are accepted as-is (after trimming), but are not
                described by MDN.

        Returns:
            The `CrossOriginResourcePolicy` instance for method chaining.

        Raises:
            ValueError: if the value contains CR/LF characters.
        """
        self._value = self._normalize_value(str(value))
        return self

    # Backwards-compatible alias (keep for existing callers).
    def set(self, value: str) -> CrossOriginResourcePolicy:
        """
        Backwards-compatible alias for `value(...)`.

        Prefer `value(...)` going forward.
        """
        return self.value(value)

    def same_origin(self) -> CrossOriginResourcePolicy:
        """Restrict resource loading to the same origin."""
        self._value = "same-origin"
        return self

    def same_site(self) -> CrossOriginResourcePolicy:
        """Allow resource loading from the same site."""
        self._value = "same-site"
        return self

    def cross_origin(self) -> CrossOriginResourcePolicy:
        """Allow resource loading from any origin."""
        self._value = "cross-origin"
        return self

    @staticmethod
    def _normalize_value(value: str) -> str:
        v = value.strip()

        # Guard against header injection when callers skip Secure.validate_and_normalize_headers().
        if "\r" in v or "\n" in v:
            raise ValueError("Cross-Origin-Resource-Policy value must not contain CR/LF characters")

        # Canonicalize known directives (case-insensitive) to the MDN tokens.
        lc = v.lower()
        if lc in _ALLOWED:
            return lc

        # Unknown: keep trimmed string verbatim as an escape hatch.
        return v
