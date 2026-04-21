from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, Any, TypeAlias, overload

from ..headers.base_header import BaseHeader
from ..headers.custom_header import CustomHeader
from .types import HeaderItems, HeaderPair

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

HeaderInput: TypeAlias = BaseHeader | HeaderPair | list[str]
HEADER_PAIR_SIZE = 2


class ConfiguredHeaders(list[BaseHeader]):
    """Mutable header builder collection with centralized mutation bookkeeping."""

    def __init__(
        self,
        headers: Iterable[HeaderInput] = (),
        *,
        on_change: Callable[[], None],
    ) -> None:
        self._on_change = on_change
        super().__init__(_coerce_header_object(header, operation="ConfiguredHeaders") for header in headers)

    def replace_all(self, headers: Iterable[HeaderInput]) -> None:
        replacement = [_coerce_header_object(header, operation="headers_list") for header in headers]
        super().clear()
        super().extend(replacement)
        self._on_change()

    def append(self, header: HeaderInput) -> None:
        super().append(_coerce_header_object(header, operation="headers_list.append"))
        self._on_change()

    def extend(self, headers: Iterable[HeaderInput]) -> None:
        super().extend(_coerce_header_object(header, operation="headers_list.extend") for header in headers)
        self._on_change()

    def insert(self, index: int, header: HeaderInput) -> None:
        super().insert(index, _coerce_header_object(header, operation="headers_list.insert"))
        self._on_change()

    @overload
    def __setitem__(self, index: int, header: HeaderInput) -> None: ...

    @overload
    def __setitem__(self, index: slice, header: Iterable[HeaderInput]) -> None: ...

    def __setitem__(self, index: int | slice, header: HeaderInput | Iterable[HeaderInput]) -> None:
        if isinstance(index, slice):
            super().__setitem__(
                index,
                [_coerce_header_object(item, operation="headers_list assignment") for item in header],
            )
        else:
            super().__setitem__(index, _coerce_header_object(header, operation="headers_list assignment"))
        self._on_change()

    def __delitem__(self, index: int | slice) -> None:
        super().__delitem__(index)
        self._on_change()

    def clear(self) -> None:
        super().clear()
        self._on_change()

    def pop(self, index: int = -1) -> BaseHeader:
        header = super().pop(index)
        self._on_change()
        return header

    def remove(self, header: BaseHeader) -> None:
        super().remove(header)
        self._on_change()

    def reverse(self) -> None:
        super().reverse()
        self._on_change()

    def sort(self, *, key: Callable[[BaseHeader], Any] | None = None, reverse: bool = False) -> None:
        super().sort(key=key, reverse=reverse)
        self._on_change()

    def __iadd__(self, headers: Iterable[HeaderInput]) -> ConfiguredHeaders:
        self.extend(headers)
        return self


def header_items_from_objects(headers: Iterable[BaseHeader]) -> HeaderItems:
    return tuple((header.header_name, header.header_value) for header in headers)


def header_mapping_from_items(items: HeaderItems) -> MappingProxyType[str, str]:
    headers: dict[str, str] = {}
    seen_names: set[str] = set()

    for name, value in items:
        lowered_name = name.lower()
        if lowered_name in seen_names:
            raise ValueError(f"Multiple '{name}' headers present; use `header_items()` when emitting multiples.")
        seen_names.add(lowered_name)
        headers[name] = value

    return MappingProxyType(headers)


def _coerce_header_object(header: HeaderInput, *, operation: str) -> BaseHeader:
    if isinstance(header, BaseHeader):
        return header

    if (isinstance(header, tuple) and len(header) == HEADER_PAIR_SIZE) or (
        isinstance(header, list) and len(header) == HEADER_PAIR_SIZE
    ):
        name, value = header
        if isinstance(name, str) and isinstance(value, str):
            return CustomHeader(header=name, value=value)

    raise TypeError(f"{operation} expects BaseHeader objects or (name, value) pairs")
