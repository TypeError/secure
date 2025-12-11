# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control
# https://owasp.org/www-project-secure-headers/#cache-control
#
# Cache-Control by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class CacheControl(BaseHeader):
    """
    Represents the `Cache-Control` HTTP header, allowing the addition of various caching directives.

    If no directives are added, it returns the default value.

    This class also provides helpers for request directives such as
    `max-stale`, `min-fresh`, and `only-if-cached`, for cases where
    you want to construct `Cache-Control` on outgoing requests.

    Default header value: `no-store, max-age=0`

    Example:
        cache_control = CacheControl().no_cache().no_store().max_age(0)
        print(cache_control.header_name)   # Output: 'Cache-Control'
        print(cache_control.header_value)  # Output: 'no-cache, no-store, max-age=0'

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching
        - https://owasp.org/www-project-secure-headers/#cache-control
    """

    header_name: str = HeaderName.CACHE_CONTROL.value
    _directives: list[str] = field(default_factory=list)
    _default_value: str = HeaderDefaultValue.CACHE_CONTROL.value

    @property
    def header_value(self) -> str:
        """Return the current `Cache-Control` header value, or the default if no directives are added."""
        return ", ".join(self._directives) if self._directives else self._default_value

    def _build(self, directive: str) -> None:
        """Add a directive to the list, preventing duplicates.

        Args:
            directive: The caching directive to add.
        """
        if directive not in self._directives:
            self._directives.append(directive)

    def set(self, value: str) -> CacheControl:
        """Set a custom value for the `Cache-Control` header, replacing all existing directives.

        Args:
            value: The custom header value.

        Returns:
            The `CacheControl` instance for method chaining.
        """
        self._directives = [value]
        return self

    def clear(self) -> CacheControl:
        """Clear all directives from the `Cache-Control` header, returning to the default state.

        Returns:
            The `CacheControl` instance for method chaining.
        """
        self._directives.clear()
        return self

    # -------------------------------------------------------------------------
    # Directive helpers (alphabetical by directive name)
    # -------------------------------------------------------------------------

    def immutable(self) -> CacheControl:
        """Add the `immutable` response directive.

        Indicates that the resource will not be updated during its freshness lifetime, so
        the client can skip revalidation.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control#immutable

        Returns:
            The `CacheControl` instance for method chaining.
        """
        self._build("immutable")
        return self

    def max_age(self, seconds: int) -> CacheControl:
        """Set the `max-age` directive, defining how long the resource is considered fresh.

        This directive is valid in both requests and responses.

        Args:
            seconds: The maximum time, in seconds, that the resource is fresh.

        Returns:
            The `CacheControl` instance for method chaining.

        Raises:
            ValueError: If `seconds` is negative.
        """
        if seconds < 0:
            raise ValueError("seconds must be a non-negative integer")
        self._build(f"max-age={seconds}")
        return self

    def max_stale(self, seconds: int | None = None) -> CacheControl:
        """Add the `max-stale` request directive, optionally with a limit.

        If `seconds` is omitted, any stale age is acceptable.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control#max-stale

        Returns:
            The `CacheControl` instance for method chaining.

        Raises:
            ValueError: If `seconds` is negative when provided.
        """
        if seconds is None:
            directive = "max-stale"
        else:
            if seconds < 0:
                raise ValueError("seconds must be a non-negative integer")
            directive = f"max-stale={seconds}"
        self._build(directive)
        return self

    def min_fresh(self, seconds: int) -> CacheControl:
        """Add the `min-fresh` request directive.

        Indicates the client requires a response that will be fresh for at least
        the specified number of seconds.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control#min-fresh

        Returns:
            The `CacheControl` instance for method chaining.

        Raises:
            ValueError: If `seconds` is negative.
        """
        if seconds < 0:
            raise ValueError("seconds must be a non-negative integer")
        self._build(f"min-fresh={seconds}")
        return self

    def must_revalidate(self) -> CacheControl:
        """Add the `must-revalidate` response directive.

        Indicates that once a response becomes stale, caches must not reuse it
        without successful validation with the origin server.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control#must-revalidate

        Returns:
            The `CacheControl` instance for method chaining.
        """
        self._build("must-revalidate")
        return self

    def must_understand(self) -> CacheControl:
        """Add the `must-understand` response directive.

        Indicates that a cache may store the response only if it understands
        the caching requirements for the status code. Typically paired with
        `no-store` so that caches which do not understand `must-understand`
        will not store the response.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control#must-understand

        Returns:
            The `CacheControl` instance for method chaining.
        """
        self._build("must-understand")
        return self

    def no_cache(self) -> CacheControl:
        """Add the `no-cache` directive, requiring cache revalidation.

        In responses, this means caches must revalidate with the origin server
        before using a stored response. In requests, it asks caches to revalidate
        the response with the origin.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control#no-cache

        Returns:
            The `CacheControl` instance for method chaining.
        """
        self._build("no-cache")
        return self

    def no_store(self) -> CacheControl:
        """Add the `no-store` directive, preventing the response from being stored by caches.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control#no-store

        Returns:
            The `CacheControl` instance for method chaining.
        """
        self._build("no-store")
        return self

    def no_transform(self) -> CacheControl:
        """Add the `no-transform` directive, preventing intermediaries from modifying the content.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control#no-transform

        Returns:
            The `CacheControl` instance for method chaining.
        """
        self._build("no-transform")
        return self

    def only_if_cached(self) -> CacheControl:
        """Add the `only-if-cached` request directive.

        Indicates that the client only wants a response if it is already stored
        in a cache; otherwise, a 504 (Gateway Timeout) is preferred.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control#only-if-cached

        Returns:
            The `CacheControl` instance for method chaining.
        """
        self._build("only-if-cached")
        return self

    def private(self) -> CacheControl:
        """Add the `private` response directive, allowing caching only by a single user agent.

        Shared caches (for example, CDN or proxy caches) must not store the response.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control#private

        Returns:
            The `CacheControl` instance for method chaining.
        """
        self._build("private")
        return self

    def proxy_revalidate(self) -> CacheControl:
        """Add the `proxy-revalidate` response directive.

        Similar to `must-revalidate`, but applies only to shared caches.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control#proxy-revalidate

        Returns:
            The `CacheControl` instance for method chaining.
        """
        self._build("proxy-revalidate")
        return self

    def public(self) -> CacheControl:
        """Add the `public` response directive, allowing caching by any cache.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control#public

        Returns:
            The `CacheControl` instance for method chaining.
        """
        self._build("public")
        return self

    def s_maxage(self, seconds: int) -> CacheControl:
        """Set the `s-maxage` response directive for shared caches.

        Overrides `max-age` for shared caches (such as CDNs).

        Args:
            seconds: The maximum time, in seconds, that the resource is fresh for shared caches.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control#s-maxage

        Returns:
            The `CacheControl` instance for method chaining.

        Raises:
            ValueError: If `seconds` is negative.
        """
        if seconds < 0:
            raise ValueError("seconds must be a non-negative integer")
        self._build(f"s-maxage={seconds}")
        return self

    def stale_if_error(self, seconds: int) -> CacheControl:
        """Set the `stale-if-error` response directive.

        Defines how long stale content can be used when an error is encountered
        while revalidating or fetching a fresh response.

        Args:
            seconds: The time, in seconds, for how long stale content is allowed if there's an error.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control#stale-if-error

        Returns:
            The `CacheControl` instance for method chaining.

        Raises:
            ValueError: If `seconds` is negative.
        """
        if seconds < 0:
            raise ValueError("seconds must be a non-negative integer")
        self._build(f"stale-if-error={seconds}")
        return self

    def stale_while_revalidate(self, seconds: int) -> CacheControl:
        """Set the `stale-while-revalidate` response directive.

        Defines how long stale content can be served while revalidation happens
        in the background.

        Args:
            seconds: The time, in seconds, for how long stale content is allowed during revalidation.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control#stale-while-revalidate

        Returns:
            The `CacheControl` instance for method chaining.

        Raises:
            ValueError: If `seconds` is negative.
        """
        if seconds < 0:
            raise ValueError("seconds must be a non-negative integer")
        self._build(f"stale-while-revalidate={seconds}")
        return self
