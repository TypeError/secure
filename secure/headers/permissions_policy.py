from typing import List
import warnings


class PermissionsPolicy:
    """
    Disable browser features and APIs

    Replaces the `Feature-Policy` header

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Feature-Policy
    https://github.com/w3c/webappsec-permissions-policy/blob/main/permissions-policy-explainer.md
    """

    def __init__(self) -> None:
        self.__policy: List[str] = []
        self.header = "Permissions-Policy"
        self.value = (
            "accelerometer=(), ambient-light-sensor=(), autoplay=(), battery=(), "
            "camera=(), clipboard-read=(), clipboard-write=(), cross-origin-isolated=(), "
            "display-capture=(), document-domain=(), encrypted-media=(), "
            "execution-while-not-rendered=(), execution-while-out-of-viewport=(), "
            "fullscreen=(), gamepad=(), geolocation=(), gyroscope=(), magnetometer=(), "
            "microphone=(), midi=(), navigation-override=(), payment=(), "
            "picture-in-picture=(), publickey-credentials-get=(), screen-wake-lock=(), "
            "speaker-selection=(), sync-xhr=(), usb=(), web-share=(), "
            "xr-spatial-tracking=()"
        )

    def _build(self, directive: str, *sources: str) -> None:
        self.__policy.append(f"{directive}=({' '.join(sources)})")
        self.value = ", ".join(self.__policy)

    def set(self, value: str) -> "PermissionsPolicy":
        self._build(value)
        return self

    def accelerometer(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("accelerometer", *allowlist)
        return self

    def ambient_light_sensor(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("ambient-light-sensor", *allowlist)
        return self

    def autoplay(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("autoplay", *allowlist)
        return self

    def battery(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("battery", *allowlist)
        return self

    def camera(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("camera", *allowlist)
        return self

    def clipboard_read(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("clipboard-read", *allowlist)
        return self

    def clipboard_write(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("clipboard-write", *allowlist)
        return self

    def cross_origin_isolated(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("cross-origin-isolated", *allowlist)
        return self

    def display_capture(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("display-capture", *allowlist)
        return self

    def document_domain(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("document-domain", *allowlist)
        return self

    def encrypted_media(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("encrypted-media", *allowlist)
        return self

    def execution_while_not_rendered(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("execution-while-not-rendered", *allowlist)
        return self

    def execution_while_out_of_viewport(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("execution-while-out-of-viewport", *allowlist)
        return self

    def fullscreen(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("fullscreen", *allowlist)
        return self

    def gamepad(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("gamepad", *allowlist)
        return self

    def geolocation(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("geolocation", *allowlist)
        return self

    def gyroscope(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("gyroscope", *allowlist)
        return self

    def magnetometer(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("magnetometer", *allowlist)
        return self

    def microphone(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("microphone", *allowlist)
        return self

    def midi(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("midi", *allowlist)
        return self

    def navigation_override(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("navigation-override", *allowlist)
        return self

    def payment(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("payment", *allowlist)
        return self

    def picture_in_picture(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("picture-in-picture", *allowlist)
        return self

    def publickey_credentials_get(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("publickey-credentials-get", *allowlist)
        return self

    def screen_wake_lock(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("screen-wake-lock", *allowlist)
        return self

    def speaker(self, *allowlist: str) -> "PermissionsPolicy":
        warnings.warn(
            "'speaker' feature was removed in favor of 'speaker_selection'",
            DeprecationWarning,
        )
        self._build("speaker", *allowlist)
        return self

    def speaker_selection(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("speaker-selection", *allowlist)
        return self

    def sync_xhr(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("sync-xhr", *allowlist)
        return self

    def usb(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("usb", *allowlist)
        return self

    def web_share(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("web-share", *allowlist)
        return self

    def vibrate(self) -> "PermissionsPolicy":
        warnings.warn(
            "'vibrate' feature has been removed without ever actually having been implemented",
            DeprecationWarning,
        )
        return self

    def vr(self, *allowlist: str) -> "PermissionsPolicy":
        warnings.warn(
            "'vr' feature was renamed to 'xr_spatial_tracking'", DeprecationWarning
        )
        self._build("vr", *allowlist)
        return self

    def xr_spatial_tracking(self, *allowlist: str) -> "PermissionsPolicy":
        self._build("xr-spatial-tracking", *allowlist)
        return self
