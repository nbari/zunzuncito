Rid
===

The ``rid`` argument, contains the name of the environ variable  containing the request id if any, for example when using GAE::

   app = zunzuncito.ZunZun(root, versions, hosts, routes, rid='REQUEST_LOG_ID')


This helps to add a Request-ID header to all your responses, example when you
make a request like::

    curl -i http://api.zunzun.io/md5/python

The response is something like:

.. code-block:: rest
   :emphasize-lines: 2
   :linenos:

   HTTP/1.1 200 OK
   Request-ID: 52b041e500ff018603acd9c1c60001737e7a756e7a756e6369746f2d617069000131000100
   Content-Type: application/json; charset=UTF-8
   Vary: Accept-Encoding
   Date: Tue, 17 Dec 2013 12:21:57 GMT
   Server: Google Frontend
   Cache-Control: private
   Alternate-Protocol: 80:quic,80:quic
   Transfer-Encoding: chunked

   {
   "hash": "23eeeb4347bdd26bfc6b7ee9a3b755dd",
   "string": "python",
   "type": "md5"
   }

This can help to track the request in both server/client side.
