from typing import Any

from secure.secure import Secure


class Framework:
    """Secure supported frameworks."""

    def __init__(self, secure: Secure) -> None:
        self.secure = secure

    def aiohttp(self, response: Any) -> None:
        """Update Secure Headers to aiohttp response object."""
        self.secure.set_headers(response)

    def bottle(self, response: Any) -> None:
        """Update Secure Headers to Bottle response object."""
        self.secure.set_headers(response)

    def cherrypy(self) -> list[tuple[str, str]]:
        """Return tuple of Secure Headers for CherryPy."""
        headers = self.secure.headers
        tuple_headers = list(headers.items())
        return tuple_headers

    def django(self, response: Any) -> None:
        """Update Secure Headers to Django response object."""
        self.secure.set_headers(response)

    def falcon(self, response: Any) -> None:
        """Update Secure Headers to Falcon response object."""
        self.secure.set_headers(response, use_set_header=True)

    def flask(self, response: Any) -> None:
        """Update Secure Headers to Flask response object."""
        self.secure.set_headers(response)

    def fastapi(self, response: Any) -> None:
        """Update Secure Headers to FastAPI response object."""
        self.secure.set_headers(response)

    def hug(self, response: Any) -> None:
        """Update Secure Headers to Hug response object."""
        self.secure.set_headers(response, use_set_header=True)

    def masonite(self, request: Any) -> None:
        """Update Secure Headers to Masonite request object."""
        try:
            request.header(self.secure.headers)
        except AttributeError as e:
            print(f"Failed to set headers on Masonite request: {e}")

    def pyramid(self, response: Any) -> None:
        """Update Secure Headers to Pyramid response object."""
        self.secure.set_headers(response)

    def quart(self, response: Any) -> None:
        """Update Secure Headers to Quart response object."""
        self.secure.set_headers(response)

    def responder(self, response: Any) -> None:
        """Update Secure Headers to Responder response object."""
        self.secure.set_headers(response)

    def sanic(self, response: Any) -> None:
        """Update Secure Headers to Sanic response object."""
        self.secure.set_headers(response)

    def starlette(self, response: Any) -> None:
        """Update Secure Headers to Starlette response object."""
        self.secure.set_headers(response)

    def tornado(self, response: Any) -> None:
        """Update Secure Headers to Tornado RequestHandler object."""
        self.secure.set_headers(response, use_set_header=True)
