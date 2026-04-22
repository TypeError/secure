import asyncio
import unittest
from unittest import mock

from secure import DEFAULT_ALLOWED_HEADERS, MULTI_OK
from secure._internal.emit import set_headers_async
from secure._internal.normalize import normalize_header_items
from secure._internal.policy import allowlist_header_objects, deduplicate_header_objects
from secure.headers import CustomHeader


class _AsyncHeadersMapping:
    def __init__(self) -> None:
        self.storage: dict[str, str] = {}

    async def __setitem__(self, key: str, value: str) -> None:
        self.storage[key] = value


class _AsyncHeadersResponse:
    def __init__(self) -> None:
        self.headers = _AsyncHeadersMapping()


class TestInternalHelpers(unittest.TestCase):
    def test_normalize_header_items_warns_and_drops_invalid_names(self) -> None:
        logger = mock.Mock()

        items = normalize_header_items(
            (("Bad Header", "value"),),
            on_invalid="warn",
            logger=logger,
        )

        self.assertEqual(dict(items), {})
        logger.warning.assert_called_once_with("Invalid header name 'Bad Header' (RFC 7230 token required)")

    def test_normalize_header_items_preserves_obs_text_when_allowed(self) -> None:
        items = normalize_header_items(
            (("X-Obs-Text", "caf\xe9"),),
            allow_obs_text=True,
        )

        self.assertEqual(items["X-Obs-Text"], "caf\xe9")

    def test_allowlist_header_objects_warn_keeps_unexpected_headers(self) -> None:
        logger = mock.Mock()
        headers = [CustomHeader("X-App-Header", "value")]

        kept = allowlist_header_objects(
            headers,
            allowed=DEFAULT_ALLOWED_HEADERS,
            on_unexpected="warn",
            logger=logger,
        )

        self.assertEqual([header.header_name for header in kept], ["X-App-Header"])
        logger.warning.assert_called_once_with("Unexpected header %r kept (not in allowlist)", "X-App-Header")

    def test_deduplicate_header_objects_preserves_multi_ok_order(self) -> None:
        headers = [
            CustomHeader("Content-Security-Policy", "default-src 'self'"),
            CustomHeader("Content-Security-Policy", "report-uri /csp"),
        ]

        deduplicated = deduplicate_header_objects(
            headers,
            action="raise",
            comma_join_ok=frozenset(),
            multi_ok=MULTI_OK,
        )

        self.assertEqual(
            [(header.header_name, header.header_value) for header in deduplicated],
            [
                ("Content-Security-Policy", "default-src 'self'"),
                ("Content-Security-Policy", "report-uri /csp"),
            ],
        )

    def test_set_headers_async_helper_awaits_async_headers_mapping(self) -> None:
        response = _AsyncHeadersResponse()

        asyncio.run(set_headers_async(response, (("X-Test", "value"),)))

        self.assertEqual(response.headers.storage, {"X-Test": "value"})
