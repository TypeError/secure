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
        self, path="/", secure=True, httponly=True, samesite=SameSite.LAX, expires=False
    ):
        """Set Secure Cookie options.

        :param path: Cookie Path option (default = "/")
        :param secure: Cookie Secure option (default = True)
        :param httponly: Cookie HttpOnly option (default = True)
        :param samesite: Cookie SameSite option (default = LAX)
        :param expires: Cookie Expires option (default = False)
        """
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
        """Update Secure Cookie to aiohttp response object.

        :param response: The aiohttp response object.
        :param name: Cookie name
        :param value: Cookie value
        """
        set_header_dict(response, name, value, **self.options)

    def bottle(self, response, name, value):
        """Update Secure Cookie to Bottle response object.

        :param response: The Bottle response object (bottle.response).
        :param name: Cookie name
        :param value: Cookie value
        """
        cookie_value = Cookie.secure_cookie(value, **self.options)
        response.add_header("Set-Cookie", "{}={}".format(name, cookie_value))

    def cherrypy(self, header, name, value):
        """Update Secure Cookie to CherryPy header object.

        :param header: CherryPy header object (cherrypy.response.headers)
        :param name: Cookie name
        :param value: Cookie value
        """
        cookie_value = Cookie.secure_cookie(value, **self.options)
        header["Set-Cookie"] = "{}={}".format(name, cookie_value)

    def django(self, response, name, value):
        """Update Secure Cookie to Django response object.

        :param response: The Django response object (django.http.HttpResponse).
        :param name: Cookie name
        :param value: Cookie value
        """
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
        """Update Secure Cookie to Falcon response object.

        :param response: The Falcon response object (falcon.Response).
        :param name:
        :param value:
        """
        set_header_tuple(response, name, value, **self.options)

    def flask(self, response, name, value):
        """Update Secure Cookie to Flask response object.

        :param response: The Flask response object (flask.Response).
        :param name: Cookie name
        :param value: Cookie value
        """
        if self.expires:
            expires = cookie_expiration(self.expires, timedelta_obj=False)
        else:
            expires = None

        response.set_cookie(
            name,
            value,
            expires=expires,
            path=self.path,
            secure=self.secure,
            httponly=self.httponly,
            samesite=self.samesite.value,
        )

    def hug(self, response, name, value):
        """Update Secure Cookie to hug response object.

        :param response: The hug response object.
        :param name: Cookie name
        :param value: Cookie value
        """
        set_header_tuple(response, name, value, **self.options)

    def masonite(self, request, name, value):
        """Update Secure Cookies to Masonite request object.

        :param request: The Masonite request object (masonite.request.Request).
        :param name: Cookie name
        :param value: Cookie value
        """
        cookie_value = Cookie.secure_cookie(value, **self.options)
        request.header("Set-Cookie", "{}={}".format(name, cookie_value))

    def pyramid(self, response, name, value):
        """Update Secure Cookie to Pyramid response object.

        :param response: The Pyramid response object (pyramid.response).
        :param name: Cookie name
        :param value: Cookie value
        """
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
        """Update Secure Cookie to Quart response object.

        :param response: The Quart response object (quart.wrappers.response.Response).
        :param name: Cookie name
        :param value: Cookie value
        """
        set_header_dict(response, name, value, **self.options)

    def responder(self, response, name, value):
        """Update Secure Cookie to Responder response object.

        :param response: The Responder response object.
        :param name: Cookie name
        :param value: Cookie value
        """
        set_cookie_dict(response, name, value, **self.options)

    def sanic(self, response, name, value):
        """Update Secure Cookie to Sanic response object.

        :param response: The Sanic response object (sanic.response).
        :param name: Cookie name
        :param value: Cookie value
        """
        set_header_dict(response, name, value, **self.options)

    def starlette(self, response, name, value):
        """Update Secure Cookie to Starlette response object.

        :param response: The Starlette response object.
        :param name: Cookie name
        :param value: Cookie value
        """
        set_header_dict(response, name, value, **self.options)

    def tornado(self, response, name, value):
        """Update Secure Cookie to Tornado RequestHandler object.

        :param response: The Tornado RequestHandler object (tornado.web.RequestHandler).
        :param name: Cookie name
        :param value: Cookie value
        """
        set_header_tuple(response, name, value, **self.options)
