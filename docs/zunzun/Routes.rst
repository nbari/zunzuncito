Routes
======

The ``routes`` argument must be a dictionary containing defined routes per
vroot

.. code-block:: python
   :emphasize-lines: 9,10,11,12
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


.. note::
   By default, if no **routes** specified, the request are handled by matching the URI
   request with an valid **API Resource**, you only need to specify **routes** if want to
   handle different URI requests with a single **API Resource**


Routes dictionary structure
---------------------------

The ``routes`` dictionary needs this structure:

+-------+--------------------+--------------+--------------+
| vroot | regular expression | API Resource | HTTP methods |
+=======+====================+==============+==============+
| 'default' | '/(md5|sha1|sha256|sha512)(/.*)?' | 'hasher' | 'GET, POST' |
+-----------+-----------------------------------+----------+-------------+
