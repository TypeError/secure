class Header:
    def __init__(self, header, value, info="N/A"):
        self.header = header
        self.value = value
        self.info = info


class Security_Headers:
    # Header recommendations from the OWASP Secure Headers Project
    # (https://www.owasp.org/index.php/OWASP_Secure_Headers_Project)

    http_strict_transport_security = Header(
        "Strict-Transport-Security",
        "max-age=63072000; includeSubdomains",
        "Ensure application is loaded over HTTPS",
    )

    x_frame_options = Header(
        "X-Frame-Options", "DENY", "Disable iframes (Clickjacking protection)"
    )

    x_xss_protection = Header(
        "X-XSS-Protection", "1; mode=block", "Enable Cross-Site Scripting filters"
    )

    x_content_type_options = Header(
        "X-Content-Type-Options", "nosniff", "Prevent MIME-sniffing"
    )

    content_security_policy = Header(
        "Content-Security-Policy",
        "script-src 'self'; object-src 'self'",
        "Prevent Cross-site injections",
    )

    referrer_policy = Header(
        "Referrer-Policy",
        "no-referrer, strict-origin-when-cross-origin"
        "Enable referrer if same origin, remove path for cross origin and disable referrer in unsupported browsers",
    )

    cache_control = Header(
        "Cache-control", "no-cache, no-store", "Prevent cacheable HTTPS response"
    )

    pragma = Header("Pragma", "no-cache", "Prevent cacheable HTTPS response")

    @staticmethod
    def secure_headers(
        hsts=True,
        frame=True,
        xss=True,
        content=True,
        csp=True,
        referrer=True,
        cache=False,
    ):
        headers = []
        if hsts:
            headers.append(Security_Headers.http_strict_transport_security)
        if frame:
            headers.append(Security_Headers.x_frame_options)
        if xss:
            headers.append(Security_Headers.x_xss_protection)
        if content:
            headers.append(Security_Headers.x_content_type_options)
        if csp:
            headers.append(Security_Headers.content_security_policy)
        if referrer:
            headers.append(Security_Headers.referrer_policy)
        if cache:
            headers.append(Security_Headers.cache_control)
            headers.append(Security_Headers.pragma)

        return headers


def default_headers():
    headers = {}
    for header in Security_Headers.secure_headers():
        headers[header.header] = header.value

    return headers


class Cookies:
    def __init__(self, value):
        self.value = value

    def secure_cookie(self, path="/", secure=True, httponly=True, samesite="lax"):
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

        return cookie_value


def responder_headers(
    req,
    resp,
    hsts=False,
    frame=True,
    xss=True,
    content=True,
    csp=False,
    referrer=True,
    cache=False,
):
    for header in Security_Headers.secure_headers(
        hsts, frame, xss, content, csp, referrer, cache
    ):
        resp.headers[header.header] = header.value


def responder_cookies(
    req, resp, name, value, path="/", secure=True, httponly=True, samesite="lax"
):
    resp.cookies[name] = Cookies.secure_cookie(value, path, secure, httponly, samesite)
