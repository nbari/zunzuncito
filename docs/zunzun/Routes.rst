Routes
======

The ``routes`` argument must be a dictionary containing defined routes per
**vroot**.

.. code-block:: python
   :emphasize-lines: 14,15,16,17,18,19
   :linenos:

   import zunzuncito

   root = 'my_api'

   versions = ['v0', 'v1']

   hosts = {
       '*': 'default',
       'domain.tld': 'default',
       '*.domain.tld': 'default',
       'beta.domain.tld': 'beta'
   }

   routes = {'default':[
       ('/(md5|sha1|sha256|sha512)(/.*)?', 'hasher', 'GET, POST')
   ],'beta':[
       ('/upload/?.*', 'upload', 'PUT, POST'),
       ('/.*', 'default')
   ]}

   app = zunzuncito.ZunZun(root, versions, hosts, routes, debug=True)


.. note::
   By default, if no **routes** specified, the requests are handled by matching the URI
   request with an valid **API Resource**, you only need to specify **routes** if want to
   handle different URI requests with a single **API Resource**


Example
.......

The request::

    http://api.zunzun.io/v0/env

Will be handled by the python custom module `zun_env/zun_env.py <https://github.com/nbari/zunzuncito/blob/master/my_api/default/v0/zun_env/zun_env.py>`_

But all the following `GET <http://en.wikipedia.org/wiki/GET_(HTTP)#Request_methods>`_ requests:

* `http://api.zunzun.io/v0/md5/freebsd <http://api.zunzun.io/v0/md5/freebsd>`_
* `http://api.zunzun.io/v0/sha1/freebsd <http://api.zunzun.io/v0/sha1/freebsd>`_
* `http://api.zunzun.io/v0/sha256/freebsd <http://api.zunzun.io/v0/sha256/freebsd>`_
* `http://api.zunzun.io/v0/sha512/freebsd <http://api.zunzun.io/v0/sha512/freebsd>`_

And also this `POST <http://en.wikipedia.org/wiki/POST_(HTTP)#Request_methods>`_ requests::

    curl -i -X POST http://api.zunzun.io/v0/md5 -d 'freebsd'

    curl -i -X POST http://api.zunzun.io/v0/sha1 -d 'freebsd'

    curl -i -X POST http://api.zunzun.io/v0/sha256 -d 'freebsd'

    curl -i -X POST http://api.zunzun.io/v0/sha512 -d 'freebsd'


Will be handled by the pythom custom module `zun_hasher/zun_hahser.py <https://github.com/nbari/zunzuncito/tree/master/my_api/default/v0/zun_hasher>`_, this is because a specified route::

       ('/(md5|sha1|sha256|sha512)(/.*)?', 'hasher', 'GET, POST')

You can totally omit routes and handle all by following the API
`directory structure <#id1>`_,
this can give you more fine control over you API, for example in
the previous example you could create modules for every hash algorithm, and
have independent modules like:

.. code-block:: rest
   :emphasize-lines: 3,6,9,12
   :linenos:

   `--v0
       |--__init__.py
       |--zun_md5
       |  |--__init__.py
       |  `--zun_md5.py
       |--zun_sha1
       |  |--__init__.py
       |  `--zun_sha1.py
       |--zun_sha256
       |  |--__init__.py
       |  `--zun_sha256.py
       `--zun_sha512
          |--__init__.py
          `--zun_sha512.py


.. note::
   Defining routes or using the directory structure is a design choice, some
   times having all in one module can be easy to maintain, while other times
   having a module for each specific task, would be prefered.

.. seealso::
   The `zun_ prefix </en/latest/zunzun/Prefix.html>`_

The flow
........

When a new request arrive, the ZunZun router searches for a ``vroot`` declared on
the `hosts </en/latest/zunzun/Hosts.html>`_ dictionary matching the current `HTTP_HOST <http://en.wikipedia.org/wiki/Hostname>`_.

Once a ``vroot`` is found, the ZunZun router parses the `REQUEST_URI <http://en.wikipedia.org/wiki/URI_scheme>`_ in order to
accomplish this pattern::

    /version/api_resource/path


The router first analyses the URI and determines if it is versioned or not by
finding a match with the current `specified versions </en/latest/zunzun/Versions.html>`_
in case no one is found, fallback to the default which is always the first
item on the versions list in case one provided, or ``v0``.

After this process, the REQUEST_URI becomes a list of resources - something
like:

.. code-block:: python

   ['version', 'api_resource', 'path']

   # for  http://api.zunzun.io/v0/env
   ['v0', 'env']

   # for http://api.zunzun.io/v0/sha256/freebsd
   ['v0', 'sha256', 'freebsd']


The second step on the router is to find a match within the ``routes`` dictionary and the
local modules.

In case a list of ``routes`` is passed as an argument to the ZunZun instance, the
router will try to match the `API_resource </en/latest/resource.html>`_ with the items of the ``routes``
dictionary. If no matches are found it will try to find the module in the root directory.

Routes dictionary structure
...........................

In the above example, the  ``routes`` dictionary contains:

+---------+---------------------------------+--------------+--------------+
| vroot   | regular expression              | API Resource | HTTP methods |
+=========+=================================+==============+==============+
| default | /(md5|sha1|sha256|sha512)(/.*)? | hasher       | 'GET, POST'  |
+---------+---------------------------------+--------------+--------------+
| beta    | /upload/?.*                     | upload       | 'PUT, POST'  |
+---------+---------------------------------+--------------+--------------+
| beta    | /.*                             | default      |              |
+---------+---------------------------------+--------------+--------------+

Translating the table to code:

.. code-block:: python
   :linenos:

   routes = {}
   routes['default'] = [
       ('/(md5|sha1|sha256|sha512)(/.*)?', 'hasher', 'GET, POST')
   ]
   routes['beta'] = [
       ('/upload/?.*', 'upload', 'PUT, POST'),
       ('/.*', 'default')
   ]

.. warning::

   Regular expressions have priority over local **API Resources**, for example
   the regex ``(/.*)`` will catch-all all the request, that's why in our
   example is the last regex, since order is important.


Directory structure
-------------------

The API directory structure for the examples presented here is:

.. sidebar:: API directory structure

   :default: **vroot** directory
   :beta: **vroot** directory

.. code-block:: rest
   :emphasize-lines: 6,27
   :linenos:

   /home/
     `--zunzun/
        |--app.py
        `--my_api
           |--__init__.py
           |--default
           |  |--__init__.py
           |  |--v0
           |  |  |--__init__.py
           |  |  |--zun_default
           |  |  |  |--__init__.py
           |  |  |  `--zun_default.py
           |  |  |--zun_env
           |  |  |  |--__init__.py
           |  |  |  `--zun_env.py
           |  |  `--zun_hasher
           |  |     |--__init__.py
           |  |     `--zun_hasher.py
           |  `--v1
           |     |--__init__.py
           |     |--zun_default
           |     |  |--__init__.py
           |     |  `--zun_default.py
           |     `--zun_hasher
           |        |--__init__.py
           |        `--zun_hasher.py
           `--beta
              |--__init__.py
              `--v0
                 |--__init__.py
                 |--zun_default
                 |  |--__init__.py
                 |  `--zun_default.py
                 `--zun_upload
                    |--__init__.py
                    `--zun_upload.py
