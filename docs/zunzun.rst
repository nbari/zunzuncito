ZunZun class
============

An example
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

   app = zunzuncito.ZunZun(root, versions, hosts, routes, debug=True)


.. toctree::
   :maxdepth: 2

   zunzun/Root
   zunzun/Versions
   zunzun/Hosts
   zunzun/Routes
   zunzun/Prefix
   zunzun/Rid
   zunzun/Debug
