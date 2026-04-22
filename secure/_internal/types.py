from __future__ import annotations

from typing import Literal, Protocol, TypeAlias

OnInvalidPolicy = Literal["drop", "warn", "raise"]
DeduplicateAction = Literal["raise", "first", "last", "concat"]
OnUnexpectedPolicy = Literal["raise", "drop", "warn"]


class HeadersProtocol(Protocol):
    @property
    def headers(self) -> object: ...


class SetHeaderProtocol(Protocol):
    def set_header(self, key: str, value: str) -> object | None: ...


ResponseProtocol: TypeAlias = HeadersProtocol | SetHeaderProtocol
HeaderPair: TypeAlias = tuple[str, str]
HeaderItems: TypeAlias = tuple[HeaderPair, ...]
