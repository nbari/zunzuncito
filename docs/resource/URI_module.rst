URI module
==========

Every resource has a module, this is made with the intention to have more order
and give more flexibility.

URI parts
.........

.. code-block:: rest

    http://api.zunzun.io/v0/get/client/ip
    \__________________/\_/\__/\_____/\_/
             |           |   | \__|____|/
             |       version |    |  | |
       host (default)    resource |path|
                                  |    |
                               path[0] |
                                       |
                                    path[1]



**ZunZun** translates that URI to::

    my_api.default.v0.zun_get.zun_client.zun_client


Example
.......

The request http://api.zunzun.io/get/client/ will be handled by the file
``zun_cilent.py`` notice that that the URI ends with an **/**


If the request where http://api.zunzun.io/get/client without the ending slash
it will be handled by ``zun_get.py``.


.. seealso::

    `URI scheme <a href="http://en.wikipedia.org/wiki/URI_scheme">`_,
    `Uniform_resource_locator <a http://en.wikipedia.org/wiki/Uniform_resource_locator>`_
