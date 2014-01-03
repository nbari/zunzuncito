MethodException
===============

While defining `routes </en/latest/zunzun/Routes.html>`_ or using the
`allow_methods </en/latest/resource/allow_methods.html>`_ decorator you
can specify the allowed `HTTP methods
<http://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods>`_ to
support, the `ZunZun </en/latest/zunzun.html>`_ instance, internally will verify
for the corret method, otherwise will raise an ``MethodException``

The ``MethodException`` behaves similar to the
`HTTPException </en/latest/tools/HTTPException.html>`_ the only difference is
that by default sets the status code to `405 <https://github.com/nbari/zunzuncito/blob/master/zunzuncito/http_status_codes.py#L40>`_

.. code-block:: python

   MethodException(status=405, title=None, description=None, headers=None, code=None, display=False)


For example the zun_exception.py custom module only accepts 'GET' methods
therefor if you try the following::

    curl -i -X HEAD http://api.zunzun.io/exception/foo

The answer will be simillar to:

.. code-block:: rest
   :linenos:
   :emphasize-lines: 1

   HTTP/1.1 405 Method Not Allowed
   Request-ID: 52c6ac4e00ff060346c67c66450001737e7a756e7a756e6369746f2d617069000131000100
   Content-Type: application/json; charset=UTF-8
   Date: Fri, 03 Jan 2014 12:25:50 GMT
   Server: Google Frontend
   Content-Length: 0
   Alternate-Protocol: 80:quic,80:quic
