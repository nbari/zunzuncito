Rid
===

The ```rid`` argument, contains the name of the environ variable  containing the request id if any, for example when using GAE::

   app = zunzuncito.ZunZun(root, versions, hosts, routes, rid='REQUEST_LOG_ID')
