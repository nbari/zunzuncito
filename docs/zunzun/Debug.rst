Debug
=====

The python `logging <http://docs.python.org/2/library/logging.html>`_ module is used for creating logs

To enable debugging, set the ``debug`` argument to **True**, this will log how
the API is handling the requests, besides seting the loglevel to **DEBUG**
you can run the app like this::

   app = zunzuncito.ZunZun(root, versions, hosts, routes, debug=True)

.. note::

   The default loglevel is **INFO**
