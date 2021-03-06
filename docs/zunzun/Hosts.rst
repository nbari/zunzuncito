Hosts
=====

The ``hosts`` argument contains a dictionary of domains and vroots.


A very basic API, contents of file **app.py** can be:

.. sidebar:: Hosts dictionary elements

    :\*: wildcard matching all HTTP_HOSTS
    :default: vroot

.. code-block:: python
   :emphasize-lines: 7
   :linenos:

   import zunzuncito

   root = 'my_api'

   versions = ['v0', 'v1']

   hosts = {'*': 'default'}

   routes = {'default':[
       ('/my/?.*', 'ip_tools', 'GET')
   ]}

   app = zunzuncito.ZunZun(root, versions, hosts, routes, debug=True)


To support `multi-tenancy <http://en.wikipedia.org/wiki/Multitenancy>`_ the
**hosts** dictionary is needed.

A `dictionary structure <http://docs.python.org/2/tutorial/datastructures.html#dictionaries>`_ is
formed by **key: value** elements, in this case the key is used for
specifying the 'host' and the value to specify the **vroot**


Hosts structure & vroot
-----------------------

The wildcard character **\*** can be used, for example:

.. code-block:: rest
   :linenos:

   hosts = {
       '*': 'default',
       '*.zunzun.io': 'default',
       'ejemplo.org': 'ejemplo_org',
       'api.ejemplo.org': 'api_ejemplo_org'
   }

* line 2 matches any host ``*`` and will be served on vroot '**default**'
* line 3 matches any host ending with ``zunzun.io`` and will be served on vroot '**default**'
* line 4 matches host ``ejemplo.org`` and will be server on vroot '**ejemplo_org**'
* line 5 matches host ``api.ejemplo.org`` and will be served on vroot
  '**api_ejemplo_org**'

Notice that the vroot values use ``_`` as separator instead of a dot, this
is to prevent conflicts on how python read files. for example this request::

    http://api.ejemplo.org/v0/gevent

Internally will be calling something like:

.. code-block:: python

   import my_api.api_ejemplo_org.v0.zun_gevent.zun_gevent



Directory structure
-------------------

The API directory structure for this example would be:

.. sidebar:: virtual roots (vroot)

   :default: `line 2, 3 <#hosts-structure-vroot>`_
   :ejemplo_org: `line 4 <#hosts-structure-vroot>`_
   :api_ejemplo_org: `line 5 <#hosts-structure-vroot>`_


.. code-block:: rest
   :linenos:
   :emphasize-lines: 6,13,20

    /home/
     `--zunzun/
        |--app.py
        `--my_api
           |--__init__.py
           |--default
           |  |--__init__.py
           |  `--v0
           |     |--__init__.py
           |     `--zun_default
           |        |--__init__.py
           |        `--zun_default.py
           |--ejemplo_org
           |  |--__init__.py
           |  `--v0
           |     |--__init__.py
           |     `--zun_default
           |        |--__init__.py
           |        `--zun_default.py
           `--api_ejemplo_org
              |--__init__.py
              `--v0
                 |--__init__.py
                 |--zun_gevent
                 |  |--__init__.py
                 |  `--zun_gevent.py
                 `--zun_default
                    |--__init__.py
                    `--zun_default.py
