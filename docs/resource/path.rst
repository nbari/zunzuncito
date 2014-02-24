path
====

``path`` is the name of the variable containing a `list <http://docs.python.org/2/tutorial/datastructures.html>`_ of elements of the URI after
has been parsed.

Suppose the incoming request is::

    http://api.zunzun.io/v1/gevent/ip


`ZunZun <en/latest/zunzun.html>`_ instance will convert it to::

    ['v1', 'gevent', 'ip']

where::

    vroot = default
    version = v1
    resource = gevent
    path = ['ip']

for the incoming request::

    http://api.zunzun.io/gevent/aa/bb

this will be generated::

    vroot = default
    version = v0
    resource = gevent
    path = ['aa', 'bb']


Example
.......

.. code-block:: python
   :linenos:
   :emphasize-lines: 11, 21

   from zunzuncito import tools


   class APIResource(object):

       def dispatch(self, request, response):

           response.headers.update(self.headers)

           try:
               name = request.path[0]
           except Exception:
               name = ''

           return 'Name: ' + name
