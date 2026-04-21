import asyncio
from collections.abc import Awaitable, Callable, Generator
import unittest

import secure as secure_pkg
from secure import (
    ContentSecurityPolicy,
    CustomHeader,
    Preset,
    Secure,
    Server,
    StrictTransportSecurity,
)
from secure.secure import (
    COMMA_JOIN_OK,
    DEFAULT_ALLOWED_HEADERS,
    MULTI_OK,
    HeaderSetError,
)


class MockResponse:
    def __init__(self) -> None:
        self.headers: dict[str, str] = {}

    def set_header(self, key: str, value: str) -> None:
        """A simple method to simulate the set_header method."""
        self.headers[key] = value


class MockResponseWithSetHeader:
    def __init__(self) -> None:
        self.headers: dict[str, str] = {}
        self.header_storage: dict[str, str] = {}

    def set_header(self, key: str, value: str) -> None:
        """Simulate set_header method."""
        self.header_storage[key] = value


class MockResponseAsyncSetHeader:
    def __init__(self) -> None:
        self.headers: dict[str, str] = {}
        self.header_storage: dict[str, str] = {}

    async def set_header(self, key: str, value: str) -> None:
        """Simulate async set_header method."""
        self.header_storage[key] = value


class MockResponseNoHeaders:
    pass


class _AsyncHeadersMapping:
    def __init__(self) -> None:
        self.storage: dict[str, str] = {}

    async def __setitem__(self, key: str, value: str) -> None:
        self.storage[key] = value


class MockAsyncHeadersResponse:
    def __init__(self) -> None:
        self.headers = _AsyncHeadersMapping()

    async def set_header(self, key: str, value: str) -> None:
        """Async set_header method for protocol compliance."""
        await self.headers.__setitem__(key, value)


class MockResponseRaiseSetHeader:
    def set_header(self, key: str, value: str) -> None:
        raise ValueError("boom")


class MockResponseAwaitableSetHeader:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def set_header(self, key: str, value: str) -> Awaitable[None]:
        class _Awaitable:
            def __init__(self, callback: Callable[[], None]) -> None:
                self._callback = callback

            def __await__(self) -> Generator[None, None, None]:
                async def _run() -> None:
                    self._callback()

                return _run().__await__()

        return _Awaitable(lambda: self.calls.append((key, value)))


def _expected_basic_csp_value() -> str:
    """Builder matching the CSP used by the BASIC preset."""
    return (
        ContentSecurityPolicy()
        .default_src("'self'")
        .base_uri("'self'")
        .font_src("'self'", "https:", "data:")
        .form_action("'self'")
        .frame_ancestors("'self'")
        .img_src("'self'", "data:")
        .object_src("'none'")
        .script_src("'self'")
        .script_src_attr("'none'")
        .style_src("'self'", "https:", "'unsafe-inline'")
        .upgrade_insecure_requests()
    ).header_value


class TestSecure(unittest.TestCase):
    def setUp(self) -> None:
        # Initialize Secure with some test headers
        self.secure = Secure(
            custom=[
                CustomHeader("X-Test-Header-1", "Value1"),
                CustomHeader("X-Test-Header-2", "Value2"),
            ]
        )

    def test_with_default_headers(self) -> None:
        """Test that the Balanced defaults are correctly applied."""
        secure_headers = Secure.with_default_headers()
        response = MockResponse()

        secure_headers.set_headers(response)

        self.assertNotIn("Cache-Control", response.headers)

        self.assertIn("Content-Security-Policy", response.headers)
        self.assertEqual(
            response.headers["Content-Security-Policy"],
            _expected_basic_csp_value(),
        )

        self.assertIn("Cross-Origin-Opener-Policy", response.headers)
        self.assertEqual(response.headers["Cross-Origin-Opener-Policy"], "same-origin")

        self.assertIn("Cross-Origin-Resource-Policy", response.headers)
        self.assertEqual(response.headers["Cross-Origin-Resource-Policy"], "same-origin")

        self.assertIn("Permissions-Policy", response.headers)
        self.assertEqual(
            response.headers["Permissions-Policy"],
            "geolocation=(), microphone=(), camera=()",
        )

        self.assertIn("Referrer-Policy", response.headers)
        self.assertEqual(response.headers["Referrer-Policy"], "strict-origin-when-cross-origin")

        self.assertIn("Server", response.headers)
        self.assertEqual(response.headers["Server"], "")

        self.assertIn("Strict-Transport-Security", response.headers)
        self.assertEqual(
            response.headers["Strict-Transport-Security"],
            "max-age=31536000; includeSubDomains",
        )

        self.assertIn("X-Content-Type-Options", response.headers)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

        self.assertIn("X-Frame-Options", response.headers)
        self.assertEqual(response.headers["X-Frame-Options"], "SAMEORIGIN")

        self.assertNotIn("Origin-Agent-Cluster", response.headers)
        self.assertNotIn("X-Download-Options", response.headers)
        self.assertNotIn("X-XSS-Protection", response.headers)
        self.assertNotIn("X-Permitted-Cross-Domain-Policies", response.headers)
        self.assertNotIn("X-DNS-Prefetch-Control", response.headers)

    def test_with_default_headers_matches_balanced_preset(self) -> None:
        """with_default_headers() should mirror the BALANCED preset."""
        balanced = Secure.from_preset(Preset.BALANCED)

        self.assertEqual(Secure.with_default_headers().headers, balanced.headers)

    def test_balanced_preset_omits_cache_control(self) -> None:
        """Balanced preset purposely excludes Cache-Control."""
        balanced_headers = Secure.from_preset(Preset.BALANCED).headers

        self.assertNotIn("Cache-Control", balanced_headers)

    def test_from_preset_basic(self) -> None:
        """Test that the BASIC preset is applied correctly."""
        secure_headers = Secure.from_preset(Preset.BASIC)
        response = MockResponse()

        # Apply the headers to the response object
        secure_headers.set_headers(response)

        self.assertNotIn("Cache-Control", response.headers)
        self.assertNotIn("Permissions-Policy", response.headers)
        self.assertNotIn("Server", response.headers)

        self.assertIn("Content-Security-Policy", response.headers)
        self.assertEqual(
            response.headers["Content-Security-Policy"],
            _expected_basic_csp_value(),
        )

        self.assertIn("Cross-Origin-Opener-Policy", response.headers)
        self.assertEqual(response.headers["Cross-Origin-Opener-Policy"], "same-origin")

        self.assertIn("Cross-Origin-Resource-Policy", response.headers)
        self.assertEqual(response.headers["Cross-Origin-Resource-Policy"], "same-origin")

        self.assertIn("Referrer-Policy", response.headers)
        self.assertEqual(response.headers["Referrer-Policy"], "no-referrer")

        self.assertIn("Strict-Transport-Security", response.headers)
        self.assertEqual(
            response.headers["Strict-Transport-Security"],
            "max-age=31536000; includeSubDomains",
        )

        self.assertIn("X-Content-Type-Options", response.headers)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

        self.assertIn("X-Frame-Options", response.headers)
        self.assertEqual(response.headers["X-Frame-Options"], "SAMEORIGIN")

        self.assertIn("X-Permitted-Cross-Domain-Policies", response.headers)
        self.assertEqual(response.headers["X-Permitted-Cross-Domain-Policies"], "none")

        self.assertIn("X-DNS-Prefetch-Control", response.headers)
        self.assertEqual(response.headers["X-DNS-Prefetch-Control"], "off")

        self.assertIn("Origin-Agent-Cluster", response.headers)
        self.assertEqual(response.headers["Origin-Agent-Cluster"], "?1")

        self.assertIn("X-Download-Options", response.headers)
        self.assertEqual(response.headers["X-Download-Options"], "noopen")

        self.assertIn("X-XSS-Protection", response.headers)
        self.assertEqual(response.headers["X-XSS-Protection"], "0")

    def test_from_preset_strict(self) -> None:
        """Test that the STRICT preset is applied correctly."""
        secure_headers = Secure.from_preset(Preset.STRICT)
        response = MockResponse()

        # Apply the headers to the response object
        secure_headers.set_headers(response)

        # Strict preset headers
        self.assertIn("Cache-Control", response.headers)
        self.assertEqual(response.headers["Cache-Control"], "no-store, max-age=0")

        self.assertIn("Content-Security-Policy", response.headers)
        self.assertEqual(
            response.headers["Content-Security-Policy"],
            (
                "default-src 'self'; script-src 'self'; style-src 'self'; "
                "object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
            ),
        )

        self.assertIn("Cross-Origin-Embedder-Policy", response.headers)
        self.assertEqual(response.headers["Cross-Origin-Embedder-Policy"], "require-corp")

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
            "max-age=63072000; includeSubDomains",
        )

        self.assertIn("X-Content-Type-Options", response.headers)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

        self.assertIn("X-Frame-Options", response.headers)
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")

    def test_custom_headers(self) -> None:
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

    def test_async_set_headers(self) -> None:
        """Test that async setting headers works correctly."""
        secure_headers = Secure.with_default_headers()
        response = MockResponse()

        async def mock_set_headers() -> None:
            await secure_headers.set_headers_async(response)

        asyncio.run(mock_set_headers())

        # Verify that headers are set asynchronously
        self.assertIn("Strict-Transport-Security", response.headers)
        self.assertEqual(
            response.headers["Strict-Transport-Security"],
            "max-age=31536000; includeSubDomains",
        )

        self.assertIn("X-Content-Type-Options", response.headers)
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

        # Additional assertions for other headers
        self.assertIn("Content-Security-Policy", response.headers)
        self.assertIn("Cross-Origin-Opener-Policy", response.headers)
        self.assertIn("Permissions-Policy", response.headers)
        self.assertIn("Referrer-Policy", response.headers)
        self.assertIn("Server", response.headers)
        self.assertIn("X-Frame-Options", response.headers)
        self.assertNotIn("Cache-Control", response.headers)

    def test_set_headers_with_set_header_method(self) -> None:
        """Test setting headers on a response object with set_header method."""
        response = MockResponseWithSetHeader()
        self.secure.set_headers(response)

        # Verify that headers are set using set_header method
        self.assertEqual(response.header_storage, self.secure.headers)
        # Ensure set_header was called correct number of times
        self.assertEqual(len(response.header_storage), len(self.secure.headers))

    def test_set_headers_with_headers_dict(self) -> None:
        """Test set_headers with a response object that has a headers dictionary."""
        response = MockResponse()
        self.secure.set_headers(response)

        # Verify that headers are set
        self.assertEqual(response.headers, self.secure.headers)

    def test_set_headers_async_with_async_set_header(self) -> None:
        """Test set_headers_async with a response object that has an asynchronous set_header method."""
        response = MockResponseAsyncSetHeader()

        async def test_async() -> None:
            await self.secure.set_headers_async(response)

        asyncio.run(test_async())

        # Verify that headers are set using async set_header method
        self.assertEqual(response.header_storage, self.secure.headers)
        # Ensure set_header was called correct number of times
        self.assertEqual(len(response.header_storage), len(self.secure.headers))

    def test_set_headers_async_with_headers_dict(self) -> None:
        """Test set_headers_async with a response object that has a headers dictionary."""
        response = MockResponse()
        asyncio.run(self.secure.set_headers_async(response))

        # Verify that headers are set
        self.assertEqual(response.headers, self.secure.headers)

    def test_validate_and_normalize_headers_drops_invalid_entries(self) -> None:
        """Test that invalid headers are removed before emission."""
        secure_headers = Secure(
            custom=[
                CustomHeader("X-Invalid-Header", "\n"),
                CustomHeader("X-Valid-Header", "value"),
            ]
        )
        secure_headers.validate_and_normalize_headers()

        response = MockResponse()
        secure_headers.set_headers(response)

        self.assertNotIn("X-Invalid-Header", response.headers)
        self.assertEqual(response.headers["X-Valid-Header"], "value")

    def test_validate_and_normalize_headers_applies_normalized_values(self) -> None:
        """Test that normalized headers drive both sync and async setters."""
        secure_headers = Secure(
            custom=[
                CustomHeader("X-Test-Header", "value\nwith\r\nbad"),
            ]
        )
        secure_headers.validate_and_normalize_headers()

        response_sync = MockResponse()
        secure_headers.set_headers(response_sync)
        self.assertEqual(response_sync.headers["X-Test-Header"], "value with bad")

        response_async = MockResponse()
        asyncio.run(secure_headers.set_headers_async(response_async))
        self.assertEqual(response_async.headers["X-Test-Header"], "value with bad")

        self.assertEqual(secure_headers.headers["X-Test-Header"], "value with bad")

    def test_set_headers_missing_interface(self) -> None:
        """Test that an error is raised when response object lacks required methods."""
        secure_headers = Secure.with_default_headers()
        response = MockResponseNoHeaders()

        with self.assertRaises(AttributeError) as context:
            secure_headers.set_headers(response)  # type: ignore

        self.assertIn(
            "does not support setting headers",
            str(context.exception),
        )

    def test_set_headers_with_async_set_header_in_sync_context(self) -> None:
        """Test set_headers raises RuntimeError when encountering async set_header in sync context."""
        response = MockResponseAsyncSetHeader()
        with self.assertRaises(RuntimeError):
            self.secure.set_headers(response)

    def test_set_headers_overwrites_existing_headers(self) -> None:
        """Test that existing headers are overwritten by Secure."""
        secure_headers = Secure.with_default_headers()
        response = MockResponse()
        response.headers["Referrer-Policy"] = "unsafe-url"

        # Apply the headers to the response object
        secure_headers.set_headers(response)

        # Verify that the header has been overwritten
        self.assertEqual(response.headers["Referrer-Policy"], "strict-origin-when-cross-origin")

    def test_custom_header_inclusion(self) -> None:
        """Test that custom headers are included and applied."""
        custom_header = CustomHeader("X-Custom-Header", "CustomValue")
        secure_headers = Secure(custom=[custom_header])
        response = MockResponse()

        # Apply the headers to the response object
        secure_headers.set_headers(response)

        self.assertIn("X-Custom-Header", response.headers)
        self.assertEqual(response.headers["X-Custom-Header"], "CustomValue")

    def test_headers_property(self) -> None:
        """Test that the headers property returns the correct headers."""
        secure_headers = Secure.with_default_headers()

        expected_headers = {header.header_name: header.header_value for header in secure_headers.headers_list}

        self.assertEqual(secure_headers.headers, expected_headers)

    def test_str_representation(self) -> None:
        """Test the __str__ method of Secure class."""
        secure_headers = Secure.with_default_headers()
        headers_str = str(secure_headers)

        for header in secure_headers.headers_list:
            header_line = f"{header.header_name}: {header.header_value}"
            self.assertIn(header_line, headers_str)

    def test_repr_representation(self) -> None:
        """Test the __repr__ method of Secure class."""
        secure_headers = Secure.with_default_headers()
        repr_str = repr(secure_headers)

        self.assertIn("Secure(headers_list=", repr_str)
        self.assertIn("headers_list=", repr_str)

    def test_str_representation_uses_normalized_values(self) -> None:
        """str() should reflect the normalized output used when setting headers."""
        secure_headers = Secure(
            custom=[
                CustomHeader("X-Test-Normalized", "value\nwith\r\nspaces"),
            ]
        )
        secure_headers.validate_and_normalize_headers()
        self.assertIn("X-Test-Normalized: value with spaces", str(secure_headers))

    def test_package_exports_header_constants(self) -> None:
        """The public package API should re-export the pipeline helpers the docs mention."""
        self.assertIs(secure_pkg.DEFAULT_ALLOWED_HEADERS, DEFAULT_ALLOWED_HEADERS)
        self.assertIs(secure_pkg.COMMA_JOIN_OK, COMMA_JOIN_OK)
        self.assertIs(secure_pkg.MULTI_OK, MULTI_OK)

    def test_invalid_preset(self) -> None:
        """Test that an invalid preset raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            Secure.from_preset("invalid_preset")  # type: ignore

        self.assertIn("Unknown preset", str(context.exception))

    def test_empty_secure_instance(self) -> None:
        """Test that an empty Secure instance does not set any headers."""
        self.secure = Secure()
        response = MockResponse()

        self.secure.set_headers(response)
        self.assertEqual(len(response.headers), 0)

    def test_multiple_custom_headers(self) -> None:
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

    def test_custom_strict_transport_security(self) -> None:
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

    def test_setting_headers_on_response_with_both_headers_and_set_header(self) -> None:
        """Test that headers are set on response object with both headers dict and set_header method."""

        class MockResponseWithBoth:
            def __init__(self) -> None:
                self.headers: dict[str, str] = {}
                self.header_storage: dict[str, str] = {}

            def set_header(self, key: str, value: str) -> None:
                self.header_storage[key] = value

        secure_headers = Secure.with_default_headers()
        response = MockResponseWithBoth()

        # Apply the headers to the response object
        secure_headers.set_headers(response)

        # Verify that headers are set using set_header
        self.assertIn("Strict-Transport-Security", response.header_storage)
        self.assertEqual(
            response.header_storage["Strict-Transport-Security"],
            "max-age=31536000; includeSubDomains",
        )

        # Verify that headers dict was not used
        self.assertNotIn("Strict-Transport-Security", response.headers)

    def test_header_order(self) -> None:
        """Test that headers are applied in the order they are in headers_list."""
        secure_headers = Secure.with_default_headers()
        response = MockResponse()

        secure_headers.set_headers(response)

        expected_order = [header.header_name for header in secure_headers.headers_list]
        actual_order = list(response.headers.keys())

        self.assertEqual(expected_order, actual_order)

    def test_set_headers_async_with_sync_set_header(self) -> None:
        """Test async set_headers when response has a synchronous set_header method."""
        secure_headers = Secure.with_default_headers()
        response = MockResponseWithSetHeader()

        async def mock_set_headers() -> None:
            await secure_headers.set_headers_async(response)

        asyncio.run(mock_set_headers())

        # Verify that headers are set using set_header method
        self.assertEqual(response.header_storage, secure_headers.headers)

    def test_set_headers_with_no_headers_or_set_header(self) -> None:
        """Test that an error is raised when response lacks both headers and set_header."""
        secure_headers = Secure.with_default_headers()
        response = object()  # An object with neither headers nor set_header

        with self.assertRaises(AttributeError) as context:
            secure_headers.set_headers(response)  # type: ignore

        self.assertIn(
            "does not support setting headers",
            str(context.exception),
        )

    def test_headers_list_property(self) -> None:
        """Test that headers_list contains the correct headers."""
        custom_server = Server().set("CustomServer")
        custom_csp = ContentSecurityPolicy().default_src("'self'")
        custom_headers = [CustomHeader("X-Test-Header", "TestValue")]

        secure_headers = Secure(server=custom_server, csp=custom_csp, custom=custom_headers)

        # Adjust the expected order based on how Secure initializes headers
        expected_headers_list = [custom_csp, custom_server, *custom_headers]

        self.assertEqual(secure_headers.headers_list, expected_headers_list)

    def test_headers_property_with_no_headers(self) -> None:
        """Test that headers property returns an empty dict when no headers are set."""
        secure_headers = Secure()
        self.assertEqual(secure_headers.headers, {})

    def test_headers_property_tracks_builder_mutation_after_access(self) -> None:
        """Header mapping should reflect later builder updates instead of staying cached."""
        server = Server().set("Initial")
        secure_headers = Secure(server=server)

        self.assertEqual(secure_headers.headers["Server"], "Initial")

        server.set("Updated")

        self.assertEqual(secure_headers.headers["Server"], "Updated")

    def test_allowlist_headers_drop_unexpected(self) -> None:
        """Headers not on the allowlist are removed when using drop policy."""
        secure_headers = Secure(custom=[CustomHeader("X-Not-Allowed", "value")])
        secure_headers.allowlist_headers(on_unexpected="drop")

        header_names = [h.header_name for h in secure_headers.headers_list]
        self.assertNotIn("X-Not-Allowed", header_names)

    def test_allowlist_headers_raises_on_unexpected(self) -> None:
        """Allowlist should raise when encountering unexpected names under the default policy."""
        secure_headers = Secure(custom=[CustomHeader("X-Not-Allowed", "value")])

        with self.assertRaises(ValueError):
            secure_headers.allowlist_headers()  # default on_unexpected is "raise"

    def test_allowlist_respects_allow_x_prefixed(self) -> None:
        """Allowlist can be relaxed to accept any `X-` header when requested."""
        secure_headers = Secure(custom=[CustomHeader("X-Extra-Header", "ok")])
        secure_headers.allowlist_headers(allow_x_prefixed=True)
        header_names = [h.header_name for h in secure_headers.headers_list]
        self.assertIn("X-Extra-Header", header_names)

    def test_deduplicate_concat_merges_cache_control(self) -> None:
        """Comma-joinable headers can be concatenated via concat action."""
        secure_headers = Secure(
            custom=[
                CustomHeader("Cache-Control", "max-age=0"),
                CustomHeader("Cache-Control", "no-cache"),
            ]
        )
        secure_headers.deduplicate_headers(action="concat")

        self.assertEqual(len(secure_headers.headers_list), 1)
        only_header = secure_headers.headers_list[0]
        self.assertEqual(only_header.header_name, "Cache-Control")
        self.assertEqual(only_header.header_value, "max-age=0, no-cache")

    def test_deduplicate_headers_raise_on_duplicate(self) -> None:
        """Duplicates without a merge policy still surface as errors."""
        secure_headers = Secure(
            custom=[
                CustomHeader("X-Test-Header", "a"),
                CustomHeader("X-Test-Header", "b"),
            ]
        )

        with self.assertRaises(ValueError):
            secure_headers.deduplicate_headers()

    def test_validate_and_normalize_headers_strict_rejects_crlf(self) -> None:
        """Strict mode in validation treats CR/LF as configuration errors."""
        secure_headers = Secure(
            custom=[
                CustomHeader("X-Strict", "bad\rvalue"),
            ]
        )

        with self.assertRaises(ValueError):
            secure_headers.validate_and_normalize_headers(strict=True)

    def test_validate_and_normalize_headers_is_cleared_by_headers_list_mutation(self) -> None:
        """Mutating `headers_list` should discard any normalized snapshot."""
        secure_headers = Secure(custom=[CustomHeader("X-Test", "value\nwith\r\nspaces")])
        secure_headers.validate_and_normalize_headers()

        secure_headers.headers_list.append(CustomHeader("X-New", "fresh"))

        self.assertEqual(
            secure_headers.header_items(),
            (
                ("X-Test", "value\nwith\r\nspaces"),
                ("X-New", "fresh"),
            ),
        )

    def test_validate_and_normalize_headers_is_cleared_by_builder_mutation(self) -> None:
        """Mutating an existing builder should invalidate stale normalized output."""
        server = Server().set("Initial")
        secure_headers = Secure(server=server)
        secure_headers.validate_and_normalize_headers()

        server.set("Updated")

        self.assertEqual(secure_headers.headers["Server"], "Updated")

    def test_headers_property_raises_on_duplicates(self) -> None:
        """Accessing `headers` should fail when duplicates are configured."""
        secure_headers = Secure(
            custom=[
                CustomHeader("X-Dupe", "a"),
                CustomHeader("X-Dupe", "b"),
            ]
        )

        with self.assertRaises(ValueError):
            _ = secure_headers.headers

    def test_set_headers_wraps_setter_errors(self) -> None:
        """Synchronous setter errors are surfaced as HeaderSetError."""
        secure_headers = Secure(custom=[CustomHeader("X-Test", "value")])
        response = MockResponseRaiseSetHeader()

        with self.assertRaises(HeaderSetError):
            secure_headers.set_headers(response)

    def test_set_headers_async_wraps_setter_errors(self) -> None:
        """Async setter errors propagate as HeaderSetError as well."""
        secure_headers = Secure(custom=[CustomHeader("X-Test", "value")])
        response = MockResponseRaiseSetHeader()

        async def run() -> None:
            with self.assertRaises(HeaderSetError):
                await secure_headers.set_headers_async(response)

        asyncio.run(run())

    def test_set_headers_runtime_error_on_async_setter(self) -> None:
        """Sync set_headers should detect awaitables returned from set_header."""
        secure_headers = Secure(custom=[CustomHeader("X-Test", "value")])
        response = MockResponseAwaitableSetHeader()

        with self.assertRaises(RuntimeError):
            secure_headers.set_headers(response)

    def test_set_headers_async_handles_async_headers_mapping(self) -> None:
        """Async header mappings are awaited to completion."""
        secure_headers = Secure(custom=[CustomHeader("X-Async", "value")])
        response = MockAsyncHeadersResponse()

        async def run() -> None:
            await secure_headers.set_headers_async(response)

        asyncio.run(run())

        self.assertEqual(response.headers.storage, secure_headers.headers)


if __name__ == "__main__":
    unittest.main()
