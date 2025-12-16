import unittest

import secure
import secure.headers
import secure.middleware


class TestExportSurface(unittest.TestCase):
    def test_secure_package_exports(self) -> None:
        expected = {
            "COMMA_JOIN_OK",
            "DEFAULT_ALLOWED_HEADERS",
            "MULTI_OK",
            "CacheControl",
            "ContentSecurityPolicy",
            "CrossOriginEmbedderPolicy",
            "CrossOriginOpenerPolicy",
            "CrossOriginResourcePolicy",
            "CustomHeader",
            "PermissionsPolicy",
            "Preset",
            "ReferrerPolicy",
            "Secure",
            "Server",
            "StrictTransportSecurity",
            "XDnsPrefetchControl",
            "XContentTypeOptions",
            "XFrameOptions",
            "XPermittedCrossDomainPolicies",
        }

        self.assertEqual(set(secure.__all__), expected)
        for name in expected:
            with self.subTest(export=name):
                self.assertTrue(hasattr(secure, name))

    def test_headers_package_exports(self) -> None:
        expected = {
            "BaseHeader",
            "CacheControl",
            "ContentSecurityPolicy",
            "CrossOriginEmbedderPolicy",
            "CrossOriginOpenerPolicy",
            "CrossOriginResourcePolicy",
            "CustomHeader",
            "PermissionsPolicy",
            "ReferrerPolicy",
            "Server",
            "StrictTransportSecurity",
            "XContentTypeOptions",
            "XDnsPrefetchControl",
            "XFrameOptions",
            "XPermittedCrossDomainPolicies",
        }

        self.assertEqual(set(secure.headers.__all__), expected)
        for name in expected:
            with self.subTest(header=name):
                self.assertTrue(hasattr(secure.headers, name))

    def test_middleware_package_exports(self) -> None:
        expected = {"SecureASGIMiddleware", "SecureWSGIMiddleware"}

        self.assertEqual(set(secure.middleware.__all__), expected)
        for name in expected:
            with self.subTest(middleware=name):
                self.assertTrue(hasattr(secure.middleware, name))
