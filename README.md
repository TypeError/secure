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
| [Dash](https://dash.plotly.com/)                      | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#dash)       |
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
| [Shiny](https://shiny.posit.co/py/)                   | [Integration Guide](https://github.com/TypeError/secure/blob/main/docs/frameworks.md#shiny)      |
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

`Secure.with_default_headers()` is equivalent to `Secure.from_preset(Preset.BALANCED)`, the recommended default profile.

`set_headers` and `set_headers_async` both operate on a response object that either:

- Exposes a `set_header(name, value)` method, or
- Exposes a mutable `headers` mapping that supports item assignment.

If your framework uses a different contract, see the framework specific guides or use `header_items()` to apply headers manually.

## Middleware

`secure.middleware` re-exports `SecureWSGIMiddleware` and `SecureASGIMiddleware`. Each middleware accepts a `Secure` instance (defaulting to `Secure.with_default_headers()`), overwrites headers by default, and only appends duplicates when a normalized name is included in `multi_ok` (the default `secure.MULTI_OK` includes `Content-Security-Policy`).

### WSGI (Flask + Django)

Wrap any WSGI stack with `SecureWSGIMiddleware`, and pass a configured `Secure` instance if you need a custom CSP or additional headers.

```python
from flask import Flask
from secure import Secure
from secure.middleware import SecureWSGIMiddleware

secure_headers = Secure.with_default_headers()
app = Flask(__name__)
app.wsgi_app = SecureWSGIMiddleware(app.wsgi_app, secure=secure_headers)
```

For Django, apply the headers through a middleware class since Django’s middleware pipeline wraps requests and responses rather than the raw WSGI callable:

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

Register the class in your `MIDDLEWARE` setting to enforce security headers on every response.

### ASGI (FastAPI + Shiny for Python)

`SecureASGIMiddleware` modifies only HTTP scopes (WebSocket messages pass through untouched). Mount it manually or via FastAPI’s `add_middleware`, and pass any `Secure` instance if you need to adjust the defaults.

```python
from fastapi import FastAPI
from secure import Secure
from secure.middleware import SecureASGIMiddleware

secure_headers = Secure.with_default_headers()
app = FastAPI()
app.add_middleware(SecureASGIMiddleware, secure=secure_headers)
```

If you need to tailor the CSP, build a custom `Secure` instance before wiring the middleware:

```python
from secure import ContentSecurityPolicy

secure_headers = Secure(
    csp=ContentSecurityPolicy().default_src("'self'").script_src("https://trusted.cdn")
)
app = SecureASGIMiddleware(app, secure=secure_headers)
```

Shiny for Python apps can be wrapped in the same way:

```python
from shiny import App
from secure import Secure
from secure.middleware import SecureASGIMiddleware

secure_headers = Secure.with_default_headers()
app = SecureASGIMiddleware(App(), secure=secure_headers)
```

### Customizing `multi_ok`

Pass the `multi_ok` argument to either middleware to append additional occurrences of headers that must appear multiple times (for example, when downstream code already emits a `Content-Security-Policy` line).

---

## Default secure headers

When you call `Secure.with_default_headers()` (or `Secure.from_preset(Preset.BALANCED)`), `secure` configures the recommended defaults that balance security and usability:

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

These defaults limit cross origin data leaks, mitigate clickjacking and MIME sniffing, and enforce a conservative Content Security Policy you can extend later. Balanced omits `Cache-Control` as well as the legacy/compatibility headers (`X-Permitted-Cross-Domain-Policies`, `X-DNS-Prefetch-Control`, `Origin-Agent-Cluster`, `X-Download-Options`, `X-XSS-Protection`), so add them manually if your deployment still depends on them.

---

## Presets

If you prefer to think in terms of profiles instead of individual headers, `secure` provides presets via the `Preset` enum and `Secure.from_preset`.

```python
from secure import Preset, Secure

# Recommended defaults for most applications
balanced_headers = Secure.from_preset(Preset.BALANCED)

# Helmet-parity defaults for compatibility-focused setups
basic_headers = Secure.from_preset(Preset.BASIC)

# Hardened defaults for security-focused deployments
strict_headers = Secure.from_preset(Preset.STRICT)
```

### BALANCED preset

The `BALANCED` preset is the new recommended default and matches `Secure.with_default_headers()`. It balances security with compatibility while keeping response headers relatively tight:

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

Balanced omits `Cache-Control` and the legacy/resource headers included by `Preset.BASIC`, but you can still add them manually if your deployment relies on them.

### BASIC preset

The `BASIC` preset matches Helmet.js defaults and ships with a broader compatibility-focused header set. It is useful when you require the same collection of headers Helmet enables out of the box:

```http
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Resource-Policy: same-origin
Content-Security-Policy: default-src 'self'; base-uri 'self'; font-src 'self' https: data:; form-action 'self'; frame-ancestors 'self'; img-src 'self' data:; object-src 'none'; script-src 'self'; script-src-attr 'none'; style-src 'self' https: 'unsafe-inline'; upgrade-insecure-requests
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: no-referrer
X-Permitted-Cross-Domain-Policies: none
X-DNS-Prefetch-Control: off
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Origin-Agent-Cluster: ?1
X-Download-Options: noopen
X-XSS-Protection: 0
```

This preset still avoids `Cache-Control` and `Server` but includes the extra headers that Helmet adds for historical/compatibility reasons.

### STRICT preset

The `STRICT` preset enables stronger protections and is a better fit for security focused deployments that can tolerate tighter restrictions. It is conceptually similar to:

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

Start with `BALANCED` and move to `STRICT` once you have validated that your application works correctly with the stricter Content Security Policy, caching, and frame restrictions. `STRICT` no longer sets HSTS preload by default, so you can opt-in separately when you are ready.

---

## Policy builders

`secure` lets you build rich header values through small, focused builder classes. Two common examples are `ContentSecurityPolicy` and `PermissionsPolicy`.

### Content Security Policy

```python
from secure import Secure
from secure.headers import ContentSecurityPolicy

csp = (
    ContentSecurityPolicy()
    .default_src("'self'")
    .script_src("'self'", "cdn.typeerror.com")
    .style_src("'unsafe-inline'")
    .img_src("'self'", "images.typeerror.com")
    .connect_src("'self'", "api.typeerror.com")
)

secure_headers = Secure(csp=csp)
```

Resulting header:

```http
Content-Security-Policy: default-src 'self'; script-src 'self' cdn.typeerror.com; style-src 'unsafe-inline'; img-src 'self' images.typeerror.com; connect-src 'self' api.typeerror.com
```

You can treat the CSP builder as a safe string builder for CSP directives and keep all CSP logic in one place.

### Permissions Policy

```python
from secure import Secure
from secure.headers import PermissionsPolicy

permissions = (
    PermissionsPolicy().geolocation("'self'").camera("'none'").microphone("'none'")
)

secure_headers = Secure(permissions=permissions)
```

Resulting header:

```http
Permissions-Policy: geolocation=(self), camera=(), microphone=()
```

Other headers, such as `StrictTransportSecurity`, `CrossOriginOpenerPolicy`, `CrossOriginEmbedderPolicy`, `ReferrerPolicy`, `Server`, and `XFrameOptions`, also have small builder classes that mirror their directive structure.

---

## Advanced usage: header pipeline and validation

For most applications, it is enough to construct a `Secure` instance and call `set_headers` or `set_headers_async`. If you want stronger guarantees and clearer failure modes, you can run headers through an explicit pipeline.

```python
import logging

from secure import COMMA_JOIN_OK, DEFAULT_ALLOWED_HEADERS, MULTI_OK, Secure

logger = logging.getLogger("secure")

secure_headers = (
    Secure.with_default_headers()
    .allowlist_headers(
        allowed=DEFAULT_ALLOWED_HEADERS,
        allow_extra=["X-My-App-Header"],
        on_unexpected="warn",  # "raise" (default), "drop", or "warn"
        allow_x_prefixed=False,
        logger=logger,
    )
    .deduplicate_headers(
        action="raise",  # "raise" (default), "first", "last", or "concat"
        comma_join_ok=COMMA_JOIN_OK,
        multi_ok=MULTI_OK,
        logger=logger,
    )
    .validate_and_normalize_headers(
        on_invalid="drop",  # "drop" (default), "warn", or "raise"
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
- After the pipeline runs through `validate_and_normalize_headers()`, `Secure` uses the normalized `.headers` mapping when `set_headers` or `set_headers_async` apply the headers, ensuring dropped entries never reach the wire and sanitized values replace unsafe input.

If you need to emit multi valued headers, such as multiple `Set-Cookie` fields, you can bypass the single valued mapping and work with `header_items()` directly:

```python
for name, value in secure_headers.header_items():
    response.headers.add(name, value)
```

This pipeline gives you a repeatable, testable flow for going from high level policy objects to concrete headers on the wire.

---

## Framework examples

Below are simple examples for a synchronous and an asynchronous framework. See the framework specific guides for more detailed patterns.

### Shiny for Python

#### Recommended: ASGI middleware wrapper

Wraps the Shiny ASGI application and injects headers by intercepting the ASGI `http.response.start` message.

```python
from secure import Secure
from secure.middleware import SecureASGIMiddleware
from shiny import App, ui

secure_headers = Secure.with_default_headers()

app_ui = ui.page_fluid("Hello Shiny!")


def server(input, output, session):
    pass


app = App(app_ui, server)

app = SecureASGIMiddleware(app, secure=secure_headers)
```

### FastAPI

#### Recommended: `add_middleware` (ASGI)

Injects headers by intercepting the ASGI `http.response.start` message.

```python
from fastapi import FastAPI
from secure import Secure
from secure.middleware import SecureASGIMiddleware

app = FastAPI()
secure_headers = Secure.with_default_headers()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.add_middleware(SecureASGIMiddleware, secure=secure_headers)
```

#### Alternative: route-level hook (@app.middleware("http"))

Applies headers directly to the response object returned by `call_next`.

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
    return {"Hello": "World"}
```

### Starlette

#### Recommended: `add_middleware` (ASGI)

```python
from secure import Secure
from secure.middleware import SecureASGIMiddleware
from starlette.applications import Starlette
from starlette.responses import JSONResponse

secure_headers = Secure.with_default_headers()

app = Starlette()
app.add_middleware(SecureASGIMiddleware, secure=secure_headers)


@app.route("/")
async def read_root(request):
    return JSONResponse({"hello": "world"})
```

### Flask

#### Recommended: `after_request` hook

Applies headers directly to the Flask `Response` object.

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

#### Alternative: WSGI middleware (`app.wsgi_app`)

Wraps the WSGI application and injects headers by wrapping `start_response`.
Useful for deployment-level / framework-agnostic WSGI setups.

```python
from flask import Flask
from secure import Secure
from secure.middleware.wsgi import SecureWSGIMiddleware

app = Flask(__name__)
secure_headers = Secure.with_default_headers()


@app.get("/")
def home():
    return {"Hello": "World"}


app.wsgi_app = SecureWSGIMiddleware(app.wsgi_app, secure=secure_headers)

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
- Migration notes for the v2.0.0 release and preset/default changes: <https://github.com/TypeError/secure/tree/main/docs/migration.md>

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

Issues and pull requests are welcome. If you’d like to discuss an idea, please open a GitHub issue so we can align on the design before implementation. See [CONTRIBUTING](https://github.com/TypeError/secure/blob/main/CONTRIBUTING.md) for details.

---

## Code of Conduct

See [CODE_OF_CONDUCT](https://github.com/TypeError/secure/blob/main/CODE_OF_CONDUCT.md) for our Code of Conduct.

---

## Changelog

See [CHANGELOG](https://github.com/TypeError/secure/blob/main/CHANGELOG.md) for a detailed list of changes by release.

---

## Acknowledgements

Thank you to everyone who contributes ideas, issues, pull requests, and feedback, as well as the maintainers of MDN and OWASP resources that this project builds on.
