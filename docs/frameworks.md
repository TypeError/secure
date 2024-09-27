# Framework Integration

`secure.py` supports several popular Python web frameworks. Below are examples showing how to set the default security headers in each framework, along with a brief introduction and links to each project. Additionally, we provide guidance for integrating Secure Headers with custom or unsupported frameworks.

## Table of Contents

- [aiohttp](#aiohttp)
- [Bottle](#bottle)
- [CherryPy](#cherrypy)
- [Django](#django)
- [Falcon](#falcon)
- [FastAPI](#fastapi)
- [Flask](#flask)
- [Masonite](#masonite)
- [Morepath](#morepath)
- [Pyramid](#pyramid)
- [Quart](#quart)
- [Responder](#responder)
- [Sanic](#sanic)
- [Starlette](#starlette)
- [Tornado](#tornado)
- [TurboGears](#turbogears)
- [Web2py](#web2py)
- [Custom Frameworks](#custom-frameworks)

---

### Note: Overriding the `Server` Header in Uvicorn-based Frameworks

If you're using Uvicorn as the ASGI server (commonly used with frameworks like FastAPI, Starlette, and others), Uvicorn automatically injects a `Server: uvicorn` header into all HTTP responses by default. This can lead to multiple `Server` headers when using `Secure.py` to set a custom `Server` header.

To prevent Uvicorn from adding its default `Server` header, you can disable it by passing the `--no-server-header` option when running Uvicorn, or by setting `server_header=False` in the `uvicorn.run()` method:

```python
import uvicorn

uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,
    server_header=False,  # Disable Uvicorn's default Server header
)
```

If you're using Uvicorn via Gunicorn (e.g., with the `UvicornWorker`), note that this setting is not passed through automatically. In such cases, you may need to subclass the worker to fully override the `Server` header.

For more information, refer to the [Uvicorn Settings](https://www.uvicorn.org/settings/#http).

---

## aiohttp

**[aiohttp](https://docs.aiohttp.org)** is an asynchronous HTTP client/server framework for asyncio and Python. It's designed for building efficient web applications with asynchronous capabilities.

### Middleware Example

```python
from aiohttp import web
from secure import Secure

secure_headers = Secure.with_default_headers()

@web.middleware
async def add_security_headers(request, handler):
    response = await handler(request)
    await secure_headers.set_headers_async(response)
    return response

app = web.Application(middlewares=[add_security_headers])

app.router.add_get("/", lambda request: web.Response(text="Hello, world"))
web.run_app(app)
```

### Single Route Example

```python
from aiohttp import web
from secure import Secure

secure_headers = Secure.with_default_headers()

async def handle(request):
    response = web.Response(text="Hello, world")
    await secure_headers.set_headers_async(response)
    return response

app = web.Application()
app.router.add_get("/", handle)
web.run_app(app)
```

---

## Bottle

**[Bottle](https://bottlepy.org)** is a fast, simple, and lightweight WSGI micro web-framework for Python. It's perfect for small applications and rapid prototyping.

### Middleware Example

```python
from bottle import Bottle, response, run
from secure import Secure

secure_headers = Secure.with_default_headers()
app = Bottle()

@app.hook("after_request")
def add_security_headers():
    secure_headers.set_headers(response)

run(app, host="localhost", port=8080)
```

### Single Route Example

```python
from bottle import Bottle, response, run
from secure import Secure

secure_headers = Secure.with_default_headers()
app = Bottle()

@app.route("/")
def index():
    secure_headers.set_headers(response)
    return "Hello, world"

run(app, host="localhost", port=8080)
```

---

## CherryPy

**[CherryPy](https://cherrypy.dev)** is a minimalist, object-oriented web framework that allows developers to build web applications in a way similar to building other Python applications.

### Middleware Example

```python
import cherrypy
from secure import Secure

secure_headers = Secure.with_default_headers()

class HelloWorld:
    @cherrypy.expose
    def index(self):
        cherrypy.response.headers.update(secure_headers.headers)
        return b"Hello, world"

config = {
    "/": {
        "tools.response_headers.on": True,
        "tools.response_headers.headers": secure_headers.headers
    }
}

cherrypy.quickstart(HelloWorld(), "/", config)
```

### Single Route Example

```python
import cherrypy
from secure import Secure

secure_headers = Secure.with_default_headers()

class HelloWorld:
    @cherrypy.expose
    def index(self):
        cherrypy.response.headers.update(secure_headers.headers)
        return b"Hello, world"

cherrypy.quickstart(HelloWorld())
```

---

## Django

**[Django](https://www.djangoproject.com)** is a high-level Python web framework that encourages rapid development and clean, pragmatic design.

### Middleware Example

```python
from django.http import HttpResponse
from secure import Secure

secure_headers = Secure.with_default_headers()

def set_secure_headers(get_response):
    def middleware(request):
        response = get_response(request)
        secure_headers.set_headers(response)
        return response
    return middleware
```

### Single Route Example

```python
from django.http import HttpResponse
from secure import Secure

secure_headers = Secure.with_default_headers()

def home(request):
    response = HttpResponse("Hello, world")
    secure_headers.set_headers(response)
    return response
```

---

## Falcon

**[Falcon](https://falconframework.org)** is a minimalist WSGI library for building speedy web APIs and app backends.

### Middleware Example

```python
import falcon
from secure import Secure

secure_headers = Secure.with_default_headers()

class SecureMiddleware:
    def process_response(self, req, resp, resource, req_succeeded):
        secure_headers.set_headers(resp)

app = falcon.App(middleware=[SecureMiddleware()])

class HelloWorldResource:
    def on_get(self, req, resp):
        resp.text = "Hello, world"

app.add_route("/", HelloWorldResource())
```

### Single Route Example

```python
import falcon
from secure import Secure

secure_headers = Secure.with_default_headers()

class HelloWorldResource:
    def on_get(self, req, resp):
        resp.text = "Hello, world"
        secure_headers.set_headers(resp)

app = falcon.App()
app.add_route("/", HelloWorldResource())
```

---

## FastAPI

**[FastAPI](https://fastapi.tiangolo.com)** is a modern, fast web framework for building APIs with Python 3.6+.

### Middleware Example

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
```

### Single Route Example

```python
from fastapi import FastAPI, Response
from secure import Secure

app = FastAPI()
secure_headers = Secure.with_default_headers()

@app.get("/")
def read_root(response: Response):
    secure_headers.set_headers(response)
    return {"Hello": "World"}
```

---

## Flask

**[Flask](https://flask.palletsprojects.com)** is a lightweight WSGI web application framework.

### Middleware Example

```python
from flask import Flask, Response
from secure import Secure

app = Flask(__name__)
secure_headers = Secure.with_default_headers()

@app.after_request
def add_security_headers(response: Response):
    secure_headers.set_headers(response)
    return response
```

### Single Route Example

```python
from flask import Flask, Response
from secure import Secure

app = Flask(__name__)
secure_headers = Secure.with_default_headers()

@app.route("/")
def home():
    response = Response("Hello, world")
    secure_headers.set_headers(response)
    return response
```

---

## Masonite

**[Masonite](https://docs.masoniteproject.com)** is a modern and developer-friendly Python web framework.

### Middleware Example

```python
from masonite.foundation import Application
from masonite.response import Response
from secure import Secure

app = Application()
secure_headers = Secure.with_default_headers()

def add_security_headers(response: Response):
    secure_headers.set_headers(response)
    return response
```

### Single Route Example

```python
from masonite.request import Request
from masonite.response import Response
from masonite.foundation import Application
from secure import Secure

app = Application()
secure_headers = Secure.with_default_headers()

@app.route("/")
def home(request: Request, response: Response):
    return add_security_headers(response.view("Hello, world"))
```

---

## Morepath

**[Morepath](https://morepath.readthedocs.io)** is a Python web framework that provides URL to object mapping.

### Middleware Example

Morepath doesn’t have middleware. Use per-view settings as shown in the single route example.

### Single Route Example

```python
import morepath
from secure import Secure

secure_headers = Secure.with_default_headers()

class App(morepath.App):
    pass

@App.path(path="")
class Root:
    pass

@App.view(model=Root)
def hello_world(self, request):
    response = morepath.Response("Hello, world")
    secure_headers.set_headers(response)
    return response

morepath.run(App())
```

---

## Pyramid

**[Pyramid](https://trypyramid.com)** is a small, fast Python web framework.

### Middleware Example

```python
from pyramid.config import Configurator
from pyramid.response import Response
from secure import Secure

secure_headers = Secure.with_default_headers()

def add_security_headers(handler, registry):
    def tween(request):
        response = handler(request)
        secure_headers.set_headers(response)
        return response
    return tween
```

### Single Route Example

```python
from pyramid.config import Configurator
from pyramid.response import Response
from secure import Secure

secure_headers = Secure.with_default_headers()

def hello_world(request):
    response = Response("Hello, world")
    secure_headers.set_headers(response)
    return response
```

---

## Quart

**[Quart](https://quart.palletsprojects.com)** is an async Python web framework.

### Middleware Example

```python
from quart import Quart, Response
from secure import Secure

app = Quart(__name__)
secure_headers = Secure.with_default_headers()

@app.after_request
async def add_security_headers(response: Response):
    await secure_headers.set_headers_async(response)
    return response
```

### Single Route Example

```python
from quart import Quart, Response
from secure import Secure

app = Quart(__name__)
secure_headers = Secure.with_default_headers()

@app.route("/")
async def index():
    response = Response("Hello, world")
    await secure_headers.set_headers_async(response)
    return response
```

---

## Responder

**[Responder](https://responder.kennethreitz.org)** is a fast web framework for building APIs.

### Middleware Example

```python
import responder
from secure import Secure

api = responder.API()
secure_headers = Secure.with_default_headers()

@api.route("/")
async def add_security_headers(req, resp):
    await secure_headers.set_headers_async(resp)
```

### Single Route Example

```python
import responder
from secure import Secure

api = responder.API()
secure_headers = Secure.with_default_headers()

@api.route("/")
async def home(req, resp):
    resp.text = "Hello, world"
    await secure_headers.set_headers_async(resp)
```

---

## Sanic

**[Sanic](https://sanicframework.org)** is a Python web framework written for fast performance.

### Middleware Example

```python
from sanic import Sanic, response
from secure import Secure

app = Sanic("SecureApp")
secure_headers = Secure.with_default_headers()

@app.middleware("response")
async def add_security_headers(request, resp):
    secure_headers.set_headers(resp)
```

### Single Route Example

```python
from sanic import Sanic, response
from secure import Secure

app = Sanic("SecureApp")
secure_headers = Secure.with_default_headers()

@app.route("/")
async def index(request):
    resp = response.text("Hello, world")
    secure_headers.set_headers(resp)
    return resp
```

---

## Starlette

**[Starlette](https://www.starlette.io)** is a lightweight ASGI framework.

### Middleware Example

```python
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from secure import Secure

secure_headers = Secure.with_default_headers()

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        await secure_headers.set_headers_async(response)
        return response
```

### Single Route Example

```python
from starlette.applications import Starlette
from starlette.responses import Response
from secure import Secure

secure_headers = Secure.with_default_headers()

async def homepage(request):
    response = Response("Hello, world")
    await secure_headers.set_headers_async(response)
    return response
```

---

## Tornado

**[Tornado](https://www.tornadoweb.org)** is a Python web framework designed for asynchronous networking.

### Middleware Example

Tornado doesn't directly support middleware, but you can use it in each request handler as shown in the single route example.

### Single Route Example

```python
import tornado.ioloop
import tornado.web
from secure import Secure

secure_headers = Secure.with_default_headers()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        secure_headers.set_headers(self)
```

---

## TurboGears

**[TurboGears](https://turbogears.org)** is a full-stack framework.

### Middleware Example

```python
from tg import AppConfig, Response, TGController, expose
from secure import Secure

secure_headers = Secure.with_default_headers()

class SecureMiddleware:
    def __init__(self, req, resp):
        secure_headers.set_headers(resp)

config = AppConfig(minimal=True, root_controller=TGController)
config["middleware"] = [SecureMiddleware]
```

### Single Route Example

```python
from tg import AppConfig, Response, TGController, expose
from secure import Secure

secure_headers = Secure.with_default_headers()

class RootController(TGController):
    @expose()
    def index(self):
        response = Response("Hello, world")
        secure_headers.set_headers(response)
        return response
```

---

## Web2py

**[Web2py](http://www.web2py.com)** is a free web framework designed for rapid development of database-driven applications.

### Middleware Example

Web2py doesn't directly support middleware, but you can use it in each route.

### Single Route Example

```python
from gluon import current
from secure import Secure

secure_headers = Secure.with_default_headers()

def index():
    secure_headers.set_headers(current.response)
    return "Hello, world"
```

---

## Custom Frameworks

If you are using a framework that is not listed here, `secure.py` can still be integrated. Most frameworks offer a way to manipulate response headers, which is all you need to apply security headers.

### General Steps:

1. **Identify the Response Object**: Each framework typically has a response object or an equivalent that allows you to modify HTTP headers.

2. **Set Headers**: Use the `set_headers()` or `set_headers_async()` method to inject security headers into the response before sending it back to the client.

3. **Asynchronous Support**: For asynchronous frameworks, ensure that you're calling the correct async version of methods.

### Example:

```python
from secure import Secure

secure_headers = Secure().with_default_headers()

def add_secure_headers(response):
    secure_headers.set_headers(response)
    return response

# Apply the `add_secure_headers` function wherever your framework handles responses.
```

---

### Need Help?

If you encounter any issues integrating Secure Headers with your custom framework, feel free to open an issue on our [GitHub repository](https://github.com/TypeError/secure) or consult the framework's documentation for handling response headers.
