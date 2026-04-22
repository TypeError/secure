# Framework Integration

`secure` keeps the same `Secure` object across frameworks. What changes is how you attach it.

## How to choose an integration style

- Use `set_headers()` when the response object is synchronous and you are already inside a response hook, middleware callback, or view.
- Use `set_headers_async()` in async code when the response object may expose async setters, or when you want one helper that works safely in async integrations.
- Use `SecureWSGIMiddleware` when you want app-wide coverage and can wrap a WSGI application directly.
- Use `SecureASGIMiddleware` when you want app-wide coverage in an ASGI stack such as FastAPI, Starlette, or Shiny.

Prefer middleware when your framework makes it easy. Use per-response setters when you are integrating into an existing hook or only securing part of an application.

## Uvicorn `Server` header

Uvicorn adds `Server: uvicorn` by default. If you want `secure` to control the `Server` header, disable Uvicorn's default header with `--no-server-header` or `server_header=False`.

```python
import uvicorn

uvicorn.run(app, host="0.0.0.0", port=8000, server_header=False)
```

## Table of contents

- [aiohttp](#aiohttp)
- [Bottle](#bottle)
- [CherryPy](#cherrypy)
- [Custom frameworks](#custom-frameworks)
- [Dash](#dash)
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
- [Shiny](#shiny)
- [Starlette](#starlette)
- [Tornado](#tornado)
- [TurboGears](#turbogears)

## aiohttp

Async framework with first-class middleware support.

### Recommended: middleware with `set_headers_async()`

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
```

### Alternative: set headers in a single handler

```python
from aiohttp import web
from secure import Secure

secure_headers = Secure.with_default_headers()


async def home(request):
    response = web.Response(text="Hello, world")
    await secure_headers.set_headers_async(response)
    return response
```

## Bottle

Small WSGI framework with request hooks.

### Recommended: `after_request` hook with `set_headers()`

```python
from bottle import Bottle, response
from secure import Secure

app = Bottle()
secure_headers = Secure.with_default_headers()


@app.hook("after_request")
def add_security_headers():
    secure_headers.set_headers(response)
```

### Fallback: set headers in a route

```python
from bottle import Bottle, response
from secure import Secure

app = Bottle()
secure_headers = Secure.with_default_headers()


@app.route("/")
def home():
    secure_headers.set_headers(response)
    return "Hello, world"
```

## CherryPy

Object-oriented framework where the response object is available in the handler.

### Fallback: set headers in the exposed method

```python
import cherrypy
from secure import Secure

secure_headers = Secure.with_default_headers()


class App:
    @cherrypy.expose
    def index(self):
        secure_headers.set_headers(cherrypy.response)
        return b"Hello, world"


cherrypy.quickstart(App())
```

## Custom frameworks

If your framework is not listed here, the integration rule is still simple: configure one `Secure` instance, then apply it to the response as late as possible before it is sent.

### Recommended: use the response object's setter or headers mapping

```python
from secure import Secure

secure_headers = Secure.with_default_headers()


def add_security_headers(response):
    secure_headers.set_headers(response)
    return response
```

### Fallback: emit header pairs manually

```python
from secure import Secure

secure_headers = Secure.with_default_headers()

for name, value in secure_headers.header_items():
    response.headers[name] = value
```

## Dash

Dash runs on top of Flask, so the usual Flask integration patterns apply.

### Recommended: Flask `after_request` on `app.server`

```python
import dash
from dash import html
from secure import Secure

app = dash.Dash(__name__)
server = app.server
secure_headers = Secure.with_default_headers()

app.layout = html.Div("Hello Dash!")


@server.after_request
def add_security_headers(response):
    secure_headers.set_headers(response)
    return response
```

### Alternative: `SecureWSGIMiddleware`

```python
import dash
from dash import html
from secure import Secure
from secure.middleware import SecureWSGIMiddleware

app = dash.Dash(__name__)
server = app.server
secure_headers = Secure.with_default_headers()

app.layout = html.Div("Hello Dash!")
server.wsgi_app = SecureWSGIMiddleware(server.wsgi_app, secure=secure_headers)
```

## Django

Django is usually best integrated through Django middleware rather than raw WSGI wrapping.

### Recommended: Django middleware class

```python
from secure import Secure


class SecureHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.secure = Secure.with_default_headers()

    def __call__(self, request):
        response = self.get_response(request)
        self.secure.set_headers(response)
        return response
```

### Fallback: set headers in a view

```python
from django.http import HttpResponse
from secure import Secure

secure_headers = Secure.with_default_headers()


def home(request):
    response = HttpResponse("Hello, world")
    secure_headers.set_headers(response)
    return response
```

## Falcon

Falcon exposes a clean response middleware hook.

### Recommended: Falcon middleware

```python
import falcon
from secure import Secure

secure_headers = Secure.with_default_headers()


class SecureMiddleware:
    def process_response(self, req, resp, resource, req_succeeded):
        secure_headers.set_headers(resp)


app = falcon.App(middleware=[SecureMiddleware()])
```

### Fallback: set headers in the resource

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

## FastAPI

ASGI framework. Middleware is the clearest default.

### Recommended: `SecureASGIMiddleware`

```python
from fastapi import FastAPI
from secure import Secure
from secure.middleware import SecureASGIMiddleware

app = FastAPI()
secure_headers = Secure.with_default_headers()

app.add_middleware(SecureASGIMiddleware, secure=secure_headers)
```

### Alternative: `@app.middleware("http")`

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

### Fallback: set headers in one route

```python
from fastapi import FastAPI, Response
from secure import Secure

app = FastAPI()
secure_headers = Secure.with_default_headers()


@app.get("/")
def home(response: Response):
    secure_headers.set_headers(response)
    return {"hello": "world"}
```

## Flask

WSGI framework with a straightforward response hook.

### Recommended: `after_request`

```python
from flask import Flask
from secure import Secure

app = Flask(__name__)
secure_headers = Secure.with_default_headers()


@app.after_request
def add_security_headers(response):
    secure_headers.set_headers(response)
    return response
```

### Alternative: `SecureWSGIMiddleware`

```python
from flask import Flask
from secure import Secure
from secure.middleware import SecureWSGIMiddleware

app = Flask(__name__)
secure_headers = Secure.with_default_headers()

app.wsgi_app = SecureWSGIMiddleware(app.wsgi_app, secure=secure_headers)
```

## Masonite

Minimal fallback example. Masonite routing and controller setup varies by version, so apply `Secure` to the response object you return.

### Fallback: apply to the response you return

```python
from masonite.response import Response
from secure import Secure

secure_headers = Secure.with_default_headers()


def home(response: Response):
    rendered = response.json({"hello": "world"})
    secure_headers.set_headers(rendered)
    return rendered
```

## Morepath

Minimal fallback example. Morepath does not use a conventional middleware layer for this.

### Fallback: set headers in the view

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
def home(self, request):
    response = morepath.Response("Hello, world")
    secure_headers.set_headers(response)
    return response
```

## Pyramid

Pyramid applications commonly use tweens for cross-cutting response changes.

### Recommended: tween

Register the tween in your `Configurator` with `config.add_tween("yourpackage.security.add_security_headers")`.

```python
from secure import Secure

secure_headers = Secure.with_default_headers()


def add_security_headers(handler, registry):
    def tween(request):
        response = handler(request)
        secure_headers.set_headers(response)
        return response

    return tween
```

### Fallback: set headers in a view

```python
from pyramid.response import Response
from secure import Secure

secure_headers = Secure.with_default_headers()


def home(request):
    response = Response("Hello, world")
    secure_headers.set_headers(response)
    return response
```

## Quart

Async Flask-compatible framework.

### Recommended: `after_request` with `set_headers_async()`

```python
from quart import Quart
from secure import Secure

app = Quart(__name__)
secure_headers = Secure.with_default_headers()


@app.after_request
async def add_security_headers(response):
    await secure_headers.set_headers_async(response)
    return response
```

### Fallback: set headers in a route

```python
from quart import Quart, Response
from secure import Secure

app = Quart(__name__)
secure_headers = Secure.with_default_headers()


@app.route("/")
async def home():
    response = Response("Hello, world")
    await secure_headers.set_headers_async(response)
    return response
```

## Responder

Minimal fallback example. Route handlers typically own the response.

### Fallback: set headers in the route

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

## Sanic

Sanic exposes response middleware for app-wide coverage.

### Recommended: response middleware with `set_headers_async()`

```python
from sanic import Sanic
from secure import Secure

app = Sanic("secure-app")
secure_headers = Secure.with_default_headers()


@app.middleware("response")
async def add_security_headers(request, response):
    await secure_headers.set_headers_async(response)
    return response
```

### Fallback: set headers in a route

```python
from sanic import Sanic, response
from secure import Secure

app = Sanic("secure-app")
secure_headers = Secure.with_default_headers()


@app.get("/")
async def home(request):
    resp = response.text("Hello, world")
    await secure_headers.set_headers_async(resp)
    return resp
```

## Shiny

Shiny applications are ASGI apps, so ASGI middleware is the cleanest path.

### Recommended: `SecureASGIMiddleware`

```python
from secure import Secure
from secure.middleware import SecureASGIMiddleware
from shiny import App, ui

secure_headers = Secure.with_default_headers()

app_ui = ui.page_fluid("Hello Shiny!")


def server(input, output, session):
    pass


app = App(app_ui, server)
app = SecureASGIMiddleware(app, secure=secure_headers)
```

## Starlette

ASGI framework. Use ASGI middleware unless you only need route-level control.

### Recommended: `SecureASGIMiddleware`

```python
from secure import Secure
from secure.middleware import SecureASGIMiddleware
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route

secure_headers = Secure.with_default_headers()


async def home(request):
    return PlainTextResponse("Hello, world")


app = Starlette(routes=[Route("/", home)])
app.add_middleware(SecureASGIMiddleware, secure=secure_headers)
```

### Alternative: set headers in an endpoint

```python
from secure import Secure
from starlette.applications import Starlette
from starlette.responses import Response
from starlette.routing import Route

secure_headers = Secure.with_default_headers()


async def home(request):
    response = Response("Hello, world")
    await secure_headers.set_headers_async(response)
    return response


app = Starlette(routes=[Route("/", home)])
```

## Tornado

Tornado usually applies headers inside request handlers.

### Fallback: set headers in the handler

```python
import tornado.web
from secure import Secure

secure_headers = Secure.with_default_headers()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
        secure_headers.set_headers(self)
```

## TurboGears

Minimal fallback example. If you do not already have a framework-level hook in place, apply headers in the controller response path.

### Fallback: set headers in the controller

```python
from tg import Response, TGController, expose
from secure import Secure

secure_headers = Secure.with_default_headers()


class RootController(TGController):
    @expose()
    def index(self):
        response = Response("Hello, world")
        secure_headers.set_headers(response)
        return response
```
