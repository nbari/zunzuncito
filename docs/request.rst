Request class
=============

When receiving a `request <http://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html>`_
a **request object** is created and  passed as an
argument to the `dispatch </latest/resource/dispatch_method.html>`_
method of the `APIResource class </latest/resource/APIResource.html>`_

Example
.......

.. code-block:: python
   :linenos:
   :emphasize-lines: 6

   from zunzuncito import tools

   class APIResource(object):


       def dispatch(self, request, response):
           """ your code goes here """

Request object contents
.......................

========== ================================================================================
Name       Description
========== ================================================================================
log        `logger <http://docs.python.org/2/library/logging.html>`_ intance
request_id The `request id </en/latest/zunzun/Rid.html>`_
environ    The `wsgi environ <http://www.python.org/dev/peps/pep-0333/#environ-variables>`_
URI        `REQUEST_URI or PATH_INFO <http://en.wikipedia.org/wiki/URI_scheme>`_
host       The `host </en/latest/zunzun/Hosts.html>`_ name.
method     The request method (GET, POST, HEAD, etc)
path       `list of URI elements </en/latest/resource/path.html>`_
resource   Name of the API resource
version    Current `version </en/latest/zunzun/Versions.html>`_
vroot      Name of the `vroot </en/latest/zunzun/Hosts.html?highlight=vroot>`_
========== ================================================================================

Example
.......

.. code-block:: python
   :linenos:
   :emphasize-lines: 7

   from urlparse import parse_qsl
   from zunzuncito import tools

   class APIResource(object):


       @tools.allow_methods('get, post')
       def dispatch(self, request, response):

          """
          log this request
          """
          request.log.info(tools.log_json({
              'API': request.version,
              'Method': request.method,
              'URI': request.URI,
              'vroot': request.vroot
          }, True))

          if request.method == 'POST':
              data = dict(parse_qsl(request.environ['wsgi.input'].read(), True))
          else
              data = dict(parse_qsl(request.environ['QUERY_STRING'], True))

          data = {k: v.decode('utf-8') for k, v in data.items()}

          return tools.log_json(data)
