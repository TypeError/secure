# Security header recommendations and information from the MDN Web Docs and the OWASP Secure Headers Project
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
# https://owasp.org/www-project-secure-headers/#cache-control

from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum


class HeaderName(Enum):
    """Enumeration of standard HTTP security headers.

    This enum provides the header names for various security headers
    like Cache-Control, Content-Security-Policy, Strict-Transport-Security, etc.
    It is used to ensure consistency in header naming across the codebase.
    """

    # Caching
    CACHE_CONTROL = "Cache-Control"

    # Content policy
    CONTENT_SECURITY_POLICY = "Content-Security-Policy"

    # Content policy (report-only)
    CONTENT_SECURITY_POLICY_REPORT_ONLY = "Content-Security-Policy-Report-Only"

    # Embedding security
    CROSS_ORIGIN_EMBEDDER_POLICY = "Cross-Origin-Embedder-Policy"

    # Context isolation
    CROSS_ORIGIN_OPENER_POLICY = "Cross-Origin-Opener-Policy"

    # Permissions
    PERMISSION_POLICY = "Permissions-Policy"

    # Referrer control
    REFERRER_POLICY = "Referrer-Policy"

    # Server identification
    SERVER = "Server"

    # HTTPS enforcement
    STRICT_TRANSPORT_SECURITY = "Strict-Transport-Security"

    # MIME type protection
    X_CONTENT_TYPE_OPTIONS = "X-Content-Type-Options"

    # Clickjacking protection
    X_FRAME_OPTIONS = "X-Frame-Options"


class HeaderDefaultValue(Enum):
    """Enumeration of default values for standard HTTP security headers.

    This enum provides default values for headers like Cache-Control, Content-Security-Policy,
    Strict-Transport-Security, and others. These values represent recommended security defaults
    where applicable.
    """

    # Cache-Control to prevent caching of sensitive data
    CACHE_CONTROL = "no-store"

    # Basic Content Security Policy to allow resources only from the same origin
    CONTENT_SECURITY_POLICY = (
        "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'"
    )

    # Cross-Origin Embedder Policy set to 'require-corp' to enforce stricter security.
    # This ensures that embedded cross-origin resources must explicitly allow being embedded.
    # Note: This may break third-party content that does not allow cross-origin embedding.
    CROSS_ORIGIN_EMBEDDER_POLICY = "require-corp"

    # Cross-Origin Opener Policy to isolate browsing contexts and prevent cross-origin leaks
    CROSS_ORIGIN_OPENER_POLICY = "same-origin"

    # Permissions Policy to disable risky features by default (geolocation, microphone, camera)
    PERMISSION_POLICY = "geolocation=(), microphone=(), camera=()"

    # Referrer Policy to balance security and usability, limits information sent on cross-origin requests
    REFERRER_POLICY = "strict-origin-when-cross-origin"

    # Server header omitted to hide server details from attackers
    SERVER = ""

    # Strict Transport Security to enforce HTTPS for one year
    STRICT_TRANSPORT_SECURITY = "max-age=31536000"

    # Prevent MIME-type sniffing to block potential security threats from improperly typed content
    X_CONTENT_TYPE_OPTIONS = "nosniff"

    # Clickjacking protection, allows framing only from the same origin
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
