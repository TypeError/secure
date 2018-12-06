from .headers import Security_Headers, set_headers, tuple_headers, dict_headers


class SecureHeaders:
    def headers(
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
        headers = dict_headers(
            server, hsts, xfo, xss, content, csp, referrer, cache, feature
        )
        return headers

    def responder(
        resp,
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
        set_headers(
            resp, server, hsts, xfo, xss, content, csp, referrer, cache, feature
        )

    def bottle(
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
        set_headers(
            response, server, hsts, xfo, xss, content, csp, referrer, cache, feature
        )

    def sanic(
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
        set_headers(
            response, server, hsts, xfo, xss, content, csp, referrer, cache, feature
        )

    def falcon(
        resp,
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

        for header in Security_Headers.secure_headers(
            server, hsts, xfo, xss, content, csp, referrer, cache, feature
        ):
            resp.set_header(header.header, header.value)

    def pyramid(
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

        for header in Security_Headers.secure_headers(
            server, hsts, xfo, xss, content, csp, referrer, cache, feature
        ):
            response.headers.add(header.header, header.value)

    def cherrypy(
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
        headers = tuple_headers(
            server, hsts, xfo, xss, content, csp, referrer, cache, feature
        )
        return headers

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

        for header in Security_Headers.secure_headers(
            server, hsts, xfo, xss, content, csp, referrer, cache, feature
        ):
            response.set_header(header.header, header.value)

    def tornado(
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

        for header in Security_Headers.secure_headers(
            server, hsts, xfo, xss, content, csp, referrer, cache, feature
        ):
            response.set_header(header.header, header.value)

    def aiohttp(
        resp,
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
        set_headers(
            resp, server, hsts, xfo, xss, content, csp, referrer, cache, feature
        )

    def quart(
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
        set_headers(
            response, server, hsts, xfo, xss, content, csp, referrer, cache, feature
        )

    def starlette(
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
        set_headers(
            response, server, hsts, xfo, xss, content, csp, referrer, cache, feature
        )
