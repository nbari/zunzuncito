_catchall resource
==================

**ZunZun** proccess request only for does who have an existing module, for
example using the following directory structure notice we only have 2 modules,
``default`` and ``hassher``

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
                 `--zun_hasher
                    |--__init__.py
                    `--zun_hasher.py
