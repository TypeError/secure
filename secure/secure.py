from __future__ import annotations

from collections import defaultdict
from enum import Enum
from functools import cached_property
import inspect
import logging
import re
from types import MappingProxyType
from typing import TYPE_CHECKING, Literal, Protocol, TypeAlias

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

from .headers import (
    BaseHeader,
    CacheControl,
    ContentSecurityPolicy,
    CrossOriginEmbedderPolicy,
    CrossOriginOpenerPolicy,
    CrossOriginResourcePolicy,
    CustomHeader,
    PermissionsPolicy,
    ReferrerPolicy,
    Server,
    StrictTransportSecurity,
    XContentTypeOptions,
    XDnsPrefetchControl,
    XFrameOptions,
    XPermittedCrossDomainPolicies,
)

# ---------------------------------------------------------------------------
# Configuration / constants
# ---------------------------------------------------------------------------

# Headers that may appear multiple times as separate fields.
MULTI_OK: frozenset[str] = frozenset(
    {
        "content-security-policy",
    }
)

# Headers where RFC7230-style comma merging is safe/expected.
COMMA_JOIN_OK: frozenset[str] = frozenset({"cache-control"})

# A default allowlist of secure headers.
DEFAULT_ALLOWED_HEADERS: frozenset[str] = frozenset(
    {
        "cache-control",
        "content-security-policy",
        "content-security-policy-report-only",
        "cross-origin-embedder-policy",
        "cross-origin-opener-policy",
        "cross-origin-resource-policy",
        "origin-agent-cluster",
        "permissions-policy",
        "referrer-policy",
        "strict-transport-security",
        "x-content-type-options",
        "x-dns-prefetch-control",
        "x-download-options",
        "x-frame-options",
        "x-permitted-cross-domain-policies",
        "x-xss-protection",
    }
)

# RFC 7230 token (visible ASCII except separators).
HEADER_NAME_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")

OnInvalidPolicy = Literal["drop", "warn", "raise"]
DeduplicateAction = Literal["raise", "first", "last", "concat"]
OnUnexpectedPolicy = Literal["raise", "drop", "warn"]


# ---------------------------------------------------------------------------
# Protocols / errors
# ---------------------------------------------------------------------------


class HeaderSetError(RuntimeError):
    """Raised when applying a header to a response fails."""


class HeadersProtocol(Protocol):
    # Intentionally broad: frameworks type headers differently.
    headers: object


class SetHeaderProtocol(Protocol):
    def set_header(self, key: str, value: str) -> object | None: ...


# Union type for supported response objects.
ResponseProtocol: TypeAlias = HeadersProtocol | SetHeaderProtocol


# ---------------------------------------------------------------------------
# Presets
# ---------------------------------------------------------------------------


class Preset(Enum):
    """Predefined security header presets for :class:`Secure`."""

    BASIC = "basic"
    BALANCED = "balanced"
    STRICT = "strict"


def _baseline_content_security_policy() -> ContentSecurityPolicy:
    """Shared CSP builder used by the BASIC and BALANCED presets."""
    return (
        ContentSecurityPolicy()
        .default_src("'self'")
        .base_uri("'self'")
        .font_src("'self'", "https:", "data:")
        .form_action("'self'")
        .frame_ancestors("'self'")
        .img_src("'self'", "data:")
        .object_src("'none'")
        .script_src("'self'")
        .script_src_attr("'none'")
        .style_src("'self'", "https:", "'unsafe-inline'")
        .upgrade_insecure_requests()
    )


# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------


class Secure:
    """
    Configure and apply HTTP security headers for web applications.

    A :class:`Secure` instance encapsulates a set of header objects that can be
    applied to response objects from common Python web frameworks (FastAPI,
    Starlette, Flask, Django, etc.).

    Typical pipeline:

    >>> secure = (
    ...     Secure.with_default_headers().allowlist_headers().deduplicate_headers().validate_and_normalize_headers()
    ... )

    Then, inside your framework integration:

    >>> secure.set_headers(response)
    >>> # or in async contexts:
    >>> await secure.set_headers_async(response)

    Attributes
    ----------
    headers_list :
        Ordered list of header objects representing the configured headers.
        Methods like :meth:`allowlist_headers` and :meth:`deduplicate_headers`
        operate on this list in place and return ``self`` for chaining.
    """

    def __init__(  # noqa: PLR0913
        self,
        *,
        cache: CacheControl | None = None,
        coep: CrossOriginEmbedderPolicy | None = None,
        coop: CrossOriginOpenerPolicy | None = None,
        corp: CrossOriginResourcePolicy | None = None,
        csp: ContentSecurityPolicy | None = None,
        custom: list[CustomHeader] | None = None,
        hsts: StrictTransportSecurity | None = None,
        permissions: PermissionsPolicy | None = None,
        referrer: ReferrerPolicy | None = None,
        xpcdp: XPermittedCrossDomainPolicies | None = None,
        xdfc: XDnsPrefetchControl | None = None,
        server: Server | None = None,
        xcto: XContentTypeOptions | None = None,
        xfo: XFrameOptions | None = None,
    ) -> None:
        """
        Initialize a :class:`Secure` instance with the specified security headers.

        Parameters
        ----------
        cache :
            Cache-Control header configuration.
        coep :
            Cross-Origin-Embedder-Policy header configuration.
        coop :
            Cross-Origin-Opener-Policy header configuration.
        corp :
            Cross-Origin-Resource-Policy header configuration.
        csp :
            Content-Security-Policy header configuration.
        custom :
            Additional custom headers to include (app-specific).
        hsts :
            Strict-Transport-Security header configuration.
        permissions :
            Permissions-Policy header configuration.
        referrer :
            Referrer-Policy header configuration.
        xpcdp :
            X-Permitted-Cross-Domain-Policies header configuration.
        xdfc :
            X-DNS-Prefetch-Control header configuration.
        server :
            Server header configuration.
        xcto :
            X-Content-Type-Options header configuration.
        xfo :
            X-Frame-Options header configuration.
        """
        self.headers_list: list[BaseHeader] = []

        params: list[BaseHeader | None] = [
            cache,
            coep,
            coop,
            corp,
            csp,
            hsts,
            permissions,
            referrer,
            xpcdp,
            xdfc,
            server,
            xcto,
            xfo,
        ]

        for header in params:
            if header is not None:
                self.headers_list.append(header)

        if custom:
            self.headers_list.extend(custom)

        self._headers_override: Mapping[str, str] | None = None

    @classmethod
    def with_default_headers(cls) -> Secure:
        """
        Create a :class:`Secure` instance with a sensible default set of headers.

        This configuration is suitable for many modern applications and can be
        customized with methods like :meth:`allowlist_headers` or by adding
        additional header builder objects.

        Returns
        -------
        Secure
            Instance preconfigured with :data:`Preset.BALANCED`, the recommended
            default profile.
        """
        return cls.from_preset(Preset.BALANCED)

    @classmethod
    def from_preset(cls, preset: Preset) -> Secure:
        """
        Create a :class:`Secure` instance using a predefined security preset.

        Parameters
        ----------
        preset :
            The security preset to use, for example :data:`Preset.BALANCED` for the
            recommended default profile, :data:`Preset.BASIC` for Helmet-parity
            behavior, or :data:`Preset.STRICT` for a hardened configuration with
            stronger guarantees.

        Returns
        -------
        Secure
            Instance configured with the selected preset.

        Raises
        ------
        ValueError
            If an unknown preset is provided.
        """
        match preset:
            case Preset.BASIC:
                return cls(
                    coop=CrossOriginOpenerPolicy().same_origin(),
                    csp=_baseline_content_security_policy(),
                    corp=CrossOriginResourcePolicy().same_origin(),
                    hsts=StrictTransportSecurity().max_age(31536000).include_subdomains(),
                    referrer=ReferrerPolicy().no_referrer(),
                    xcto=XContentTypeOptions().nosniff(),
                    xfo=XFrameOptions().sameorigin(),
                    xdfc=XDnsPrefetchControl().disable(),
                    xpcdp=XPermittedCrossDomainPolicies().none(),
                    custom=[
                        CustomHeader(
                            header="Origin-Agent-Cluster",
                            value="?1",
                        ),
                        CustomHeader(
                            header="X-Download-Options",
                            value="noopen",
                        ),
                        CustomHeader(
                            header="X-XSS-Protection",
                            value="0",
                        ),
                    ],
                )
            case Preset.BALANCED:
                return cls(
                    coop=CrossOriginOpenerPolicy().same_origin(),
                    corp=CrossOriginResourcePolicy().same_origin(),
                    csp=_baseline_content_security_policy(),
                    hsts=StrictTransportSecurity().max_age(31536000).include_subdomains(),
                    permissions=PermissionsPolicy().geolocation().microphone().camera(),
                    referrer=ReferrerPolicy().strict_origin_when_cross_origin(),
                    server=Server().set(""),
                    xcto=XContentTypeOptions().nosniff(),
                    xfo=XFrameOptions().sameorigin(),
                )

            case Preset.STRICT:
                return cls(
                    cache=CacheControl().no_store().max_age(0),
                    coep=CrossOriginEmbedderPolicy().require_corp(),
                    coop=CrossOriginOpenerPolicy().same_origin(),
                    csp=(
                        ContentSecurityPolicy()
                        .default_src("'self'")
                        .script_src("'self'")
                        .style_src("'self'")
                        .object_src("'none'")
                        .base_uri("'none'")
                        .frame_ancestors("'none'")
                    ),
                    hsts=StrictTransportSecurity().max_age(63072000).include_subdomains(),
                    permissions=PermissionsPolicy().geolocation().microphone().camera(),
                    referrer=ReferrerPolicy().no_referrer(),
                    server=Server().set(""),
                    xcto=XContentTypeOptions().nosniff(),
                    xfo=XFrameOptions().deny(),
                )

            case _:
                raise ValueError(f"Unknown preset: {preset}")

    def __str__(self) -> str:
        """Return a human-readable listing of headers and their effective values."""
        return "\n".join(f"{name}: {value}" for name, value in self._resolved_header_items())

    def __repr__(self) -> str:
        """Return a detailed representation of the :class:`Secure` instance."""
        return f"{self.__class__.__name__}(headers_list={self.headers_list!r})"

    # ------------------------------------------------------------------
    # Header normalization / safety helpers
    # ------------------------------------------------------------------

    def validate_and_normalize_headers(  # noqa: PLR0915
        self,
        *,
        on_invalid: OnInvalidPolicy = "drop",
        strict: bool = False,
        allow_obs_text: bool = False,
        logger: logging.Logger | None = None,
    ) -> Secure:
        """
        Validate and normalize the current header items and cache an immutable mapping.

        This operates on :meth:`header_items` (not ``headers_list`` directly) to
        preserve ordering, multi-valued behavior, and any prior deduplication.

        The resulting mapping is stored as an internal override that is returned
        by :attr:`headers`.

        Parameters
        ----------
        on_invalid :
            Policy for invalid headers:
            - ``"drop"``: silently drop invalid entries (default).
            - ``"warn"``: log a warning and drop invalid entries.
            - ``"raise"``: raise :class:`ValueError` on invalid entries.
        strict :
            If true, treat CR/LF and disallowed characters as hard errors.
            Other invalid cases (name/value) are governed by ``on_invalid``.
        allow_obs_text :
            If true, allow "obs-text" (bytes 0x80-0xFF) as per older RFCs.
        logger :
            Optional :class:`logging.Logger` used when ``on_invalid="warn"`` or
            when dropping headers with ``on_invalid="drop"`` but logging is desired.

        Returns
        -------
        Secure
            The same instance, for call chaining.

        Raises
        ------
        ValueError
            If a header name is invalid (when ``on_invalid="raise"``),
            if duplicates are found when building the single-valued mapping,
            or if ``strict=True`` and CR/LF or disallowed characters are present.
        """
        log = logger or logging.getLogger(__name__)

        # Visible ASCII per RFCs.
        sp = 0x20
        vchar_min, vchar_max = 0x21, 0x7E
        obs_min, obs_max = 0x80, 0xFF

        def _handle_invalid(msg: str) -> None:
            if on_invalid == "warn":
                log.warning(msg)
            elif on_invalid == "raise":
                raise ValueError(msg)
            # on_invalid == "drop": silently drop

        def _validate_pair(name: str, value: str) -> tuple[str, str] | None:  # noqa: PLR0912
            strict_flag = bool(strict)
            name = name.strip()

            if not HEADER_NAME_RE.match(name):
                _handle_invalid(f"Invalid header name {name!r} (RFC 7230 token required)")
                return None

            # Prevent folded-header smuggling.
            if value.startswith((" ", "\t")):
                _handle_invalid(f"Header {name!r} starts with forbidden whitespace")
                return None

            # CR/LF must never appear in values.
            if ("\r" in value) or ("\n" in value):
                if strict_flag:
                    raise ValueError(f"Header {name!r} contained CR/LF")
                value = " ".join(value.splitlines())

            value = value.strip()
            if not value:
                _handle_invalid(f"Dropping header {name!r}: empty value")
                return None

            _allow_obs = allow_obs_text

            needs_sanitize = False
            for ch in value:
                code = ord(ch)
                if not (
                    ch == "\t"
                    or code == sp
                    or (vchar_min <= code <= vchar_max)
                    or (_allow_obs and (obs_min <= code <= obs_max))
                ):
                    needs_sanitize = True
                    break

            if not needs_sanitize:
                return name, value

            sanitized: list[str] = []
            append = sanitized.append

            for ch in value:
                code = ord(ch)
                if (
                    ch == "\t"
                    or code == sp
                    or (vchar_min <= code <= vchar_max)
                    or (_allow_obs and (obs_min <= code <= obs_max))
                ):
                    append(ch)
                else:
                    if strict_flag:
                        raise ValueError(f"Header {name!r} contains disallowed char U+{code:04X}")
                    append(" ")

            norm_value = "".join(sanitized).strip()
            if not norm_value:
                _handle_invalid(f"Dropping header {name!r}: empty after sanitization")
                return None

            return name, norm_value

        items = self.header_items()

        cleaned: dict[str, str] = {}
        seen_lc: set[str] = set()

        for name, value in items:
            pair = _validate_pair(name, value)
            if pair is None:
                continue

            norm_name, norm_value = pair
            lname = norm_name.lower()

            if lname in seen_lc:
                raise ValueError(
                    f"Duplicate header {norm_name!r} encountered during normalization. "
                    "Run deduplicate_headers() first or use header_items() for multi-valued headers."
                )

            seen_lc.add(lname)
            cleaned[norm_name] = norm_value

        self._headers_override = MappingProxyType(cleaned)

        # Reset cached_property.
        self.__dict__.pop("headers", None)

        return self

    def deduplicate_headers(
        self,
        *,
        action: DeduplicateAction = "raise",
        comma_join_ok: frozenset[str] = COMMA_JOIN_OK,
        multi_ok: frozenset[str] = MULTI_OK,
        logger: logging.Logger | None = None,
    ) -> Secure:
        """
        Deduplicate headers in :attr:`headers_list` according to the chosen policy.

        Parameters
        ----------
        action :
            Policy when encountering disallowed duplicates:
            - ``"raise"``: raise :class:`ValueError` (default).
            - ``"first"``: keep the first instance and drop others.
            - ``"last"``: keep the last instance and drop others.
            - ``"concat"``: join values with commas when safe.
        comma_join_ok :
            Names (lowercased) for which RFC 7230-style comma joining is safe.
        multi_ok :
            Names (lowercased) that are allowed to appear multiple times
            (for example Content-Security-Policy).
        logger :
            Optional :class:`logging.Logger` used for warning messages when
            dropping duplicates in non-``"raise"`` modes.

        Returns
        -------
        Secure
            The same instance, for call chaining.

        Raises
        ------
        ValueError
            If duplicates are found for headers that are not in ``multi_ok``
            and the action is ``"raise"`` or ``"concat"`` for unsafe headers.
        """
        log = logger or logging.getLogger(__name__)

        # Group by lowercase name; store (first_index, BaseHeader).
        groups: dict[str, list[tuple[int, BaseHeader]]] = defaultdict(list)

        for idx, h in enumerate(self.headers_list):
            if not hasattr(h, "header_name") or not hasattr(h, "header_value"):
                raise TypeError("deduplicate_headers() requires BaseHeader objects only")
            groups[h.header_name.lower()].append((idx, h))

        # Stable processing order by first appearance.
        ordered_keys = sorted(groups.keys(), key=lambda k: groups[k][0][0])

        def _clone(name: str, value: str) -> BaseHeader:
            # Preserve type stability using CustomHeader as neutral carrier.
            return CustomHeader(header=name, value=value)

        def _handle_disallowed_dupes(
            lname: str,
            entries: list[tuple[int, BaseHeader]],
        ) -> tuple[list[BaseHeader], str | None]:
            """Return (new_items, dup_error_name_if_any)."""
            if action == "first":
                _, h = entries[0]
                if len(entries) > 1:
                    log.warning("Dropping duplicate header(s) for %r (keeping first)", h.header_name)
                return [_clone(h.header_name, h.header_value)], None

            if action == "last":
                _, h = entries[-1]
                if len(entries) > 1:
                    log.warning("Dropping duplicate header(s) for %r (keeping last)", h.header_name)
                return [_clone(h.header_name, h.header_value)], None

            if action == "concat":
                if lname in comma_join_ok:
                    nm = entries[0][1].header_name
                    joined = ", ".join(h.header_value for _, h in entries)
                    return [_clone(nm, joined)], None

                # Not safe to join.
                return [], entries[0][1].header_name

            # Default "raise".
            return [], entries[0][1].header_name

        new_list: list[BaseHeader] = []
        dup_errors: list[str] = []

        for lname in ordered_keys:
            entries = groups[lname]

            if len(entries) == 1:
                _, h = entries[0]
                new_list.append(_clone(h.header_name, h.header_value))
                continue

            if lname in multi_ok:
                for _, h in entries:
                    new_list.append(_clone(h.header_name, h.header_value))
                continue

            produced, err = _handle_disallowed_dupes(lname, entries)
            new_list.extend(produced)

            if err is not None:
                dup_errors.append(err)

        if dup_errors:
            names = ", ".join(sorted(set(dup_errors)))
            raise ValueError(f"Duplicate header(s) not allowed: {names}. Define each at most once.")

        self.headers_list = new_list
        self._headers_override = None
        self.__dict__.pop("headers", None)

        return self

    def allowlist_headers(
        self,
        *,
        allowed: Iterable[str] = DEFAULT_ALLOWED_HEADERS,
        allow_extra: Iterable[str] | None = None,
        on_unexpected: OnUnexpectedPolicy = "raise",
        allow_x_prefixed: bool = False,
        logger: logging.Logger | None = None,
    ) -> Secure:
        """
        Enforce a case-insensitive allowlist for header names in :attr:`headers_list`.

        Parameters
        ----------
        allowed :
            Base allowlist of header names (case-insensitive).
        allow_extra :
            Additional names to allow, for example app-specific headers.
        on_unexpected :
            Policy for headers not in the allowlist:
            - ``"raise"``: error on any name not in the allowlist (default).
            - ``"drop"``: remove unexpected headers (logs if logger is set).
            - ``"warn"``: keep unexpected headers but log a warning.
        allow_x_prefixed :
            If true, allows any header starting with ``"x-"``.
        logger :
            Optional :class:`logging.Logger` used for warnings in ``"drop"`` and
            ``"warn"`` modes.

        Returns
        -------
        Secure
            The same instance, for call chaining.

        Raises
        ------
        ValueError
            If ``on_unexpected="raise"`` and any header is not in the allowlist.
        """
        log = logger or logging.getLogger(__name__)

        # Build the lowercase allowlist.
        allowed_lc = {h.lower() for h in allowed}
        if allow_extra:
            allowed_lc.update(h.lower() for h in allow_extra)

        def _keep(name_lc: str) -> bool:
            return (name_lc in allowed_lc) or (allow_x_prefixed and name_lc.startswith("x-"))

        kept: list[BaseHeader] = []
        unexpected_names: list[str] = []

        for h in self.headers_list:
            if not hasattr(h, "header_name") or not hasattr(h, "header_value"):
                raise TypeError("allowlist_headers() requires BaseHeader objects only")

            name = h.header_name
            lname = name.lower()

            if _keep(lname):
                kept.append(h)
                continue

            if on_unexpected == "warn":
                log.warning("Unexpected header %r kept (not in allowlist)", name)
                kept.append(h)
            elif on_unexpected == "drop":
                log.warning("Unexpected header %r dropped (not in allowlist)", name)
            else:  # "raise" (default)
                unexpected_names.append(name)

        if unexpected_names:
            names = ", ".join(sorted(set(unexpected_names)))
            raise ValueError(
                f"Unexpected header(s) not in allowlist: {names}. "
                "Enable allow_extra or set on_unexpected to 'drop'/'warn'."
            )

        self.headers_list = kept

        # Invalidate any cached mapping / overrides derived from headers_list.
        self._headers_override = None
        self.__dict__.pop("headers", None)

        return self

    # ------------------------------------------------------------------
    # Serialization / access
    # ------------------------------------------------------------------

    def header_items(self) -> tuple[tuple[str, str], ...]:
        """
        Serialize the current headers into ``(name, value)`` pairs.

        This method supports two forms in :attr:`headers_list`:

        * Header objects with ``.header_name`` and ``.header_value`` attributes.
        * Tuple-like items with at least two elements (name, value).

        It does not enforce uniqueness. Use :meth:`deduplicate_headers` or
        :meth:`validate_and_normalize_headers` when you need a single-valued
        mapping.

        Returns
        -------
        tuple[tuple[str, str], ...]
            Immutable sequence of ``(name, value)`` pairs.
        """
        header_tuple_size = 2
        items: list[tuple[str, str]] = []
        append = items.append

        for h in self.headers_list:
            if hasattr(h, "header_name") and hasattr(h, "header_value"):
                append((h.header_name, h.header_value))
            elif isinstance(h, (tuple, list)) and len(h) >= header_tuple_size:
                append((h[0], h[1]))
            else:
                raise TypeError("header_items() expected elements with .header_name/.header_value or 2-tuples")

        return tuple(items)

    def _resolved_header_items(self) -> tuple[tuple[str, str], ...]:
        """
        Return the list of header items honoring any normalized override.
        """
        if self._headers_override is not None:
            return tuple(self._headers_override.items())
        return self.header_items()

    @cached_property
    def headers(self) -> Mapping[str, str]:
        """
        Single-valued, immutable mapping of headers.

        By default, this is derived from :meth:`header_items`. If
        :meth:`validate_and_normalize_headers` has been called, the mapping
        returned here is the normalized override produced by that method.

        Returns
        -------
        Mapping[str, str]
            Immutable mapping of header names to header values.

        Raises
        ------
        ValueError
            If any header name appears more than once (case-insensitive) when
            building the mapping and no override is set. This includes headers
            in :data:`MULTI_OK`. Use :meth:`header_items` to emit multi-valued
            headers or call :meth:`deduplicate_headers` first.
        """
        if self._headers_override is not None:
            return self._headers_override

        data: dict[str, str] = {}
        seen: set[str] = set()

        for name, value in self.header_items():
            k = name.lower()
            if k in seen:
                raise ValueError(f"Multiple '{name}' headers present; use `header_items()` when emitting multiples.")
            seen.add(k)
            data[name] = value

        return MappingProxyType(data)

    # ------------------------------------------------------------------
    # Application to framework responses
    # ------------------------------------------------------------------

    def set_headers(self, response: ResponseProtocol) -> None:  # noqa: PLR0912
        """
        Apply configured headers synchronously to ``response``.

        This method is strictly sync-only. It is suitable for synchronous
        frameworks or sync response objects in async frameworks.

        Supported patterns
        ------------------
        * ``response.set_header(name, value)`` (synchronous).
        * ``response.headers.set(name, value)`` (Werkzeug-style headers container).
        * ``response.headers[name] = value`` (mapping interface).

        Parameters
        ----------
        response :
            Response object implementing either :class:`SetHeaderProtocol` or
            :class:`HeadersProtocol`.

        Raises
        ------
        RuntimeError
            If an async setter is detected (for example an async method is used
            in a sync context).
        AttributeError
            If the response lacks both ``.set_header`` and ``.headers``, or if
            ``.headers`` does not support setting values.
        HeaderSetError
            If setting an individual header fails.
        """
        items = self._resolved_header_items()

        # Path 1: response.set_header(...)
        if hasattr(response, "set_header"):
            set_header = response.set_header

            if inspect.iscoroutinefunction(set_header):
                raise RuntimeError(
                    "Async 'set_header' detected in sync context. Use 'await set_headers_async(response)'."
                )

            try:
                for name, value in items:
                    result = set_header(name, value)
                    if inspect.isawaitable(result):
                        raise RuntimeError(
                            "Async 'set_header' returned awaitable in sync context. "
                            "Use 'await set_headers_async(response)'."
                        )
            except (TypeError, ValueError, AttributeError) as e:
                raise HeaderSetError(f"Failed to set headers: {e}") from e

            return

        # Path 2: response.headers...
        if hasattr(response, "headers"):
            hdrs = response.headers

            # Prefer Werkzeug-style: response.headers.set(name, value)
            set_fn = getattr(hdrs, "set", None)
            if callable(set_fn):
                if inspect.iscoroutinefunction(set_fn):
                    raise RuntimeError(
                        "Async headers setter detected in sync context. Use 'await set_headers_async(response)'."
                    )

                try:
                    for name, value in items:
                        result = set_fn(name, value)
                        if inspect.isawaitable(result):
                            raise RuntimeError(
                                "Async headers setter returned awaitable in sync context. "
                                "Use 'await set_headers_async(response)'."
                            )
                except (TypeError, ValueError, AttributeError) as e:
                    raise HeaderSetError(f"Failed to set headers: {e}") from e

                return

            # Fallback: response.headers[name] = value  # noqa: ERA001
            setitem = getattr(hdrs, "__setitem__", None)
            if callable(setitem):
                if inspect.iscoroutinefunction(setitem):
                    raise RuntimeError(
                        "Async headers mapping detected in sync context. Use 'await set_headers_async(response)'."
                    )

                try:
                    for name, value in items:
                        hdrs[name] = value
                except (TypeError, ValueError, AttributeError) as e:
                    raise HeaderSetError(f"Failed to set headers: {e}") from e

                return

            raise AttributeError("Response object has .headers but it does not support setting header values.")

        raise AttributeError("Response object does not support setting headers.")

    async def set_headers_async(self, response: ResponseProtocol) -> None:  # noqa: PLR0912
        """
        Apply configured headers asynchronously to ``response``.

        This method is designed for async frameworks such as FastAPI and
        Starlette. It transparently supports sync or async setters.

        Supported patterns
        ------------------
        * ``await response.set_header(name, value)`` for async setters.
        * ``response.set_header(name, value)`` for sync setters returning ``None``.
        * ``await response.headers.set(name, value)`` for async headers containers.
        * ``response.headers.set(name, value)`` for sync headers containers.
        * ``await response.headers.__setitem__(name, value)`` for async mappings.
        * ``response.headers[name] = value`` for sync mappings.

        Parameters
        ----------
        response :
            Response object implementing either :class:`SetHeaderProtocol` or
            :class:`HeadersProtocol`.

        Raises
        ------
        AttributeError
            If the response lacks both ``.set_header`` and ``.headers``, or if
            ``.headers`` does not support setting values.
        HeaderSetError
            If setting an individual header fails.
        """
        items = self._resolved_header_items()

        # Path 1: response.set_header(...)
        if hasattr(response, "set_header"):
            set_header = response.set_header

            try:
                for name, value in items:
                    result = set_header(name, value)
                    if inspect.isawaitable(result):
                        await result
            except (TypeError, ValueError, AttributeError) as e:
                raise HeaderSetError(f"Failed to set headers: {e}") from e

            return

        # Path 2: response.headers...
        if hasattr(response, "headers"):
            hdrs = response.headers

            # Prefer Werkzeug-style: response.headers.set(name, value)
            set_fn = getattr(hdrs, "set", None)
            if callable(set_fn):
                try:
                    for name, value in items:
                        result = set_fn(name, value)
                        if inspect.isawaitable(result):
                            await result
                except (TypeError, ValueError, AttributeError) as e:
                    raise HeaderSetError(f"Failed to set headers: {e}") from e

                return

            # Fallback: response.headers.__setitem__(name, value)  # noqa: ERA001
            setitem = getattr(hdrs, "__setitem__", None)
            if callable(setitem):
                try:
                    for name, value in items:
                        result = setitem(name, value)
                        if inspect.isawaitable(result):
                            await result
                except (TypeError, ValueError, AttributeError) as e:
                    raise HeaderSetError(f"Failed to set headers: {e}") from e

                return

            raise AttributeError("Response object has .headers but it does not support setting header values.")

        raise AttributeError("Response object does not support setting headers.")
