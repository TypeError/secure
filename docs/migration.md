# v2.0.0 Migration Notes

## Package and import changes

- The package is published as `secure` (not `secure.py`). Import the public API via `from secure import Secure, Preset, ContentSecurityPolicy`, and prefer package-level re-exports in application code and examples.
- `Secure.with_default_headers()` now equals `Secure.from_preset(Preset.BALANCED)`, so you can keep calling the same helpers while taking advantage of the new preset enum. Balanced is the recommended default and intentionally omits `Cache-Control`; add it explicitly when your deployment depends on caching directives.

```python
from secure import Secure, StrictTransportSecurity

secure_headers = Secure(
    hsts=StrictTransportSecurity().max_age(63072000)
)
```

## Presets and defaults

- There are three built-in presets now: `Preset.BALANCED` (the recommended default that `with_default_headers()` uses), `Preset.BASIC` (the compatibility-oriented profile), and `Preset.STRICT` (the hardened profile). `Preset.MODERN` has been removed in favor of this clearer contract.
- The `BASIC` preset emits additional compatibility headers such as `X-Permitted-Cross-Domain-Policies`, `X-DNS-Prefetch-Control`, `Origin-Agent-Cluster`, `X-Download-Options`, and `X-XSS-Protection`. Use `Preset.BALANCED` when you want a leaner baseline and add those headers manually only when you still depend on them.
- `Preset.STRICT` continues to enable COEP, CSP base/frame restrictions, and a strict permissions policy, but it no longer preloads HSTS by default; add `.preload()` yourself when you are ready to opt into the preload list.

## Header pipeline helpers

- Use `secure_headers.allowlist_headers(...).deduplicate_headers(...).validate_and_normalize_headers(...)` to enforce a clean, single-valued header mapping before calling `set_headers`/`set_headers_async`. This pipeline combines allowlists, duplicate resolution, and validation with sanitized output that you can inspect via `secure_headers.headers` or emit manually via `secure_headers.header_items()`.
- `Secure.header_items()` keeps the original ordering and multi-valued headers, so you can still emit headers like CSP multiple times when necessary.

## Setters and async support

- `set_headers` raises a clear error if the response object only exposes async setters, while `set_headers_async` transparently awaits either sync or async `set_header`/`headers.__setitem__` calls.
- `secure.middleware` provides the framework-agnostic `SecureWSGIMiddleware` and `SecureASGIMiddleware` entry points for application-wide integration.

## Security gotchas

- The `Server` header defaults to an empty string, so disable framework defaults (e.g., `uvicorn --no-server-header`) if you apply a custom value to avoid duplicate headers.
- `Preset.BASIC` includes legacy/compatibility defaults such as `X-Permitted-Cross-Domain-Policies: none` and `X-XSS-Protection: 0`. Use `Preset.BALANCED` (or roll your own `Secure` instance) when you want a leaner header set.

Refer back to the [README](../README.md) and the individual header docs for exact builder methods when adapting your existing configuration to v2.0.0.
