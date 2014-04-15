Response class
==============

All requests need a `response <http://www.python.org/dev/peps/pep-0333/#the-start-response-callable>`_,
the ``response`` class creates an object for every request, the one can be used to send
`custom headers <http://en.wikipedia.org/wiki/List_of_HTTP_header_fields>`_ or
`HTTP status codes </en/latest/http_status_codes.html>`_.

The second argument for the dispatch method is the response object:

.. code-block:: python
   :linenos:
   :emphasize-lines: 6

   from zunzuncito import tools

   class APIResource(object):


       def dispatch(self, request, response):
           """ your code goes here """

Response object contents
.......................

============== ========================================================================================================
Name           Description
============== ========================================================================================================
log            `logger <http://docs.python.org/2/library/logging.html>`_ intance.
request_id     The `request id </en/latest/zunzun/Rid.html>`_.
headers        A `CaseInsensitiveDict </en/latest/tools/CaseInsensitiveDict.html>`_ instance, for storing the headers.
status         Default **200** an int respresenting an `HTTP status code </en/latest/http_status_codes.html>`_.
start_response `The start_response() Callable <http://www.python.org/dev/peps/pep-0333/#the-start-response-callable>`_.
extra          A list for repeated headers used with the ``add_header`` method
============== ========================================================================================================

add_header
..........

If you need to create multiple headers using the same key for example to set up
cookies you should use the ``add_header`` method.

Example
.......

.. code-block:: python
   :linenos:
   :emphasize-lines: 11, 21

   from zunzuncito import tools


   class APIResource(object):

       def __init__(self):
           self.headers['Content-Type'] = 'text/html; charset=UTF-8'

       def dispatch(self, request, response):

           response.headers.update(self.headers)

           try:
               name = request.path[0]
           except Exception:
               name = ''

          if name:
                return 'Name: ' + name

           response.status =  406
