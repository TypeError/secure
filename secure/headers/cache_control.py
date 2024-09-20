from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class CacheControl(BaseHeader):
    """
    Represents the `Cache-Control` HTTP header, allowing the addition of various caching directives.

    If no directives are added, it returns the default value.

    Example:
        cache_control = CacheControl().no_cache().no_store().max_age(0)
        print(cache_control.header_name)   # Output: 'Cache-Control'
        print(cache_control.header_value)  # Output: 'no-cache, no-store, max-age=0'

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
    """

    header_name: str = HeaderName.CACHE_CONTROL.value
    _directives: list[str] = field(default_factory=list)
    _default_value: str = HeaderDefaultValue.CACHE_CONTROL.value

    @property
    def header_value(self) -> str:
        """Return the current header value, or the default if no directives are added."""
        return ", ".join(self._directives) if self._directives else self._default_value

    def _build(self, directive: str) -> None:
        """Add a directive to the list, preventing duplicates."""
        if directive not in self._directives:
            self._directives.append(directive)

    def set(self, value: str) -> CacheControl:
        """Set a custom value for the `Cache-Control` header, replacing all existing directives.

        Args:
            value: The custom header value.

        Returns:
            The CacheControl instance (self) for method chaining.
        """
        self._directives = [value]
        return self

    def clear(self) -> CacheControl:
        """Clear all directives from the Cache-Control header, returning to the default state.

        Returns:
            The CacheControl instance (self) for method chaining.
        """
        self._directives.clear()
        return self

    def immutable(self) -> CacheControl:
        """Add the 'immutable' directive."""
        self._build("immutable")
        return self

    def max_age(self, seconds: int) -> CacheControl:
        """Set the 'max-age' directive, defining how long the resource should be considered fresh.

        Args:
            seconds: The maximum time, in seconds, that the resource is fresh.

        Returns:
            The CacheControl instance (self) for method chaining.

        Raises:
            ValueError: If 'seconds' is negative.
        """
        if seconds < 0:
            raise ValueError("seconds must be a non-negative integer")
        self._build(f"max-age={seconds}")
        return self

    def must_revalidate(self) -> CacheControl:
        """Add the 'must-revalidate' directive."""
        self._build("must-revalidate")
        return self

    def must_understand(self) -> CacheControl:
        """Add the 'must-understand' directive."""
        self._build("must-understand")
        return self

    def no_cache(self) -> CacheControl:
        """Add the 'no-cache' directive."""
        self._build("no-cache")
        return self

    def no_store(self) -> CacheControl:
        """Add the 'no-store' directive."""
        self._build("no-store")
        return self

    def no_transform(self) -> CacheControl:
        """Add the 'no-transform' directive."""
        self._build("no-transform")
        return self

    def private(self) -> CacheControl:
        """Add the 'private' directive."""
        self._build("private")
        return self

    def proxy_revalidate(self) -> CacheControl:
        """Add the 'proxy-revalidate' directive."""
        self._build("proxy-revalidate")
        return self

    def public(self) -> CacheControl:
        """Add the 'public' directive."""
        self._build("public")
        return self

    def s_maxage(self, seconds: int) -> CacheControl:
        """Set the 's-maxage' directive for shared caches.

        Args:
            seconds: The maximum amount of time, in seconds, that the resource is fresh for shared caches.

        Returns:
            The CacheControl instance (self) for method chaining.

        Raises:
            ValueError: If 'seconds' is negative.
        """
        if seconds < 0:
            raise ValueError("seconds must be a non-negative integer")
        self._build(f"s-maxage={seconds}")
        return self

    def stale_if_error(self, seconds: int) -> CacheControl:
        """Set the 'stale-if-error' directive, which defines how long stale content can be used on error.

        Args:
            seconds: The time, in seconds, for how long stale content is allowed if there's an error.

        Returns:
            The CacheControl instance (self) for method chaining.

        Raises:
            ValueError: If 'seconds' is negative.
        """
        if seconds < 0:
            raise ValueError("seconds must be a non-negative integer")
        self._build(f"stale-if-error={seconds}")
        return self

    def stale_while_revalidate(self, seconds: int) -> CacheControl:
        """Set the 'stale-while-revalidate' directive, defining how long stale content can be used during revalidation.

        Args:
            seconds: The time, in seconds, for how long stale content is allowed during revalidation.

        Returns:
            The CacheControl instance (self) for method chaining.

        Raises:
            ValueError: If 'seconds' is negative.
        """
        if seconds < 0:
            raise ValueError("seconds must be a non-negative integer")
        self._build(f"stale-while-revalidate={seconds}")
        return self
