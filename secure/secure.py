from __future__ import annotations

import inspect
from functools import cached_property
from typing import Any, Protocol, runtime_checkable

from .headers import (
    BaseHeader,
    CacheControl,
    ContentSecurityPolicy,
    CrossOriginEmbedderPolicy,
    CrossOriginOpenerPolicy,
    CustomHeader,
    PermissionsPolicy,
    ReferrerPolicy,
    Server,
    StrictTransportSecurity,
    XContentTypeOptions,
    XFrameOptions,
)


class Preset(Enum):
    BASIC = "basic"
    STRICT = "strict"
    CUSTOM = "custom"


@runtime_checkable
class ResponseProtocol(Protocol):
    """Protocol to define the expected interface of the response object."""

    headers: dict[str, str]

    def set_header(self, header_name: str, header_value: str) -> Any: ...


class Secure:
    """Set Secure Header options.

    :param server: Server header options
    :param hsts: Strict-Transport-Security (HSTS) header options
    :param xfo: X-Frame-Options header options
    :param content: X-Content-Type-Options header options
    :param csp: Content-Security-Policy header options
    :param referrer: Referrer-Policy header options
    :param cache: Cache-Control header options
    :param permissions: Permissions-Policy header options
    :param coop: Cross-Origin-Opener-Policy header options
    :param ceop: Cross-Origin-Embedder-Policy header options
    :param custom: List of custom headers

    **Usage with Django:**

    ```python
    secure_headers = Secure()
    response = HttpResponse()
    secure_headers.set_headers(response)
    ```

    **Usage with FastAPI:**

    ```python
    secure_headers = Secure()
    @app.get("/")
    async def read_root():
        response = JSONResponse(content={"message": "Hello World"})
        await secure_headers.set_headers_async(response)
        return response
    ```
    """

    __slots__ = ("headers_list",)

    def __init__(
        self,
        server: Server | None = None,
        hsts: StrictTransportSecurity | None = None,
        xfo: XFrameOptions | None = None,
        content: XContentTypeOptions | None = None,
        csp: ContentSecurityPolicy | None = None,
        referrer: ReferrerPolicy | None = None,
        cache: CacheControl | None = None,
        permissions: PermissionsPolicy | None = None,
        coop: CrossOriginOpenerPolicy | None = None,
        ceop: CrossOriginEmbedderPolicy | None = None,
        custom: list[CustomHeader] | None = None,
    ) -> None:
        # Initialize the list of header instances
        self.headers_list: list[BaseHeader] = []

        # Add only provided headers, no defaults here
        headers = {
            "server": server,
            "hsts": hsts,
            "xfo": xfo,
            "content": content,
            "csp": csp,
            "referrer": referrer,
            "cache": cache,
            "permissions": permissions,
            "coop": coop,
            "ceop": ceop,
        }

        for header in headers.values():
            if header is not None:
                self.headers_list.append(header)

        # Add custom headers if provided
        if custom:
            self.headers_list.extend(custom)

    @classmethod
    def with_default_headers(cls) -> Secure:
        """Create a Secure instance using a default set of common security headers."""
        return cls(
            # HSTS with a max age of 1 year and include subdomains
            hsts=StrictTransportSecurity().max_age(31536000).include_subdomains(),
            # X-Frame-Options set to 'DENY'
            xfo=XFrameOptions().deny(),
            # X-Content-Type-Options set to 'nosniff'
            content=XContentTypeOptions().nosniff(),
            # Content-Security-Policy with default-src 'self'
            csp=ContentSecurityPolicy().default_src("'self'"),
            # Referrer-Policy set to 'no-referrer-when-downgrade'
            referrer=ReferrerPolicy().no_referrer_when_downgrade(),
            # Permissions-Policy disabling camera and microphone
            permissions=PermissionsPolicy().camera("'none'").microphone("'none'"),
        )

    def __str__(self) -> str:
        return "\n".join(
            f"{header.header_name}: {header.header_value}"
            for header in self.headers_list
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(headers_list={self.headers_list!r})"

    @cached_property
    def headers(self) -> dict[str, str]:
        """Collects all the headers as a dictionary."""
        return {header.header_name: header.header_value for header in self.headers_list}

    def set_headers(self, response: ResponseProtocol) -> None:
        """Set headers on the response object synchronously.

        :param response: Response object that supports setting headers.
        """
        self._apply_headers(response, is_async=False)

    async def set_headers_async(self, response: ResponseProtocol) -> None:
        """Set headers on the response object asynchronously.

        :param response: Response object that supports setting headers.
        """
        await self._apply_headers(response, is_async=True)

    def _set_header(
        self, response: ResponseProtocol, header_name: str, header_value: str
    ) -> None:
        """Helper method to set a single header."""
        if hasattr(response, "set_header"):
            set_header = response.set_header
            set_header(header_name, header_value)
        elif hasattr(response, "headers"):
            response.headers[header_name] = header_value
        else:
            raise AttributeError(
                f"The response object of type '{type(response).__name__}' does not support setting headers."
            )

    def _apply_headers(self, response: ResponseProtocol, is_async: bool) -> Any:
        """Internal method to apply headers to the response object.

        :param response: Response object that supports setting headers.
        :param is_async: Indicates whether to handle asynchronous operations.
        """
        if is_async:
            return self._apply_headers_async(response)

        for header_name, header_value in self.headers.items():
            self._set_header(response, header_name, header_value)

    async def _apply_headers_async(self, response: ResponseProtocol) -> None:
        """Internal async method to apply headers to the response object.

        :param response: Response object that supports setting headers asynchronously.
        """
        for header_name, header_value in self.headers.items():
            if hasattr(response, "set_header"):
                set_header = response.set_header
                if inspect.iscoroutinefunction(set_header):
                    await set_header(header_name, header_value)
                else:
                    set_header(header_name, header_value)
            elif hasattr(response, "headers"):
                response.headers[header_name] = header_value
            else:
                raise AttributeError(
                    f"The response object of type '{type(response).__name__}' does not support setting headers."
                )

    @classmethod
    def from_preset(cls, preset: Preset) -> Secure:
        match preset:
            case Preset.BASIC:
                return cls(
                    hsts=StrictTransportSecurity().max_age(63072000),
                    xfo=XFrameOptions().sameorigin(),
                    referrer=ReferrerPolicy().no_referrer_when_downgrade(),
                )
            case Preset.STRICT:
                return cls(
                    hsts=StrictTransportSecurity()
                    .max_age(31536000)
                    .include_subdomains()
                    .preload(),
                    xfo=XFrameOptions().deny(),
                    referrer=ReferrerPolicy().no_referrer(),
                    csp=ContentSecurityPolicy().default_src("'self'"),
                )
            case Preset.CUSTOM:
                return cls()
