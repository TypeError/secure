from typing import List


class ContentSecurityPolicy:
    """
    Prevent Cross-site injections

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
    https://developers.google.com/web/fundamentals/security/csp

    """

    def __init__(self) -> None:
        self.__policy: List[str] = []
        self.header = "Content-Security-Policy"
        self.value = "script-src 'self'; object-src 'self'"

    def _build(self, directive: str, *sources: str) -> None:
        if len(sources) == 0:
            self.__policy.append(directive)
        else:
            self.__policy.append(f"{directive} {' '.join(sources)}")
        self.value = "; ".join(self.__policy)

    def set(self, value: str) -> "ContentSecurityPolicy":
        """Set custom value for `Content-Security-Policy` header

        :param value: custom header value
        :type value: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build(value)
        return self

    def custom_directive(
        self, directive: str, *sources: str
    ) -> "ContentSecurityPolicy":
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
        self.header = "Content-Security-Policy-Report-Only"

    def base_uri(self, *sources: str) -> "ContentSecurityPolicy":
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

    def child_src(self, *sources: str) -> "ContentSecurityPolicy":
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

    def connect_src(self, *sources: str) -> "ContentSecurityPolicy":
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

    def default_src(self, *sources: str) -> "ContentSecurityPolicy":
        """Sets fallback valid orgins for other directives

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/default-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("default-src", *sources)
        return self

    def font_src(self, *sources: str) -> "ContentSecurityPolicy":
        """Set valid origins for `@font-face`

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/font-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("font-src", *sources)
        return self

    def form_action(self, *sources: str) -> "ContentSecurityPolicy":
        """Set valid origins for form submissions

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/form-action

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("form-action", *sources)
        return self

    def frame_ancestors(self, *sources: str) -> "ContentSecurityPolicy":
        """Set valid origins that can embed the resource

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("frame-ancestors", *sources)
        return self

    def frame_src(self, *sources: str) -> "ContentSecurityPolicy":
        """Set valid origins for frames

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("frame-src", *sources)
        return self

    def img_src(self, *sources: str) -> "ContentSecurityPolicy":
        """Set valid origins for images

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/img-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("img-src", *sources)
        return self

    def manifest_src(self, *sources: str) -> "ContentSecurityPolicy":
        """Set valid origins for manifest files

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/manifest-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("manifest-src", *sources)
        return self

    def media_src(self, *sources: str) -> "ContentSecurityPolicy":
        """Set valid origins for media

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/media-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("media-src", *sources)
        return self

    def object_src(self, *sources: str) -> "ContentSecurityPolicy":
        """Set valid origins for plugins

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/object-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("object-src", *sources)
        return self

    def prefetch_src(self, *sources: str) -> "ContentSecurityPolicy":
        """Set valid resources that may prefetched or prerendered

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/prefetch-src

        :param sources: variable number of sources
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("prefetch-src", *sources)
        return self

    def report_to(self, report_to: ReportTo) -> "ContentSecurityPolicy":
        """Configure reporting endpoints

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/report-to

        :param report_to: ReportTo class
        :type report_to: ReportTo
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("report-to", report_to.value)
        return self

    def report_uri(self, *values: str) -> "ContentSecurityPolicy":
        """Configure reporting endpoints in an older format

        **Deprecated**
        This header has been deprecated in favor of report-to.
        However, as it is not yet supported in most browsers, it is recommended to set both headers.
        Browsers that support report-to will ignore report-uri if both headers are set.

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/report-uri

        :param values: variable number of URIs
        :type values: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("report-uri", *values)
        return self

    def sandbox(self, *values: str) -> "ContentSecurityPolicy":
        """Enables sandbox restrictions

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/sandbox

        :param values: variable number of types
        :type values: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("sandbox", *values)
        return self

    def script_src(self, *sources: str) -> "ContentSecurityPolicy":
        """Set valid origins for JavaScript

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src

        :param sources: variable number of types
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("script-src", *sources)
        return self

    def style_src(self, *sources: str) -> "ContentSecurityPolicy":
        """Set valid origins for styles

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/style-src

        :param sources: variable number of types
        :type sources: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("style-src", *sources)
        return self

    def upgrade_insecure_requests(self) -> "ContentSecurityPolicy":
        """Upgrade HTTP URLs to HTTPS

        Resouces:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/upgrade-insecure-requests

        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        self._build("upgrade-insecure-requests")
        return self

    def worker_src(self, *sources: str) -> "ContentSecurityPolicy":
        """Set valid origins for worker scripts

        Resouces:
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

        :param value: nounce value
        :type value: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        value = f"'nonce-{value}'"
        return value
