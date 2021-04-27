from typing import Any, Dict, List, Optional, Tuple, Union

from .headers import (
    CacheControl,
    ContentSecurityPolicy,
    PermissionsPolicy,
    ReferrerPolicy,
    ReportTo,
    Server,
    StrictTransportSecurity,
    XContentTypeOptions,
    XFrameOptions,
    XXSSProtection,
)


class Secure:
    """Set Secure Header options

    :param server: Server header options
    :param hsts: Strict-Transport-Security (HSTS) header options
    :param xfo: X-Frame-Options (XFO) header options
    :param xxp: X-XSS-Protection (XXP) header options
    :param content: X-Content-Type-Options header options
    :param csp: Content-Security-Policy (CSP) header options
    :param referrer: Referrer-Policy header options
    :param cache: Cache-control, Pragma and Expires headers options
    :param feature: Feature-Policy header options
    """

    framework: "Framework"

    def __init__(
        self,
        server: Optional[Server] = None,
        hsts: Optional[StrictTransportSecurity] = StrictTransportSecurity(),
        xfo: Optional[XFrameOptions] = XFrameOptions(),
        xxp: Optional[XXSSProtection] = XXSSProtection(),
        content: Optional[XContentTypeOptions] = XContentTypeOptions(),
        csp: Optional[ContentSecurityPolicy] = None,
        referrer: Optional[ReferrerPolicy] = ReferrerPolicy(),
        cache: Optional[CacheControl] = CacheControl(),
        permissions: Optional[PermissionsPolicy] = None,
        report_to: Optional[ReportTo] = None,
    ) -> None:
        self.server = server
        self.hsts = hsts
        self.xfo = xfo
        self.xxp = xxp
        self.content = content
        self.csp = csp
        self.referrer = referrer
        self.cache = cache
        self.permissions = permissions
        self.report_to = report_to

        self.framework = self.Framework(self)

    def __repr__(self) -> str:
        return "\n".join(
            [f"{header}:{value}" for header, value in self.headers().items()]
        )

    def _header_list(
        self,
    ) -> List[
        Union[
            CacheControl,
            ContentSecurityPolicy,
            PermissionsPolicy,
            ReferrerPolicy,
            ReportTo,
            Server,
            StrictTransportSecurity,
            XContentTypeOptions,
            XFrameOptions,
            XXSSProtection,
        ]
    ]:
        headers = [
            self.server,
            self.hsts,
            self.xfo,
            self.xxp,
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
        for header in self._header_list():
            response.headers[header.header] = header.value

    def _set_header_tuple(self, response: Any) -> None:
        for header in self._header_list():
            response.set_header(header.header, header.value)

    class Framework:
        """
        Secure supported frameworks
        """

        def __init__(self, secure: "Secure") -> None:
            self.secure = secure

        def aiohttp(self, response: Any) -> None:
            """Update Secure Headers to aiohttp response object.

            :param response: aiohttp response object.
            """
            self.secure._set_header_dict(response)

        def bottle(self, response: Any) -> None:
            """Update Secure Headers to Bottle response object.

            :param response: Bottle response object (bottle.response).
            """
            self.secure._set_header_dict(response)

        def cherrypy(self) -> List[Tuple[str, str]]:
            """Return tuple of Secure Headers for CherryPy (tools.response_headers.headers).

            :return: A list with a tuple of Secure Headers.
            """
            return self.secure.headers_tuple()

        def django(self, response: Any) -> None:
            """Update Secure Headers to Django response object.

            :param response: Django response object (django.http.HttpResponse)
            """
            for header, value in self.secure.headers().items():
                response[header] = value

        def falcon(self, response: Any) -> None:
            """Update Secure Headers to Falcon response object.

            :param response: Falcon response object (falcon.Response)
            """
            self.secure._set_header_tuple(response)

        def flask(self, response: Any) -> None:
            """Update Secure Headers to Flask response object.

            :param response: Flask response object (flask.Response)
            """
            self.secure._set_header_dict(response)

        def fastapi(self, response: Any) -> None:
            """Update Secure Headers to FastAPI response object.

            :param response: FastAPI response object.
            """
            self.secure._set_header_dict(response)

        def hug(self, response: Any) -> None:
            """Update Secure Headers to hug response object.

            :param response: hug response object
            """
            self.secure._set_header_tuple(response)

        def masonite(self, request: Any) -> None:
            """Update Secure Headers to Masonite request object.

            :param request: Masonite request object (masonite.request.Request)
            """
            request.header(self.secure.headers())

        def pyramid(self, response: Any) -> None:
            """Update Secure Headers to Pyramid response object.

            :param response: Pyramid response object (pyramid.response).
            """
            self.secure._set_header_dict(response)

        def quart(self, response: Any) -> None:
            """Update Secure Headers to Quart response object.

            :param response: Quart response object (quart.wrappers.response.Response)
            """
            self.secure._set_header_dict(response)

        def responder(self, response: Any) -> None:
            """Update Secure Headers to Responder response object.

            :param response: Responder response object.
            """
            self.secure._set_header_dict(response)

        def sanic(self, response: Any) -> None:
            """Update Secure Headers to Sanic response object.

            :param response: Sanic response object (sanic.response).
            """
            self.secure._set_header_dict(response)

        def starlette(self, response: Any) -> None:
            """Update Secure Headers to Starlette response object.

            :param response: Starlette response object.
            """
            self.secure._set_header_dict(response)

        def tornado(self, response: Any) -> None:
            """Update Secure Headers to Tornado RequestHandler object.

            :param response: Tornado RequestHandler object (tornado.web.RequestHandler).
            """
            self.secure._set_header_tuple(response)
