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
    """Normalize a header name for case-insensitive comparison."""
    return s.strip().lower()


class SecureWSGIMiddleware:
    """
    Add Secure's configured HTTP security headers to a WSGI application.

    This middleware wraps a WSGI app and injects headers by wrapping the
    WSGI ``start_response`` callable. This is a protocol-level integration:
    it does not require a framework-specific response object.

    Behavior
    --------
    - Overwrites existing headers by default (case-insensitive) to avoid duplicate
      single-value headers (e.g., ``X-Frame-Options``).
    - For header names in ``multi_ok`` (default: :data:`secure.secure.MULTI_OK`),
      existing values are preserved and Secure's values are appended.

    Notes
    -----
    - Many frameworks (e.g., Flask) also expose higher-level hooks (after_request).
      This middleware is useful when you want a server-/deployment-level wrapper
      or a framework-agnostic approach.
    - Django is typically integrated via Django's middleware interface (response
      objects). This WSGI middleware is still valid when running Django under WSGI.

    Examples
    --------
    Flask (recommended hook is ``app.wsgi_app``):

    >>> from flask import Flask
    >>> from secure.middleware import SecureWSGIMiddleware
    >>> app = Flask(__name__)
    >>> app.wsgi_app = SecureWSGIMiddleware(app.wsgi_app)

    Pass a custom Secure instance (e.g., custom CSP):

    >>> from secure import Secure
    >>> secure = Secure.with_default_headers()
    >>> app.wsgi_app = SecureWSGIMiddleware(app.wsgi_app, secure=secure)
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
        app:
            The WSGI application to wrap.
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
        self.multi_ok = frozenset(_norm_str(h) for h in provided)

    def __call__(self, environ: WSGIEnviron, start_response: StartResponse) -> Iterable[bytes]:
        """
        Invoke the wrapped WSGI app, injecting configured security headers.

        This method wraps ``start_response`` so it can modify the outgoing header
        list immediately before the server sends them to the client.
        """

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
