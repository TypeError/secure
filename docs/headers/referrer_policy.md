# Referrer-Policy

## Purpose

The `Referrer-Policy` response header controls how much referrer information (sent via the `Referer` header) is included with outgoing requests. It is primarily a privacy and data-minimization control, with important security implications when navigating across origins or downgrading from HTTPS to HTTP.

> Note: `Referer` is intentionally misspelled in HTTP. `Referrer-Policy` does **not** share that misspelling.

## Default behavior

**Default header value:** `strict-origin-when-cross-origin`

This matches modern browser defaults: if no policy is specified (or the provided value is invalid), the effective policy is `strict-origin-when-cross-origin`.

## Best practices (recommended choices)

- **`strict-origin-when-cross-origin` (recommended default)**  
  Sends the full referrer (origin + path + query) for same-origin requests; sends **origin only** for cross-origin HTTPS→HTTPS; sends **no `Referer`** when downgrading (HTTPS→HTTP).
- **`no-referrer` (max privacy)**  
  Omits the `Referer` header entirely for all requests.
- **`same-origin` (strict privacy across sites)**  
  Sends referrer only for same-origin requests; omits it for cross-origin requests.
- **Avoid `unsafe-url`** unless you fully understand the impact (it can leak sensitive URL data across origins and to insecure destinations).

## Configuration with `Secure`

```python
from secure.secure import Secure
from secure.headers import ReferrerPolicy

secure = Secure(
    referrer=ReferrerPolicy()  # uses the default: strict-origin-when-cross-origin
)
```

### Set a single explicit policy

Use `value(...)` (or `custom(...)`) when you want to **replace** any configured policies and set exactly one value:

```python
from secure.secure import Secure
from secure.headers import ReferrerPolicy

secure = Secure(
    referrer=ReferrerPolicy().value("no-referrer")
)
```

You can also use the fluent directive helpers:

```python
secure = Secure(
    referrer=ReferrerPolicy().no_referrer()
)
```

### Specify a fallback policy list (HTTP header only)

Browsers support a **comma-separated list** in the `Referrer-Policy` HTTP header. The desired (most modern) policy should be listed **last**.

```python
from secure.headers import ReferrerPolicy

rp = ReferrerPolicy().fallback("no-referrer", "strict-origin-when-cross-origin")
print(rp.header_name)   # Referrer-Policy
print(rp.header_value)  # no-referrer, strict-origin-when-cross-origin
```

You can build the same list with `.add(...)`:

```python
rp = (
    ReferrerPolicy()
    .clear()
    .add("no-referrer")
    .add("strict-origin-when-cross-origin")
)
```

> Note: the fallback _list_ behavior is supported in the HTTP header, but not in the HTML `referrerpolicy` attribute.

## API reference (ReferrerPolicy)

### Core builder methods

- `value("...")` / `custom("...")`
  Replace all configured policies with the provided value (supports comma-separated lists).
- `add("...")` / `set("...")`
  Append one or more policy tokens (supports comma-separated lists). Duplicate tokens are ignored.
- `fallback(*policies)`
  Replace the current policies with an explicit ordered fallback list.
- `clear()`
  Clear configured policies (returns to default behavior unless you add values afterward).

### Directive helpers (MDN policies)

Each of these appends the corresponding token (same behavior as `add("token")`):

- `no_referrer()` → `no-referrer`
  Omits the `Referer` header entirely.
- `no_referrer_when_downgrade()` → `no-referrer-when-downgrade`
  Sends full referrer for same-or-more secure requests; omits referrer on downgrade (HTTPS→HTTP).
- `origin()` → `origin`
  Sends only the origin (scheme + host + port).
- `origin_when_cross_origin()` → `origin-when-cross-origin`
  Same-origin: full referrer; cross-origin and downgrade: origin only.
- `same_origin()` → `same-origin`
  Same-origin: full referrer; cross-origin: omit referrer.
- `strict_origin()` → `strict-origin`
  Sends only origin for same-security requests; omits on downgrade (HTTPS→HTTP).
- `strict_origin_when_cross_origin()` → `strict-origin-when-cross-origin`
  Same-origin: full referrer; cross-origin HTTPS→HTTPS: origin only; downgrade: omit.
- `unsafe_url()` → `unsafe-url`
  Sends origin + path + query for all requests (generally discouraged; may leak sensitive data).

## Example usage

```python
from secure.headers import ReferrerPolicy

referrer_policy = ReferrerPolicy().strict_origin_when_cross_origin()
print(referrer_policy.header_name)   # 'Referrer-Policy'
print(referrer_policy.header_value)  # 'strict-origin-when-cross-origin'
```

## Resources

- MDN Web Docs: Referrer-Policy
  [https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy)
- OWASP Secure Headers Project: Referrer-Policy
  [https://owasp.org/www-project-secure-headers/#referrer-policy](https://owasp.org/www-project-secure-headers/#referrer-policy)

## Attribution

This library implements security recommendations from trusted sources:

- MDN Web Docs (licensed under CC-BY-SA 2.5)
  [https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor](https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor)
  [https://creativecommons.org/licenses/by-sa/2.5/](https://creativecommons.org/licenses/by-sa/2.5/)
- OWASP Secure Headers Project (licensed under CC-BY-SA 4.0)
  [https://creativecommons.org/licenses/by-sa/4.0/](https://creativecommons.org/licenses/by-sa/4.0/)
