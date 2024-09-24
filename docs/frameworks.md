# Framework Integration

`secure.py` supports several popular Python web frameworks. Below are examples showing how to set the default security headers in each framework, along with a brief introduction and links to each project. Additionally, we provide guidance for integrating Secure Headers with custom or unsupported frameworks.

## Table of Contents

- [aiohttp](#aiohttp)
- [Bottle](#bottle)
- [Django](#django)
- [Falcon](#falcon)
- [FastAPI](#fastapi)
- [Flask](#flask)
- [Morepath](#morepath)
- [Pyramid](#pyramid)
- [Quart](#quart)
- [Sanic](#sanic)
- [Starlette](#starlette)
- [Tornado](#tornado)
- [TurboGears](#turbogears)
- [Web2py](#web2py)
- [Custom Frameworks](#custom-frameworks)

---

## aiohttp

**[aiohttp](https://docs.aiohttp.org)** is an asynchronous HTTP client/server framework for asyncio and Python. It's designed for building efficient web applications with asynchronous capabilities.

```python
from aiohttp import web

from secure import Secure

secure_headers = Secure.with_default_headers()


async def handle(request):
    return web.Response(text="Hello, world")


@web.middleware
async def add_security_headers(request, handler):
    response = await handler(request)
    secure_headers.set_headers(response)
    return response


app = web.Application(middlewares=[add_security_headers])

app.router.add_get("/", handle)

web.run_app(app)
```

---

## Bottle

**[Bottle](https://bottlepy.org)** is a fast, simple, and lightweight WSGI micro web-framework for Python. It's perfect for small applications and rapid prototyping.

```python
from bottle import Bottle, response, run

from secure import Secure

secure_headers = Secure.with_default_headers()
app = Bottle()


@app.hook("after_request")
def add_security_headers():
    secure_headers.set_headers(response)


@app.route("/")
def index():
    return "Hello, world"


run(app, host="localhost", port=8080)
```

---

## Django

**[Django](https://www.djangoproject.com)** is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It's widely used and has a rich ecosystem.

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

**[Falcon](https://falconframework.org)** is a minimalist WSGI library for building speedy web APIs and app backends. It's designed to be fast, reliable, and extensible.

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

**[FastAPI](https://fastapi.tiangolo.com)** is a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints. It's known for its speed and ease of use.

```python
from fastapi import FastAPI

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

**[Flask](https://flask.palletsprojects.com/)** is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.

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

## Morepath

**[Morepath](https://morepath.readthedocs.io)** is a Python web framework with superpowers. It is an expressive model-driven microframework providing URL to object mapping, and more.

```python
import morepath

from secure import Secure


class App(morepath.App):
    pass


secure_headers = Secure.with_default_headers()


@App.path(path="")
class Root:
    pass


@App.view(model=Root)
def hello_world(self, request):
    response = morepath.Response("Hello, world")
    secure_headers.set_headers(response)
    return response


if __name__ == "__main__":
    morepath.run(App())
```

---

## Pyramid

**[Pyramid](https://trypyramid.com)** is a small, fast, down-to-earth Python web framework. It is minimalistic, offering only the core tools needed to build web applications.

```python
from pyramid.config import Configurator
from pyramid.response import Response

from secure import Secure

secure_headers = Secure.with_default_headers()


def hello_world(request):
    response = Response("Hello, world")
    secure_headers.set_headers(response)
    return response


if __name__ == "__main__":
    with Configurator() as config:
        config.add_route("home", "/")
        config.add_view(hello_world, route_name="home")
        app = config.make_wsgi_app()

    from waitress import serve

    serve(app, listen="0.0.0.0:8000")

```

---

## Quart

**[Quart](https://pgjones.gitlab.io/quart/)** is an async Python web framework and is a drop-in replacement for Flask, offering the same API but with async capabilities.

```python
from quart import Quart, Response

from secure import Secure

app = Quart(__name__)
secure_headers = Secure.with_default_headers()


@app.after_request
async def add_security_headers(response: Response):
    secure_headers.set_headers(response)
    return response


@app.route("/")
async def index():
    return "Hello, world"


app.run()
```

---

## Sanic

**[Sanic](https://sanicframework.org)** is a Python 3.7+ web server and web framework that's written to go fast. It allows for the handling of asynchronous requests.

```python
from sanic import Sanic, response

from secure import Secure

app = Sanic("SecureApp")
secure_headers = Secure.with_default_headers()


@app.middleware("response")
async def add_security_headers(request, resp):
    secure_headers.set_headers(resp)


@app.route("/")
async def index(request):
    return response.text("Hello, world")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, workers=1)
```

---

## Starlette

**[Starlette](https://www.starlette.io/)** is a lightweight ASGI framework/toolkit, which is ideal for building high-performance async services. It's the foundation of FastAPI.

```python
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

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

**[Tornado](https://www.tornadoweb.org/)** is a Python web framework and asynchronous networking library, originally developed at FriendFeed. It's known for its high performance and scalability.

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
    return tornado.web.Application(
        [
            (r"/", MainHandler),
        ]
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
```

---

## TurboGears

**[TurboGears](https://turbogears.org/)** is a full-stack framework for rapid development of modern, data-driven web applications. It combines the best ideas from the worlds of Ruby and Python.

```python
from tg import AppConfig, Response, TGController, expose

from secure import Secure

secure_headers = Secure.with_default_headers()


class RootController(TGController):
    @expose(content_type="text/plain")
    def index(self):
        response = Response("Hello, world")
        secure_headers.set_headers(response)
        return response


if __name__ == "__main__":
    config = AppConfig(minimal=True, root_controller=RootController())
    config.renderers = ["json"]
    config["package"] = __name__

    app = config.make_wsgi_app()

    # Run the TurboGears app using a WSGI server
    from wsgiref.simple_server import make_server

    httpd = make_server("127.0.0.1", 8080, app)
    print("Serving on port 8080...")
    httpd.serve_forever()
```

---

## Web2py

**[Web2py](http://www.web2py.com/)** is a free, open-source web framework for agile development of secure database-driven web applications. It follows a Model-View-Controller (MVC) design.

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
