import asyncio
from typing import TYPE_CHECKING
import unittest

from secure import CustomHeader, Secure

if TYPE_CHECKING:
    from collections.abc import MutableMapping


class HeadersOnlyResponse:
    def __init__(self) -> None:
        self.headers: MutableMapping[str, str] = {}


class SetHeaderResponse:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def set_header(self, key: str, value: str) -> None:
        self.calls.append((key, value))


class AsyncSetHeaderResponse:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    async def set_header(self, key: str, value: str) -> None:
        self.calls.append((key, value))


class AsyncOnlySetHeader:
    async def set_header(self, key: str, value: str) -> None:
        pass


class TestSetHeaders(unittest.TestCase):
    def test_headers_mapping_path_applies_headers(self) -> None:
        secure_headers = Secure(custom=[CustomHeader("X-Test", "value")])
        response = HeadersOnlyResponse()

        secure_headers.set_headers(response)

        self.assertEqual(response.headers["X-Test"], "value")

    def test_set_headers_prefers_set_header_method(self) -> None:
        secure_headers = Secure(custom=[CustomHeader("X-Method", "value")])
        response = SetHeaderResponse()

        secure_headers.set_headers(response)

        self.assertEqual(response.calls, [("X-Method", "value")])

    def test_set_headers_async_accepts_async_set_header(self) -> None:
        secure_headers = Secure(custom=[CustomHeader("X-Async", "value")])
        response = AsyncSetHeaderResponse()

        asyncio.run(secure_headers.set_headers_async(response))

        self.assertEqual(response.calls, [("X-Async", "value")])

    def test_set_headers_rejects_async_method_in_sync_context(self) -> None:
        secure_headers = Secure(custom=[CustomHeader("X-AsyncOnly", "value")])

        with self.assertRaises(RuntimeError):
            secure_headers.set_headers(AsyncOnlySetHeader())


if __name__ == "__main__":
    unittest.main()
