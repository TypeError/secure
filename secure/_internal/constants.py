from __future__ import annotations

import re

# Headers that may appear multiple times as separate fields.
MULTI_OK: frozenset[str] = frozenset(
    {
        "content-security-policy",
    }
)

# Headers where RFC7230-style comma merging is safe/expected.
COMMA_JOIN_OK: frozenset[str] = frozenset({"cache-control"})

# A default allowlist of secure headers.
DEFAULT_ALLOWED_HEADERS: frozenset[str] = frozenset(
    {
        "cache-control",
        "content-security-policy",
        "content-security-policy-report-only",
        "cross-origin-embedder-policy",
        "cross-origin-opener-policy",
        "cross-origin-resource-policy",
        "origin-agent-cluster",
        "permissions-policy",
        "referrer-policy",
        "server",
        "strict-transport-security",
        "x-content-type-options",
        "x-dns-prefetch-control",
        "x-download-options",
        "x-frame-options",
        "x-permitted-cross-domain-policies",
        "x-xss-protection",
    }
)

# RFC 7230 token (visible ASCII except separators).
HEADER_NAME_RE = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")
