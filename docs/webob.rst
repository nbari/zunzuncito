webob
=====

What is it?
...........

`WebOb <http://www.webob.org>`_ is a Python library that provides wrappers
around the WSGI request environment, and an object to help create WSGI
responses. The objects map much of the specified behavior of HTTP, including
header parsing, content negotiation and correct handling of conditional and
range requests.

This helps you create rich applications and valid middleware without knowing
all the complexities of WSGI and HTTP.

Why ?
.....

The `ZunZun <en/latest/zunzun.html>`_ instance allows you to handle the request
by following defined routes and by calling the `dispatch method </en/latest/resource/dispatch_method.html>`_,
the way you process the request is up to you, you can either do all by your
self or use tools that can allow you to simplify this process, for this last
one, **WebOb** is a library that integrates very easy and that may help you to
parse the GET, POST arguments, set/get cookies, etc; with out hassle.


Example
.......

.. code-block:: python
   :linenos:
   :emphasize-lines: 3,


   import logging

   from webob import Request
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
           req = Request(environ)

           data = {}
           data['req-GET'] = req.GET
           data['req-POST'] = req.POST
           data['req-application_url'] = req.application_url
           data['req-body'] = req.body
           data['req-content_type'] = req.content_type
           data['req-cookies'] = req.cookies
           data['req-method'] = req.method
           data['req-params'] = req.params
           data['req-path'] = req.path
           data['req-path_info'] = req.path_info
           data['req-path_qs'] = req.path_qs
           data['req-path_url'] = req.path_url
           data['req-query_string'] = req.query_string
           data['req-script_name'] = req.script_name
           data['req-url'] = req.url

           return tools.log_json(data, 4)
