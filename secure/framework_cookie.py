from .cookie import Cookie, set_cookie, alt_set_cookie, cookie_expiration, SameSite


class SecureCookie:
    SameSite = SameSite

    def responder(
        resp,
        name,
        value,
        path="/",
        secure=True,
        httponly=True,
        samesite=SameSite.lax,
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
        samesite=SameSite.lax,
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
        samesite=SameSite.lax,
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
        samesite=SameSite.lax,
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
        samesite=SameSite.lax,
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
            samesite=samesite.value,
        )

    def cherrypy(
        header,
        name,
        value,
        path="/",
        secure=True,
        httponly=True,
        samesite=SameSite.lax,
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
        samesite=SameSite.lax,
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
        samesite=SameSite.lax,
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
        samesite=SameSite.lax,
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
        samesite=SameSite.lax,
        expires=False,
    ):
        alt_set_cookie(resp, name, value, path, secure, httponly, samesite, expires)

    def starlette(
        resp,
        name,
        value,
        path="/",
        secure=True,
        httponly=True,
        samesite=SameSite.lax,
        expires=False,
    ):
        alt_set_cookie(resp, name, value, path, secure, httponly, samesite, expires)
