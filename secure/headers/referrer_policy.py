# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy
# https://owasp.org/www-project-secure-headers/#referrer-policy
#
# Referrer-Policy by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


def _split_policies(value: str) -> list[str]:
    """Split a header value into individual policy tokens.

    The Referrer-Policy HTTP header supports a comma-separated list of values
    to specify a fallback policy; the desired (most modern) policy should be
    specified last.

    This helper is intentionally lightweight: it trims whitespace and rejects
    CR/LF to avoid header injection. Full RFC validation and sanitization is
    handled by :meth:`Secure.validate_and_normalize_headers`.
    """
    if ("\r" in value) or ("\n" in value):
        raise ValueError("Referrer-Policy value must not contain CR or LF")

    parts: list[str] = []
    for raw in value.split(","):
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
    """Represents the ``Referrer-Policy`` HTTP response header.

    The Referrer-Policy header controls how much referrer information (sent
    with the ``Referer`` header) should be included with outgoing requests.

    Default header value: ``strict-origin-when-cross-origin``

    Notes
    -----
    * ``Referer`` is intentionally misspelled in HTTP; ``Referrer-Policy`` does
      **not** share that misspelling (MDN).
    * The HTTP header supports a comma-separated list of policies to provide a
      fallback for older user agents. When specifying multiple values, put the
      desired policy **last**.

    Examples
    --------
    Minimal (use a single policy):

    >>> from secure.headers import ReferrerPolicy
    >>> rp = ReferrerPolicy().value("no-referrer")
    >>> rp.header_name
    'Referrer-Policy'
    >>> rp.header_value
    'no-referrer'

    Fallback list (desired policy last):

    >>> rp = ReferrerPolicy().clear().add("no-referrer").add("strict-origin-when-cross-origin")
    >>> rp.header_value
    'no-referrer, strict-origin-when-cross-origin'

    Resources
    ---------
    * https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Referrer-Policy
    * https://owasp.org/www-project-secure-headers/#referrer-policy
    """

    header_name: str = HeaderName.REFERRER_POLICY.value
    _policies: list[str] = field(default_factory=list)
    _default_value: str = HeaderDefaultValue.REFERRER_POLICY.value

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
