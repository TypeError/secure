# X-DNS-Prefetch-Control

## What it does

`X-DNS-Prefetch-Control` controls **DNS prefetching**, where browsers may proactively resolve domain names for links and referenced subresources (images, CSS, JS, etc.) in the background to reduce perceived latency.

## Minimal example

```python
from secure import Secure, XDnsPrefetchControl

secure_headers = Secure(
    xdfc=XDnsPrefetchControl().off()
)
```

## Resulting header

```http
X-DNS-Prefetch-Control: off
```

## Practical note

When this header is absent, supporting browsers commonly behave as if DNS prefetching is on. Add the header only when you want to state a clear preference.

## Default behavior

If you create `XDnsPrefetchControl()` and do not set a directive, it returns the library default value:

- **Default header value:** `off`

> Note (MDN behavior): In browsers that support DNS prefetching, if this header is **not present**, the effective behavior is typically **`on`**. This library’s default is **privacy-first** when you choose to emit the header.

## Using with `Secure`

If you don’t configure anything, the default value is emitted.
`Preset.BASIC` includes `X-DNS-Prefetch-Control: off`; `Preset.BALANCED` and `Preset.STRICT` leave it out unless you add it explicitly.

## Common recipes

### 1) Disable DNS prefetching (recommended when you don’t control outbound links)

```python
from secure import XDnsPrefetchControl

xdfc = XDnsPrefetchControl()  # default: off
print(xdfc.header_name)   # X-DNS-Prefetch-Control
print(xdfc.header_value)  # off
```

### 2) Enable DNS prefetching

```python
xdfc = XDnsPrefetchControl().on()
print(xdfc.header_value)  # on
```

### 3) Backwards-compatible builder names

If you prefer the older API vocabulary:

```python
xdfc = XDnsPrefetchControl().allow()   # == .on()
xdfc = XDnsPrefetchControl().disable() # == .off()
```

## Builder API

### Canonical directives

- `.on()`
  Enables DNS prefetching (commonly the effective behavior when the header is absent in supporting browsers).

- `.off()`
  Disables DNS prefetching (useful to reduce information leakage to third-party domains).

### Backwards-compatible aliases

- `.allow()` → same as `.on()`
- `.disable()` → same as `.off()`

## Escape hatches

### `.value("...")` / `.set("...")`

Set an explicit header value (replaces the current value):

```python
xdfc = XDnsPrefetchControl().value("off")
print(xdfc.header_value)  # off
```

If you pass `ON` / `Off` (any casing), the builder normalizes to `on` / `off` for stable output.

### `.custom("token")`

Set a **non-standard / non-MDN** token (escape hatch):

```python
xdfc = XDnsPrefetchControl().custom("off")
print(xdfc.header_value)  # off
```

(For this header, non-`on`/`off` values are unusual, but the escape hatch exists for consistency across the library.)

### `.clear()`

Reset to the library default:

```python
xdfc = XDnsPrefetchControl().on().clear()
print(xdfc.header_value)  # off
```

## Deterministic output & overwrites

- Output is always a **single token** (`on` or `off`) when using `.on()` / `.off()` (stable and deterministic).
- Setting the value multiple times overwrites the previous value (last call wins).
- `.set(...)`, `.value(...)`, and `.custom(...)` reject CR/LF; `Secure.validate_and_normalize_headers(...)` performs the broader normalization pass.

## Compatibility notes

- This header is **non-standard**.
- Browser behavior differs across engines and versions; treat this as a best-effort control rather than a guaranteed security boundary.

## Attribution

This library implements security recommendations and behavior described by:

- [MDN Web Docs: X-DNS-Prefetch-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-DNS-Prefetch-Control) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project: X-DNS-Prefetch-Control](https://owasp.org/www-project-secure-headers/#x-dns-prefetch-control) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
