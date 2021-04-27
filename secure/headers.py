# Header information and recommendations are adapted from:
# - OWASP Secure Headers Project (https://owasp.org/www-project-secure-headers/)
# - MDN Web Docs (https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#security)
# - web.dev (https://web.dev)
# - The World Wide Web Consortium (W3C) (https://www.w3.org)

import json
from typing import Dict, List, Optional, Union
import warnings


class Server:
    """Replace server header"""

    def __init__(self) -> None:
        self.header = "Server"
        self.value = "NULL"

    def set(self, value: str) -> "Server":
        """Set custom value for `Server` header

        :param value: custom header value
        :type value: str
        :return: Server class
        :rtype: Server
        """
        self.value = value
        return self


class XContentTypeOptions:
    """Prevent MIME-sniffing

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options
    https://owasp.org/www-project-secure-headers/#x-content-type-options
    """

    def __init__(self) -> None:
        self.header = "X-Content-Type-Options"
        self.value = "nosniff"

    def set(self, value: str) -> "XContentTypeOptions":
        """Set custom value for `X-Content-Type-Options` header

        :param value: custom header value
        :type value: str
        :return: XContentTypeOptions class
        :rtype: XContentTypeOptions
        """
        self.value = value
        return self


class ReportTo:
    """Configure reporting endpoints

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/report-to
    https://developers.google.com/web/updates/2018/09/reportingapi

    :param max_age: endpoint TIL in seconds
    :type max_age: int
    :param include_subdomains: enable for subdomains, defaults to False
    :type include_subdomains: bool, optional
    :param group: endpoint name, defaults to None
    :type group: Optional[str], optional
    :param endpoints: variable number of endpoints
    :type endpoints: List[Dict[str, Union[str, int]]]
    """

    def __init__(
        self,
        max_age: int,
        include_subdomains: bool = False,
        group: Optional[str] = None,
        *endpoints: List[Dict[str, Union[str, int]]],
    ) -> None:
        self.header = "Report-To"

        report_to_endpoints = json.dumps(endpoints)

        report_to_object: Dict[str, Union[str, int]] = {
            "max_age": max_age,
            "endpoints": report_to_endpoints,
        }

        if group:
            report_to_object["group"] = group

        if include_subdomains:
            report_to_object["include_subdomains"] = include_subdomains

        self.value = json.dumps(report_to_object)

    def set(self, value: str) -> "ReportTo":
        """Set custom value for `Report-To` header

        :param value: custom header value
        :type value: str
        :return: ReportTo class
        :rtype: ReportTo
        """
        self.value = value
        return self


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

        :param value: nounce value
        :type value: str
        :return: ContentSecurityPolicy class
        :rtype: ContentSecurityPolicy
        """
        value = "'nonce-<{}>'".format(value)
        return value


class XFrameOptions:
    """
    Disable framing from different origins (clickjacking defense)

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
    """

    def __init__(self) -> None:
        self.header = "X-Frame-Options"
        self.value = "SAMEORIGIN"

    def set(self, value: str) -> "XFrameOptions":
        """Set custom value for X-Frame-Options header

        :param value: custom header value
        :type value: str
        :return: XFrameOptions class
        :rtype: XFrameOptions
        """
        self.value = value
        return self

    def deny(self) -> "XFrameOptions":
        """Disable rending site in a frame

        :return: XFrameOptions class
        :rtype: XFrameOptions
        """
        self.value = "deny"
        return self

    def sameorigin(self) -> "XFrameOptions":
        """Disable rending site in a frame if not same origin

        :return: XFrameOptions class
        :rtype: XFrameOptions
        """
        self.value = "sameorigin"
        return self


class XXSSProtection:
    """
    Enable browser Cross-Site Scripting filters

    **Depreciated**

    Recommended to utilize `Content-Security-Policy`
    instead of the legacy `X-XSS-Protection` header.

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection
    https://owasp.org/www-project-secure-headers/#x-xss-protection
    """

    def __init__(self) -> None:
        self.header = "X-XSS-Protection"
        self.value = "0"

    def set(self, value: str) -> "XXSSProtection":
        """Set custom value for `X-XSS-Protection` header

        :param value: custom header value
        :type value: str
        :return: XXSSProtection class
        :rtype: XXSSProtection
        """
        warnings.warn(
            "Recommended to utilize Content-Security-Policy",
            DeprecationWarning,
        )
        self.value = value
        return self


class ReferrerPolicy:
    """
    Enable full referrer if same origin, remove path for cross origin and
    disable referrer in unsupported browsers

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
    https://owasp.org/www-project-secure-headers/#referrer-policy
    """

    def __init__(self) -> None:
        self.__policy: List[str] = []
        self.header = "Referrer-Policy"
        self.value = "no-referrer, strict-origin-when-cross-origin"

    def _build(self, directive: str) -> None:
        self.__policy.append(directive)
        self.value = ", ".join(self.__policy)

    def set(self, value: str) -> "ReferrerPolicy":
        """Set custom value for `Referrer-Policy` header

        :param value: custom header value
        :type value: str
        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build(value)
        return self

    def no_referrer(self) -> "ReferrerPolicy":
        """The `Referer` header will not be sent

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("no-referrer")
        return self

    def no_referrer_when_downgrade(self) -> "ReferrerPolicy":
        """The `Referer` header will not be sent if HTTPS -> HTTP

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("no-referrer-when-downgrade")
        return self

    def origin(self) -> "ReferrerPolicy":
        """The `Referer` header will contain only the origin

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("origin")
        return self

    def origin_when_cross_origin(self) -> "ReferrerPolicy":
        """The `Referer` header will contain the full URL
        but only the origin if cross-origin

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("origin-when-cross-origin")
        return self

    def same_origin(self) -> "ReferrerPolicy":
        """The `Referer` header will be sent with the full URL if same-origin

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("same-origin")
        return self

    def strict_origin(self) -> "ReferrerPolicy":
        """The `Referer` header will be sent only for same-origin

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("strict-origin")
        return self

    def strict_origin_when_cross_origin(self) -> "ReferrerPolicy":
        """The `Referer` header will only contain the origin if HTTPS -> HTTP

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("strict-origin-when-cross-origin")
        return self

    def unsafe_url(self) -> "ReferrerPolicy":
        """The `Referer` header will contain the full URL

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("unsafe-url")
        return self


class StrictTransportSecurity:
    """
    Ensure application communication is sent over HTTPS

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
    https://owasp.org/www-project-secure-headers/#http-strict-transport-security
    """

    def __init__(self) -> None:
        self.__policy: List[str] = []
        self.header = "Strict-Transport-Security"
        self.value = "max-age=63072000; includeSubdomains"

    def _build(self, directive: str) -> None:
        self.__policy.append(directive)
        self.value = "; ".join(self.__policy)

    def set(self, value: str) -> "StrictTransportSecurity":
        """Set custom value for `Strict-Transport-Security` header

        :param value: custom header value
        :type value: str
        :return: StrictTransportSecurity class
        :rtype: StrictTransportSecurity
        """
        self._build(value)
        return self

    def include_subdomains(self) -> "StrictTransportSecurity":
        """Include subdomains to HSTS policy [Optional]

        :return: [description]
        :rtype: [type]
        """
        self._build("includeSubDomains")
        return self

    def max_age(self, seconds: int) -> "StrictTransportSecurity":
        """Instruct the browser to remember HTTPS preference
        until time (seconds) expires.

        :param seconds: time in seconds
        :type seconds: str
        :return: StrictTransportSecurity class
        :rtype: StrictTransportSecurity
        """
        self._build("max-age={}".format(seconds))
        return self

    def preload(self) -> "StrictTransportSecurity":
        """Instruct browser to always use HTTPS [Optional]

        Please see:
        https://hstspreload.org

        :return: StrictTransportSecurity class
        :rtype: StrictTransportSecurity
        """
        self._build("preload")
        return self


class CacheControl:
    """
    Prevent cacheable HTTPS response

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
    """

    def __init__(self) -> None:
        self.__policy: List[str] = []
        self.header = "Cache-Control"
        self.value = "no-store"

    def _build(self, directive: str) -> None:
        self.__policy.append(directive)
        self.value = ", ".join(self.__policy)

    def set(self, value: str) -> "CacheControl":
        """Set custom value for `Cache-control` header

        :param value: custom header value
        :type value: str
        :return: CacheControl class
        :rtype: CacheControl
        """
        self._build(value)
        return self

    def immutable(self) -> "CacheControl":
        self._build("immutable")
        return self

    def max_age(self, seconds: int) -> "CacheControl":
        self._build("max-age={}".format(seconds))
        return self

    def max_stale(self, seconds: int) -> "CacheControl":
        self._build("max-stale={}".format(seconds))
        return self

    def min_fresh(self, seconds: int) -> "CacheControl":
        self._build("min-fresh={}".format(seconds))
        return self

    def must_revalidate(self) -> "CacheControl":
        self._build("must-revalidate")
        return self

    def no_cache(self) -> "CacheControl":
        self._build("no-cache")
        return self

    def no_store(self) -> "CacheControl":
        self._build("no-store")
        return self

    def no_transform(self) -> "CacheControl":
        self._build("no-transform")
        return self

    def only_if_cached(self) -> "CacheControl":
        self._build("only-if-cached")
        return self

    def private(self) -> "CacheControl":
        self._build("private")
        return self

    def proxy_revalidate(self) -> "CacheControl":
        self._build("proxy-revalidate")
        return self

    def public(self) -> "CacheControl":
        self._build("public")
        return self

    def s_maxage(self, seconds: int) -> "CacheControl":
        self._build("s-maxage={}".format(seconds))
        return self

    def stale_if_error(self, seconds: int) -> "CacheControl":
        self._build("stale-if-error={}".format(seconds))
        return self

    def stale_while_revalidate(self, seconds: int) -> "CacheControl":
        self._build("stale-while-revalidate={}".format(seconds))
        return self


class PermissionsPolicy:
    """
    Disable browser features and APIs

    Replaces the `Feature-Policy` header

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Feature-Policy
    https://github.com/w3c/webappsec-permissions-policy/blob/main/permissions-policy-explainer.md
    """

    def __init__(self) -> None:
        self.__policy: List[str] = []
        self.header = "Permissions-Policy"
        self.value = (
            "accelerometer=(), ambient-light-sensor=(), autoplay=(),"
            "camera=(), encrypted-media=(), fullscreen=(),"
            "geolocation=(), gyroscope=(), magnetometer=(),"
            "microphone=(); midi=(), payment=(),"
            "picture-in-picture=(), speaker=(), sync-xhr=(), usb=(),"
            "vr=()"
        )

    def _build(self, directive: str, *sources: str) -> None:
        self.__policy.append(f"{directive}=({' '.join(sources)})")
        self.value = ", ".join(self.__policy)

    def set(self, value: str) -> "PermissionsPolicy":
        self._build(value)
        return self

    def accelerometer(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("accelerometer", *allowlist)
        return self

    def ambient_light_sensor(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("ambient-light-sensor ", *allowlist)
        return self

    def autoplay(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("autoplay", *allowlist)
        return self

    def camera(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("camera", *allowlist)
        return self

    def document_domain(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("document-domain", *allowlist)
        return self

    def encrypted_media(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("encrypted-media", *allowlist)
        return self

    def fullscreen(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("fullscreen", *allowlist)
        return self

    def geolocation(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("geolocation", *allowlist)
        return self

    def gyroscope(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("gyroscope", *allowlist)
        return self

    def magnetometer(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("magnetometer", *allowlist)
        return self

    def microphone(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("microphone", *allowlist)
        return self

    def midi(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("midi", *allowlist)
        return self

    def payment(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("payment", *allowlist)
        return self

    def picture_in_picture(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("picture-in-picture", *allowlist)
        return self

    def speaker(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("speaker", *allowlist)
        return self

    def sync_xhr(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("sync-xhr", *allowlist)
        return self

    def usb(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("usb", *allowlist)
        return self

    def vibrate(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("vibrate", *allowlist)
        return self

    def vr(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("vr", *allowlist)
        return self
