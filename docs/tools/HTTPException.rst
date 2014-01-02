HTTPException
=============

The ``HTTPException`` class extends the `HTTPError <https://github.com/nbari/zunzuncito/blob/master/zunzuncito/tools.py#L13>`_
class, the main idea of it, is to handle posible erros and properly reply with the corresponding
`HTTP status code  </en/latest/http_status_codes.html>`_


Example
.......

.. code-block:: python
   :linenos:
   :emphasize-lines: 17


   import os
   from zunzuncito import tools
   from zunzuncito import http_status_codes


   class APIResource(object):

       def __init__(self, api):
           self.api = api
           self.status = 200
           self.headers = api.headers.copy()

       def dispatch(self, environ, start_response):
           try:
               name = self.api.path[0]
           except:
               raise tools.HTTPException(400)

the line::

    raise tools.HTTPException(400)

For a request like::

    curl -i http://api.zunzun.io/exception

Will reply with this::

    HTTP/1.1 400 Bad Request
    Request-ID:
    52c597a700ff0229fef9f477280001737e7a756e7a756e6369746f2d617069000131000100
    Content-Type: application/json; charset=UTF-8
    Date: Thu, 02 Jan 2014 16:45:27 GMT
    Server: Google Frontend
    Content-Length: 0
    Alternate-Protocol: 80:quic,80:quic

This is because the request URI is missing the `path </en/latest/resource/path.html>`_ and should be something
like::

    curl -i http://api.zunzun.io/exception/foo

    HTTP/1.1 200 OK
    Request-ID:
    52c597d200ff0d89f81dcec4280001737e7a756e7a756e6369746f2d617069000131000100
    Content-Type: application/json; charset=UTF-8
    Vary: Accept-Encoding
    Date: Thu, 02 Jan 2014 16:46:11 GMT
    Server: Google Frontend
    Cache-Control: private
    Alternate-Protocol: 80:quic,80:quic
    Transfer-Encoding: chunked

    my_api.default.v0.zun_exception.zun_exception

.. note ::

   If you only pass the integer `HTTP status code </en/latest/http_status_codes.html>`_ to the HTTPExecption, only the response
   headers will be sent.


Body response
.............

Besides only replying with the headers you may want to give a more informative
/ verbose message, the HTTPExeption accept the following arguments:

.. code-block:: python

   HTTPException(status, title=None, description=None, headers=None, code=None, display=False)
