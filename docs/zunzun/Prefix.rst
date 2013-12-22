Prefix
======


The ``prefix`` argument is the string that should be appended to all the names
of the python modules.

.. code-block:: python
   :emphasize-lines: 14
   :linenos:

   import zunzuncito

   root = 'my_api'

   versions = ['v0', 'v1']

   hosts = {'*': 'default'}

   routes = {'default':[
       ('/(md5|sha1|sha256|sha512)(/.*)?', 'hasher', 'GET, POST'),
       ('/.*', 'default')
   ]}

   app = zunzuncito.ZunZun(root, versions, hosts, routes, prefix='zzz_')

* The default prefix is ``zun_``


Directory structure
-------------------

The directory containing the sources for the application would look like:

.. code-block:: rest
   :emphasize-lines: 10,12,13,15,18,20,21,23
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
             |  |--zzz_default
             |  |  |--__init__.py
             |  |  `--zzz_default.py
             |  `--zzz_hasher
             |    |--__init__.py
             |    `--zzz_hasher.py
             `--v1
                |--__init__.py
                |--zzz_default
                | |--__init__.py
                | `--zzz_default.py
                `--zzz_hasher
                  |--__init__.py
                  `--zzz_hasher.py

* In this case the **my_api** directory, is the ``root`` and all modules (API
  Resources) start with 'zzz_'


.. note::
    The idea of the **prefix** is to avoid conflics with current python modules

.. seealso::
    `pep 395 <http://www.python.org/dev/peps/pep-0395/>`_, `python import <http://docs.python.org/3/reference/import.html>`_
