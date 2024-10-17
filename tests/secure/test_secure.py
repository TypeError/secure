import asyncio
import unittest

from secure import (
    ContentSecurityPolicy,
    CustomHeader,
    Preset,
    Secure,
    Server,
    StrictTransportSecurity,
)


class MockResponse:
    def __init__(self):
        self.headers: dict[str, str] = {}

    def set_header(self, key: str, value: str):
        """A simple method to simulate the set_header method."""
        self.headers[key] = value


class MockResponseWithSetHeader:
    def __init__(self):
        self.headers: dict[str, str] = {}
        self.header_storage: dict[str, str] = {}

    def set_header(self, key: str, value: str):
        """Simulate set_header method."""
        self.header_storage[key] = value


class MockResponseAsyncSetHeader:
    def __init__(self):
        self.headers: dict[str, str] = {}
        self.header_storage: dict[str, str] = {}

    async def set_header(self, key: str, value: str):
        """Simulate async set_header method."""
        self.header_storage[key] = value


class MockResponseNoHeaders:
    pass


class TestSecure(unittest.TestCase):
    def setUp(self):
        # Initialize Secure with some test headers
        self.secure = Secure(
            custom=[
                CustomHeader("X-Test-Header-1", "Value1"),
                CustomHeader("X-Test-Header-2", "Value2"),
            ]
        )
        # Precompute headers dictionary
        self.secure.headers = {
            header.header_name: header.header_value
            for header in self.secure.headers_list
        }

    def test_with_default_headers(self):
        """Test that default headers are correctly applied."""
        secure_headers = Secure.with_default_headers()
        response = MockResponse()

        # Apply the headers to the response object
        secure_headers.set_headers(response)

        # Check if the expected default headers are applied
        self.assertIn("Cache-Control", response.headers)
        self.assertEqual(response.headers["Cache-Control"], "no-store")

        self.assertIn("Content-Security-Policy", response.headers)
        self.assertEqual(
            response.headers["Content-Security-Policy"],
            "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'",
        )

        self.assertIn("Cross-Origin-Opener-Policy", response.headers)
        self.assertEqual(response.headers["Cross-Origin-Opener-Policy"], "same-origin")

        self.assertNotIn("Cross-Origin-Embedder-Policy", response.headers)

        self.assertIn("Permissions-Policy", response.headers)
        self.assertEqual(
            response.headers["Permissions-Policy"],
            "geolocation=(), microphone=(), camera=()",
        )

        self.assertIn("Referrer-Policy", response.headers)
        self.assertEqual(
            response.headers["Referrer-Policy"], "strict-origin-when-cross-origin"
        )

        self.assertIn("Server", response.headers)
        self.assertEqual(response.headers["Server"], "")

        self.assertIn("Strict-Transport-Security", response.headers)
        self.assertEqual(
            response.headers["Strict-Transport-Security"],
            "max-age=31536000",
        )

        self.assertIn("X-Content-Type-Options", response.headers)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

        self.assertIn("X-Frame-Options", response.headers)
        self.assertEqual(response.headers["X-Frame-Options"], "SAMEORIGIN")

    def test_from_preset_basic(self):
        """Test that the BASIC preset is applied correctly."""
        secure_headers = Secure.from_preset(Preset.BASIC)
        response = MockResponse()

        # Apply the headers to the response object
        secure_headers.set_headers(response)

        # Basic preset headers
        self.assertIn("Cache-Control", response.headers)
        self.assertEqual(response.headers["Cache-Control"], "no-store")

        self.assertIn("Referrer-Policy", response.headers)
        self.assertEqual(
            response.headers["Referrer-Policy"], "strict-origin-when-cross-origin"
        )

        self.assertIn("Server", response.headers)
        self.assertEqual(response.headers["Server"], "")

        self.assertIn("Strict-Transport-Security", response.headers)
        self.assertEqual(
            response.headers["Strict-Transport-Security"], "max-age=31536000"
        )

        self.assertIn("X-Content-Type-Options", response.headers)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

        self.assertIn("X-Frame-Options", response.headers)
        self.assertEqual(response.headers["X-Frame-Options"], "SAMEORIGIN")

        # Optional headers in basic preset
        self.assertNotIn("Content-Security-Policy", response.headers)
        self.assertNotIn("Permissions-Policy", response.headers)
        self.assertNotIn("Cross-Origin-Opener-Policy", response.headers)

    def test_from_preset_strict(self):
        """Test that the STRICT preset is applied correctly."""
        secure_headers = Secure.from_preset(Preset.STRICT)
        response = MockResponse()

        # Apply the headers to the response object
        secure_headers.set_headers(response)

        # Strict preset headers
        self.assertIn("Cache-Control", response.headers)
        self.assertEqual(response.headers["Cache-Control"], "no-store")

        self.assertIn("Content-Security-Policy", response.headers)
        self.assertEqual(
            response.headers["Content-Security-Policy"],
            (
                "default-src 'self'; script-src 'self'; style-src 'self'; "
                "object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
            ),
        )

        self.assertIn("Cross-Origin-Embedder-Policy", response.headers)
        self.assertEqual(
            response.headers["Cross-Origin-Embedder-Policy"], "require-corp"
        )

        self.assertIn("Cross-Origin-Opener-Policy", response.headers)
        self.assertEqual(response.headers["Cross-Origin-Opener-Policy"], "same-origin")

        self.assertIn("Permissions-Policy", response.headers)
        self.assertEqual(
            response.headers["Permissions-Policy"],
            "geolocation=(), microphone=(), camera=()",
        )

        self.assertIn("Referrer-Policy", response.headers)
        self.assertEqual(response.headers["Referrer-Policy"], "no-referrer")

        self.assertIn("Server", response.headers)
        self.assertEqual(response.headers["Server"], "")

        self.assertIn("Strict-Transport-Security", response.headers)
        self.assertEqual(
            response.headers["Strict-Transport-Security"],
            "max-age=63072000; includeSubDomains; preload",
        )

        self.assertIn("X-Content-Type-Options", response.headers)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

        self.assertIn("X-Frame-Options", response.headers)
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")

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

        asyncio.run(mock_set_headers())

        # Verify that headers are set asynchronously
        self.assertIn("Strict-Transport-Security", response.headers)
        self.assertEqual(
            response.headers["Strict-Transport-Security"],
            "max-age=31536000",
        )

        self.assertIn("X-Content-Type-Options", response.headers)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

        # Additional assertions for other headers
        self.assertIn("Cache-Control", response.headers)
        self.assertIn("Content-Security-Policy", response.headers)
        self.assertIn("Cross-Origin-Opener-Policy", response.headers)
        self.assertIn("Permissions-Policy", response.headers)
        self.assertIn("Referrer-Policy", response.headers)
        self.assertIn("Server", response.headers)
        self.assertIn("X-Frame-Options", response.headers)

    def test_set_headers_with_set_header_method(self):
        """Test setting headers on a response object with set_header method."""
        response = MockResponseWithSetHeader()
        self.secure.set_headers(response)

        # Verify that headers are set using set_header method
        self.assertEqual(response.header_storage, self.secure.headers)
        # Ensure set_header was called correct number of times
        self.assertEqual(len(response.header_storage), len(self.secure.headers))

    def test_set_headers_with_headers_dict(self):
        """Test set_headers with a response object that has a headers dictionary."""
        response = MockResponse()
        self.secure.set_headers(response)

        # Verify that headers are set
        self.assertEqual(response.headers, self.secure.headers)

    def test_set_headers_async_with_async_set_header(self):
        """Test set_headers_async with a response object that has an asynchronous set_header method."""
        response = MockResponseAsyncSetHeader()

        async def test_async():
            await self.secure.set_headers_async(response)

        asyncio.run(test_async())

        # Verify that headers are set using async set_header method
        self.assertEqual(response.header_storage, self.secure.headers)
        # Ensure set_header was called correct number of times
        self.assertEqual(len(response.header_storage), len(self.secure.headers))

    def test_set_headers_async_with_headers_dict(self):
        """Test set_headers_async with a response object that has a headers dictionary."""
        response = MockResponse()
        asyncio.run(self.secure.set_headers_async(response))

        # Verify that headers are set
        self.assertEqual(response.headers, self.secure.headers)

    def test_set_headers_missing_interface(self):
        """Test that an error is raised when response object lacks required methods."""
        secure_headers = Secure.with_default_headers()
        response = MockResponseNoHeaders()

        with self.assertRaises(AttributeError) as context:
            secure_headers.set_headers(response)  # type: ignore

        self.assertIn(
            "does not support setting headers",
            str(context.exception),
        )

    def test_set_headers_with_async_set_header_in_sync_context(self):
        """Test set_headers raises RuntimeError when encountering async set_header in sync context."""
        response = MockResponseAsyncSetHeader()
        with self.assertRaises(RuntimeError):
            self.secure.set_headers(response)

    def test_set_headers_overwrites_existing_headers(self):
        """Test that existing headers are overwritten by Secure."""
        secure_headers = Secure.with_default_headers()
        response = MockResponse()
        response.headers["Cache-Control"] = "public"

        # Apply the headers to the response object
        secure_headers.set_headers(response)

        # Verify that the header has been overwritten
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_custom_header_inclusion(self):
        """Test that custom headers are included and applied."""
        custom_header = CustomHeader("X-Custom-Header", "CustomValue")
        secure_headers = Secure(custom=[custom_header])
        response = MockResponse()

        # Apply the headers to the response object
        secure_headers.set_headers(response)

        self.assertIn("X-Custom-Header", response.headers)
        self.assertEqual(response.headers["X-Custom-Header"], "CustomValue")

    def test_headers_property(self):
        """Test that the headers property returns the correct headers."""
        secure_headers = Secure.with_default_headers()

        expected_headers = {
            header.header_name: header.header_value
            for header in secure_headers.headers_list
        }

        self.assertEqual(secure_headers.headers, expected_headers)

    def test_str_representation(self):
        """Test the __str__ method of Secure class."""
        secure_headers = Secure.with_default_headers()
        headers_str = str(secure_headers)

        for header in secure_headers.headers_list:
            header_line = f"{header.header_name}: {header.header_value}"
            self.assertIn(header_line, headers_str)

    def test_repr_representation(self):
        """Test the __repr__ method of Secure class."""
        secure_headers = Secure.with_default_headers()
        repr_str = repr(secure_headers)

        self.assertIn("Secure(headers_list=", repr_str)
        self.assertIn("headers_list=", repr_str)

    def test_invalid_preset(self):
        """Test that an invalid preset raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            Secure.from_preset("invalid_preset")  # type: ignore

        self.assertIn("Unknown preset", str(context.exception))

    def test_empty_secure_instance(self):
        """Test that an empty Secure instance does not set any headers."""
        self.secure = Secure()
        response = MockResponse()

        self.secure.set_headers(response)
        self.assertEqual(len(response.headers), 0)

    def test_multiple_custom_headers(self):
        """Test that multiple custom headers are applied correctly."""
        custom_headers = [
            CustomHeader("X-Custom-Header-1", "Value1"),
            CustomHeader("X-Custom-Header-2", "Value2"),
        ]
        secure_headers = Secure(custom=custom_headers)
        response = MockResponse()

        secure_headers.set_headers(response)

        self.assertIn("X-Custom-Header-1", response.headers)
        self.assertEqual(response.headers["X-Custom-Header-1"], "Value1")

        self.assertIn("X-Custom-Header-2", response.headers)
        self.assertEqual(response.headers["X-Custom-Header-2"], "Value2")

    def test_custom_strict_transport_security(self):
        """Test setting a custom Strict-Transport-Security header."""
        custom_hsts = StrictTransportSecurity().max_age(123456).include_subdomains()
        secure_headers = Secure(hsts=custom_hsts)
        response = MockResponse()

        secure_headers.set_headers(response)

        self.assertIn("Strict-Transport-Security", response.headers)
        self.assertEqual(
            response.headers["Strict-Transport-Security"],
            "max-age=123456; includeSubDomains",
        )

    def test_setting_headers_on_response_with_both_headers_and_set_header(self):
        """Test that headers are set on response object with both headers dict and set_header method."""

        class MockResponseWithBoth:
            def __init__(self):
                self.headers: dict[str, str] = {}
                self.header_storage: dict[str, str] = {}

            def set_header(self, key: str, value: str):
                self.header_storage[key] = value

        secure_headers = Secure.with_default_headers()
        response = MockResponseWithBoth()

        # Apply the headers to the response object
        secure_headers.set_headers(response)

        # Verify that headers are set using set_header
        self.assertIn("Strict-Transport-Security", response.header_storage)
        self.assertEqual(
            response.header_storage["Strict-Transport-Security"], "max-age=31536000"
        )

        # Verify that headers dict was not used
        self.assertNotIn("Strict-Transport-Security", response.headers)

    def test_header_order(self):
        """Test that headers are applied in the order they are in headers_list."""
        secure_headers = Secure.with_default_headers()
        response = MockResponse()

        secure_headers.set_headers(response)

        expected_order = [header.header_name for header in secure_headers.headers_list]
        actual_order = list(response.headers.keys())

        self.assertEqual(expected_order, actual_order)

    def test_set_headers_async_with_sync_set_header(self):
        """Test async set_headers when response has a synchronous set_header method."""
        secure_headers = Secure.with_default_headers()
        response = MockResponseWithSetHeader()

        async def mock_set_headers():
            await secure_headers.set_headers_async(response)

        asyncio.run(mock_set_headers())

        # Verify that headers are set using set_header method
        self.assertEqual(response.header_storage, secure_headers.headers)

    def test_set_headers_with_no_headers_or_set_header(self):
        """Test that an error is raised when response lacks both headers and set_header."""
        secure_headers = Secure.with_default_headers()
        response = object()  # An object with neither headers nor set_header

        with self.assertRaises(AttributeError) as context:
            secure_headers.set_headers(response)  # type: ignore

        self.assertIn(
            "does not support setting headers",
            str(context.exception),
        )

    def test_headers_list_property(self):
        """Test that headers_list contains the correct headers."""
        custom_server = Server().set("CustomServer")
        custom_csp = ContentSecurityPolicy().default_src("'self'")
        custom_headers = [CustomHeader("X-Test-Header", "TestValue")]

        secure_headers = Secure(
            server=custom_server, csp=custom_csp, custom=custom_headers
        )

        # Adjust the expected order based on how Secure initializes headers
        expected_headers_list = [custom_csp, custom_server] + custom_headers

        self.assertEqual(secure_headers.headers_list, expected_headers_list)

    def test_headers_property_with_no_headers(self):
        """Test that headers property returns an empty dict when no headers are set."""
        secure_headers = Secure()
        self.assertEqual(secure_headers.headers, {})


if __name__ == "__main__":
    unittest.main()
