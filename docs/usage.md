# Usage

`Secure` is the public entry point. Configure it once, then reuse it wherever your framework gives you access to the response.

## Start with a preset

`Secure.with_default_headers()` is the recommended starting point. It matches `Preset.BALANCED`.

```python
from secure import Secure

secure_headers = Secure.with_default_headers()
```

You can also choose a preset explicitly:

```python
from secure import Preset, Secure

balanced = Secure.from_preset(Preset.BALANCED)
basic = Secure.from_preset(Preset.BASIC)
strict = Secure.from_preset(Preset.STRICT)
```

- `Preset.BALANCED`: recommended default for most applications.
- `Preset.BASIC`: Helmet-style compatibility.
- `Preset.STRICT`: tighter CSP, cross-origin isolation headers, disabled caching, and stricter framing rules.

## Apply headers to a response

Use `set_headers()` for synchronous response objects:

```python
from secure import Secure

secure_headers = Secure.with_default_headers()


def add_security_headers(response):
    secure_headers.set_headers(response)
    return response
```

Use `set_headers_async()` in async code or when the response object may expose async setters:

```python
from secure import Secure

secure_headers = Secure.with_default_headers()


async def add_security_headers(response):
    await secure_headers.set_headers_async(response)
    return response
```

`Secure` works with response objects that provide either:

- `response.set_header(name, value)`
- `response.headers[name] = value`

If your framework uses a different contract, emit headers manually with `header_items()`.

## App-wide middleware

If you want application-wide coverage, use the middleware classes from `secure.middleware`.

- Both `SecureASGIMiddleware` and `SecureWSGIMiddleware` overwrite configured header names by default.
- Use `multi_ok` when you intentionally want controlled duplication instead of overwrite.
- `SecureASGIMiddleware` only modifies HTTP responses. WebSocket and other non-HTTP scopes pass through unchanged.

```python
from secure import Secure
from secure.middleware import SecureASGIMiddleware

secure_headers = Secure.with_default_headers()
secured_app = SecureASGIMiddleware(app, secure=secure_headers)
```

If you need multiple `Content-Security-Policy` headers, keep those names in `multi_ok` and emit the policy values you intend to preserve.

## Build an explicit configuration

Presets are the shortest path. When you need more control, pass builder objects into `Secure`.

```python
from secure import (
    ContentSecurityPolicy,
    PermissionsPolicy,
    Secure,
    StrictTransportSecurity,
)

secure_headers = Secure(
    csp=(
        ContentSecurityPolicy()
        .default_src("'self'")
        .img_src("'self'", "https://images.example.com")
        .script_src("'self'", "https://cdn.example.com")
    ),
    hsts=StrictTransportSecurity().max_age(63072000).include_subdomains(),
    permissions=PermissionsPolicy().geolocation().microphone().camera(),
)
```

This keeps the configuration readable while avoiding hand-built header strings.
Stricter CSP changes should always be tested against the real application before rollout.

## Optional validation pipeline

Most applications do not need this. It is useful when headers are being merged, extended, or generated dynamically and you want validation before emission.

```python
from secure import Secure

secure_headers = (
    Secure.with_default_headers()
    .allowlist_headers()
    .deduplicate_headers()
    .validate_and_normalize_headers()
)
```

After `validate_and_normalize_headers()`, the normalized mapping is available via `secure_headers.headers`.

## Manual emission

Use `header_items()` when a framework does not expose a supported response interface or when you need ordered header pairs.

```python
from secure import Secure

secure_headers = Secure.with_default_headers()

for name, value in secure_headers.header_items():
    response.headers[name] = value
```

For framework-specific examples, see [Framework Integration](./frameworks.md).
