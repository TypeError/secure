# CustomHeader Class

## Purpose

The `CustomHeader` class lets you create arbitrary HTTP response headers when `secure` does not provide a dedicated builder.

## Best Practices

- Prefer standard header names when they exist; use custom names only for application- or infrastructure-specific behavior.
- If you use `allowlist_headers(...)`, remember that custom names may need to be added through `allow_extra=...`.

## Configuration with `secure`

The `CustomHeader` class in `secure` provides flexibility for developers to define and set custom HTTP headers as needed. You can specify both the header name and value and update the value later if necessary.

### Example Configuration

```python
from secure import CustomHeader

custom_header = CustomHeader("X-Custom-Header", "CustomValue")
```

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

This can then be applied as part of your Secure headers configuration:

```python
from secure import Secure

secure_headers = Secure(custom=[custom_header])
```

## **Resources**

- [MDN Web Docs: HTTP Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
