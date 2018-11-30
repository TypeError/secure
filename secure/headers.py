class Header:
    def __init__(self, header, value, info="N/A"):
        self.header = header
        self.value = value
        self.info = info


class Security_Headers:
    # Header recommendations from the OWASP Secure Headers Project
    # (https://www.owasp.org/index.php/OWASP_Secure_Headers_Project)

    server = Header("Server", "Secure")

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
        "no-referrer, strict-origin-when-cross-origin",
        "Enable full referrer if same origin, remove path for cross origin and disable referrer in unsupported browsers",
    )

    cache_control = Header(
        "Cache-control", "no-cache, no-store", "Prevent cacheable HTTPS response"
    )

    pragma = Header("Pragma", "no-cache", "Prevent cacheable HTTPS response")

    @staticmethod
    def secure_headers(
        server=True,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=True,
        referrer=True,
        cache=True,
    ):
        headers = []
        if server:
            if type(server) == str:
                Security_Headers.server.value = server
            headers.append(Security_Headers.server)
        if hsts:
            headers.append(Security_Headers.http_strict_transport_security)
        if xfo:
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


def set_headers(resp, server, hsts, xfo, xss, content, csp, referrer, cache):
    for header in Security_Headers.secure_headers(
        server, hsts, xfo, xss, content, csp, referrer, cache
    ):
        resp.headers[header.header] = header.value
