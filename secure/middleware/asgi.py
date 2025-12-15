from __future__ import annotations

from collections.abc import Awaitable, Callable, Iterable, MutableMapping
from typing import Any, TypeAlias, cast

from secure import Secure
from secure.secure import MULTI_OK

# ---------------------------------------------------------------------------
# ASGI typing (checker-friendly + Starlette add_middleware-friendly)
# ---------------------------------------------------------------------------

Scope: TypeAlias = Any
Message: TypeAlias = MutableMapping[str, Any]

Receive: TypeAlias = Callable[[], Awaitable[Any]]
Send: TypeAlias = Callable[[Any], Awaitable[None]]

ASGIApp: TypeAlias = Callable[[Scope, Receive, Send], Awaitable[None]]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _norm_str(s: str) -> str:
    """Normalize a header name for case-insensitive comparison."""
    return s.strip().lower()


def _b_norm(b: bytes) -> bytes:
    """Normalize header-name bytes for case-insensitive comparison."""
    return b.strip().lower()


def _encode_name(name: str) -> bytes:
    """Encode an HTTP header field-name as ASCII bytes (ASGI requires bytes)."""
    return name.encode("ascii")


def _encode_value(value: str) -> bytes:
    """Encode an HTTP header value as latin-1 bytes (common ASGI convention)."""
    return value.encode("latin-1")


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------


class SecureASGIMiddleware:
    """
    Add Secure's configured HTTP security headers to an ASGI application.

    This middleware wraps an ASGI app and injects headers by intercepting the
    ``http.response.start`` message. This is the most reliable way to apply
    headers for ASGI apps that do not expose a mutable response object (for
    example: Shiny for Python). It also works well with Starlette and FastAPI.

    Behavior
    --------
    - Applies only to HTTP scopes (``scope["type"] == "http"``).
    - Overwrites existing headers by default (case-insensitive) to avoid duplicate
      single-value headers (e.g., ``X-Content-Type-Options``).
    - For header names in ``multi_ok`` (default: :data:`secure.secure.MULTI_OK`),
      existing values are preserved and Secure's values are appended.
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
        provided = multi_ok if multi_ok is not None else MULTI_OK
        self.multi_ok_b = frozenset(_b_norm(_encode_name(_norm_str(h))) for h in provided)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # Starlette/FastAPI commonly treat scope as a MutableMapping, but type it loosely.
        scope_map = cast("MutableMapping[str, Any]", scope)

        if scope_map.get("type") != "http":
            return await self.app(scope, receive, send)

        async def send_wrapper(message_any: Any) -> None:
            message = cast("Message", message_any)

            if message.get("type") == "http.response.start":
                headers: list[tuple[bytes, bytes]] = list(message.get("headers", []))

                positions: dict[bytes, list[int]] = {}
                for i, (k, _v) in enumerate(headers):
                    positions.setdefault(_b_norm(k), []).append(i)

                for k, v in self.secure.headers.items():
                    kb = _encode_name(k)
                    nb = _b_norm(kb)
                    vb = _encode_value(v)

                    if nb in self.multi_ok_b:
                        headers.append((kb, vb))
                        continue

                    if nb in positions:
                        for i in reversed(positions[nb]):
                            headers.pop(i)
                        positions.pop(nb, None)

                    headers.append((kb, vb))
                    positions[nb] = [len(headers) - 1]

                message["headers"] = headers

            await send(message_any)

        return await self.app(scope, receive, send_wrapper)

    @staticmethod
    def factory(
        app: ASGIApp,
        *,
        secure: Secure | None = None,
        multi_ok: Iterable[str] | None = None,
        **_kwargs: object,
    ) -> ASGIApp:
        """
        Starlette/FastAPI add_middleware()-compatible factory.

        Some strict type checkers don't accept passing a callable middleware
        class directly to add_middleware() (because the constructor returns an
        instance, not an ASGIApp). This factory returns an ASGIApp explicitly.
        """
        del _kwargs
        return SecureASGIMiddleware(app, secure=secure, multi_ok=multi_ok)
