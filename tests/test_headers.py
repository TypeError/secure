import unittest
import secure


class TestDefaultHeaders(unittest.TestCase):
    def test_headers(self):
        secure_headers = secure.Secure().headers()
        self.assertEqual(
            secure_headers["Strict-Transport-Security"],
            "max-age=63072000; includeSubdomains",
        )
        self.assertEqual(
            secure_headers["X-Frame-Options"],
            "SAMEORIGIN",
        )
        self.assertEqual(
            secure_headers["X-XSS-Protection"],
            "0",
        )
        self.assertEqual(
            secure_headers["X-Content-Type-Options"],
            "nosniff",
        )
        self.assertEqual(
            secure_headers["Referrer-Policy"],
            "no-referrer, strict-origin-when-cross-origin",
        )
        self.assertEqual(
            secure_headers["Cache-control"],
            "no-store",
        )


class TestHeaders(unittest.TestCase):
    def test_header(self):
        csp = (
            secure.ContentSecurityPolicy()
            .default_src("'none'")
            .base_uri("'self'")
            .connect_src("'self'", "api.spam.com")
            .frame_src("'none'")
            .img_src("'self'", "static.spam.com")
        )
        secure_headers = secure.Secure(csp=csp).headers()
        self.assertEqual(
            secure_headers["Content-Security-Policy"],
            "default-src 'none'; base-uri 'self'; "
            "connect-src 'self' api.spam.com; frame-src 'none'; img-src 'self' "
            "static.spam.com",
        )


class TestHStSHeader(unittest.TestCase):
    def test_header(self):
        hsts = (
            secure.StrictTransportSecurity()
            .include_subdomains()
            .preload()
            .max_age(2592000)
        )
        secure_headers = secure.Secure(hsts=hsts).headers()
        self.assertEqual(
            secure_headers["Strict-Transport-Security"],
            "includeSubDomains; preload; max-age=2592000",
        )


class TestXFOHeader(unittest.TestCase):
    def test_header(self):
        xfo = secure.XFrameOptions().deny()
        secure_headers = secure.Secure(xfo=xfo).headers()
        self.assertEqual(secure_headers["X-Frame-Options"], "deny")


class TestReferrerHeader(unittest.TestCase):
    def test_header(self):
        referrer = secure.ReferrerPolicy().strict_origin()
        secure_headers = secure.Secure(referrer=referrer).headers()
        self.assertEqual(secure_headers["Referrer-Policy"], "strict-origin")


class TestPermissionsHeader(unittest.TestCase):
    def test_header(self):
        permissions = (
            secure.PermissionsPolicy().geolocation("self", '"spam.com"').vibrate()
        )
        secure_headers = secure.Secure(permissions=permissions).headers()
        self.assertEqual(
            secure_headers["Permissions-Policy"],
            'geolocation=(self "spam.com"), vibrate=()',
        )


class TestCacheHeader(unittest.TestCase):
    def test_header(self):
        cache = secure.CacheControl().no_cache()
        secure_headers = secure.Secure(cache=cache).headers()
        self.assertEqual(secure_headers["Cache-Control"], "no-cache")
