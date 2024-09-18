from __future__ import annotations  # type: ignore

from dataclasses import dataclass

from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass
class Server(BaseHeader):
    """Replace server header"""

    header_name: str = HeaderName.SERVER.value
    header_value: str = HeaderDefaultValue.SERVER.value

    def set(self, value: str) -> Server:
        """Set custom value for `Server` header

        :param value: custom header value
        :type value: str
        :return: Server class
        :rtype: Server
        """
        self.header_value = value
        return self
