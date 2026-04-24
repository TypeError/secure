# CustomHeader Class

## What it does

The `CustomHeader` class lets you create arbitrary HTTP response headers when `secure` does not provide a dedicated builder.

## Minimal example

```python
from secure import CustomHeader, Secure

custom_header = CustomHeader("X-Custom-Header", "CustomValue")
secure_headers = Secure(custom=[custom_header])
```

## Resulting header

```http
X-Custom-Header: CustomValue
```

## Practical note

Use `CustomHeader` for app-specific or infrastructure-specific headers. If you later call `allowlist_headers(...)`, remember to allow the custom name explicitly when needed.

## Best Practices

- Prefer standard header names when they exist; use custom names only for application- or infrastructure-specific behavior.
- If you use `allowlist_headers(...)`, remember that custom names may need to be added through `allow_extra=...`.

## Configuration with `Secure`

Use `CustomHeader` when you need a header without a dedicated builder. You can set the name and value directly, then update the value later if needed.

### Methods Available

- **`set(value)` / `value(value)`**: Updates the value of the custom header.
- **`header_value`**: Property that retrieves the current value of the custom header.

## Example Usage

To define a custom header and use it in a secure configuration:

```python
from secure import CustomHeader

custom_header = CustomHeader("X-Custom-Header", "CustomValue")
print(custom_header.header_name)   # Output: 'X-Custom-Header'
print(custom_header.header_value)  # Output: 'CustomValue'

# Update the value
custom_header.set("NewValue")
print(custom_header.header_value)  # Output: 'NewValue'
```

## **Resources**

- [MDN Web Docs: HTTP Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
