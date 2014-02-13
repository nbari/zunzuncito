@allow_methods decorator
========================

The ``@allow_methods`` decorator when applied to the `dispatch method </en/latest/resource/dispatch_method.html>`_ works like a filter to specified `HTTP methods <http://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods>`_


Example
.......

.. code-block:: python
   :linenos:
   :emphasize-lines: 6


   import logging
   from zunzuncito import tools

   class APIResource(object):

       @tools.allow_methods('post, put')
       def dispatch(self, request, response):
           """ your code goes here """


In this case all the request that are not **POST** or **PUT** will be rejected
