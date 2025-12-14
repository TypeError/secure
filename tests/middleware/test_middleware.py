import asyncio
from typing import Any, Literal, TypedDict, cast

from secure import CustomHeader, Secure
from secure.middleware import SecureASGIMiddleware, SecureWSGIMiddleware


def _find_header_values(headers: list[tuple[str, str]], name: str) -> list[str]:
    lc = name.lower()
    return [value for key, value in headers if key.lower() == lc]


class _CapturedWSGI(TypedDict):
    status: str
    headers: list[tuple[str, str]]
    exc_info: Any
    body: bytes


def _run_wsgi_with_middleware(middleware) -> _CapturedWSGI:
    captured: _CapturedWSGI = {
        "status": "",
        "headers": [],
        "exc_info": None,
        "body": b"",
    }

    def start_response(
        status: str,
        headers: list[tuple[str, str]],
        exc_info: Any = None,
    ):
        captured["status"] = status
        captured["headers"] = headers
        captured["exc_info"] = exc_info
        return lambda _: None

    body = list(middleware({}, start_response))
    captured["body"] = b"".join(body)
    return captured


def test_wsgi_overwrites_existing_header():
    secure_headers = Secure.with_default_headers()
    app_headers = [("X-Frame-Options", "DENY")]

    def app(environ, start_response):
        start_response("200 OK", app_headers)
        return [b"ok"]

    middleware = SecureWSGIMiddleware(app, secure=secure_headers)
    captured = _run_wsgi_with_middleware(middleware)

    xfo_values = _find_header_values(captured["headers"], "x-frame-options")
    assert xfo_values == [secure_headers.headers["X-Frame-Options"]]


def test_wsgi_multi_ok_appends_existing_header():
    secure_headers = Secure.with_default_headers()
    app_headers = [("Content-Security-Policy", "app-csp")]

    def app(environ, start_response):
        start_response("200 OK", app_headers)
        return [b"ok"]

    middleware = SecureWSGIMiddleware(app, secure=secure_headers)
    captured = _run_wsgi_with_middleware(middleware)

    csp_values = _find_header_values(captured["headers"], "content-security-policy")
    assert csp_values == ["app-csp", secure_headers.headers["Content-Security-Policy"]]


def test_wsgi_preserves_status_and_extra_headers():
    secure_headers = Secure.with_default_headers()
    app_headers = [("X-Custom", "keep")]

    def app(environ, start_response):
        start_response("200 OK", app_headers)
        return [b"ok"]

    middleware = SecureWSGIMiddleware(app, secure=secure_headers)
    captured = _run_wsgi_with_middleware(middleware)

    assert captured["status"] == "200 OK"
    assert _find_header_values(captured["headers"], "x-custom") == ["keep"]


def _headers_by_name_bytes(headers: list[tuple[bytes, bytes]], name: bytes) -> list[bytes]:
    lc = name.lower()
    return [value for key, value in headers if key.lower() == lc]


def _http_app(response_headers: list[tuple[bytes, bytes]]):
    async def app(scope, receive, send):
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": response_headers,
            }
        )
        await send({"type": "http.response.body", "body": b"", "more_body": False})

    return app


class _HTTPResponseStart(TypedDict):
    type: Literal["http.response.start"]
    status: int
    headers: list[tuple[bytes, bytes]]


async def _run_asgi(scope: dict[str, Any], app) -> list[dict[str, Any]]:
    messages: list[dict[str, Any]] = []

    async def send(message: dict[str, Any]):
        messages.append(message)

    async def receive() -> dict[str, Any]:
        return {"type": "http.request", "body": b"", "more_body": False}

    await app(scope, receive, send)
    return messages


def test_asgi_overwrites_numeric_headers():
    secure_headers = Secure.with_default_headers()
    default_xfo = secure_headers.headers["X-Frame-Options"].encode("latin-1")
    app = _http_app(
        [
            (b"x-frame-options", b"DENY"),
            (b"x-custom", b"keep"),
        ]
    )

    middleware = SecureASGIMiddleware(app, secure=secure_headers)
    messages = asyncio.run(_run_asgi({"type": "http"}, middleware))
    start = cast(
        "_HTTPResponseStart",
        next(m for m in messages if m["type"] == "http.response.start"),
    )
    headers = start["headers"]

    xfo_values = _headers_by_name_bytes(headers, b"x-frame-options")
    assert xfo_values == [default_xfo]
    assert _headers_by_name_bytes(headers, b"x-custom") == [b"keep"]


def test_asgi_multi_ok_appends_default_csp():
    secure_headers = Secure.with_default_headers()
    expected_csp = secure_headers.headers["Content-Security-Policy"].encode("latin-1")
    app = _http_app([(b"content-security-policy", b"app-csp")])

    middleware = SecureASGIMiddleware(app, secure=secure_headers)
    messages = asyncio.run(_run_asgi({"type": "http"}, middleware))
    start = cast(
        "_HTTPResponseStart",
        next(m for m in messages if m["type"] == "http.response.start"),
    )
    headers = start["headers"]

    csp_values = _headers_by_name_bytes(headers, b"content-security-policy")
    assert csp_values == [b"app-csp", expected_csp]


def test_asgi_ignores_non_http_scopes():
    async def websocket_app(scope, receive, send):
        await send({"type": "websocket.accept"})

    middleware = SecureASGIMiddleware(websocket_app)
    messages = asyncio.run(_run_asgi({"type": "websocket"}, middleware))

    assert messages == [{"type": "websocket.accept"}]


def test_asgi_multi_ok_custom_header():
    secure_headers = Secure(custom=[CustomHeader("X-Extra", "new")])
    app = _http_app([(b"x-extra", b"existing")])

    middleware = SecureASGIMiddleware(app, secure=secure_headers, multi_ok=["x-extra"])
    messages = asyncio.run(_run_asgi({"type": "http"}, middleware))
    start = cast(
        "_HTTPResponseStart",
        next(m for m in messages if m["type"] == "http.response.start"),
    )
    headers = start["headers"]

    extra_values = _headers_by_name_bytes(headers, b"x-extra")
    assert extra_values == [b"existing", b"new"]
