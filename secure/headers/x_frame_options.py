from __future__ import annotations  # type: ignore

from dataclasses import dataclass

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class XFrameOptions(BaseHeader):
    """
    Disable framing from different origins (clickjacking defense)

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
    """

    header_name: str = HeaderName.X_FRAME_OPTIONS.value
    header_value: str = HeaderDefaultValue.X_FRAME_OPTIONS.value

    def set(self, value: str) -> XFrameOptions:
        """Set custom value for X-Frame-Options header

        :param value: custom header value
        :type value: str
        :return: XFrameOptions class
        :rtype: XFrameOptions
        """
        self.header_value = value
        return self

    def deny(self) -> XFrameOptions:
        """Disable rending site in a frame

        :return: XFrameOptions class
        :rtype: XFrameOptions
        """
        self.header_value = "deny"
        return self

    def sameorigin(self) -> XFrameOptions:
        """Disable rending site in a frame if not same origin

        :return: XFrameOptions class
        :rtype: XFrameOptions
        """
        self.header_value = "sameorigin"
        return self
