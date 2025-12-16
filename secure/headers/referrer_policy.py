# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy
# https://owasp.org/www-project-secure-headers/#referrer-policy
#
# Referrer-Policy by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers._validation import normalize_header_value
from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


def _split_policies(value: str) -> list[str]:
    """Split a header value into individual policy tokens."""
    cleaned = normalize_header_value(value, what="Referrer-Policy value")
    if not cleaned:
        return []

    parts: list[str] = []
    for raw in cleaned.split(","):
        token = raw.strip()
        if not token:
            continue

        # Tokens should not contain internal whitespace; treat this as an error to
        # help catch accidental pastes and prevent ambiguous serialization.
        if any(ch in token for ch in (" ", "\t")):
            raise ValueError(f"Invalid Referrer-Policy token {token!r}")

        parts.append(token.lower())
    return parts


@dataclass
class ReferrerPolicy(BaseHeader):
    """
    Builder for the ``Referrer-Policy`` HTTP response header.

    Default header value: ``strict-origin-when-cross-origin``

    Notes:
        * ``Referrer-Policy`` controls how much of the ``Referer`` header is sent.
        * The comma-separated fallback list should place the primary policy last.

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy
        - https://owasp.org/www-project-secure-headers/#referrer-policy
    """

    header_name: str = field(init=False, default=HeaderName.REFERRER_POLICY.value, repr=False)
    _policies: list[str] = field(default_factory=list, repr=False)
    _default_value: str = field(init=False, default=HeaderDefaultValue.REFERRER_POLICY.value, repr=False)

    @property
    def header_value(self) -> str:
        """Return the current ``Referrer-Policy`` header value."""
        return ", ".join(self._policies) if self._policies else self._default_value

    def _add_token(self, token: str) -> None:
        if token not in self._policies:
            self._policies.append(token)

    def add(self, value: str) -> ReferrerPolicy:
        """Add one or more policy tokens.

        Parameters
        ----------
        value:
            A single policy token (e.g., ``"no-referrer"``) or a comma-separated
            list (e.g., ``"no-referrer, strict-origin-when-cross-origin"``).

        Returns
        -------
        ReferrerPolicy
            The same instance, for fluent chaining.
        """
        for token in _split_policies(value):
            self._add_token(token)
        return self

    # Backwards-compatible alias: historically this method appended rather than replaced.
    def set(self, value: str) -> ReferrerPolicy:
        """Alias of :meth:`add` (appends one or more policy tokens)."""
        return self.add(value)

    def value(self, value: str) -> ReferrerPolicy:
        """Replace the current policies with ``value``.

        Use this when you want a single, explicit policy. For fallback lists,
        call :meth:`add` repeatedly or pass a comma-separated list.
        """
        self.clear()
        return self.add(value)

    def custom(self, value: str) -> ReferrerPolicy:
        """Escape hatch: same as :meth:`value`."""
        return self.value(value)

    def fallback(self, *policies: str) -> ReferrerPolicy:
        """Replace the current policies with an explicit fallback list.

        The desired (most modern) policy should be the **last** item.
        """
        self.clear()
        for p in policies:
            self.add(p)
        return self

    def clear(self) -> ReferrerPolicy:
        """Clear all configured policies."""
        self._policies.clear()
        return self

    # --- Directive helpers (MDN-defined tokens) ---------------------------------

    def no_referrer(self) -> ReferrerPolicy:
        """Set the policy to ``no-referrer`` (omit the ``Referer`` header entirely)."""
        return self.add("no-referrer")

    def no_referrer_when_downgrade(self) -> ReferrerPolicy:
        """Set the policy to ``no-referrer-when-downgrade``.

        Sends origin + path + query for same-or-more secure requests (HTTP→HTTP, HTTP→HTTPS, HTTPS→HTTPS),
        but omits ``Referer`` for less secure destinations (HTTPS→HTTP, HTTPS→file).
        """
        return self.add("no-referrer-when-downgrade")

    def origin(self) -> ReferrerPolicy:
        """Set the policy to ``origin`` (send only the origin, e.g. ``https://example.com/``)."""
        return self.add("origin")

    def origin_when_cross_origin(self) -> ReferrerPolicy:
        """Set the policy to ``origin-when-cross-origin``.

        Same-origin: send origin + path + query. Cross-origin (and HTTPS→HTTP): send only the origin.
        """
        return self.add("origin-when-cross-origin")

    def same_origin(self) -> ReferrerPolicy:
        """Set the policy to ``same-origin``.

        Same-origin: send origin + path + query. Cross-origin: omit the ``Referer`` header.
        """
        return self.add("same-origin")

    def strict_origin(self) -> ReferrerPolicy:
        """Set the policy to ``strict-origin``.

        Sends only the origin for same-security requests (HTTPS→HTTPS) and omits ``Referer`` on downgrade (HTTPS→HTTP).
        """
        return self.add("strict-origin")

    def strict_origin_when_cross_origin(self) -> ReferrerPolicy:
        """Set the policy to ``strict-origin-when-cross-origin`` (the modern default).

        Same-origin: send origin + path + query. Cross-origin: send only the origin on HTTPS→HTTPS,
        and omit on downgrade (HTTPS→HTTP).
        """
        return self.add("strict-origin-when-cross-origin")

    def unsafe_url(self) -> ReferrerPolicy:
        """Set the policy to ``unsafe-url`` (send origin + path + query for all requests, regardless of security).

        Warning: this can leak sensitive URL data from HTTPS pages to insecure origins.
        """
        return self.add("unsafe-url")
