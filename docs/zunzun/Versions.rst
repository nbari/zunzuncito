Versions
========

The ``versions`` argument must be a list of names representing the available API versions.

.. code-block:: python
   :emphasize-lines: 5
   :linenos:

   import zunzuncito

   root = 'my_api'

   versions = ['v0', 'v1']

   hosts = {'*': 'default'}

   routes = {'default':[
       ('/my/?.*', 'ip_tools', 'GET'),
       ('/(md5|sha1|sha256|sha512)(/.*)?', 'hasher', 'GET, POST'),
       ('/.*', 'default')
   ]}

   app = zunzuncito.ZunZun(root, versions, hosts, routes)


Request example
---------------

When no version is specified on the URI request, the default version is the first element off the list, example::


    curl -i http://api.zunzun.io/my/ip

Or::

    curl -i http://api.zunzun.io/v0/my/ip


The output could be something like:

.. code-block:: rest
   :linenos:
   :emphasize-lines: 12

   HTTP/1.1 200 OK
   Request-ID: 52ad9da400ff0dda875ef62f7d0001737e7a756e7a756e6369746f2d617069000131000100
   Content-Type: application/json; charset=UTF-8
   Vary: Accept-Encoding
   Date: Sun, 15 Dec 2013 12:16:37 GMT
   Server: Google Frontend
   Cache-Control: private
   Alternate-Protocol: 80:quic,80:quic
   Transfer-Encoding: chunked

   {
       "ip": "89.181.199.57"
   }


Now if we change the version, notice the ``v1``::

    curl -i http://api.zunzun.io/v1/my/ip


The output could be something like:

.. code-block:: rest
   :linenos:
   :emphasize-lines: 12,13

   HTTP/1.1 200 OK
   Request-ID: 52ada62f00ff06ee2d1086b0d00001737e7a756e7a756e6369746f2d617069000131000100
   Content-Type: application/json; charset=UTF-8
   Vary: Accept-Encoding
   Date: Sun, 15 Dec 2013 12:53:03 GMT
   Server: Google Frontend
   Cache-Control: private
   Alternate-Protocol: 80:quic,80:quic
   Transfer-Encoding: chunked

   {
   "inet_ntoa": 1505085241,
   "ip": "89.181.199.57"
   }


How it works internally
-----------------------

The API directory structre looks like:

.. code-block:: rest
   :emphasize-lines: 8,13,16,21
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
            |  `--zun_ip_tools
            |    |--__init__.py
            |    `--zun_ip_tools.py
            `--v1
               |--__init__.py
               |--zun_default
               | |--__init__.py
               | `--zun_default.py
               `--zun_ip_tools
                 |--__init__.py
                 `--zun_ip_tools.py
