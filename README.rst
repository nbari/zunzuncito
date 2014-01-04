Design Goals
============

* Keep it simple and small, avoiding extra complexity at all cost. `KISS <http://en.wikipedia.org/wiki/KISS_principle>`_
* Create routes on the fly or by defining regular expressions.
* Support API versions out of the box without altering routes.
* Via decorator or in a defined route, accepts only certain `HTTP methods <http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html>`_.
* Follow the single responsibility `principle <http://en.wikipedia.org/wiki/Single_responsibility_principle>`_.
* Be compatible with any WSGI server. Example: `uWSGI <http://uwsgi-docs.readthedocs.org/en/latest/>`_, `Gunicorn <http://gunicorn.org/>`_, `Twisted <http://twistedmatrix.com/>`_, etc.
* Tracing Request-ID "rid" per request.
* Compatibility with Google App Engine. `demo <http://api.zunzun.io>`_
* `Multi-tenant <http://en.wikipedia.org/wiki/Multitenancy>`_ Support.
* Ability to create almost anything easy, example: Support `chunked transfer encoding <http://en.wikipedia.org/wiki/Chunked_transfer_encoding>`_

Install
.......

Via pip::

  $ pip install zunzuncito

If you don't have pip, after downloading the sources, you can run::

  $ python setup.py install


Quick start
...........

* `http://docs.zunzun.io/en/latest/Quickstart.html <http://docs.zunzun.io/en/latest/Quickstart.html>`_


Documentation
..............

* `docs.zunzun.io <http://docs.zunzun.io>`_

* `www.zunzun.io <http://www.zunzun.io>`_


What & Why ZunZuncito
......................

ZunZuncito is a python package that allows to create and maintain `REST <http://en.wikipedia.org/wiki/REST>`_ API's without hassle.

The simplicity for sketching and debugging helps to develop very fast; versioning is inherit by default, which allows to serve and maintain existing applications, while working in new releases with no need to create separate instances. All the applications are WSGI `PEP 333 <http://www.python.org/dev/peps/pep-0333/>`_ compliant, allowing to migrate existing code to more robust frameworks, without need to modify the existing code.

Why ?
.....

* The need to upload large files by chunks and support resumable uploads trying to accomplish something like the `nginx upload module <http://www.grid.net.ru/nginx/resumable_uploads.en.html>`_ does in pure python.


The idea of creating ZunZuncito, was the need of a very small and light tool (batteries included), that could help to create and deploy REST API's quickly, without forcing the developers to learn or follow a complex flow but, in contrast, from the very beginning, guide them to properly structure their API, giving special attention to "versioned URI's", having with this a solid base that allows to work in different versions within a single ZunZun instance without interrupting service of any existing API `resources <http://en.wikipedia.org/wiki/Web_resource>`_.
