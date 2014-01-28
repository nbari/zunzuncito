dispatch method
===============

The ``dispatch`` method belongs to the `APIResource <en/latest/resource/APIResource.html>`_
class and is called by the `ZunZun <en/latest/zunzun.html>`_ instance in
order to process the requests.


Basic template
..............


.. code-block:: python
   :linenos:
   :emphasize-lines: 4, 17


   import logging
   from zunzuncito import tools

   class APIResource(object):

       def __init__(self, api):
           self.api = api
           self.log = logging.getLogger()
           self.log.info(tools.log_json({
               'vroot': api.vroot,
               'API': api.version,
               'URI': api.URI,
               'method': api.method
           }, True)
           )

       def dispatch(self, environ):
           """ your code goes here """

Status codes
............

The default `HTTP status code <http://en.wikipedia.org/wiki/List_of_HTTP_status_codes>`_
is 200, but based on your needs you can change it to fit you response very eazy
by just doing something like::

    self.api.status = 201

Headers
.......

As with the status codes, same happens with the `HTTP headers <http://en.wikipedia.org/wiki/List_of_HTTP_header_fields>`_,
The default headers are::

    Content-Type: 'application/json; charset=UTF-8'
    Request-ID: <request_id>


For updating/replacing you just need to do something like::

    self.api.headers['my_custom_header'] = str(uuid.uuid4())

Example
.......

.. seealso::

   `pep 0333 <http://www.python.org/dev/peps/pep-0333/>`_
