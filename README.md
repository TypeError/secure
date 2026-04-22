# secure

HTTP security headers for Python web applications, centered on one object: `Secure`.

[![PyPI Version](https://img.shields.io/pypi/v/secure.svg)](https://pypi.org/project/secure/)
[![Python Versions](https://img.shields.io/pypi/pyversions/secure.svg)](https://pypi.org/project/secure/)
[![License](https://img.shields.io/pypi/l/secure.svg)](https://github.com/TypeError/secure/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/TypeError/secure.svg)](https://github.com/TypeError/secure/stargazers)

`secure` exists to keep header policy out of ad hoc view code. Instead of copying header strings into routes, middleware, and framework-specific hooks, you configure one `Secure` instance and apply it consistently.

Hand-written header code tends to drift. Headers get missed, defaults vary between apps, and sync or async framework details leak into otherwise simple code. `secure` gives you a small public API, opinionated presets, and typed builders when you need to go beyond the defaults.

## Install

`secure` requires Python 3.10+ and has no external dependencies.

```bash
uv add secure
```

```bash
pip install secure
```

## Quick start

Start with `Secure.with_default_headers()`. It uses `Preset.BALANCED`, the recommended default for most applications.

```python
from secure import Secure

class Response:
    def __init__(self):
        self.headers = {}

response = Response()
Secure.with_default_headers().set_headers(response)
```

`Secure` applies headers to response objects that expose either:

- `response.set_header(name, value)`
- `response.headers[name] = value`

The quick start uses the `response.headers[name] = value` form.

Use `set_headers()` for synchronous response objects. Use `set_headers_async()` in async code or when the response object may use async setters.

## Presets

Most applications should start with `BALANCED`.

```python
from secure import Preset, Secure

balanced = Secure.from_preset(Preset.BALANCED)
basic = Secure.from_preset(Preset.BASIC)
strict = Secure.from_preset(Preset.STRICT)
```

- `Preset.BALANCED`: recommended default. Modern baseline with CSP, HSTS, referrer policy, permissions policy, and common browser protections.
- `Preset.BASIC`: compatibility-oriented. Adds legacy and interoperability headers that some deployments still expect.
- `Preset.STRICT`: hardened profile. Tightens CSP, disables caching, and denies framing.

Choose `BALANCED` unless you have a specific reason to prefer `BASIC` or `STRICT`.

## Middleware

If your framework supports app-wide middleware, prefer that over setting headers one response at a time.

### WSGI

```python
from flask import Flask
from secure import Secure
from secure.middleware import SecureWSGIMiddleware

app = Flask(__name__)
secure_headers = Secure.with_default_headers()

app.wsgi_app = SecureWSGIMiddleware(app.wsgi_app, secure=secure_headers)
```

### ASGI

```python
from fastapi import FastAPI
from secure import Secure
from secure.middleware import SecureASGIMiddleware

app = FastAPI()
secure_headers = Secure.with_default_headers()

app.add_middleware(SecureASGIMiddleware, secure=secure_headers)
```

Use `SecureWSGIMiddleware` when you can wrap a WSGI app directly. Use `SecureASGIMiddleware` when you want app-wide coverage in an ASGI stack such as FastAPI, Starlette, or Shiny.

## Advanced usage

Most applications can stop at a preset. When you need to tune a specific header, keep `Secure` as the entry point and pass builder objects into it.

### Custom policy

```python
from secure import ContentSecurityPolicy, Secure, StrictTransportSecurity

secure_headers = Secure(
    csp=(
        ContentSecurityPolicy()
        .default_src("'self'")
        .img_src("'self'", "https://images.example.com")
        .script_src("'self'", "https://cdn.example.com")
    ),
    hsts=StrictTransportSecurity().max_age(63072000).include_subdomains(),
)
```

### Optional validation

The validation pipeline is optional. Use it when headers are being composed dynamically and you want stricter checks before emission.

```python
from secure import Secure

secure_headers = (
    Secure.with_default_headers()
    .allowlist_headers()
    .deduplicate_headers()
    .validate_and_normalize_headers()
)
```

If you need manual emission for an unsupported response contract, iterate over `secure_headers.header_items()`.

## Framework examples

See [docs/frameworks.md](./docs/frameworks.md) for the full matrix. The most common patterns are:

### FastAPI

```python
from fastapi import FastAPI
from secure import Secure
from secure.middleware import SecureASGIMiddleware

app = FastAPI()
secure_headers = Secure.with_default_headers()
app.add_middleware(SecureASGIMiddleware, secure=secure_headers)
```

### Flask

```python
from flask import Flask
from secure import Secure

app = Flask(__name__)
secure_headers = Secure.with_default_headers()


@app.after_request
def add_security_headers(response):
    secure_headers.set_headers(response)
    return response
```

### Starlette

```python
from secure import Secure
from secure.middleware import SecureASGIMiddleware
from starlette.applications import Starlette

app = Starlette()
secure_headers = Secure.with_default_headers()
app.add_middleware(SecureASGIMiddleware, secure=secure_headers)
```

## Links

- [Documentation index](./docs/README.md)
- [Installation](./docs/installation.md)
- [Usage](./docs/usage.md)
- [Framework integration](./docs/frameworks.md)
- [Migration notes](./docs/migration.md)
