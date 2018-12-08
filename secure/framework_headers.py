from .headers import (
    Security_Headers,
    set_header_dict,
    set_header_tuple,
    tuple_headers,
    dict_headers,
)


class SecureHeaders:
    def __init__(
        self,
        server=False,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=False,
        referrer=True,
        cache=True,
        feature=False,
    ):
        self.server = server
        self.hsts = hsts
        self.xfo = xfo
        self.xss = xss
        self.content = content
        self.csp = csp
        self.referrer = referrer
        self.cache = cache
        self.feature = feature
        self.options = {
            "server": server,
            "hsts": hsts,
            "xfo": xfo,
            "xss": xss,
            "content": content,
            "csp": csp,
            "referrer": referrer,
            "cache": cache,
            "feature": feature,
        }

    def headers(self):
        headers = dict_headers(**self.options)
        return headers

    def aiohttp(self, response):
        set_header_dict(response, **self.options)

    def bottle(self, response):
        set_header_dict(response, **self.options)

    def cherrypy(self):
        headers = tuple_headers(**self.options)
        return headers

    def django(self, response):
        for header in Security_Headers.secure_headers(**self.options):
            response[header.header] = header.value

    def falcon(self, response):
        set_header_tuple(response, **self.options)

    def flask(self, response):
        set_header_dict(response, **self.options)

    def hug(
        response,
        server=False,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=False,
        referrer=True,
        cache=True,
        feature=False,
    ):
        set_header_tuple(
            response, server, hsts, xfo, xss, content, csp, referrer, cache, feature
        )

    def pyramid(self, response):
        for header in Security_Headers.secure_headers(**self.options):
            response.headers.add(header.header, header.value)

    def quart(self, response):
        set_header_dict(response, **self.options)

    def responder(self, response):
        set_header_dict(response, **self.options)

    def sanic(self, response):
        set_header_dict(response, **self.options)

    def starlette(self, response):
        set_header_dict(response, **self.options)

    def tornado(self, response):
        set_header_tuple(response, **self.options)
