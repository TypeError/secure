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

    The response object should have a `headers` dictionary.
    """

    headers: dict[str, str]


class Secure:
    """A class to configure and apply security headers for web applications."""

    def __init__(
        self,
        *,
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
        """Initialize the Secure instance with the specified security headers."""
        self.headers_list: list[BaseHeader] = [
            header
            for header in (
                server,
                hsts,
                xfo,
                content,
                csp,
                referrer,
                cache,
                permissions,
                coop,
                ceop,
            )
            if header is not None
        ]

        # Add custom headers if provided
        if custom:
            self.headers_list.extend(custom)

    @classmethod
    def with_default_headers(cls) -> Secure:
        """Create a `Secure` instance with a default set of common security headers."""
        return cls(
            hsts=StrictTransportSecurity().max_age(31536000).include_subdomains(),
            xfo=XFrameOptions().deny(),
            content=XContentTypeOptions().nosniff(),
            csp=ContentSecurityPolicy().default_src("'self'"),
            referrer=ReferrerPolicy().no_referrer_when_downgrade(),
            permissions=PermissionsPolicy().camera("'none'").microphone("'none'"),
        )

    @classmethod
    def from_preset(cls, preset: Preset) -> Secure:
        """Create a `Secure` instance using a predefined security preset."""
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
            if hasattr(response, "headers"):
                response.headers[header_name] = header_value
            elif hasattr(response, "set_header"):
                set_header = cast(
                    Callable[[str, str], Any], getattr(response, "set_header")
                )
                if inspect.iscoroutinefunction(set_header):
                    raise RuntimeError(
                        "Encountered asynchronous 'set_header' in synchronous context."
                    )
                set_header(header_name, header_value)
            else:
                raise AttributeError(
                    f"Response object of type '{type(response).__name__}' does not support setting headers."
                )

    async def set_headers_async(self, response: ResponseProtocol) -> None:
        """Set security headers on the response object asynchronously."""
        for header_name, header_value in self.headers.items():
            if hasattr(response, "headers"):
                response.headers[header_name] = header_value
            elif hasattr(response, "set_header"):
                set_header = cast(
                    Callable[[str, str], Any], getattr(response, "set_header")
                )
                if inspect.iscoroutinefunction(set_header):
                    await set_header(header_name, header_value)
                else:
                    set_header(header_name, header_value)
            else:
                raise AttributeError(
                    f"Response object of type '{type(response).__name__}' does not support setting headers."
                )
