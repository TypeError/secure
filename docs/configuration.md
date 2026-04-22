# Configuration Guide

This guide covers the parts of `secure` you are most likely to customize after the quick start. Keep `Secure` as the public entry point and pass it the builders you need.

## Default configuration

`Secure.with_default_headers()` uses `Preset.BALANCED`, which provides a modern baseline while keeping the header set lean:

- **Cross-Origin-Opener-Policy:** `same-origin`
- **Cross-Origin-Resource-Policy:** `same-origin`
- **Content-Security-Policy:** `default-src 'self'; base-uri 'self'; font-src 'self' https: data:; form-action 'self'; frame-ancestors 'self'; img-src 'self' data:; object-src 'none'; script-src 'self'; script-src-attr 'none'; style-src 'self' https: 'unsafe-inline'; upgrade-insecure-requests`
- **Strict-Transport-Security:** `max-age=31536000; includeSubDomains`
- **Permissions-Policy:** `geolocation=(), microphone=(), camera=()`
- **Referrer-Policy:** `strict-origin-when-cross-origin`
- **Server:** empty string
- **X-Content-Type-Options:** `nosniff`
- **X-Frame-Options:** `SAMEORIGIN`

Balanced intentionally skips `Cache-Control` and the compatibility headers (`X-Permitted-Cross-Domain-Policies`, `X-DNS-Prefetch-Control`, `Origin-Agent-Cluster`, `X-Download-Options`, `X-XSS-Protection`). Add them explicitly when your deployment still depends on them.

## Customizing individual builders

All public header builders are re-exported from `secure`, so most applications can stay on the package-level API.

### `X-Frame-Options`

If you want to allow framing only from the same origin, use:

```python
from secure import Secure, XFrameOptions

secure_headers = Secure(xfo=XFrameOptions().sameorigin())
```

This protects against clickjacking while still allowing same-origin embedding.

### `Strict-Transport-Security`

To enforce HTTPS for all subdomains and opt into preload when you are ready, configure HSTS explicitly:

```python
from secure import Secure, StrictTransportSecurity

secure_headers = Secure(
    hsts=StrictTransportSecurity().max_age(63072000).include_subdomains().preload()
)
```

This enforces HTTPS for two years, applies the rule to subdomains, and opts into the preload list.

## Adding custom headers

Use `CustomHeader` for application-specific response headers that do not have a dedicated builder:

```python
from secure import CustomHeader, Secure

custom_header = CustomHeader("X-Custom-Header", "CustomValue")
secure_headers = Secure(custom=[custom_header])
```

## Starting from a preset

Every `Secure` instance exposes its configured builders through `headers_list`, so you can replace or extend a preset after construction:

```python
from secure import Preset, Secure, StrictTransportSecurity

secure_headers = Secure.from_preset(Preset.BASIC)

secure_headers.headers_list = [
    header
    for header in secure_headers.headers_list
    if header.header_name != "Strict-Transport-Security"
]
secure_headers.headers_list.append(
    StrictTransportSecurity().max_age(63072000).include_subdomains()
)
```

This replaces the preset HSTS builder while leaving the rest of the preset untouched.

## Validation and normalization

If you need stronger guarantees before emission, `Secure` also exposes optional pipeline helpers:

- `allowlist_headers(...)` filters or rejects unexpected header names in the current `headers_list`.
- `deduplicate_headers(...)` resolves duplicate header names in `headers_list` before you build a single-valued mapping.
- `validate_and_normalize_headers(...)` validates and normalizes the current `header_items()`, then caches the single-valued mapping used by `.headers`, `set_headers()`, and `set_headers_async()`.

If you intentionally emit duplicate headers such as multiple `Content-Security-Policy` values, use `header_items()` instead of `.headers`.

For per-header builder details, see the docs under [headers](./headers).
