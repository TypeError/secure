# Secure

Secure 🔒 is a small library that adds optional security headers and cookie attributes for [Responder](https://github.com/kennethreitz/responder).

## Install

`pipenv install secure`   

## Headers

#### Strict-Transport-Security (HSTS)
Ensure application is loaded over HTTPS  
Value: `max-age=63072000; includeSubdomains`  
 
#### X-Frame-Options
Disable iframes (Clickjacking protection)  
Value: `DENY`  

#### X-XSS-Protection
Enable Cross-Site Scripting filters  
Value: `X-XSS-Protection", "1; mode=block`  

#### X-Content-Type-Options
Prevent MIME-sniffing  
Value: `nosniff`  

#### Content-Security-Policy (CSP)
Prevent Cross-site injections  
Value: `script-src 'self'; object-src 'self'`  

#### Referrer-Policy
Enable full referrer if same origin, remove path for cross origin and disable referrer in unsupported browsers  
Value: `no-referrer, strict-origin-when-cross-origin`

#### Cache-control / Pragma
Prevent cacheable HTTPS response  
Value: `no-cache, no-store` / `no-cache`

*Recommendations used by Secure 🔒 and more information regarding security headers can be found at the [OWASP Secure Headers Project](https://www.owasp.org/index.php/OWASP_Secure_Headers_Project).*
 
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

## Responder Headers
### Usage

```Python
import responder
import secure

api = responder.API()

... 

@api.route(before_request=True)
def prepare_response(req, resp):
    secure.responder_headers(req, resp)
```

**HTTP response headers:** 
 
```
x-frame-options: DENY
x-xss-protection: 1; mode=block
x-content-type-options: nosniff
referrer-policy: no-referrer, strict-origin-when-cross-origin
```

### Options

**Example**:
`secure.responder_headers(req, resp, csp=True)`

- `hsts` - *(default=False)* *
- `frame` - *(default=True)*
- `xss` - *(default=True)*
- `content` - *(default=True)*
- `csp` - *(default=False)* *
- `referrer` - *(default=True)*
- `cache` - *(default=False)*

You should use Responder's [built in HSTS option](https://python-responder.org/en/latest/tour.html#hsts-redirect-to-https) and the CSP headers should be carefully constructed, however you can use the defaults by including the `hsts=True` and/or `csp=True` options. 


## Responder Cookies

### Usage

```Python
import responder
import secure

api = responder.API()

... 

@api.route("/secure")
async def greet_world(req, resp):
    resp.text = "Secure"
    secure.responder_cookies(req, resp, name="responder", value="ABC123", expires=1)
```

*Set-Cookie HTTP response header:*   

`set-cookie: responder=ABC123; Path=/; Secure; HttpOnly; SameSite=Lax; Expires=Tue, 27 Nov 2018 11:38:56 GMT;`

### Options

**Example**:

`secure.responder_cookies(req,resp, name="responder-cookie", value="ABC123", secure=False)`

- `path`  -*(default="/")*
- `secure` - *(default=True)*
- `httponly` - *(default=True)*
- `samesite` - *options: `lax` or `strict` (default="lax")*
- `expires` - cookie expiration in hours (default=False)


## Attribution/References
- [Responder: A familiar HTTP Service Framework](https://python-responder.org/en/latest/)
- [kennethreitz/setup.py: 📦 A Human’s Ultimate Guide to setup.py.](https://github.com/kennethreitz/setup.py)
- [OWASP -  Application Security FAQ - Browser Cache](https://www.owasp.org/index.php/OWASP_Application_Security_FAQ#Browser_Cache)
- [OWASP - HttpOnly](https://www.owasp.org/index.php/HttpOnly)
- [OWASP - SameSite](https://www.owasp.org/index.php/SameSite)
- [OWASP - Secure Headers Project](https://www.owasp.org/index.php/OWASP_Secure_Headers_Project)
- [OWASP - SecureFlag](https://www.owasp.org/index.php/SecureFlag)
- [OWASP - Session Management Cheat Sheet](https://www.owasp.org/index.php/Session_Management_Cheat_Sheet#Cookies)
- [Mozilla Web Security](https://infosec.mozilla.org/guidelines/web_security)
