# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy
# https://owasp.org/www-project-secure-headers/#cross-origin-opener-policy
#
# Cross-Origin-Opener-Policy by Mozilla Contributors is licensed under CC-BY-SA 2.5.
# https://developer.mozilla.org/en-US/docs/MDN/Community/Roles_teams#contributor
# https://creativecommons.org/licenses/by-sa/2.5/


from __future__ import annotations  # type: ignore

from dataclasses import dataclass

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class CrossOriginOpenerPolicy(BaseHeader):
    """
    The Cross-Origin-Opener-Policy (COOP) header will process-isolate your document.

    COOP will prevent potential attackers from accessing to your global object if they were opening it in a popup.
    Preventing a set of cross-origin attacks dubbed XS-Leaks.

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy
    https://owasp.org/www-project-secure-headers/#cross-origin-opener-policy
    """

    header_name: str = HeaderName.CROSS_ORIGIN_OPENER_POLICY.value
    header_value: str = HeaderDefaultValue.CROSS_ORIGIN_OPENER_POLICY.value

    def set(self, value: str) -> CrossOriginOpenerPolicy:
        """Set custom value for Cross-Origin-Opener-Policy header

        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy
        https://owasp.org/www-project-secure-headers/#cross-origin-opener-policy

        :param value: custom header value
        :type value: str
        :return: CrossOriginOpenerPolicy class
        :rtype: CrossOriginOpenerPolicy
        """
        self.header_value = value
        return self

    def unsafe_none(self) -> CrossOriginOpenerPolicy:
        """Allows the document to be added to its opener’s browsing context group unless the opener itself has a COOP
            of same-origin or same-origin-allow-popups (it is the default value).

        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy
        https://owasp.org/www-project-secure-headers/#cross-origin-opener-policy

            :return: CrossOriginOpenerPolicy class
            :rtype: CrossOriginOpenerPolicy
        """
        self.header_value = "unsafe-none"
        return self

    def same_origin_allow_popups(self) -> CrossOriginOpenerPolicy:
        """Retains references to newly opened windows or tabs which either don’t set COOP or which opt out of isolation
        by setting a COOP of unsafe-none.

        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy
        https://owasp.org/www-project-secure-headers/#cross-origin-opener-policy


        :return: CrossOriginOpenerPolicy class
        :rtype: CrossOriginOpenerPolicy
        """
        self.header_value = "same-origin-allow-popups"
        return self

    def same_origin(self) -> CrossOriginOpenerPolicy:
        """Isolates the browsing context exclusively to same-origin documents.
        Cross-origin documents are not loaded in the same browsing context.

        https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cross-Origin-Opener-Policy
        https://owasp.org/www-project-secure-headers/#cross-origin-opener-policy

        :return: CrossOriginOpenerPolicy class
        :rtype: CrossOriginOpenerPolicy
        """
        self.header_value = "same-origin"
        return self
