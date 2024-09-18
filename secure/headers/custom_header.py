from secure.headers.base_header import BaseHeader


class CustomHeader(BaseHeader):
    def __init__(self, header: str, value: str) -> None:
        self.header = header
        self.value = value
