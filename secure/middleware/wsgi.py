from __future__ import annotations

from collections.abc import Iterable
from types import TracebackType
from typing import Any, TypeAlias

from ..secure import MULTI_OK, Secure

# ---------------------------------------------------------------------------
# WSGI typing aliases
# ---------------------------------------------------------------------------

HeaderList: TypeAlias = list[tuple[str, str]]

# PEP 3333: exc_info may be a 3-tuple, or None. In practice (and in wsgiref types),
# it's also allowed to be (None, None, None) as a sentinel.
ExcInfo: TypeAlias = tuple[type[BaseException], BaseException, TracebackType] | tuple[None, None, None] | None

# PEP 3333: start_response(status, headers[, exc_info]) -> write(body_bytes)
WriteCallable: TypeAlias = Any  # write callable exists, but is rarely used in modern apps

try:
    # Python 3.11+ provides useful WSGI types in the stdlib.
    from wsgiref.types import StartResponse, WSGIApplication, WSGIEnvironment
except Exception:  # pragma: no cover
    from collections.abc import Callable

    WSGIEnvironment = dict[str, Any]
    StartResponse = Callable[[str, HeaderList, ExcInfo], WriteCallable]
    WSGIApplication = Callable[[WSGIEnvironment, StartResponse], Iterable[bytes]]

WSGIApp: TypeAlias = WSGIApplication

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _normalize_header_name(name: str) -> str:
    """Normalize a header field-name for case-insensitive comparison."""
    return name.strip().lower()


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------


class SecureWSGIMiddleware:
    """
    Apply Secure's configured HTTP security headers to a WSGI application.

    This middleware wraps a WSGI app and injects headers by wrapping the WSGI
    ``start_response`` callable. It does not require a framework-specific
    response object.

    Parameters
    ----------
    app:
        The WSGI application to wrap.
    secure:
        A configured :class:`~secure.Secure` instance. If omitted, uses
        :meth:`~secure.Secure.with_default_headers`.
    multi_ok:
        Header names allowed to appear multiple times in a response. For these,
        Secure's value is appended instead of overwriting. Defaults to
        :data:`secure.secure.MULTI_OK`.

    Behavior
    --------
    - Overwrites existing headers by default (case-insensitive) to avoid duplicates
      for single-value headers (e.g., ``X-Frame-Options``).
    - For header names in ``multi_ok``, existing values are preserved and
      Secure's value is appended.

    Notes
    -----
    WSGI technically allows calling ``start_response`` multiple times in error
    scenarios (via ``exc_info``). This middleware preserves that behavior by
    forwarding ``exc_info`` unchanged.
    """

    def __init__(
        self,
        app: WSGIApp,
        *,
        secure: Secure | None = None,
        multi_ok: Iterable[str] | None = None,
    ) -> None:
        self.app = app
        self.secure = secure or Secure.with_default_headers()

        provided = MULTI_OK if multi_ok is None else multi_ok
        self._multi_ok: frozenset[str] = frozenset(_normalize_header_name(h) for h in provided)

    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]:
        """
        Invoke the wrapped WSGI app, injecting configured security headers.

        Parameters
        ----------
        environ:
            The WSGI environment for the request.
        start_response:
            The WSGI ``start_response`` callable provided by the server.

        Returns
        -------
        Iterable[bytes]
            The response body iterable returned by the wrapped application.
        """

        def custom_start_response(
            status: str,
            headers: HeaderList,
            exc_info: ExcInfo = None,
        ) -> WriteCallable:
            out: HeaderList = list(headers)

            # Track existing occurrences by normalized key.
            positions: dict[str, list[int]] = {}
            for i, (k, _v) in enumerate(out):
                positions.setdefault(_normalize_header_name(k), []).append(i)

            # Apply Secure headers.
            for k, v in self.secure.headers.items():
                nk = _normalize_header_name(k)

                if nk in self._multi_ok:
                    out.append((k, v))
                    continue

                if nk in positions:
                    for idx in reversed(positions[nk]):
                        out.pop(idx)
                    positions.pop(nk, None)

                out.append((k, v))
                positions[nk] = [len(out) - 1]

            return start_response(status, out, exc_info)

        return self.app(environ, custom_start_response)
