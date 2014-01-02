tools
=====

`tools <https://github.com/nbari/zunzuncito/blob/master/zunzuncito/tools.py>`_ are
a set of classes and functions that help to proccess the reply of the request more easy.

.. code-block:: python
   :linenos:
   :emphasize-lines: 2


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

.. toctree::
   :maxdepth: 2

   tools/HTTPError
   tools/HTTPException
   tools/MethodException
   tools/allow_methods
   tools/log_json
   tools/clean_dict
   tools/CaseInsensitiveDict
