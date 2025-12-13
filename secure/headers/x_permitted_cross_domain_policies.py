# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Permitted-Cross-Domain-Policies
# https://owasp.org/www-project-secure-headers/#x-permitted-cross-domain-policies
#
# X-Permitted-Cross-Domain-Policies by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field
from typing import Final, Literal

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName

PermittedCrossDomainPolicy = Literal[
    "none",
    "master-only",
    "by-content-type",
    "by-ftp-filename",
    "all",
    "none-this-response",
]

_ALLOWED_POLICIES: Final[set[str]] = {
    "none",
    "master-only",
    "by-content-type",
    "by-ftp-filename",
    "all",
    "none-this-response",
}


def _normalize_header_value(value: str) -> str:
    """
    Normalize a header value for safe serialization.

    This strips leading/trailing whitespace and replaces any CR/LF with spaces.
    Further validation (RFC conformance, obs-text handling) is performed by
    Secure.validate_and_normalize_headers().
    """
    return value.replace("\r", " ").replace("\n", " ").strip()


@dataclass
class XPermittedCrossDomainPolicies(BaseHeader):
    """
    Represents the `X-Permitted-Cross-Domain-Policies` HTTP response header.

    This header defines a meta-policy controlling whether site resources can be accessed
    cross-origin by documents running in legacy web clients (for example, Adobe Acrobat
    or Microsoft Silverlight).

    Usage is less common since Adobe Flash Player and Microsoft Silverlight have been
    deprecated, but many security tools still check for `X-Permitted-Cross-Domain-Policies: none`
    to mitigate the risk of an overly-permissive cross-domain policy file being present.

    Default header value: `none`

    Example:
        xpcdp = XPermittedCrossDomainPolicies().none()
        print(xpcdp.header_name)   # 'X-Permitted-Cross-Domain-Policies'
        print(xpcdp.header_value)  # 'none'

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Permitted-Cross-Domain-Policies
        - https://owasp.org/www-project-secure-headers/#x-permitted-cross-domain-policies
    """

    header_name: str = HeaderName.X_PERMITTED_CROSS_DOMAIN_POLICIES.value
    _value: str = field(default_factory=lambda: HeaderDefaultValue.X_PERMITTED_CROSS_DOMAIN_POLICIES.value)

    @property
    def header_value(self) -> str:
        """Return the current header value."""
        return self._value

    # --- Escape hatches / lifecycle -------------------------------------------------

    def clear(self) -> XPermittedCrossDomainPolicies:
        """Reset the header to the default value (`none`)."""
        self._value = HeaderDefaultValue.X_PERMITTED_CROSS_DOMAIN_POLICIES.value
        return self

    def value(self, value: str) -> XPermittedCrossDomainPolicies:
        """
        Set a custom header value.

        Prefer the directive helper methods (e.g., :meth:`none`, :meth:`master_only`)
        when you want a well-known policy.
        """
        self._value = _normalize_header_value(value)
        return self

    def custom(self, value: str) -> XPermittedCrossDomainPolicies:
        """Alias for :meth:`value`."""
        return self.value(value)

    def set(self, value: str) -> XPermittedCrossDomainPolicies:
        """Backwards-compatible alias for :meth:`value`."""
        return self.value(value)

    def policy(self, policy: PermittedCrossDomainPolicy) -> XPermittedCrossDomainPolicies:
        """Set the header to one of the known directive values."""
        if policy not in _ALLOWED_POLICIES:
            raise ValueError(f"Unsupported X-Permitted-Cross-Domain-Policies value: {policy!r}")
        self._value = policy
        return self

    # --- Directive helpers ----------------------------------------------------------

    def none(self) -> XPermittedCrossDomainPolicies:
        """Disallow policy files anywhere on the target server, including a master policy file."""
        return self.policy("none")

    def master_only(self) -> XPermittedCrossDomainPolicies:
        """Allow cross-domain access to the master policy file defined on the same domain."""
        return self.policy("master-only")

    def by_content_type(self) -> XPermittedCrossDomainPolicies:
        """Allow only policy files served with `Content-Type: text/x-cross-domain-policy` (HTTP/HTTPS only)."""
        return self.policy("by-content-type")

    def by_ftp_filename(self) -> XPermittedCrossDomainPolicies:
        """Allow only policy files named `crossdomain.xml` (FTP only)."""
        return self.policy("by-ftp-filename")

    def all(self) -> XPermittedCrossDomainPolicies:
        """Allow all policy files on this target domain."""
        return self.policy("all")

    def none_this_response(self) -> XPermittedCrossDomainPolicies:
        """Indicate the current document should not be used as a policy file."""
        return self.policy("none-this-response")
