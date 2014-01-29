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

The `ZunZun <en/latest/zunzun.html>`_ instance allows you to handle the request
by following defined routes and by calling the `dispatch method </en/latest/resource/dispatch_method.html>`_,
the way you process the request is up to you, you can either do all by your
self or use tools that can allow you to simplify this process, for this last
one **WebOb** is a libray that integrates very easy and can help you to
simplify thins.
