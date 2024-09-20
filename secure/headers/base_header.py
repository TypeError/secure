from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum


class HeaderName(Enum):
    CACHE_CONTROL = "Cache-Control"
    CONTENT_SECURITY_POLICY = "Content-Security-Policy"
    CONTENT_SECURITY_POLICY_REPORT_ONLY = "Content-Security-Policy-Report-Only"
    CROSS_ORIGIN_EMBEDDER_POLICY = "Cross-Origin-Embedder-Policy"
    CROSS_ORIGIN_OPENER_POLICY = "Cross-Origin-Opener-Policy"
    PERMISSION_POLICY = "Permissions-Policy"
    REFERRER_POLICY = "Referrer-Policy"
    SERVER = "Server"
    STRICT_TRANSPORT_SECURITY = "Strict-Transport-Security"
    X_CONTENT_TYPE_OPTIONS = "X-Content-Type-Options"
    X_FRAME_OPTIONS = "X-Frame-Options"


class HeaderDefaultValue(Enum):
    CACHE_CONTROL = "no-store"
    CONTENT_SECURITY_POLICY = "script-src 'self'; object-src 'self'"
    CROSS_ORIGIN_EMBEDDER_POLICY = "require-corp"
    CROSS_ORIGIN_OPENER_POLICY = "same-origin"
    PERMISSION_POLICY = "geolocation=(), microphone=(), camera=(), payment=()"
    REFERRER_POLICY = "no-referrer, strict-origin-when-cross-origin"
    SERVER = "NULL"
    STRICT_TRANSPORT_SECURITY = "max-age=63072000; includeSubdomains"
    X_CONTENT_TYPE_OPTIONS = "nosniff"
    X_FRAME_OPTIONS = "SAMEORIGIN"


@dataclass
class BaseHeader:
    """Base class for all header classes."""

    header_name: str

    @property
    @abstractmethod
    def header_value(self) -> str: ...
