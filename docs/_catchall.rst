_catchall resource
==================

**ZunZun** process request only for does who have an existing module, for
example using the following directory structure notice we only have 2 modules,
``zun_default``, ``zun_hassher`` and ``zun_gevent``.

.. code-block:: rest
   :emphasize-lines: 10, 13
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
   :emphasize-lines: 3,4

   routes = {'default':[
       ('/(md5|sha1|sha256|sha512)(/.*)?', 'hasher', 'GET, POST'),
       ('/.*', 'default')
   ]}

For example the ``zun_hasher`` module will handle all the request for URI containing::

  /md5, /sha1, /sha256, /sha512

But the regex::

    '/.*'

Will match anything and send it to the ``zun_default`` module, the problem
with this regex, is that since it will catch anything, if you make a request
for example to::

    api.zunzun.io/gevent

It will answerd by the ``zun_default`` since the regex catched the request.
