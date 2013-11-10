Quick Start
===========

This is the directory structure::

   :emphasize-lines: 3,4

   /home/
     `--zunzun/
        |--app.py
        `--my_api
          |--__init__.py
          |--v0
          |  |--__init__.py
          |  `--zun_default
          |     |--__init__.py
          |     `--zun_default.py
          `--v1
             |--__init__.py
             `--zun_default
               |--__init__.py
               `--zun_default.py

Inside directory /home/zunzun there is a file called **app.py** and a directory **my_api**.

For a very basic API, contents of file **app.py** can be:

.. code-block:: python

   import zunzuncito

   root = 'my_api'

   versions = ['v0', 'v1']

   routes = [
      ('/my', 'ip_tools', 'GET'),
   ]

   app = zunzuncito.ZunZun(root, versions, routes)
