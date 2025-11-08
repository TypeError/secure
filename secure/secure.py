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

# Headers that may appear multiple times as separate fields.
MULTI_OK: frozenset[str] = frozenset(
    {
        "content-security-policy",
    }
)

# Headers where RFC7230-style comma merging is safe/expected
COMMA_JOIN_OK: frozenset[str] = frozenset({"cache-control"})


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

    def validate_and_normalize_headers(  # noqa: PLR0915
        self,
        *,
        on_invalid: str = "drop",  # "drop" | "warn" | "raise"
        strict: bool = False,  # hard-fail on CR/LF + illegal chars
        allow_obs_text: bool = False,
        logger: logging.Logger | None = None,
    ) -> Secure:
        """
        Validate/normalize the *current* headers and replace the cached mapping in-place.
        No persistent class state is added; behavior is controlled only by call arguments.

        Returns:
            self (chainable)
        """

        log = logger or logging.getLogger("secure")

        # Token per RFC 7230 tchar (visible ASCII except separators).
        header_name_re = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")

        # Visible ASCII per RFCs
        sp = 0x20
        vchar_min, vchar_max = 0x21, 0x7E
        # obs-text (RFC 7230 §3.2.4) — rarely needed
        obs_min, obs_max = 0x80, 0xFF

        def _handle_invalid(msg: str) -> None:
            if on_invalid == "warn":
                log.warning(msg)
            elif on_invalid == "raise" or strict:
                raise ValueError(msg)
            # "drop" does nothing; caller will skip the pair

        def _validate_pair(name: str, value: str) -> tuple[str, str] | None:
            # Normalize header name casing to canonical case-insensitive form.
            nonlocal strict

            name = name.strip()
            if not header_name_re.match(name):
                _handle_invalid(f"Invalid header name {name!r} (RFC 7230 token required)")
                return None  # already raised if strict/raise

            # CR/LF must never appear in header values. If not strict, coalesce lines.
            if ("\r" in value) or ("\n" in value):
                if strict:
                    raise ValueError(f"Header {name!r} contained CR/LF")
                value = " ".join(value.splitlines())

            value = value.strip()
            if not value:
                _handle_invalid(f"Dropping header {name!r}: empty value")
                return None

            # Fast path: if all chars are HTAB/SP/VCHAR (and optional obs-text), keep as-is.
            # Bind lookups locally for speed in tight loops.
            _sp = sp
            _vmin, _vmax = vchar_min, vchar_max
            _allow_obs = allow_obs_text
            _omin, _omax = obs_min, obs_max

            # Check if sanitization is needed; avoid building a new string if not.
            needs_sanitize = False
            for ch in value:
                code = ord(ch)
                if not (
                    ch == "\t" or code == _sp or (_vmin <= code <= _vmax) or (_allow_obs and (_omin <= code <= _omax))
                ):
                    needs_sanitize = True
                    break

            if not needs_sanitize:
                return name, value

            # Sanitize disallowed characters: strict -> error, else replace with SP.
            sanitized_chars: list[str] = []
            append = sanitized_chars.append
            for ch in value:
                code = ord(ch)
                if ch == "\t" or code == _sp or (_vmin <= code <= _vmax) or (_allow_obs and (_omin <= code <= _omax)):
                    append(ch)
                else:
                    if strict:
                        raise ValueError(f"Header {name!r} contains disallowed char U+{code:04X}")
                    append(" ")

            norm_value = "".join(sanitized_chars).strip()
            if not norm_value:
                _handle_invalid(f"Dropping header {name!r}: empty after sanitization")
                return None

            return name, norm_value

        # Pull the current cached mapping (a MappingProxyType) and rebuild it.
        try:
            current = dict(self.headers)
        except Exception as e:  # pragma: no cover
            raise RuntimeError(
                "Secure.validate_and_normalize_headers() expected self.headers to be mapping-like"
            ) from e

        cleaned: dict[str, str] = {}
        for k, v in current.items():
            pair = _validate_pair(k, v)
            if pair is None:
                continue
            name, value = pair
            cleaned[name] = value

        # Ensure `headers` is a @cached_property so we can swap its cached value.
        hdr_descr = getattr(type(self), "headers", None)
        if not isinstance(hdr_descr, cached_property):
            raise TypeError("`headers` must be a @cached_property to swap it in-place.")

        # Overwrite the cached property value with a read-only mapping.
        self.__dict__["headers"] = MappingProxyType(cleaned)
        return self

    def deduplicate_headers(
        self,
        *,
        action: str = "raise",  # "raise" | "first" | "last" | "concat"
        comma_join_ok: frozenset[str] = COMMA_JOIN_OK,
        multi_ok: frozenset[str] = MULTI_OK,
        logger: logging.Logger | None = None,
    ) -> Secure:
        """
        Deduplicate current headers in-place according to the chosen policy,
        while respecting headers explicitly allowed to be multi-valued.

        Returns:
            self (chainable)
        """
        log = logger or logging.getLogger("secure")

        # Group by lowercase name; store (first_index, OriginalName, value)
        groups: dict[str, list[tuple[int, str, str]]] = defaultdict(list)

        # Read items robustly (object with attrs or 2-tuple)
        for idx, h in enumerate(self.headers_list):
            try:
                nm = h.header_name
                val = h.header_value
            except AttributeError:
                nm, val = h  # type: ignore[misc]
            groups[nm.lower()].append((idx, nm, val))

        # Stable processing order by first appearance
        ordered_keys = sorted(groups.keys(), key=lambda k: groups[k][0][0])

        def _make_pair(name: str, value: str) -> tuple[str, str]:
            return (name, value)

        def _handle_disallowed_dupes(
            lname: str, entries: list[tuple[int, str, str]]
        ) -> tuple[list[tuple[str, str]], str | None]:
            """Return (new_items, dup_error_name_if_any)."""
            if action == "first":
                _, nm, val = entries[0]
                if len(entries) > 1:
                    log.warning("Dropping duplicate header(s) for %r (keeping first)", nm)
                return [_make_pair(nm, val)], None

            if action == "last":
                _, nm, val = entries[-1]
                if len(entries) > 1:
                    log.warning("Dropping duplicate header(s) for %r (keeping last)", nm)
                return [_make_pair(nm, val)], None

            if action == "concat":
                if lname in comma_join_ok:
                    _, nm0, _ = entries[0]
                    joined = ", ".join(v for _, _, v in entries)
                    return [_make_pair(nm0, joined)], None
                # not safe to join → error
                return [], entries[0][1]

            # default "raise"
            return [], entries[0][1]

        new_list: list[tuple[str, str]] = []
        dup_errors: list[str] = []

        for lname in ordered_keys:
            entries = groups[lname]
            if len(entries) == 1:
                _, nm, val = entries[0]
                new_list.append(_make_pair(nm, val))
                continue

            if lname in multi_ok:
                # keep all, preserve order
                for _, nm, val in entries:
                    new_list.append(_make_pair(nm, val))
                continue

            produced, err = _handle_disallowed_dupes(lname, entries)
            new_list.extend(produced)
            if err is not None:
                dup_errors.append(err)

        if dup_errors:
            names = ", ".join(sorted(set(dup_errors)))
            raise ValueError(f"Duplicate header(s) not allowed: {names}. Define each at most once.")

        # Swap in the rebuilt list as simple (name, value) pairs.
        self.headers_list = new_list  # type: ignore[assignment]

        # Invalidate any cached mapping derived from headers_list (if present).
        if "headers" in self.__dict__:
            self.__dict__.pop("headers", None)

        return self

    def header_items(self) -> tuple[tuple[str, str], ...]:
        """
        Serialize the current headers into (name, value) pairs.

        Assumes duplicate handling (if any) has already been performed elsewhere,
        e.g., via `self.deduplicate_headers(...)`.
        """

        header_tuple_size = 2
        items: list[tuple[str, str]] = []
        append = items.append

        for h in self.headers_list:
            # Support both object form (header_name/header_value) and 2-tuples.
            if hasattr(h, "header_name") and hasattr(h, "header_value"):
                append((h.header_name, h.header_value))  # BaseHeader-style
            elif isinstance(h, (tuple, list)) and len(h) >= header_tuple_size:
                append((h[0], h[1]))  # tuple-like
            else:
                raise TypeError("header_items() expected elements with .header_name/.header_value or 2-tuples")

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
                        result = set_header(name, value)
                        if inspect.isawaitable(result):
                            await result
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
                        await setitem(name, value)  # type: ignore[misc]
                    except (TypeError, ValueError, AttributeError) as e:
                        raise HeaderSetError(f"Failed to set header {name!r}: {e}") from e

                async def _apply_all_hdrs() -> None:
                    for k, v in items:
                        await _apply_hdr_one(k, v)

                asyncio.run(_apply_all_hdrs())
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
                        result = set_header(name, value)
                        if inspect.isawaitable(result):
                            await result
                    except (TypeError, ValueError, AttributeError) as e:
                        raise HeaderSetError(f"Failed to set header {name!r}: {e}") from e

                for k, v in items:
                    await _apply_one(k, v)
                return

            async def _apply_one_syncish(name: str, value: str) -> None:
                try:
                    res = set_header(name, value)
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
                        await setitem(name, value)  # type: ignore[misc]
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
