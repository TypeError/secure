from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class ContentSecurityPolicy(BaseHeader):
    """
    Prevent Cross-site injections

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
    https://developers.google.com/web/fundamentals/security/csp

    """

    _policy: list[str] = field(default_factory=list)
    header_name: str = HeaderName.CONTENT_SECURITY_POLICY.value
    header_value: str = HeaderDefaultValue.CONTENT_SECURITY_POLICY.value

    def _build(self, directive: str, *sources: str) -> None:
        if len(sources) == 0:
            self._policy.append(directive)
        else:
            self._policy.append(f"{directive} {' '.join(sources)}")
        self.header_value = "; ".join(self._policy)

    def set(self, value: str) -> ContentSecurityPolicy:
        """Set custom value for `Content-Security-Policy` header

        :param value: custom header value
        :type value: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build(value)
        return self

    def custom_directive(self, directive: str, *sources: str) -> ContentSecurityPolicy:
        """Set custom directive and sources

        :param directive: custom directive
        :type directive: str
        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build(directive, *sources)
        return self

    def report_only(self) -> None:
        """Set Content-Security-Policy header to Content-Security-Policy-Report-Only"""
        self.header_name = HeaderName.CONTENT_SECURITY_POLICY_REPORT_ONLY.value

    def base_uri(self, *sources: str) -> ContentSecurityPolicy:
        """Sets valid origins for `<base>`

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/base-uri

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("base-uri", *sources)
        return self

    def child_src(self, *sources: str) -> ContentSecurityPolicy:
        """Sets valid origins for web workers

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/child-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("child-src", *sources)
        return self

    def connect_src(self, *sources: str) -> ContentSecurityPolicy:
        """Sets valid origins for script interfaces

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/connect-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("connect-src", *sources)
        return self

    def default_src(self, *sources: str) -> ContentSecurityPolicy:
        """Sets fallback valid origins for other directives

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/default-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("default-src", *sources)
        return self

    def font_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for `@font-face`

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/font-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("font-src", *sources)
        return self

    def form_action(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for form submissions

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/form-action

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("form-action", *sources)
        return self

    def frame_ancestors(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins that can embed the resource

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("frame-ancestors", *sources)
        return self

    def frame_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for frames

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("frame-src", *sources)
        return self

    def img_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for images

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/img-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("img-src", *sources)
        return self

    def manifest_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for manifest files

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/manifest-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("manifest-src", *sources)
        return self

    def media_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for media

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/media-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("media-src", *sources)
        return self

    def object_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for plugins

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/object-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("object-src", *sources)
        return self

    def report_to(self, *values: str) -> ContentSecurityPolicy:
        """Configure reporting endpoints

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/report-to

        :param values: variable number of URIs
        :type values: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("report-to", *values)
        return self

    def sandbox(self, *values: str) -> ContentSecurityPolicy:
        """Enables sandbox restrictions

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/sandbox

        :param values: variable number of types
        :type values: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("sandbox", *values)
        return self

    def script_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for JavaScript

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src

        :param sources: variable number of types
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("script-src", *sources)
        return self

    def style_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for styles

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/style-src

        :param sources: variable number of types
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("style-src", *sources)
        return self

    def upgrade_insecure_requests(self) -> ContentSecurityPolicy:
        """Upgrade HTTP URLs to HTTPS

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/upgrade-insecure-requests

        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("upgrade-insecure-requests")
        return self

    def worker_src(self, *sources: str) -> ContentSecurityPolicy:
        """Set valid origins for worker scripts

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/worker-src

        :param sources: variable number of types
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("worker-src", *sources)
        return self

    @staticmethod
    def nonce(value: str) -> str:
        """Creates a nonce format

        Resources:
        https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce

        :param value: nonce value
        :type value: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        value = f"'nonce-{value}'"
        return value
