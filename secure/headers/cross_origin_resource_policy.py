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

from secure.headers._validation import normalize_header_value
from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName

CorpDirective = Literal["same-site", "same-origin", "cross-origin"]

_ALLOWED: Final[frozenset[str]] = frozenset({"same-site", "same-origin", "cross-origin"})


@dataclass
class CrossOriginResourcePolicy(BaseHeader):
    """
    Builder for the ``Cross-Origin-Resource-Policy`` (CORP) HTTP response header.

    CORP expresses the resource owner's intent for which origins may load this
    resource, with MDN documenting ``same-site``, ``same-origin``, and
    ``cross-origin`` directives.

    Default header value: `same-origin`

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Resource-Policy
        - https://resourcepolicy.fyi/
        - https://owasp.org/www-project-secure-headers/#cross-origin-resource-policy
    """

    header_name: str = field(init=False, default=HeaderName.CROSS_ORIGIN_RESOURCE_POLICY.value, repr=False)
    _default_value: str = field(init=False, default=HeaderDefaultValue.CROSS_ORIGIN_RESOURCE_POLICY.value, repr=False)
    _value: str = field(default_factory=lambda: HeaderDefaultValue.CROSS_ORIGIN_RESOURCE_POLICY.value, repr=False)

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
        self._value = self._default_value
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
        v = normalize_header_value(value, what="Cross-Origin-Resource-Policy value")

        # Canonicalize known directives (case-insensitive) to the MDN tokens.
        lc = v.lower()
        if lc in _ALLOWED:
            return lc

        # Unknown: keep trimmed string verbatim as an escape hatch.
        return v
