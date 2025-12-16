import unittest

from secure.headers import (
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
from secure.headers.base_header import HeaderDefaultValue


class TestHeaderConsistency(unittest.TestCase):
    def test_value_methods_reject_crlf(self) -> None:
        """Ensure every header's `value()` method rejects CR/LF injections."""
        factories = [
            ("CacheControl", lambda: CacheControl()),
            ("ContentSecurityPolicy", lambda: ContentSecurityPolicy()),
            ("CrossOriginEmbedderPolicy", lambda: CrossOriginEmbedderPolicy()),
            ("CrossOriginOpenerPolicy", lambda: CrossOriginOpenerPolicy()),
            ("CrossOriginResourcePolicy", lambda: CrossOriginResourcePolicy()),
            ("PermissionsPolicy", lambda: PermissionsPolicy()),
            ("ReferrerPolicy", lambda: ReferrerPolicy()),
            ("Server", lambda: Server()),
            ("StrictTransportSecurity", lambda: StrictTransportSecurity()),
            ("XContentTypeOptions", lambda: XContentTypeOptions()),
            ("XDnsPrefetchControl", lambda: XDnsPrefetchControl()),
            ("XFrameOptions", lambda: XFrameOptions()),
            ("XPermittedCrossDomainPolicies", lambda: XPermittedCrossDomainPolicies()),
            ("CustomHeader", lambda: CustomHeader("X-Test", "value")),
        ]

        for name, factory in factories:
            header = factory()
            with self.subTest(header=name), self.assertRaises(ValueError):
                header.value("bad\rvalue")

    def test_clear_restores_default_values(self) -> None:
        """Each header should return to its library default after `clear()`."""
        cases = [
            (CacheControl(), "public, max-age=60", HeaderDefaultValue.CACHE_CONTROL.value),
            (
                ContentSecurityPolicy(),
                "default-src 'self'",
                HeaderDefaultValue.CONTENT_SECURITY_POLICY.value,
            ),
            (CrossOriginEmbedderPolicy(), "unsafe-none", HeaderDefaultValue.CROSS_ORIGIN_EMBEDDER_POLICY.value),
            (CrossOriginOpenerPolicy(), "unsafe-none", HeaderDefaultValue.CROSS_ORIGIN_OPENER_POLICY.value),
            (CrossOriginResourcePolicy(), "cross-origin", HeaderDefaultValue.CROSS_ORIGIN_RESOURCE_POLICY.value),
            (PermissionsPolicy(), "geolocation=()", HeaderDefaultValue.PERMISSION_POLICY.value),
            (ReferrerPolicy(), "no-referrer", HeaderDefaultValue.REFERRER_POLICY.value),
            (Server(), "Custom", HeaderDefaultValue.SERVER.value),
            (StrictTransportSecurity(), "max-age=0", HeaderDefaultValue.STRICT_TRANSPORT_SECURITY.value),
            (XContentTypeOptions(), "detect", HeaderDefaultValue.X_CONTENT_TYPE_OPTIONS.value),
            (XDnsPrefetchControl(), "on", HeaderDefaultValue.X_DNS_PREFETCH_CONTROL.value),
            (XFrameOptions(), "DENY", HeaderDefaultValue.X_FRAME_OPTIONS.value),
            (XPermittedCrossDomainPolicies(), "all", HeaderDefaultValue.X_PERMITTED_CROSS_DOMAIN_POLICIES.value),
        ]

        for header, value, expected in cases:
            header.value(value)
            header.clear()
            with self.subTest(header=header.__class__.__name__):
                self.assertEqual(header.header_value, expected)

    def test_cache_control_canonical_order(self) -> None:
        """Canonical ordering should be stable regardless of helper call order."""
        cc = CacheControl().public().max_age(60).no_cache()
        self.assertEqual(cc.header_value, "no-cache, public, max-age=60")

    def test_content_security_policy_values_deduplicate(self) -> None:
        """Duplicate tokens for the same directive should be ignored."""
        csp = ContentSecurityPolicy().default_src("'self'").custom_directive("default-src", "'self'", "https:")
        self.assertEqual(csp.header_value, "default-src 'self' https:")

    def test_permissions_policy_wildcard_must_be_alone(self) -> None:
        policy = PermissionsPolicy().camera("*")
        with self.assertRaises(ValueError):
            policy.camera("*", "self")

    def test_referrer_policy_add_is_idempotent(self) -> None:
        rp = ReferrerPolicy().add("no-referrer").add("no-referrer").add("same-origin")
        self.assertEqual(rp.header_value, "no-referrer, same-origin")

    def test_xdns_prefetch_control_normalizes_values(self) -> None:
        xdfc = XDnsPrefetchControl().set("ON").set("OFF")
        self.assertEqual(xdfc.header_value, "off")
        xdfc.on()
        self.assertEqual(xdfc.header_value, "on")
        xdfc.off()
        self.assertEqual(xdfc.header_value, "off")

    def test_x_permitted_policy_rejects_unknown(self) -> None:
        with self.assertRaises(ValueError):
            XPermittedCrossDomainPolicies().policy("unsupported")  # type: ignore
