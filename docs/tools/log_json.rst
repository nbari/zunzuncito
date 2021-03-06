log_json
========

The ``log_json`` is a function that given a `dictionary <http://docs.python.org/2/tutorial/datastructures.html#dictionaries>`_, returns a
`json <http://json.org/example>`_ structure.

This helps that logs can be parsed and processed by external tools.

The arguments are::

    log_json(log, indent=False)


:log: a python dictionary
:indent: returns the json structured indented (more human readable)

.. note::

   If indent is a non-negative integer, then JSON array elements and object
   members will be pretty-printed with that indent level. An indent level of 0,
   or negative, will only insert newlines. None (the default) selects the most
   compact representation.

.. seealso::

   `python json <http://docs.python.org/2/library/json.html#basic-usage>`_

Example
.......

.. code-block:: python
   :linenos:
   :emphasize-lines: 7


   from zunzuncito import tools

   class APIResource(object):

       def dispatch(self, request, response):

           request.log.debug(tools.log_json({
               'API': request.version,
               'Method': request.method,
               'URI': request.URI,
               'vroot': request.vroot
           }, True))

           """ your code goes here """


.. seealso::

   `Structured Logging <http://docs.python.org/2/howto/logging-cookbook.html#implementing-structured-logging>`_
