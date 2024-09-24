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

| Framework                                     | Documentation                                        |
| --------------------------------------------- | ---------------------------------------------------- |
| [aiohttp](https://docs.aiohttp.org)           | [Integration Guide](./docs/frameworks.md#aiohttp)    |
| [Bottle](https://bottlepy.org)                | [Integration Guide](./docs/frameworks.md#bottle)     |
| [CherryPy](https://cherrypy.org)              | [Integration Guide](./docs/frameworks.md#cherrypy)   |
| [Django](https://www.djangoproject.com)       | [Integration Guide](./docs/frameworks.md#django)     |
| [Falcon](https://falconframework.org)         | [Integration Guide](./docs/frameworks.md#falcon)     |
| [FastAPI](https://fastapi.tiangolo.com)       | [Integration Guide](./docs/frameworks.md#fastapi)    |
| [Flask](http://flask.pocoo.org)               | [Integration Guide](./docs/frameworks.md#flask)      |
| [Masonite](https://docs.masoniteproject.com/) | [Integration Guide](./docs/frameworks.md#masonite)   |
| [Morepath](https://morepath.readthedocs.io)   | [Integration Guide](./docs/frameworks.md#morepath)   |
| [Pyramid](https://trypyramid.com)             | [Integration Guide](./docs/frameworks.md#pyramid)    |
| [Quart](https://pgjones.gitlab.io/quart/)     | [Integration Guide](./docs/frameworks.md#quart)      |
| [Responder](https://python-responder.org)     | [Integration Guide](./docs/frameworks.md#responder)  |
| [Sanic](https://sanicframework.org)           | [Integration Guide](./docs/frameworks.md#sanic)      |
| [Starlette](https://www.starlette.io/)        | [Integration Guide](./docs/frameworks.md#starlette)  |
| [Tornado](https://www.tornadoweb.org/)        | [Integration Guide](./docs/frameworks.md#tornado)    |
| [TurboGears](https://turbogears.org/)         | [Integration Guide](./docs/frameworks.md#turbogears) |

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
Cache-Control: no-store
Cross-Origin-Opener-Policy: same-origin
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'
Strict-Transport-Security: max-age=31536000
Permissions-Policy: geolocation=(), microphone=(), camera=()
Referrer-Policy: strict-origin-when-cross-origin
Server:
X-Content-Type-Options: nosniff
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
Content-Security-Policy: default-src 'self'; script-src 'self' cdn.example.com; style-src 'self' cdn.example.com; img-src 'self' images.example.com; connect-src 'self' api.example.com
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
Permissions-Policy: geolocation=('self'), camera=('none'), microphone=('none')
```

---

## **Framework Examples**

### **FastAPI**

```python
from fastapi import FastAPI

from secure import Secure

app = FastAPI()
secure_headers = Secure.with_default_headers()


@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    secure_headers.set_headers(response)
    return response


@app.get("/")
def read_root():
    return {"Hello": "World"}
```

### Flask

```python
from flask import Flask, Response

from secure import Secure

app = Flask(__name__)
secure_headers = Secure.with_default_headers()


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
