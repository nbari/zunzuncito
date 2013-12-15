Root
====


The ``root`` argument is the name of the directory containing all your
sources::

    app = zunzuncito.ZunZun(root, versions, hosts, routes)


You can see the 'root' as the DocumentRoot of the application

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
