from .cookie import Cookie, set_cookie, alt_set_cookie, cookie_expiration
from .headers import Security_Headers, set_headers, tuple_headers


class SecureHeaders:
    def responder(
        resp,
        server=True,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=False,
        referrer=True,
        cache=True,
    ):
        set_headers(resp, server, hsts, xfo, xss, content, csp, referrer, cache)

    def bottle(
        response,
        server=True,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=False,
        referrer=True,
        cache=True,
    ):
        set_headers(response, server, hsts, xfo, xss, content, csp, referrer, cache)

    def sanic(
        response,
        server=True,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=False,
        referrer=True,
        cache=True,
    ):
        set_headers(response, server, hsts, xfo, xss, content, csp, referrer, cache)

    def falcon(
        resp,
        server=True,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=False,
        referrer=True,
        cache=True,
    ):

        for header in Security_Headers.secure_headers(
            server, hsts, xfo, xss, content, csp, referrer, cache
        ):
            resp.set_header(header.header, header.value)

    def pyramid(
        response,
        server=True,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=False,
        referrer=True,
        cache=True,
    ):

        for header in Security_Headers.secure_headers(
            server, hsts, xfo, xss, content, csp, referrer, cache
        ):
            response.headers.add(header.header, header.value)

    def cherrypy(
        server=True,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=False,
        referrer=True,
        cache=True,
    ):
        headers = tuple_headers(server, hsts, xfo, xss, content, csp, referrer, cache)
        return headers

    def hug(
        response,
        server=True,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=False,
        referrer=True,
        cache=True,
    ):

        for header in Security_Headers.secure_headers(
            server, hsts, xfo, xss, content, csp, referrer, cache
        ):
            response.set_header(header.header, header.value)

    def tornado(
        response,
        server=True,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=False,
        referrer=True,
        cache=True,
    ):

        for header in Security_Headers.secure_headers(
            server, hsts, xfo, xss, content, csp, referrer, cache
        ):
            response.set_header(header.header, header.value)

    def aiohttp(
        resp,
        server=True,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=False,
        referrer=True,
        cache=True,
    ):
        set_headers(resp, server, hsts, xfo, xss, content, csp, referrer, cache)

    def quart(
        response,
        server=True,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=False,
        referrer=True,
        cache=True,
    ):
        set_headers(response, server, hsts, xfo, xss, content, csp, referrer, cache)


class SecureCookie:
    def responder(
        resp,
        name,
        value,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
        expires=False,
    ):
        set_cookie(resp, name, value, path, secure, httponly, samesite, expires)

    def bottle(
        response,
        name,
        value,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
        expires=False,
    ):
        cookie_value = Cookie.secure_cookie(
            value, path, secure, httponly, samesite, expires
        )
        response.add_header("Set-Cookie", "{}={}".format(name, cookie_value))

    def sanic(
        response,
        name,
        value,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
        expires=False,
    ):
        alt_set_cookie(response, name, value, path, secure, httponly, samesite, expires)

    def falcon(
        resp,
        name,
        value,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
        expires=False,
    ):

        cookie_value = Cookie.secure_cookie(
            value, path, secure, httponly, samesite, expires
        )
        resp.set_header("Set-Cookie", "{}={}".format(name, cookie_value))

    def pyramid(
        response,
        name,
        value,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
        expires=False,
    ):
        if expires:
            expires = cookie_expiration(expires, timedelta_obj=True)
        else:
            expires = None

        response.set_cookie(
            name,
            value,
            path=path,
            secure=secure,
            httponly=httponly,
            expires=expires,
            samesite=samesite,
        )

    def cherrypy(
        header,
        name,
        value,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
        expires=False,
    ):
        cookie_value = Cookie.secure_cookie(
            value, path, secure, httponly, samesite, expires
        )
        header["Set-Cookie"] = "{}={}".format(name, cookie_value)

    def hug(
        response,
        name,
        value,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
        expires=False,
    ):

        cookie_value = Cookie.secure_cookie(
            value, path, secure, httponly, samesite, expires
        )
        response.set_header("Set-Cookie", "{}={}".format(name, cookie_value))

    def tornado(
        response,
        name,
        value,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
        expires=False,
    ):

        cookie_value = Cookie.secure_cookie(
            value, path, secure, httponly, samesite, expires
        )
        response.set_header("Set-Cookie", "{}={}".format(name, cookie_value))

    def aiohttp(
        resp,
        name,
        value,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
        expires=False,
    ):
        alt_set_cookie(resp, name, value, path, secure, httponly, samesite, expires)

    def quart(
        resp,
        name,
        value,
        path="/",
        secure=True,
        httponly=True,
        samesite="lax",
        expires=False,
    ):
        alt_set_cookie(resp, name, value, path, secure, httponly, samesite, expires)
