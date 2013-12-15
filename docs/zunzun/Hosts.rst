Hosts
=====


A very basic API, contents of file **app.py** can be:

.. code-block:: python
   :emphasize-lines: 7
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


To support `multi-tenancy <http://en.wikipedia.org/wiki/Multitenancy>`_ the
**hosts** dictionary is needed.

A `dictionary structure
<http://docs.python.org/2/tutorial/datastructures.html#dictionaries>`_ is formed by **key: value** elements, in this case the key is used for specifying the 'host' and the value to specify the **vroot**

The wildcard character ***** can be used, for example:

.. code-block:: rest
   :linenos:

   hosts = {
       '*': 'default',
       '*.zunzun.io': 'default',
       'ejemplo.org': 'ejemplo_org',
       'api.ejemplo.org': 'api_ejemplo_org'
   }

In this case
