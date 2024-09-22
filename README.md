# secure.py

_A simple, yet powerful way to secure your Python web applications across multiple frameworks._

[![PyPI Version](https://img.shields.io/pypi/v/secure.svg)](https://pypi.org/project/secure/)
[![Python Versions](https://img.shields.io/pypi/pyversions/secure.svg)](https://pypi.org/project/secure/)
[![Downloads](https://pepy.tech/badge/secure)](https://pepy.tech/project/secure)
[![License](https://img.shields.io/pypi/l/secure.svg)](https://github.com/TypeError/secure/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/TypeError/secure.svg)](https://github.com/TypeError/secure/stargazers)

## **Introduction**

In today's web landscape, security is paramount. **secure.py** is a lightweight Python library designed to effortlessly add **security headers** to your web applications, protecting them from common vulnerabilities. Whether you're using **Django**, **Flask**, **FastAPI**, or any other popular framework, `secure.py` provides a unified API to enhance your application's security posture.

---

## **Why Use secure.py?**

- 🔒 **Apply Essential Security Headers**: Implement headers like CSP, HSTS, and more with minimal effort.
- 🛠️ **Consistent API Across Frameworks**: A unified approach for different web frameworks.
- ⚙️ **Customizable with Secure Defaults**: Start secure out-of-the-box and customize as needed.
- 🚀 **Easy Integration**: Compatible with Python's most-used frameworks.
- 🐍 **Modern Pythonic Design**: Leverages Python 3.10+ features for cleaner and more efficient code.

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

- 🔒 **Secure Headers**: Automatically apply headers like `Strict-Transport-Security`, `X-Frame-Options`, and more.
- 🛠️ **Customizable Policies**: Flexibly build your own security policies using method chaining.
- 🌐 **Framework Integration**: Compatible with various frameworks, ensuring cross-compatibility.
- 🚀 **No External Dependencies**: Lightweight and easy to include in any project.
- 🧩 **Easy to Use**: Integrate security headers in just a few lines of code.
- ⚡ **Asynchronous Support**: Async support for modern frameworks like **FastAPI** and **Starlette**.
- 📝 **Enhanced Type Hinting**: Complete type annotations for better developer experience.
- 📚 **Attribution to Trusted Sources**: Implements recommendations from MDN and OWASP.

---

## **Requirements**

- **Python 3.10** or higher

  This library leverages modern Python features introduced in Python 3.10 and 3.11, such as:

  - **Union Type Operator (`|`)**: Simplifies type annotations.
  - **Structural Pattern Matching (`match` statement)**: Enhances control flow.
  - **Improved Type Hinting and Annotations**: Provides better code clarity and maintenance.
  - **`cached_property`**: Optimize memory usage and performance.

  **Note:** If you're using an older version of Python (3.6 to 3.9), please use version **0.3.0** of this library, which maintains compatibility with those versions.

- **Dependencies**

  This library has no external dependencies outside of the Python Standard Library.

---

## **Installation**

You can install secure.py using pip, pipenv, or poetry:

**pip**:

```bash
pip install secure
```

**Pipenv**:

```bash
pipenv install secure
```

**Poetry**:

```bash
poetry add secure
```

---

## **Getting Started**

Once installed, you can quickly integrate `secure.py` into your project:

### Synchronous Usage

```python
import secure

# Initialize secure headers with default settings
secure_headers = secure.Secure.with_default_headers()

# Apply the headers to your framework response object
secure_headers.set_headers(response)
```

### Asynchronous Usage

For frameworks like **FastAPI** and **Starlette** that support asynchronous operations, use the async method:

```python
import secure

# Initialize secure headers with default settings
secure_headers = secure.Secure.with_default_headers()

# Apply the headers asynchronously to your framework response object
await secure_headers.set_headers_async(response)
```

### **Example Usage**

```python
import secure

# Create a Secure instance with default headers
secure_headers = secure.Secure.with_default_headers()

# Apply default secure headers to a response object
secure_headers.set_headers(response)
```

---

## **Default Secure Headers**

By default, `secure.py` applies the following headers when using `with_default_headers()`:

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Content-Security-Policy: default-src 'self'
Referrer-Policy: no-referrer-when-downgrade
Permissions-Policy: camera=(), microphone=()
```

---

## **Policy Builders**

`secure.py` allows you to customize headers such as **Content-Security-Policy** and **Permissions-Policy** with ease:

### **Content-Security-Policy Example**

```python
import secure

# Build a custom CSP policy
csp = (
    secure.ContentSecurityPolicy()
    .default_src("'self'")
    .script_src("'self'", "cdn.example.com")
    .style_src("'self'", "cdn.example.com")
    .img_src("'self'", "images.example.com")
    .connect_src("'self'", "api.example.com")
)

# Apply it to secure headers
secure_headers = secure.Secure(csp=csp)
```

**Resulting HTTP headers:**

```http
content-security-policy: default-src 'self'; script-src 'self' cdn.example.com; style-src 'self' cdn.example.com; img-src 'self' images.example.com; connect-src 'self' api.example.com
```

### **Permissions-Policy Example**

```python
import secure

# Build a custom Permissions Policy
permissions = (
    secure.PermissionsPolicy()
    .geolocation("'self'")
    .camera("'none'")
    .microphone("'none'")
)

# Apply it to secure headers
secure_headers = secure.Secure(permissions=permissions)
```

**Resulting HTTP headers:**

```http
permissions-policy: geolocation=('self'), camera=(), microphone=()
```

---

## **Framework Examples**

### **FastAPI**

```python
import uvicorn
from fastapi import FastAPI
import secure

app = FastAPI()

# Define security headers
secure_headers = secure.Secure()

# Apply headers middleware
@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    await secure_headers.set_headers_async(response)
    return response

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run(app, port=8081, host="localhost")
```

### **Django**

```python
# settings.py
import secure

secure_headers = secure.Secure()

MIDDLEWARE = [
    # ... other middleware ...
    'your_project.middleware.SecureHeadersMiddleware',
]

# your_project/middleware.py
from django.utils.deprecation import MiddlewareMixin

class SecureHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        secure_headers.set_headers(response)
        return response
```

### Flask

```python
from flask import Flask
import secure

app = Flask(__name__)
secure_headers = secure.Secure()

@app.after_request
def set_secure_headers(response):
    secure_headers.set_headers(response)
    return response

@app.route('/')
def index():
    return 'Hello, World!'

```

---

## **Documentation**

For more details, including advanced configurations and integration examples, please visit the **[full documentation](https://github.com/TypeError/secure/tree/main/docs)**.

---

## **Attribution**

This library implements security recommendations from trusted sources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))

We have included attribution comments in the source code where appropriate.

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

---

## **Changelog**

For a detailed list of changes, please refer to the **[CHANGELOG](https://github.com/TypeError/secure/blob/main/CHANGELOG.md)**.

---

## **Acknowledgements**

We would like to thank the contributors of MDN Web Docs and OWASP Secure Headers Project for their invaluable resources and guidelines that help make the web a safer place.
