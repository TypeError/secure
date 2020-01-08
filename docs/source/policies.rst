Policy Builder
----------------

CSP()
^^^^^^^

**Directives:** ``base_uri(sources)``, ``block_all_mixed_content()``,
``child_src(sources)``, ``connect_src(sources)``,
``default_src(sources)``, ``font_src(sources)``,
``form_action(sources)``, ``frame_ancestors(sources)``,
``frame_src(sources)``, ``img_src(sources)``,
``manifest_src(sources)``, ``media_src(sources)``,
``object_src(sources)``, ``plugin_types(types)``,
``report_to(json_object)``, ``report_uri(uri)``,
``require_sri_for(values)``, ``sandbox(values)``,
``script_src(sources)``, ``style_src(sources)``,
``upgrade_insecure_requests()``, ``worker_src(sources)``

**Values()**: ``self_``, ``none``, ``unsafe_inline``, ``unsafe_eval``,
``strict_dynamic``, ``nonce(nonce_value)``, ``all`` = "*"

**Example:**

.. code:: python

   csp_value = (
       SecurePolicies.CSP()
       .default_src(SecurePolicies.CSP().Values.none)
       .base_uri(SecurePolicies.CSP().Values.self_)
       .block_all_mixed_content()
       .connect_src(SecurePolicies.CSP().Values.self_, "api.spam.com")
       .frame_src(SecurePolicies.CSP().Values.none)
       .img_src(SecurePolicies.CSP().Values.self_, "static.spam.com")
   )

   # default-src 'none'; base-uri 'self'; block-all-mixed-content; connect-src 'self' api.spam.com; frame-src 'none'; img-src 'self' static.spam.com

*You can check the effectiveness of your CSP Policy at the* `CSP
Evaluator <https://csp-evaluator.withgoogle.com>`__

HSTS()
^^^^^^^

**Directives:** ``include_subDomains()``, ``max_age(seconds)``,
``preload()``

**Example:**

.. code:: python

   hsts_value = (
       SecurePolicies.HSTS()
       .include_subdomains()
       .preload()
       .max_age(SecurePolicies.Seconds.one_month)
   )

   # includeSubDomains; preload; max-age=2592000

XXP()
^^^^^^

**Directives:** ``disabled()`` = 0, ``enabled()`` = 1,
``enabled_block()`` = 1; mode=block, ``enabled_report(uri)`` = 1;
report=uri

**Example:**

.. code:: python

   xxp_value = SecurePolicies.XXP().enabled_block()

   # 1; mode=block

XFO()
^^^^^^

**Directives:** ``allow_from(uri)``, ``deny()``, ``sameorigin()``

**Example:**

.. code:: python

   xfo_value = SecurePolicies.XFO().deny()

   # deny

Referrer()
^^^^^^^^^^^

**Directives:** ``no_referrer()``, ``no_referrer_when_downgrade()``,
``origin()``, ``origin_when_cross_origin()``, ``same_origin()``,
``strict_origin()``, ``strict_origin_when_cross_origin()``,
``unsafe_url()``

**Example:**

.. code:: python

   referrer_value = SecurePolicies.Referrer().no_referrer()

   # no-referrer

Feature()
^^^^^^^^^^

**Directives:** ``accelerometer(allowlist)``,
``ambient_light_sensor(allowlist)``, ``autoplay(allowlist)``,
``camera(allowlist)``, ``document_domain(allowlist)``,
``encrypted_media(allowlist)``, ``fullscreen(allowlist)``,
``geolocation(allowlist)``, ``gyroscope(allowlist)``,
``magnetometer(allowlist)``, ``microphone(allowlist)``,
``midi(allowlist)``, ``payment(allowlist)``,
``picture_in_picture(allowlist)``, ``speaker(allowlist)``,
``sync_xhr(allowlist)``, ``usb(allowlist)``, ``Values(allowlist)``,
``vr(allowlist)``

**Values()**: ``self_``, ``none``, ``src``, ``all_`` = "*"

**Example:**

.. code:: python

   feature_value = (
       SecurePolicies.Feature()
       .geolocation(SecurePolicies.Feature.Values.self_, "spam.com")
       .vibrate(SecurePolicies.Feature.Values.none)
   )

   # geolocation 'self' spam.com; vibrate 'none'

Cache()
^^^^^^^^

**Directives:** ``immutable()``, ``max_age(seconds)``,
``max_stale(seconds)``, ``min_fresh(seconds)``, ``must_revalidate()``,
``no_cache()``, ``no_store()``, ``no_transform()``,
``only_if_cached()``, ``private()``, ``proxy_revalidate()``,
``public()``, ``s_maxage(seconds)``, ``stale_if_error(seconds)``,
``stale_while_revalidate(seconds)``,

**Example:**

.. code:: python

   cache_value = SecurePolicies.Cache().no_store().must_revalidate().proxy_revalidate()

   # no-store, must-revalidate, proxy-revalidate

Seconds
^^^^^^^

**Values:** ``five_minutes`` = “300”, ``one_week`` = “604800”,
``one_month`` = “2592000”, ``one_year`` = “31536000”, ``two_years`` =
“63072000”

Usage
^^^^^^

.. _example-1:

**Example:**

.. code:: python

   from sanic import Sanic
   from secure import SecureHeaders, SecurePolicies

   csp_value = (
       SecurePolicies.CSP()
       .default_src(SecurePolicies.CSP().Values.none)
       .base_uri(SecurePolicies.CSP().Values.self_)
       .block_all_mixed_content()
       .connect_src(SecurePolicies.CSP().Values.self_, "api.spam.com")
       .frame_src(SecurePolicies.CSP().Values.none)
       .img_src(SecurePolicies.CSP().Values.self_, "static.spam.com")
   )

   hsts_value = (
       SecurePolicies.HSTS()
       .include_subdomains()
       .preload()
       .max_age(SecurePolicies.Seconds.one_month)
   )

   xxp_value = SecurePolicies.XXP().enabled_block()

   xfo_value = SecurePolicies.XFO().deny()

   referrer_value = SecurePolicies.Referrer().no_referrer()

   feature_value = (
       SecurePolicies.Feature()
       .geolocation(SecurePolicies.Feature.Values.self_, "spam.com")
       .vibrate(SecurePolicies.Feature.Values.none)
   )

   cache_value = SecurePolicies.Cache().no_store().must_revalidate().proxy_revalidate()

   secure_headers = SecureHeaders(
       csp=csp_value,
       hsts=hsts_value,
       xfo=xfo_value,
       xxp=xxp_value,
       referrer=referrer_value,
       feature=feature_value,
       cache=cache_value,
   )
   secure_cookie = SecureCookie()

   app = Sanic()

   . . . 

   @app.middleware("response")
   async def set_secure_headers(request, response):
       secure_headers.sanic(response)

   . . . 

Response Headers:

.. code:: http

   Strict-Transport-Security: includeSubDomains; preload; max-age=2592000
   X-Frame-Options: deny
   X-XSS-Protection: 1; mode=block
   X-Content-Type-Options: nosniff
   Content-Security-Policy: default-src 'none'; base-uri 'self'; block-all-mixed-content; connect-src 'self' api.spam.com; frame-src 'none'; img-src 'self' static.spam.com
   Referrer-Policy: no-referrer
   Cache-control: no-store, must-revalidate, proxy-revalidate
   Feature-Policy: geolocation 'self' spam.com; vibrate 'none'
