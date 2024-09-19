from __future__ import annotations

import asyncio
from typing import Any

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
    :param report_to: Report-To header options
    :param coop: Cross-Origin-Opener-Policy header options
    :param ceop: Cross-Origin-Embedder-Policy header options
    :param custom: List of custom headers
    """

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
        return f"Secure(headers_list={self.headers_list!r})"

    def get_headers(self) -> dict[str, str]:
        """Collects all the headers as a dictionary."""
        return {header.header_name: header.header_value for header in self.headers_list}

    def set_headers(self, response: Any) -> None:
        """Helper method to set headers on the response object.

        :param response: Response object.
        """
        headers = self.get_headers()
        for header_name, header_value in headers.items():
            if hasattr(response, "set_header"):
                response.set_header(header_name, header_value)
            else:
                try:
                    response.headers[header_name] = header_value
                except AttributeError:
                    raise AttributeError(
                        "The response object does not support setting headers via 'set_header' or 'headers' attribute."
                    )

    async def set_headers_async(self, response: Any) -> None:
        """Asynchronously set headers on the response object.

        :param response: Response object that supports async operations.
        """
        headers = self.get_headers()

        for header_name, header_value in headers.items():
            if hasattr(response, "set_header"):
                await asyncio.sleep(
                    0
                )  # Example of yielding control back to the event loop
                response.set_header(header_name, header_value)
            else:
                try:
                    await asyncio.sleep(0)  # Yield control
                    response.headers[header_name] = header_value
                except AttributeError:
                    raise AttributeError(
                        "The response object does not support setting headers via 'set_header' or 'headers' attribute."
                    )
