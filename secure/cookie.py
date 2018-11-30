from datetime import datetime, timedelta


class Cookie:
    def __init__(self, value):
        self.value = value

    def secure_cookie(
        self, path="/", secure=True, httponly=True, samesite="lax", expires=False
    ):
        cookie_value = f"{self}; Path={path}"
        if secure:
            cookie_value += "; Secure"
        if httponly:
            cookie_value += "; HttpOnly"
        if samesite:
            if samesite == "lax":
                cookie_value += "; SameSite=Lax"
            elif samesite == "strict":
                cookie_value += "; SameSite=Strict"
        if expires:
            cookie_value += f"; Expires={cookie_expiration(expires)}"

        return cookie_value

    def secure_cookie_tuple(
        self, path="/", secure=True, httponly=True, samesite="lax", expires=False
    ):
        cookie_value = f"{self}; Path={path}"
        if secure:
            cookie_value += "; Secure"
        if httponly:
            cookie_value += "; HttpOnly"
        if samesite:
            if samesite == "lax":
                cookie_value += "; SameSite=Lax"
            elif samesite == "strict":
                cookie_value += "; SameSite=Strict"
        if expires:
            cookie_value += f"; Expires={cookie_expiration(expires)}"

        return cookie_value


def cookie_expiration(hours):
    expire_time = datetime.utcnow() + timedelta(hours=hours)
    expire_time = f"{expire_time.strftime('%a, %d %b %Y %H:%M:%S')} GMT"
    return expire_time


def set_cookie(resp, name, value, path, secure, httponly, samesite, expires):
    resp.cookies[name] = Cookie.secure_cookie(
        value, path, secure, httponly, samesite, expires
    )


def alt_set_cookie(resp, name, value, path, secure, httponly, samesite, expires):
    resp.headers[
        "Set-Cookie"
    ] = f"{name}={Cookie.secure_cookie(value, path, secure, httponly, samesite, expires)}"
