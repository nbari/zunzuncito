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
           host          resource |path|
                                  |    |
                               path[0] |
                                       |
                                    path[1]
