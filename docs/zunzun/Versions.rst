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



When no version is specified on the URI request, the default version is the first element off the list, example::


    curl -i http://api.zunzun.io/my/ip

or::

    curl -i http://api.zunzun.io/v0/my/ip


The output could be something like:

.. code-block:: rest
   :linenos:

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
