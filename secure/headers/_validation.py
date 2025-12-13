from __future__ import annotations


def normalize_header_value(value: str, *, what: str = "header value") -> str:
    """
    Trim whitespace and reject CR/LF characters in header strings.

    Args:
        value: Raw header string.
        what: Description of the value (used for error messages).

    Returns:
        The stripped string without CR/LF characters.

    Raises:
        ValueError: If CR or LF are present.
    """
    if "\r" in value or "\n" in value:
        raise ValueError(f"{what} must not contain CR/LF characters")
    return value.strip()
