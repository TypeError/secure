class Header:
    def __init__(self, header, value, info="N/A"):
        self.header = header
        self.value = value
        self.info = info


class Security_Headers:
    # Header recommendations from the OWASP Secure Headers Project
    # (https://www.owasp.org/index.php/OWASP_Secure_Headers_Project)

    server = Header("Server", "NULL")

    http_strict_transport_security = Header(
        "Strict-Transport-Security",
        "max-age=63072000; includeSubdomains",
        "Ensure application communication is sent over HTTPS",
    )

    x_frame_options = Header(
        "X-Frame-Options",
        "SAMEORIGIN",
        "Disable framing from different origins (clickjacking defense)",
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
        "Cache-control",
        "no-cache, no-store, must-revalidate",
        "Prevent cacheable HTTPS response",
    )

    pragma = Header("Pragma", "no-cache", "Prevent cacheable HTTPS response")

    feature_policy = Header(
        "Feature-Policy",
        "accelerometer 'none'; ambient-light-sensor 'none'; autoplay 'none'; camera 'none'; encrypted-media 'none';"
        + "fullscreen 'none'; geolocation 'none'; gyroscope 'none'; magnetometer 'none'; microphone 'none'; midi 'none';"
        + "payment 'none'; picture-in-picture 'none'; speaker 'none'; sync-xhr 'none'; usb 'none'; vr 'none';",
    )

    @staticmethod
    def secure_headers(
        server=False,
        hsts=True,
        xfo=True,
        xss=True,
        content=True,
        csp=False,
        referrer=True,
        cache=True,
        feature=False,
    ):
        headers = []
        if server:
            if type(server) == str:
                Security_Headers.server.value = server
            headers.append(Security_Headers.server)
        if hsts:
            if type(hsts) == str:
                Security_Headers.http_strict_transport_security.value = hsts
            headers.append(Security_Headers.http_strict_transport_security)
        if xfo:
            if type(xfo) == str:
                Security_Headers.x_frame_options.value = xfo
            headers.append(Security_Headers.x_frame_options)
        if xss:
            if type(xss) == str:
                Security_Headers.x_xss_protection.value = xss
            headers.append(Security_Headers.x_xss_protection)
        if content:
            if type(content) == str:
                Security_Headers.x_content_type_options.value = content
            headers.append(Security_Headers.x_content_type_options)
        if csp:
            if type(csp) == str:
                Security_Headers.content_security_policy.value = csp
            headers.append(Security_Headers.content_security_policy)
        if referrer:
            if type(referrer) == str:
                Security_Headers.referrer_policy.value = referrer
            headers.append(Security_Headers.referrer_policy)
        if cache:
            if type(cache) == str:
                Security_Headers.cache_control.value = cache
                headers.append(Security_Headers.cache_control)
            else:
                headers.append(Security_Headers.cache_control)
                headers.append(Security_Headers.pragma)
        if feature:
            if type(feature) == str:
                Security_Headers.referrer_policy.value = feature
            headers.append(Security_Headers.feature_policy)

        return headers


def default_headers():
    headers = {}
    for header in Security_Headers.secure_headers():
        headers[header.header] = header.value

    return headers


def dict_headers(server, hsts, xfo, xss, content, csp, referrer, cache, feature):
    headers = {}
    for header in Security_Headers.secure_headers(
        server, hsts, xfo, xss, content, csp, referrer, cache, feature
    ):
        headers[header.header] = header.value
    return headers


def tuple_headers(server, hsts, xfo, xss, content, csp, referrer, cache, feature):
    headers = []
    for header in Security_Headers.secure_headers(
        server, hsts, xfo, xss, content, csp, referrer, cache, feature
    ):
        headers.append((header.header, header.value))
    return headers


def set_header_dict(
    response, server, hsts, xfo, xss, content, csp, referrer, cache, feature
):
    for header in Security_Headers.secure_headers(
        server, hsts, xfo, xss, content, csp, referrer, cache, feature
    ):
        response.headers[header.header] = header.value


def set_header_tuple(
    response, server, hsts, xfo, xss, content, csp, referrer, cache, feature
):
    for header in Security_Headers.secure_headers(
        server, hsts, xfo, xss, content, csp, referrer, cache, feature
    ):
        response.set_header(header.header, header.value)
