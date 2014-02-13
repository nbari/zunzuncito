gevent
======

`gevent <http://www.gevent.org/>`_ is a coroutine-based Python networking library that uses greenlet to
provide a high-level synchronous API on top of the libev event loop.


When using gevent and 'yield' you may want to call the 'start_response' before
so that it can send your proper headers, for this you must use something like::

    response.send()


.. seealso::

   `The start_response() Callable <http://www.python.org/dev/peps/pep-0333/#the-start-response-callable>`_


Example
-------

The following code will:
    * output the result using content-type: 'text/html',
    * print 'sleep 1 second.' and call gevent.sleep(1),
    * print 'sleep 3 second...' and call gevent.sleep(3),
    * print 'done. getting some ips...' call gevent.socket.gethostbyname


.. code-block:: python
   :emphasize-lines: 38
   :linenos:

   import gevent
   import gevent.socket

   from zunzuncito import tools


   def bg_task():
       for i in range(1, 10):
           print "background task", i
           gevent.sleep(2)


   def long_task():
       for i in range(1, 10):
           print i
           gevent.sleep()


   class APIResource(object):

       def __init__(self):
           self.headers = {'Content-Type': 'text/html; charset=UTF-8'}

       def dispatch(self, request, response):

           request.log.debug(tools.lo g_json({
               'API': request.version,
               'Method': request.method,
               'URI': request.URI,
               'vroot': request.vroot
           }, True))

           response.headers.update(self.headers)

           """
           calls start_response
           """
           response.send()

           t = gevent.spawn(long_task)
           t.join()

           yield "sleep 1 second.<br/>"

           gevent.sleep(1)

           yield "sleep 3 seconds...<br/>"

           gevent.sleep(3)

           yield "done.<br/>getting some ips...<br/>"

           urls = [
               'www.google.com',
               'www.example.com',
               'www.python.org',
               'zunzun.io']

           jobs = [gevent.spawn(gevent.socket.gethostbyname, url) for url in urls]
           gevent.joinall(jobs, timeout=2)

           for j in jobs:
               yield "ip = %s<br/>" % j.value

           gevent.spawn(bg_task)
