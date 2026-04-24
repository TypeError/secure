# secure

Add modern security headers to any Python web app in minutes.

Works with FastAPI, Flask, Django, Starlette, and Shiny for Python. No dependencies.

<p align="center">
  <img src="https://typeerror.com/assets/secure-hex.png" alt="secure hex" width="200">
</p>

[![PyPI Version](https://img.shields.io/pypi/v/secure.svg)](https://pypi.org/project/secure/) [![Python Versions](https://img.shields.io/pypi/pyversions/secure.svg)](https://pypi.org/project/secure/) [![License](https://img.shields.io/pypi/l/secure.svg)](https://github.com/TypeError/secure/blob/main/LICENSE)

Quick links: [Quick start](#quick-start) · [Headers](#what-headers-are-applied-by-default) · [Middleware](#middleware)

---

## Introduction

Security headers are one of the simplest ways to improve a web application's security, but they are often applied inconsistently across frameworks and deployments.

`secure` provides a single, modern, well-typed API for configuring and applying HTTP security headers in Python.

- Good defaults that are safe to adopt
- A small, explicit API
- Sync and async support
- Framework-agnostic design

```python
import secure
```

---

## Why use `secure`

- Apply essential security headers in a few lines
- Share one configuration across multiple frameworks
- Start with presets, then customize
- Keep header logic out of your handlers
- Use one library for FastAPI, Starlette, Flask, Django, Shiny for Python, and more

If you want a strong security baseline without adding a large dependency, `secure` is designed for that use case.

---

## Installation

```bash
uv add secure
# or
pip install secure
```

---

## Quick start

```python
import secure

secure_headers = secure.Secure.with_default_headers()

# Apply to any response object with headers support
secure_headers.set_headers(response)
# or
await secure_headers.set_headers_async(response)
```

`Secure.with_default_headers()` maps to `Preset.BALANCED`, the recommended default.

> Works with FastAPI, Flask, Django, Starlette, and Shiny for Python in minutes.

---

## What headers are applied by default

```http
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
Content-Security-Policy: default-src 'self'; base-uri 'self'; font-src 'self' https: data:; form-action 'self'; frame-ancestors 'self'; img-src 'self' data:; object-src 'none'; script-src 'self'; script-src-attr 'none'; style-src 'self' https: 'unsafe-inline'; upgrade-insecure-requests
Strict-Transport-Security: max-age=31536000; includeSubDomains
Permissions-Policy: geolocation=(), microphone=(), camera=()
Referrer-Policy: strict-origin-when-cross-origin
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
```

This baseline reflects modern browser guidance from MDN and OWASP. It reduces cross-origin risk, prevents MIME sniffing, and provides a conservative Content Security Policy you can extend.

The default CSP is designed to work for most applications while avoiding unsafe script execution. Interactive apps or third-party integrations may require additional CSP configuration depending on how scripts, styles, or external resources are used.

---

## Presets

```python
from secure import Preset, Secure

Secure.from_preset(Preset.BALANCED)
Secure.from_preset(Preset.BASIC)
Secure.from_preset(Preset.STRICT)
```

- **BALANCED**: recommended default
- **BASIC**: Helmet-style compatibility
- **STRICT**: tighter CSP and isolation

Start with BALANCED and move stricter only when needed.

---

## Middleware

`secure` provides both ASGI and WSGI middleware.

- Works with FastAPI, Starlette, Shiny, Flask, Django, and others
- Overwrites headers by default
- Allows controlled duplication via `multi_ok`

### ASGI example

```python
from fastapi import FastAPI
from secure import Secure
from secure.middleware import SecureASGIMiddleware

app = FastAPI()
secure_headers = Secure.with_default_headers()

app.add_middleware(SecureASGIMiddleware, secure=secure_headers)
```

### Django example

```python
from secure import Secure

class SecureHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.secure = Secure.with_default_headers()

    def __call__(self, request):
        response = self.get_response(request)
        self.secure.set_headers(response)
        return response
```

---

## Framework examples

### FastAPI

```python
app.add_middleware(SecureASGIMiddleware, secure=secure_headers)
```

### Flask

```python
@app.after_request
def add_security_headers(response):
    secure_headers.set_headers(response)
    return response
```

### Shiny for Python

```python
from shiny import App
from secure.middleware import SecureASGIMiddleware

app = SecureASGIMiddleware(App(), secure=secure_headers)
```

Interactive apps may require additional CSP configuration depending on how scripts, styles, or external resources are used.

---

## Policy builders

### Content Security Policy

```python
from secure.headers import ContentSecurityPolicy

csp = (
    ContentSecurityPolicy()
    .default_src("'self'")
    .script_src("'self'", "cdn.example.com")
)
```

### Permissions Policy

```python
from secure.headers import PermissionsPolicy

permissions = (
    PermissionsPolicy()
    .geolocation("'self'")
    .camera("'none'")
)
```

---

## Header pipeline and validation

Optional pipeline for stricter control:

```python
secure_headers = (
    Secure.with_default_headers()
    .allowlist_headers(...)
    .deduplicate_headers(...)
    .validate_and_normalize_headers(...)
)
```

Use this when you need strict validation, predictable output, or want to fail fast on unsafe headers.

---

## Supported frameworks

FastAPI, Starlette, Flask, Django, Shiny for Python, aiohttp, Sanic, Pyramid, Tornado, and more.

See the full [framework integration guides](https://github.com/TypeError/secure/tree/main/docs/frameworks.md).

---

## Requirements

- Python 3.10+
- No external dependencies

---

## Documentation

Read the full [documentation](https://github.com/TypeError/secure/tree/main/docs).

---

## Learn more

- [MDN HTTP Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)

---

## License

MIT License

---

## Contributing

Issues and pull requests are welcome.

---

## Acknowledgements

Built using guidance from MDN and OWASP secure headers recommendations.
