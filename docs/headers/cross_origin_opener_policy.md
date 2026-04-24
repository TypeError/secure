# Cross-Origin-Opener-Policy

## What it does

The `Cross-Origin-Opener-Policy` (COOP) response header controls whether documents opened via `Window.open()` (or navigations) share the same **browsing context group (BCG)** as their opener. When a document is opened into a new BCG, references between the opener and the opened document are severed, which helps mitigate cross-origin attacks often referred to as **XS-Leaks**.

## Minimal example

```python
from secure import CrossOriginOpenerPolicy, Secure

secure_headers = Secure(
    coop=CrossOriginOpenerPolicy().same_origin()
)
```

## Resulting header

```http
Cross-Origin-Opener-Policy: same-origin
```

## Practical note

`same-origin` is a strong default, but popup-based flows such as OAuth or payment providers sometimes need `same-origin-allow-popups`. Test those flows before tightening COOP.

## Defaults

- **Browser/spec behavior:** If the header is **absent**, the effective behavior is equivalent to `unsafe-none` (opt-out).
- **Library default:** This library’s builder defaults to `same-origin` (a secure default), and the built-in presets also configure COOP as `same-origin`.

## Best Practices

- **`same-origin`**: Strong isolation; commonly used for cross-origin isolation (often paired with COEP).
- **`same-origin-allow-popups`**: Like `same-origin`, but relaxes behavior for integrations that open trusted popups/tabs that opt out (e.g., OAuth/payment flows).
- **`noopener-allow-popups`**: Always isolates into a new BCG (except when opened by a same-origin document that also uses `noopener-allow-popups`). Useful when you need to isolate **same-origin** apps from each other (e.g., `/chat` vs `/passwords`) while still allowing popups.
- **`unsafe-none`**: Opts out of COOP isolation.

## Configuration with `Secure`

Use the `CrossOriginOpenerPolicy` builder and pass it into `Secure(...)`.

## Methods Available

Directive helpers (recommended):

- `same_origin()`
- `same_origin_allow_popups()`
- `noopener_allow_popups()`
- `unsafe_none()`

Escape hatches:

- `value("...")` / `custom("...")`: Set a raw value (rejects CR/LF).
- `set("...")`: Backwards-compatible alias for `value(...)`.
- `clear()`: Reset back to the library default (`same-origin`).

## Example Usage

```python
from secure import CrossOriginOpenerPolicy, Secure

coop = CrossOriginOpenerPolicy().same_origin()
print(coop.header_name)   # 'Cross-Origin-Opener-Policy'
print(coop.header_value)  # 'same-origin'

secure_headers = Secure(coop=coop)
```

## Notes

- For **cross-origin isolation** (e.g., `SharedArrayBuffer`), COOP is typically paired with **COEP** (often `require-corp`), and your app must satisfy other isolation requirements.

## Attribution

This library implements security recommendations from trusted sources:

- [MDN Web Docs: Cross-Origin-Opener-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/#cross-origin-opener-policy) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
