ZunZun class
============

**ZunZun** is the name of the `class <http://docs.python.org/2/tutorial/classes.html>`_
that will parse all the incoming request and route them to a proper `APIResource </en/latest/resource.html>`_
class to proccess the requests

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
