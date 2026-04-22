from __future__ import annotations

from collections import defaultdict
import logging
from typing import TYPE_CHECKING

from ..headers.base_header import BaseHeader
from ..headers.custom_header import CustomHeader

if TYPE_CHECKING:
    from collections.abc import Iterable

    from .types import DeduplicateAction, OnUnexpectedPolicy


def deduplicate_header_objects(
    headers: Iterable[BaseHeader],
    *,
    action: DeduplicateAction = "raise",
    comma_join_ok: frozenset[str],
    multi_ok: frozenset[str],
    logger: logging.Logger | None = None,
) -> list[BaseHeader]:
    """
    Deduplicate header objects while preserving stable header ordering.
    """
    log = logger or logging.getLogger(__name__)
    groups: dict[str, list[tuple[int, BaseHeader]]] = defaultdict(list)

    for index, header in enumerate(headers):
        validated_header = _require_header_object(header, operation="deduplicate_headers")
        groups[validated_header.header_name.lower()].append((index, validated_header))

    ordered_keys = sorted(groups.keys(), key=lambda key: groups[key][0][0])
    deduplicated_headers: list[BaseHeader] = []
    duplicate_errors: list[str] = []

    for lowered_name in ordered_keys:
        entries = groups[lowered_name]

        if len(entries) == 1:
            _, header = entries[0]
            deduplicated_headers.append(_clone_as_custom_header(header.header_name, header.header_value))
            continue

        if lowered_name in multi_ok:
            for _, header in entries:
                deduplicated_headers.append(_clone_as_custom_header(header.header_name, header.header_value))
            continue

        resolved_headers, error_name = _resolve_duplicate_headers(
            lowered_name,
            entries,
            action=action,
            comma_join_ok=comma_join_ok,
            logger=log,
        )
        deduplicated_headers.extend(resolved_headers)

        if error_name is not None:
            duplicate_errors.append(error_name)

    if duplicate_errors:
        names = ", ".join(sorted(set(duplicate_errors)))
        raise ValueError(f"Duplicate header(s) not allowed: {names}. Define each at most once.")

    return deduplicated_headers


def allowlist_header_objects(  # noqa: PLR0913
    headers: Iterable[BaseHeader],
    *,
    allowed: Iterable[str],
    allow_extra: Iterable[str] | None = None,
    on_unexpected: OnUnexpectedPolicy = "raise",
    allow_x_prefixed: bool = False,
    logger: logging.Logger | None = None,
) -> list[BaseHeader]:
    """
    Filter header objects against a case-insensitive allowlist.
    """
    log = logger or logging.getLogger(__name__)
    allowed_lc = {header.lower() for header in allowed}
    if allow_extra:
        allowed_lc.update(header.lower() for header in allow_extra)

    kept: list[BaseHeader] = []
    unexpected_names: list[str] = []

    for header in headers:
        validated_header = _require_header_object(header, operation="allowlist_headers")
        header_name = validated_header.header_name
        lowered_name = header_name.lower()

        if _is_allowed_header_name(
            lowered_name,
            allowed=allowed_lc,
            allow_x_prefixed=allow_x_prefixed,
        ):
            kept.append(validated_header)
            continue

        if on_unexpected == "warn":
            log.warning("Unexpected header %r kept (not in allowlist)", header_name)
            kept.append(validated_header)
        elif on_unexpected == "drop":
            log.warning("Unexpected header %r dropped (not in allowlist)", header_name)
        else:
            unexpected_names.append(header_name)

    if unexpected_names:
        names = ", ".join(sorted(set(unexpected_names)))
        raise ValueError(
            f"Unexpected header(s) not in allowlist: {names}. Enable allow_extra or set on_unexpected to 'drop'/'warn'."
        )

    return kept


def _require_header_object(header: object, *, operation: str) -> BaseHeader:
    if not isinstance(header, BaseHeader):
        raise TypeError(f"{operation}() requires BaseHeader objects only")
    return header


def _clone_as_custom_header(name: str, value: str) -> BaseHeader:
    return CustomHeader(header=name, value=value)


def _resolve_duplicate_headers(
    lowered_name: str,
    entries: list[tuple[int, BaseHeader]],
    *,
    action: DeduplicateAction,
    comma_join_ok: frozenset[str],
    logger: logging.Logger,
) -> tuple[list[BaseHeader], str | None]:
    if action == "first":
        _, header = entries[0]
        if len(entries) > 1:
            logger.warning("Dropping duplicate header(s) for %r (keeping first)", header.header_name)
        return [_clone_as_custom_header(header.header_name, header.header_value)], None

    if action == "last":
        _, header = entries[-1]
        if len(entries) > 1:
            logger.warning("Dropping duplicate header(s) for %r (keeping last)", header.header_name)
        return [_clone_as_custom_header(header.header_name, header.header_value)], None

    if action == "concat":
        if lowered_name in comma_join_ok:
            name = entries[0][1].header_name
            joined_value = ", ".join(header.header_value for _, header in entries)
            return [_clone_as_custom_header(name, joined_value)], None

        return [], entries[0][1].header_name

    return [], entries[0][1].header_name


def _is_allowed_header_name(
    lowered_name: str,
    *,
    allowed: set[str],
    allow_x_prefixed: bool,
) -> bool:
    return lowered_name in allowed or (allow_x_prefixed and lowered_name.startswith("x-"))
