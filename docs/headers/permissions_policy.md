# Permissions-Policy Header

## Purpose

The `Permissions-Policy` header allows you to enable or disable browser features and APIs for your web applications. This header replaces the deprecated `Feature-Policy` header and provides fine-grained control over which features are allowed in your site, such as geolocation, camera access, or microphone use.

## Best Practices

- Disable unnecessary features to reduce your site's attack surface and protect user privacy.
- Allow features only for trusted sources or specific origins to avoid potential misuse.
- Use a restrictive default policy, then selectively enable features as required.

## Configuration in `secure.py`

The `PermissionsPolicy` class in `secure.py` allows you to configure the `Permissions-Policy` header with specific directives for controlling access to browser APIs and features.

### Example Configuration

```python
secure_headers = Secure(
    permissions=PermissionsPolicy()
        .geolocation()
        .microphone()
        .camera()
)
```

### Methods Available

- **`add_directive(directive, *allowlist)`**: Add a custom directive with an optional allowlist of origins.
- **`geolocation(*allowlist)`**: Control access to geolocation data.
- **`camera(*allowlist)`**: Control access to the camera.
- **`microphone(*allowlist)`**: Control access to the microphone.
- **`usb(*allowlist)`**: Control access to USB devices.
- More methods are available for other browser features, such as accelerometer, gyroscope, and more.

## Example Usage

To set up a `Permissions-Policy` header that controls access to specific features:

```python
permissions_policy = PermissionsPolicy()
    .geolocation()
    .camera()
    .microphone()
print(permissions_policy.header_name)   # Output: 'Permissions-Policy'
print(permissions_policy.header_value)  # Output: 'geolocation=(), camera=(), microphone=()'
```

This can then be applied as part of your Secure headers configuration.

```python
secure_headers = Secure(permissions=permissions_policy)
```

## **Resources**

- [MDN Web Docs: Permissions-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy)
- [OWASP Secure Headers Project: Permissions-Policy](https://owasp.org/www-project-secure-headers/#permissions-policy)

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/#permissions-policy) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
