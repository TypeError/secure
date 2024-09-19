from __future__ import annotations

import inspect
from functools import cached_property
from typing import Any, Protocol, runtime_checkable

from secure.headers.custom_header import CustomHeader

from .headers import (
    cache_control,
    content_security_policy,
    cross_origin_embedder_policy,
    cross_origin_opener_policy,
    permissions_policy,
    referrer_policy,
    server,
    strict_transport_security,
    x_content_type_options,
    x_frame_options,
)
from .headers.base_header import BaseHeader


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
        server: server.Server | None = None,
        hsts: strict_transport_security.StrictTransportSecurity | None = None,
        xfo: x_frame_options.XFrameOptions | None = None,
        content: x_content_type_options.XContentTypeOptions | None = None,
        csp: content_security_policy.ContentSecurityPolicy | None = None,
        referrer: referrer_policy.ReferrerPolicy | None = None,
        cache: cache_control.CacheControl | None = None,
        permissions: permissions_policy.PermissionsPolicy | None = None,
        coop: cross_origin_opener_policy.CrossOriginOpenerPolicy | None = None,
        ceop: cross_origin_embedder_policy.CrossOriginEmbedderPolicy | None = None,
        custom: list[CustomHeader] | None = None,
    ) -> None:
        # Initialize the list of header instances
        self.headers_list: list[BaseHeader] = []

        # Add headers with defaults or provided values
        if server is not None:
            self.headers_list.append(server)
        self.headers_list.append(
            hsts or strict_transport_security.StrictTransportSecurity()
        )
        self.headers_list.append(xfo or x_frame_options.XFrameOptions())
        self.headers_list.append(
            content or x_content_type_options.XContentTypeOptions()
        )
        if csp is not None:
            self.headers_list.append(csp)
        self.headers_list.append(referrer or referrer_policy.ReferrerPolicy())
        if cache is not None:
            self.headers_list.append(cache)
        if permissions is not None:
            self.headers_list.append(permissions)
        self.headers_list.append(
            coop or cross_origin_opener_policy.CrossOriginOpenerPolicy()
        )
        if ceop is not None:
            self.headers_list.append(ceop)

        # Add custom headers if provided
        if custom:
            self.headers_list.extend(custom)

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
