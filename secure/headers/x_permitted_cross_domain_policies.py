# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Permitted-Cross-Domain-Policies
# https://owasp.org/www-project-secure-headers/#x-permitted-cross-domain-policies
#
# X-Permitted-Cross-Domain-Policies by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class XPermittedCrossDomainPolicies(BaseHeader):
    """
    Represents the `X-Permitted-Cross-Domain-Policies` HTTP header.

    This header controls which cross-domain policy files (for example for Adobe
    products) are allowed to control access to your content.

    Default header value: `none`

    Valid values:
        - `none`            No cross-domain policies are allowed.
        - `master-only`     Only a master policy file is allowed.
        - `by-content-type` Only policy files served with an appropriate
                              content type are allowed.
        - `all`             All policy files on this domain are allowed.
    Example:
        xpcdp = XPermittedCrossDomainPolicies().none()
        print(xpcdp.header_name)   # 'X-Permitted-Cross-Domain-Policies'
        print(xpcdp.header_value)  # 'none'

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Permitted-Cross-Domain-Policies
        - https://owasp.org/www-project-secure-headers/#x-permitted-cross-domain-policies
    """

    header_name: str = HeaderName.X_PERMITTED_CROSS_DOMAIN_POLICIES.value
    _value: str = field(default_factory=lambda: HeaderDefaultValue.X_PERMITTED_CROSS_DOMAIN_POLICIES.value)

    @property
    def header_value(self) -> str:
        """Return the current header value."""
        return self._value

    def set(self, value: str) -> XPermittedCrossDomainPolicies:
        """
        Set a custom value for the `X-Permitted-Cross-Domain-Policies` header.

        Args:
            value:
                The header value to use. It should be one of `none`,
                `master-only`, `by-content-type`, or `all`.

        Returns:
            The `XPermittedCrossDomainPolicies` instance for method chaining.
        """
        self._value = value
        return self

    def none(self) -> XPermittedCrossDomainPolicies:
        """
        Disallow all cross-domain policy files.

        Returns:
            The `XPermittedCrossDomainPolicies` instance for method chaining.
        """
        self._value = "none"
        return self

    def master_only(self) -> XPermittedCrossDomainPolicies:
        """
        Allow only a single master cross-domain policy file.

        Returns:
            The `XPermittedCrossDomainPolicies` instance for method chaining.
        """
        self._value = "master-only"
        return self

    def by_content_type(self) -> XPermittedCrossDomainPolicies:
        """
        Allow policy files that are served with an appropriate content type.

        Returns:
            The `XPermittedCrossDomainPolicies` instance for method chaining.
        """
        self._value = "by-content-type"
        return self

    def all(self) -> XPermittedCrossDomainPolicies:
        """
        Allow all cross-domain policy files on this domain.

        Returns:
            The `XPermittedCrossDomainPolicies` instance for method chaining.
        """
        self._value = "all"
        return self
