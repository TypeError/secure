# X-Content-Type-Options Header

## Purpose

The `X-Content-Type-Options` header prevents browsers from MIME-sniffing a response away from the declared `Content-Type`. This helps protect against certain types of attacks, such as cross-site scripting (XSS) and drive-by downloads, where an attacker tries to disguise a file's MIME type in order to trick the browser into executing malicious content.

## Best Practices

- **Set to `nosniff`**: This is the recommended value, as it tells the browser to strictly follow the declared `Content-Type` and not attempt to guess or "sniff" the MIME type. This helps prevent MIME-based attacks.

## Configuration in `secure.py`

The `XContentTypeOptions` class in `secure.py` allows you to easily configure the `X-Content-Type-Options` header. The default value is `nosniff`, which is the recommended setting.

### Example Configuration

```python
secure_headers = Secure(
    xcto=XContentTypeOptions().nosniff()
)
```

### Methods Available

- **`nosniff()`**: Sets the `X-Content-Type-Options` header to `nosniff`, which prevents MIME-sniffing by browsers.
- **`set(value)`**: Sets a custom value for the `X-Content-Type-Options` header.
- **`clear()`**: Clears any custom value and reverts the header to its default value (`nosniff`).

## Example Usage

To set up the `X-Content-Type-Options` header and prevent MIME-sniffing:

```python
xcto_header = XContentTypeOptions().nosniff()
print(xcto_header.header_name)   # Output: 'X-Content-Type-Options'
print(xcto_header.header_value)  # Output: 'nosniff'
```

This can then be applied as part of your Secure headers configuration:

```python
secure_headers = Secure(xcto=xcto_header)
```

## **Resources**

- [MDN Web Docs: X-Content-Type-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options)
- [OWASP Secure Headers Project: X-Content-Type-Options](https://owasp.org/www-project-secure-headers/#x-content-type-options)

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/#x-content-type-options) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
