# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy
# https://owasp.org/www-project-secure-headers/#content-security-policy
#
# Content-Security-Policy by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field
import re

from secure.headers._validation import normalize_header_value
from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName

_DIRECTIVE_NAME_RE = re.compile(r"^[A-Za-z0-9-]+$")
_NONCE_RE = re.compile(r"^[A-Za-z0-9+/_=-]+$")
_ASCII_SPACE = 0x20
_ASCII_DEL = 0x7F


@dataclass
class ContentSecurityPolicy(BaseHeader):
    """
    Fluent builder for the ``Content-Security-Policy`` HTTP response header.

    Default header value:
        `default-src 'self'; script-src 'self'; style-src 'self';
         object-src 'none'; base-uri 'self'; frame-ancestors 'self';
         form-action 'self'`

    Notes:
        * The structured helpers intentionally avoid full CSP validation; use
          ``.value(...)`` when you need to emit an exact policy string.
        * Multiple policies can be sent by instantiating another
          ``ContentSecurityPolicy`` and adding it to ``Secure.headers_list``.
        * MDN describes fallback behavior between directives (e.g., ``default-src``
          acts as a fallback for fetch directives).

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
        - https://owasp.org/www-project-secure-headers/#content-security-policy
    """

    header_name: str = field(init=False, default=HeaderName.CONTENT_SECURITY_POLICY.value, repr=False)

    # Structured directives built via fluent helpers. Each directive appears at most once.
    # Values are stored as tokens (space-separated in serialization). A value of ``None``
    # means the directive is valueless (for example: ``upgrade-insecure-requests``).
    _directives: dict[str, list[str] | None] = field(default_factory=dict, repr=False)

    # Escape hatch: if set, this raw string is used as the header value.
    _raw_value: str | None = field(default=None, repr=False)

    _default_value: str = field(init=False, default=HeaderDefaultValue.CONTENT_SECURITY_POLICY.value, repr=False)

    @property
    def header_value(self) -> str:
        """Return the current `Content-Security-Policy` header value."""
        if self._raw_value is not None:
            return self._raw_value

        if not self._directives:
            return self._default_value

        parts: list[str] = []
        for directive, values in self._directives.items():
            if values:
                parts.append(f"{directive} {' '.join(values)}")
            else:
                parts.append(directive)
        return "; ".join(parts)

    # -------------------------------------------------------------------------
    # Low-level helpers / escape hatches
    # -------------------------------------------------------------------------

    def value(self, value: str) -> ContentSecurityPolicy:
        """Set an exact header value (escape hatch)."""
        self._raw_value = normalize_header_value(value, what="Content-Security-Policy value")
        self._directives.clear()
        return self

    # Backwards-compatible alias.
    def set(self, value: str) -> ContentSecurityPolicy:
        """Alias for :meth:`value`."""
        return self.value(value)

    def clear(self) -> ContentSecurityPolicy:
        """Clear all configured directives and any raw override.

        After calling this, the header value falls back to the library default.
        """
        self._raw_value = None
        self._directives.clear()
        return self

    def report_only(self) -> ContentSecurityPolicy:
        """Use the report-only header name (`Content-Security-Policy-Report-Only`)."""
        self.header_name = HeaderName.CONTENT_SECURITY_POLICY_REPORT_ONLY.value
        return self

    def enforce(self) -> ContentSecurityPolicy:
        """Use the enforcing header name (`Content-Security-Policy`)."""
        self.header_name = HeaderName.CONTENT_SECURITY_POLICY.value
        return self

    def custom(self, directive: str, *values: str) -> ContentSecurityPolicy:
        """Alias for :meth:`custom_directive`."""
        return self.custom_directive(directive, *values)

    def custom_directive(self, directive: str, *values: str) -> ContentSecurityPolicy:
        """Add (or update) a directive.

        - Directives are de-duplicated: each directive name appears at most once.
        - Values are treated as tokens: duplicates are removed (preserving order).
        - Passing no values sets a valueless directive (overwriting prior values).

        Args:
            directive: Directive name (for example, ``default-src``).
            *values: Directive tokens (for example, ``'self'``, ``https:``, ``example.com``).

        Returns:
            The same instance, for method chaining.
        """
        self._touch_structured()
        d = self._normalize_directive_name(directive)

        if not values:
            # Valueless directive (or explicit "clear values" for a directive).
            self._directives[d] = None
            return self

        tokens = [self._validate_token(v) for v in values]

        existing = self._directives.get(d)
        if existing is None:
            existing_list: list[str] = []
            self._directives[d] = existing_list
        else:
            existing_list = existing

        # De-dupe while preserving insertion order.
        seen = set(existing_list)
        for t in tokens:
            if t not in seen:
                existing_list.append(t)
                seen.add(t)
        return self

    # -------------------------------------------------------------------------
    # Directive helpers (alphabetical by directive name)
    # -------------------------------------------------------------------------

    def base_uri(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for the document `<base>` element."""
        return self.custom_directive("base-uri", *sources)

    def block_all_mixed_content(self) -> ContentSecurityPolicy:
        """Prevent loading any assets using HTTP when the page is loaded using HTTPS.

        Deprecated in MDN's reference; prefer modern HTTPS-only deployments and
        consider `upgrade-insecure-requests` instead when appropriate.
        """
        return self.custom_directive("block-all-mixed-content")

    def child_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for web workers and nested browsing contexts."""
        return self.custom_directive("child-src", *sources)

    def connect_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for script interfaces (for example, XHR, Fetch, WebSocket)."""
        return self.custom_directive("connect-src", *sources)

    def default_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set the fallback policy for all fetch directives."""
        return self.custom_directive("default-src", *sources)

    def fenced_frame_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for nested browsing contexts loaded into `<fencedframe>`."""
        return self.custom_directive("fenced-frame-src", *sources)

    def font_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for fonts."""
        return self.custom_directive("font-src", *sources)

    def form_action(self, *sources: str) -> ContentSecurityPolicy:
        """Restrict the URLs which can be used as the target of form submissions."""
        return self.custom_directive("form-action", *sources)

    def frame_ancestors(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid parent sources that may embed the page in a frame."""
        return self.custom_directive("frame-ancestors", *sources)

    def frame_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for nested browsing contexts loaded into frames/iframes."""
        return self.custom_directive("frame-src", *sources)

    def img_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for images and favicons."""
        return self.custom_directive("img-src", *sources)

    def manifest_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for application manifests."""
        return self.custom_directive("manifest-src", *sources)

    def media_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for media (audio, video, track)."""
        return self.custom_directive("media-src", *sources)

    def object_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for plugin-like objects (for example, `<object>`, `<embed>`)."""
        return self.custom_directive("object-src", *sources)

    def prefetch_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources to be prefetched or prerendered.

        Deprecated and non-standard in MDN's reference; use only if you have a
        specific compatibility need.
        """
        return self.custom_directive("prefetch-src", *sources)

    def report_to(self, *values: str) -> ContentSecurityPolicy:
        """Configure reporting endpoints via `report-to` groups."""
        return self.custom_directive("report-to", *values)

    def report_uri(self, *uris: str) -> ContentSecurityPolicy:
        """Configure the legacy reporting endpoint(s) via `report-uri`.

        Deprecated in MDN's reference. If you use `report-to`, note that browsers
        that support `report-to` ignore `report-uri`.
        """
        return self.custom_directive("report-uri", *uris)

    def require_trusted_types_for(self, *values: str) -> ContentSecurityPolicy:
        """Enforce Trusted Types at specific DOM injection sinks."""
        return self.custom_directive("require-trusted-types-for", *values)

    def sandbox(self, *values: str) -> ContentSecurityPolicy:
        """Enable a sandbox for the requested resource (similar to `<iframe sandbox>`)."""
        return self.custom_directive("sandbox", *values)

    def script_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for JavaScript and WebAssembly resources."""
        return self.custom_directive("script-src", *sources)

    def script_src_attr(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for inline event handlers."""
        return self.custom_directive("script-src-attr", *sources)

    def script_src_elem(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for `<script>` elements."""
        return self.custom_directive("script-src-elem", *sources)

    def style_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for stylesheets."""
        return self.custom_directive("style-src", *sources)

    def style_src_attr(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for inline styles on individual elements."""
        return self.custom_directive("style-src-attr", *sources)

    def style_src_elem(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for `<style>` and stylesheet `<link>` elements."""
        return self.custom_directive("style-src-elem", *sources)

    def trusted_types(self, *values: str) -> ContentSecurityPolicy:
        """Specify an allowlist of Trusted Types policies."""
        return self.custom_directive("trusted-types", *values)

    def upgrade_insecure_requests(self) -> ContentSecurityPolicy:
        """Upgrade insecure HTTP requests to HTTPS."""
        return self.custom_directive("upgrade-insecure-requests")

    def worker_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for `Worker`, `SharedWorker`, and `ServiceWorker` scripts."""
        return self.custom_directive("worker-src", *sources)

    # -------------------------------------------------------------------------
    # CSP value helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def keyword(name: str) -> str:
        """Return a quoted CSP keyword/source expression (for example, ``'self'``)."""
        if not name:
            raise ValueError("CSP keyword must be non-empty")
        if any(ch.isspace() for ch in name) or any(ch in name for ch in "'\";\r\n"):
            raise ValueError("CSP keyword contains invalid characters")
        return f"'{name}'"

    @staticmethod
    def nonce(value: str) -> str:
        """Create a nonce source expression for inline scripts or styles.

        The provided value should be Base64 or URL-safe Base64.
        """
        if not value or not _NONCE_RE.fullmatch(value):
            raise ValueError("nonce value must be Base64 (or URL-safe Base64) characters only")
        return f"'nonce-{value}'"

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    def _touch_structured(self) -> None:
        """Switch from raw override to structured directive building (if needed)."""
        if self._raw_value is not None:
            self._raw_value = None

    @staticmethod
    def _normalize_directive_name(directive: str) -> str:
        if not directive:
            raise ValueError("directive name must be non-empty")
        if any(ch.isspace() for ch in directive) or any(ch in directive for ch in ";\r\n"):
            raise ValueError("directive name contains invalid characters")
        if not _DIRECTIVE_NAME_RE.fullmatch(directive):
            raise ValueError(f"invalid directive name: {directive!r}")
        return directive

    @staticmethod
    def _validate_token(token: str) -> str:
        if not token:
            raise ValueError("directive value tokens must be non-empty")
        if any(ch.isspace() for ch in token) or any(ch in token for ch in ";\r\n"):
            raise ValueError(f"directive token contains invalid characters: {token!r}")
        # Disallow other ASCII control characters.
        if any(ord(ch) < _ASCII_SPACE or ord(ch) == _ASCII_DEL for ch in token):
            raise ValueError(f"directive token contains control characters: {token!r}")
        return token
