# Secure

[![image](https://img.shields.io/pypi/v/secure.svg)](https://pypi.org/project/secure/)
[![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/)
[![image](https://img.shields.io/pypi/l/secure.svg)](https://pypi.org/project/secure/)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Secure 🔒 is a lightweight package that adds optional security headers and cookie attributes for Python web frameworks.

### Supported Python web frameworks:
[aiohttp](https://docs.aiohttp.org), [Bottle](https://bottlepy.org), [CherryPy](https://cherrypy.org), [Django](https://www.djangoproject.com), [Falcon](https://falconframework.org), [Flask](http://flask.pocoo.org), [hug](http://www.hug.rest), [Pyramid](https://trypyramid.com), [Quart](https://pgjones.gitlab.io/quart/), [Responder](https://python-responder.org), [Sanic](https://sanicframework.org), [Starlette](https://www.starlette.io/), [Tornado](https://www.tornadoweb.org/) 


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

## Security Headers

Security Headers are HTTP response headers that, when set, can enhance the security of your web application by enabling browser security policies. 

You can assess the security of your HTTP response headers at [securityheaders.com](https://securityheaders.com)

*Recommendations used by Secure 🔒 and more information regarding security headers can be found at the [OWASP Secure Headers Project](https://www.owasp.org/index.php/OWASP_Secure_Headers_Project).*
 
## Headers  

#### Server
Contain information about server software   
**Default Value:** `NULL` *(obfuscate server information, not included by default)*

#### Strict-Transport-Security (HSTS)
Ensure application communication is sent over HTTPS   
**Default Value:** `max-age=63072000; includeSubdomains`  
 
#### X-Frame-Options (XFO)
Disable framing from different origins (clickjacking defense)  
**Default Value:** `SAMEORIGIN`  

#### X-XSS-Protection
Enable browser cross-site scripting filters  
**Default Value:** `1; mode=block`  

#### X-Content-Type-Options
Prevent MIME-sniffing  
**Default Value:** `nosniff`  

#### Content-Security-Policy (CSP)
Prevent cross-site injections  
**Default Value:** `script-src 'self'; object-src 'self'`  *(not included by default)**

#### Referrer-Policy
Enable full referrer if same origin, remove path for cross origin and disable referrer in unsupported browsers  
**Default Value:** `no-referrer, strict-origin-when-cross-origin`

#### Cache-control / Pragma
Prevent cacheable HTTPS response  
**Default Value:** `no-cache, no-store, must-revalidate` / `no-cache`

#### Feature-Policy
Disable browser features and APIs  
**Default Value:** `accelerometer 'none'; ambient-light-sensor 'none'; autoplay 'none'; camera 'none'; encrypted-media 'none'; fullscreen 'none'; geolocation 'none'; gyroscope 'none'; magnetometer 'none'; microphone 'none'; midi 'none'; payment 'none'; picture-in-picture 'none'; speaker 'none'; sync-xhr 'none'; usb 'none'; vr 'none';",` *(not included by default)*

 **The Content-Security-Policy (CSP) header can break functionality and can (and should) be carefully constructed, use the `csp=True` option to enable default values.*
 
 ### Example
`secure_headers.framework(response)`

 **Default HTTP response headers:** 
 
```HTTP
Strict-Transport-Security: max-age=63072000; includeSubdomains
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Referrer-Policy: no-referrer, strict-origin-when-cross-origin
Cache-control: no-cache, no-store, must-revalidate
Pragma: no-cache
```

### Options

You can toggle the setting of headers with default values by passing `True` or `False` and override default values by passing a string to the following options:   

- `server` - set the Server header, e.g. `Server=“Secure”` *(string / bool / SecurePolicies, default=False)*
- `hsts` - set the Strict-Transport-Security header *(string / bool / SecurePolicies, default=True)*  
- `xfo` - set the X-Frame-Options header *(string / bool / SecurePolicies, default=True)*  
- `xxp` - set the X-XSS-Protection header *(string / bool / SecurePolicies, default=True)*  
- `content` - set the X-Content-Type-Options header *(string / bool / SecurePolicies, default=True)*  
- `csp` - set the Content-Security-Policy *(string / bool / SecurePolicies, default=False)* *  
- `referrer` - set the Referrer-Policy header *(string / bool / SecurePolicies, default=True)*  
- `cache` - set the Cache-control and Pragma headers *(string / bool / SecurePolicies, default=True)*  
- `feature` - set the Feature-Policy header *(SecurePolicies / string / bool / SecurePolicies, default=False)*  

####  Example

```Python
from secure import SecureHeaders

secure_headers = SecureHeaders(csp=True, hsts=False, xfo="DENY")

. . . 

secure_headers.framework(response)

```

## SecurePolicies - Header Policy Builder

### Methods

#### CSP()
**Directives:** `base_uri(sources)`, `block_all_mixed_content()`, `connect_src(sources)`, `default_src(sources)`, `font_src(sources)`, `form_action(sources)`, `frame_ancestors(sources)`, `frame_src(sources)`, `img_src(sources)`, `manifest_src(sources)`, `media_src(sources)`, `object_src(sources)`, `plugin_types(types)`, `report_to(json_object)`, `report_uri(uri)`, `require_sri_for(values)`, `sandbox(values)`,  `script_src(sources)`, `style_src(sources)`, `upgrade_insecure_requests()`, `worker_src(sources)`

**Values()**: `self_`, `none`, `unsafe_inline`, `unsafe_eval`, `strict_dynamic`, `nonce(nonce_value)`, `all` = "*"

**Example:**

```Python
csp_value = (
    SecurePolicies.CSP()
    .default_src(SecurePolicies.CSP().Values.none)
    .base_uri(SecurePolicies.CSP().Values.self_)
    .block_all_mixed_content()
    .connect_src(SecurePolicies.CSP().Values.self_, "api.spam.com")
    .frame_src(SecurePolicies.CSP().Values.none)
    .img_src(SecurePolicies.CSP().Values.self_, "static.spam.com")
)

# default-src 'none'; base-uri 'self'; block-all-mixed-content; connect-src 'self' api.spam.com; frame-src 'none'; img-src 'self' static.spam.com
```

*You can check the effectiveness of your CSP Policy at the [CSP Evaluator](https://csp-evaluator.withgoogle.com)*


#### HSTS()
**Directives:** `include_subDomains()`, `max_age(seconds)`, `preload()`

**Example:**

```Python
hsts_value = (
    SecurePolicies.HSTS()
    .include_subdomains()
    .preload()
    .max_age(SecurePolicies.Seconds.one_month)
)

# includeSubDomains; preload; max-age=2592000
```

#### XXP()
**Directives:** `disabled()` = 0, `enabled()` = 1, `enabled_block()` = 1; mode=block, `enabled_report(uri)` = 1; report=uri

**Example:**

```Python
xxp_value = SecurePolicies.XXP().enabled_block()

# 1; mode=block
```


#### XFO()
**Directives:** `allow_from(uri)`, `deny()`, `sameorigin()`

**Example:**

```Python
xfo_value = SecurePolicies.XFO().deny()

# deny
```


#### Referrer()
**Directives:** `no_referrer()`, `no_referrer_when_downgrade()`, `origin()`, `origin_when_cross_origin()`, `same_origin()`, `strict_origin()`, `strict_origin_when_cross_origin()`, `unsafe_url()`

**Example:**

```Python
referrer_value = SecurePolicies.Referrer().no_referrer()

# no-referrer
```


#### Feature()
**Directives:** `accelerometer(allowlist)`, `ambient_light_sensor(allowlist)`, `autoplay(allowlist)`, `camera(allowlist)`, `document_domain(allowlist)`, `encrypted_media(allowlist)`, `fullscreen(allowlist)`, `geolocation(allowlist)`, `gyroscope(allowlist)`, `magnetometer(allowlist)`, `microphone(allowlist)`, `midi(allowlist)`, `payment(allowlist)`, `picture_in_picture(allowlist)`, `speaker(allowlist)`, `sync_xhr(allowlist)`, `usb(allowlist)`, `Values(allowlist)`, `vr(allowlist)`

**Values()**: `self_`, `none`, `src`, `all` = "*"

**Example:**

```Python
feature_value = (
    SecurePolicies.Feature()
    .geolocation(SecurePolicies.Feature.Values.self_, "spam.com")
    .vibrate(SecurePolicies.Feature.Values.none)
)

# geolocation 'self' spam.com; vibrate 'none'
```


#### Cache
**Directives:** `immutable()`, `max_age(seconds)`, `max_stale(seconds)`, `min_fresh(seconds)`, `must_revalidate()`, `no_cache()`, `no_store()`, `no_transform()`, `only_if_cached()`, `private()`, `proxy_revalidate()`, `public()`, `s_maxage(seconds)`, `stale_if_error(seconds)`, `stale_while_revalidate(seconds)`,

**Example:**

```Python
cache_value = SecurePolicies.Cache().no_store().must_revalidate().proxy_revalidate()

# no-store, must-revalidate, proxy-revalidate
```
 

### Seconds
**Values:** `five_minutes` = "300", `one_week` = "604800", `one_month` = "2592000", `one_year` = "31536000", `two_years` = "63072000"

## Usage
##### Example
```Python
from sanic import Sanic
from secure import SecureHeaders, SecurePolicies

csp_value = (
    SecurePolicies.CSP()
    .default_src(SecurePolicies.CSP().Values.none)
    .base_uri(SecurePolicies.CSP().Values.self_)
    .block_all_mixed_content()
    .connect_src(SecurePolicies.CSP().Values.self_, "api.spam.com")
    .frame_src(SecurePolicies.CSP().Values.none)
    .img_src(SecurePolicies.CSP().Values.self_, "static.spam.com")
)

hsts_value = (
    SecurePolicies.HSTS()
    .include_subdomains()
    .preload()
    .max_age(SecurePolicies.Seconds.one_month)
)

xxp_value = SecurePolicies.XXP().enabled_block()

xfo_value = SecurePolicies.XFO().deny()

referrer_value = SecurePolicies.Referrer().no_referrer()

feature_value = (
    SecurePolicies.Feature()
    .geolocation(SecurePolicies.Feature.Values.self_, "spam.com")
    .vibrate(SecurePolicies.Feature.Values.none)
)

cache_value = SecurePolicies.Cache().no_store().must_revalidate().proxy_revalidate()

secure_headers = SecureHeaders(
    csp=csp_value,
    hsts=hsts_value,
    xfo=xfo_value,
    xxp=xxp_value,
    referrer=referrer_value,
    feature=feature_value,
    cache=cache_value,
)
secure_cookie = SecureCookie()

app = Sanic()

. . . 

@app.middleware("response")
async def set_secure_headers(request, response):
    secure_headers.sanic(response)

. . . 
```

Response Headers:

```HTTP
Strict-Transport-Security: includeSubDomains; preload; max-age=2592000
X-Frame-Options: deny
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Content-Security-Policy: default-src 'none'; base-uri 'self'; block-all-mixed-content; connect-src 'self' api.spam.com; frame-src 'none'; img-src 'self' static.spam.com
Referrer-Policy: no-referrer
Cache-control: no-store, must-revalidate, proxy-revalidate
Feature-Policy: geolocation 'self' spam.com; vibrate 'none'
```


## Resources:
* **CSP:** [CSP Cheat Sheet | Scott Helme](https://scotthelme.co.uk/csp-cheat-sheet/), [Content-Security-Policy | MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy), [Content Security Policy Cheat Sheet | OWASP](https://www.owasp.org/index.php/Content_Security_Policy_Cheat_Sheet), [Content Security Policy CSP Reference & Examples](https://content-security-policy.com)
* **XXP:** [X-XSS-Protection | MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection)
* **XFO:** [X-Frame-Options | MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options)
* **HSTS:** [Strict-Transport-Security | MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security), 
[HTTP Strict Transport Security Cheat Sheet | OWASP](https://www.owasp.org/index.php/HTTP_Strict_Transport_Security_Cheat_Sheet)
* **Referrer:** [A new security header: Referrer Policy | Scott Helme](https://scotthelme.co.uk/a-new-security-header-referrer-policy/), [Referrer-Policy | MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy)
* **Feature:** [A new security header: Feature Policy | Scott Helme](https://scotthelme.co.uk/a-new-security-header-feature-policy/), [Feature-Policy | MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Feature-Policy), [Introduction to Feature Policy | Google Developers](https://developers.google.com/web/updates/2018/06/feature-policy)
* **Cache:** [Cache-Control | MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)

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
secure_cookie.framework(response, name="spam", value="eggs")
```

*Default Set-Cookie HTTP response header:*   

```HTTP
Set-Cookie: spam=eggs; Path=/; secure; HttpOnly; SameSite=lax
```

### Options

You can modify default cookie attribute values by passing the following options:   

- `name`  - set the cookie name *(string, No default value)*
- `value`  - set the cookie value *(string, No default value)*
- `path`  - set the Path attribute, e.g.`path=“/secure”` *(string, default="/")*
- `secure` - set the Secure flag *(bool, default=True)*
- `httponly` - set the HttpOnly flag *(bool, default=True)*
- `samesite` - set the SameSite attribute, e.g. `SecureCookie.SameSite.lax` *(bool / enum, options: `SecureCookie.SameSite.lax`, `SecureCookie.SameSite.lax` or `False`, default=SecureCookie.SameSite.lax)**
- `expires` - set the Expires attribute with the cookie expiration in hours, e.g.`expires=1` *(number / bool, default=False)*

*You can also import the SameSite options enum from Secure, `from secure import SecureCookie, SameSite`*

#### Example
```Python
from secure import SecureCookie
secure_cookie = SecureCookie(expires=1, samesite=SecureCookie.SameSite.strict)

secure_cookie.framework(response, name="spam", value="eggs")
```

# Framework Agnostic
Return Dictionary of Headers:  
`secure_headers.headers()`

##### Example
```Python
secure_headers.headers(csp=True, feature=True)
```

Return Value:  

`{'Strict-Transport-Security': 'max-age=63072000; includeSubdomains', 'X-Frame-Options': 'SAMEORIGIN', 'X-XSS-Protection': '1; mode=block', 'X-Content-Type-Options': 'nosniff', 'Content-Security-Policy': "script-src 'self'; object-src 'self'", 'Referrer-Policy': 'no-referrer, strict-origin-when-cross-origin', 'Cache-control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Feature-Policy': "accelerometer 'none'; ambient-light-sensor 'none'; autoplay 'none'; camera 'none'; encrypted-media 'none';fullscreen 'none'; geolocation 'none'; gyroscope 'none'; magnetometer 'none'; microphone 'none'; midi 'none';payment 'none'; picture-in-picture 'none'; speaker 'none'; sync-xhr 'none'; usb 'none'; vr 'none';"}`

# Supported Frameworks

## aiohttp

#### Headers
`secure_headers.aiohttp(resp)`

##### Example
```Python
from aiohttp import web
from aiohttp.web import middleware
from secure import SecureHeaders

secure_headers = SecureHeaders()

. . . 

@middleware
async def set_secure_headers(request, handler):
    resp = await handler(request)
    secure_headers.aiohttp(resp)
    return resp
    
. . . 

app = web.Application(middlewares=[set_secure_headers])

. . . 
```

#### Cookies
```Python
secure_cookie.aiohttp(resp, name="spam", value="eggs")
```

##### Example
```Python
from aiohttp import web
from secure import SecureCookie

secure_cookie = SecureCookie()

. . . 

@routes.get("/secure")
async def set_secure_cookie(request):
    resp = web.Response(text="Secure")
    secure_cookie.aiohttp(resp, name="spam", value="eggs")
    return resp
    
. . . 
```


## Bottle

#### Headers
`secure_headers.bottle(response)`

##### Example
```Python
from bottle import route, run, response, hook
from secure import SecureHeaders

secure_headers = SecureHeaders()

. . . 

@hook("after_request")
def set_secure_headers():
    secure_headers.bottle(response)
    
. . . 
```

#### Cookies
```Python
secure_cookie.bottle(response, name="spam", value="eggs")
```

##### Example
```Python
from bottle import route, run, response, hook
from secure import SecureCookie

secure_cookie = SecureCookie()

. . . 

@route("/secure")
def set_secure_cookie():
    secure_cookie.bottle(response, name="spam", value="eggs")
    return "Secure"
    
. . . 
```

## CherryPy

#### Headers
`"tools.response_headers.headers": secure_headers.cherrypy()`

##### Example
CherryPy [Application Configuration](http://docs.cherrypy.org/en/latest/config.html#application-config):

```Python
import cherrypy
from secure import SecureHeaders

secure_headers = SecureHeaders()

. . . 

config = {
    "/": {
        "tools.response_headers.on": True,
        "tools.response_headers.headers": secure_headers.cherrypy(),
    }
}

. . . 
```

#### Cookies
```Python
response_headers = cherrypy.response.headers
secure_cookie.cherrypy(response_headers, name="spam", value="eggs")
```

##### Example
```Python
import cherrypy
from secure import SecureCookie

secure_cookie = SecureCookie()

. . . 

class SetSecureCookie(object):
    @cherrypy.expose
    def set_secure_cookie(self):
        response_headers = cherrypy.response.headers
        secure_cookie.cherrypy(response_headers, name="spam", value="eggs")
        return "Secure"
    
. . . 
```

## Django

#### Headers
`secure_headers.django(response)`

##### Example
Django [Middleware Documentation](https://docs.djangoproject.com/en/2.1/topics/http/middleware/):


```Python
# securemiddleware.py
from secure import SecureHeaders

secure_headers = SecureHeaders()

. . . 

def set_secure_headers(get_response):
    def middleware(request):
        response = get_response(request)
        secure_headers.django(response)
        return response

    return middleware
    
. . . 
```

```Python
# settings.py

...

MIDDLEWARE = [
    'app.securemiddleware.set_secure_headers'
]

```

#### Cookies
```Python
secure_cookie.django(response, name="spam", value="eggs")
```

##### Example
```Python
from django.http import HttpResponse
from secure import SecureCookie

secure_cookie = SecureCookie()

. . . 

def set_secure_cookie(request):
    response = HttpResponse("Secure")
    secure_cookie.django(response, name="spam", value="eggs")
    return response
    
. . . 
    
```

## Falcon

#### Headers
`secure_headers.falcon(resp)`

##### Example
```Python
import falcon
from secure import SecureHeaders

secure_headers = SecureHeaders()

. . . 

class SetSecureHeaders(object):
    def process_request(self, req, resp):
        secure_headers.falcon(resp)

. . . 

app = api = falcon.API(middleware=[SetSecureHeaders()])

. . . 
```

#### Cookies
```Python
secure_cookie.falcon(resp, name="spam", value="eggs")
```

##### Example
```Python
import falcon
from secure import SecureCookie

secure_cookie = SecureCookie()

. . . 

class SetSecureCookie(object):
    def on_get(self, req, resp):
        resp.body = "Secure"
        secure_cookie.falcon(resp, name="spam", value="eggs")
        
. . . 
```

## Flask

#### Headers
`secure_headers.flask(response)`

##### Example
```Python
from flask import Flask, Response
from secure import SecureHeaders

secure_headers = SecureHeaders()

app = Flask(__name__)

. . . 

@app.after_request
def set_secure_headers(response):
    secure_headers.flask(response)
    return response
    
. . . 
```

#### Cookies
```Python
secure_cookie.flask(resp, name="spam", value="eggs")
```

##### Example
```Python
from flask import Flask, Response
from secure import SecureCookie

secure_cookie = SecureCookie()

. . . 

@app.route("/secure")
def set_secure_cookie():
    resp = Response("Secure")
    secure_cookie.flask(resp, name="spam", value="eggs")
    return resp
        
. . . 
```

## hug

#### Headers
`SecureHeaders.hug(response)`
*Pass response and options directly to SecureHeaders*

##### Example
```Python
import hug
from secure import SecureHeaders

. . . 

@hug.response_middleware()
def set_secure_headers(request, response, resource):
    SecureHeaders.hug(response)

. . . 
```

#### Cookies
```Python
SecureCookie.hug(response, name="hug", value="ABC123")
```
*Pass response and options directly to SecureCookie*

##### Example
```Python
import hug
from secure import SecureCookie

. . . 

@hug.get("/secure")
def set_secure_cookie(response=None):
    SecureCookie.hug(response, name="spam", value="eggs")
    return "Secure"
        
. . . 
```


## Pyramid

#### Headers
Pyramid [Tween](https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hooks.html#registering-tweens):

```Python
def set_secure_headers(handler, registry):
    def tween(request):
        response = handler(request)
        secure_headers.pyramid(response)
        return response

    return tween
```

##### Example
```Python
from pyramid.config import Configurator
from pyramid.response import Response
from secure import SecureHeaders

secure_headers = SecureHeaders()

. . . 

def set_secure_headers(handler, registry):
    def tween(request):
        response = handler(request)
        secure_headers.pyramid(response)
        return response

    return tween

. . . 

config.add_tween(".set_secure_headers")

. . . 
```


#### Cookies
```Python
response = Response("Secure")
secure_cookie.pyramid(response, name="spam", value="eggs")
```

##### Example
```Python
from pyramid.config import Configurator
from pyramid.response import Response
from secure import SecureCookie

secure_cookie = SecureCookie()

. . . 

def set_secure_cookie(request):
    response = Response("Secure")
    secure_cookie.pyramid(response, name="spam", value="eggs")
    return response
    
. . . 
```

## Quart

#### Headers
`secure_headers.quart(response)`

##### Example
```Python
from quart import Quart, Response
from secure import SecureHeaders

secure_headers = SecureHeaders()

app = Quart(__name__)

. . . 

@app.after_request
async def set_secure_headers(response):
    secure_headers.quart(response)
    return response

. . . 
```


#### Cookies
```Python
secure_cookie.quart(resp, name="spam", value="eggs")
```

##### Example
```Python
from quart import Quart, Response
from secure import SecureCookie

secure_cookie = SecureCookie()

app = Quart(__name__)

. . . 

@app.route("/secure")
async def set_secure_cookie():
    resp = Response("Secure")
    secure_cookie.quart(resp, name="spam", value="eggs")
    return resp
    
. . . 
```

## Responder

#### Headers
`secure_headers.responder(resp)`

##### Example
```Python
import responder
from secure import SecureHeaders

secure_headers = SecureHeaders()

api = responder.API()

. . . 

@api.route(before_request=True)
def set_secure_headers(req, resp):
    secure_headers.responder(resp)

. . . 
```

You should use Responder's [built in HSTS](https://python-responder.org/en/latest/tour.html#hsts-redirect-to-https) and pass the `hsts=False` option. 


#### Cookies
```Python
secure_cookie.responder(resp, name="spam", value="eggs")
```

##### Example
```Python
import responder
from secure import SecureCookie

secure_cookie = SecureCookie()

api = responder.API()

. . . 

@api.route("/secure")
async def set_secure_cookie(req, resp):
    resp.text = "Secure"
    secure_cookie.responder(resp, name="spam", value="eggs")
    
. . . 
```


## Sanic

#### Headers
`secure_headers.sanic(response)`

##### Example
```Python
from sanic import Sanic
from secure import SecureHeaders

secure_headers = SecureHeaders()

app = Sanic()

. . . 

@app.middleware("response")
async def set_secure_headers(request, response):
    secure_headers.sanic(response)

. . . 
```

#### Cookies
```Python
secure_cookie.sanic(response, name="spam", value="eggs")
```

##### Example
```Python
from sanic import Sanic
from sanic.response import text
from secure import SecureCookie

secure_cookie = SecureCookie()

app = Sanic()

. . . 

@app.route("/secure")
async def set_secure_cookie(request):
    response = text("Secure")
    secure_cookie.sanic(response, name="spam", value="eggs")
    return response
    
. . . 
```

*To set  Cross Origin Resource Sharing (CORS) headers, please see [sanic-cors](https://github.com/ashleysommer/sanic-cors).*

## Starlette

#### Headers
`secure_headers.starlette(response)`

##### Example
```Python
from starlette.applications import Starlette
import uvicorn
from secure import SecureHeaders

secure_headers = SecureHeaders()

app = Starlette()

. . . 

@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    secure_headers.starlette(response)
    return response

. . . 
```

#### Cookies
```Python
secure_cookie.starlette(response, name="spam", value="eggs")
```

##### Example
```Python
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
import uvicorn
from secure import SecureHeaders, SecureCookie

secure_cookie = SecureCookie()

app = Starlette()

. . . 

@app.route("/secure")
async def set_secure_cookie(request):
    response = PlainTextResponse("Secure")
    secure_cookie.starlette(response, name="spam", value="eggs")
    return response

. . . 
```

## Tornado

#### Headers
`secure_headers.tornado(self)`

##### Example
```Python
import tornado.ioloop
import tornado.web
from secure import SecureHeaders

secure_headers = SecureHeaders()

. . . 

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        secure_headers.tornado(self)

. . . 
```

#### Cookies
```Python
secure_cookie.tornado(self, name="spam", value="eggs")
```

##### Example
```Python
import tornado.ioloop
import tornado.web
from secure import SecureCookie

secure_cookie = SecureCookie()

. . . 

class SetSecureCookie(BaseHandler):
    def get(self):
        secure_cookie.tornado(self, name="spam", value="eggs")
        self.write("Secure")
    
. . . 
```



## Attribution/References

#### Frameworks
- [aiohttp](https://github.com/aio-libs/aiohttp) - Asynchronous HTTP client/server framework for asyncio and Python
- [Bottle](https://github.com/bottlepy/bottle) - A fast and simple micro-framework for python web-applications.
- [CherryPy](https://github.com/cherrypy/cherrypy) - A pythonic, object-oriented HTTP framework.
- [Django](https://github.com/django/django/) - The Web framework for perfectionists with deadlines.
- [Falcon](https://github.com/falconry/falcon) - A bare-metal Python web API framework for building high-performance microservices, app backends, and higher-level frameworks.
- [Flask](https://github.com/pallets/flask) - The Python micro framework for building web applications.
- [hug](https://github.com/timothycrosley/hug) - Embrace the APIs of the future. Hug aims to make developing APIs as simple as possible, but no simpler.
- [Pyramid](https://github.com/Pylons/pyramid) - A Python web framework
- [Quart](https://gitlab.com/pgjones/quart) - A Python ASGI web microframework.
- [Responder](https://github.com/kennethreitz/responder) - A familiar HTTP Service Framework
- [Sanic](https://github.com/huge-success/sanic) - An Async Python 3.5+ web server that's written to go fast
- [Starlette](https://github.com/encode/starlette) - The little ASGI framework that shines. ✨
- [Tornado](https://github.com/tornadoweb/tornado) - A Python web framework and asynchronous networking library, originally developed at FriendFeed.

#### Resources
- [kennethreitz/setup.py: 📦 A Human’s Ultimate Guide to setup.py.](https://github.com/kennethreitz/setup.py)
- [OWASP - Secure Headers Project](https://www.owasp.org/index.php/OWASP_Secure_Headers_Project)
- [OWASP - Session Management Cheat Sheet](https://www.owasp.org/index.php/Session_Management_Cheat_Sheet#Cookies)
- [Mozilla Web Security](https://infosec.mozilla.org/guidelines/web_security)
- [securityheaders.com](https://securityheaders.com)
