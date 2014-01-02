HTTPException
=============

The ``HTTPException`` class extends the `HTTPError <https://github.com/nbari/zunzuncito/blob/master/zunzuncito/tools.py#L13>`_
class, the main idea of it, is to handle posible erros and to properly reply with the corresponding
`HTTP status code  <en/latest/http_status_codes.html>`_


Example
.......

.. code-block:: python
   :linenos:
   :emphasize-lines: 13


   import logging
   import os
   from zunzuncito import tools
   from zunzuncito import http_status_codes


   class APIResource(object):

       def __init__(self, api):
           self.api = api
           self.status = 200
           self.headers = api.headers.copy()
           self.log = logging.getLogger()
           self.log.info(tools.log_json({
               'vroot': api.vroot,
               'API': api.version,
               'URI': api.URI,
               'method': api.method
           }, True)
           )

       def dispatch(self, environ, start_response):
           try:
               name = self.api.path[0]
           except:
               raise tools.HTTPException(400)
