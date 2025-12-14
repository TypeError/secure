# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-DNS-Prefetch-Control
# https://owasp.org/www-project-secure-headers/#x-dns-prefetch-control
#
# X-DNS-Prefetch-Control by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field
from typing import Final

from secure.headers._validation import normalize_header_value
from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName

_VALID_VALUES: Final[frozenset[str]] = frozenset({"on", "off"})


@dataclass
class XDnsPrefetchControl(BaseHeader):
    """
    Builder for the non-standard `X-DNS-Prefetch-Control` HTTP header.

    Default header value: `off`

    Notes:
        * Browsers may ignore this header as it is non-standard, but it documents
          the desired behavior for DNS prefetching.
        * Normalization keeps ``on``/``off`` lowercase while permitting other values unchanged.

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-DNS-Prefetch-Control
        - https://owasp.org/www-project-secure-headers/#x-dns-prefetch-control
    """

    header_name: str = field(init=False, default=HeaderName.X_DNS_PREFETCH_CONTROL.value, repr=False)
    _default_value: str = field(init=False, default=HeaderDefaultValue.X_DNS_PREFETCH_CONTROL.value, repr=False)
    _value: str = field(default_factory=lambda: HeaderDefaultValue.X_DNS_PREFETCH_CONTROL.value, repr=False)

    @property
    def header_value(self) -> str:
        """Return the current header value."""
        return self._value

    def clear(self) -> XDnsPrefetchControl:
        """Reset to the library default value (`off`)."""
        self._value = self._default_value
        return self

    def set(self, value: str) -> XDnsPrefetchControl:
        """
        Set a custom value for the `X-DNS-Prefetch-Control` header.

        Typical values are `on` or `off`. If `value` is `on`/`off` (case-insensitive),
        it will be normalized to lowercase for deterministic output.
        """
        cleaned = normalize_header_value(value, what="X-DNS-Prefetch-Control value")
        self._value = self._normalize(cleaned)
        return self

    def value(self, value: str) -> XDnsPrefetchControl:
        """Alias for :meth:`set`."""
        return self.set(value)

    def custom(self, value: str) -> XDnsPrefetchControl:
        """Alias for :meth:`set` (escape hatch)."""
        return self.set(value)

    def on(self) -> XDnsPrefetchControl:
        """
        Enable DNS prefetching.

        This is what browsers do (when supported) if the header is not present.
        """
        self._value = "on"
        return self

    def off(self) -> XDnsPrefetchControl:
        """
        Disable DNS prefetching.

        Useful if you don't control the links on the page or don't want to leak
        information to these domains.
        """
        self._value = "off"
        return self

    # Backwards-compatible aliases (keep existing public API)
    def allow(self) -> XDnsPrefetchControl:
        """Alias for :meth:`on`."""
        return self.on()

    def disable(self) -> XDnsPrefetchControl:
        """Alias for :meth:`off`."""
        return self.off()

    @staticmethod
    def _normalize(value: str) -> str:
        """Trim whitespace and canonicalize `on`/`off` to lowercase when recognized."""
        v = value.strip()
        v_lc = v.lower()
        return v_lc if v_lc in _VALID_VALUES else v
