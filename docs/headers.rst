Secure Headers
----------------

Security Headers are HTTP response headers that, when set, can enhance
the security of your web application by enabling browser security
policies.

You can assess the security of your HTTP response headers at
`securityheaders.com <https://securityheaders.com>`__

*Recommendations used by secure,py and more information regarding
security headers can be found at the* `OWASP Secure Headers
Project <https://www.owasp.org/index.php/OWASP_Secure_Headers_Project>`__ *.*

Server
^^^^^^^^^^^^^^

| Contain information about server software
| **Default Value:** ``NULL`` *(obfuscate server information, not
  included by default)*

Strict-Transport-Security (HSTS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Ensure application communication is sent over HTTPS
| **Default Value:** ``max-age=63072000; includeSubdomains``

X-Frame-Options (XFO)
^^^^^^^^^^^^^^^^^^^^^^

| Disable framing from different origins (clickjacking defense)
| **Default Value:** ``SAMEORIGIN``

X-XSS-Protection
^^^^^^^^^^^^^^^^^^

| Enable browser cross-site scripting filters
| **Default Value:** ``0``

X-Content-Type-Options
^^^^^^^^^^^^^^^^^^^^^^^

| Prevent MIME-sniffing
| **Default Value:** ``nosniff``

Content-Security-Policy (CSP)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Prevent cross-site injections
| **Default Value:** ``script-src 'self'; object-src 'self'`` *(not
  included by default)*\*

Referrer-Policy
^^^^^^^^^^^^^^^^

| Enable full referrer if same origin, remove path for cross origin and
  disable referrer in unsupported browsers
| **Default Value:** ``no-referrer, strict-origin-when-cross-origin``

Cache-control
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Prevent cacheable HTTPS response
| **Default Value:** ``no-cache``

Permissions-Policy
^^^^^^^^^^^^^^^

| Disable browser features and APIs
| **Default Value:** ``accelerometer=(), ambient-light-sensor=(), autoplay=(),camera=(), encrypted-media=(), fullscreen=(),geolocation=(), gyroscope=(), magnetometer=(),microphone=(); midi=(), payment=(),picture-in-picture=(), speaker=(), sync-xhr=(), usb=(),vr=()``  *(not included by default)*    


**Additional information:**
  - The ``Strict-Transport-Security`` (HSTS) header will tell the browser to **only** utilize secure HTTPS connections for the domain, and in the default configuration, including all subdomains. The HSTS header requires trusted certificates and users will unable to connect to the site if using self-signed or expired certificates.  The browser will honor the HSTS header for the time directed in the ``max-age`` attribute *(default = 2 years)*, and setting the ``max-age`` to ``0`` will disable an already set HSTS header. Use the ``hsts=False`` option to not include the HSTS header in Secure Headers.
  - The ``Content-Security-Policy`` (CSP) header can break functionality and can (and should) be carefully constructed, use the ``csp=secure.ContentSecurityPolicy()`` option to enable default values.

Usage
^^^^^^^

.. code:: python

   secure_headers = secure.Secure()
   secure_headers.framework.[framework](response)

**Default HTTP response headers:**

.. code:: http

   Strict-Transport-Security: max-age=63072000; includeSubdomains
   X-Frame-Options: SAMEORIGIN
   X-XSS-Protection: 0
   X-Content-Type-Options: nosniff
   Referrer-Policy: no-referrer, strict-origin-when-cross-origin
   Cache-control: no-cache, no-store, must-revalidate, max-age=0
   Pragma: no-cache
   Expires: 0

Options
^^^^^^^^

You can toggle the setting of headers with default and override default values by passing a class to
the following options:

-  ``server`` - set the Server header, ``secure.Secure(server=secure.Server())`` *(default=False)*
-  ``hsts`` - set the Strict-Transport-Security header ``secure.Secure(hsts=secure.StrictTransportSecurity())``  *(default=True)*
-  ``xfo`` - set the X-Frame-Options header ``secure.Secure(xfo=secure.XFrameOptions())``  *(default=True)*
-  ``xxp`` - set the X-XSS-Protection header ``secure.Secure(xxp=secure.XXSSProtection())``  *(default=True)*
-  ``content`` - set the X-Content-Type-Options header  ``secure.Secure(content=secure.XContentTypeOptions())`` *(default=True)*
-  ``csp`` - set the Content-Security-Policy  ``secure.Secure(csp=secure.ContentSecurityPolicy())`` *(default=False)* \*
-  ``referrer`` - set the Referrer-Policy header  ``secure.Secure(referrer=secure.ReferrerPolicy())``  *(default=True)*
-  ``cache`` - set the Cache-control header  ``secure.Secure(cache=secure.CacheControl())`` *(default=True)*
-  ``permissions`` - set the Permissions-Policy header  ``secure.Secure(permissions=secure.PermissionsPolicy())``  *(default=False)*

**Example:**

.. code:: python

   import secure

   csp = secure.ContentSecurityPolicy()
   xfo = secure.XFrameOptions().deny()

   secure_headers = secure.Secure(csp=csp, hsts=None, xfo=xfo)

   . . . 

   secure_headers.framework.[framework](response)

   
   **HTTP response headers:**

.. code:: http

   x-frame-options: deny
   x-xss-protection: 0
   x-content-type-options: nosniff
   content-security-policy: script-src 'self'; object-src 'self'
   referrer-policy: no-referrer, strict-origin-when-cross-origin
   cache-control: no-store
