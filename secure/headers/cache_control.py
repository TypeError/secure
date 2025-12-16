# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control
# https://owasp.org/www-project-secure-headers/#cache-control
#
# Cache-Control by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import ClassVar

from secure.headers._validation import normalize_header_value
from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName

_TOKEN_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")


@dataclass
class CacheControl(BaseHeader):
    """
    Fluent builder for the `Cache-Control` HTTP header.

    Default header value: `no-store, max-age=0`

    Notes:
        * Directive names are case-insensitive; lowercase is the recommended form.
        * Directives are comma-separated and resilient to repeated calls for the
          same helper.
        * Common directives follow a deterministic, canonical order to keep
          serialized output stable regardless of call order.

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control
        - https://owasp.org/www-project-secure-headers/#cache-control
    """

    header_name: str = field(init=False, default=HeaderName.CACHE_CONTROL.value, repr=False)

    # Directive storage:
    # - Keys are lowercase directive names (e.g., "max-age", "no-store")
    # - Values are None (valueless directive) or a string (e.g., "60")
    _directives: dict[str, str | None] = field(default_factory=dict)

    # Extra/unrecognized directives (escape hatch). Stored as fully-rendered tokens.
    _extras: list[str] = field(default_factory=list)

    # Exact override for the entire header value (escape hatch).
    _raw_value: str | None = None

    # Library default value for when no directives are set.
    _default_value: str = HeaderDefaultValue.CACHE_CONTROL.value

    # Deterministic serialization order (independent of call order).
    _CANONICAL_ORDER: ClassVar[tuple[str, ...]] = (
        # Common "secure" baseline and typical patterns first.
        "no-store",
        "no-cache",
        "private",
        "public",
        # Age-based caching controls.
        "max-age",
        "s-maxage",
        "max-stale",
        "min-fresh",
        # Validation / capability controls.
        "must-revalidate",
        "proxy-revalidate",
        "must-understand",
        # Transformation / immutability / stale extensions.
        "no-transform",
        "immutable",
        "stale-while-revalidate",
        "stale-if-error",
        # Request-only.
        "only-if-cached",
    )

    # -------------------------------------------------------------------------
    # Serialization
    # -------------------------------------------------------------------------

    @property
    def header_value(self) -> str:
        """Return the current `Cache-Control` header value, or the default if unset."""
        if self._raw_value is not None:
            return self._raw_value

        if not self._directives and not self._extras:
            return self._default_value

        parts: list[str] = []
        present_names: set[str] = set()

        def _add(name: str, val: str | None) -> None:
            token = name if val is None else f"{name}={val}"
            parts.append(token)
            present_names.add(name)

        for name in self._CANONICAL_ORDER:
            if name in self._directives:
                _add(name, self._directives[name])

        for name in sorted(k for k in self._directives if k not in self._CANONICAL_ORDER):
            _add(name, self._directives[name])

        # Append extras, skipping anything that would duplicate a directive name.
        # Extras are sorted for determinism.
        for token in sorted(set(self._extras)):
            extra_name = token.split("=", 1)[0].strip().lower()
            if not extra_name or extra_name in present_names:
                continue
            parts.append(token)

        return ", ".join(parts)

    # -------------------------------------------------------------------------
    # Escape hatches / resets
    # -------------------------------------------------------------------------

    def value(self, value: str) -> CacheControl:
        """
        Set an explicit header value, replacing all configured directives.

        This is an escape hatch: it bypasses directive helpers.

        Safety:
        - Rejects CR/LF to prevent header-splitting.
        - Strips leading/trailing whitespace and rejects empty results.
        """
        v = normalize_header_value(value, what="Cache-Control value")
        if not v:
            raise ValueError("Cache-Control value must not be empty")

        self._raw_value = v
        self._directives.clear()
        self._extras.clear()
        return self

    # Backwards-compatible alias (older versions used `set()`).
    def set(self, value: str) -> CacheControl:
        """Alias for :meth:`value`."""
        return self.value(value)

    def clear(self) -> CacheControl:
        """Clear all directives and explicit value, returning to the default state."""
        self._raw_value = None
        self._directives.clear()
        self._extras.clear()
        return self

    def custom(self, directive: str) -> CacheControl:
        """
        Add a custom directive token (non-standard / extra).

        This is intended for directives not covered by helper methods.

        Examples:
            .custom("foo")
            .custom("foo=bar")

        Safety:
        - Rejects commas (would break tokenization).
        - Rejects CR/LF (header-splitting).
        - Validates the directive *name* as an RFC token.
        """
        self._ensure_directive_mode()

        d = directive.strip()
        if not d:
            raise ValueError("custom directive must be a non-empty string")
        if ("," in d) or ("\r" in d) or ("\n" in d):
            raise ValueError("custom directive must not contain ',', CR, or LF characters")

        if "=" in d:
            name, rest = d.split("=", 1)
            name = name.strip().lower()
            if not name or not _TOKEN_RE.match(name):
                raise ValueError(f"custom directive name must be a valid token (got {name!r})")
            token = f"{name}={rest.strip()}"
        else:
            name = d.strip().lower()
            if not _TOKEN_RE.match(name):
                raise ValueError(f"custom directive name must be a valid token (got {name!r})")
            token = name

        if token not in self._extras:
            self._extras.append(token)
        return self

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    def _ensure_directive_mode(self) -> None:
        if self._raw_value is not None:
            self._raw_value = None

    @staticmethod
    def _validate_seconds(seconds: int) -> int:
        if isinstance(seconds, bool) or not isinstance(seconds, int):
            raise TypeError("seconds must be an integer")
        if seconds < 0:
            raise ValueError("seconds must be a non-negative integer")
        return seconds

    def _set_bool(self, name: str) -> None:
        self._ensure_directive_mode()
        self._directives[name] = None

    def _set_seconds(self, name: str, seconds: int) -> None:
        self._ensure_directive_mode()
        n = self._validate_seconds(seconds)
        self._directives[name] = str(n)

    # -------------------------------------------------------------------------
    # Directive helpers
    # -------------------------------------------------------------------------

    def immutable(self) -> CacheControl:
        """Indicate the response will not be updated while it is fresh."""
        self._set_bool("immutable")
        return self

    def max_age(self, seconds: int) -> CacheControl:
        """Set `max-age=N` (freshness lifetime in responses, acceptable age in requests)."""
        self._set_seconds("max-age", seconds)
        return self

    def max_stale(self, seconds: int | None = None) -> CacheControl:
        """Allow reusing a stale response within `seconds`, or any stale age when omitted (request)."""
        self._ensure_directive_mode()
        if seconds is None:
            self._directives["max-stale"] = None
        else:
            self._directives["max-stale"] = str(self._validate_seconds(seconds))
        return self

    def min_fresh(self, seconds: int) -> CacheControl:
        """Require a stored response to remain fresh for at least `seconds` (request)."""
        self._set_seconds("min-fresh", seconds)
        return self

    def must_revalidate(self) -> CacheControl:
        """Require revalidation with the origin server once a stored response becomes stale (response)."""
        self._set_bool("must-revalidate")
        return self

    def must_understand(self) -> CacheControl:
        """Store the response only if the cache understands the caching requirements for its status code."""
        self._set_bool("must-understand")
        return self

    def no_cache(self) -> CacheControl:
        """Allow storing but require validation with the origin server before each reuse."""
        self._set_bool("no-cache")
        return self

    def no_store(self) -> CacheControl:
        """Instruct caches (private or shared) not to store this response."""
        self._set_bool("no-store")
        return self

    def no_transform(self) -> CacheControl:
        """Instruct intermediaries not to transform the request or response content."""
        self._set_bool("no-transform")
        return self

    def only_if_cached(self) -> CacheControl:
        """Request an already-cached response; if none is available, a 504 may be returned (request)."""
        self._set_bool("only-if-cached")
        return self

    def private(self) -> CacheControl:
        """Indicate the response may be stored only in a private cache (e.g., a browser cache)."""
        self._set_bool("private")
        return self

    def proxy_revalidate(self) -> CacheControl:
        """Like `must-revalidate`, but for shared caches only (response)."""
        self._set_bool("proxy-revalidate")
        return self

    def public(self) -> CacheControl:
        """Indicate the response may be stored in a shared cache (response)."""
        self._set_bool("public")
        return self

    def s_maxage(self, seconds: int) -> CacheControl:
        """Set `s-maxage=N` (freshness lifetime in shared caches only)."""
        self._set_seconds("s-maxage", seconds)
        return self

    def s_max_age(self, seconds: int) -> CacheControl:
        """Alias for :meth:`s_maxage`."""
        return self.s_maxage(seconds)

    def stale_if_error(self, seconds: int) -> CacheControl:
        """Allow reusing a stale response for `seconds` when a 500/502/503/504 error is encountered."""
        self._set_seconds("stale-if-error", seconds)
        return self

    def stale_while_revalidate(self, seconds: int) -> CacheControl:
        """Allow reusing a stale response for `seconds` while revalidation happens in the background."""
        self._set_seconds("stale-while-revalidate", seconds)
        return self
