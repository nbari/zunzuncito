log_json
========

The ``log_json`` is a function that given a `dictionary <http://docs.python.org/2/tutorial/datastructures.html#dictionaries>`_, returns a
`json <http://json.org/example>`_ structure.

The idea is that later the logs can be parsed and processed by external tools.

The arguments are::

    log_json(log, indent=False)

 :log: a python dictionary
 :indent: return the json structured indent more human readable


Example
.......

.. code-block:: python
   :linenos:
   :emphasize-lines: 12,13,14,15,16,17


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


.. seealso::

   `Structured Logging <http://docs.python.org/2/howto/logging-cookbook.html#implementing-structured-logging>`_
