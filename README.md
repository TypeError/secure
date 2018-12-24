# secure.py

[![image](https://img.shields.io/pypi/v/secure.svg)](https://pypi.org/project/secure/)
[![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/)
[![image](https://img.shields.io/pypi/l/secure.svg)](https://pypi.org/project/secure/)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

secure.py 🔒 is a lightweight package that adds optional security headers and cookie attributes for Python web frameworks.

### Supported Python web frameworks:
[aiohttp](https://docs.aiohttp.org), [Bottle](https://bottlepy.org), [CherryPy](https://cherrypy.org), [Django](https://www.djangoproject.com), [Falcon](https://falconframework.org), [Flask](http://flask.pocoo.org), [hug](http://www.hug.rest), [Masonite](https://docs.masoniteproject.com), [Pyramid](https://trypyramid.com), [Quart](https://pgjones.gitlab.io/quart/), [Responder](https://python-responder.org), [Sanic](https://sanicframework.org), [Starlette](https://www.starlette.io/), [Tornado](https://www.tornadoweb.org/) 


## Install
**pip**:

```console
$ pip install secure
```

**Pipenv**:

```console
$ pipenv install secure
```

After installing secure:

```Python
from secure import SecureHeaders, SecureCookie

secure_headers = SecureHeaders()
secure_cookie = SecureCookie()
```

## Secure Headers
 
 ### Example
`secure_headers.framework(response)`

 **Default HTTP response headers:** 
 
```HTTP
Strict-Transport-Security: max-age=63072000; includeSubdomains
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Referrer-Policy: no-referrer, strict-origin-when-cross-origin
Cache-control: no-cache, no-store, must-revalidate, max-age=0
Pragma: no-cache
Expires: 0
```

## Secure Cookie

### Example

```Python
secure_cookie.framework(response, name="spam", value="eggs")
```

**Default Set-Cookie HTTP response header:**   

```HTTP
Set-Cookie: spam=eggs; Path=/; secure; HttpOnly; SameSite=lax
```

## Documentation
Please see the full set of documentation at [https://secure.readthedocs.io](https://secure.readthedocs.io)

## Resources
- [kennethreitz/setup.py: 📦 A Human’s Ultimate Guide to setup.py.](https://github.com/kennethreitz/setup.py)
- [OWASP - Secure Headers Project](https://www.owasp.org/index.php/OWASP_Secure_Headers_Project)
- [OWASP - Session Management Cheat Sheet](https://www.owasp.org/index.php/Session_Management_Cheat_Sheet#Cookies)
- [Mozilla Web Security](https://infosec.mozilla.org/guidelines/web_security)
- [securityheaders.com](https://securityheaders.com)
