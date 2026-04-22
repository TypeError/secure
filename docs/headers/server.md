# Server Header

## Purpose

The `Server` header can reveal details about the software handling the request. In `secure`, the builder defaults to an empty string so your application can avoid adding identifying detail when the surrounding stack allows it.

## Best Practices

- **Set an empty value or custom string**: Use an empty or generic value when you want `secure` to control the header.
- **Avoid exposing server information**: Avoid leaving the default server response, which may expose sensitive version information.
- **Check upstream defaults**: Proxies, ASGI servers, and framework middleware may still add their own `Server` header unless you disable that behavior.

## Configuration with `secure`

The `Server` class in `secure` allows you to easily control the `Server` header value, with the default value set to an empty string to enhance security.

### Example Configuration

```python
from secure import Secure, Server

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
from secure import Server

server_header = Server().set("")
print(server_header.header_name)   # Output: 'Server'
print(server_header.header_value)  # Output: ''
```

This can then be applied as part of your Secure headers configuration:

```python
from secure import Secure

secure_headers = Secure(server=server_header)
```

### Special Considerations for Frameworks

Some frameworks like Uvicorn automatically inject a `Server` header. If you're using Uvicorn and need to override or remove this header, refer to the [framework integration guide](../frameworks.md) for specific instructions on how to disable Uvicorn's default `Server` header.

## **Resources**

- [MDN Web Docs: Server Header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server)
- [OWASP Secure Headers Project: Server Header](https://owasp.org/www-project-secure-headers/#server-header)

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Server) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/#server-header) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
