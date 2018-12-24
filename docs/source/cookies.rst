Secure Cookies
-----------------

Path
^^^^^^^

The Path directive instructs the browser to only send the cookie if
provided path exists in the URL.

.. _secure-1:

Secure
^^^^^^^

The Secure flag instructs the browser to only send the cookie via HTTPS.

HttpOnly
^^^^^^^^^

The HttpOnly flag instructs the browser to not allow any client side
code to access the cookie’s contents.

SameSite
^^^^^^^^^

The SameSite flag directs the browser not to include cookies on certain
cross-site requests. There are two values that can be set for the
same-site attribute, lax or strict. The lax value allows the cookie to
be sent via certain cross-site GET requests, but disallows the cookie on
all POST requests. For example cookies are still sent on links
``<a href=“x”>``, prerendering ``<link rel=“prerender” href=“x”`` and
forms sent by GET requests ``<form-method=“get”...``, but cookies will
not be sent via POST requests ``<form-method=“post”...``, images
``<img src=“x”>`` or iframes ``<iframe src=“x”>``. The strict value
prevents the cookie from being sent cross-site in any context. Strict
offers greater security but may impede functionality. This approach
makes authenticated CSRF attacks impossible with the strict flag and
only possible via state changing GET requests with the lax flag.

Expires
^^^^^^^^^

The Expires attribute sets an expiration date for persistent cookies.

.. _example-2:

Usage
^^^^^^^

.. code:: python

   secure_cookie.framework(response, name="spam", value="eggs")

*Default Set-Cookie HTTP response header:*

.. code:: http

   Set-Cookie: spam=eggs; Path=/; secure; HttpOnly; SameSite=lax

.. _options-1:

Options
^^^^^^^^^

You can modify default cookie attribute values by passing the following
options:

-  ``name`` - set the cookie name *(string, No default value)*
-  ``value`` - set the cookie value *(string, No default value)*
-  ``path`` - set the Path attribute, e.g. ``path=“/secure”`` *(string,
   default=“/”)*
-  ``secure`` - set the Secure flag *(bool, default=True)*
-  ``httponly`` - set the HttpOnly flag *(bool, default=True)*
-  ``samesite`` - set the SameSite attribute,
   e.g. ``SecureCookie.SameSite.LAX`` *(bool / enum, options:*
   ``SecureCookie.SameSite.STRICT``, ``SecureCookie.SameSite.LAX`` *or*
   ``False``, *default=SecureCookie.SameSite.LAX)*
-  ``expires`` - set the Expires attribute with the cookie expiration in
   hours, e.g. ``expires=1`` *(number / bool, default=False)*

*You can also import the SameSite options enum from Secure,*
``from secure import SecureCookie, SameSite``

.. _example-3:

**Example:**

.. code:: python

   from secure import SecureCookie
   secure_cookie = SecureCookie(expires=1, samesite=SecureCookie.SameSite.STRICT)

   secure_cookie.framework(response, name="spam", value="eggs")
