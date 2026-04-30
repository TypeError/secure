# secure

[![PyPI Version](https://img.shields.io/pypi/v/secure.svg)](https://pypi.org/project/secure/) [![Python Versions](https://img.shields.io/pypi/pyversions/secure.svg)](https://pypi.org/project/secure/) [![License](https://img.shields.io/pypi/l/secure.svg)](https://github.com/TypeError/secure/blob/main/LICENSE)

Define HTTP security headers once. Apply them consistently across Python web apps.

`secure` provides a small, dependency-free API for configuring modern security headers across common Python web frameworks through ASGI middleware, WSGI middleware, or framework response hooks.

Use it when you want to avoid copy-pasted header strings spread across handlers, hooks, and middleware.

<p align="center">
  <img src="https://typeerror.com/assets/secure-hex.png" alt="secure hex" width="200">
</p>

Quick links: [Quick start](#quick-start) · [Headers](#what-headers-are-applied-by-default) · [Middleware](#middleware)

---

## Why use `secure`

Setting headers manually is fine for one endpoint. It gets harder to review when values are copied across routes, response hooks, reverse-proxy settings, and different framework integrations.

`secure` helps you:

- Keep one `Secure` policy object instead of scattered header strings
- Apply the same policy through ASGI middleware, WSGI middleware, or response hooks
- Start with practical presets, then customize headers for your application
- Use builders for complex headers such as Content Security Policy and Permissions Policy
- Make duplicate handling, header overwrites, and validation explicit

The defaults are a reasonable starting point, not a substitute for application-specific review. Content Security Policy in particular should be adjusted for the scripts, styles, assets, and third-party services your app actually uses.

---

## Installation

```bash
uv add secure
# or
pip install secure
```

---

## Quick start

### FastAPI / ASGI middleware

Use middleware when you can attach `secure` once and cover the whole application.

```python
from fastapi import FastAPI
from secure import Secure
from secure.middleware import SecureASGIMiddleware

app = FastAPI()
secure_headers = Secure.with_default_headers()

app.add_middleware(SecureASGIMiddleware, secure=secure_headers)
```

### Response hooks and handlers

Use the same policy object in framework hooks, middleware callbacks, or handlers that expose a response object with headers support.

```python
from secure import Secure

secure_headers = Secure.with_default_headers()

secure_headers.set_headers(response)
# or
await secure_headers.set_headers_async(response)
```

`Secure.with_default_headers()` maps to `Preset.BALANCED`, a practical default designed to be customized.

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

This preset reflects modern browser guidance from MDN and OWASP. It reduces cross-origin risk, prevents MIME sniffing, and provides a conservative Content Security Policy you can extend.

The default CSP avoids unsafe script execution by default, but CSP is context-sensitive. Interactive apps, dashboards, CDNs, analytics, embedded content, or other third-party integrations may require additional configuration.

---

## Presets

```python
from secure import Preset, Secure

Secure.from_preset(Preset.BALANCED)
Secure.from_preset(Preset.BASIC)
Secure.from_preset(Preset.STRICT)
```

- **BALANCED**: practical default for many applications
- **BASIC**: Helmet-style compatibility
- **STRICT**: tighter CSP and isolation

Start with BALANCED, review the generated headers, and move stricter only when needed.

---

## Middleware

`secure` provides both ASGI and WSGI middleware.

- Overwrites headers by default
- Allows controlled duplication via `multi_ok`
- Only modifies HTTP responses in ASGI apps

### ASGI

```python
from secure import Secure
from secure.middleware import SecureASGIMiddleware

secure_headers = Secure.with_default_headers()
app = SecureASGIMiddleware(app, secure=secure_headers)
```

### WSGI

```python
from secure import Secure
from secure.middleware import SecureWSGIMiddleware

secure_headers = Secure.with_default_headers()
app = SecureWSGIMiddleware(app, secure=secure_headers)
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

## Framework integration examples

These examples show common integration paths. See the full [framework integration guide](https://github.com/TypeError/secure/tree/main/docs/frameworks.md) for additional frameworks and notes about first-class middleware versus minimal fallback examples.

### FastAPI

```python
from secure.middleware import SecureASGIMiddleware

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

Interactive apps often need CSP configuration for their script, style, and asset loading patterns.

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

Use the optional pipeline when you need stricter control:

```python
secure_headers = (
    Secure.with_default_headers()
    .allowlist_headers(...)
    .deduplicate_headers(...)
    .validate_and_normalize_headers(...)
)
```

This makes header allowlists, deduplication, normalization, and validation explicit instead of leaving those choices spread across application code.

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
