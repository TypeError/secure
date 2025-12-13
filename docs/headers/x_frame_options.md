# X-Frame-Options

## What it does

`X-Frame-Options` is an HTTP **response header** that tells supporting browsers whether a page is allowed to render inside a `<frame>`, `<iframe>`, `<embed>`, or `<object>`. It is commonly used to reduce **clickjacking** risk by preventing (or restricting) framing.

> Prefer `Content-Security-Policy: frame-ancestors ...` for modern, more flexible control. `X-Frame-Options` is kept for compatibility with older clients and simpler deployments.

**Default header value:** `SAMEORIGIN`

## Important notes

- **CSP is the modern replacement:** For comprehensive framing control, use CSP `frame-ancestors` (recommended).
- **`<meta http-equiv="X-Frame-Options" ...>` does nothing:** Browsers enforce `X-Frame-Options` only when it is sent as an HTTP response header.

## Directives

### `DENY`

The page **cannot** be displayed in a frame, regardless of what site is attempting to frame it (including the same site).

### `SAMEORIGIN`

The page can be displayed only if **all ancestor frames** have the **same origin** as the page itself.

### `ALLOW-FROM <origin>` (obsolete)

This directive is **obsolete**. Modern browsers that encounter `ALLOW-FROM` may **ignore the header completely**. Use CSP `frame-ancestors` instead.

## Using this library

### Minimal usage

```python
from secure import Secure
from secure.headers import XFrameOptions

secure = Secure(xfo=XFrameOptions().sameorigin())
```

### Choose a directive

```python
from secure.headers import XFrameOptions

xfo = XFrameOptions().deny()
print(xfo.header_name)   # 'X-Frame-Options'
print(xfo.header_value)  # 'DENY'
```

### Escape hatches

If you already have a fully-formed value, set it directly:

```python
from secure.headers import XFrameOptions

xfo = XFrameOptions().value("SAMEORIGIN")
# Aliases (for compatibility / readability):
xfo = XFrameOptions().set("SAMEORIGIN")
xfo = XFrameOptions().custom("SAMEORIGIN")
```

Reset to the library default:

```python
xfo = XFrameOptions().deny().clear()
print(xfo.header_value)  # 'SAMEORIGIN'
```

### Obsolete directive (not recommended)

```python
from secure.headers import XFrameOptions

# Warning: obsolete; prefer CSP frame-ancestors
xfo = XFrameOptions().allow_from("https://example.com")
```

## How it fits with presets

The built-in presets include `X-Frame-Options` by default:

- `Preset.BASIC` / `Preset.MODERN`: `SAMEORIGIN`
- `Preset.STRICT`: `DENY`

If you want full modern control, keep CSP `frame-ancestors` and treat `X-Frame-Options` as a compatibility layer.

## Resources

- MDN: X-Frame-Options (Reference) — [https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options)
- MDN: Clickjacking — [https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/Clickjacking](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/Clickjacking)
- OWASP Secure Headers Project: X-Frame-Options — [https://owasp.org/www-project-secure-headers/#x-frame-options](https://owasp.org/www-project-secure-headers/#x-frame-options)

## Attribution

This library implements security recommendations from trusted sources:

- MDN Web Docs (CC-BY-SA 2.5): [https://creativecommons.org/licenses/by-sa/2.5/](https://creativecommons.org/licenses/by-sa/2.5/)
- OWASP Secure Headers Project (CC-BY-SA 4.0): [https://creativecommons.org/licenses/by-sa/4.0/](https://creativecommons.org/licenses/by-sa/4.0/)
