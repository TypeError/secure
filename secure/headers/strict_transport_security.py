# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security
# https://owasp.org/www-project-secure-headers/
#
# Strict-Transport-Security by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers._validation import normalize_header_value
from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName

_PRELOAD_MIN_MAX_AGE_SECONDS = 31_536_000  # 1 year


@dataclass
class StrictTransportSecurity(BaseHeader):
    """
    Builder for the ``Strict-Transport-Security`` (HSTS) HTTP response header.

    Default header value: ``max-age=31536000``

    Notes:
        * Only send this header over HTTPS; browsers ignore it otherwise.
        * ``preload`` requires ``includeSubDomains`` and at least one year ``max-age``.
        * ``max-age`` is required by the HSTS specification.

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security
        - https://hstspreload.org/
        - https://owasp.org/www-project-secure-headers/
    """

    header_name: str = field(init=False, default=HeaderName.STRICT_TRANSPORT_SECURITY.value, repr=False)
    _default_value: str = field(init=False, default=HeaderDefaultValue.STRICT_TRANSPORT_SECURITY.value, repr=False)

    # Structured directives
    _max_age: int | None = None
    _include_subdomains: bool = False
    _preload: bool = False

    # Escape hatch: if set, emitted exactly as provided (after basic safety checks).
    _raw_value: str | None = None

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    @property
    def header_value(self) -> str:
        """Return the serialized ``Strict-Transport-Security`` header value."""
        if self._raw_value is not None:
            return self._raw_value

        # If nothing was explicitly configured, emit the library default.
        if self._max_age is None and not self._include_subdomains and not self._preload:
            return self._default_value

        max_age = self._max_age if self._max_age is not None else self._default_max_age_seconds()

        parts: list[str] = [f"max-age={max_age}"]

        if self._preload:
            # MDN: preload requires includeSubDomains and min max-age.
            if max_age < _PRELOAD_MIN_MAX_AGE_SECONDS:
                raise ValueError(
                    "preload requires max-age to be at least 31536000 seconds (1 year). "
                    "Increase max-age or remove preload()."
                )
            parts.append("includeSubDomains")
            parts.append("preload")
            return "; ".join(parts)

        if self._include_subdomains:
            parts.append("includeSubDomains")

        return "; ".join(parts)

    def _default_max_age_seconds(self) -> int:
        """Extract the integer max-age from the library default (fallback: 31536000)."""
        prefix = "max-age="
        if self._default_value.startswith(prefix):
            rest = self._default_value[len(prefix) :].split(";", 1)[0].strip()
            try:
                return int(rest)
            except ValueError:
                pass
        return _PRELOAD_MIN_MAX_AGE_SECONDS

    @staticmethod
    def _ensure_no_newlines(value: str) -> str:
        """Reject values that could enable header injection via CR/LF."""
        return normalize_header_value(value, what="Strict-Transport-Security value")

    def clear(self) -> StrictTransportSecurity:
        """Clear configured directives and reset back to the library default."""
        self._max_age = None
        self._include_subdomains = False
        self._preload = False
        self._raw_value = None
        return self

    # ------------------------------------------------------------------
    # Directive builders
    # ------------------------------------------------------------------

    def value(self, value: str) -> StrictTransportSecurity:
        """Set a raw header value (escape hatch), replacing any configured directives."""
        value = self._ensure_no_newlines(value).strip()
        self._raw_value = value
        self._max_age = None
        self._include_subdomains = False
        self._preload = False
        return self

    # Backwards-compatible alias used by other header modules in this codebase.
    set = value

    def max_age(self, seconds: int) -> StrictTransportSecurity:
        """Set ``max-age``: how long (in seconds) the browser should remember to use HTTPS only."""
        if seconds < 0:
            raise ValueError("max-age must be a non-negative integer (use 0 to disable HSTS).")

        if self._preload and seconds < _PRELOAD_MIN_MAX_AGE_SECONDS:
            raise ValueError(
                "preload requires max-age to be at least 31536000 seconds (1 year). "
                "Increase max-age or remove preload()."
            )

        self._raw_value = None
        self._max_age = int(seconds)
        return self

    def include_subdomains(self) -> StrictTransportSecurity:
        """Add ``includeSubDomains``: apply the HSTS policy to all subdomains as well."""
        self._raw_value = None
        self._include_subdomains = True
        return self

    def preload(self) -> StrictTransportSecurity:
        """Add ``preload``: enable HSTS preload list requirements (requires includeSubDomains and 1y+ max-age)."""
        self._raw_value = None
        self._preload = True
        self._include_subdomains = True  # required when preload is used (per MDN)

        if self._max_age is not None and self._max_age < _PRELOAD_MIN_MAX_AGE_SECONDS:
            raise ValueError(
                "preload requires max-age to be at least 31536000 seconds (1 year). "
                "Increase max-age or remove preload()."
            )

        return self
