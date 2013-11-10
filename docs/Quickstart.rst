Quick Start
===========

Create a file app.py with this:

.. code-block:: python

   import zunzuncito

   root = 'my_api'

   versions = ['v0', 'v1']

   routes = [
      ('/my', 'ip_tools', 'GET'),
   ]

   app = zunzuncito.ZunZun(root, versions, routes)

Create a directory named 'my_api' with the following structure:

::
   --app.py
   --my_api
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
