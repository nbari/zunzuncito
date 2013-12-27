Debug
=====

The python `logging <http://docs.python.org/2/library/logging.html>`_ module is used for creating logs

To log how the API is handling the requests you can run the app like this::

   app = zunzuncito.ZunZun(root, versions, hosts, routes, debug=True)

.. note::

   The default loglevel is **INFO**
