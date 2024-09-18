# Header information and recommendations are adapted from:
# - OWASP Secure Headers Project (https://owasp.org/www-project-secure-headers/)
# - MDN Web Docs (https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#security)
# - web.dev (https://web.dev)
# - The World Wide Web Consortium (W3C) (https://www.w3.org)

from typing import Any, Dict, List, Optional, Tuple, Union

from .headers import (
    server,
    cache_control,
    content_security_policy,
    permissions_policy,
    referrer_policy,
    report_to,
    strict_transport_security,
    x_content_type_options,
    x_frame_options,
    cross_origin_opener_policy,
    cross_origin_embedder_policy,
)


class Secure:
    """Set Secure Header options

    :param server: Server header options
    :param hsts: Strict-Transport-Security (HSTS) header options
    :param xfo: X-Frame-Options (XFO) header options
    :param content: X-Content-Type-Options header options
    :param csp: Content-Security-Policy (CSP) header options
    :param referrer: Referrer-Policy header options
    :param cache: Cache-control, Pragma and Expires headers options
    :param coop: Cross-Origin-Opener-Policy header options
    :param coep: Cross-Origin-Embedder-Policy header options
    """

    framework: "Framework"

    def __init__(
        self,
        server: Optional[server.Server] = None,
        hsts: Optional[
            strict_transport_security.StrictTransportSecurity
        ] = strict_transport_security.StrictTransportSecurity(),
        xfo: Optional[x_frame_options.XFrameOptions] = x_frame_options.XFrameOptions(),
        content: Optional[
            x_content_type_options.XContentTypeOptions
        ] = x_content_type_options.XContentTypeOptions(),
        csp: Optional[content_security_policy.ContentSecurityPolicy] = None,
        referrer: Optional[
            referrer_policy.ReferrerPolicy
        ] = referrer_policy.ReferrerPolicy(),
        cache: Optional[cache_control.CacheControl] = None,
        permissions: Optional[permissions_policy.PermissionsPolicy] = None,
        report_to: Optional[report_to.ReportTo] = None,
        coop: Optional[
            cross_origin_opener_policy
        ] = cross_origin_opener_policy.CrossOriginOpenerPolicy(),
        ceop: Optional[cross_origin_embedder_policy] = None,
    ) -> None:
        self.server = server
        self.hsts = hsts
        self.xfo = xfo
        self.content = content
        self.csp = csp
        self.referrer = referrer
        self.cache = cache
        self.permissions = permissions
        self.report_to = report_to
        self.coop = coop
        self.ceop = ceop

        self.framework = self.Framework(self)

    def __repr__(self) -> str:
        return "\n".join(
            [f"{header}:{value}" for header, value in self.headers().items()]
        )

    def _header_list(
        self,
    ) -> List[
        Union[
            cache_control.CacheControl,
            content_security_policy.ContentSecurityPolicy,
            permissions_policy.PermissionsPolicy,
            referrer_policy.ReferrerPolicy,
            report_to.ReportTo,
            server.Server,
            strict_transport_security.StrictTransportSecurity,
            x_content_type_options.XContentTypeOptions,
            x_frame_options.XFrameOptions,
        ]
    ]:
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
        ]

        return [header for header in headers if header is not None]

    def headers(self) -> Dict[str, str]:
        """Dictionary of secure headers

        :return: dictionary containing security headers
        :rtype: Dict[str, str]
        """
        headers: Dict[str, str] = {}

        for header in self._header_list():
            headers[header.header] = header.value

        return headers

    def headers_tuple(self) -> List[Tuple[str, str]]:
        """List of a tuple containing secure headers

        :return: list of tuples containing security headers
        :rtype: List[Tuple[str, str]]
        """
        headers: List[Tuple[str, str]] = []
        for header in self._header_list():
            headers.append((header.header, header.value))
        return headers

    def _set_header_dict(self, response: Any) -> None:
        """Function to set (dict) secure headers to response object."""

        for header in self._header_list():
            response.headers[header.header] = header.value

    def _set_header_tuple(self, response: Any) -> None:
        """Function to set (tuple) secure headers to response object."""

        for header in self._header_list():
            response.set_header(header.header, header.value)

        """
