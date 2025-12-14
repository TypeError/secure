from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from secure import Secure
from secure.secure import MULTI_OK

Scope = dict[str, Any]
Receive = Callable[[], Any]
Send = Callable[[dict[str, Any]], Any]
ASGIApp = Callable[[Scope, Receive, Send], Any]


def _b_norm(b: bytes) -> bytes:
    return b.strip().lower()


def _encode_name(name: str) -> bytes:
    # HTTP header field-names are ASCII
    return name.encode("ascii")


def _encode_value(value: str) -> bytes:
    # header values are bytes on the wire; latin-1 is a common safe mapping
    return value.encode("latin-1")


class SecureASGIMiddleware:
    """
    ASGI middleware that adds/overwrites security headers for HTTP responses.

    Applies only to scope["type"] == "http".

    Overwrite behavior:
      - Overwrites existing headers by default (case-insensitive)
      - For header names in `multi_ok`, it appends instead of overwriting
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
        multi_ok :
            Header names that should append instead of overwriting. Defaults to :data:`secure.secure.MULTI_OK`.
        """
        self.app = app
        self.secure = secure or Secure.with_default_headers()
        provided = multi_ok if multi_ok is not None else MULTI_OK
        # store normalized BYTES keys for fast comparisons in ASGI land
        self.multi_ok_b = frozenset(_b_norm(_encode_name(h)) for h in provided)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
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
