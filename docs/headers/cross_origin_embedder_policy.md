# Cross-Origin-Embedder-Policy Header

## Purpose

The `Cross-Origin-Embedder-Policy` (COEP) header prevents a document from loading any cross-origin resources that don’t explicitly grant permission. It works alongside the `Cross-Origin-Resource-Policy` (CORP) to enhance security, especially in modern applications dealing with cross-origin requests.

## Best Practices

- **`require-corp`**: Only allow loading resources from the same origin or those explicitly permitting cross-origin access. This is the most secure setting.
- **`unsafe-none`**: Permits loading cross-origin resources without explicit permission. Use this only when security constraints aren't a concern.

## Configuration in `secure.py`

The `CrossOriginEmbedderPolicy` class in `secure.py` allows you to configure the COEP header with options like `require-corp` or `unsafe-none` to control resource loading policies.

### Example Configuration

```python
secure_headers = Secure(
    coep=CrossOriginEmbedderPolicy().require_corp()
)
```

### Methods Available

- **`require_corp()`**: Ensures resources are loaded only from the same origin or from origins that grant explicit permission.
- **`unsafe_none()`**: Disables the COEP policy, allowing cross-origin resources to be loaded without restriction.

## Example Usage

To set up a `Cross-Origin-Embedder-Policy` header that requires cross-origin resources to explicitly permit being loaded:

```python
coep = CrossOriginEmbedderPolicy().require_corp()
print(coep.header_name)   # Output: 'Cross-Origin-Embedder-Policy'
print(coep.header_value)  # Output: 'require-corp'
```

This can then be applied as part of your Secure headers configuration.

```python
secure_headers = Secure(coep=coep)
```

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Embedder-Policy) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/#cross-origin-embedder-policy) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
