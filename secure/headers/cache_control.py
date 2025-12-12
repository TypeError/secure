# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control
# https://owasp.org/www-project-secure-headers/#cache-control
#
# Cache-Control by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class CacheControl(BaseHeader):
    """
    Represents the `Cache-Control` HTTP header.

    `Cache-Control` is a comma-separated list of *directives* that control caching
    behavior for both requests and responses.

    If no directives are configured, this class returns the library default value
    (from `HeaderDefaultValue.CACHE_CONTROL`).

    Notes
    -----
    - Directives are case-insensitive, but lowercase is recommended.
    - Some directives accept an integer argument, e.g. `max-age=60`.
    - Some directives are request-only (e.g., `only-if-cached`) but this builder
      does not prevent you from constructing them; you control where you apply it.
    - `must-understand` should be paired with `no-store` for safe fallback behavior
      when a cache does not support `must-understand`.

    Default header value
    --------------------
    `no-store, max-age=0`

    Examples
    --------
    Default (secure baseline):

        cc = CacheControl()
        print(cc.header_name)   # Cache-Control
        print(cc.header_value)  # no-store, max-age=0

    Typical "do not cache" response:

        cc = CacheControl().no_store().max_age(0)
        print(cc.header_value)  # no-store, max-age=0

    Caching public assets for one week:

        cc = CacheControl().public().max_age(604800)
        print(cc.header_value)  # public, max-age=604800

    Resources
    ---------
    - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control
    - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching
    - https://owasp.org/www-project-secure-headers/#cache-control
    """

    header_name: str = HeaderName.CACHE_CONTROL.value

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
        for name, val in self._directives.items():
            if val is None:
                parts.append(name)
            else:
                parts.append(f"{name}={val}")

        parts.extend(self._extras)
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
        """
        if ("\r" in value) or ("\n" in value):
            raise ValueError("Cache-Control value must not contain CR/LF characters")
        self._raw_value = value
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
        Add a custom directive token (non-standard / non-MDN).

        Examples:
            .custom("foo")
            .custom("foo=bar")

        Safety:
        - Rejects commas (would break tokenization).
        - Rejects CR/LF (header-splitting).
        """
        self._ensure_directive_mode()

        d = directive.strip()
        if not d:
            raise ValueError("custom directive must be a non-empty string")
        if "," in d:
            raise ValueError("custom directive must not contain commas")
        if ("\r" in d) or ("\n" in d):
            raise ValueError("custom directive must not contain CR/LF characters")

        # Normalize the directive name portion to lowercase for consistency.
        if "=" in d:
            name, rest = d.split("=", 1)
            token = f"{name.strip().lower()}={rest.strip()}"
        else:
            token = d.lower()

        if token not in self._extras:
            self._extras.append(token)
        return self

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    def _ensure_directive_mode(self) -> None:
        # If the user previously set an explicit raw value, switching back to
        # directive helpers should drop that override.
        if self._raw_value is not None:
            self._raw_value = None

    @staticmethod
    def _validate_seconds(seconds: int) -> int:
        # Avoid bool-as-int surprises.
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
    # Directive helpers (alphabetical by directive name)
    # -------------------------------------------------------------------------

    def immutable(self) -> CacheControl:
        """Add the `immutable` response directive."""
        self._set_bool("immutable")
        return self

    def max_age(self, seconds: int) -> CacheControl:
        """Set `max-age=N` (request/response directive)."""
        self._set_seconds("max-age", seconds)
        return self

    def max_stale(self, seconds: int | None = None) -> CacheControl:
        """
        Add the `max-stale` request directive.

        If `seconds` is omitted, any stale age is acceptable.
        """
        self._ensure_directive_mode()
        if seconds is None:
            self._directives["max-stale"] = None
        else:
            self._directives["max-stale"] = str(self._validate_seconds(seconds))
        return self

    def min_fresh(self, seconds: int) -> CacheControl:
        """Set `min-fresh=N` (request directive)."""
        self._set_seconds("min-fresh", seconds)
        return self

    def must_revalidate(self) -> CacheControl:
        """Add the `must-revalidate` response directive."""
        self._set_bool("must-revalidate")
        return self

    def must_understand(self) -> CacheControl:
        """
        Add the `must-understand` response directive.

        Recommended: pair with `no-store` for fallback behavior.
        """
        self._set_bool("must-understand")
        return self

    def no_cache(self) -> CacheControl:
        """Add the `no-cache` directive (request/response)."""
        self._set_bool("no-cache")
        return self

    def no_store(self) -> CacheControl:
        """Add the `no-store` directive (request/response)."""
        self._set_bool("no-store")
        return self

    def no_transform(self) -> CacheControl:
        """Add the `no-transform` directive (request/response)."""
        self._set_bool("no-transform")
        return self

    def only_if_cached(self) -> CacheControl:
        """Add the `only-if-cached` request directive."""
        self._set_bool("only-if-cached")
        return self

    def private(self) -> CacheControl:
        """Add the `private` response directive."""
        self._set_bool("private")
        return self

    def proxy_revalidate(self) -> CacheControl:
        """Add the `proxy-revalidate` response directive."""
        self._set_bool("proxy-revalidate")
        return self

    def public(self) -> CacheControl:
        """Add the `public` response directive."""
        self._set_bool("public")
        return self

    def s_maxage(self, seconds: int) -> CacheControl:
        """Set `s-maxage=N` (response directive)."""
        self._set_seconds("s-maxage", seconds)
        return self

    def stale_if_error(self, seconds: int) -> CacheControl:
        """Set `stale-if-error=N` (request/response directive)."""
        self._set_seconds("stale-if-error", seconds)
        return self

    def stale_while_revalidate(self, seconds: int) -> CacheControl:
        """Set `stale-while-revalidate=N` (response directive)."""
        self._set_seconds("stale-while-revalidate", seconds)
        return self
