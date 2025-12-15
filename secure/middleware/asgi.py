from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterable, MutableMapping
from typing import Any, TypeAlias, cast

from secure import Secure
from secure.secure import MULTI_OK

# ---------------------------------------------------------------------------
# ASGI typing aliases
# ---------------------------------------------------------------------------

Scope: TypeAlias = Any
Message: TypeAlias = MutableMapping[str, Any]

Receive: TypeAlias = Callable[[], Awaitable[Any]]
Send: TypeAlias = Callable[[Any], Awaitable[None]]

ASGIApp: TypeAlias = Callable[[Scope, Receive, Send], Awaitable[None]]

# ASGI response start header list type (ASGI uses bytes for header names/values)
HeaderList: TypeAlias = list[tuple[bytes, bytes]]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _norm_str(value: str) -> str:
    """Normalize a header name for case-insensitive comparison."""
    return value.strip().lower()


def _b_norm(value: bytes) -> bytes:
    """Normalize header-name bytes for case-insensitive comparison."""
    return value.strip().lower()


def _encode_name(name: str) -> bytes:
    """
    Encode an HTTP header field-name as ASCII bytes.

    ASGI requires header names to be `bytes`. HTTP header field-names are ASCII.
    """
    return name.encode("ascii")


def _encode_value(value: str) -> bytes:
    """
    Encode an HTTP header value as latin-1 bytes.

    In ASGI servers, header values are conventionally latin-1 encoded bytes.
    (This matches typical ASGI implementations and avoids Unicode issues.)
    """
    return value.encode("latin-1")


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------


class SecureASGIMiddleware:
    """
    Apply Secure's configured HTTP security headers to an ASGI application.

    This middleware wraps an ASGI app and injects headers by intercepting the
    ``http.response.start`` message.

    When it applies
    --------------
    - Only for HTTP scopes (``scope["type"] == "http"``).
    - It does not modify websocket/lifespan/etc scopes.

    Overwrite vs append
    -------------------
    - For most headers, existing values are removed (case-insensitive) and the
      Secure value is added to avoid duplicates.
    - For headers listed in ``multi_ok`` (default: :data:`secure.secure.MULTI_OK`),
      existing values are preserved and Secure's value is appended.

    Notes
    -----
    - This approach works well for frameworks that don't expose a mutable
      response object (e.g., some ASGI toolkits) and also works with Starlette/FastAPI.
    """

    def __init__(
        self,
        app: ASGIApp,
        *,
        secure: Secure | None = None,
        multi_ok: Iterable[str] | None = None,
    ) -> None:
        self.app = app
        self.secure = secure or Secure.with_default_headers()

        provided = MULTI_OK if multi_ok is None else multi_ok
        # Normalize once during init; comparisons during request handling are bytes-based.
        self._multi_ok_b = frozenset(_b_norm(_encode_name(_norm_str(name))) for name in provided)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        scope_map = cast("MutableMapping[str, Any]", scope)
        if scope_map.get("type") != "http":
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message_any: Message) -> None:
            message = message_any

            if message.get("type") == "http.response.start":
                raw_headers = message.get("headers", [])
                headers: HeaderList = list(raw_headers)

                # Build an index of existing header positions (case-insensitive).
                # Key is normalized header name bytes.
                positions: dict[bytes, list[int]] = {}
                for i, (k, _v) in enumerate(headers):
                    positions.setdefault(_b_norm(k), []).append(i)

                # Apply Secure headers.
                for name_str, value_str in self.secure.headers.items():
                    name_b = _encode_name(name_str)
                    norm_name_b = _b_norm(name_b)
                    value_b = _encode_value(value_str)

                    if norm_name_b in self._multi_ok_b:
                        headers.append((name_b, value_b))
                        continue

                    # Remove all existing values for this header (if present).
                    if norm_name_b in positions:
                        for idx in reversed(positions[norm_name_b]):
                            headers.pop(idx)
                        positions.pop(norm_name_b, None)

                    headers.append((name_b, value_b))
                    positions[norm_name_b] = [len(headers) - 1]

                message["headers"] = headers

            await send(message_any)

        await self.app(scope, receive, send_wrapper)
