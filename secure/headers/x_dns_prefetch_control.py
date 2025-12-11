# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-DNS-Prefetch-Control
# https://owasp.org/www-project-secure-headers/#x-dns-prefetch-control
#
# X-DNS-Prefetch-Control by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class XDnsPrefetchControl(BaseHeader):
    """
    Represents the `X-DNS-Prefetch-Control` HTTP header.

    This header controls whether the browser is allowed to perform DNS
    prefetching for links on the page, which can improve performance at the
    cost of some privacy.

    Default header value: `off`

    Common values:
        - `off` Disable DNS prefetching.
        - `on`  Enable DNS prefetching.

    Example:
        xdfc = XDnsPrefetchControl().disable()
        print(xdfc.header_name)   # 'X-DNS-Prefetch-Control'
        print(xdfc.header_value)  # 'off'

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-DNS-Prefetch-Control
        - https://owasp.org/www-project-secure-headers/#x-dns-prefetch-control
    """

    header_name: str = HeaderName.X_DNS_PREFETCH_CONTROL.value
    _value: str = field(default_factory=lambda: HeaderDefaultValue.X_DNS_PREFETCH_CONTROL.value)

    @property
    def header_value(self) -> str:
        """Return the current header value."""
        return self._value

    def set(self, value: str) -> XDnsPrefetchControl:
        """
        Set a custom value for the `X-DNS-Prefetch-Control` header.

        Args:
            value:
                The header value to use. Typical values are `on` or `off`.

        Returns:
            The `XDnsPrefetchControl` instance for method chaining.
        """
        self._value = value
        return self

    def allow(self) -> XDnsPrefetchControl:
        """
        Enable DNS prefetching (`on`).

        Returns:
            The `XDnsPrefetchControl` instance for method chaining.
        """
        self._value = "on"
        return self

    def disable(self) -> XDnsPrefetchControl:
        """
        Disable DNS prefetching (`off`).

        Returns:
            The `XDnsPrefetchControl` instance for method chaining.
        """
        self._value = "off"
        return self
