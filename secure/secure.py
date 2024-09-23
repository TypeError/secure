from __future__ import annotations

import inspect
from collections.abc import Callable
from enum import Enum
from functools import cached_property
from typing import Any, Protocol, cast, runtime_checkable

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
    """Enumeration of predefined security presets."""

    BASIC = "basic"
    STRICT = "strict"


@runtime_checkable
class ResponseProtocol(Protocol):
    """Protocol defining the expected interface of a response object.

    The response object should have a `headers` dictionary or a `set_header` method.
    """

    headers: dict[str, str]

    def set_header(self, key: str, value: str) -> Any: ...


class Secure:
    """A class to configure and apply security headers for web applications."""

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
        """Initialize the Secure instance with the specified security headers."""
        # Store headers in the order defined by the parameters
        self.headers_list: list[BaseHeader] = []
        # Using the order of parameters in the function signature
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

        for header in params:
            if header is not None:
                self.headers_list.append(header)

        # Add custom headers if provided
        if custom:
            self.headers_list.extend(custom)

    @classmethod
    def with_default_headers(cls) -> Secure:
        """Create a `Secure` instance with a default set of common security headers."""
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
        """Create a `Secure` instance using a predefined security preset."""
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
        """Return a string representation of the security headers."""
        return "\n".join(
            f"{header.header_name}: {header.header_value}"
            for header in self.headers_list
        )

    def __repr__(self) -> str:
        """Return a detailed string representation of the `Secure` instance."""
        return f"{self.__class__.__name__}(headers_list={self.headers_list!r})"

    @cached_property
    def headers(self) -> dict[str, str]:
        """Collect all configured headers as a dictionary."""
        return {header.header_name: header.header_value for header in self.headers_list}

    def set_headers(self, response: ResponseProtocol) -> None:
        """Set security headers on the response object synchronously."""
        for header_name, header_value in self.headers.items():
            if hasattr(response, "set_header"):
                set_header = cast(
                    Callable[[str, str], Any], getattr(response, "set_header")
                )
                if inspect.iscoroutinefunction(set_header):
                    raise RuntimeError(
                        "Encountered asynchronous 'set_header' in synchronous context."
                    )
                set_header(header_name, header_value)  # Use set_header if present
            elif hasattr(response, "headers"):
                response.headers[header_name] = header_value  # Fallback to headers
            else:
                raise AttributeError(
                    f"Response object of type '{type(response).__name__}' does not support setting headers."
                )

    async def set_headers_async(self, response: ResponseProtocol) -> None:
        """Set security headers on the response object asynchronously."""
        for header_name, header_value in self.headers.items():
            if hasattr(response, "set_header"):
                set_header = cast(
                    Callable[[str, str], Any], getattr(response, "set_header")
                )
                if inspect.iscoroutinefunction(set_header):
                    await set_header(header_name, header_value)  # Use async set_header
                else:
                    set_header(header_name, header_value)  # Use synchronous set_header
            elif hasattr(response, "headers"):
                response.headers[header_name] = header_value  # Fallback to headers
            else:
                raise AttributeError(
                    f"Response object of type '{type(response).__name__}' does not support setting headers."
                )
