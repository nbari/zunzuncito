dispatch method
===============

The ``dispatch`` method belongs to the `APIResource <en/latest/resource/APIResource.html>`_
class and is called by the `ZunZun <en/latest/zunzun.html>`_ instance in
order to process the requests.


Basic template
--------------


.. code-block:: python
   :linenos:
   :emphasize-lines: 5, 20


   import logging
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
           """ your code goes here """
