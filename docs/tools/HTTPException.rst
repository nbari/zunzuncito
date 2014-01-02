HTTPException
=============

The ``HTTPException`` class extends the `HTTPError <https://github.com/nbari/zunzuncito/blob/master/zunzuncito/tools.py#L13>`_
class, the main idea of it, is to handle posible erros and properly reply with the corresponding
`HTTP status code  <en/latest/http_status_codes.html>`_


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

    curl -i -X POST http://localhost:8080/delete/

Will reply with this::

    HTTP/1.1 400 Bad Request
    Request-ID: ea6b28ac-a733-482d-a398-16c620ba2b4e
    Content-Type: application/json; charset=UTF-8

This is because the request URI is missing the `path <en/latest/resource/path.html>`_ and should be something
like::

    curl -i -X POST http://localhost:8080/delete/foo

.. note ::

   If you only pass the integer `HTTP status code <en/latest/http_status_codes.html>`_ to the HTTPExecption, only the response
headers will be sent.


Body response
.............

Besides only replying with the headers you may want to give a more informative
/ verbose message, the HTTPExeption accept the following arguments:

.. code-block:: python

   HTTPException(status, title=None, description=None, headers=None, code=None, display=False)
