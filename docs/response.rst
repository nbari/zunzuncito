Response class
==============

All requests need a `response <http://www.python.org/dev/peps/pep-0333/#the-start-response-callable>`_,
the ``response`` class creates an object for every request, the one can be used to send
`custom headers <http://en.wikipedia.org/wiki/List_of_HTTP_header_fields>`_ or
`HTTP status codes </en/latest/http_status_codes.html>`_.

Example
.......

.. code-block:: python
   :linenos:
   :emphasize-lines: 6

   from zunzuncito import tools

   class APIResource(object):


       def dispatch(self, request, response):
           """ your code goes here """

Response object contents
.......................

============== =======================================================================================================
Name           Description
============== =======================================================================================================
log            `logger <http://docs.python.org/2/library/logging.html>`_ intance
request_id     The `request id </en/latest/zunzun/Rid.html>`_
headers        A `CaseInsensitiveDict </en/latest/tools/CaseInsensitiveDict.html> instance.
status         200 an int respresenting an `HTTP status code </en/latest/http_status_codes.html>`_
start_response `The start_response() Callable <http://www.python.org/dev/peps/pep-0333/#the-start-response-callable>`_
============== =======================================================================================================
