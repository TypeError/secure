from .cookie import Cookie, set_cookie, alt_set_cookie
from .headers import Security_Headers, set_headers


class SecureHeaders:
    def responder(
        resp,
        server=False,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=True,
        referrer=True,
        cache=True,
    ):
        set_headers(resp, server, hsts, xfo, xss, content, csp, referrer, cache)

    def bottle(
        response,
        server=False,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=True,
        referrer=True,
        cache=True,
    ):
        set_headers(response, server, hsts, xfo, xss, content, csp, referrer, cache)

    def sanic(
        response,
        server=False,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=True,
        referrer=True,
        cache=True,
    ):
        set_headers(response, server, hsts, xfo, xss, content, csp, referrer, cache)

    def falcon(
        resp,
        server=False,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=True,
        referrer=True,
        cache=True,
    ):

        for header in Security_Headers.secure_headers(
            server, hsts, xfo, xss, content, csp, referrer, cache
        ):
            resp.set_header(header.header, header.value)


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
