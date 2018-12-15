from .policies import get_policy, get_policy_multi_opt


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
        header="Strict-Transport-Security",
        value="max-age=63072000; includeSubdomains",
        info="Ensure application communication is sent over HTTPS",
    )

    x_frame_options = Header(
        header="X-Frame-Options",
        value="SAMEORIGIN",
        info="Disable framing from different origins (clickjacking defense)",
    )

    x_xss_protection = Header(
        header="X-XSS-Protection",
        value="1; mode=block",
        info="Enable Cross-Site Scripting filters",
    )

    x_content_type_options = Header(
        header="X-Content-Type-Options", value="nosniff", info="Prevent MIME-sniffing"
    )

    content_security_policy = Header(
        header="Content-Security-Policy",
        value="script-src 'self'; object-src 'self'",
        info="Prevent Cross-site injections",
    )

    referrer_policy = Header(
        header="Referrer-Policy",
        value="no-referrer, strict-origin-when-cross-origin",
        info="Enable full referrer if same origin, remove path for cross origin and disable referrer in unsupported browsers",
    )

    cache_control = Header(
        header="Cache-control",
        value="no-cache, no-store, must-revalidate, max-age=0",
        info="Prevent cacheable HTTPS response",
    )

    pragma = Header(
        header="Pragma", value="no-cache", info="Prevent cacheable HTTPS response"
    )

    expires = Header(
        header="Expires", value="0", info="Prevent cacheable HTTPS response"
    )

    feature_policy = Header(
        header="Feature-Policy",
        value="accelerometer 'none'; ambient-light-sensor 'none'; autoplay 'none'; camera 'none'; "
        + "encrypted-media 'none'; fullscreen 'none'; geolocation 'none'; gyroscope 'none'; magnetometer 'none'; "
        + "microphone 'none'; midi 'none'; payment 'none'; picture-in-picture 'none'; speaker 'none'; "
        + "sync-xhr 'none'; usb 'none'; vr 'none';",
        info="Disable browser features and APIs",
    )

    @staticmethod
    def secure_headers(
        server=False,
        hsts=True,
        xfo=True,
        xxp=True,
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
            elif hasattr(hsts, "hsts_policy"):
                policy_value = get_policy(hsts, "; ")
                Security_Headers.http_strict_transport_security.value = policy_value
            headers.append(Security_Headers.http_strict_transport_security)
        if xfo:
            if type(xfo) == str:
                Security_Headers.x_frame_options.value = xfo
            elif hasattr(xfo, "xfo_policy"):
                Security_Headers.x_frame_options.value = xfo.policy
            headers.append(Security_Headers.x_frame_options)
        if xxp:
            if type(xxp) == str:
                Security_Headers.x_xss_protection.value = xxp
            elif hasattr(xxp, "xxp_policy"):
                Security_Headers.x_xss_protection.value = xxp.policy
            headers.append(Security_Headers.x_xss_protection)
        if content:
            if type(content) == str:
                Security_Headers.x_content_type_options.value = content
            headers.append(Security_Headers.x_content_type_options)
        if csp:
            if type(csp) == str:
                Security_Headers.content_security_policy.value = csp
            elif hasattr(csp, "csp_policy"):
                policy_value = get_policy_multi_opt(csp)
                Security_Headers.content_security_policy.value = policy_value
            headers.append(Security_Headers.content_security_policy)
        if referrer:
            if type(referrer) == str:
                Security_Headers.referrer_policy.value = referrer
            elif hasattr(referrer, "referrer_policy"):
                policy_value = get_policy(referrer, ", ")
                Security_Headers.referrer_policy.value = policy_value
            headers.append(Security_Headers.referrer_policy)
        if cache:
            if type(cache) == str:
                Security_Headers.cache_control.value = cache
            elif hasattr(cache, "cache_policy"):
                policy_value = get_policy(cache, ", ")
                Security_Headers.cache_control.value = policy_value
            else:
                headers.append(Security_Headers.pragma)
                headers.append(Security_Headers.expires)
            headers.append(Security_Headers.cache_control)

        if feature:
            if type(feature) == str:
                Security_Headers.feature_policy.value = feature
            elif hasattr(feature, "feature_policy"):
                policy_value = get_policy_multi_opt(feature)
                Security_Headers.feature_policy.value = policy_value
            headers.append(Security_Headers.feature_policy)

        return headers


def default_headers():
    headers = {}
    for header in Security_Headers.secure_headers():
        headers[header.header] = header.value

    return headers


def dict_headers(server, hsts, xfo, xxp, content, csp, referrer, cache, feature):
    headers = {}
    for header in Security_Headers.secure_headers(
        server, hsts, xfo, xxp, content, csp, referrer, cache, feature
    ):
        headers[header.header] = header.value
    return headers


def tuple_headers(server, hsts, xfo, xxp, content, csp, referrer, cache, feature):
    headers = []
    for header in Security_Headers.secure_headers(
        server, hsts, xfo, xxp, content, csp, referrer, cache, feature
    ):
        headers.append((header.header, header.value))
    return headers


def set_header_dict(
    response, server, hsts, xfo, xxp, content, csp, referrer, cache, feature
):
    for header in Security_Headers.secure_headers(
        server, hsts, xfo, xxp, content, csp, referrer, cache, feature
    ):
        response.headers[header.header] = header.value


def set_header_tuple(
    response, server, hsts, xfo, xxp, content, csp, referrer, cache, feature
):
    for header in Security_Headers.secure_headers(
        server, hsts, xfo, xxp, content, csp, referrer, cache, feature
    ):
        response.set_header(header.header, header.value)
