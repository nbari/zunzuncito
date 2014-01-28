HTTPException
=============

The ``HTTPException`` class extends the `HTTPError <https://github.com/nbari/zunzuncito/blob/master/zunzuncito/tools.py#L13>`_
class, the main idea of it, is to handle posible erros and properly reply with the corresponding
`HTTP status code  </en/latest/http_status_codes.html>`_


Example
.......

.. code-block:: python
   :linenos:
   :emphasize-lines: 13


   from zunzuncito import tools


   class APIResource(object):

       def __init__(self, api):
           self.api = api

       def dispatch(self, environ):
           try:
               name = self.api.path[0]
           except:
               raise tools.HTTPException(400)

the line::

    raise tools.HTTPException(400)

For a request like::

    curl -i http://api.zunzun.io/exception

Will reply with this:

.. code-block:: rest
   :linenos:
   :emphasize-lines: 1

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

That will return something like:

.. code-block:: rest
   :linenos:
   :emphasize-lines: 1

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


For example the following snippet of code taken from `zun_exception.py <https://github.com/nbari/zunzuncito/blob/master/my_api/default/v0/zun_exception/zun_exception.py>`_:

.. code-block:: rest
   :linenos:
   :emphasize-lines: 3

    if name != 'foo':
        raise tools.HTTPException(
            406,
            title='exeption example',
            description='name must be foo',
            code='my-custom-code',
            display=True)


When the request is::

    curl -i http://api.zunzun.io/v0/exception/naranjas


Notice that the `path </en/latest/resource/path.html>`_ in this case is::

    path = ['naranjas']


Will reply with something like:

.. code-block:: rest
   :linenos:
   :emphasize-lines: 1

    HTTP/1.1 406 Not Acceptable
    Request-ID: 52c59bdf00ff0b7042cbfd5d120001737e7a756e7a756e6369746f2d617069000131000100
    Content-Type: application/json; charset=UTF-8
    Vary: Accept-Encoding
    Date: Thu, 02 Jan 2014 17:03:27 GMT
    Server: Google Frontend
    Cache-Control: private
    Alternate-Protocol: 80:quic,80:quic
    Transfer-Encoding: chunked

    {
        "code": "my-custom-code",
        "description": "name must be foo",
        "status": "406",
        "title": "exeption example"
    }
