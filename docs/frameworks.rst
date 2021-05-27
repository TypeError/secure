Supported Frameworks
=====================

Framework Agnostic
--------------------

| Return Dictionary of Headers: 
| ``secure.Secure().headers()``

.. _example-4:


**Example:**

.. code:: python

    csp = secure.ContentSecurityPolicy()
    secure_headers = secure.Secure(csp=csp)

**Return Value:**

``{'Strict-Transport-Security': 'max-age=63072000; includeSubdomains', 'X-Frame-Options': 'SAMEORIGIN', 'X-XSS-Protection': '0', 'X-Content-Type-Options': 'nosniff', 'Content-Security-Policy': "script-src 'self'; object-src 'self'", 'Referrer-Policy': 'no-referrer, strict-origin-when-cross-origin', 'Cache-Control': 'no-store'}``


aiohttp
--------

``secure_headers.framework.aiohttp(resp)``

.. _example-5:

**Example:**

.. code:: python

   from aiohttp import web
   from aiohttp.web import middleware
   import secure

   secure_headers = secure.Secure()

   . . . 

   @middleware
   async def set_secure_headers(request, handler):
       resp = await handler(request)
       secure_headers.framework.aiohttp(resp)
       return resp
       
   . . . 

   app = web.Application(middlewares=[set_secure_headers])

   . . . 


Bottle
------

``secure_headers.framework.bottle(response)``

.. _example-7:

**Example:**

.. code:: python

   from bottle import route, run, response, hook
   import secure

   secure_headers = secure.Secure()

   . . . 

   @hook("after_request")
   def set_secure_headers():
       secure_headers.framework.bottle(response)
       
   . . . 


CherryPy
--------

``"tools.response_headers.headers": secure_headers.framework.cherrypy()``

.. _example-9:

**Example:**

CherryPy `Application
Configuration <http://docs.cherrypy.org/en/latest/config.html#application-config>`__:

.. code:: python

   import cherrypy
   import secure

   secure_headers = secure.Secure()

   . . . 

   config = {
       "/": {
           "tools.response_headers.on": True,
           "tools.response_headers.headers": secure_headers.framework.cherrypy(),
       }
   }

   . . . 


Django
------

``secure_headers.framework.django(response)``

.. _example-11:

**Example:**

Django `Middleware
Documentation <https://docs.djangoproject.com/en/2.1/topics/http/middleware/>`__:

.. code:: python

   # securemiddleware.py
   import secure

   secure_headers = secure.Secure()

   . . . 

   def set_secure_headers(get_response):
       def middleware(request):
           response = get_response(request)
           secure_headers.framework.django(response)
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

FastAPI
------

``secure_headers.framework.fastapi(resp)``

.. _example-13:

**Example:**

.. code:: python

    from fastapi import FastAPI
    import secure

    secure_headers = secure.Secure()

    . . . 

    @app.middleware("http")
    async def set_secure_headers(request, call_next):
        response = await call_next(request)
        secure_headers.framework.fastapi(response)
        return response

    . . . 


Falcon
------

``secure_headers.framework.falcon(resp)``

.. _example-13:

**Example:**

.. code:: python

   import falcon
   import secure

   secure_headers = secure.Secure()

   . . . 

   class SetSecureHeaders(object):
       def process_request(self, req, resp):
           secure_headers.framework.falcon(resp)

   . . . 

   app = api = falcon.API(middleware=[SetSecureHeaders()])

   . . . 


Flask
-----

``secure_headers.framework.flask(response)``

.. _example-15:

**Example:**

.. code:: python

   from flask import Flask, Response
   import secure

   secure_headers = secure.Secure()

   app = Flask(__name__)

   . . . 

   @app.after_request
   def set_secure_headers(response):
       secure_headers.framework.flask(response)
       return response
       
   . . . 

hug
---

``secure_headers.framework.hug(response)`` 

.. _example-17:

**Example:**

.. code:: python

  import hug
  import secure

  secure_headers = secure.Secure()

   . . . 

  @hug.response_middleware()
  def set_secure_headers(request, response, resource):
      secure_headers.framework.hug(response)

   . . . 



Masonite
--------

``secure_headers.framework.masonite(self.request)``

.. _example-19:

**Example:**

Masonite
`Middleware <https://docs.masoniteproject.com/advanced/middleware#creating-middleware>`__:

.. code:: python

  # SecureMiddleware.py

  from masonite.request import Request

  import secure

  secure_headers = secure.Secure()

  class SecureMiddleware:
      def __init__(self, request: Request):

          self.request = request

      def before(self):
          secure_headers.framework.masonite(self.request)

   . . . 

.. code:: python

   # middleware.py

   ...

  HTTP_MIDDLEWARE = [
      SecureMiddleware,
  ]

   ...


Pyramid
-------

Pyramid
`Tween <https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/hooks.html#registering-tweens>`__:

.. code:: python

   def set_secure_headers(handler, registry):
       def tween(request):
           response = handler(request)
           secure_headers.framework.pyramid(response)
           return response

       return tween

.. _example-21:

**Example:**

.. code:: python

   from pyramid.config import Configurator
   from pyramid.response import Response
   import secure

   secure_headers = secure.Secure()

   . . . 

   def set_secure_headers(handler, registry):
       def tween(request):
           response = handler(request)
           secure_headers.framework.pyramid(response)
           return response

       return tween

   . . . 

   config.add_tween(".set_secure_headers")

   . . . 



Quart
-----

``secure_headers.framework.quart(response)``

.. _example-23:

**Example:**

.. code:: python

   from quart import Quart, Response
   import secure

   secure_headers = secure.Secure()

   app = Quart(__name__)

   . . . 

   @app.after_request
   async def set_secure_headers(response):
       secure_headers.framework.quart(response)
       return response

   . . . 



Responder
---------

``secure_headers.framework.responder(resp)``

.. _example-25:

**Example:**

.. code:: python

   import responder
   import secure

   secure_headers = secure.Secure()

   api = responder.API()

   . . . 

   @api.route(before_request=True)
   def set_secure_headers(req, resp):
       secure_headers.framework.responder(resp)

   . . . 

You should use Responder’s `built in
HSTS <https://python-responder.org/en/latest/tour.html#hsts-redirect-to-https>`__
and pass the ``hsts=False`` option.


Sanic
-----

``secure_headers.framework.sanic(response)``

.. _example-27:

**Example:**

.. code:: python

   from sanic import Sanic
   import secure

   secure_headers = secure.Secure()

   app = Sanic()

   . . . 

   @app.middleware("response")
   async def set_secure_headers(request, response):
       secure_headers.framework.sanic(response)

   . . . 


*To set Cross Origin Resource Sharing (CORS) headers, please
see* `sanic-cors <https://github.com/ashleysommer/sanic-cors>`__ *.*

Starlette
---------

``secure_headers.framework.starlette(response)``

.. _example-29:

**Example:**

.. code:: python

   from starlette.applications import Starlette
   import uvicorn
   import secure

   secure_headers = secure.Secure()

   app = Starlette()

   . . . 

   @app.middleware("http")
   async def set_secure_headers(request, call_next):
       response = await call_next(request)
       secure_headers.framework.starlette(response)
       return response

   . . . 


Tornado
-------

``secure_headers.framework.tornado(self)``

.. _example-31:

**Example:**

.. code:: python

   import tornado.ioloop
   import tornado.web
   import secure

   secure_headers = secure.Secure()

   . . . 

   class BaseHandler(tornado.web.RequestHandler):
       def set_default_headers(self):
           secure_headers.framework.tornado(self)

   . . . 


