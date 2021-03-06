WebOb
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

The following code, handles the request for `http://api.zunzun.io/webob <http://api.zunzun.io/webob>`_.

.. code-block:: python
   :linenos:
   :emphasize-lines: 1, 9

   from webob import Request
   from zunzuncito import tools


   class APIResource(object):


       def dispatch(self, request, response):
           req = Request(request.environ)

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


Basically you only need to pass the **environ** argument to the ``webob.Request``::

    def dispatch(self, environ):
        req = Request(environ)
        """ your code goes here """

.. seealso::

    `WebOb Request <http://docs.webob.org/en/latest/reference.html#id1>`_

GAE
...

When using google app engine you need to add this lines to your
`app.yaml <https://developers.google.com/appengine/docs/python/config/appconfig>`_
file in order to be available to import webob::

   libraries:
   - name: webob
     version: latest
