# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy
# https://owasp.org/www-project-secure-headers/#cross-origin-embedder-policy
#
# Cross-Origin-Embedder-Policy by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field
from typing import Literal

from secure.headers._validation import normalize_header_value
from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName

COEPDirective = Literal["unsafe-none", "require-corp", "credentialless"]


@dataclass
class CrossOriginEmbedderPolicy(BaseHeader):
    """
    Builder for the ``Cross-Origin-Embedder-Policy`` (COEP) HTTP response header.

    COEP controls how the document embeds and loads cross-origin resources, with
    directives that range from no isolation (``unsafe-none``) to strict isolation
    (``require-corp``) or credentialless loading.

    Default header value: ``require-corp``

    Notes:
        * Per MDN, omitting the header is equivalent to ``unsafe-none``.
        * Each helper closes over canonical MDN directives while ``value(...)``
          acts as an escape hatch for custom strings.

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy
        - https://owasp.org/www-project-secure-headers/#cross-origin-embedder-policy
    """

    header_name: str = field(init=False, default=HeaderName.CROSS_ORIGIN_EMBEDDER_POLICY.value, repr=False)
    _default_value: str = field(init=False, default=HeaderDefaultValue.CROSS_ORIGIN_EMBEDDER_POLICY.value, repr=False)
    _directive: str = field(default=HeaderDefaultValue.CROSS_ORIGIN_EMBEDDER_POLICY.value, repr=False)

    def _normalize(self, value: str) -> str:
        """Normalize a directive value (trim + lowercase)."""
        v = normalize_header_value(value, what="Cross-Origin-Embedder-Policy value")

        if not v:
            return HeaderDefaultValue.CROSS_ORIGIN_EMBEDDER_POLICY.value
        return v.lower()

    @property
    def header_value(self) -> str:
        """Return the current ``Cross-Origin-Embedder-Policy`` header value."""
        return self._normalize(self._directive)

    def set(self, value: COEPDirective | str) -> CrossOriginEmbedderPolicy:
        """Set a COEP directive.

        This method accepts any string as an escape hatch. For MDN-defined values,
        prefer :meth:`unsafe_none`, :meth:`require_corp`, or :meth:`credentialless`.

        Args:
            value: Directive value (e.g., ``"require-corp"``).

        Returns:
            This instance for method chaining.
        """
        self._directive = self._normalize(str(value))
        return self

    def value(self, value: COEPDirective | str) -> CrossOriginEmbedderPolicy:
        """Alias for :meth:`set` to align with other headers."""
        return self.set(value)

    def clear(self) -> CrossOriginEmbedderPolicy:
        """Reset to the library default directive."""
        self._directive = self._default_value
        return self

    def unsafe_none(self) -> CrossOriginEmbedderPolicy:
        """Set COEP to ``unsafe-none``.

        ``unsafe-none`` allows the document to load cross-origin resources without
        explicit CORP/CORS permission.
        """
        self._directive = "unsafe-none"
        return self

    def require_corp(self) -> CrossOriginEmbedderPolicy:
        """Set COEP to ``require-corp``.

        ``require-corp`` blocks cross-origin resource loading unless the resource
        is explicitly permitted via CORP (for ``no-cors``) or via CORS (for ``cors``).
        """
        self._directive = "require-corp"
        return self

    def credentialless(self) -> CrossOriginEmbedderPolicy:
        """Set COEP to ``credentialless``.

        ``credentialless`` allows loading some cross-origin resources without
        explicit CORP opt-in, but strips credentials (cookies are omitted on the
        request and ignored in the response).
        """
        self._directive = "credentialless"
        return self
