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
        response.add_header(
            "Set-Cookie",
            f"{name}={Cookie.secure_cookie(value, path, secure, httponly, samesite, expires)}",
        )

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
        resp.set_header(
            "Set-Cookie",
            f"{name}={Cookie.secure_cookie(value, path, secure, httponly, samesite, expires)}",
        )

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

        header[
            "Set-Cookie"
        ] = f"{name}={Cookie.secure_cookie(value, path, secure, httponly, samesite, expires)}"
