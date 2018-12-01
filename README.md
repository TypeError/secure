# Secure

Secure 🔒 is a lightweight package that adds optional security headers and cookie attributes for Python web frameworks.

Supported Python web frameworks:  
- [Bottle](https://bottlepy.org)  
- [CherryPy](https://cherrypy.org)  
- [Falcon](https://falconframework.org)  
- [Pyramid](https://trypyramid.com)  
- [Responder](https://python-responder.org)  
- [Sanic](https://sanicframework.org)  

Please see [flask-talisman](https://github.com/GoogleCloudPlatform/flask-talisman) for Flask support and [django-security](https://github.com/sdelements/django-security/) for Django support. 

## Install
pip:
`pip install secure`

pipenv:
`pipenv install secure`   

## Headers
 
#### Server
Contain information about server software   
**Value:** `NULL` *(obfuscate server information)*

#### Strict-Transport-Security (HSTS)
Ensure application communication is sent over HTTPS   
**Value:** `max-age=63072000; includeSubdomains`  
 
#### X-Frame-Options (XFO)
Disable framing from different origins (clickjacking defense)  
**Value:** `SAMEORIGIN`  

#### X-XSS-Protection
Enable browser cross-site scripting filters  
**Value:** `X-XSS-Protection", "1; mode=block`  

#### X-Content-Type-Options
Prevent MIME-sniffing  
**Value:** `nosniff`  

#### Content-Security-Policy (CSP)
Prevent cross-site injections  
**Value:** `script-src 'self'; object-src 'self'`  *(not included by default)**

#### Referrer-Policy
Enable full referrer if same origin, remove path for cross origin and disable referrer in unsupported browsers  
**Value:** `no-referrer, strict-origin-when-cross-origin`

#### Cache-control / Pragma
Prevent cacheable HTTPS response  
**Value:** `no-cache, no-store, must-revalidate` / `no-cache`

 **The Content-Security-Policy (CSP) header can break functionality and can (and should) be carefully constructed, use the `csp=True` option to enable default values.*


*Recommendations used by Secure 🔒 and more information regarding security headers can be found at the [OWASP Secure Headers Project](https://www.owasp.org/index.php/OWASP_Secure_Headers_Project).*
 
 ### Example
`secure.SecureHeaders.framework(response)`

 **Default HTTP response headers:** 
 
```HTTP
Server: NULL
Strict-Transport-Security: max-age=63072000; includeSubdomains
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Referrer-Policy: no-referrer, strict-origin-when-cross-origin
Cache-control: no-cache, no-store, must-revalidate
Pragma: no-cache
```

### Options

You can toggle the setting of headers with default values by passing the following options:   

- `server` - set the Server header, e.g. `Server=“Secure”` *(string / bool, default=True)*
- `hsts` - set the Strict-Transport-Security header *(bool, default=True)*  
- `xfo` - set the X-Frame-Options header *(bool, default=True)*  
- `xss` - set the X-XSS-Protection header *(bool, default=True)*  
- `content` - set the X-Content-Type-Options header *(bool, default=True)*  
- `csp` - set the Content-Security-Policy *(bool, default=False)* *  
- `referrer` - set the Referrer-Policy header *(bool, default=True)*  
- `cache` - set the Cache-control and Pragma headers *(bool, default=True)*  

####  Example

```Python
secure.SecureHeaders.framework(response, hsts=False, csp=True)
```

## Cookies
#### Path
The Path directive instructs the browser to only send the cookie if provided path exists in the URL. 

#### Secure
The Secure flag instructs the browser to only send the cookie via HTTPS.

#### HttpOnly
The HttpOnly flag instructs the browser to not allow any client side code to access the cookie's contents.

#### SameSite
The SameSite flag directs the browser not to include cookies on certain cross-site requests. There are two values that can be set for the same-site attribute, lax or strict. The lax value allows the cookie to be sent via certain cross-site GET requests, but disallows the cookie on all POST requests. For example cookies are still sent on links `<a href=“x”>`, prerendering `<link rel=“prerender” href=“x”` and forms sent by GET requests `<form-method=“get”...`, but cookies will not be sent via POST requests `<form-method=“post”...`, images `<img src=“x”>` or iframes `<iframe src=“x”>`. The strict value prevents the cookie from being sent cross-site in any context. Strict offers greater security but may impede functionality. This approach makes authenticated CSRF attacks impossible with the strict flag and only possible via state changing GET requests with the lax flag.

#### Expires
The Expires attribute sets an expiration date for persistent cookies.

### Example

```Python
secure.SecureCookie.framework(response, name="framework", value="ABC123")
```

*Default Set-Cookie HTTP response header:*   

```HTTP
Set-Cookie: framework=ABC123; Path=/; secure; HttpOnly; SameSite=lax
```

### Options

You can modify default cookie attribute values by passing the following options:   

- `name`  - set the cookie name *(string, No default value)*
- `value`  - set the cookie value *(string, No default value)*
- `path`  - set the Path attribute, e.g.`path=“/secure”` *(string, default="/")*
- `secure` - set the Secure flag *(bool, default=True)*
- `httponly` - set the HttpOnly flag *(bool, default=True)*
- `samesite` - set the SameSite attribute, e.g. `samesite=“strict”` *(bool / string, options: `"lax"`, `"strict"` or `False`, default="lax")*
- `expires` - set the Expires attribute with the cookie expiration in hours, e.g.`expires=1` *(number / bool, default=False)*

#### Example
```Python
secure.SecureCookie.framework(
        response,
        name="framework",
        value="ABC123",
        samesite=False,
        path="/secure",
        expires=24,
    )
```

# Supported Frameworks
## Bottle

#### Headers
`secure.SecureHeaders.bottle(response)`

##### Example
```Python
from bottle import route, run, response, hook
from secure import SecureHeaders

. . . 

@hook("after_request")
def set_secure_headers():
    SecureHeaders.bottle(response)
    
. . . 
```

#### Cookies
```Python
secure.SecureCookie.bottle(response, name="bottle", value="ABC123")
```

##### Example
```Python
from bottle import route, run, response, hook
from secure import SecureCookie

. . . 

@route("/secure")
def set_secure_cookie():
    SecureCookie.bottle(response, name="bottle", value="ABC123")
    return "Secure"
    
. . . 
```

## CherryPy

#### Headers
`'tools.response_headers.headers': SecureHeaders.cherrypy()`

##### Example
CherryPy [Application Configuration](http://docs.cherrypy.org/en/latest/config.html#application-config):

```Python
import cherrypy
from secure import SecureHeaders

. . . 

config = {
    '/': {
        'tools.response_headers.on': True,
        'tools.response_headers.headers': SecureHeaders.cherrypy(),
    }
}

. . . 
```

#### Cookies
```Python
response_headers = cherrypy.response.headers
secure.SecureCookie.cherrypy(response_headers, name="cherrypy", value="ABC123")
```

##### Example
```Python
import cherrypy
from secure import SecureCookie

. . . 

class SetSecureCookie(object):
    @cherrypy.expose
    def set_secure_cookie(self):
        response_headers = cherrypy.response.headers
        SecureCookie.cherrypy(response_headers, name="cherrypy", value="ABC123")
        return "Secure"
    
. . . 
```


## Falcon

#### Headers
`secure.SecureHeaders.falcon(resp)`

##### Example
```Python
import falcon
from secure import SecureHeaders

. . . 

class SetSecureHeaders(object):
    def process_request(self, req, resp):
        SecureHeaders.falcon(resp)

app = api = falcon.API(middleware=[SetSecureHeaders()])

. . . 
```

#### Cookies
```Python
secure.SecureCookie.falcon(resp, name="falcon", value="ABC123")
```

##### Example
```Python
import falcon
from secure import SecureCookie

. . . 

class SetSecureCookie(object):
    def on_get(self, req, resp):
        resp.body = "Secure"
        SecureCookie.falcon(resp, name="falcon", value="ABC123")
        
. . . 
```

## Pyramid

#### Headers
Pyramid [Tween](https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hooks.html#registering-tweens):

```Python
def set_secure_headers(handler, registry):
    def tween(request):
        response = handler(request)
        secure.SecureHeaders.pyramid(response)
        return response
        
```

##### Example
```Python
from pyramid.config import Configurator
from pyramid.response import Response
from secure import SecureHeaders

. . . 

def set_secure_headers(handler, registry):
    def tween(request):
        response = handler(request)
        SecureHeaders.pyramid(response)
        return response

    return tween

. . . 

config.add_tween(".set_secure_headers")

. . . 
```


#### Cookies
```Python
response = Response("Secure")
    secure.SecureCookie.pyramid(response, name="pyramid", value="ABC123")
```

##### Example
```Python
from pyramid.config import Configurator
from pyramid.response import Response
from secure import SecureCookie

. . . 

def set_secure_cookie(request):
    response = Response("Secure")
    SecureCookie.pyramid(response, name="pyramid", value="ABC123")
    return response
    
. . . 
```

## Responder

#### Headers
`secure.SecureHeaders.responder(resp)`

##### Example
```Python
import responder
from secure import SecureHeaders

api = responder.API()

. . . 

@api.route(before_request=True)
def set_secure_headers(req, resp):
    SecureHeaders.responder(resp)

. . . 
```

You should use Responder's [built in HSTS](https://python-responder.org/en/latest/tour.html#hsts-redirect-to-https) and pass the `hsts=False` option. 


#### Cookies
```Python
secure.SecureCookie.responder(resp, name="reponder", value="ABC123")
```

##### Example
```Python
import responder
from secure import SecureCookie

api = responder.API(cors=True)

. . . 

@api.route("/secure")
async def set_secure_cookie(req, resp):
    resp.text = "Secure"
    SecureCookie.responder(resp, name="reponder", value="ABC123")
    
. . . 
```

## Sanic

#### Headers
`secure.SecureHeaders.sanic(response)`

##### Example
```Python
from sanic import Sanic
from secure import SecureHeaders, SecureCookie

app = Sanic()

. . . 

@app.middleware('response')
async def set_secure_headers(request, response):
    SecureHeaders.sanic(response)

. . . 
```

#### Cookies
```Python
secure.SecureCookie.sanic(response, name="sanic", value="ABC123")
```

##### Example
```Python
from sanic import Sanic
from sanic.response import text

from secure import SecureHeaders, SecureCookie

app = Sanic()

. . . 

@app.route("/secure")
async def set_secure_cookie(request):
    response = text("Secure")
    SecureCookie.sanic(response, name="sanic", value="ABC123")
    return response
    
. . . 
```




## Attribution/References

#### Frameworks
- [Bottle: A fast and simple micro-framework for python web-applications.](https://github.com/bottlepy/bottle)
- [CherryPy: A pythonic, object-oriented HTTP framework.](https://github.com/cherrypy/cherrypy)
- [Falcon: A bare-metal Python web API framework for building high-performance microservices, app backends, and higher-level frameworks.](https://github.com/falconry/falcon)
- [Pyramid: aAPython web framework](https://github.com/Pylons/pyramid)
- [Sanic: An Async Python 3.5+ web server that's written to go fast](https://github.com/huge-success/sanic)  
- [Responder: A familiar HTTP Service Framework](https://python-responder.org/en/latest/)  

#### Resources
- [kennethreitz/setup.py: 📦 A Human’s Ultimate Guide to setup.py.](https://github.com/kennethreitz/setup.py)
- [OWASP -  Application Security FAQ - Browser Cache](https://www.owasp.org/index.php/OWASP_Application_Security_FAQ#Browser_Cache)
- [OWASP - HttpOnly](https://www.owasp.org/index.php/HttpOnly)
- [OWASP - SameSite](https://www.owasp.org/index.php/SameSite)
- [OWASP - Secure Headers Project](https://www.owasp.org/index.php/OWASP_Secure_Headers_Project)
- [OWASP - SecureFlag](https://www.owasp.org/index.php/SecureFlag)
- [OWASP - Session Management Cheat Sheet](https://www.owasp.org/index.php/Session_Management_Cheat_Sheet#Cookies)
- [Mozilla Web Security](https://infosec.mozilla.org/guidelines/web_security)
