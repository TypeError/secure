# X-Permitted-Cross-Domain-Policies

## Purpose

`X-Permitted-Cross-Domain-Policies` is a **response header** that sets a _meta-policy_ controlling whether site resources can be accessed cross-origin by documents running in legacy web clients (for example, Adobe Acrobat or Microsoft Silverlight).

Usage is less common today because Flash/Silverlight have been deprecated, but many security testing tools still check for `X-Permitted-Cross-Domain-Policies: none` to reduce the risk of an overly-permissive cross-domain policy being present accidentally or maliciously.

> This documentation format mirrors the style used in the existing header docs (e.g., Cache-Control).

## Default behavior

If you create `XPermittedCrossDomainPolicies()` and do not set a policy, it returns the library default value:

- **Default header value:** `none`

This is the least permissive option and is the most common secure setting when you do not need legacy cross-domain policy behavior.

## Using with `Secure`

```python
from secure import Secure, XPermittedCrossDomainPolicies

secure = Secure(
    xpcdp=XPermittedCrossDomainPolicies().none()
)
```

If you don’t configure anything, the default value is emitted.

## Common recipes

### 1) Disallow cross-domain policy files (recommended default)

```python
from secure import XPermittedCrossDomainPolicies

xpcdp = XPermittedCrossDomainPolicies()  # default: none
print(xpcdp.header_name)   # X-Permitted-Cross-Domain-Policies
print(xpcdp.header_value)  # none
```

MDN notes this is the typical configuration when you don’t need legacy clients.

### 2) Allow only a master policy file

```python
xpcdp = XPermittedCrossDomainPolicies().master_only()
print(xpcdp.header_value)  # master-only
```

This allows cross-domain access to the master policy file defined on the same domain.

### 3) Constrain policy files by content type (HTTP/HTTPS only)

```python
xpcdp = XPermittedCrossDomainPolicies().by_content_type()
print(xpcdp.header_value)  # by-content-type
```

Only policy files served with `Content-Type: text/x-cross-domain-policy` are allowed.

### 4) Indicate this response should not be treated as a policy file

```python
xpcdp = XPermittedCrossDomainPolicies().none_this_response()
print(xpcdp.header_value)  # none-this-response
```

This directive is unique to the HTTP header and indicates the current document should not be used as a policy file.

## Builder API

### Policy directives (single value)

- `.none()`
- `.master_only()`
- `.by_content_type()` (HTTP/HTTPS only)
- `.by_ftp_filename()` (FTP only)
- `.all()`
- `.none_this_response()` (HTTP-header-only)

These map directly to the directive definitions described by MDN (and largely echoed by OWASP).

### Typed helper

- `.policy("none" | "master-only" | "by-content-type" | "by-ftp-filename" | "all" | "none-this-response")`

Raises `ValueError` for unsupported values (helps catch typos early).

## Escape hatches

### `.value("...")`

Set an explicit header value (replaces any configured directive):

```python
xpcdp = XPermittedCrossDomainPolicies().value("none")
print(xpcdp.header_value)  # none
```

### `.custom("token")`

Alias for `.value(...)` (use when you intentionally want a raw string value):

```python
xpcdp = XPermittedCrossDomainPolicies().custom("master-only")
print(xpcdp.header_value)  # master-only
```

### `.clear()`

Reset to the default:

```python
xpcdp = XPermittedCrossDomainPolicies().all().clear()
print(xpcdp.header_value)  # none
```

## Deterministic output & safety

- The header value is rendered as a **single directive token**, so output is inherently deterministic.
- Raw setters (`.value(...)` / `.custom(...)`) normalize obvious header-splitting primitives (CR/LF) before serialization; stricter validation can be enforced via `Secure.validate_and_normalize_headers(...)`.

## Attribution

This library implements security recommendations and behavior described by:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Permitted-Cross-Domain-Policies) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/#x-permitted-cross-domain-policies) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
