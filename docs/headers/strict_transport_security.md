# Strict-Transport-Security (HSTS) Header

## Purpose

The `Strict-Transport-Security` (HSTS) header ensures that the application communicates over HTTPS, preventing man-in-the-middle attacks by instructing the browser to automatically upgrade all HTTP connections to HTTPS. Additionally, this header helps protect your site from downgrade attacks, where an attacker might try to force a user to communicate over an insecure HTTP connection.

## Best Practices

- **Set a long max-age**: A duration of one year (`31536000` seconds) is recommended to enforce HTTPS for an extended period.
- **Include subdomains**: Use the `includeSubDomains` directive to apply the policy to all subdomains.
- **Use the preload directive**: Opt into the HSTS preload list to ensure that browsers always load your site over HTTPS, even on the first visit.

## Configuration in `secure.py`

The `StrictTransportSecurity` class in `secure.py` allows you to configure the `Strict-Transport-Security` (HSTS) header with options like `max-age`, `includeSubDomains`, and `preload`.

### Example Configuration

```python
secure_headers = Secure(
    hsts=StrictTransportSecurity()
        .max_age(31536000)
        .include_subdomains()
        .preload()
)
```

### Methods Available

- **`max_age(seconds)`**: Set the maximum duration (in seconds) for which the browser should enforce the HTTPS-only policy.
- **`include_subdomains()`**: Apply the HSTS policy to all subdomains of the domain.
- **`preload()`**: Opt into the HSTS preload list, ensuring that all requests to your site are made over HTTPS, even on the first visit.

## Example Usage

To set up a `Strict-Transport-Security` header with a one-year max age, including subdomains and opting into the HSTS preload list:

```python
hsts_header = StrictTransportSecurity().max_age(31536000).include_subdomains().preload()
print(hsts_header.header_name)   # Output: 'Strict-Transport-Security'
print(hsts_header.header_value)  # Output: 'max-age=31536000; includeSubDomains; preload'
```

This can then be applied as part of your Secure headers configuration:

```python
secure_headers = Secure(hsts=hsts_header)
```

## **Resources**

- [MDN Web Docs: Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security)
- [OWASP Secure Headers Project: HSTS](https://owasp.org/www-project-secure-headers/#http-strict-transport-security)
- [HSTS Preload List](https://hstspreload.org/)

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/#http-strict-transport-security) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
