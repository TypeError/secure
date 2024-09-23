# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
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

    Default header value: `default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'`

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
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
        """Set `Content-Security-Policy` header to `Content-Security-Policy-Report-Only`.

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

    def base_uri(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for `<base>` element.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/base-uri

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("base-uri", *sources)

    def child_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for web workers.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/child-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("child-src", *sources)

    def connect_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for script interfaces (e.g., XMLHttpRequest, WebSocket).

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/connect-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("connect-src", *sources)

    def default_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set fallback valid origins for other directives.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/default-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("default-src", *sources)

    def font_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for `@font-face`.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/font-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("font-src", *sources)

    def form_action(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for form submissions.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/form-action

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("form-action", *sources)

    def frame_ancestors(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins that can embed the resource (e.g., iframes).

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("frame-ancestors", *sources)

    def frame_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for frames.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("frame-src", *sources)

    def img_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for images.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/img-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("img-src", *sources)

    def manifest_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for manifest files.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/manifest-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("manifest-src", *sources)

    def media_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for media content.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/media-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("media-src", *sources)

    def object_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for plugin objects (e.g., `<object>`, `<embed>`, `<applet>`).

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/object-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("object-src", *sources)

    def report_to(self, *values: str) -> ContentSecurityPolicy:
        """Configure reporting endpoints.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/report-to

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("report-to", *values)

    def sandbox(self, *values: str) -> ContentSecurityPolicy:
        """Enable sandboxing for scripts and iframes.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/sandbox

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("sandbox", *values)

    def script_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for JavaScript sources.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("script-src", *sources)

    def style_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for CSS and styles.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/style-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("style-src", *sources)

    def upgrade_insecure_requests(self) -> ContentSecurityPolicy:
        """Upgrade HTTP URLs to HTTPS.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/upgrade-insecure-requests

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("upgrade-insecure-requests")

    def worker_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for worker scripts.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/worker-src

        Returns:
            The `ContentSecurityPolicy` instance for method chaining.
        """
        return self.custom_directive("worker-src", *sources)

    @staticmethod
    def nonce(value: str) -> str:
        """Creates a nonce format for inline scripts.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce

        Args:
            value: The nonce value.

        Returns:
            A string formatted as a nonce.
        """
        return f"'nonce-{value}'"
