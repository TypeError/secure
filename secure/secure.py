# Header information and recommendations are adapted from:
# - OWASP Secure Headers Project (https://owasp.org/www-project-secure-headers/)
# - MDN Web Docs (https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#security)
# - web.dev (https://web.dev)
# - The World Wide Web Consortium (W3C) (https://www.w3.org)

from __future__ import annotations  # type: ignore

from typing import Any


from secure.headers.custom_header import CustomHeader

from .headers import (
    cache_control,
    content_security_policy,
    cross_origin_embedder_policy,
    cross_origin_opener_policy,
    permissions_policy,
    referrer_policy,
    report_to,
    server,
    strict_transport_security,
    x_content_type_options,
    x_frame_options,
)
from .headers.base_header import BaseHeader


class Secure:
    """Set Secure Header options.

    :param server: Server header options
    :param hsts: Strict-Transport-Security (HSTS) header options
    :param xfo: X-Frame-Options (XFO) header options
    :param content: X-Content-Type-Options header options
    :param csp: Content-Security-Policy (CSP) header options
    :param referrer: Referrer-Policy header options
    :param cache: Cache-Control, Pragma, and Expires headers options
    :param permissions: Permissions-Policy header options
    :param report_to: Report-To header options
    :param coop: Cross-Origin-Opener-Policy header options
    :param ceop: Cross-Origin-Embedder-Policy header options
    """

    def __init__(
        self,
        server: server.Server | None = None,
        hsts: strict_transport_security.StrictTransportSecurity | None = None,
        xfo: x_frame_options.XFrameOptions | None = None,
        content: x_content_type_options.XContentTypeOptions | None = None,
        csp: content_security_policy.ContentSecurityPolicy | None = None,
        referrer: referrer_policy.ReferrerPolicy | None = None,
        cache: cache_control.CacheControl | None = None,
        permissions: permissions_policy.PermissionsPolicy | None = None,
        report_to: report_to.ReportTo | None = None,
        coop: cross_origin_opener_policy.CrossOriginOpenerPolicy | None = None,
        ceop: cross_origin_embedder_policy.CrossOriginEmbedderPolicy | None = None,
        custom: list[CustomHeader] | None = None,
    ) -> None:
        self.server = server
        self.hsts = hsts or strict_transport_security.StrictTransportSecurity()
        self.xfo = xfo or x_frame_options.XFrameOptions()
        self.content = content or x_content_type_options.XContentTypeOptions()
        self.csp = csp
        self.referrer = referrer or referrer_policy.ReferrerPolicy()
        self.cache = cache
        self.permissions = permissions
        self.report_to = report_to
        self.coop = coop or cross_origin_opener_policy.CrossOriginOpenerPolicy()
        self.ceop = ceop
        self.custom = custom or []

    def __str__(self) -> str:
        headers = self.headers
        return "\n".join(f"{header}: {value}" for header, value in headers.items())

    def __repr__(self) -> str:
        return (
            f"Secure(server={self.server!r}, hsts={self.hsts!r}, xfo={self.xfo!r}, "
            f"content={self.content!r}, csp={self.csp!r}, referrer={self.referrer!r}, "
            f"cache={self.cache!r}, permissions={self.permissions!r}, report_to={self.report_to!r}, "
            f"coop={self.coop!r}, ceop={self.ceop!r}, custom={self.custom!r})"
        )

    def __len__(self) -> int:
        return len(self.headers)

    def _header_list(self) -> list[BaseHeader]:
        headers = [
            self.server,
            self.hsts,
            self.xfo,
            self.content,
            self.csp,
            self.referrer,
            self.cache,
            self.permissions,
            self.report_to,
            self.coop,
            self.ceop,
            *self.custom,
        ]
        return [
            header
            for header in headers
            if header is not None and isinstance(header, BaseHeader)
        ]

    @property
    def headers(self) -> dict[str, str]:
        """Dictionary containing secure headers.

        :param as_tuple: If True, return headers as list of tuples, otherwise as a dictionary.
        :return: Dictionary containing security headers.
        """
        headers = {
            header.header_name: header.header_value for header in self._header_list()
        }
        return headers

    def set_headers(self, response: Any, use_set_header: bool = False) -> None:
        """Helper method to set headers on the response object.

        :param response: Response object.
        :param use_set_header: Whether to use set_header method or direct assignment.
        """
        headers = self.headers
        try:
            if use_set_header:
                for header, value in headers:
                    response.set_header(header, value)
            else:
                for header, value in headers:
                    response.headers[header] = value
        except AttributeError as e:
            print(f"Failed to set headers: {e}")
