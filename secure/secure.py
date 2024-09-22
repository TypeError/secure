from __future__ import annotations

import inspect
from enum import Enum
from functools import cached_property
from typing import Protocol, runtime_checkable

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

    The response object should have a `headers` dictionary and an optional
    `set_header` method to set headers individually.
    """

    headers: dict[str, str]

    def set_header(self, header_name: str, header_value: str) -> None: ...


class Secure:
    """A class to configure and apply security headers for web applications.

    The `Secure` class provides a simple interface to configure and apply
    a comprehensive set of HTTP security headers to protect web applications
    from various security threats such as cross-site scripting (XSS), clickjacking,
    MIME-sniffing vulnerabilities, and more.

    It supports headers like Strict-Transport-Security (HSTS), Content-Security-Policy (CSP),
    X-Frame-Options, Referrer-Policy, and others. You can configure these headers manually
    by providing their respective classes, or use built-in presets or default configurations
    for common use cases.

    Parameters:
        server (Server | None, optional): Configuration for the `Server` header to hide or modify it.
        hsts (StrictTransportSecurity | None, optional): HSTS options to enforce HTTPS.
        xfo (XFrameOptions | None, optional): X-Frame-Options to prevent clickjacking attacks.
        content (XContentTypeOptions | None, optional): X-Content-Type-Options to prevent MIME-sniffing.
        csp (ContentSecurityPolicy | None, optional): CSP to prevent XSS and content injection.
        referrer (ReferrerPolicy | None, optional): Referrer-Policy to control referrer information.
        cache (CacheControl | None, optional): Cache-Control to define caching behavior.
        permissions (PermissionsPolicy | None, optional): Permissions-Policy to control browser APIs.
        coop (CrossOriginOpenerPolicy | None, optional): COOP to mitigate cross-origin attacks.
        ceop (CrossOriginEmbedderPolicy | None, optional): COEP to control resource embedding.
        custom (list[CustomHeader] | None, optional): List of custom headers to add.

    Examples:
        **Using Default Headers:**

        ```python
        from secure import Secure

        secure_headers = Secure.with_default_headers()
        response = HttpResponse()
        secure_headers.set_headers(response)
        ```

        **Using Presets:**

        ```python
        from secure import Secure, Preset

        secure_headers = Secure.from_preset(Preset.STRICT)
        ```

        **Custom Configuration:**

        ```python
        from secure import (
            Secure,
            StrictTransportSecurity,
            XFrameOptions,
            ReferrerPolicy,
            ContentSecurityPolicy,
            PermissionsPolicy,
        )

        secure_headers = Secure(
            hsts=StrictTransportSecurity().max_age(63072000).include_subdomains(),
            xfo=XFrameOptions().sameorigin(),
            referrer=ReferrerPolicy().strict_origin_when_cross_origin(),
            csp=ContentSecurityPolicy()
                .default_src("'self'")
                .script_src("'self'", "'unsafe-inline'"),
            permissions=PermissionsPolicy().geolocation("'none'"),
        )
        ```
    """

    __slots__ = ("headers_list",)

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
        """Create a `Secure` instance with a default set of common security headers.

        This method returns a `Secure` instance configured with a recommended set of default security headers.
        These headers provide a baseline level of security for most web applications.

        The default headers included are:

        - **Strict-Transport-Security**: Enforces secure (HTTP over SSL/TLS) connections to the server.
        - **X-Frame-Options**: Protects against clickjacking attacks by controlling whether the browser should render pages in a `<frame>`, `<iframe>`, `<embed>`, or `<object>`.
        - **X-Content-Type-Options**: Prevents browsers from MIME-sniffing a response away from the declared content-type.
        - **Content-Security-Policy**: Prevents cross-site scripting (XSS), clickjacking and other code injection attacks.
        - **Referrer-Policy**: Governs which referrer information should be included with requests.
        - **Permissions-Policy**: Allows or denies the use of browser features.

        Returns:
            Secure: An instance configured with a secure set of default headers.
        """
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
        """Create a `Secure` instance using a predefined security preset.

        This method provides quick configuration of security headers using predefined presets.
        Currently, the following presets are available:

        - `Preset.BASIC`: A basic set of security headers suitable for general use.
        - `Preset.STRICT`: A stricter set of security headers for enhanced security.

        Args:
            preset (Preset): The security preset to use (`Preset.BASIC` or `Preset.STRICT`).

        Returns:
            Secure: An instance configured with the specified preset.

        Raises:
            ValueError: If an unknown preset is provided.
        """
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
        """Return a string representation of the security headers.

        Returns:
            str: A string listing all configured security headers in the format "Header-Name: Header-Value".
        """
        return "\n".join(
            f"{header.header_name}: {header.header_value}"
            for header in self.headers_list
        )

    def __repr__(self) -> str:
        """Return a detailed string representation of the `Secure` instance.

        Returns:
            str: A string representation showing the list of configured headers.
        """
        return f"{self.__class__.__name__}(headers_list={self.headers_list!r})"

    @cached_property
    def headers(self) -> dict[str, str]:
        """Collect all configured headers as a dictionary.

        Returns:
            dict[str, str]: A dictionary mapping header names to their values.
        """
        return {header.header_name: header.header_value for header in self.headers_list}

    def set_headers(self, response: ResponseProtocol) -> None:
        """Set security headers on the response object synchronously.

        This method adds the configured security headers to the given response object.
        It supports response objects that have either a `set_header` method or a `headers` dictionary attribute.

        Args:
            response (ResponseProtocol): The response object to modify.

        Raises:
            AttributeError: If the response object does not support setting headers via `set_header` method or `headers` attribute.
            RuntimeError: If an asynchronous `set_header` method is encountered in a synchronous context.
        """
        for header_name, header_value in self.headers.items():
            if hasattr(response, "set_header"):
                set_header = response.set_header
                if inspect.iscoroutinefunction(set_header):
                    raise RuntimeError(
                        "Encountered asynchronous 'set_header' in synchronous context."
                    )
                set_header(header_name, header_value)
            elif hasattr(response, "headers"):
                response.headers[header_name] = header_value
            else:
                raise AttributeError(
                    f"Response object of type '{type(response).__name__}' does not support setting headers."
                )

    async def set_headers_async(self, response: ResponseProtocol) -> None:
        """Set security headers on the response object asynchronously.

        This method adds the configured security headers to the given response object.
        It supports response objects that have either a `set_header` method or a `headers` dictionary attribute.
        If the `set_header` method is asynchronous, it awaits it; otherwise, it calls it directly.

        Args:
            response (ResponseProtocol): The response object to modify.

        Raises:
            AttributeError: If the response object does not support setting headers via `set_header` method or `headers` attribute.
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
                    f"Response object of type '{type(response).__name__}' does not support setting headers."
                )
