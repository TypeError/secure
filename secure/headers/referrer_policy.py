from typing import List


class ReferrerPolicy:
    """
    Enable full referrer if same origin, remove path for cross origin and
    disable referrer in unsupported browsers

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy
    https://owasp.org/www-project-secure-headers/#referrer-policy
    """

    def __init__(self) -> None:
        self.__policy: List[str] = []
        self.header = "Referrer-Policy"
        self.value = "no-referrer, strict-origin-when-cross-origin"

    def _build(self, directive: str) -> None:
        self.__policy.append(directive)
        self.value = ", ".join(self.__policy)

    def set(self, value: str) -> "ReferrerPolicy":
        """Set custom value for `Referrer-Policy` header

        :param value: custom header value
        :type value: str
        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build(value)
        return self

    def no_referrer(self) -> "ReferrerPolicy":
        """The `Referer` header will not be sent

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("no-referrer")
        return self

    def no_referrer_when_downgrade(self) -> "ReferrerPolicy":
        """The `Referer` header will not be sent if HTTPS -> HTTP

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("no-referrer-when-downgrade")
        return self

    def origin(self) -> "ReferrerPolicy":
        """The `Referer` header will contain only the origin

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("origin")
        return self

    def origin_when_cross_origin(self) -> "ReferrerPolicy":
        """The `Referer` header will contain the full URL
        but only the origin if cross-origin

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("origin-when-cross-origin")
        return self

    def same_origin(self) -> "ReferrerPolicy":
        """The `Referer` header will be sent with the full URL if same-origin

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("same-origin")
        return self

    def strict_origin(self) -> "ReferrerPolicy":
        """The `Referer` header will be sent only for same-origin

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("strict-origin")
        return self

    def strict_origin_when_cross_origin(self) -> "ReferrerPolicy":
        """The `Referer` header will only contain the origin if HTTPS -> HTTP

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("strict-origin-when-cross-origin")
        return self

    def unsafe_url(self) -> "ReferrerPolicy":
        """The `Referer` header will contain the full URL

        :return: ReferrerPolicy class
        :rtype: ReferrerPolicy
        """
        self._build("unsafe-url")
        return self
