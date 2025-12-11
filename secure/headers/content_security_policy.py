# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy
# https://owasp.org/www-project-secure-headers/#content-security-policy
#
# Content-Security-Policy by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class ContentSecurityPolicy(BaseHeader):
    """
    Represents the `Content-Security-Policy` HTTP header, which helps prevent cross-site injections
    by specifying allowed sources for content.

    Default header value: `default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'self'; form-action 'self'`

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP
        - https://developers.google.com/web/fundamentals/security/csp
        - https://owasp.org/www-project-secure-headers/#content-security-policy
    """

    header_name: str = HeaderName.CONTENT_SECURITY_POLICY.value
    _directives: list[str] = field(default_factory=list)
    _default_value: str = HeaderDefaultValue.CONTENT_SECURITY_POLICY.value

    @property
    def header_value(self) -> str:
        """Return the current `Content-Security-Policy` header value."""
        return "; ".join(self._directives) if self._directives else self._default_value

    def _build(self, directive: str, *sources: str) -> None:
        """Add a directive to the policy.

        Args:
            directive: The directive name.
            *sources: The allowed sources for the directive.
        """
        if sources:
            self._directives.append(f"{directive} {' '.join(sources)}")
        else:
            self._directives.append(directive)

    def set(self, value: str) -> ContentSecurityPolicy:
        """Set a custom value for the `Content-Security-Policy` header.

        Args:
            value: Custom header value.

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        self._directives = [value]
        return self

    def clear(self) -> ContentSecurityPolicy:
        """Clear all directives from the `Content-Security-Policy` header.

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        self._directives.clear()
        return self

    def report_only(self) -> ContentSecurityPolicy:
        """Set header name to `Content-Security-Policy-Report-Only` for report-only mode.

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        self.header_name = HeaderName.CONTENT_SECURITY_POLICY_REPORT_ONLY.value
        return self

    def custom_directive(self, directive: str, *sources: str) -> ContentSecurityPolicy:
        """Add a custom directive and its allowed sources.

        Args:
            directive: Custom directive.
            *sources: Allowed sources for the directive.

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        self._build(directive, *sources)
        return self

    # -------------------------------------------------------------------------
    # Directive helpers (alphabetical by directive name)
    # -------------------------------------------------------------------------

    def base_uri(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for the document `<base>` element.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/base-uri

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("base-uri", *sources)

    def child_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for web workers and nested browsing contexts.

        Note:
            In CSP Level 3, `frame-src` and `worker-src` are preferred. `child-src`
            acts mainly as a fallback for those directives.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/child-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("child-src", *sources)

    def connect_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for script interfaces (for example, XHR, Fetch, WebSocket).

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/connect-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("connect-src", *sources)

    def default_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set fallback sources for other fetch directives.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/default-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("default-src", *sources)

    def fenced_frame_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for `<fencedframe>` nested browsing contexts.

        Note:
            This directive is currently experimental and not supported in all browsers.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/fenced-frame-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("fenced-frame-src", *sources)

    def font_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for font resources (for `@font-face`, etc.).

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/font-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("font-src", *sources)

    def form_action(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid action URLs for form submissions.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/form-action

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("form-action", *sources)

    def frame_ancestors(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources that can embed this resource (for example, in `<iframe>`).

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("frame-ancestors", *sources)

    def frame_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for nested browsing contexts (`<frame>`, `<iframe>`).

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("frame-src", *sources)

    def img_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for images.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/img-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("img-src", *sources)

    def manifest_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for manifest files.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/manifest-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("manifest-src", *sources)

    def media_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for media (audio, video, track).

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/media-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("media-src", *sources)

    def object_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for plugin-like objects (for example, `<object>`, `<embed>`, `<applet>`).

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/object-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("object-src", *sources)

    def report_to(self, *values: str) -> ContentSecurityPolicy:
        """Configure reporting endpoints via `report-to` groups.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/report-to

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("report-to", *values)

    def require_trusted_types_for(self, *values: str) -> ContentSecurityPolicy:
        """Enforce Trusted Types at DOM XSS sinks.

        Typically used with the `'script'` value.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/require-trusted-types-for
            https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("require-trusted-types-for", *values)

    def sandbox(self, *values: str) -> ContentSecurityPolicy:
        """Enable sandboxing for the document (similar to `<iframe sandbox>`).

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/sandbox

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("sandbox", *values)

    def script_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for JavaScript execution.

        Applies to `<script>` elements, inline event handlers, and other script execution contexts.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/script-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("script-src", *sources)

    def script_src_attr(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for JavaScript inline event handlers (for example, `onclick`).

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/script-src-attr

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("script-src-attr", *sources)

    def script_src_elem(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for JavaScript `<script>` elements.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/script-src-elem

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("script-src-elem", *sources)

    def style_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for stylesheets.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/style-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("style-src", *sources)

    def style_src_attr(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for inline `style` attributes on DOM elements.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/style-src-attr

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("style-src-attr", *sources)

    def style_src_elem(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for `<style>` elements and `<link rel=\"stylesheet\">`.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/style-src-elem

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("style-src-elem", *sources)

    def trusted_types(self, *policies: str) -> ContentSecurityPolicy:
        """Allowlist Trusted Types policy names that can be created.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/trusted-types
            https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("trusted-types", *policies)

    def upgrade_insecure_requests(self) -> ContentSecurityPolicy:
        """Upgrade insecure HTTP requests to HTTPS.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/upgrade-insecure-requests

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("upgrade-insecure-requests")

    def worker_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid sources for `Worker`, `SharedWorker`, and `ServiceWorker` scripts.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/worker-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("worker-src", *sources)

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def nonce(value: str) -> str:
        """Create a nonce source for inline scripts or styles.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce

        Args:
            value: The nonce value.

        Returns:
            A string formatted as a CSP nonce source.
        """
        return f"'nonce-{value}'"
