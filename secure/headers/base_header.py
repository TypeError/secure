from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum


class HeaderName(Enum):
    """Enumeration of standard HTTP security headers.

    This enum provides the header names for various security headers
    like Cache-Control, Content-Security-Policy, Strict-Transport-Security, etc.
    It is used to ensure consistency in header naming across the codebase.
    """

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
    """Enumeration of default values for standard HTTP security headers.

    This enum provides default values for headers like Cache-Control, Content-Security-Policy,
    Strict-Transport-Security, and others. These values represent recommended security defaults
    where applicable.
    """

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
    """Abstract base class for HTTP security headers.

    This class defines the basic structure for security headers by requiring
    derived classes to implement the `header_value` property, which provides
    the value of the header.

    Attributes:
        header_name (str): The name of the security header.
    """

    header_name: str

    @property
    @abstractmethod
    def header_value(self) -> str:
        """Abstract property for getting the header value.

        This property should be implemented by subclasses to return the
        security header's value.

        Returns:
            str: The value of the header.
        """
        ...
