Policy Builder
----------------

ContentSecurityPolicy()
^^^^^^^

**Directives:** ``base_uri(sources)``,
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

**Example:**

.. code:: python

   csp_policy = (
   secure.ContentSecurityPolicy()
   .default_src("'none'")
   .base_uri("'self'")
   .connect_src("'self'", "api.spam.com")
   .frame_src("'none'")
   .img_src("'self'", "static.spam.com")
   )

   secure_headers = secure.Secure(csp=csp_policy)

   # default-src 'none'; base-uri 'self'; connect-src 'self' api.spam.com; frame-src 'none'; img-src 'self' static.spam.com

*You can check the effectiveness of your CSP Policy at the* `CSP
Evaluator <https://csp-evaluator.withgoogle.com>`__

StrictTransportSecurity()
^^^^^^^

**Directives:** ``include_subDomains()``, ``max_age(seconds)``,
``preload()``

**Example:**

.. code:: python

   hsts_value = (
   secure.StrictTransportSecurity()
   .include_subdomains()
   .preload()
   .max_age(2592000)
   )

   secure_headers = secure.Secure(hsts=hsts_value)

   # includeSubDomains; preload; max-age=2592000

XFrameOptions()
^^^^^^

**Directives:** ``allow_from(uri)``, ``deny()``, ``sameorigin()``

**Example:**

.. code:: python

   xfo_value = secure.XFrameOptions().deny()

   secure_headers = secure.Secure(xfo=xfo_value)

   # deny

ReferrerPolicy()
^^^^^^^^^^^

**Directives:** ``no_referrer()``, ``no_referrer_when_downgrade()``,
``origin()``, ``origin_when_cross_origin()``, ``same_origin()``,
``strict_origin()``, ``strict_origin_when_cross_origin()``,
``unsafe_url()``

**Example:**

.. code:: python

   referrer = secure.ReferrerPolicy().strict_origin()

   secure_headers = secure.Secure(referrer=referrer).headers()
  
   # strict-origin

PermissionsPolicy()
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

**Example:**

.. code:: python

   permissions = (
   secure.PermissionsPolicy().geolocation("self", '"spam.com"').vibrate()
   )

   secure_headers = secure.Secure(permissions=permissions).headers()

   # geolocation=(self "spam.com"), vibrate=()

CacheControl()
^^^^^^^^

**Directives:** ``immutable()``, ``max_age(seconds)``,
``max_stale(seconds)``, ``min_fresh(seconds)``, ``must_revalidate()``,
``no_cache()``, ``no_store()``, ``no_transform()``,
``only_if_cached()``, ``private()``, ``proxy_revalidate()``,
``public()``, ``s_maxage(seconds)``, ``stale_if_error(seconds)``,
``stale_while_revalidate(seconds)``,

**Example:**

.. code:: python

   cache = secure.CacheControl().no_cache()

   secure_headers = secure.Secure(cache=cache).headers()

   # no-store


Usage
^^^^^^

.. _example-1:

**Example:**

.. code:: python

   import uvicorn
   from fastapi import FastAPI
   import secure
   
   app = FastAPI()
   
   server = secure.Server().set("Secure")
   
   csp = (
       secure.ContentSecurityPolicy()
       .default_src("'none'")
       .base_uri("'self'")
       .connect_src("'self'" "api.spam.com")
       .frame_src("'none'")
       .img_src("'self'", "static.spam.com")
   )
   
   hsts = secure.StrictTransportSecurity().include_subdomains().preload().max_age(2592000)
   
   referrer = secure.ReferrerPolicy().no_referrer()
   
   permissions_value = (
       secure.PermissionsPolicy().geolocation("self", "'spam.com'").vibrate()
   )
   
   cache_value = secure.CacheControl().must_revalidate()
   
   secure_headers = secure.Secure(
       server=server,
       csp=csp,
       hsts=hsts,
       referrer=referrer,
       permissions=permissions_value,
       cache=cache_value,
   )
   
   
   @app.middleware("http")
   async def set_secure_headers(request, call_next):
       response = await call_next(request)
       secure_headers.framework.fastapi(response)
       return response
   
   
   @app.get("/")
   async def root():
       return {"message": "Secure"}
   
   
   if __name__ == "__main__":
       uvicorn.run(app, port=8081, host="localhost")
   
   . . . 

Response Headers:

.. code:: http

   server: Secure
   strict-transport-security: includeSubDomains; preload; max-age=2592000
   x-frame-options: SAMEORIGIN
   x-xss-protection: 0
   x-content-type-options: nosniff
   content-security-policy: default-src 'none'; base-uri 'self'; connect-src 'self'api.spam.com; frame-src 'none'; img-src 'self' static.spam.com
   referrer-policy: no-referrer
   cache-control: must-revalidate
   permissions-policy: geolocation=(self 'spam.com'), vibrate=()
