from typing import List


class ClearSiteData:
    """
    The Clear-Site-Data header clears browsing data (cookies, storage, cache)
    associated with the requesting website.
    It allows web developers to have more control over the data stored
    by a client browser for their origins.

    Resources:
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Clear-Site-Data
    """

    def __init__(self) -> None:
        self.__policy: List[str] = []
        self.header = "Clear-Site-Data"
        self.value = ""

    def _build(self, directive: str) -> None:
        self.__policy.append(directive)
        self.value = ", ".join(self.__policy)

    def clear_storage(self) -> "ClearSiteData":
        self._build("Storage")
        return self

    def clear_cache(self) -> "ClearSiteData":
        self._build("Cache")
        return self

    def clear_cookies(self) -> "ClearSiteData":
        self._build("Cookies")
        return self

    def clear_execution_context(self) -> "ClearSiteData":
        self._build("executionContexts")
        return self

    def clear_wildcard(self) -> "ClearSiteData":
        self._build("*")
        return self
