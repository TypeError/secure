from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class PermissionsPolicy(BaseHeader):
    """
    Represents the `Permissions-Policy` HTTP header, which allows you to disable browser features and APIs.

    Replaces the `Feature-Policy` header.

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Feature-Policy
        - https://github.com/w3c/webappsec-permissions-policy/blob/main/permissions-policy-explainer.md
    """

    header_name: str = HeaderName.PERMISSION_POLICY.value
    _directives: list[str] = field(default_factory=list)
    _default_value: str = HeaderDefaultValue.PERMISSION_POLICY.value

    @property
    def header_value(self) -> str:
        """Return the current `Permissions-Policy` header value."""
        return ", ".join(self._directives) if self._directives else self._default_value

    def _build(self, directive: str, *sources: str) -> None:
        """Add a directive to the permissions policy.

        Args:
            directive: The directive name.
            *sources: The allowed sources for the directive.
        """
        self._directives.append(f"{directive}=({' '.join(sources)})")

    def set(self, value: str) -> PermissionsPolicy:
        """Set a custom value for the `Permissions-Policy` header.

        Args:
            value: Custom header value.

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        self._build(value)
        return self

    def clear(self) -> PermissionsPolicy:
        """Clear all directives from the Permissions-Policy.

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        self._directives.clear()
        return self

    def add_directive(self, directive: str, *allowlist: str) -> PermissionsPolicy:
        """Helper to add directives to the permissions policy."""
        self._build(directive, *allowlist)
        return self

    def accelerometer(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("accelerometer", *allowlist)

    def ambient_light_sensor(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("ambient-light-sensor", *allowlist)

    def autoplay(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("autoplay", *allowlist)

    def battery(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("battery", *allowlist)

    def camera(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("camera", *allowlist)

    def clipboard_read(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("clipboard-read", *allowlist)

    def clipboard_write(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("clipboard-write", *allowlist)

    def cross_origin_isolated(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("cross-origin-isolated", *allowlist)

    def display_capture(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("display-capture", *allowlist)

    def document_domain(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("document-domain", *allowlist)

    def encrypted_media(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("encrypted-media", *allowlist)

    def execution_while_not_rendered(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("execution-while-not-rendered", *allowlist)

    def execution_while_out_of_viewport(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("execution-while-out-of-viewport", *allowlist)

    def fullscreen(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("fullscreen", *allowlist)

    def gamepad(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("gamepad", *allowlist)

    def geolocation(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("geolocation", *allowlist)

    def gyroscope(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("gyroscope", *allowlist)

    def magnetometer(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("magnetometer", *allowlist)

    def microphone(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("microphone", *allowlist)

    def midi(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("midi", *allowlist)

    def navigation_override(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("navigation-override", *allowlist)

    def payment(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("payment", *allowlist)

    def picture_in_picture(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("picture-in-picture", *allowlist)

    def publickey_credentials_get(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("publickey-credentials-get", *allowlist)

    def screen_wake_lock(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("screen-wake-lock", *allowlist)

    def speaker_selection(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("speaker-selection", *allowlist)

    def sync_xhr(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("sync-xhr", *allowlist)

    def usb(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("usb", *allowlist)

    def web_share(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("web-share", *allowlist)

    def xr_spatial_tracking(self, *allowlist: str) -> PermissionsPolicy:
        return self.add_directive("xr-spatial-tracking", *allowlist)
