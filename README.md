# secure.py

[![PyPI Version](https://img.shields.io/pypi/v/secure.svg)](https://pypi.org/project/secure/)
[![Python Versions](https://img.shields.io/pypi/pyversions/secure.svg)](https://pypi.org/project/secure/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License](https://img.shields.io/pypi/l/secure.svg)](https://github.com/TypeError/secure/blob/main/LICENSE)

## **Introduction**

**secure.py** is a lightweight and easy-to-use Python library that helps you add optional **security headers** to your web applications across multiple frameworks. It simplifies the application of best security practices for headers such as **Content Security Policy (CSP)**, **Strict-Transport-Security (HSTS)**, **Referrer-Policy**, and more, making your applications safer from common vulnerabilities.

### **Why use secure.py?**

- Apply essential security headers in your Python web applications with minimal effort.
- Consistent API for a wide range of popular web frameworks.
- Supports customization while providing **secure defaults**.
- Easy integration with Python's most used frameworks like Django, Flask, FastAPI, and more.

---

## **Supported Frameworks**

**secure.py** supports the following Python web frameworks:

- [aiohttp](https://docs.aiohttp.org)
- [Bottle](https://bottlepy.org)
- [Django](https://www.djangoproject.com)
- [Falcon](https://falconframework.org)
- [FastAPI](https://fastapi.tiangolo.com)
- [Flask](http://flask.pocoo.org)
- [Pyramid](https://trypyramid.com)
- [Quart](https://pgjones.gitlab.io/quart/)
- [Sanic](https://sanicframework.org)
- [Starlette](https://www.starlette.io/)
- [Tornado](https://www.tornadoweb.org/)

---

## **Features**

- **Secure Headers**: Automatically apply headers like `Strict-Transport-Security`, `X-Frame-Options`, `Content-Security-Policy`, `Referrer-Policy`, and more.
- **Customizable Policies**: Build your own security policies with flexibility using method chaining for headers like CSP.
- **Framework Integration**: Secure headers can be applied to various frameworks, ensuring cross-compatibility.
- **No External Dependencies**: `secure.py` is lightweight and introduces no external dependencies, making it easy to include in any project without worrying about compatibility issues.
- **Easy to Use**: Integrate security headers in just a few lines of code with sensible defaults that adhere to best security practices.
- **Asynchronous Support**: Now provides `async` support for modern asynchronous frameworks like **FastAPI**, **Sanic**, and **Starlette**.

---

## Requirements

- **Python 3.10** or higher

  This library leverages modern Python features introduced in Python 3.10, such as:

  - **Union Type Operator (`|`)**: Simplifies type annotations.
  - **Structural Pattern Matching (`match` statement)**: Enhances control flow.
  - **Improved Type Hinting**: Provides better code clarity and maintenance.

  **Note:** If you're using an older version of Python (3.6 to 3.9), please use version **0.3.0** of this library, which maintains compatibility with those versions.

- **Dependencies**

  This library has no external dependencies outside of the Python Standard Library.

---

## **Installation**

You can install secure.py using pip or pipenv:

**pip**:

```bash
pip install secure
```

**Pipenv**:

```bash
pipenv install secure
```

---

## **Getting Started**

Once installed, you can quickly integrate `secure.py` into your project:

### Synchronous Usage

```python
import secure

# Initialize secure headers
secure_headers = secure.Secure()

# Apply the headers to your framework response object
secure_headers.set_headers(response)
```

### Asynchronous Usage

For frameworks like **FastAPI** and **Starlette** that support asynchronous operations, use the async method:

```python
import secure

# Initialize secure headers
secure_headers = secure.Secure()

# Apply the headers asynchronously to your framework response object
await secure_headers.set_headers_async(response)
```

### **Example Usage**

```python
import secure

secure_headers = secure.Secure()

# Apply default secure headers to a response object
secure_headers.set_headers(response)
```

---

## **Default Secure Headers**

By default, `secure.py` applies the following headers:

```http
strict-transport-security: max-age=63072000; includeSubdomains
x-frame-options: SAMEORIGIN
x-content-type-options: nosniff
referrer-policy: no-referrer, strict-origin-when-cross-origin
cache-control: no-store
```

---

## **Policy Builders**

`secure.py` allows you to customize headers such as **Content-Security-Policy** with ease:

### **Content-Security-Policy Example**

```python
import secure

# Build a custom CSP policy
csp = (
    secure.ContentSecurityPolicy()
    .default_src("'none'")
    .base_uri("'self'")
    .connect_src("'self'", "api.example.com")
    .frame_src("'none'")
    .img_src("'self'", "static.example.com")
)

# Apply it to secure headers
secure_headers = secure.Secure(csp=csp)
```

**Resulting HTTP headers:**

```http
strict-transport-security: max-age=63072000; includeSubdomains
x-frame-options: SAMEORIGIN
x-content-type-options: nosniff
referrer-policy: no-referrer, strict-origin-when-cross-origin
cache-control: no-store
content-security-policy: default-src 'none'; base-uri 'self'; connect-src 'self' api.example.com; frame-src 'none'; img-src 'self' static.example.com
```

---

## **Framework Example: FastAPI**

Here's how you can use `secure.py` with **FastAPI**:

```python
import uvicorn
from fastapi import FastAPI
import secure

app = FastAPI()

# Define security headers
secure_headers = secure.Secure(
    server=secure.Server().set("Secure"),
    csp=secure.ContentSecurityPolicy().default_src("'none'").img_src("'self'", "static.example.com"),
    hsts=secure.StrictTransportSecurity().include_subdomains().preload().max_age(2592000),
    referrer=secure.ReferrerPolicy().no_referrer(),
    permissions=secure.PermissionsPolicy().geolocation("self", "'example.com'").vibrate(),
    cache=secure.CacheControl().must_revalidate(),
)

# Apply headers middleware
@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    await secure_headers.set_headers_async(response)  # Use async version
    return response

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, port=8081, host="localhost")
```

**Resulting HTTP headers:**

```http
server: Secure
strict-transport-security: includeSubDomains; preload; max-age=2592000
x-frame-options: SAMEORIGIN
x-content-type-options: nosniff
content-security-policy: default-src 'none'; img-src 'self' static.example.com
referrer-policy: no-referrer
cache-control: must-revalidate
permissions-policy: geolocation=(self 'example.com'), vibrate=()
```

---

## **Documentation**

For more details, including advanced configurations and integration examples, please visit the **[full documentation](https://secure.readthedocs.io)**.

---

## **Resources**

- [OWASP - Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
- [MDN Web Docs: Security Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#security)
- [web.dev: Security Best Practices](https://web.dev)
- [The World Wide Web Consortium (W3C)](https://www.w3.org)

---

### **License**

This project is licensed under the terms of the **[MIT License](https://opensource.org/licenses/MIT)**.

---

## **Contributing**

Contributions are welcome! If you'd like to contribute to `secure.py`, please feel free to open an issue or submit a pull request on **[GitHub](https://github.com/TypeError/secure)**.
