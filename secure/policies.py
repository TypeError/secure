class SecurePolicies:
    class CSP:
        def __init__(self):
            self.csp_policy = True
            self.policy = []

        def base_uri(self, *options):
            self.policy.append(("base-uri", options))
            return self

        def block_all_mixed_content(self):
            self.policy.append(("block-all-mixed-content", False))
            return self

        def connect_src(self, *options):
            self.policy.append(("connect-src", options))
            return self

        def default_src(self, *options):
            self.policy.append(("default-src", options))
            return self

        def font_src(self, *options):
            self.policy.append(("font-src", options))
            return self

        def form_action(self, *options):
            self.policy.append(("form-action", options))
            return self

        def frame_ancestors(self, *options):
            self.policy.append(("frame-ancestors", options))
            return self

        def frame_src(self):
            self.policy.append(("frame-src", False))
            return self

        def img_src(self, *options):
            self.policy.append(("img-src", options))
            return self

        def manifest_src(self, *options):
            self.policy.append(("manifest-src", options))
            return self

        def media_src(self, *options):
            self.policy.append(("media-src", options))
            return self

        def object_src(self, *options):
            self.policy.append(("object-src", options))
            return self

        def plugin_types(self, *options):
            self.policy.append(("plugin-types", options))
            return self

        def require_sri_for(self, *options):
            self.policy.append(("require-sri-for", options))
            return self

        def report_to(self, json_object):
            self.policy.append(("report-to", json_object))
            return self

        def report_uri(self, uri):
            self.policy.append(("report-uri", uri))
            return self

        def sandbox(self, *options):
            self.policy.append(("sandbox", options))
            return self

        def script_nonce(self, *options):
            self.policy.append(("script-nonce", options))
            return self

        def script_src(self, *options):
            self.policy.append(("script-src", options))
            return self

        def style_src(self, *options):
            self.policy.append(("style-src", options))
            return self

        def upgrade_insecure_requests(self):
            self.policy.append(("upgrade-insecure-requests", False))
            return self

        def worker_src(self, *options):
            self.policy.append(("worker-src", options))
            return self

        class Values:
            self_ = "'self'"
            none = "'none'"
            unsafe_inline = "'unsafe-inline'"
            unsafe_eval = "'unsafe-eval'"
            strict_dynamic = "'strict-dynamic'"

            @staticmethod
            def Nonce(nonce_value):
                value = "'nonce-<{}>'".format(nonce_value)
                return value

    class XFO:
        def __init__(self):
            self.xfo_policy = True
            self.policy = ""

        def allow_from(self, uri):
            self.policy = "allow-from {}".format(uri)
            return self

        def deny(self):
            self.policy = "deny"
            return self

        def sameorigin(self):
            self.policy = "sameorigin"
            return self

    class XXP:
        def __init__(self):
            self.xxp_policy = True
            self.policy = ""

        def disabled(self):
            self.policy = "0"
            return self

        def enabled(self):
            self.policy = "1"
            return self

        def enabled_block(self):
            self.policy = "1; mode=block"
            return self

        def enabled_report(self, uri):
            self.policy = "1; report={}".format(uri)
            return self

    class Referrer:
        def __init__(self):
            self.referrer_policy = True
            self.policy = []

        def no_referrer(self):
            self.policy.append("no-referrer")
            return self

        def no_referrer_when_downgrade(self):
            self.policy.append("no-referrer-when-downgrade")
            return self

        def origin(self):
            self.policy.append("origin")
            return self

        def origin_when_cross_origin(self):
            self.policy.append("origin-when-cross-origin")
            return self

        def same_origin(self):
            self.policy.append("same-origin")
            return self

        def strict_origin(self):
            self.policy.append("strict-origin")
            return self

        def strict_origin_when_cross_origin(self):
            self.policy.append("strict-origin-when-cross-origin")
            return self

        def unsafe_url(self):
            self.policy.append("unsafe-url")
            return self

    class Seconds:
        five_minutes = "300"
        one_week = "604800"
        one_month = "2592000"
        one_year = "31536000"
        two_years = "63072000"

    class HSTS:
        def __init__(self):
            self.hsts_policy = True
            self.policy = []

        def include_subDomains(self):
            self.policy.append("includeSubDomains")
            return self

        def max_age(self, seconds):
            self.policy.append("max-age={}".format(seconds))
            return self

        def preload(self):
            self.policy.append("preload")
            return self

    class Cache:
        def __init__(self):
            self.cache_policy = True
            self.policy = []

        def immutable(self):
            self.policy.append("immutable")
            return self

        def max_age(self, seconds):
            self.policy.append("max-age={}".format(seconds))
            return self

        def max_stale(self, seconds):
            self.policy.append("max-stale={}".format(seconds))
            return self

        def min_fresh(self, seconds):
            self.policy.append("min-fresh={}".format(seconds))
            return self

        def must_revalidate(self):
            self.policy.append("must-revalidate")
            return self

        def no_cache(self):
            self.policy.append("no-cache")
            return self

        def no_store(self):
            self.policy.append("no-store")
            return self

        def no_transform(self):
            self.policy.append("no-transform")
            return self

        def only_if_cached(self):
            self.policy.append("only-if-cached")
            return self

        def private(self):
            self.policy.append("private")
            return self

        def proxy_revalidate(self):
            self.policy.append("proxy-revalidate")
            return self

        def public(self):
            self.policy.append("public")
            return self

        def s_maxage(self, seconds):
            self.policy.append("s-maxage={}".format(seconds))
            return self

        def stale_if_error(self, seconds):
            self.policy.append("stale-if-error={}".format(seconds))
            return self

        def stale_while_revalidate(self, seconds):
            self.policy.append("stale-while-revalidate={}".format(seconds))
            return self

    class Feature:
        def __init__(self):
            self.feature_policy = True
            self.policy = []

        def accelerometer(self, *options):
            self.policy.append(("accelerometer", options))
            return self

        def ambient_light_sensor(self, *options):
            self.policy.append(("ambient-light-sensor ", options))
            return self

        def autoplay(self, *options):
            self.policy.append(("autoplay", options))
            return self

        def camera(self, *options):
            self.policy.append(("camera", options))
            return self

        def document_domain(self, *options):
            self.policy.append(("document-domain", options))
            return self

        def encrypted_media(self, *options):
            self.policy.append(("encrypted-media", options))
            return self

        def fullscreen(self, *options):
            self.policy.append(("fullscreen", options))
            return self

        def geolocation(self, *options):
            self.policy.append(("geolocation", options))
            return self

        def gyroscope(self, *options):
            self.policy.append(("gyroscope", options))
            return self

        def magnetometer(self, *options):
            self.policy.append(("magnetometer", options))
            return self

        def microphone(self, *options):
            self.policy.append(("microphone", options))
            return self

        def midi(self, *options):
            self.policy.append(("midi", options))
            return self

        def payment(self, *options):
            self.policy.append(("payment", options))
            return self

        def picture_in_picture(self, *options):
            self.policy.append(("picture-in-picture", options))
            return self

        def speaker(self, *options):
            self.policy.append(("speaker", options))
            return self

        def sync_xhr(self, *options):
            self.policy.append(("sync-xhr", options))
            return self

        def usb(self, *options):
            self.policy.append(("usb", options))
            return self

        def vr(self, *options):
            self.policy.append(("vr", options))
            return self

        class Values:
            self_ = "'self'"
            none = "'none'"
            src = "'src'"
            all = "*"


def get_policy(policy, separator):
    if type(policy.policy) is list:
        value = "{}".format(separator).join(policy.policy)
    else:
        value = policy.policy
    return value


def get_policy_multi_opt(policy):
    values = []
    for option in policy.policy:
        directive = option[0]
        if option[1]:
            if option[1] is list:
                resources = " ".join(option[1])
            else:
                resources = option[1]
            values.append("{} {}".format(directive, resources))
        else:
            values.append(directive)
    value = "; ".join(values)
    return value
