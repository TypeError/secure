import unittest

from secure import ContentSecurityPolicy, Preset, Secure, Server


class MockResponse:
    def __init__(self):
        self.headers: dict[str, str] = {}


class TestSecure(unittest.TestCase):
    def test_with_default_headers(self):
        """Test that default headers are correctly applied."""
        secure_headers = Secure.with_default_headers()
        response = MockResponse()

        # Apply the headers to the response object
        secure_headers.set_headers(response)

        # Check if the expected default headers are applied
        self.assertIn("Strict-Transport-Security", response.headers)
        self.assertEqual(
            response.headers["Strict-Transport-Security"],
            "max-age=31536000; includeSubDomains",
        )

        self.assertIn("X-Frame-Options", response.headers)
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")

        self.assertIn("X-Content-Type-Options", response.headers)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

        self.assertIn("Content-Security-Policy", response.headers)
        self.assertEqual(
            response.headers["Content-Security-Policy"], "default-src 'self'"
        )

        self.assertIn("Referrer-Policy", response.headers)
        self.assertEqual(
            response.headers["Referrer-Policy"], "no-referrer-when-downgrade"
        )

    def test_from_preset_basic(self):
        """Test that the BASIC preset is applied correctly."""
        secure_headers = Secure.from_preset(Preset.BASIC)
        response = MockResponse()

        # Apply the headers to the response object
        secure_headers.set_headers(response)

        self.assertIn("Strict-Transport-Security", response.headers)
        self.assertEqual(
            response.headers["Strict-Transport-Security"], "max-age=63072000"
        )

        self.assertIn("X-Frame-Options", response.headers)
        self.assertEqual(response.headers["X-Frame-Options"], "SAMEORIGIN")

        self.assertIn("Referrer-Policy", response.headers)
        self.assertEqual(
            response.headers["Referrer-Policy"], "no-referrer-when-downgrade"
        )

    def test_from_preset_strict(self):
        """Test that the STRICT preset is applied correctly."""
        secure_headers = Secure.from_preset(Preset.STRICT)
        response = MockResponse()

        # Apply the headers to the response object
        secure_headers.set_headers(response)

        self.assertIn("Strict-Transport-Security", response.headers)
        self.assertEqual(
            response.headers["Strict-Transport-Security"],
            "max-age=31536000; includeSubDomains; preload",
        )

        self.assertIn("X-Frame-Options", response.headers)
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")

        self.assertIn("Content-Security-Policy", response.headers)
        self.assertEqual(
            response.headers["Content-Security-Policy"], "default-src 'self'"
        )

        self.assertIn("Referrer-Policy", response.headers)
        self.assertEqual(response.headers["Referrer-Policy"], "no-referrer")

    def test_custom_headers(self):
        """Test that custom headers are applied correctly."""
        custom_server = Server().set("SecureServer")
        custom_csp = ContentSecurityPolicy().default_src("'none'").img_src("'self'")

        secure_headers = Secure(server=custom_server, csp=custom_csp)
        response = MockResponse()

        # Apply the custom headers
        secure_headers.set_headers(response)

        self.assertIn("Server", response.headers)
        self.assertEqual(response.headers["Server"], "SecureServer")

        self.assertIn("Content-Security-Policy", response.headers)
        self.assertEqual(
            response.headers["Content-Security-Policy"],
            "default-src 'none'; img-src 'self'",
        )

    def test_async_set_headers(self):
        """Test that async setting headers works correctly."""
        secure_headers = Secure.with_default_headers()
        response = MockResponse()

        async def mock_set_headers():
            await secure_headers.set_headers_async(response)

        import asyncio

        asyncio.run(mock_set_headers())

        self.assertIn("Strict-Transport-Security", response.headers)
        self.assertEqual(
            response.headers["Strict-Transport-Security"],
            "max-age=31536000; includeSubDomains",
        )


if __name__ == "__main__":
    unittest.main()
