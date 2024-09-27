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

### Presets Overview

`secure.py` offers two preset configurations: `STRICT` and `BASIC`. These are pre-configured sets of security headers that can be quickly applied to your web application for different security needs.

---

## **STRICT Preset**

The `STRICT` preset applies a high level of security headers, ideal for applications that need strict protection against various web vulnerabilities, such as XSS, clickjacking, and cross-origin attacks.

### Example Code:

```python
from flask import Flask, Response

from secure import Preset, Secure

app = Flask(__name__)
secure_headers = Secure.from_preset(Preset.STRICT)

@app.after_request
def add_security_headers(response: Response):
    secure_headers.set_headers(response)
    return response

@app.route("/")
def home():
    return "Hello, world"

if __name__ == "__main__":
    app.run()
```

### Example Headers:

```http
Cache-Control: no-store
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Opener-Policy: same-origin
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
Permissions-Policy: geolocation=(), microphone=(), camera=()
Referrer-Policy: no-referrer
Server:
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

This preset is perfect for highly sensitive applications, enforcing strict rules around resource loading and connection security.

---

## **BASIC Preset**

The `BASIC` preset applies a more relaxed set of headers that still offer strong security protection, suitable for most standard applications.

### Example Code:

```python
from flask import Flask, Response

from secure import Preset, Secure

app = Flask(__name__)
secure_headers = Secure.from_preset(Preset.BASIC)

@app.after_request
def add_security_headers(response: Response):
    secure_headers.set_headers(response)
    return response

@app.route("/")
def home():
    return "Hello, world"

if __name__ == "__main__":
    app.run()
```

### Example Headers:

```http
Cache-Control: no-store
Strict-Transport-Security: max-age=31536000
Referrer-Policy: strict-origin-when-cross-origin
Server:
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
```

The `BASIC` preset is suitable for most general-purpose applications, balancing security and flexibility.

---

You can easily adjust between these presets based on your application's needs by importing `Preset.BASIC` or `Preset.STRICT` and applying it to your response handlers.

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
