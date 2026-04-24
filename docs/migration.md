# v2 Migration Notes

The first stable v2 release is `2.0.1`. Skip `2.0.0`.

If your application already uses `Secure` to set headers on responses, the upgrade should be straightforward. Most changes are about preset names, package-level imports, and clearer sync versus async integration.

## What stayed the same

- `Secure` is still the main entry point.
- Header builders such as `ContentSecurityPolicy` and `StrictTransportSecurity` are still the way to define custom policies.
- `set_headers(response)` is still the sync path for supported response objects.

## What changed

- Import from the package root: `from secure import Secure, Preset, ContentSecurityPolicy`.
- `Secure.with_default_headers()` now means `Secure.from_preset(Preset.BALANCED)`.
- Presets are now `Preset.BALANCED`, `Preset.BASIC`, and `Preset.STRICT`.
- `Preset.BALANCED` is the recommended default. `Preset.BASIC` is the compatibility-oriented option. `Preset.STRICT` is not the default.
- `set_headers_async(response)` is available for async integrations and async response setters.
- `secure.middleware` exposes `SecureWSGIMiddleware` and `SecureASGIMiddleware` for app-wide integration.

## What might break

- `Preset.MODERN` is gone. Replace it with `Preset.BALANCED` for the new default or `Preset.STRICT` if you specifically want a tighter profile.
- The default profile is now `BALANCED`, which intentionally omits `Cache-Control` and the legacy compatibility headers from `BASIC`.
- `Preset.STRICT` no longer enables HSTS preload by default. Add `.preload()` yourself if you rely on that behavior.
- `set_headers()` is sync-only. If your response object only supports async setters, switch to `await set_headers_async(response)`.
- If you set the `Server` header, disable framework or server defaults such as Uvicorn's `Server: uvicorn` to avoid duplicates.

## Minimal upgrade path

If you previously relied on the default helpers, this is usually enough:

```python
from secure import Secure

secure_headers = Secure.with_default_headers()
secure_headers.set_headers(response)
```

If you want the new preset API explicitly:

```python
from secure import Preset, Secure

secure_headers = Secure.from_preset(Preset.BALANCED)
```

If your old code expected stricter defaults, review `Preset.STRICT` before switching. The main thing to check is CSP behavior, caching, framing, and HSTS preload.
