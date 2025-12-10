# secure

A small, focused library for adding modern security headers to Python web applications.

[![PyPI Version](https://img.shields.io/pypi/v/secure.svg)](https://pypi.org/project/secure/)
[![Python Versions](https://img.shields.io/pypi/pyversions/secure.svg)](https://pypi.org/project/secure/)
[![License](https://img.shields.io/pypi/l/secure.svg)](https://github.com/TypeError/secure/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/TypeError/secure.svg)](https://github.com/TypeError/secure/stargazers)

---

## Introduction

Security headers are one of the simplest ways to raise the security bar for a web application, but they are often applied inconsistently across frameworks and deployments.

`secure` gives you a single, modern, well typed API for configuring and applying HTTP security headers in Python. It focuses on:

- Good defaults that are safe to adopt.
- A small, explicit API instead of a large framework.
- Support for both synchronous and asynchronous response objects.
- Framework agnostic integration so you can use the same configuration everywhere.

The package is published on PyPI as `secure` and imported with:

```python
import secure
```

---

## Why use `secure`

- Apply essential security headers with a few lines of code.
- Share one configuration across multiple frameworks and applications.
- Start from secure presets, then customize as your needs grow.
- Keep header logic out of your views and handlers.
- Use one library for FastAPI, Starlette, Flask, Django, and more.
- Rely on modern Python 3.10+ features and full type hints for better editor support.

If you want your app to ship with a strong security baseline without pulling in a heavyweight dependency, `secure` is designed for you.

---

## Supported frameworks

`secure` integrates with a range of popular Python web frameworks. The core API is framework independent, and each framework uses the same `Secure` object and methods.

| Framework                                             | Documentation                                                                                    |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| [aiohttp](https://docs.aiohttp.org)                   | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#aiohttp)    |
| [Bottle](https://bottlepy.org)                        | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#bottle)     |
| [CherryPy](https://cherrypy.dev/)                     | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#cherrypy)   |
| [Django](https://www.djangoproject.com)               | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#django)     |
| [Falcon](https://falconframework.org)                 | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#falcon)     |
| [FastAPI](https://fastapi.tiangolo.com)               | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#fastapi)    |
| [Flask](http://flask.pocoo.org)                       | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#flask)      |
| [Masonite](https://docs.masoniteproject.com/)         | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#masonite)   |
| [Morepath](https://morepath.readthedocs.io)           | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#morepath)   |
| [Pyramid](https://trypyramid.com)                     | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#pyramid)    |
| [Quart](https://quart.palletsprojects.com/en/latest/) | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#quart)      |
| [Responder](https://responder.kennethreitz.org/)      | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#responder)  |
| [Sanic](https://sanicframework.org)                   | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#sanic)      |
| [Starlette](https://www.starlette.io/)                | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#starlette)  |
| [Tornado](https://www.tornadoweb.org/)                | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#tornado)    |
| [TurboGears](https://turbogears.org/)                 | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#turbogears) |

---

## Features

- **Secure headers**  
  Apply headers like `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, and more.

- **Presets with secure defaults**  
  Start from opinionated presets like `Preset.BASIC` and `Preset.STRICT`, then customize as needed.

- **Policy builders**  
  Compose complex policies such as CSP and Permissions Policy through a fluent API.

- **Framework agnostic**  
  Works with sync and async response objects and does not depend on any single framework.

- **Zero external dependencies**  
  Easy to audit and suitable for security sensitive environments.

- **Modern Python design**  
  Uses Python 3.10+ features and full type hints so your editor and type checker can help you.

---

## Requirements

- **Python 3.10 or higher**

  `secure` targets modern Python and is currently tested on Python 3.10 through 3.13.

  It uses features introduced in Python 3.10, including:

  - Union type operator (`|`) for cleaner type annotations.
  - Structural pattern matching (`match`).
  - Improved typing and annotations.
  - `functools.cached_property` for efficient lazy computation.

  If you need support for Python 3.6 through 3.9, use version `0.3.0` of the library.

- **Dependencies**

  This library has no external dependencies outside of the Python standard library.

---

## Installation

You can install `secure` with your preferred Python package manager.

### Using `uv`

```bash
uv add secure
```

### Using `pip`

```bash
pip install secure
```

---

## Quick start

The core entry point is the `Secure` class. A typical simple setup looks like this:

```python
import secure

secure_headers = secure.Secure.with_default_headers()

# For a synchronous framework
secure_headers.set_headers(response)

# For an asynchronous framework
await secure_headers.set_headers_async(response)
```

`Secure.with_default_headers()` is equivalent to `Secure.from_preset(Preset.BASIC)`.

`set_headers` and `set_headers_async` both operate on a response object that either:

- Exposes a `set_header(name, value)` method, or
- Exposes a mutable `headers` mapping that supports item assignment.

If your framework uses a different contract, see the framework specific guides or use `header_items()` to apply headers manually.

---

## Default secure headers

When you call `Secure.with_default_headers()` (or `Secure.from_preset(Preset.BASIC)`), `secure` configures a balanced, modern set of headers suitable for many applications:

```http
Cross-Origin-Opener-Policy: same-origin
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'
Strict-Transport-Security: max-age=31536000
Permissions-Policy: geolocation=(), microphone=(), camera=()
Referrer-Policy: strict-origin-when-cross-origin
Server:
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
```

These defaults help limit cross origin data leaks, mitigate clickjacking and MIME sniffing, and establish a conservative Content Security Policy you can extend later.

---

## Presets

If you prefer to think in terms of profiles instead of individual headers, `secure` provides presets via the `Preset` enum and `Secure.from_preset`.

```python
import secure
from secure import Preset

# A balanced starting point for most applications
secure_headers = secure.Secure.from_preset(Preset.BASIC)

# A stricter profile for security focused deployments
strict_headers = secure.Secure.from_preset(Preset.STRICT)
```

### BASIC preset

The `BASIC` preset is a balanced default that matches `Secure.with_default_headers()`. It configures a modern baseline that works for many applications:

```http
Cross-Origin-Opener-Policy: same-origin
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'
Strict-Transport-Security: max-age=31536000
Permissions-Policy: geolocation=(), microphone=(), camera=()
Referrer-Policy: strict-origin-when-cross-origin
Server:
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
```

Use this when you want a strong starting point that you can refine over time.

### STRICT preset

The `STRICT` preset enables stronger protections and is a better fit for security focused deployments that can tolerate tighter restrictions. It is conceptually similar to:

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

Start with `BASIC` and move to `STRICT` once you have validated that your application works correctly with the stricter Content Security Policy, caching, and frame restrictions.

---

## Policy builders

`secure` lets you build rich header values through small, focused builder classes. Two common examples are `ContentSecurityPolicy` and `PermissionsPolicy`.

### Content Security Policy

```python
import secure

csp = (
    secure.ContentSecurityPolicy()
    .default_src("'self'")
    .script_src("'self'", "cdn.typeerror.com")
    .style_src("'unsafe-inline'")
    .img_src("'self'", "images.typeerror.com")
    .connect_src("'self'", "api.typeerror.com")
)

secure_headers = secure.Secure(csp=csp)
```

Resulting header:

```http
Content-Security-Policy: default-src 'self'; script-src 'self' cdn.typeerror.com; style-src 'unsafe-inline'; img-src 'self' images.typeerror.com; connect-src 'self' api.typeerror.com
```

You can treat the CSP builder as a safe string builder for CSP directives and keep all CSP logic in one place.

### Permissions Policy

```python
import secure

permissions = (
    secure.PermissionsPolicy()
    .geolocation("'self'")
    .camera("'none'")
    .microphone("'none'")
)

secure_headers = secure.Secure(permissions=permissions)
```

Resulting header:

```http
Permissions-Policy: geolocation=('self'), camera=('none'), microphone=('none')
```

Other headers, such as `StrictTransportSecurity`, `CrossOriginOpenerPolicy`, `CrossOriginEmbedderPolicy`, `ReferrerPolicy`, `Server`, and `XFrameOptions`, also have small builder classes that mirror their directive structure.

---

## Advanced usage: header pipeline and validation

For most applications, it is enough to construct a `Secure` instance and call `set_headers` or `set_headers_async`. If you want stronger guarantees and clearer failure modes, you can run headers through an explicit pipeline.

```python
import logging
import secure

logger = logging.getLogger("secure")

secure_headers = (
    secure.Secure.with_default_headers()
    .allowlist_headers(
        allowed=secure.DEFAULT_ALLOWED_HEADERS,
        allow_extra=["X-My-App-Header"],
        on_unexpected="warn",      # "raise" (default), "drop", or "warn"
        allow_x_prefixed=False,
        logger=logger,
    )
    .deduplicate_headers(
        action="raise",            # "raise" (default), "first", "last", or "concat"
        comma_join_ok=secure.COMMA_JOIN_OK,
        multi_ok=secure.MULTI_OK,
        logger=logger,
    )
    .validate_and_normalize_headers(
        on_invalid="drop",         # "drop" (default), "warn", or "raise"
        strict=False,
        allow_obs_text=False,
        logger=logger,
    )
)
```

Key ideas:

- `allowlist_headers` enforces a case insensitive allowlist of header names and decides what to do with unexpected headers.
- `deduplicate_headers` resolves repeated header names so that you end up with clean `name, value` pairs.
- `validate_and_normalize_headers` validates header names and values, then freezes them into a single valued, immutable mapping exposed via the `.headers` property.

If you need to emit multi valued headers, such as multiple `Set-Cookie` fields, you can bypass the single valued mapping and work with `header_items()` directly:

```python
for name, value in secure_headers.header_items():
    response.headers.add(name, value)
```

This pipeline gives you a repeatable, testable flow for going from high level policy objects to concrete headers on the wire.

---

## Framework examples

Below are simple examples for a synchronous and an asynchronous framework. See the framework specific guides for more detailed patterns.

### FastAPI

```python
from fastapi import FastAPI

from secure import Secure

app = FastAPI()
secure_headers = Secure.with_default_headers()


@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    await secure_headers.set_headers_async(response)
    return response


@app.get("/")
def read_root():
    return {"hello": "world"}
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

## Error handling and logging

`secure` is designed to fail fast and clearly when something is misconfigured, with hooks for logging and diagnostics.

### Applying headers

`set_headers` and `set_headers_async` may raise:

- `HeaderSetError` when the underlying response object refuses a header or an unexpected error occurs while setting one.
- `AttributeError` when the response object implements neither `set_header(name, value)` nor a mutable `headers` mapping.
- `RuntimeError` from `set_headers` if it detects that the only available setter is asynchronous. In that case, use `set_headers_async` instead.

### Validation helpers

The pipeline methods may raise `ValueError` when configured to do so:

- `allowlist_headers` with `on_unexpected="raise"` when encountering an unexpected header name.
- `deduplicate_headers` with `action="raise"` when it cannot safely resolve duplicates.
- `validate_and_normalize_headers` with `on_invalid="raise"` or when it detects invalid or duplicate entries during normalization.

Passing a `logger` into these methods is recommended in production so you can see which headers were rejected and why, even when you choose `"drop"` or `"warn"` modes instead of raising.

---

## Documentation

For additional examples, framework specific helpers, and more detailed guidance, see the documentation in the `docs` directory:

- Configuration details.
- Framework integration notes.
- Reference for header builder classes.

Documentation: <https://github.com/TypeError/secure/tree/main/docs>

---

## Attribution

`secure` implements recommendations from widely used security resources:

- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) (licensed under [CC-BY-SA 2.5](https://creativecommons.org/licenses/by-sa/2.5/))
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/) (licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/))

Attribution comments are included in the source code where appropriate.

---

## Resources

- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
- [MDN Web Docs: HTTP Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
- [web.dev security guidance](https://web.dev)
- [W3C](https://www.w3.org)

---

## License

This project is licensed under the terms of the [MIT License](https://opensource.org/licenses/MIT).

---

## Contributing

Issues and pull requests are welcome. If you would like to discuss an idea, open an issue on GitHub so we can talk about the design before implementation.

Repository: <https://github.com/TypeError/secure>

---

## Changelog

See the [CHANGELOG](https://github.com/TypeError/secure/blob/main/CHANGELOG.md) for a detailed list of changes by release.

---

## Acknowledgements

Thank you to everyone who contributes ideas, issues, pull requests, and feedback, as well as the maintainers of MDN and OWASP resources that this project builds on.
