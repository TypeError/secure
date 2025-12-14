# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy
# https://owasp.org/www-project-secure-headers/#permissions-policy
#
# Permissions-Policy by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/

from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers._validation import normalize_header_value
from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


def _normalize_token(raw: str, tokens_len: int) -> str | None:
    """Normalize a single allowlist token. Returns None for wildcard, empty string to skip."""
    token = normalize_header_value(str(raw), what="allowlist token")
    if not token:
        return ""

    # Map convenience aliases to their normalized forms
    token_mappings = {
        "none": "()",
        "'none'": "()",
        '"none"': "()",
        "()": "()",
        "*": None,
        "'*'": None,
        '"*"': None,
        "self": "self",
        "'self'": "self",
        '"self"': "self",
        "src": "src",
        "'src'": "src",
        '"src"': "src",
    }

    if token in token_mappings:
        result = token_mappings[token]
        if result == "()" and tokens_len != 1:
            raise ValueError("() / none cannot be combined with other allowlist tokens")
        return result

    # Origins: MDN uses double quotes
    if token.startswith(("http://", "https://")):
        if (token.startswith('"') and token.endswith('"')) or (token.startswith("'") and token.endswith("'")):
            return f'"{token[1:-1]}"' if token.startswith("'") else token
        return f'"{token}"'

    return token


def _normalize_allowlist(tokens: tuple[str, ...]) -> str:
    """
    Normalize an allowlist according to MDN's header syntax.

    - Empty allowlist disables the feature: ()
    - Wildcard allows all origins: *
    - Otherwise: (<token> <token> ...)

    Notes
    -----
    MDN examples show `self` and `src` as bare tokens, and origins as double-quoted
    strings (e.g. "https://a.example.com").
    """
    if not tokens:
        return "()"

    cleaned: list[str] = []
    saw_wildcard = False

    for raw in tokens:
        normalized = _normalize_token(raw, len(tokens))

        if normalized == "":
            continue
        if normalized == "()":
            return "()"
        if normalized is None:
            saw_wildcard = True
            continue

        cleaned.append(normalized)

    if saw_wildcard:
        if cleaned:
            raise ValueError("Wildcard (*) must be used alone in a Permissions-Policy allowlist")
        return "*"

    if not cleaned:
        return "()"

    for t in cleaned:
        if any(ch.isspace() for ch in t):
            raise ValueError("Allowlist tokens must not contain whitespace; pass each token separately")
        if "," in t:
            raise ValueError("Allowlist tokens must not contain commas")

    return f"({' '.join(cleaned)})"


@dataclass
class PermissionsPolicy(BaseHeader):
    """
    Builder for the `Permissions-Policy` HTTP header.

    Default header value: `geolocation=(), microphone=(), camera=()`

    Notes:
        * Directive helpers cover MDN features; use ``value(...)`` when you already
          have a ready-made header string.
        * Allowlists follow MDN syntax: ``()``, ``*``, ``self``, ``src``, or
          double-quoted origins; ``()``/``none`` cannot be mixed with other tokens,
          and wildcard must stand alone.
        * Call helpers repeatedly without worrying about duplicates: each directive
          is unique and re-assigning it keeps the order of the most recent write.

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Permissions-Policy
        - https://owasp.org/www-project-secure-headers/#permissions-policy
        - https://www.w3.org/TR/permissions-policy-1/
    """

    header_name: str = field(init=False, default=HeaderName.PERMISSION_POLICY.value, repr=False)
    _default_value: str = field(init=False, default=HeaderDefaultValue.PERMISSION_POLICY.value, repr=False)

    # Directive -> normalized allowlist string (e.g. "()", "*", '(self "https://a.example.com")')
    _directives: dict[str, str] = field(default_factory=dict, repr=False)

    # If set, overrides directive-building entirely.
    _raw_value: str | None = field(default=None, repr=False)

    @property
    def header_value(self) -> str:
        """Return the current `Permissions-Policy` header value."""
        if self._raw_value is not None:
            return self._raw_value

        if not self._directives:
            return self._default_value

        # Dict preserves insertion order; updating an existing directive keeps its position.
        return ", ".join(f"{name}={allowlist}" for name, allowlist in self._directives.items())

    # ---------------------------------------------------------------------
    # Escape hatches / lifecycle
    # ---------------------------------------------------------------------

    def value(self, value: str) -> PermissionsPolicy:
        """
        Set a raw header value (escape hatch).

        This bypasses directive-building and uses `value` verbatim after trimming.

        Notes
        -----
        `Secure.validate_and_normalize_headers()` is responsible for final safety checks
        (e.g., CR/LF handling). This method rejects CR/LF up front.
        """
        value = normalize_header_value(str(value), what="Permissions-Policy value")
        if not value:
            raise ValueError("Permissions-Policy value must not be empty")

        self._raw_value = value
        return self

    def set(self, value: str) -> PermissionsPolicy:
        """Alias for :meth:`value` (kept for backwards compatibility)."""
        return self.value(value)

    def clear(self) -> PermissionsPolicy:
        """Clear all configured directives and any raw override."""
        self._directives.clear()
        self._raw_value = None
        return self

    # ---------------------------------------------------------------------
    # Directive builder
    # ---------------------------------------------------------------------

    def add_directive(self, directive: str, *allowlist: str) -> PermissionsPolicy:
        """
        Add or replace a directive.

        Parameters
        ----------
        directive:
            The directive name (e.g. "geolocation", "camera", "fullscreen").
        *allowlist:
            Allowlist tokens. Examples:
            - no tokens -> () (disabled)
            - "*" -> * (allowed everywhere)
            - "self", "https://a.example.com" -> (self "https://a.example.com")

        Returns
        -------
        PermissionsPolicy
            The instance (for chaining).
        """
        directive = normalize_header_value(str(directive), what="directive")
        if not directive:
            raise ValueError("Directive name must not be empty")
        if any(ch.isspace() for ch in directive) or any(ch in directive for ch in ",;="):
            raise ValueError(f"Invalid directive name: {directive!r}")

        # Directive-building and raw value are mutually exclusive.
        self._raw_value = None

        self._directives[directive] = _normalize_allowlist(tuple(allowlist))
        return self

    def directive(self, directive: str, *allowlist: str) -> PermissionsPolicy:
        """Alias for :meth:`add_directive`."""
        return self.add_directive(directive, *allowlist)

    # ---------------------------------------------------------------------
    # Directives (MDN list evolves; `add_directive()` remains the catch-all)
    # ---------------------------------------------------------------------

    def accelerometer(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the Accelerometer sensor."""
        return self.add_directive("accelerometer", *allowlist)

    def ambient_light_sensor(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the Ambient Light sensor."""
        return self.add_directive("ambient-light-sensor", *allowlist)

    def aria_notify(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use ARIA notifications (aria-notify)."""
        return self.add_directive("aria-notify", *allowlist)

    def attribution_reporting(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use Attribution Reporting."""
        return self.add_directive("attribution-reporting", *allowlist)

    def autoplay(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether media is allowed to autoplay."""
        return self.add_directive("autoplay", *allowlist)

    def bluetooth(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the Web Bluetooth API."""
        return self.add_directive("bluetooth", *allowlist)

    def browsing_topics(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use browsing-topics."""
        return self.add_directive("browsing-topics", *allowlist)

    def compute_pressure(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the Compute Pressure API."""
        return self.add_directive("compute-pressure", *allowlist)

    def cross_origin_isolated(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the document can be cross-origin isolated."""
        return self.add_directive("cross-origin-isolated", *allowlist)

    def fullscreen(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the Fullscreen API."""
        return self.add_directive("fullscreen", *allowlist)

    def gamepad(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the Gamepad API."""
        return self.add_directive("gamepad", *allowlist)

    def geolocation(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the Geolocation API."""
        return self.add_directive("geolocation", *allowlist)

    def gyroscope(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the Gyroscope sensor."""
        return self.add_directive("gyroscope", *allowlist)

    def hid(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the WebHID API."""
        return self.add_directive("hid", *allowlist)

    def identity_credentials_get(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use identity credentials (identity-credentials-get)."""
        return self.add_directive("identity-credentials-get", *allowlist)

    def idle_detection(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use idle detection."""
        return self.add_directive("idle-detection", *allowlist)

    def local_fonts(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can access local fonts."""
        return self.add_directive("local-fonts", *allowlist)

    def magnetometer(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the Magnetometer sensor."""
        return self.add_directive("magnetometer", *allowlist)

    def microphone(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can access the microphone."""
        return self.add_directive("microphone", *allowlist)

    def on_device_speech_recognition(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use on-device speech recognition."""
        return self.add_directive("on-device-speech-recognition", *allowlist)

    def otp_credentials(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the WebOTP API."""
        return self.add_directive("otp-credentials", *allowlist)

    def publickey_credentials_create(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can create WebAuthn credentials."""
        return self.add_directive("publickey-credentials-create", *allowlist)

    def publickey_credentials_get(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use WebAuthn credential assertion."""
        return self.add_directive("publickey-credentials-get", *allowlist)

    def serial(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the Web Serial API."""
        return self.add_directive("serial", *allowlist)

    def speaker_selection(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can select audio output devices."""
        return self.add_directive("speaker-selection", *allowlist)

    def storage_access(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can request storage access."""
        return self.add_directive("storage-access", *allowlist)

    def summarizer(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use summarizer."""
        return self.add_directive("summarizer", *allowlist)

    def translator(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use translator."""
        return self.add_directive("translator", *allowlist)

    def language_detector(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use language detection."""
        return self.add_directive("language-detector", *allowlist)

    def usb(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the WebUSB API."""
        return self.add_directive("usb", *allowlist)

    def web_share(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the Web Share API."""
        return self.add_directive("web-share", *allowlist)

    def window_management(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use window management."""
        return self.add_directive("window-management", *allowlist)

    def xr_spatial_tracking(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use XR spatial tracking."""
        return self.add_directive("xr-spatial-tracking", *allowlist)

    # ---------------------------------------------------------------------
    # Non-MDN / legacy directives (kept for backwards compatibility)
    # ---------------------------------------------------------------------

    def battery(self, *allowlist: str) -> PermissionsPolicy:
        """Legacy/nonstandard: controls whether the page can access battery status."""
        return self.add_directive("battery", *allowlist)

    def camera(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can access the camera."""
        return self.add_directive("camera", *allowlist)

    def clipboard_read(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can read from the clipboard."""
        return self.add_directive("clipboard-read", *allowlist)

    def clipboard_write(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can write to the clipboard."""
        return self.add_directive("clipboard-write", *allowlist)

    def display_capture(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can capture the display (screen capture)."""
        return self.add_directive("display-capture", *allowlist)

    def document_domain(self, *allowlist: str) -> PermissionsPolicy:
        """Legacy/nonstandard: controls whether the page can use `document.domain`."""
        return self.add_directive("document-domain", *allowlist)

    def encrypted_media(self, *allowlist: str) -> PermissionsPolicy:
        """Legacy/nonstandard: controls whether the page can use encrypted media."""
        return self.add_directive("encrypted-media", *allowlist)

    def execution_while_not_rendered(self, *allowlist: str) -> PermissionsPolicy:
        """Legacy/nonstandard: controls whether the page can execute when not rendered."""
        return self.add_directive("execution-while-not-rendered", *allowlist)

    def execution_while_out_of_viewport(self, *allowlist: str) -> PermissionsPolicy:
        """Legacy/nonstandard: controls whether the page can execute while out of the viewport."""
        return self.add_directive("execution-while-out-of-viewport", *allowlist)

    def midi(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the Web MIDI API."""
        return self.add_directive("midi", *allowlist)

    def navigation_override(self, *allowlist: str) -> PermissionsPolicy:
        """Legacy/nonstandard: controls whether the page can override navigation."""
        return self.add_directive("navigation-override", *allowlist)

    def payment(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the Payment Request API."""
        return self.add_directive("payment", *allowlist)

    def picture_in_picture(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use Picture-in-Picture."""
        return self.add_directive("picture-in-picture", *allowlist)

    def screen_wake_lock(self, *allowlist: str) -> PermissionsPolicy:
        """Controls whether the page can use the Screen Wake Lock API."""
        return self.add_directive("screen-wake-lock", *allowlist)

    def sync_xhr(self, *allowlist: str) -> PermissionsPolicy:
        """Legacy/nonstandard: controls whether the page can use synchronous XHR."""
        return self.add_directive("sync-xhr", *allowlist)
