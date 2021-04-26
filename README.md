# secure.py

[![image](https://img.shields.io/pypi/v/secure.svg)](https://pypi.org/project/secure/)
[![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/)
[![image](https://img.shields.io/pypi/l/secure.svg)](https://pypi.org/project/secure/)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build Status](https://travis-ci.org/TypeError/secure.svg?branch=master)](https://travis-ci.org/TypeError/secure)

secure.py 🔒 is a lightweight package that adds optional security headers for Python web frameworks.

## Supported Python web frameworks

[aiohttp](https://docs.aiohttp.org), [Bottle](https://bottlepy.org), [CherryPy](https://cherrypy.org), [Django](https://www.djangoproject.com), [Falcon](https://falconframework.org), [FastAPI](https://fastapi.tiangolo.com), [Flask](http://flask.pocoo.org), [hug](http://www.hug.rest), [Masonite](https://docs.masoniteproject.com), [Pyramid](https://trypyramid.com), [Quart](https://pgjones.gitlab.io/quart/), [Responder](https://python-responder.org), [Sanic](https://sanicframework.org), [Starlette](https://www.starlette.io/), [Tornado](https://www.tornadoweb.org/)

## Install

**pip**:

```console
pip install secure
```

**Pipenv**:

```console
pipenv install secure
```

After installing secure:

```Python
import secure

secure_headers = secure.Secure()
```

## Secure Headers

### Example

`secure_headers.framework(response)`

**Default HTTP response headers:**

```HTTP
strict-transport-security: max-age=63072000; includeSubdomains
x-frame-options: SAMEORIGIN
x-xss-protection: 0
x-content-type-options: nosniff
referrer-policy: no-referrer, strict-origin-when-cross-origin
cache-control: no-store
```

## Policy Builders

### Policy Builder Example

**Content Security Policy builder:**

```python
    csp = (
            secure.ContentSecurityPolicy()
            .default_src("'none'")
            .base_uri("'self'")
            .connect_src("'self'", "api.spam.com")
            .frame_src("'none'")
            .img_src("'self'", "static.spam.com")
        )
        secure_headers = secure.Secure(csp=csp)
```

**HTTP response headers:**

```HTTP
strict-transport-security: max-age=63072000; includeSubdomains
x-frame-options: SAMEORIGIN
x-xss-protection: 0
x-content-type-options: nosniff
referrer-policy: no-referrer, strict-origin-when-cross-origin
cache-control: no-store
content-security-policy: default-src 'none'; base-uri 'self'; connect-src 'self' api.spam.com; frame-src 'none'; img-src 'self' static.spam.com"
```

## Documentation

Please see the full set of documentation at [https://secure.readthedocs.io](https://secure.readthedocs.io)

## FastAPI Example

```python
import uvicorn
from fastapi import FastAPI
import secure

app = FastAPI()

server = secure.Server().set("Secure")

csp = (
    secure.ContentSecurityPolicy()
    .default_src("'none'")
    .base_uri("'self'")
    .connect_src("'self'" "api.spam.com")
    .frame_src("'none'")
    .img_src("'self'", "static.spam.com")
)

hsts = secure.StrictTransportSecurity().include_subdomains().preload().max_age(2592000)

referrer = secure.ReferrerPolicy().no_referrer()

permissions_value = (
    secure.PermissionsPolicy().geolocation("self", "'spam.com'").vibrate()
)

cache_value = secure.CacheControl().must_revalidate()

secure_headers = secure.Secure(
    server=server,
    csp=csp,
    hsts=hsts,
    referrer=referrer,
    permissions=permissions_value,
    cache=cache_value,
)


@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response


@app.get("/")
async def root():
    return {"message": "Secure"}


if __name__ == "__main__":
    uvicorn.run(app, port=8081, host="localhost")
```

## Resources

- [kennethreitz/setup.py: 📦 A Human’s Ultimate Guide to setup.py.](https://github.com/kennethreitz/setup.py)
- [OWASP - Secure Headers Project](https://www.owasp.org/index.php/OWASP_Secure_Headers_Project)
- [Mozilla Web Security](https://infosec.mozilla.org/guidelines/web_security)
- [securityheaders.com](https://securityheaders.com)
- [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers#security)
- [web.dev](https://web.dev)
- [The World Wide Web Consortium (W3C)](https://www.w3.org)
