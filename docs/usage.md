# Usage Guide

`Secure` is the main entry point for applying HTTP security headers. Start with a preset, customize the builders you need, then apply the result to sync or async response objects.

## Quick start

```python
from secure import Secure

secure_headers = Secure.with_default_headers()

def add_security_headers(response):
    secure_headers.set_headers(response)
    return response
```

For async frameworks or async response objects:

```python
async def add_security_headers(response):
    await secure_headers.set_headers_async(response)
    return response
```

`set_headers` works with synchronous `set_header(...)` methods or mutable `headers` mappings. `set_headers_async` supports the same contracts and also awaits async setters when the response object requires them.

## Presets

`secure` ships with three presets:

- `Preset.BALANCED` is the recommended default and matches `Secure.with_default_headers()`.
- `Preset.BASIC` is a compatibility-oriented profile with a few legacy and interoperability headers.
- `Preset.STRICT` is a tighter profile for deployments that can tolerate stricter CSP, framing, and caching rules.

### `Preset.BALANCED`

```python
from secure import Preset, Secure

secure_headers = Secure.from_preset(Preset.BALANCED)
```

Representative headers:

```http
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
Content-Security-Policy: default-src 'self'; base-uri 'self'; font-src 'self' https: data:; form-action 'self'; frame-ancestors 'self'; img-src 'self' data:; object-src 'none'; script-src 'self'; script-src-attr 'none'; style-src 'self' https: 'unsafe-inline'; upgrade-insecure-requests
Strict-Transport-Security: max-age=31536000; includeSubDomains
Permissions-Policy: geolocation=(), microphone=(), camera=()
Referrer-Policy: strict-origin-when-cross-origin
Server:
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
```

Balanced intentionally omits `Cache-Control` and the compatibility headers that `Preset.BASIC` adds.

### `Preset.BASIC`

```python
from secure import Preset, Secure

secure_headers = Secure.from_preset(Preset.BASIC)
```

In addition to the Balanced baseline, `Preset.BASIC` adds:

```http
Referrer-Policy: no-referrer
X-Permitted-Cross-Domain-Policies: none
X-DNS-Prefetch-Control: off
Origin-Agent-Cluster: ?1
X-Download-Options: noopen
X-XSS-Protection: 0
```

### `Preset.STRICT`

```python
from secure import Preset, Secure

secure_headers = Secure.from_preset(Preset.STRICT)
```

Representative headers:

```http
Cache-Control: no-store, max-age=0
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Opener-Policy: same-origin
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'
Strict-Transport-Security: max-age=63072000; includeSubDomains
Permissions-Policy: geolocation=(), microphone=(), camera=()
Referrer-Policy: no-referrer
Server:
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

`Preset.STRICT` does not enable HSTS preload by default. Opt in separately with `StrictTransportSecurity().preload()` once your deployment is ready.

## Customizing headers

Use the package-level builder exports to tailor individual headers while keeping `Secure` as the facade:

```python
from secure import ContentSecurityPolicy, Secure

secure_headers = Secure(
    csp=ContentSecurityPolicy()
    .default_src("'self'")
    .img_src("'self'", "https://trusted-images.example")
)
```

You can also start from a preset and replace specific builders:

```python
from secure import Preset, Secure, StrictTransportSecurity

secure_headers = Secure.from_preset(Preset.BALANCED)
secure_headers.headers_list = [
    header
    for header in secure_headers.headers_list
    if header.header_name != "Strict-Transport-Security"
]
secure_headers.headers_list.append(
    StrictTransportSecurity().max_age(63072000).include_subdomains()
)
```

## Validation pipeline

Most applications can stop at `Secure(...).set_headers(...)`. If you want stricter checks before emission, run the optional pipeline helpers:

```python
import logging

from secure import COMMA_JOIN_OK, DEFAULT_ALLOWED_HEADERS, MULTI_OK, Secure

logger = logging.getLogger("secure")

secure_headers = (
    Secure.with_default_headers()
    .allowlist_headers(
        allowed=DEFAULT_ALLOWED_HEADERS,
        allow_extra=["X-My-App-Header"],
        on_unexpected="warn",
        logger=logger,
    )
    .deduplicate_headers(
        action="raise",
        comma_join_ok=COMMA_JOIN_OK,
        multi_ok=MULTI_OK,
        logger=logger,
    )
    .validate_and_normalize_headers(on_invalid="drop", logger=logger)
)
```

After `validate_and_normalize_headers()`, the normalized single-valued mapping is available via `secure_headers.headers`. If you need ordered or multi-valued output, use `secure_headers.header_items()` instead.

## Middleware

`secure.middleware` exposes `SecureWSGIMiddleware` and `SecureASGIMiddleware` for framework-wide integration.

WSGI example:

```python
from flask import Flask
from secure import Secure
from secure.middleware import SecureWSGIMiddleware

app = Flask(__name__)
secure_headers = Secure.with_default_headers()
app.wsgi_app = SecureWSGIMiddleware(app.wsgi_app, secure=secure_headers)
```

ASGI example:

```python
from fastapi import FastAPI
from secure import Secure
from secure.middleware import SecureASGIMiddleware

app = FastAPI()
secure_headers = Secure.with_default_headers()
app.add_middleware(SecureASGIMiddleware, secure=secure_headers)
```

See [Framework Integration](./frameworks.md) for more examples.
