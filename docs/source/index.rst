.. secure.py documentation master file, created by
   sphinx-quickstart on Wed Dec 19 05:31:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

secure.py
==========

|version| |Python 3| |license| |black|

secure.py 🔒 is a lightweight package that adds optional security headers for Python web frameworks.

Supported Python web frameworks:
--------------------------------

`aiohttp <https://docs.aiohttp.org>`__,
`Bottle <https://bottlepy.org>`__, `CherryPy <https://cherrypy.org>`__,
`Django <https://www.djangoproject.com>`__,
`Falcon <https://falconframework.org>`__,
`FastAPI <https://fastapi.tiangolo.com>`__,
`Flask <http://flask.pocoo.org>`__,
`hug <http://www.hug.rest>`__,
`Masonite <https://docs.masoniteproject.com>`__,
`Pyramid <https://trypyramid.com>`__,
`Quart <https://pgjones.gitlab.io/quart/>`__,
`Responder <https://python-responder.org>`__,
`Sanic <https://sanicframework.org>`__,
`Starlette <https://www.starlette.io/>`__,
`Tornado <https://www.tornadoweb.org/>`__

Install
-------

**pip**:

.. code:: console

   $ pip install secure

**Pipenv**:

.. code:: console

   $ pipenv install secure

After installing secure.py:

.. code:: python

   from secure import SecureHeaders, SecureCookie

   secure_headers = SecureHeaders()
   secure_cookie = SecureCookie()

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   headers
   policies
   frameworks
   resources


.. |version| image:: https://img.shields.io/pypi/v/secure.svg
   :target: https://pypi.org/project/secure/
.. |Python 3| image:: https://img.shields.io/badge/python-3-blue.svg
   :target: https://www.python.org/downloads/
.. |license| image:: https://img.shields.io/pypi/l/secure.svg
   :target: https://pypi.org/project/secure/
.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
