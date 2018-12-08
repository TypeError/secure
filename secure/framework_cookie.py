from .cookie import (
    Cookie,
    set_cookie_dict,
    set_header_dict,
    set_header_tuple,
    cookie_expiration,
    SameSite,
)


class SecureCookie:
    def __init__(
        self, path="/", secure=True, httponly=True, samesite=SameSite.lax, expires=False
    ):
        self.path = path
        self.secure = secure
        self.httponly = httponly
        self.samesite = samesite
        self.expires = expires
        self.options = {
            "path": path,
            "secure": secure,
            "httponly": httponly,
            "samesite": samesite,
            "expires": expires,
        }

    SameSite = SameSite

    def aiohttp(self, response, name, value):
        set_header_dict(response, name, value, **self.options)

    def bottle(self, response, name, value):
        cookie_value = Cookie.secure_cookie(value, **self.options)
        response.add_header("Set-Cookie", "{}={}".format(name, cookie_value))

    def cherrypy(self, header, name, value):
        cookie_value = Cookie.secure_cookie(value, **self.options)
        header["Set-Cookie"] = "{}={}".format(name, cookie_value)

    def django(self, response, name, value):
        response.set_cookie(
            name,
            value=value,
            expires=self.expires,
            path=self.path,
            secure=self.secure,
            httponly=self.httponly,
            samesite=self.samesite.value,
        )

    def falcon(self, response, name, value):
        set_header_tuple(response, name, value, **self.options)

    def flask(self, response, name, value):
        set_header_dict(response, name, value, **self.options)

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
        set_header_tuple(
            response, name, value, path, secure, httponly, samesite, expires
        )

    def pyramid(self, response, name, value):
        if self.expires:
            expires = cookie_expiration(self.expires, timedelta_obj=True)
        else:
            expires = None

        response.set_cookie(
            name,
            value,
            path=self.path,
            secure=self.secure,
            httponly=self.httponly,
            expires=expires,
            samesite=self.samesite.value,
        )

    def quart(self, response, name, value):
        set_header_dict(response, name, value, **self.options)

    def responder(self, response, name, value):
        set_cookie_dict(response, name, value, **self.options)

    def sanic(self, response, name, value):
        set_header_dict(response, name, value, **self.options)

    def starlette(self, response, name, value):
        set_header_dict(response, name, value, **self.options)

    def tornado(self, response, name, value):
        set_header_tuple(response, name, value, **self.options)
