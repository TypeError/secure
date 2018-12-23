from .headers import (
    Security_Headers,
    set_header_dict,
    set_header_tuple,
    tuple_headers,
    dict_headers,
)


class SecureHeaders:
    """Set Secure Header options.

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

    def __init__(
        self,
        server=False,
        hsts=True,
        xfo=True,
        xxp=True,
        content=True,
        csp=False,
        referrer=True,
        cache=True,
        feature=False,
    ):
        self.server = server
        self.hsts = hsts
        self.xfo = xfo
        self.xxp = xxp
        self.content = content
        self.csp = csp
        self.referrer = referrer
        self.cache = cache
        self.feature = feature
        self.options = {
            "server": server,
            "hsts": hsts,
            "xfo": xfo,
            "xxp": xxp,
            "content": content,
            "csp": csp,
            "referrer": referrer,
            "cache": cache,
            "feature": feature,
        }

    def headers(self):
        """ Return dictionary of Secure Headers.

        :return: A dictionary of Secure Headers.
        """
        headers = dict_headers(**self.options)
        return headers

    def aiohttp(self, response):
        """Update Secure Headers to aiohttp response object.

        :param response: The aiohttp response object.
        """
        set_header_dict(response, **self.options)

    def bottle(self, response):
        """Update Secure Headers to Bottle response object.

        :param response: The Bottle response object (bottle.response).
        """
        set_header_dict(response, **self.options)

    def cherrypy(self):
        """Return tuple of Secure Headers for CherryPy (tools.response_headers.headers).

        :return: A tuple of Secure Headers.
        """
        headers = tuple_headers(**self.options)
        return headers

    def django(self, response):
        """Update Secure Headers to Django response object.

        :param response: The Django response object (django.http.HttpResponse).
        """
        for header in Security_Headers.secure_headers(**self.options):
            response[header.header] = header.value

    def falcon(self, response):
        """Update Secure Headers to Falcon response object.

        :param response: The Falcon response object (falcon.Response).
        """
        set_header_tuple(response, **self.options)

    def flask(self, response):
        """Update Secure Headers to Flask response object.

        :param response: The Flask response object (flask.Response).
        """
        set_header_dict(response, **self.options)

    def hug(self, response):
        """Update Secure Headers to hug response object.

        :param response: The hug response object.
        """
        set_header_tuple(response, **self.options)

    def masonite(self, request):
        """Update Secure Headers to Masonite request object.

        :param request: The Masonite request object (masonite.request.Request).
        """
        request.header(dict_headers(**self.options))

    def pyramid(self, response):
        """Update Secure Headers to Pyramid response object.

        :param response: The Pyramid response object (pyramid.response).
        """
        for header in Security_Headers.secure_headers(**self.options):
            response.headers.add(header.header, header.value)

    def quart(self, response):
        """Update Secure Headers to Quart response object.

        :param response: The Quart response object (quart.wrappers.response.Response).
        """
        set_header_dict(response, **self.options)

    def responder(self, response):
        """Update Secure Headers to Responder response object.

        :param response: The Responder response object.
        """
        set_header_dict(response, **self.options)

    def sanic(self, response):
        """Update Secure Headers to Sanic response object.

        :param response: The Sanic response object (sanic.response).
        """
        set_header_dict(response, **self.options)

    def starlette(self, response):
        """Update Secure Headers to Starlette response object.

        :param response: The Starlette response object.
        """
        set_header_dict(response, **self.options)

    def tornado(self, response):
        """Update Secure Headers to Tornado RequestHandler object.

        :param response: The Tornado RequestHandler object (tornado.web.RequestHandler).
        """
        set_header_tuple(response, **self.options)
