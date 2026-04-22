from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    from ._internal.types import DeduplicateAction, HeaderItems, OnInvalidPolicy, OnUnexpectedPolicy, ResponseProtocol
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

from ._internal import emit as _emit
from ._internal.configured_headers import ConfiguredHeaders, header_items_from_objects, header_mapping_from_items
from ._internal.constants import COMMA_JOIN_OK, DEFAULT_ALLOWED_HEADERS, MULTI_OK
from ._internal.normalize import normalize_header_items
from ._internal.policy import allowlist_header_objects, deduplicate_header_objects
from ._internal.presets import Preset, preset_kwargs

HeaderSetError = _emit.HeaderSetError

# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------


class Secure:
    """
    Configure and apply HTTP security headers for web applications.

    A :class:`Secure` instance is the library's public facade. It encapsulates a
    set of typed header builders and applies them to response objects from common
    Python web frameworks (FastAPI, Starlette, Flask, Django, etc.).

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
        params: tuple[BaseHeader | None, ...] = (
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
        )
        configured_headers = [header for header in params if header is not None]

        if custom:
            configured_headers.extend(custom)

        self._headers = ConfiguredHeaders(configured_headers, on_change=self._discard_normalized_headers)
        self._normalized_headers: Mapping[str, str] | None = None
        self._normalized_source_items: HeaderItems | None = None

    @property
    def headers_list(self) -> list[BaseHeader]:
        """Mutable ordered list of configured header builders."""
        return self._headers

    @headers_list.setter
    def headers_list(self, headers: Iterable[BaseHeader]) -> None:
        self._headers.replace_all(headers)

    def _discard_normalized_headers(self) -> None:
        self._normalized_headers = None
        self._normalized_source_items = None

    def _normalized_headers_for(
        self,
        header_items: HeaderItems,
    ) -> Mapping[str, str] | None:
        if self._normalized_headers is None:
            return None

        if self._normalized_source_items != header_items:
            self._discard_normalized_headers()
            return None

        return self._normalized_headers

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
            recommended default profile, :data:`Preset.BASIC` for compatibility-
            oriented behavior, or :data:`Preset.STRICT` for a hardened configuration with
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
        return cls(**preset_kwargs(preset))

    def __str__(self) -> str:
        """Return a human-readable listing of headers and their effective values."""
        return "\n".join(f"{name}: {value}" for name, value in self._resolved_header_items())

    def __repr__(self) -> str:
        """Return a detailed representation of the :class:`Secure` instance."""
        return f"{self.__class__.__name__}(headers_list={self.headers_list!r})"

    # ------------------------------------------------------------------
    # Header normalization / safety helpers
    # ------------------------------------------------------------------

    def validate_and_normalize_headers(
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

        The resulting mapping is stored as a normalized snapshot that is returned
        by :attr:`headers` until the configured headers change.

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
        header_items = self.header_items()
        self._normalized_headers = normalize_header_items(
            header_items,
            on_invalid=on_invalid,
            strict=strict,
            allow_obs_text=allow_obs_text,
            logger=logger or logging.getLogger(__name__),
        )
        self._normalized_source_items = header_items
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
        self.headers_list = deduplicate_header_objects(
            self._headers,
            action=action,
            comma_join_ok=comma_join_ok,
            multi_ok=multi_ok,
            logger=logger or logging.getLogger(__name__),
        )
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
        self.headers_list = allowlist_header_objects(
            self._headers,
            allowed=allowed,
            allow_extra=allow_extra,
            on_unexpected=on_unexpected,
            allow_x_prefixed=allow_x_prefixed,
            logger=logger or logging.getLogger(__name__),
        )
        return self

    # ------------------------------------------------------------------
    # Serialization / access
    # ------------------------------------------------------------------

    def header_items(self) -> HeaderItems:
        """
        Serialize the current headers into ``(name, value)`` pairs.

        It does not enforce uniqueness. Use :meth:`deduplicate_headers` or
        :meth:`validate_and_normalize_headers` when you need a single-valued
        mapping.

        Returns
        -------
        tuple[tuple[str, str], ...]
            Immutable sequence of ``(name, value)`` pairs.
        """
        return header_items_from_objects(self._headers)

    def _resolved_header_items(self) -> HeaderItems:
        """
        Return the list of header items honoring any normalized override.
        """
        header_items = self.header_items()
        normalized_headers = self._normalized_headers_for(header_items)
        if normalized_headers is not None:
            return tuple(normalized_headers.items())
        return header_items

    @property
    def headers(self) -> Mapping[str, str]:
        """
        Single-valued, immutable mapping of headers.

        By default, this is derived from :meth:`header_items`. If
        :meth:`validate_and_normalize_headers` has been called, the mapping
        returned here is the normalized snapshot produced by that method.

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
        header_items = self.header_items()
        normalized_headers = self._normalized_headers_for(header_items)
        if normalized_headers is not None:
            return normalized_headers

        return header_mapping_from_items(header_items)

    # ------------------------------------------------------------------
    # Application to framework responses
    # ------------------------------------------------------------------

    def set_headers(self, response: ResponseProtocol) -> None:
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
        _emit.set_headers_sync(response, self._resolved_header_items())

    async def set_headers_async(self, response: ResponseProtocol) -> None:
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
        await _emit.set_headers_async(response, self._resolved_header_items())
