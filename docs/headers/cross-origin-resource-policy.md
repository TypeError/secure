# Cross-Origin-Resource-Policy (CORP)

## Purpose

The `Cross-Origin-Resource-Policy` (CORP) response header lets a **resource owner** declare what sites/origins are allowed to load that resource.

This header is commonly used to reduce cross-origin data leaks by controlling who can load your resources (images, scripts, etc.) and by blocking certain cross-origin/cross-site `no-cors` requests when the policy is more restrictive.

## Best Practices

- **`same-origin`**: Strong default for sensitive resources; only allow loads from the same origin.
- **`same-site`**: Useful when you need to share resources across subdomains on the same “site” but not with unrelated sites.
- **`cross-origin`**: Most permissive; allow any origin to load the resource (use intentionally, not by accident).

## Configuration with `secure`

The `CrossOriginResourcePolicy` class provides a fluent API for setting CORP directives and integrates cleanly with `Secure(...)`.

### Example Configuration

```python
secure_headers = Secure(
    corp=CrossOriginResourcePolicy().same_origin()
)
```

> Library default: if you do not change it, the library’s default value is `same-origin`.

### Methods Available

- **`same_origin()`**: Set `Cross-Origin-Resource-Policy: same-origin`
- **`same_site()`**: Set `Cross-Origin-Resource-Policy: same-site`
- **`cross_origin()`**: Set `Cross-Origin-Resource-Policy: cross-origin`
- **`value(value)`**: Set an explicit value (escape hatch; canonicalizes known directives)
- **`clear()`**: Reset to the library default value
- **`set(value)`**: Backwards-compatible alias for `value(...)`

## Example Usage

To restrict resource loading to the same origin:

```python
corp = CrossOriginResourcePolicy().same_origin()
print(corp.header_name)   # Output: 'Cross-Origin-Resource-Policy'
print(corp.header_value)  # Output: 'same-origin'
```

To allow resource loading from the same site (useful for subdomains):

```python
corp = CrossOriginResourcePolicy().same_site()
print(corp.header_value)  # Output: 'same-site'
```

## **Attribution**

This library implements security recommendations from trusted sources:

- MDN Web Docs: `Cross-Origin-Resource-Policy` (licensed under CC-BY-SA 2.5)
- OWASP Secure Headers Project: Cross-Origin-Resource-Policy (licensed under CC-BY-SA 4.0)
