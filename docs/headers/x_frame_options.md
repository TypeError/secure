# X-Frame-Options Header

## Purpose

The `X-Frame-Options` header helps protect your site from clickjacking attacks by specifying whether your web pages can be embedded in `<frame>`, `<iframe>`, or `<object>` elements. This header ensures that your content is not embedded by other sites, which could trick users into clicking on unintended actions within the embedded content.

## Best Practices

- **`DENY`**: This is the most secure option, as it prevents any site from embedding your page in a frame or iframe.
- **`SAMEORIGIN`**: Allows your page to be embedded only by pages from the same origin (same domain). This option is useful when you need to embed your own pages but prevent other sites from embedding them.

## Configuration in `secure.py`

The `XFrameOptions` class in `secure.py` allows you to configure the `X-Frame-Options` header with values like `DENY` and `SAMEORIGIN`, based on your security needs.

### Example Configuration

```python
secure_headers = Secure(
    xfo=XFrameOptions().deny()
)
```

### Methods Available

- **`deny()`**: Prevents any site from embedding your page.
- **`sameorigin()`**: Allows only the same-origin pages to embed your content.
- **`set(value)`**: Sets a custom value for the `X-Frame-Options` header.
- **`clear()`**: Resets the header to its default value, which is `SAMEORIGIN`.

## Example Usage

To set up the `X-Frame-Options` header and prevent any embedding of your web pages:

```python
xfo_header = XFrameOptions().deny()
print(xfo_header.header_name)   # Output: 'X-Frame-Options'
print(xfo_header.header_value)  # Output: 'DENY'
```

This can then be applied as part of your Secure headers configuration:

```python
secure_headers = Secure(xfo=xfo_header)
```

## **Resources**

- [MDN Web Docs: X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)
- [OWASP Secure Headers Project: X-Frame-Options](https://owasp.org/www-project-secure-headers/#x-frame-options)

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/#x-frame-options) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
