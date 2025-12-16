from collections.abc import Callable
from dataclasses import dataclass
from typing import ClassVar
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
from secure.headers.base_header import BaseHeader, HeaderDefaultValue, HeaderName


@dataclass(frozen=True)
class HeaderSpec:
    name: str
    factory: Callable[[], BaseHeader]
    default: str
    expected_header_name: str
    builder: Callable[[], BaseHeader]
    builder_expected: str
    invalid: Callable[[], BaseHeader]
    deterministic: tuple[Callable[[], BaseHeader], Callable[[], BaseHeader]]
    supports_clear: bool = True


class TestHeaderContracts(unittest.TestCase):
    HEADER_SPECS: ClassVar[tuple[HeaderSpec, ...]] = (
        HeaderSpec(
            name="CacheControl",
            factory=lambda: CacheControl(),
            default=HeaderDefaultValue.CACHE_CONTROL.value,
            expected_header_name=HeaderName.CACHE_CONTROL.value,
            builder=lambda: CacheControl().no_cache().max_age(60),
            builder_expected="no-cache, max-age=60",
            invalid=lambda: CacheControl().max_age(-1),
            deterministic=(
                lambda: CacheControl().no_cache().max_age(60),
                lambda: CacheControl().no_cache().max_age(60).no_cache(),
            ),
        ),
        HeaderSpec(
            name="ContentSecurityPolicy",
            factory=lambda: ContentSecurityPolicy(),
            default=HeaderDefaultValue.CONTENT_SECURITY_POLICY.value,
            expected_header_name=HeaderName.CONTENT_SECURITY_POLICY.value,
            builder=lambda: ContentSecurityPolicy().default_src("'none'").script_src("'self'").img_src("'self'"),
            builder_expected="default-src 'none'; script-src 'self'; img-src 'self'",
            invalid=lambda: ContentSecurityPolicy().custom_directive("invalid name!", "'self'"),
            deterministic=(
                lambda: ContentSecurityPolicy().script_src("'self'"),
                lambda: ContentSecurityPolicy().script_src("'self'").script_src("'self'"),
            ),
        ),
        HeaderSpec(
            name="CrossOriginEmbedderPolicy",
            factory=lambda: CrossOriginEmbedderPolicy(),
            default=HeaderDefaultValue.CROSS_ORIGIN_EMBEDDER_POLICY.value,
            expected_header_name=HeaderName.CROSS_ORIGIN_EMBEDDER_POLICY.value,
            builder=lambda: CrossOriginEmbedderPolicy().credentialless(),
            builder_expected="credentialless",
            invalid=lambda: CrossOriginEmbedderPolicy().set("bad\nvalue"),
            deterministic=(
                lambda: CrossOriginEmbedderPolicy().require_corp(),
                lambda: CrossOriginEmbedderPolicy().require_corp().require_corp(),
            ),
        ),
        HeaderSpec(
            name="CrossOriginOpenerPolicy",
            factory=lambda: CrossOriginOpenerPolicy(),
            default=HeaderDefaultValue.CROSS_ORIGIN_OPENER_POLICY.value,
            expected_header_name=HeaderName.CROSS_ORIGIN_OPENER_POLICY.value,
            builder=lambda: CrossOriginOpenerPolicy().same_origin_allow_popups(),
            builder_expected="same-origin-allow-popups",
            invalid=lambda: CrossOriginOpenerPolicy().value("bad\rvalue"),
            deterministic=(
                lambda: CrossOriginOpenerPolicy().same_origin(),
                lambda: CrossOriginOpenerPolicy().same_origin().same_origin(),
            ),
        ),
        HeaderSpec(
            name="CrossOriginResourcePolicy",
            factory=lambda: CrossOriginResourcePolicy(),
            default=HeaderDefaultValue.CROSS_ORIGIN_RESOURCE_POLICY.value,
            expected_header_name=HeaderName.CROSS_ORIGIN_RESOURCE_POLICY.value,
            builder=lambda: CrossOriginResourcePolicy().same_site(),
            builder_expected="same-site",
            invalid=lambda: CrossOriginResourcePolicy().value("bad\nvalue"),
            deterministic=(
                lambda: CrossOriginResourcePolicy().same_origin(),
                lambda: CrossOriginResourcePolicy().same_origin().same_origin(),
            ),
        ),
        HeaderSpec(
            name="CustomHeader",
            factory=lambda: CustomHeader("X-Test", "initial"),
            default="initial",
            expected_header_name="X-Test",
            builder=lambda: CustomHeader("X-Test", "initial").set("updated"),
            builder_expected="updated",
            invalid=lambda: CustomHeader("Bad\rName", "value"),
            deterministic=(
                lambda: CustomHeader("X-Test", "value"),
                lambda: CustomHeader("X-Test", "value").set("value"),
            ),
            supports_clear=False,
        ),
        HeaderSpec(
            name="PermissionsPolicy",
            factory=lambda: PermissionsPolicy(),
            default=HeaderDefaultValue.PERMISSION_POLICY.value,
            expected_header_name=HeaderName.PERMISSION_POLICY.value,
            builder=lambda: PermissionsPolicy().camera("'self'"),
            builder_expected="camera=(self)",
            invalid=lambda: PermissionsPolicy().add_directive("bad name", "'self'"),
            deterministic=(
                lambda: PermissionsPolicy().camera("'self'"),
                lambda: PermissionsPolicy().camera("'self'").camera("'self'"),
            ),
        ),
        HeaderSpec(
            name="ReferrerPolicy",
            factory=lambda: ReferrerPolicy(),
            default=HeaderDefaultValue.REFERRER_POLICY.value,
            expected_header_name=HeaderName.REFERRER_POLICY.value,
            builder=lambda: ReferrerPolicy().fallback("no-referrer", "origin"),
            builder_expected="no-referrer, origin",
            invalid=lambda: ReferrerPolicy().add("no referrer"),
            deterministic=(
                lambda: ReferrerPolicy().add("no-referrer"),
                lambda: ReferrerPolicy().add("no-referrer").add("no-referrer"),
            ),
        ),
        HeaderSpec(
            name="Server",
            factory=lambda: Server(),
            default=HeaderDefaultValue.SERVER.value,
            expected_header_name=HeaderName.SERVER.value,
            builder=lambda: Server().set("CustomServer"),
            builder_expected="CustomServer",
            invalid=lambda: Server().set("bad\nvalue"),
            deterministic=(
                lambda: Server().set("CustomServer"),
                lambda: Server().set("CustomServer").set("CustomServer"),
            ),
        ),
        HeaderSpec(
            name="StrictTransportSecurity",
            factory=lambda: StrictTransportSecurity(),
            default=HeaderDefaultValue.STRICT_TRANSPORT_SECURITY.value,
            expected_header_name=HeaderName.STRICT_TRANSPORT_SECURITY.value,
            builder=lambda: StrictTransportSecurity().max_age(172800).include_subdomains(),
            builder_expected="max-age=172800; includeSubDomains",
            invalid=lambda: StrictTransportSecurity().max_age(-1),
            deterministic=(
                lambda: StrictTransportSecurity().max_age(60).include_subdomains(),
                lambda: StrictTransportSecurity().max_age(60).include_subdomains().include_subdomains(),
            ),
        ),
        HeaderSpec(
            name="XContentTypeOptions",
            factory=lambda: XContentTypeOptions(),
            default=HeaderDefaultValue.X_CONTENT_TYPE_OPTIONS.value,
            expected_header_name=HeaderName.X_CONTENT_TYPE_OPTIONS.value,
            builder=lambda: XContentTypeOptions().nosniff(),
            builder_expected="nosniff",
            invalid=lambda: XContentTypeOptions().set("bad\rvalue"),
            deterministic=(
                lambda: XContentTypeOptions().nosniff(),
                lambda: XContentTypeOptions().nosniff().nosniff(),
            ),
        ),
        HeaderSpec(
            name="XDnsPrefetchControl",
            factory=lambda: XDnsPrefetchControl(),
            default=HeaderDefaultValue.X_DNS_PREFETCH_CONTROL.value,
            expected_header_name=HeaderName.X_DNS_PREFETCH_CONTROL.value,
            builder=lambda: XDnsPrefetchControl().on(),
            builder_expected="on",
            invalid=lambda: XDnsPrefetchControl().set("bad\nvalue"),
            deterministic=(
                lambda: XDnsPrefetchControl().on(),
                lambda: XDnsPrefetchControl().on().on(),
            ),
        ),
        HeaderSpec(
            name="XFrameOptions",
            factory=lambda: XFrameOptions(),
            default=HeaderDefaultValue.X_FRAME_OPTIONS.value,
            expected_header_name=HeaderName.X_FRAME_OPTIONS.value,
            builder=lambda: XFrameOptions().allow_from("https://example.com"),
            builder_expected="ALLOW-FROM https://example.com",
            invalid=lambda: XFrameOptions().value("bad\rvalue"),
            deterministic=(
                lambda: XFrameOptions().deny(),
                lambda: XFrameOptions().deny().deny(),
            ),
        ),
        HeaderSpec(
            name="XPermittedCrossDomainPolicies",
            factory=lambda: XPermittedCrossDomainPolicies(),
            default=HeaderDefaultValue.X_PERMITTED_CROSS_DOMAIN_POLICIES.value,
            expected_header_name=HeaderName.X_PERMITTED_CROSS_DOMAIN_POLICIES.value,
            builder=lambda: XPermittedCrossDomainPolicies().all(),
            builder_expected="all",
            invalid=lambda: XPermittedCrossDomainPolicies().policy("unsupported"),  # type: ignore[arg-type]
            deterministic=(
                lambda: XPermittedCrossDomainPolicies().none(),
                lambda: XPermittedCrossDomainPolicies().none().none(),
            ),
        ),
    )

    def test_default_values(self) -> None:
        for spec in self.HEADER_SPECS:
            with self.subTest(header=spec.name):
                header = spec.factory()
                self.assertEqual(header.header_value, spec.default)

    def test_header_names(self) -> None:
        for spec in self.HEADER_SPECS:
            with self.subTest(header=spec.name):
                header = spec.factory()
                self.assertEqual(header.header_name, spec.expected_header_name)

    def test_clear_resets_default(self) -> None:
        for spec in self.HEADER_SPECS:
            if not spec.supports_clear:
                continue
            with self.subTest(header=spec.name):
                header = spec.builder()
                header.clear()
                self.assertEqual(header.header_value, spec.default)

    def test_builder_helpers(self) -> None:
        for spec in self.HEADER_SPECS:
            with self.subTest(header=spec.name):
                header = spec.builder()
                self.assertEqual(header.header_value, spec.builder_expected)

    def test_invalid_inputs_raise(self) -> None:
        for spec in self.HEADER_SPECS:
            with self.subTest(header=spec.name), self.assertRaises(ValueError):
                spec.invalid()

    def test_deterministic_output(self) -> None:
        for spec in self.HEADER_SPECS:
            first_fn, second_fn = spec.deterministic
            with self.subTest(header=spec.name):
                first = first_fn()
                second = second_fn()
                self.assertEqual(first.header_value, second.header_value)


if __name__ == "__main__":
    unittest.main()
