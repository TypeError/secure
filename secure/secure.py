from __future__ import annotations

import inspect
from collections.abc import MutableMapping
from enum import Enum
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


@runtime_checkable
class HeadersProtocol(Protocol):
    """Protocol for response objects that have a 'headers' attribute."""

    headers: MutableMapping[str, str]


@runtime_checkable
class SetHeaderProtocol(Protocol):
    """Protocol for response objects that have a 'set_header' method."""

    def set_header(self, key: str, value: str) -> Any: ...


ResponseProtocol = HeadersProtocol | SetHeaderProtocol
"""
Union type for response objects that conform to either HeadersProtocol or SetHeaderProtocol.
This allows the Secure class to work with a variety of web frameworks.
"""


class Preset(Enum):
    """Enumeration of predefined security presets for the Secure class."""

    BASIC = "basic"
    STRICT = "strict"


class Secure:
    """
    A class to configure and apply security headers for web applications.

    The Secure class allows you to specify various HTTP security headers to enhance
    the security of your web application. You can use predefined presets or customize
    the headers as needed.

    Attributes:
        headers_list (list[BaseHeader]): List of header objects representing the configured headers.
    """

    def __init__(
        self,
        *,
        cache: CacheControl | None = None,
        coep: CrossOriginEmbedderPolicy | None = None,
        coop: CrossOriginOpenerPolicy | None = None,
        csp: ContentSecurityPolicy | None = None,
        custom: list[CustomHeader] | None = None,
        hsts: StrictTransportSecurity | None = None,
        permissions: PermissionsPolicy | None = None,
        referrer: ReferrerPolicy | None = None,
        server: Server | None = None,
        xcto: XContentTypeOptions | None = None,
        xfo: XFrameOptions | None = None,
    ) -> None:
        """
        Initialize the Secure instance with the specified security headers.

        Args:
            cache (CacheControl | None): The Cache-Control header configuration.
            coep (CrossOriginEmbedderPolicy | None): The Cross-Origin-Embedder-Policy header configuration.
            coop (CrossOriginOpenerPolicy | None): The Cross-Origin-Opener-Policy header configuration.
            csp (ContentSecurityPolicy | None): The Content-Security-Policy header configuration.
            custom (list[CustomHeader] | None): A list of custom headers to include.
            hsts (StrictTransportSecurity | None): The Strict-Transport-Security header configuration.
            permissions (PermissionsPolicy | None): The Permissions-Policy header configuration.
            referrer (ReferrerPolicy | None): The Referrer-Policy header configuration.
            server (Server | None): The Server header configuration.
            xcto (XContentTypeOptions | None): The X-Content-Type-Options header configuration.
            xfo (XFrameOptions | None): The X-Frame-Options header configuration.
        """
        # Store headers in the order defined by the parameters
        self.headers_list: list[BaseHeader] = []
        # List of header parameters in the desired order
        params = [
            cache,
            coep,
            coop,
            csp,
            hsts,
            permissions,
            referrer,
            server,
            xcto,
            xfo,
        ]

        # Append non-None headers to the headers list
        for header in params:
            if header is not None:
                self.headers_list.append(header)

        # Add custom headers if provided
        if custom:
            self.headers_list.extend(custom)

    @classmethod
    def with_default_headers(cls) -> Secure:
        """
        Create a Secure instance with a default set of common security headers.

        Returns:
            Secure: An instance of Secure with default security headers configured.
        """
        return cls(
            cache=CacheControl().no_store(),
            coop=CrossOriginOpenerPolicy().same_origin(),
            csp=ContentSecurityPolicy()
            .default_src("'self'")
            .script_src("'self'")
            .style_src("'self'")
            .object_src("'none'"),
            hsts=StrictTransportSecurity().max_age(31536000),
            permissions=PermissionsPolicy().geolocation().microphone().camera(),
            referrer=ReferrerPolicy().strict_origin_when_cross_origin(),
            server=Server().set(""),
            xcto=XContentTypeOptions().nosniff(),
            xfo=XFrameOptions().sameorigin(),
        )

    @classmethod
    def from_preset(cls, preset: Preset) -> Secure:
        """
        Create a Secure instance using a predefined security preset.

        Args:
            preset (Preset): The security preset to use (Preset.BASIC or Preset.STRICT).

        Returns:
            Secure: An instance of Secure configured with the selected preset.

        Raises:
            ValueError: If an unknown preset is provided.
        """
        match preset:
            case Preset.BASIC:
                return cls(
                    cache=CacheControl().no_store(),
                    hsts=StrictTransportSecurity().max_age(31536000),
                    referrer=ReferrerPolicy().strict_origin_when_cross_origin(),
                    server=Server().set(""),
                    xcto=XContentTypeOptions().nosniff(),
                    xfo=XFrameOptions().sameorigin(),
                )
            case Preset.STRICT:
                return cls(
                    cache=CacheControl().no_store(),
                    coep=CrossOriginEmbedderPolicy().require_corp(),
                    coop=CrossOriginOpenerPolicy().same_origin(),
                    csp=ContentSecurityPolicy()
                    .default_src("'self'")
                    .script_src("'self'")
                    .style_src("'self'")
                    .object_src("'none'")
                    .base_uri("'none'")
                    .frame_ancestors("'none'"),
                    hsts=StrictTransportSecurity()
                    .max_age(63072000)
                    .include_subdomains()
                    .preload(),
                    permissions=PermissionsPolicy().geolocation().microphone().camera(),
                    referrer=ReferrerPolicy().no_referrer(),
                    server=Server().set(""),
                    xcto=XContentTypeOptions().nosniff(),
                    xfo=XFrameOptions().deny(),
                )
            case _:  # type: ignore
                raise ValueError(f"Unknown preset: {preset}")

    def __str__(self) -> str:
        """
        Return a string representation of the security headers.

        Returns:
            str: A string listing the headers and their values.
        """
        return "\n".join(
            f"{header.header_name}: {header.header_value}"
            for header in self.headers_list
        )

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the Secure instance.

        Returns:
            str: A string representation including the list of headers.
        """
        return f"{self.__class__.__name__}(headers_list={self.headers_list!r})"

    @cached_property
    def headers(self) -> dict[str, str]:
        """
        Collect all configured headers as a dictionary.

        Returns:
            dict[str, str]: A dictionary mapping header names to their values.
        """
        return {header.header_name: header.header_value for header in self.headers_list}

    def set_headers(self, response: ResponseProtocol) -> None:
        """
        Set security headers on the response object synchronously.

        The method checks for the presence of a 'set_header' method or 'headers' attribute
        on the response object to set the headers appropriately.

        Args:
            response (ResponseProtocol): The response object to modify.

        Raises:
            RuntimeError: If an asynchronous 'set_header' method is used in a synchronous context.
            AttributeError: If the response object does not support setting headers.
        """
        if isinstance(response, SetHeaderProtocol):
            # Use the set_header method if available
            set_header = response.set_header
            if inspect.iscoroutinefunction(set_header):
                raise RuntimeError(
                    "Encountered asynchronous 'set_header' in synchronous context."
                )
            for header_name, header_value in self.headers.items():
                set_header(header_name, header_value)
        elif isinstance(response, HeadersProtocol):  # type: ignore
            # Use the headers dictionary if available
            for header_name, header_value in self.headers.items():
                response.headers[header_name] = header_value
        else:
            raise AttributeError(
                f"Response object of type '{type(response).__name__}' does not support setting headers."
            )

    async def set_headers_async(self, response: ResponseProtocol) -> None:
        """
        Set security headers on the response object asynchronously.

        This method handles both synchronous and asynchronous 'set_header' methods,
        as well as response objects with a 'headers' attribute.

        Args:
            response (ResponseProtocol): The response object to modify.

        Raises:
            AttributeError: If the response object does not support setting headers.
        """
        if isinstance(response, SetHeaderProtocol):
            # Use the set_header method if available
            set_header = response.set_header
            if inspect.iscoroutinefunction(set_header):
                for header_name, header_value in self.headers.items():
                    await set_header(header_name, header_value)
            else:
                for header_name, header_value in self.headers.items():
                    set_header(header_name, header_value)
        elif isinstance(response, HeadersProtocol):  # type: ignore
            # Use the headers dictionary if available
            for header_name, header_value in self.headers.items():
                response.headers[header_name] = header_value
        else:
            raise AttributeError(
                f"Response object of type '{type(response).__name__}' does not support setting headers."
            )
