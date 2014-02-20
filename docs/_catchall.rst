_catchall resource
==================

**ZunZun** process request only for does who have an existing module, for
example using the following directory structure notice we only have 2 modules,
``zun_default``, ``zun_hassher`` and ``zun_gevent``.

.. code-block:: rest
   :emphasize-lines: 10, 13, 16
   :linenos:

   /home/
     `--zunzun/
        |--app.py
        `--my_api
           |--__init__.py
           `--default
              |--__init__.py
              `--v0
                 |--__init__.py
                 |--zun_default
                 |  |--__init__.py
                 |  `--zun_default.py
                 |--zun_hasher
                 |  |--__init__.py
                 |  `--zun_hasher.py
                 `--zun_gevent
                    |--__init__.py
                    `--zun_gevent.py

The `routes </en/latest/zunzun/Routes.html>`_ uses regular expresions to match
more then one request into one module, for example:

.. code-block:: python
   :linenos:
   :emphasize-lines: 2,3

   routes = {'default':[
       ('/(md5|sha1|sha256|sha512)(/.*)?', 'hasher', 'GET, POST'),
       ('/.*', 'notfound')
   ]}

For example the ``zun_hasher`` module will handle all the request for URI containing::

  /md5, /sha1, /sha256, /sha512

But the regex::

    '/.*'

Will match anything and send it to the ``zun_notfound`` module, the problem
with this regex, is that since it will catch anything, if you make a request
for example to::

    api.zunzun.io/gevent

It will be processed by the ``zun_notfound`` since the regex catched the
request.

A solution to this, could be to add a route for the gevent request, something like
this:

.. code-block:: python
   :linenos:
   :emphasize-lines: 3

   routes = {'default':[
       ('/(md5|sha1|sha256|sha512)(/.*)?', 'hasher', 'GET, POST'),
       ('/gevent/?.*', 'gevent'),
       ('/.*', 'notfound')
   ]}

That could solve the problem, but forces you to have a route for every module,
the more modules you have, the more complicated and dificult becomes to
maintain the routes dictionary.

So, be available to have regular expresions mathing many to one module, to
continue serving directly from modules that don't need a regex, and to also have
a catchall that does not need require a regex and it is olny called when all
the routes and modules options have been exhauste, the **_catchall** module was
created.

How it works
............

The only thing required, is to create a module with the name ``__catchall``, if
using the default prefix, it would be ``zun__catchall``.

* Notice the double ``__catchall`` underscore.

.. seealso::

    The `zun prefix </en/latest/zunzun/Prefix.html>`

Directory structure
...................

.. code-block:: rest
   :emphasize-lines: 19
   :linenos:

   /home/
     `--zunzun/
        |--app.py
        `--my_api
           |--__init__.py
           `--default
              |--__init__.py
              `--v0
                 |--__init__.py
                 |--zun_default
                 |  |--__init__.py
                 |  `--zun_default.py
                 |--zun_hasher
                 |  |--__init__.py
                 |  `--zun_hasher.py
                 |--zun_gevent
                 |  |--__init__.py
                 |  `--zun_gevent.py
                 `--zun__catchall
                    |--__init__.py
                    `--zun__catchall.py


When processing a request, if not module is found either in the routes or in
the directory structure, if the If the ``__catchall`` module is found, it is
goint to be used for handling the request, if not it will just return an HTTP
501 Not Implementd status.


Example
.......

The following example, will handle all *not found* modules for the incoming
request, and redirect to '/'.

.. code-block:: python
   :linenos:
   :emphasize-lines: 21

   """
   catchall resource
   """

   from zunzuncito import tools


   class APIResource(object):

       def __init__(self):
           self.headers = {'Content-Type': 'text/html; charset=UTF-8'}

       def dispatch(self, request, response):
           request.log.debug(tools.log_json({
               'API': request.version,
               'URI': request.URI,
               'rid': request.request_id,
               'vroot': request.vroot
           }, True))

           response.headers.update(self.headers)

           raise tools.HTTPException(302, headers={'Location': '/'}, log=False)
