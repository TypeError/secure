from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from secure import Secure
from secure.secure import MULTI_OK

Scope = dict[str, Any]
Receive = Callable[[], Any]
Send = Callable[[dict[str, Any]], Any]
ASGIApp = Callable[[Scope, Receive, Send], Any]


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

    Notes
    -----
    - WebSocket scopes are not modified.
    - Headers are injected only at response start; headers cannot be changed
      after the ``http.response.start`` event has been sent.
    - Header names are encoded as ASCII bytes; values are encoded as latin-1 bytes.

    Examples
    --------
    Shiny for Python:

    >>> from shiny import App, ui
    >>> from secure.middleware import SecureASGIMiddleware
    >>> app = App(ui.page_fluid("ok"), server=None)
    >>> app = SecureASGIMiddleware(app)

    FastAPI / Starlette:

    >>> from secure.middleware import SecureASGIMiddleware
    >>> app = SecureASGIMiddleware(app)
    """

    def __init__(
        self,
        app: ASGIApp,
        *,
        secure: Secure | None = None,
        multi_ok: Iterable[str] | None = None,
    ) -> None:
        """
        Parameters
        ----------
        app:
            The ASGI application to wrap.
        secure:
            A configured :class:`~secure.Secure` instance. If omitted, uses
            :meth:`~secure.Secure.with_default_headers`.
        multi_ok:
            Header names allowed to appear multiple times in a response. For these,
            Secure's value is appended instead of overwriting. If omitted, defaults
            to :data:`secure.secure.MULTI_OK`.
        """
        self.app = app
        self.secure = secure or Secure.with_default_headers()
        provided = multi_ok if multi_ok is not None else MULTI_OK

        # Store normalized BYTES keys for fast comparisons in ASGI land.
        # Normalize as str first (strip/lower), then encode.
        self.multi_ok_b = frozenset(_b_norm(_encode_name(_norm_str(h))) for h in provided)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        Invoke the wrapped ASGI app, injecting configured security headers.

        This wraps the downstream ``send`` callable so we can modify the outgoing
        ``http.response.start`` message (where headers are emitted).
        """
        if scope.get("type") != "http":
            return await self.app(scope, receive, send)

        async def send_wrapper(message: dict[str, Any]) -> None:
            if message.get("type") == "http.response.start":
                headers: list[tuple[bytes, bytes]] = list(message.get("headers", []))

                # Map normalized header name -> list of indices
                positions: dict[bytes, list[int]] = {}
                for i, (k, _v) in enumerate(headers):
                    positions.setdefault(_b_norm(k), []).append(i)

                # Apply secure headers (encode per-request so overrides are reflected)
                for k, v in self.secure.headers.items():
                    kb = _encode_name(k)
                    nb = _b_norm(kb)
                    vb = _encode_value(v)

                    if nb in self.multi_ok_b:
                        headers.append((kb, vb))
                        continue

                    # Overwrite semantics: remove all existing, then append one
                    if nb in positions:
                        for i in reversed(positions[nb]):
                            headers.pop(i)
                        positions.pop(nb, None)

                    headers.append((kb, vb))
                    positions[nb] = [len(headers) - 1]

                message["headers"] = headers

            return await send(message)

        return await self.app(scope, receive, send_wrapper)
