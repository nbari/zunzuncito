Prefix
======


The ``prefix`` argument is the string that should be appended to all the names
of the python modules.

.. code-block:: python
   :emphasize-lines: 3
   :linenos:

   import zunzuncito

   root = 'my_api'

   versions = ['v0', 'v1']

   hosts = {'*': 'default'}

   routes = {'default':[
       ('/(md5|sha1|sha256|sha512)(/.*)?', 'hasher', 'GET, POST'),
       ('/.*', 'default')
   ]}

   app = zunzuncito.ZunZun(root, versions, hosts, routes, prefix='zzz')


The directory structure for the application would look like:

.. code-block:: rest
   :emphasize-lines: 4
   :linenos:

   /home/
     `--zunzun/
        |--app.py
        `--my_api
          |--__init__.py
          `--default
            |--__init__.py
            |--v0
            |  |--__init__.py
            |  |--zun_default
            |  |  |--__init__.py
            |  |  `--zun_default.py
            |  `--zun_hasher
            |    |--__init__.py
            |    `--zun_hasher.py
            `--v1
               |--__init__.py
               |--zun_default
               | |--__init__.py
               | `--zun_default.py
               `--zun_hasher
                 |--__init__.py
                 `--zun_hasher.py

* In this case the **my_api** directory, is the ``root``
