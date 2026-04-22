# Cross-Origin-Embedder-Policy (COEP)

## Purpose

The **`Cross-Origin-Embedder-Policy`** response header configures the current document’s policy for **loading and embedding cross-origin resources**.

At a high level, COEP lets you:

- keep the default behavior (`unsafe-none`),
- require explicit opt-in via **CORP** (`Cross-Origin-Resource-Policy`) and/or **CORS** (`require-corp`), or
- allow some cross-origin loading while **stripping credentials** (`credentialless`).

## Directive values

COEP is a **single-value** header (choose one):

| Value            | Meaning                                                                                                                                                                                                     |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `unsafe-none`    | Allows cross-origin resources **without** explicit permission via CORP or CORS. _(This is the browser default if the header is not sent.)_                                                                  |
| `require-corp`   | Blocks cross-origin resource loading unless the resource is permitted via **CORP** (for `no-cors` requests) or via **CORS** (for `cors` requests).                                                          |
| `credentialless` | Allows `no-cors` cross-origin resource loading **without** CORP opt-in, but sends requests **without credentials** (cookies omitted and ignored). For other request modes, behavior matches `require-corp`. |

## Library default vs browser default

- **Browser behavior when the header is absent:** `unsafe-none`.
- **This library’s builder default:** `require-corp` (a stricter, security-forward default).

If you want “no-op” behavior, you must explicitly choose it:

```python
from secure import CrossOriginEmbedderPolicy

coep = CrossOriginEmbedderPolicy().unsafe_none()
```

## Cross-origin isolation (COOP + COEP)

Some powerful browser features require your document to be **cross-origin isolated**. To enable this, you generally need:

- `Cross-Origin-Embedder-Policy: require-corp` **or** `credentialless`, and
- `Cross-Origin-Opener-Policy: same-origin`.

## Usage with `Secure`

```python
from secure import CrossOriginEmbedderPolicy, CrossOriginOpenerPolicy, Secure

secure_headers = Secure(
    coep=CrossOriginEmbedderPolicy().require_corp(),
    coop=CrossOriginOpenerPolicy().same_origin(),
)

# Inspect emitted headers:
print(secure_headers.header_items())
```
`Preset.STRICT` includes COEP by default; `Preset.BASIC` and `Preset.BALANCED` do not.

## Header builder API

```python
from secure import CrossOriginEmbedderPolicy

coep = (
    CrossOriginEmbedderPolicy()
    .credentialless()   # or .require_corp() / .unsafe_none()
)

print(coep.header_name)   # "Cross-Origin-Embedder-Policy"
print(coep.header_value)  # "credentialless"
```

### Methods

- `unsafe_none()` — set value to `unsafe-none`
- `require_corp()` — set value to `require-corp`
- `credentialless()` — set value to `credentialless`
- `set(value)` — escape hatch: set a custom value (string)
- `clear()` — reset to the library default (`require-corp`)

## Notes / gotchas

- `require-corp` can break embedding third-party resources unless they opt-in via CORP or are requested in `cors` mode.
- `credentialless` can be a pragmatic alternative for some `no-cors` resources, but it comes with the tradeoff of **no cookies/credentials**.

## Attribution

This library implements security recommendations and definitions from trusted sources:

- MDN Web Docs (CC-BY-SA 2.5): https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Embedder-Policy
- OWASP Secure Headers Project (CC-BY-SA 4.0): https://owasp.org/www-project-secure-headers/#cross-origin-embedder-policy
