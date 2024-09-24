# Usage Guide

## Overview

The `secure.py` library is designed to simplify the configuration of HTTP security headers in Python web applications. This guide provides detailed examples of how to use the library, from setting basic security headers to leveraging advanced presets and custom configurations.

## Setting Basic Security Headers

To start using `secure.py`, you can quickly set up a default configuration that applies common security headers. Here's a basic example:

```python
from secure import Secure

secure_headers = Secure.with_default_headers()

def add_security_headers(response):
    secure_headers.set_headers(response)
    return response
```

This will apply a standard set of HTTP security headers, such as `Content-Security-Policy`, `Strict-Transport-Security`, and `X-Frame-Options`, ensuring a baseline level of security.

---

## Using Presets

`secure.py` offers pre-configured presets to make securing your application easier. These presets apply common security best practices and save you from manually configuring each header.

### Available Presets

- **`Preset.BASIC`**: A minimal configuration that includes essential security headers.
- **`Preset.STRICT`**: A stricter configuration for applications that require a higher level of security.

### Example: Using the `BASIC` Preset

```python
from secure import Secure, Preset

secure_headers = Secure.from_preset(Preset.BASIC)

def add_security_headers(response):
    secure_headers.set_headers(response)
    return response
```

### Example: Using the `STRICT` Preset

```python
from secure import Secure, Preset

secure_headers = Secure.from_preset(Preset.STRICT)

def add_security_headers(response):
    secure_headers.set_headers(response)
    return response
```

Using the `STRICT` preset enforces more comprehensive security measures, such as preventing JavaScript from untrusted sources and ensuring that all subdomains adhere to HTTPS policies.

---

## Customizing Individual Headers

In addition to using presets, you can tailor individual headers to fit your application’s specific security requirements.

### Example: Customizing `Content-Security-Policy`

```python
from secure import Secure

secure_headers = Secure(
    csp=Secure.ContentSecurityPolicy()
         .default_src("'self'")
         .img_src("https://trusted-images.com")
)

def add_security_headers(response):
    secure_headers.set_headers(response)
    return response
```

In this example, the `Content-Security-Policy` (CSP) header is customized to allow images from a trusted domain while enforcing `'self'` as the default source for all other content.

---

## Asynchronous Usage

For asynchronous frameworks (such as `aiohttp`, `FastAPI`, or `Quart`), you can use the `set_headers_async()` method to apply security headers without blocking the event loop:

```python
async def add_security_headers(response):
    await secure_headers.set_headers_async(response)
    return response
```

This approach ensures that your security headers are applied efficiently in non-blocking environments.

---

## Full Example with Customization

The following is a complete example demonstrating how to combine default headers with custom configurations:

```python
from secure import Secure

secure_headers = Secure(
    hsts=Secure.StrictTransportSecurity()
         .max_age(63072000)
         .include_subdomains(),
    xfo=Secure.XFrameOptions().deny()
)

def add_security_headers(response):
    # Apply security headers to the response
    secure_headers.set_headers(response)
    return response
```

In this example, a custom `Strict-Transport-Security` (HSTS) header is configured to enforce HTTPS for two years across all subdomains, and the `X-Frame-Options` header is set to `DENY` to prevent clickjacking.

---

## Summary

The `secure.py` library offers flexibility and ease of use when configuring HTTP security headers for Python web applications. You can use pre-configured presets for quick setups or customize headers individually to meet your specific security needs. By leveraging both synchronous and asynchronous methods, `secure.py` fits seamlessly into any Python-based web framework.

For more details on the individual headers and advanced usage, refer to the [Security Headers](./headers) documentation.

---

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
