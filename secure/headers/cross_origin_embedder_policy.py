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

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName

COEPDirective = Literal["unsafe-none", "require-corp", "credentialless"]


@dataclass
class CrossOriginEmbedderPolicy(BaseHeader):
    """Build the ``Cross-Origin-Embedder-Policy`` (COEP) response header.

    COEP configures the current document's policy for loading and embedding
    cross-origin resources. It can require opt-in via CORP
    (``Cross-Origin-Resource-Policy``) for ``no-cors`` fetches, or via CORS
    for ``cors`` fetches.

    Supported directives (MDN):
        - ``unsafe-none``: allow loading cross-origin resources without explicit CORP/CORS opt-in.
        - ``require-corp``: block cross-origin resource loading unless CORP or CORS permits it.
        - ``credentialless``: allow certain cross-origin loads without CORP opt-in, but strip credentials
          (cookies omitted on the request and ignored in the response).

    Default header value: ``require-corp``

    Note:
        Per MDN, the default behavior *when this header is not sent* is ``unsafe-none``.

    Example:
        >>> from secure import Secure
        >>> from secure.headers import CrossOriginEmbedderPolicy, CrossOriginOpenerPolicy
        >>>
        >>> secure = Secure(
        ...     coep=CrossOriginEmbedderPolicy().require_corp(),
        ...     coop=CrossOriginOpenerPolicy().same_origin(),
        ... )
        >>> secure.header_items()
        (('Cross-Origin-Embedder-Policy', 'require-corp'), ('Cross-Origin-Opener-Policy', 'same-origin'))

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy
        - https://owasp.org/www-project-secure-headers/#cross-origin-embedder-policy
    """

    header_name: str = HeaderName.CROSS_ORIGIN_EMBEDDER_POLICY.value
    _directive: str = field(default=HeaderDefaultValue.CROSS_ORIGIN_EMBEDDER_POLICY.value)

    def _normalize(self, value: str) -> str:
        """Normalize a directive value (trim + lowercase)."""
        v = value.strip()
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

    def clear(self) -> CrossOriginEmbedderPolicy:
        """Reset to the library default directive."""
        self._directive = HeaderDefaultValue.CROSS_ORIGIN_EMBEDDER_POLICY.value
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
