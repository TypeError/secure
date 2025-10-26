from __future__ import annotations

import asyncio
from collections import defaultdict
from enum import Enum
from functools import cached_property
import inspect
import logging
import re
from types import MappingProxyType
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Awaitable, Mapping, MutableMapping


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

MULTI_OK: set[str] = {"content-security-policy", "set-cookie"}


class HeaderSetError(RuntimeError):
    """Raised when applying a header to a response fails."""


@runtime_checkable
class HeadersProtocol(Protocol):
    """Protocol for response objects that have a 'headers' attribute."""

    headers: MutableMapping[str, str]


@runtime_checkable
class SetHeaderProtocol(Protocol):
    """Protocol for response objects that have a 'set_header' method."""

    def set_header(self, key: str, value: str) -> None: ...


ResponseProtocol = HeadersProtocol | SetHeaderProtocol
"""
Union type for response objects that conform to either HeadersProtocol or SetHeaderProtocol.
This allows the Secure class to work with a variety of web frameworks.
"""


class Preset(Enum):
    """Enumeration of predefined security presets for the Secure class."""

    BASIC = "basic"
    STRICT = "strict"


HTAB: int = 0x09
SP: int = 0x20
VCHAR_MIN: int = 0x21
VCHAR_MAX: int = 0x7E
OBS_MIN: int = 0x80
OBS_MAX: int = 0xFF

_LOG = logging.getLogger("secure")

# RFC 7230 token for header field-name (field-name = token)
_HEADER_NAME_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")


class Secure:
    """
    A class to configure and apply security headers for web applications.

    The Secure class allows you to specify various HTTP security headers to enhance
    the security of your web application. You can use predefined presets or customize
    the headers as needed.

    Attributes:
        headers_list (list[BaseHeader]): List of header objects representing the configured headers.
    """

    def __init__(  # noqa: PLR0913
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
        strict: bool = False,
        allow_obs_text: bool = True,
        on_invalid: str = "drop",  # "drop" | "raise" | "warn"
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
            strict: fail-fast on invalid headers (raises ValueError)
            allow_obs_text: allow 0x80-0xFF in values (RFC7230 obs-text)
            on_invalid (lenient mode only):
                - "drop" (default): skip invalid headers
                - "warn": drop and log a warning
                - "raise": escalate even in lenient mode
        """
        # Store headers in the order defined by the parameters
        self.headers_list: list[BaseHeader] = []
        # List of header parameters in the desired order
        params: list[BaseHeader | None] = [
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

        self._strict = strict
        self._allow_obs_text = allow_obs_text
        self._on_invalid = on_invalid

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
                    hsts=StrictTransportSecurity().max_age(63072000).include_subdomains().preload(),
                    permissions=PermissionsPolicy().geolocation().microphone().camera(),
                    referrer=ReferrerPolicy().no_referrer(),
                    server=Server().set(""),
                    xcto=XContentTypeOptions().nosniff(),
                    xfo=XFrameOptions().deny(),
                )
            case _:
                raise ValueError(f"Unknown preset: {preset}")

    def __str__(self) -> str:
        """
        Return a string representation of the security headers.

        Returns:
            str: A string listing the headers and their values.
        """
        return "\n".join(f"{header.header_name}: {header.header_value}" for header in self.headers_list)

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the Secure instance.

        Returns:
            str: A string representation including the list of headers.
        """
        return f"{self.__class__.__name__}(headers_list={self.headers_list!r})"

    def _validate_and_normalize_header(self, name: str | None, value: str | None) -> tuple[str, str] | None:
        """
        Validate a header field-name and field-value.

        Returns:
            (name, value) if acceptable/sanitized,
            None in lenient 'drop'/'warn' modes when unsanitizable,
            raises ValueError in 'strict' or 'raise' modes on invalid input.
        """
        # Read class-level switches if present; default to non-breaking behavior.

        log = getattr(self, "_log", _LOG)

        def _handle_invalid(msg: str) -> tuple[str, str] | None:
            if self._strict or self._on_invalid == "raise":
                raise ValueError(msg)
            if self._on_invalid == "warn":
                log.warning(msg)
            # "drop" (default) falls through
            return None

        if name is None or value is None:
            return _handle_invalid("Header name/value must not be None")

        name = name.strip()
        if not _HEADER_NAME_RE.match(name):
            return _handle_invalid(f"Invalid header name {name!r} (RFC 7230 token required)")

        # Block response-splitting
        if ("\r" in value) or ("\n" in value):
            if self._strict:
                raise ValueError(f"Header {name!r} contained CR/LF")
            # lenient: collapse newlines into a single space
            value = " ".join(value.splitlines())

        value = value.strip()

        sanitized: list[str] = []
        for ch in value:
            code = ord(ch)
            if (
                ch == "\t"
                or code == SP
                or VCHAR_MIN <= code <= VCHAR_MAX
                or (self._allow_obs_text and (OBS_MIN <= code <= OBS_MAX))
            ):  # HTAB or SP
                sanitized.append(ch)
            else:
                if self._strict:
                    raise ValueError(f"Header {name!r} contains disallowed char U+{code:04X}")
                sanitized.append(" ")

        norm_value = "".join(sanitized).strip()
        if not norm_value:
            # Empty after sanitization: treat as invalid per on_invalid/strict
            return _handle_invalid(f"Dropping header {name!r} due to empty/invalid value after sanitization")

        return name, norm_value

    def header_items(self) -> tuple[tuple[str, str], ...]:
        """
        Return all headers as (name, value) pairs, preserving allowed multi-valued
        headers (e.g., Content-Security-Policy, Set-Cookie) and rejecting unsafe
        duplicates for other headers.
        """
        groups: defaultdict[str, list[tuple[str, str]]] = defaultdict(list)
        for h in self.headers_list:
            groups[h.header_name.lower()].append((h.header_name, h.header_value))

        items: list[tuple[str, str]] = []
        dup_errors: list[str] = []

        for lname, pairs in groups.items():
            if len(pairs) == 1:
                items.append(pairs[0])
                continue
            if lname in MULTI_OK:
                # Preserve multiple fields as separate items.
                items.extend(pairs)
            else:
                # Keep original casing from the first occurrence for the error.
                dup_errors.append(pairs[0][0])

        if dup_errors:
            raise ValueError(
                "Duplicate header(s) not allowed: " + ", ".join(sorted(set(dup_errors))) + ". Define each at most once."
            )

        return tuple(items)

    @cached_property
    def headers(self) -> Mapping[str, str]:
        """
        Single-valued, immutable mapping of headers.

        Raises:
            ValueError: if any header name appears more than once (case-insensitive),
            including headers in MULTI_OK. Use `header_items()` or the setters to
            emit multi-valued headers like Content-Security-Policy or Set-Cookie.
        """
        data: dict[str, str] = {}
        seen: set[str] = set()
        for name, value in self.header_items():
            k = name.lower()
            if k in seen:
                raise ValueError(f"Multiple '{name}' headers present; use `header_items()` when emitting multiples.")
            seen.add(k)
            data[name] = value
        return MappingProxyType(data)

    def set_headers(self, response: ResponseProtocol) -> None:  # noqa: PLR0915
        """
        Apply configured headers **synchronously** to `response`.

        Supports:
        - `set_header(key, value)`: async (driven with `asyncio.run` if no running loop) or sync
        (awaits returned awaitable if present, else sets directly).
        - `.headers` mapping: async `__setitem__` (driven with `asyncio.run`) or sync.

        Raises
        ------
        RuntimeError
            If an async setter is detected while a loop is already running.
        AttributeError
            If the response lacks both `.set_header` and `.headers`.
        HeaderSetError
            If setting an individual header fails.
        """

        items = self.header_items()

        if isinstance(response, SetHeaderProtocol):
            set_header = response.set_header

            if inspect.iscoroutinefunction(set_header):
                try:
                    asyncio.get_running_loop()
                except RuntimeError:
                    pass
                else:
                    raise RuntimeError(
                        "Asynchronous 'set_header' detected while an event loop is running. "
                        "Use 'await set_headers_async(response)'."
                    )

                async def _apply_one(name: str, value: str) -> None:
                    try:
                        nv = self._validate_and_normalize_header(name, value)
                        if nv:
                            await set_header(*nv)
                    except (TypeError, ValueError, AttributeError) as e:
                        raise HeaderSetError(f"Failed to set header {name!r}: {e}") from e

                async def _apply_all() -> None:
                    for k, v in items:
                        await _apply_one(k, v)

                asyncio.run(_apply_all())
                return

            def _set_header_one(name: str, value: str) -> None:
                try:
                    res = set_header(name, value)
                    if inspect.isawaitable(res):
                        try:
                            asyncio.get_running_loop()
                        except RuntimeError:

                            async def _await_one(a: Awaitable[object]) -> None:
                                await a

                            asyncio.run(_await_one(res))  # type: ignore[arg-type]
                        else:
                            raise RuntimeError(
                                "Asynchronous header operation detected while an event loop is running. "
                                "Use 'await set_headers_async(response)'."
                            )
                except (TypeError, ValueError, AttributeError) as e:
                    raise HeaderSetError(f"Failed to set header {name!r}: {e}") from e

            for k, v in items:
                _set_header_one(k, v)
            return

        if hasattr(response, "headers"):
            hdrs = response.headers
            setitem = getattr(hdrs, "__setitem__", None)

            if inspect.iscoroutinefunction(setitem):
                try:
                    asyncio.get_running_loop()
                except RuntimeError:
                    pass
                else:
                    raise RuntimeError(
                        "Asynchronous header operation detected while an event loop is running. "
                        "Use 'await set_headers_async(response)'."
                    )

                async def _apply_hdr_one(name: str, value: str) -> None:
                    try:
                        nv = self._validate_and_normalize_header(name, value)
                        if nv:
                            await setitem(*nv)
                    except (TypeError, ValueError, AttributeError) as e:
                        raise HeaderSetError(f"Failed to set header {name!r}: {e}") from e

                async def _apply_all_hdrs() -> None:
                    for k, v in items:
                        await _apply_hdr_one(k, v)

                asyncio.run(_apply_all_hdrs())
                return

            def _hdrs_set_one(name: str, value: str) -> None:
                try:
                    nv = self._validate_and_normalize_header(name, value)
                    if nv:
                        hdrs.__setitem__(*nv)
                except (TypeError, ValueError, AttributeError) as e:
                    raise HeaderSetError(f"Failed to set header {name!r}: {e}") from e

            for k, v in items:
                _hdrs_set_one(k, v)
            return

        raise AttributeError("Response object does not support setting headers.")

    async def set_headers_async(self, response: ResponseProtocol) -> None:
        """
        Apply configured headers **asynchronously** to `response`.

        Supports:
        - `set_header(key, value)`: async (awaited) or sync (awaits returned awaitable if present).
        - `.headers` mapping: async `__setitem__` (awaited) or sync setitem.

        Raises
        ------
        AttributeError
            If the response lacks both `.set_header` and `.headers`.
        HeaderSetError
            If setting an individual header fails.
        """

        items = self.header_items()

        if isinstance(response, SetHeaderProtocol):
            set_header = response.set_header

            if inspect.iscoroutinefunction(set_header):

                async def _apply_one(name: str, value: str) -> None:
                    try:
                        nv = self._validate_and_normalize_header(name, value)
                        if nv:
                            await set_header(*nv)
                    except (TypeError, ValueError, AttributeError) as e:
                        raise HeaderSetError(f"Failed to set header {name!r}: {e}") from e

                for k, v in items:
                    await _apply_one(k, v)
                return

            async def _apply_one_syncish(name: str, value: str) -> None:
                try:
                    res = None if (nv := self._validate_and_normalize_header(name, value)) is None else set_header(*nv)
                    if inspect.isawaitable(res):
                        await res  # type: ignore[misc]
                except (TypeError, ValueError, AttributeError) as e:
                    raise HeaderSetError(f"Failed to set header {name!r}: {e}") from e

            for k, v in items:
                await _apply_one_syncish(k, v)
            return

        if hasattr(response, "headers"):
            hdrs = response.headers
            setitem = getattr(hdrs, "__setitem__", None)

            if inspect.iscoroutinefunction(setitem):

                async def _apply_hdr_one(name: str, value: str) -> None:
                    try:
                        nv = self._validate_and_normalize_header(name, value)
                        if nv:
                            await setitem(*nv)
                    except (TypeError, ValueError, AttributeError) as e:
                        raise HeaderSetError(f"Failed to set header {name!r}: {e}") from e

                for k, v in items:
                    await _apply_hdr_one(k, v)
                return

            def _hdrs_set_one(name: str, value: str) -> None:
                try:
                    hdrs[name] = value
                except (TypeError, ValueError, AttributeError) as e:
                    raise HeaderSetError(f"Failed to set header {name!r}: {e}") from e

            for k, v in items:
                _hdrs_set_one(k, v)
            return

        raise AttributeError("Response object does not support setting headers.")
