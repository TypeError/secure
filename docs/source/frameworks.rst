Supported Frameworks
=====================

Framework Agnostic
--------------------

| Return Dictionary of Headers: 
| ``secure_headers.headers()``

.. _example-4:


**Example:**

.. code:: python

   secure_headers.headers(csp=True, feature=True)

**Return Value:**

``{'Strict-Transport-Security': 'max-age=63072000; includeSubdomains', 'X-Frame-Options': 'SAMEORIGIN', 'X-XSS-Protection': '1; mode=block', 'X-Content-Type-Options': 'nosniff', 'Content-Security-Policy': "script-src 'self'; object-src 'self'", 'Referrer-Policy': 'no-referrer, strict-origin-when-cross-origin', 'Cache-control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Feature-Policy': "accelerometer 'none'; ambient-light-sensor 'none'; autoplay 'none'; camera 'none'; encrypted-media 'none';fullscreen 'none'; geolocation 'none'; gyroscope 'none'; magnetometer 'none'; microphone 'none'; midi 'none';payment 'none'; picture-in-picture 'none'; speaker 'none'; sync-xhr 'none'; usb 'none'; vr 'none';"}``


aiohttp
--------

.. _headers-1:

Headers
~~~~~~~

``secure_headers.aiohttp(resp)``

.. _example-5:

**Example:**

.. code:: python

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

.. _cookies-1:

Cookies
~~~~~~~

Cookies
~~~~~~~

.. code:: python

   secure_cookie.aiohttp(resp, name="spam", value="eggs")

.. _example-6:

**Example:**

.. code:: python

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

Bottle
------

.. _headers-2:

Headers
~~~~~~~

``secure_headers.bottle(response)``

.. _example-7:

**Example:**

.. code:: python

   from bottle import route, run, response, hook
   from secure import SecureHeaders

   secure_headers = SecureHeaders()

   . . . 

   @hook("after_request")
   def set_secure_headers():
       secure_headers.bottle(response)
       
   . . . 

.. _cookies-2:

Cookies
~~~~~~~

.. code:: python

   secure_cookie.bottle(response, name="spam", value="eggs")

.. _example-8:

**Example:**

.. code:: python

   from bottle import route, run, response, hook
   from secure import SecureCookie

   secure_cookie = SecureCookie()

   . . . 

   @route("/secure")
   def set_secure_cookie():
       secure_cookie.bottle(response, name="spam", value="eggs")
       return "Secure"
       
   . . . 

CherryPy
--------

.. _headers-3:

Headers
~~~~~~~

``"tools.response_headers.headers": secure_headers.cherrypy()``

.. _example-9:

**Example:**

CherryPy `Application
Configuration <http://docs.cherrypy.org/en/latest/config.html#application-config>`__:

.. code:: python

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

.. _cookies-3:

Cookies
~~~~~~~

.. code:: python

   response_headers = cherrypy.response.headers
   secure_cookie.cherrypy(response_headers, name="spam", value="eggs")

.. _example-10:

**Example:**

.. code:: python

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

Django
------

.. _headers-4:

Headers
~~~~~~~

``secure_headers.django(response)``

.. _example-11:

**Example:**

Django `Middleware
Documentation <https://docs.djangoproject.com/en/2.1/topics/http/middleware/>`__:

.. code:: python

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

.. code:: python

   # settings.py

   ...

   MIDDLEWARE = [
       'app.securemiddleware.set_secure_headers'
   ]

   ...

.. _cookies-4:

Cookies
~~~~~~~

.. code:: python

   secure_cookie.django(response, name="spam", value="eggs")

.. _example-12:

**Example:**

.. code:: python

   from django.http import HttpResponse
   from secure import SecureCookie

   secure_cookie = SecureCookie()

   . . . 

   def set_secure_cookie(request):
       response = HttpResponse("Secure")
       secure_cookie.django(response, name="spam", value="eggs")
       return response
       
   . . . 
       

Falcon
------

.. _headers-5:

Headers
~~~~~~~

``secure_headers.falcon(resp)``

.. _example-13:

**Example:**

.. code:: python

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

.. _cookies-5:

Cookies
~~~~~~~

.. code:: python

   secure_cookie.falcon(resp, name="spam", value="eggs")

.. _example-14:

**Example:**

.. code:: python

   import falcon
   from secure import SecureCookie

   secure_cookie = SecureCookie()

   . . . 

   class SetSecureCookie(object):
       def on_get(self, req, resp):
           resp.body = "Secure"
           secure_cookie.falcon(resp, name="spam", value="eggs")
           
   . . . 

Flask
-----

.. _headers-6:

Headers
~~~~~~~

``secure_headers.flask(response)``

.. _example-15:

**Example:**

.. code:: python

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

.. _cookies-6:

Cookies
~~~~~~~

.. code:: python

   secure_cookie.flask(resp, name="spam", value="eggs")

.. _example-16:

**Example:**

.. code:: python

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

hug
---

.. _headers-7:

Headers
~~~~~~~

``secure_headers.hug(response)`` 

.. _example-17:

**Example:**

.. code:: python

  import hug
  from secure import SecureHeaders

  secure_headers = SecureHeaders()

   . . . 

  @hug.response_middleware()
  def set_secure_headers(request, response, resource):
      secure_headers.hug(response)

   . . . 

.. _cookies-7:

Cookies
~~~~~~~

.. code:: python

   secure_cookie.hug(response, name="spam", value="eggs")

.. _example-18:

**Example:**

.. code:: python

  import hug
  from secure import SecureCookie

  secure_cookie = SecureCookie()

   . . . 

  @hug.get("/secure")
  def set_secure_cookie(response):
    secure_cookie.hug(response, name="spam", value="eggs")
    return "Secure"
           
   . . . 


Masonite
--------

.. _headers-8:

Headers
~~~~~~~

``secure_headers.masonite(self.request)``

.. _example-19:

**Example:**

Masonite
`Middleware <https://docs.masoniteproject.com/advanced/middleware#creating-middleware>`__:

.. code:: python

  # SecureMiddleware.py

  from masonite.request import Request

  from secure import SecureHeaders

  secure_headers = SecureHeaders()

  class SecureMiddleware:
      def __init__(self, request: Request):

          self.request = request

      def before(self):
          secure_headers.masonite(self.request)

   . . . 

.. code:: python

   # middleware.py

   ...

  HTTP_MIDDLEWARE = [
      SecureMiddleware,
  ]

   ...

.. _cookies-8:

Cookies
~~~~~~~

.. code:: python

   secure_headers.masonite(self.request)

.. _example-20:

**Example:**

.. code:: python

   . . . 

  def show(self, view: View, request: Request, response: Response):
      secure_cookie.masonite(request, name="spam", value="eggs")
      return response.view('Secure')
        
   . . . 


Pyramid
-------

.. _headers-9:

Headers
~~~~~~~

Pyramid
`Tween <https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hooks.html#registering-tweens>`__:

.. code:: python

   def set_secure_headers(handler, registry):
       def tween(request):
           response = handler(request)
           secure_headers.pyramid(response)
           return response

       return tween

.. _example-21:

**Example:**

.. code:: python

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

.. _cookies-9:

Cookies
~~~~~~~

.. code:: python

   response = Response("Secure")
   secure_cookie.pyramid(response, name="spam", value="eggs")

.. _example-22:

**Example:**

.. code:: python

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

Quart
-----

.. _headers-10:

Headers
~~~~~~~

``secure_headers.quart(response)``

.. _example-23:

**Example:**

.. code:: python

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

.. _cookies-10:

Cookies
~~~~~~~

.. code:: python

   secure_cookie.quart(resp, name="spam", value="eggs")

.. _example-24:

**Example:**

.. code:: python

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

Responder
---------

.. _headers-11:

Headers
~~~~~~~

``secure_headers.responder(resp)``

.. _example-25:

**Example:**

.. code:: python

   import responder
   from secure import SecureHeaders

   secure_headers = SecureHeaders()

   api = responder.API()

   . . . 

   @api.route(before_request=True)
   def set_secure_headers(req, resp):
       secure_headers.responder(resp)

   . . . 

You should use Responder’s `built in
HSTS <https://python-responder.org/en/latest/tour.html#hsts-redirect-to-https>`__
and pass the ``hsts=False`` option.

.. _cookies-11:

Cookies
~~~~~~~

.. code:: python

   secure_cookie.responder(resp, name="spam", value="eggs")

.. _example-26:

**Example:**

.. code:: python

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

Sanic
-----

.. _headers-12:

Headers
~~~~~~~

``secure_headers.sanic(response)``

.. _example-27:

**Example:**

.. code:: python

   from sanic import Sanic
   from secure import SecureHeaders

   secure_headers = SecureHeaders()

   app = Sanic()

   . . . 

   @app.middleware("response")
   async def set_secure_headers(request, response):
       secure_headers.sanic(response)

   . . . 

.. _cookies-12:

Cookies
~~~~~~~

.. code:: python

   secure_cookie.sanic(response, name="spam", value="eggs")

.. _example-28:

**Example:**

.. code:: python

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

*To set Cross Origin Resource Sharing (CORS) headers, please
see* `sanic-cors <https://github.com/ashleysommer/sanic-cors>`__ *.*

Starlette
---------

.. _headers-13:

Headers
~~~~~~~

``secure_headers.starlette(response)``

.. _example-29:

**Example:**

.. code:: python

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

.. _cookies-13:

Cookies
~~~~~~~

.. code:: python

   secure_cookie.starlette(response, name="spam", value="eggs")

.. _example-30:

**Example:**

.. code:: python

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

Tornado
-------

.. _headers-14:

Headers
~~~~~~~

``secure_headers.tornado(self)``

.. _example-31:

**Example:**

.. code:: python

   import tornado.ioloop
   import tornado.web
   from secure import SecureHeaders

   secure_headers = SecureHeaders()

   . . . 

   class BaseHandler(tornado.web.RequestHandler):
       def set_default_headers(self):
           secure_headers.tornado(self)

   . . . 

.. _cookies-14:

Cookies
~~~~~~~

.. code:: python

   secure_cookie.tornado(self, name="spam", value="eggs")

.. _example-32:

**Example:**

.. code:: python

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
