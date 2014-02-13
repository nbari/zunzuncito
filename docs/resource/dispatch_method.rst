dispatch method
===============

The ``dispatch`` method belongs to the `APIResource <en/latest/resource/APIResource.html>`_
class and is called by the `ZunZun <en/latest/zunzun.html>`_ instance in
order to process the requests.


Basic template
..............


.. code-block:: python
   :linenos:


   from zunzuncito import tools

   class APIResource(object):


       def dispatch(self, request, response):
           """ your code goes here """

Status codes
............

The default `HTTP status code <http://en.wikipedia.org/wiki/List_of_HTTP_status_codes>`_
is 200, but based on your needs you can change it to fit you response very eazy
by just doing something like::

    response.status = 201

Headers
.......

As with the status codes, same happens with the `HTTP headers <http://en.wikipedia.org/wiki/List_of_HTTP_header_fields>`_,
The default headers are::

    Content-Type: 'application/json; charset=UTF-8'
    Request-ID: <request_id>


For updating/replacing you just need to do something like::

    response.headers['my_custom_header'] = str(uuid.uuid4())

Example
.......

.. code-block:: python
   :linenos:
   :emphasize-lines: 16, 18

   from zunzuncito import tools

   class APIResource(object):

       def __init__(self, api):
           self.headers = {'Content-Type': 'text/html; charset=UTF-8'}

       def dispatch(self, request, response):

           try:
               name = self.api.path[0]
           except:
               name = ''

           if name:
               response.headers['my_custom_header'] = name
           else:
               response.status = 406

           response.headers.update(self.headers)

           return 'Name: ' + name


The output for::

    curl -i http://api.zunzun.io/status_and_headers

.. code-block:: rest
   :linenos:
   :emphasize-lines: 1

   HTTP/1.1 406 Not Acceptable
   Request-ID: 52e78a1500ff0f217359e91eb90001737e7a756e7a756e6369746f2d617069000131000100
   Content-Type: application/json; charset=UTF-8
   Vary: Accept-Encoding
   Date: Tue, 28 Jan 2014 10:44:38 GMT
   Server: Google Frontend
   Cache-Control: private
   Alternate-Protocol: 80:quic,80:quic
   Transfer-Encoding: chunked

   Name:

The output for::

    curl -i http://api.zunzun.io/status_and_headers/foo

.. code-block:: rest
   :linenos:
   :emphasize-lines: 1,3

   HTTP/1.1 200 OK
   Request-ID: 52e78a9300ff0f3fe44a7e4fbf0001737e7a756e7a756e6369746f2d617069000131000100
   my_custom_header: foo
   Content-Type: application/json; charset=UTF-8
   Vary: Accept-Encoding
   Date: Tue, 28 Jan 2014 10:46:44 GMT
   Server: Google Frontend
   Cache-Control: private
   Alternate-Protocol: 80:quic,80:quic
   Transfer-Encoding: chunked

   Name: foo


.. seealso::

   `pep 0333 <http://www.python.org/dev/peps/pep-0333/>`_
