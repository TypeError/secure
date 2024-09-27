# CustomHeader Class

## Purpose

The `CustomHeader` class allows the creation and management of custom HTTP headers with arbitrary names and values. This is particularly useful for adding non-standard headers to HTTP responses or requests, such as headers specific to your application or infrastructure.

## Best Practices

- Custom headers should follow the convention of using a prefix like `X-` (e.g., `X-Custom-Header`), although this is no longer a requirement as per the latest RFC.
- Be cautious when adding custom headers to avoid potential conflicts or leaking sensitive information.

## Configuration in `secure.py`

The `CustomHeader` class in `secure.py` provides flexibility for developers to define and set custom HTTP headers as needed. You can specify both the header name and value and update the value later if necessary.

### Example Configuration

```python
custom_header = CustomHeader("X-Custom-Header", "CustomValue")
```

### Methods Available

- **`set(value)`**: Updates the value of the custom header.
- **`header_value()`**: Retrieves the current value of the custom header.

## Example Usage

To define a custom header and use it in a secure configuration:

```python
custom_header = CustomHeader("X-Custom-Header", "CustomValue")
print(custom_header.header_name)   # Output: 'X-Custom-Header'
print(custom_header.header_value)  # Output: 'CustomValue'

# Update the value
custom_header.set("NewValue")
print(custom_header.header_value)  # Output: 'NewValue'
```

This can then be applied as part of your Secure headers configuration:

```python
secure_headers = Secure(custom=[custom_header])
```

## **Resources**

- [MDN Web Docs: HTTP Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
