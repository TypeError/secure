from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from secure import Secure
from secure.secure import MULTI_OK

WSGIEnviron = dict[str, Any]
ExcInfo = tuple[type[BaseException], BaseException, Any] | None
WriteCallable = Callable[[bytes], object]
StartResponse = Callable[[str, list[tuple[str, str]], ExcInfo], WriteCallable]
WSGIApp = Callable[[WSGIEnviron, StartResponse], Iterable[bytes]]


def _norm_str(s: str) -> str:
    return s.strip().lower()


class SecureWSGIMiddleware:
    """
    WSGI middleware that adds/overwrites security headers on every response.

    Overwrite behavior:
      - Overwrites existing headers by default (case-insensitive)
      - For header names in `multi_ok`, it appends instead of overwriting
    """

    def __init__(
        self,
        app: WSGIApp,
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
        self.multi_ok = frozenset(_norm_str(h) for h in provided)

    def __call__(self, environ: WSGIEnviron, start_response: StartResponse) -> Iterable[bytes]:
        def custom_start_response(
            status: str, headers: list[tuple[str, str]], exc_info: ExcInfo = None
        ) -> WriteCallable:
            out: list[tuple[str, str]] = list(headers)

            # Track existing occurrences by normalized key
            positions: dict[str, list[int]] = {}
            for i, (k, _v) in enumerate(out):
                positions.setdefault(_norm_str(k), []).append(i)

            # Apply secure headers
            for k, v in self.secure.headers.items():
                nk = _norm_str(k)

                if nk in self.multi_ok:
                    out.append((k, v))
                    continue

                # Remove all existing occurrences, then append ours (overwrite semantics)
                if nk in positions:
                    for i in reversed(positions[nk]):
                        out.pop(i)
                    positions.pop(nk, None)

                out.append((k, v))
                positions[nk] = [len(out) - 1]

            return start_response(status, out, exc_info)

        return self.app(environ, custom_start_response)
