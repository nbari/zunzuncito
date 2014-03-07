FAQ
===


Why I get a warnings for some requests?
.......................................

If you get something like this:

.. code-block:: json
    :linenos:

    WARNING  2014-03-07 10:01:30,845 zunzun.py:102] {
     "API": "v0",
     "HTTPError": "501",
     "URI": "/",
     "body": {
      "code": "None",
      "description": "No module named myapp_api.default.v0.zun_default.zun_default",
      "display": "False",
      "headers": "None",
      "log": "True",
      "status": "501",
      "title": "ImportError: myapp_api.default.v0.zun_default.zun_default, myapp_api.default.v0.zun__catchall.zun__catchall: No module named myapp_api.default.v0.zun__catchall.zun__catchall"
     },
     "method": "GET",
     "rid": "f8df3ffc8294c0ec0fcc10bbc7c4bfe0febbcaaaf83ff619ab56ca0209225dd0d5f1fd19e42f6b4c1fa2ef0a1f3127"
    }

Is because you could be missing an ``__init__.py``, all the subdirectories of your *API* need need to be treated like python modules.


.. sealso::

    `This is the directory structure. </en/latest/Quickstart.html>`_
