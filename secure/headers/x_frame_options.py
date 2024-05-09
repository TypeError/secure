class XFrameOptions:
    """
    Disable framing from different origins (clickjacking defense)

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
    """

    def __init__(self) -> None:
        self.header = "X-Frame-Options"
        self.value = "SAMEORIGIN"

    def set(self, value: str) -> "XFrameOptions":
        """Set custom value for X-Frame-Options header

        :param value: custom header value
        :type value: str
        :return: XFrameOptions class
        :rtype: XFrameOptions
        """
        self.value = value
        return self

    def deny(self) -> "XFrameOptions":
        """Disable rending site in a frame

        :return: XFrameOptions class
        :rtype: XFrameOptions
        """
        self.value = "deny"
        return self

    def sameorigin(self) -> "XFrameOptions":
        """Disable rending site in a frame if not same origin

        :return: XFrameOptions class
        :rtype: XFrameOptions
        """
        self.value = "sameorigin"
        return self
