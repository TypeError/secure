class Server:
    """Replace server header"""

    def __init__(self) -> None:
        self.header = "Server"
        self.value = "NULL"

    def set(self, value: str) -> "Server":
        """Set custom value for `Server` header

        :param value: custom header value
        :type value: str
        :return: Server class
        :rtype: Server
        """
        self.value = value
        return self
