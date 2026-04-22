from __future__ import annotations

from dataclasses import dataclass
import logging
from types import MappingProxyType
from typing import TYPE_CHECKING

from .constants import HEADER_NAME_RE

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    from .types import OnInvalidPolicy

SPACE_CODEPOINT = 0x20
VISIBLE_CHAR_MIN = 0x21
VISIBLE_CHAR_MAX = 0x7E
OBS_TEXT_MIN = 0x80
OBS_TEXT_MAX = 0xFF


@dataclass(frozen=True)
class _NormalizationOptions:
    on_invalid: OnInvalidPolicy
    strict: bool
    allow_obs_text: bool
    logger: logging.Logger


def normalize_header_items(
    items: Iterable[tuple[str, str]],
    *,
    on_invalid: OnInvalidPolicy = "drop",
    strict: bool = False,
    allow_obs_text: bool = False,
    logger: logging.Logger | None = None,
) -> Mapping[str, str]:
    """
    Validate and normalize header items into a single-valued immutable mapping.
    """
    options = _NormalizationOptions(
        on_invalid=on_invalid,
        strict=strict,
        allow_obs_text=allow_obs_text,
        logger=logger or logging.getLogger(__name__),
    )
    cleaned: dict[str, str] = {}
    seen_lc: set[str] = set()

    for name, value in items:
        pair = _validate_header_pair(
            name,
            value,
            options=options,
        )
        if pair is None:
            continue

        normalized_name, normalized_value = pair
        lowered_name = normalized_name.lower()

        if lowered_name in seen_lc:
            raise ValueError(
                f"Duplicate header {normalized_name!r} encountered during normalization. "
                "Run deduplicate_headers() first or use header_items() for multi-valued headers."
            )

        seen_lc.add(lowered_name)
        cleaned[normalized_name] = normalized_value

    return MappingProxyType(cleaned)


def _validate_header_pair(
    name: str,
    value: str,
    *,
    options: _NormalizationOptions,
) -> tuple[str, str] | None:
    normalized_name = name.strip()

    if not HEADER_NAME_RE.match(normalized_name):
        _handle_invalid(
            f"Invalid header name {normalized_name!r} (RFC 7230 token required)",
            options=options,
        )
        return None

    if value.startswith((" ", "\t")):
        _handle_invalid(
            f"Header {normalized_name!r} starts with forbidden whitespace",
            options=options,
        )
        return None

    normalized_value = value
    if ("\r" in normalized_value) or ("\n" in normalized_value):
        if options.strict:
            raise ValueError(f"Header {normalized_name!r} contained CR/LF")
        normalized_value = " ".join(normalized_value.splitlines())

    normalized_value = normalized_value.strip()
    if not normalized_value:
        _handle_invalid(
            f"Dropping header {normalized_name!r}: empty value",
            options=options,
        )
        return None

    if _value_is_allowed(normalized_value, allow_obs_text=options.allow_obs_text):
        return normalized_name, normalized_value

    sanitized_value = _sanitize_value(
        normalized_name,
        normalized_value,
        strict=options.strict,
        allow_obs_text=options.allow_obs_text,
    )
    if not sanitized_value:
        _handle_invalid(
            f"Dropping header {normalized_name!r}: empty after sanitization",
            options=options,
        )
        return None

    return normalized_name, sanitized_value


def _handle_invalid(message: str, *, options: _NormalizationOptions) -> None:
    if options.on_invalid == "warn":
        options.logger.warning(message)
    elif options.on_invalid == "raise":
        raise ValueError(message)


def _value_is_allowed(value: str, *, allow_obs_text: bool) -> bool:
    return all(_is_allowed_value_char(char, allow_obs_text=allow_obs_text) for char in value)


def _is_allowed_value_char(char: str, *, allow_obs_text: bool) -> bool:
    codepoint = ord(char)
    return (
        char == "\t"
        or codepoint == SPACE_CODEPOINT
        or VISIBLE_CHAR_MIN <= codepoint <= VISIBLE_CHAR_MAX
        or (allow_obs_text and OBS_TEXT_MIN <= codepoint <= OBS_TEXT_MAX)
    )


def _sanitize_value(name: str, value: str, *, strict: bool, allow_obs_text: bool) -> str:
    sanitized_characters: list[str] = []

    for char in value:
        codepoint = ord(char)
        if _is_allowed_value_char(char, allow_obs_text=allow_obs_text):
            sanitized_characters.append(char)
            continue

        if strict:
            raise ValueError(f"Header {name!r} contains disallowed char U+{codepoint:04X}")

        sanitized_characters.append(" ")

    return "".join(sanitized_characters).strip()
