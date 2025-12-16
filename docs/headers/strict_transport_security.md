# Strict-Transport-Security (HSTS)

## Purpose

The `Strict-Transport-Security` (HSTS) header tells browsers that a host **must only be accessed over HTTPS**. Once a browser has received this header, it will automatically upgrade future HTTP navigations to HTTPS for the configured duration, helping prevent man-in-the-middle and downgrade attacks.

> Important: Browsers **ignore** `Strict-Transport-Security` if it is delivered over **insecure HTTP**. You must send it over HTTPS only.

## Default behavior

If you do not configure any directives, this library emits the default header value:

- **Default header value:** `max-age=31536000` (one year)

## Best practices

- **Use a long `max-age`**: One year (`31536000` seconds) is a common baseline.
- **Include subdomains (carefully)**: Add `includeSubDomains` only if _all_ subdomains are HTTPS-ready.
- **Only use `preload` when you mean it**:
  - `preload` is intended for submitting your domain to the HSTS preload list.
  - When using `preload`, the library enforces MDN’s requirements:
    - `max-age` must be **at least 31536000**
    - `includeSubDomains` must be present

## Configuration with `secure`

The `StrictTransportSecurity` header module supports fluent, chainable configuration:

```python
from secure import Secure
from secure.headers import StrictTransportSecurity

secure_headers = Secure(
    hsts=StrictTransportSecurity()
        .max_age(31536000)
        .include_subdomains()
)
```

### Preload configuration

If you opt into preload, the library ensures preload requirements are satisfied:

```python
from secure.headers import StrictTransportSecurity

hsts = (
    StrictTransportSecurity()
    .max_age(31536000)
    .include_subdomains()
    .preload()
)

print(hsts.header_name)   # 'Strict-Transport-Security'
print(hsts.header_value)  # 'max-age=31536000; includeSubDomains; preload'
```

If `preload()` is enabled with a `max-age` less than `31536000`, the header builder will raise a `ValueError`.

## Methods available

- **`max_age(seconds)`**
  Set `max-age`: how long (in seconds) the browser should remember to only use HTTPS for this host.

- **`include_subdomains()`**
  Add `includeSubDomains`: apply the HSTS policy to all subdomains as well.

- **`preload()`**
  Add `preload`: indicates intent to meet HSTS preload requirements. This library:

  - automatically enables `includeSubDomains`
  - enforces `max-age >= 31536000`

- **`clear()`**
  Clear configured directives and reset back to the library default behavior.

- **`value(str)` / `set(str)`**
  Escape hatch: set a raw header value (replaces any configured directives). The value must not contain CR/LF characters.

## Example usage

Minimal one-year HSTS:

```python
from secure.headers import StrictTransportSecurity

hsts = StrictTransportSecurity().max_age(31536000)
print(hsts.header_value)  # 'max-age=31536000'
```

One-year HSTS including subdomains:

```python
from secure.headers import StrictTransportSecurity

hsts = StrictTransportSecurity().max_age(31536000).include_subdomains()
print(hsts.header_value)  # 'max-age=31536000; includeSubDomains'
```

## Resources

- MDN Web Docs: Strict-Transport-Security
  [https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security)
- OWASP Secure Headers Project
  [https://owasp.org/www-project-secure-headers/](https://owasp.org/www-project-secure-headers/)
- HSTS Preload List
  [https://hstspreload.org/](https://hstspreload.org/)

## Attribution

This library implements security recommendations from trusted sources:

- MDN Web Docs: Strict-Transport-Security (licensed under CC-BY-SA 2.5)
  [https://creativecommons.org/licenses/by-sa/2.5/](https://creativecommons.org/licenses/by-sa/2.5/)
- OWASP Secure Headers Project (licensed under CC-BY-SA 4.0)
  [https://creativecommons.org/licenses/by-sa/4.0/](https://creativecommons.org/licenses/by-sa/4.0/)
