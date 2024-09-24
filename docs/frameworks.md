# Framework Integration

`secure.py` supports several popular Python web frameworks. Below are examples showing how to set the default security headers in each framework, followed by a guide for integrating Secure Headers with custom or unsupported frameworks.

## Table of Contents

- [aiohttp](#aiohttp)
- [Bottle](#bottle)
- [Django](#django)
- [Falcon](#falcon)
- [FastAPI](#fastapi)
- [Flask](#flask)
- [Pyramid](#pyramid)
- [Quart](#quart)
- [Sanic](#sanic)
- [Starlette](#starlette)
- [Tornado](#tornado)
- [TurboGears](#turbogears)
- [Web2py](#web2py)
- [Morepath](#morepath)
- [Custom Frameworks](#custom-frameworks)

---

## aiohttp

```python
from aiohttp import web
from secure import Secure

secure_headers = Secure.with_default_headers()

async def handle(request):
    return web.Response(text="Hello, world")

app = web.Application()

@app.middleware
async def add_security_headers(request, handler):
    response = await handler(request)
    secure_headers.set_headers(response)
    return response

app.router.add_get('/', handle)
web.run_app(app)
```

---

## Bottle

```python
from bottle import Bottle, response, run
from secure import Secure

secure_headers = Secure.with_default_headers()
app = Bottle()

@app.hook('after_request')
def add_security_headers():
    secure_headers.set_headers(response)

@app.route('/')
def index():
    return "Hello, world"

run(app, host='localhost', port=8080)
```

---

## Django

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

```python
import falcon
from secure import Secure

secure_headers = Secure.with_default_headers()

class HelloWorldResource:
    def on_get(self, req, resp):
        resp.text = "Hello, world"
        secure_headers.set_headers(resp)

app = falcon.App()
app.add_route('/', HelloWorldResource())
```

---

## FastAPI

```python
from fastapi import FastAPI, Response
from secure import Secure

app = FastAPI()
secure_headers = Secure.with_default_headers()

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    secure_headers.set_headers(response)
    return response

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

---

## Flask

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

## Pyramid

```python
from pyramid.config import Configurator
from pyramid.response import Response
from secure import Secure

secure_headers = Secure.with_default_headers()

def hello_world(request):
    response = Response('Hello, world')
    secure_headers.set_headers(response)
    return response

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_view(hello_world, route_name='home')
        app = config.make_wsgi_app()

    from waitress import serve
    serve(app, listen='0.0.0.0:6543')
```

---

## Quart

```python
from quart import Quart, Response
from secure import Secure

app = Quart(__name__)
secure_headers = Secure.with_default_headers()

@app.after_request
async def add_security_headers(response: Response):
    secure_headers.set_headers(response)
    return response

@app.route('/')
async def index():
    return 'Hello, world'

app.run()
```

---

## Sanic

```python
from sanic import Sanic, response
from secure import Secure

app = Sanic("SecureApp")
secure_headers = Secure.with_default_headers()

@app.middleware('response')
async def add_security_headers(request, resp):
    secure_headers.set_headers(resp)

@app.route("/")
async def index(request):
    return response.text("Hello, world")

app.run(host="0.0.0.0", port=8000)
```

---

## Starlette

```python
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
from secure import Secure

secure_headers = Secure.with_default_headers()

async def homepage(request):
    return Response("Hello, world")

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        secure_headers.set_headers(response)
        return response

app = Starlette(debug=True)
app.add_route("/", homepage)
app.add_middleware(SecurityHeadersMiddleware)
```

---

## Tornado

```python
import tornado.ioloop
import tornado.web
from secure import Secure

secure_headers = Secure.with_default_headers()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        secure_headers.set_headers(self)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
```

---

## TurboGears

```python
from tg import expose, TGController, AppConfig
from secure import Secure

secure_headers = Secure.with_default_headers()

class RootController(TGController):
    @expose()
    def index(self):
        response = "Hello, world"
        secure_headers.set_headers(self.response)
        return response

config = AppConfig(minimal=True, root_controller=RootController())
app = config.make_wsgi_app()
```

---

## Web2py

```python
from gluon import current
from secure import Secure

secure_headers = Secure.with_default_headers()

def index():
    secure_headers.set_headers(current.response)
    return "Hello, world"
```

---

## Morepath

```python
import morepath
from secure import Secure

class App(morepath.App):
    pass

secure_headers = Secure.with_default_headers()

@app.path(path="")
class Root:
    pass

@app.view(model=Root)
def hello_world(request):
    response = morepath.Response("Hello, world")
    secure_headers.set_headers(response)
    return response

if __name__ == "__main__":
    morepath.run(App())
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
