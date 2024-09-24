# Content-Security-Policy Header

## Purpose

The `Content-Security-Policy` (CSP) header helps mitigate cross-site scripting (XSS), data injection, and other attacks by specifying the sources from which content can be loaded. By restricting the sources for different types of content (scripts, styles, images, etc.), CSP provides an additional layer of security.

## Best Practices

- **`default-src 'self'`**: Restricts content to the same origin by default.
- **`object-src 'none'`**: Disables plugins such as Flash and Java applets.
- **`script-src 'self'`**: Allows JavaScript execution only from your domain.
- **`upgrade-insecure-requests`**: Ensures that any HTTP URLs are upgraded to HTTPS.

## Configuration in `secure.py`

The `ContentSecurityPolicy` class in `secure.py` allows flexible configuration of CSP. You can add various directives for specific content types like `script-src`, `style-src`, `img-src`, etc., to enhance security.

### Example Configuration

```python
secure_headers = Secure(
    csp=ContentSecurityPolicy()
        .default_src("'self'")
        .script_src("'self'")
        .style_src("'self'")
        .object_src("'none'")
)
```

### Methods Available

- **`default_src(*sources)`**: Specifies default content sources.
- **`script_src(*sources)`**: Specifies valid JavaScript sources.
- **`style_src(*sources)`**: Specifies valid CSS sources.
- **`object_src(*sources)`**: Specifies valid plugin sources (e.g., `<object>`, `<embed>`, `<applet>`).
- **`upgrade_insecure_requests()`**: Automatically upgrades HTTP URLs to HTTPS.

## Example Usage

To set up a `Content-Security-Policy` header that only allows content from the same origin and restricts the use of plugins:

```python
csp = ContentSecurityPolicy()
    .default_src("'self'")
    .script_src("'self'")
    .object_src("'none'")
print(csp.header_name)   # Output: 'Content-Security-Policy'
print(csp.header_value)  # Output: "default-src 'self'; script-src 'self'; object-src 'none'"
```

This can then be applied as part of your Secure headers configuration.

```python
secure_headers = Secure(csp=csp)
```

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/#content-security-policy) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
