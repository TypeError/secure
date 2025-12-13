# v2.0.0 Migration Notes

## Package and import changes

- The package is now published as `secure` (not `secure.py`). Import the public API via `import secure` or `from secure import Secure, Preset, ContentSecurityPolicy`, and the builder classes are re-exported at the package level for convenience.
- `Secure.with_default_headers()` now equals `Secure.from_preset(Preset.BASIC)`, so you can keep calling the same helpers while taking advantage of the new preset enum.

```python
from secure import Secure, StrictTransportSecurity

secure_headers = Secure(
    hsts=StrictTransportSecurity().max_age(63072000)
)
```

## Presets and defaults

- There are three built-in presets now: `Preset.BASIC` (the default set that `with_default_headers()` uses), `Preset.MODERN` (a slimmer set of widely-supported headers), and `Preset.STRICT` (the hardened profile).
- The `BASIC` preset now emits `Cross-Origin-Resource-Policy`, `X-Permitted-Cross-Domain-Policies`, `X-DNS-Prefetch-Control`, `Origin-Agent-Cluster`, `X-Download-Options`, and `X-XSS-Protection` in addition to the headers you already know. If you relied on the older shorthand, take a moment to verify whether these additionals need adjustment for your deployment.

## Header pipeline helpers

- Use `secure_headers.allowlist_headers(...).deduplicate_headers(...).validate_and_normalize_headers(...)` to enforce a clean, single-valued header mapping before calling `set_headers`/`set_headers_async`. This pipeline combines allowlists, duplicate resolution, and validation with sanitized output that you can inspect via `secure_headers.headers` or emit manually via `secure_headers.header_items()`.
- `Secure.header_items()` keeps the original ordering and multi-valued headers, so you can still emit headers like CSP multiple times when necessary.

## Setters and async support

- `set_headers` now raises clear errors if the response object only exposes async setters, while `set_headers_async` transparently awaits either sync or async `set_header`/`headers.__setitem__` calls. If you previously manipulated headers manually, switching to these helpers gives you timeouts, logging, and validation hooks.

## Security gotchas

- The `Server` header defaults to an empty string, so disable framework defaults (e.g., `uvicorn --no-server-header`) if you apply a custom value to avoid duplicate headers.
- `Preset.BASIC` also includes legacy/compatibility defaults such as `X-Permitted-Cross-Domain-Policies: none` and `X-XSS-Protection: 0`. If you need to omit those, start from `Preset.MODERN` or build a `Secure` instance manually.

Refer back to the [README](../README.md) and the individual header docs for exact builder methods when adapting your existing configuration to v2.0.0.
