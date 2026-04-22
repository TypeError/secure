from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from collections.abc import Callable, MutableMapping

    from .types import HeaderItems, ResponseProtocol


class HeaderSetError(RuntimeError):
    """Raised when applying a header to a response fails."""


def set_headers_sync(response: ResponseProtocol, items: HeaderItems) -> None:
    """
    Apply header items to a sync response object.
    """
    if hasattr(response, "set_header"):
        _apply_sync_setter(
            response.set_header,
            items,
            coroutine_function_error=(
                "Async 'set_header' detected in sync context. Use 'await set_headers_async(response)'."
            ),
            awaitable_error=(
                "Async 'set_header' returned awaitable in sync context. Use 'await set_headers_async(response)'."
            ),
        )
        return

    _set_headers_container_sync(_get_headers_container(response), items)


async def set_headers_async(response: ResponseProtocol, items: HeaderItems) -> None:
    """
    Apply header items to a sync or async response object from async code.
    """
    if hasattr(response, "set_header"):
        await _apply_async_setter(response.set_header, items)
        return

    await _set_headers_container_async(_get_headers_container(response), items)


def _get_headers_container(response: ResponseProtocol) -> object:
    if hasattr(response, "headers"):
        return cast("object", response.headers)
    raise AttributeError("Response object does not support setting headers.")


def _set_headers_container_sync(headers: object, items: HeaderItems) -> None:
    set_fn = getattr(headers, "set", None)
    if callable(set_fn):
        _apply_sync_setter(
            set_fn,
            items,
            coroutine_function_error=(
                "Async headers setter detected in sync context. Use 'await set_headers_async(response)'."
            ),
            awaitable_error=(
                "Async headers setter returned awaitable in sync context. Use 'await set_headers_async(response)'."
            ),
        )
        return

    _set_headers_mapping_sync(headers, items)


async def _set_headers_container_async(headers: object, items: HeaderItems) -> None:
    set_fn = getattr(headers, "set", None)
    if callable(set_fn):
        await _apply_async_setter(set_fn, items)
        return

    await _set_headers_mapping_async(headers, items)


def _apply_sync_setter(
    setter: object,
    items: HeaderItems,
    *,
    coroutine_function_error: str,
    awaitable_error: str,
) -> None:
    if inspect.iscoroutinefunction(setter):
        raise RuntimeError(coroutine_function_error)

    typed_setter = cast("Callable[[str, str], object]", setter)

    try:
        for name, value in items:
            result = typed_setter(name, value)
            if inspect.isawaitable(result):
                raise RuntimeError(awaitable_error)
    except (TypeError, ValueError, AttributeError) as error:
        raise HeaderSetError(f"Failed to set headers: {error}") from error


async def _apply_async_setter(setter: object, items: HeaderItems) -> None:
    typed_setter = cast("Callable[[str, str], object]", setter)

    try:
        for name, value in items:
            result = typed_setter(name, value)
            if inspect.isawaitable(result):
                await result
    except (TypeError, ValueError, AttributeError) as error:
        raise HeaderSetError(f"Failed to set headers: {error}") from error


def _set_headers_mapping_sync(headers: object, items: HeaderItems) -> None:
    setitem = getattr(headers, "__setitem__", None)
    if not callable(setitem):
        raise AttributeError(  # noqa: TRY004
            "Response object has .headers but it does not support setting header values."
        )

    if inspect.iscoroutinefunction(setitem):
        raise RuntimeError("Async headers mapping detected in sync context. Use 'await set_headers_async(response)'.")

    try:
        headers_map = cast("MutableMapping[str, str]", headers)
        for name, value in items:
            headers_map[name] = value
    except (TypeError, ValueError, AttributeError) as error:
        raise HeaderSetError(f"Failed to set headers: {error}") from error


async def _set_headers_mapping_async(headers: object, items: HeaderItems) -> None:
    setitem = getattr(headers, "__setitem__", None)
    if not callable(setitem):
        raise AttributeError(  # noqa: TRY004
            "Response object has .headers but it does not support setting header values."
        )

    await _apply_async_setter(setitem, items)
