from datetime import datetime, timedelta
from enum import Enum


class SameSite(Enum):
    lax = "lax"
    strict = "strict"


class Cookie:
    def __init__(self, value):
        self.value = value

    def secure_cookie(
        self, path="/", secure=True, httponly=True, samesite=SameSite.lax, expires=False
    ):
        cookie_value = "{}; Path={}".format(self, path)
        if secure:
            cookie_value += "; Secure"
        if httponly:
            cookie_value += "; HttpOnly"
        if samesite:
            cookie_value += "; SameSite={}".format(samesite.value)
        if expires:
            cookie_value += "; Expires={}".format(cookie_expiration(expires))

        return cookie_value


def cookie_expiration(hours, timedelta_obj=False):
    expire_time_obj = datetime.utcnow() + timedelta(hours=hours)
    expire_time = "{} GMT".format(expire_time_obj.strftime("%a, %d %b %Y %H:%M:%S"))
    if timedelta_obj:
        return timedelta(hours=hours)
    else:
        return expire_time


def set_cookie_dict(response, name, value, path, secure, httponly, samesite, expires):
    response.cookies[name] = Cookie.secure_cookie(
        value, path, secure, httponly, samesite, expires
    )


def set_header_dict(response, name, value, path, secure, httponly, samesite, expires):
    cookie_value = Cookie.secure_cookie(
        value, path, secure, httponly, samesite, expires
    )
    response.headers["Set-Cookie"] = "{}={}".format(name, cookie_value)


def set_header_tuple(response, name, value, path, secure, httponly, samesite, expires):
    cookie_value = Cookie.secure_cookie(
        value, path, secure, httponly, samesite, expires
    )
    response.set_header("Set-Cookie", "{}={}".format(name, cookie_value))
