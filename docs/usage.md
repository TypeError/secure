# Usage Guide

## Overview

The `secure` library is designed to simplify the configuration of HTTP security headers in Python web applications. This guide provides detailed examples of how to use the library, from setting basic security headers to leveraging advanced presets and custom configurations.

## Setting Basic Security Headers

To start using `secure`, you can quickly set up a default configuration that applies common security headers. Here's a basic example:

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

`secure` offers three preset configurations: `BALANCED`, `BASIC`, and `STRICT`. These are pre-configured sets of security headers that can be quickly applied to your web application for different security needs.

---

## **BALANCED Preset**

The `BALANCED` preset is the recommended default and corresponds to `Secure.with_default_headers()`. It keeps the response headers focused while still enforcing CSP, HSTS, COOP/Corp, and other modern defaults.

### Example Code:

```python
from flask import Flask, Response

from secure import Preset, Secure

app = Flask(__name__)
secure_headers = Secure.from_preset(Preset.BALANCED)

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
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
Content-Security-Policy: default-src 'self'; base-uri 'self'; font-src 'self' https: data:; form-action 'self'; frame-ancestors 'self'; img-src 'self' data:; object-src 'none'; script-src 'self'; script-src-attr 'none'; style-src 'self' https: 'unsafe-inline'; upgrade-insecure-requests
Strict-Transport-Security: max-age=31536000; includeSubDomains
Permissions-Policy: geolocation=(), microphone=(), camera=()
Referrer-Policy: strict-origin-when-cross-origin
Server:
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
```

Balanced omits `Cache-Control` and the legacy/resource headers included by `Preset.BASIC`, so add them manually when your deployment still relies on them.

---

## **BASIC Preset**

The `BASIC` preset mirrors Helmet.js defaults. It extends the Balanced set with extra compatibility headers such as `X-Permitted-Cross-Domain-Policies` and `X-XSS-Protection`.

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
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
Content-Security-Policy: default-src 'self'; base-uri 'self'; font-src 'self' https: data:; form-action 'self'; frame-ancestors 'self'; img-src 'self' data:; object-src 'none'; script-src 'self'; script-src-attr 'none'; style-src 'self' https: 'unsafe-inline'; upgrade-insecure-requests
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: no-referrer
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-Permitted-Cross-Domain-Policies: none
X-DNS-Prefetch-Control: off
Origin-Agent-Cluster: ?1
X-Download-Options: noopen
X-XSS-Protection: 0
```

Use this preset when you want to match the Helmet.js defaults exactly.

---

## **STRICT Preset**

The `STRICT` preset applies the most walls for security-focused deployments that tolerate tighter restrictions. It enables COEP, CSP base/frame restrictions, and aggressive HSTS (without preload by default).

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
Cache-Control: no-store, max-age=0
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Opener-Policy: same-origin
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'
Strict-Transport-Security: max-age=63072000; includeSubDomains
Permissions-Policy: geolocation=(), microphone=(), camera=()
Referrer-Policy: no-referrer
Server:
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

Start with `BALANCED` and move to `STRICT` once you have validated that your application works correctly with the stricter Content Security Policy, caching, and frame restrictions.

---

You can easily adjust between these presets based on your application's needs by importing `Preset.BASIC`, `Preset.BALANCED`, or `Preset.STRICT` and applying it to your response handlers.

---

## Customizing Individual Headers

In addition to using presets, you can tailor individual headers to fit your application’s specific security requirements.

### Example: Customizing `Content-Security-Policy`

```python
from secure import ContentSecurityPolicy, Secure

secure_headers = Secure(
    csp=ContentSecurityPolicy()
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

## Middleware

Secure exposes `SecureWSGIMiddleware` and `SecureASGIMiddleware` through `secure.middleware`. Each middleware accepts a `Secure` instance (defaulting to `Secure.with_default_headers()`), overwrites headers by default, and only appends duplicates when the normalized header name is listed in `multi_ok` (which defaults to `secure.MULTI_OK`, including `Content-Security-Policy`).

### WSGI (Flask)

Wrap a Flask app by replacing its `wsgi_app`, ensuring every response passes through the middleware:

```python
from flask import Flask
from secure import Secure
from secure.middleware import SecureWSGIMiddleware

secure_headers = Secure.with_default_headers()
app = Flask(__name__)
app.wsgi_app = SecureWSGIMiddleware(app.wsgi_app, secure=secure_headers)
```

### WSGI (Django)

Django middleware wraps requests and responses rather than the raw WSGI callable, so apply secure headers with a lightweight middleware class:

```python
from secure import Secure

class SecureHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.secure = Secure.with_default_headers()

    def __call__(self, request):
        response = self.get_response(request)
        self.secure.set_headers(response)
        return response
```

Add `SecureHeadersMiddleware` to the `MIDDLEWARE` setting to run secure headers on every Django response.

### ASGI (FastAPI)

`SecureASGIMiddleware` touches only HTTP scopes and leaves WebSocket traffic unchanged. Mount it manually or via FastAPI’s middleware helper:

```python
from fastapi import FastAPI
from secure import Secure
from secure.middleware import SecureASGIMiddleware

secure_headers = Secure.with_default_headers()
app = FastAPI()
app.add_middleware(SecureASGIMiddleware, secure=secure_headers)
```

### ASGI (Shiny for Python)

Wrap a Shiny `App` directly with the middleware to secure HTTP responses:

```python
from shiny import App
from secure import Secure
from secure.middleware import SecureASGIMiddleware

secure_headers = Secure.with_default_headers()
app = SecureASGIMiddleware(App(), secure=secure_headers)
```

### Customizing `multi_ok`

Pass an explicit `multi_ok` iterable to either middleware to append headers whose names must appear multiple times (for example, when downstream code already emits `Content-Security-Policy`).

---

## Full Example with Customization

The following is a complete example demonstrating how to combine default headers with custom configurations:

```python
from secure import Secure, StrictTransportSecurity, XFrameOptions

secure_headers = Secure(
    hsts=StrictTransportSecurity()
         .max_age(63072000)
         .include_subdomains(),
    xfo=XFrameOptions().deny()
)

def add_security_headers(response):
    # Apply security headers to the response
    secure_headers.set_headers(response)
    return response
```

In this example, a custom `Strict-Transport-Security` (HSTS) header is configured to enforce HTTPS for two years across all subdomains, and the `X-Frame-Options` header is set to `DENY` to prevent clickjacking.

---

## Summary

The `secure` library offers flexibility and ease of use when configuring HTTP security headers for Python web applications. You can use pre-configured presets for quick setups or customize headers individually to meet your specific security needs. By leveraging both synchronous and asynchronous methods, `secure` fits seamlessly into any Python-based web framework.

For more details on the individual headers and advanced usage, refer to the [Security Headers](./headers) documentation.

---

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))
