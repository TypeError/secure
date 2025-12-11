# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Resource-Policy
# https://owasp.org/www-project-secure-headers/#cross-origin-resource-policy
#
# Cross-Origin-Resource-Policy by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class CrossOriginResourcePolicy(BaseHeader):
    """
    Represents the `Cross-Origin-Resource-Policy` HTTP header.

    This header controls which origins are allowed to load a given resource. It
    helps protect resources from being loaded in unexpected cross-origin
    contexts.

    Default header value: `same-origin`

    Common values:
        - `same-origin` Only same-origin documents may load the resource.
        - `same-site` Same-site documents may load the resource.
        - `cross-origin` Any origin may load the resource.

    Example:
        corp = CrossOriginResourcePolicy().same_origin()
        print(corp.header_name)   # Output: 'Cross-Origin-Resource-Policy'
        print(corp.header_value)  # Output: 'same-origin'

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Resource-Policy
        - https://owasp.org/www-project-secure-headers/#cross-origin-resource-policy
    """

    header_name: str = HeaderName.CROSS_ORIGIN_RESOURCE_POLICY.value
    _value: str = field(default_factory=lambda: HeaderDefaultValue.CROSS_ORIGIN_RESOURCE_POLICY.value)

    @property
    def header_value(self) -> str:
        """Return the current header value."""
        return self._value

    def set(self, value: str) -> CrossOriginResourcePolicy:
        """
        Set a custom value for the `Cross-Origin-Resource-Policy` header.

        Args:
            value:
                The header value to use. Typical values are `same-origin`,
                `same-site`, or `cross-origin`.

        Returns:
            The `CrossOriginResourcePolicy` instance for method chaining.
        """
        self._value = value
        return self

    def same_origin(self) -> CrossOriginResourcePolicy:
        """
        Restrict resource loading to the same origin.

        Returns:
            The `CrossOriginResourcePolicy` instance for method chaining.
        """
        self._value = "same-origin"
        return self

    def same_site(self) -> CrossOriginResourcePolicy:
        """
        Allow resource loading from the same site.

        Returns:
            The `CrossOriginResourcePolicy` instance for method chaining.
        """
        self._value = "same-site"
        return self

    def cross_origin(self) -> CrossOriginResourcePolicy:
        """
        Allow resource loading from any origin.

        Returns:
            The `CrossOriginResourcePolicy` instance for method chaining.
        """
        self._value = "cross-origin"
        return self
