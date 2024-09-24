# Server Header

## Purpose

The `Server` header provides information about the server software handling the request. By default, this header exposes the server's technology stack, which can increase the risk of targeted attacks. For enhanced security, it is recommended to obscure or remove this header to prevent unnecessary exposure of server details.

## Best Practices

- **Set an empty value or custom string**: It's generally advisable to set the `Server` header to an empty value (`""`) or use a non-informative value to avoid revealing specific details about the server software.
- **Avoid exposing server information**: Avoid leaving the default server response, which may expose sensitive version information.

## Configuration in `secure.py`

The `Server` class in `secure.py` allows you to easily control the `Server` header value, with the default value set to an empty string to enhance security.

### Example Configuration

```python
secure_headers = Secure(
    server=Server().set("")
)
```

### Methods Available

- **`set(value)`**: Set a custom value for the `Server` header.
- **`clear()`**: Clear any custom value and revert the header to its default secure value (an empty string).

## Example Usage

To set up the `Server` header and hide the server information:

```python
server_header = Server().set("")
print(server_header.header_name)   # Output: 'Server'
print(server_header.header_value)  # Output: ''
```

This can then be applied as part of your Secure headers configuration:

```python
secure_headers = Secure(server=server_header)
```

## **Resources**

- [MDN Web Docs: Server Header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server)
- [OWASP Secure Headers Project: Server Header](https://owasp.org/www-project-secure-headers/#server-header)

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/#server-header) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
