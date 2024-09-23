# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy
# https://owasp.org/www-project-secure-headers/#cross-origin-embedder-policy
#
# Cross-Origin-Embedder-Policy by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/


from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class CrossOriginEmbedderPolicy(BaseHeader):
    """
    Represents the `Cross-Origin-Embedder-Policy` HTTP header, which prevents a document from loading
    any cross-origin resources that don’t explicitly grant the document permission.

    - `CORP` applies on the loaded resource side (resource owner).
    - `COEP` applies on the “loader” of the resource side (consumer of the resource).

    Default header value: `require-corp`

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy
        - https://owasp.org/www-project-secure-headers/#cross-origin-embedder-policy
    """

    header_name: str = HeaderName.CROSS_ORIGIN_EMBEDDER_POLICY.value
    _directive: str = field(
        default=HeaderDefaultValue.CROSS_ORIGIN_EMBEDDER_POLICY.value
    )

    @property
    def header_value(self) -> str:
        """Return the current `Cross-Origin-Embedder-Policy` header value.

        Returns:
            The current COEP policy as a string.
        """
        return self._directive

    def set(self, value: str) -> CrossOriginEmbedderPolicy:
        """
        Set a custom value for the `Cross-Origin-Embedder-Policy` header.

        Args:
            value: Custom header value.

        Returns:
            The `CrossOriginEmbedderPolicy` instance for method chaining.
        """
        self._directive = value
        return self

    def clear(self) -> CrossOriginEmbedderPolicy:
        """
        Reset the `Cross-Origin-Embedder-Policy` header to its default value.

        Returns:
            The `CrossOriginEmbedderPolicy` instance for method chaining.
        """
        self._directive = HeaderDefaultValue.CROSS_ORIGIN_EMBEDDER_POLICY.value
        return self

    def unsafe_none(self) -> CrossOriginEmbedderPolicy:
        """
        Set the header to `'unsafe-none'`.

        This allows the document to fetch cross-origin resources without giving explicit permission
        through the CORS protocol or the `Cross-Origin-Resource-Policy` header (this is the default value).

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy

        Returns:
            The `CrossOriginEmbedderPolicy` instance for method chaining.
        """
        self._directive = "unsafe-none"
        return self

    def require_corp(self) -> CrossOriginEmbedderPolicy:
        """
        Set the header to `'require-corp'`.

        This ensures a document can only load resources from the same origin, or resources explicitly
        marked as loadable from another origin.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy

        Returns:
            The `CrossOriginEmbedderPolicy` instance for method chaining.
        """
        self._directive = "require-corp"
        return self
