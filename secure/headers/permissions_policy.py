# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy
# https://owasp.org/www-project-secure-headers/#permissions-policy
#
# Permissions-Policy by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/


from __future__ import annotations  # type: ignore

from dataclasses import dataclass, field

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class PermissionsPolicy(BaseHeader):
    """
    Represents the `Permissions-Policy` HTTP header, which allows you to enable or disable browser features and APIs.

    This header replaces the deprecated `Feature-Policy` header.

    Default header value: `geolocation=(), microphone=(), camera=()`

    Resources:
        - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy
        - https://owasp.org/www-project-secure-headers/#permissions-policy
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
        """Helper to add a custom directive to the permissions policy.

        Args:
            directive: The name of the directive.
            *allowlist: The allowed sources for the directive.

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        self._build(directive, *allowlist)
        return self

    def accelerometer(self, *allowlist: str) -> PermissionsPolicy:
        """Control the use of the accelerometer sensor.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/accelerometer

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("accelerometer", *allowlist)

    def ambient_light_sensor(self, *allowlist: str) -> PermissionsPolicy:
        """Control access to the ambient light sensor.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/ambient-light-sensor

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("ambient-light-sensor", *allowlist)

    def autoplay(self, *allowlist: str) -> PermissionsPolicy:
        """Control autoplay of media.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/autoplay

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("autoplay", *allowlist)

    def battery(self, *allowlist: str) -> PermissionsPolicy:
        """Control access to battery status.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/battery

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("battery", *allowlist)

    def camera(self, *allowlist: str) -> PermissionsPolicy:
        """Control access to the camera.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/camera

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("camera", *allowlist)

    def clipboard_read(self, *allowlist: str) -> PermissionsPolicy:
        """Control reading from the clipboard.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/clipboard-read

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("clipboard-read", *allowlist)

    def clipboard_write(self, *allowlist: str) -> PermissionsPolicy:
        """Control writing to the clipboard.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/clipboard-write

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("clipboard-write", *allowlist)

    def cross_origin_isolated(self, *allowlist: str) -> PermissionsPolicy:
        """Control whether a document is delivered in a cross-origin isolated state.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/cross-origin-isolated

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("cross-origin-isolated", *allowlist)

    def display_capture(self, *allowlist: str) -> PermissionsPolicy:
        """Control access to display capture APIs.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/display-capture

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("display-capture", *allowlist)

    def document_domain(self, *allowlist: str) -> PermissionsPolicy:
        """Control the use of `document.domain` to relax the same-origin policy.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/document-domain

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("document-domain", *allowlist)

    def encrypted_media(self, *allowlist: str) -> PermissionsPolicy:
        """Control the use of Encrypted Media Extensions API.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/encrypted-media

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("encrypted-media", *allowlist)

    def execution_while_not_rendered(self, *allowlist: str) -> PermissionsPolicy:
        """Control script execution when the page is not rendered.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/execution-while-not-rendered

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("execution-while-not-rendered", *allowlist)

    def execution_while_out_of_viewport(self, *allowlist: str) -> PermissionsPolicy:
        """Control script execution when the page is out of the viewport.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/execution-while-out-of-viewport

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("execution-while-out-of-viewport", *allowlist)

    def fullscreen(self, *allowlist: str) -> PermissionsPolicy:
        """Control the use of the Fullscreen API.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/fullscreen

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("fullscreen", *allowlist)

    def gamepad(self, *allowlist: str) -> PermissionsPolicy:
        """Control access to gamepad devices.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/gamepad

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("gamepad", *allowlist)

    def geolocation(self, *allowlist: str) -> PermissionsPolicy:
        """Control access to geolocation data.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/geolocation

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("geolocation", *allowlist)

    def gyroscope(self, *allowlist: str) -> PermissionsPolicy:
        """Control access to the gyroscope sensor.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/gyroscope

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("gyroscope", *allowlist)

    def magnetometer(self, *allowlist: str) -> PermissionsPolicy:
        """Control access to the magnetometer sensor.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/magnetometer

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("magnetometer", *allowlist)

    def microphone(self, *allowlist: str) -> PermissionsPolicy:
        """Control access to the microphone.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/microphone

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("microphone", *allowlist)

    def midi(self, *allowlist: str) -> PermissionsPolicy:
        """Control access to MIDI devices.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/midi

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("midi", *allowlist)

    def navigation_override(self, *allowlist: str) -> PermissionsPolicy:
        """Control the ability to override navigation.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/navigation-override

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("navigation-override", *allowlist)

    def payment(self, *allowlist: str) -> PermissionsPolicy:
        """Control the use of the Payment Request API.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/payment

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("payment", *allowlist)

    def picture_in_picture(self, *allowlist: str) -> PermissionsPolicy:
        """Control the use of Picture-in-Picture.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/picture-in-picture

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("picture-in-picture", *allowlist)

    def publickey_credentials_get(self, *allowlist: str) -> PermissionsPolicy:
        """Control the use of the Web Authentication API.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/publickey-credentials-get

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("publickey-credentials-get", *allowlist)

    def screen_wake_lock(self, *allowlist: str) -> PermissionsPolicy:
        """Control the use of the Screen Wake Lock API.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/screen-wake-lock

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("screen-wake-lock", *allowlist)

    def speaker_selection(self, *allowlist: str) -> PermissionsPolicy:
        """Control the ability to select audio output devices.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/speaker-selection

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("speaker-selection", *allowlist)

    def sync_xhr(self, *allowlist: str) -> PermissionsPolicy:
        """Control the use of synchronous XMLHttpRequest.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/sync-xhr

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("sync-xhr", *allowlist)

    def usb(self, *allowlist: str) -> PermissionsPolicy:
        """Control access to USB devices.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/usb

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("usb", *allowlist)

    def web_share(self, *allowlist: str) -> PermissionsPolicy:
        """Control the use of the Web Share API.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/web-share

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("web-share", *allowlist)

    def xr_spatial_tracking(self, *allowlist: str) -> PermissionsPolicy:
        """Control access to spatial tracking features in WebXR.

        Resources:
            https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy/xr-spatial-tracking

        Returns:
            The `PermissionsPolicy` instance for method chaining.
        """
        return self.add_directive("xr-spatial-tracking", *allowlist)
