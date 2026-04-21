from __future__ import annotations

from enum import Enum

from ..headers import (
    CacheControl,
    ContentSecurityPolicy,
    CrossOriginEmbedderPolicy,
    CrossOriginOpenerPolicy,
    CrossOriginResourcePolicy,
    CustomHeader,
    PermissionsPolicy,
    ReferrerPolicy,
    Server,
    StrictTransportSecurity,
    XContentTypeOptions,
    XDnsPrefetchControl,
    XFrameOptions,
    XPermittedCrossDomainPolicies,
)


class Preset(Enum):
    """Predefined security header presets for :class:`Secure`."""

    BASIC = "basic"
    BALANCED = "balanced"
    STRICT = "strict"


def _baseline_content_security_policy() -> ContentSecurityPolicy:
    """Shared CSP builder used by the BASIC and BALANCED presets."""
    return (
        ContentSecurityPolicy()
        .default_src("'self'")
        .base_uri("'self'")
        .font_src("'self'", "https:", "data:")
        .form_action("'self'")
        .frame_ancestors("'self'")
        .img_src("'self'", "data:")
        .object_src("'none'")
        .script_src("'self'")
        .script_src_attr("'none'")
        .style_src("'self'", "https:", "'unsafe-inline'")
        .upgrade_insecure_requests()
    )


def preset_kwargs(preset: Preset) -> dict[str, object]:
    """Return constructor kwargs for a predefined :class:`Secure` preset."""
    match preset:
        case Preset.BASIC:
            return {
                "coop": CrossOriginOpenerPolicy().same_origin(),
                "csp": _baseline_content_security_policy(),
                "corp": CrossOriginResourcePolicy().same_origin(),
                "hsts": StrictTransportSecurity().max_age(31536000).include_subdomains(),
                "referrer": ReferrerPolicy().no_referrer(),
                "xcto": XContentTypeOptions().nosniff(),
                "xfo": XFrameOptions().sameorigin(),
                "xdfc": XDnsPrefetchControl().disable(),
                "xpcdp": XPermittedCrossDomainPolicies().none(),
                "custom": [
                    CustomHeader(
                        header="Origin-Agent-Cluster",
                        value="?1",
                    ),
                    CustomHeader(
                        header="X-Download-Options",
                        value="noopen",
                    ),
                    CustomHeader(
                        header="X-XSS-Protection",
                        value="0",
                    ),
                ],
            }
        case Preset.BALANCED:
            return {
                "coop": CrossOriginOpenerPolicy().same_origin(),
                "corp": CrossOriginResourcePolicy().same_origin(),
                "csp": _baseline_content_security_policy(),
                "hsts": StrictTransportSecurity().max_age(31536000).include_subdomains(),
                "permissions": PermissionsPolicy().geolocation().microphone().camera(),
                "referrer": ReferrerPolicy().strict_origin_when_cross_origin(),
                "server": Server().set(""),
                "xcto": XContentTypeOptions().nosniff(),
                "xfo": XFrameOptions().sameorigin(),
            }
        case Preset.STRICT:
            return {
                "cache": CacheControl().no_store().max_age(0),
                "coep": CrossOriginEmbedderPolicy().require_corp(),
                "coop": CrossOriginOpenerPolicy().same_origin(),
                "csp": (
                    ContentSecurityPolicy()
                    .default_src("'self'")
                    .script_src("'self'")
                    .style_src("'self'")
                    .object_src("'none'")
                    .base_uri("'none'")
                    .frame_ancestors("'none'")
                ),
                "hsts": StrictTransportSecurity().max_age(63072000).include_subdomains(),
                "permissions": PermissionsPolicy().geolocation().microphone().camera(),
                "referrer": ReferrerPolicy().no_referrer(),
                "server": Server().set(""),
                "xcto": XContentTypeOptions().nosniff(),
                "xfo": XFrameOptions().deny(),
            }
        case _:
            raise ValueError(f"Unknown preset: {preset}")
