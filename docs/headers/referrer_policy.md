# Referrer-Policy Header

## Purpose

The `Referrer-Policy` header controls how much referrer information is included with requests made from your website. This header helps protect user privacy by limiting the amount of data exposed via the `Referer` header, especially when navigating between different origins.

## Best Practices

- **`strict-origin-when-cross-origin`**: This is a secure default, providing the full URL for same-origin requests and only the origin for cross-origin requests.
- **`no-referrer`**: Use this option to completely suppress the `Referer` header in all requests, offering the most privacy.
- **`no-referrer-when-downgrade`**: Prevents sending the referrer when transitioning from HTTPS to HTTP, protecting information from being leaked over unsecured connections.

## Configuration in `secure.py`

The `ReferrerPolicy` class in `secure.py` allows you to configure the `Referrer-Policy` header with various directives depending on your site's security and privacy requirements.

### Example Configuration

```python
secure_headers = Secure(
    referrer=ReferrerPolicy().strict_origin_when_cross_origin()
)
```

### Methods Available

- **`no_referrer()`**: No `Referer` header will be sent.
- **`no_referrer_when_downgrade()`**: The `Referer` header will not be sent when navigating from HTTPS to HTTP.
- **`origin()`**: The `Referer` header will contain only the origin of the URL.
- **`same_origin()`**: The `Referer` header will be sent only for same-origin requests.
- **`strict_origin_when_cross_origin()`**: The full URL is sent for same-origin requests, but only the origin for cross-origin requests.
- **`unsafe_url()`**: The full URL will always be sent, even for cross-origin requests. This may expose sensitive information.

## Example Usage

To set up a `Referrer-Policy` header that limits the exposure of referrer information:

```python
referrer_policy = ReferrerPolicy().strict_origin_when_cross_origin()
print(referrer_policy.header_name)   # Output: 'Referrer-Policy'
print(referrer_policy.header_value)  # Output: 'strict-origin-when-cross-origin'
```

This can then be applied as part of your Secure headers configuration:

```python
secure_headers = Secure(referrer=referrer_policy)
```

## **Resources**

- [MDN Web Docs: Referrer-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy)
- [OWASP Secure Headers Project: Referrer-Policy](https://owasp.org/www-project-secure-headers/#referrer-policy)

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/#referrer-policy) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
