Routes
======

The ``routes`` argument must be a dictionary containing defined routes per
vroot

.. code-block:: python
   :emphasize-lines: 14,15,16,17,18,19,20
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
       ('/(md5|sha1|sha256|sha512)(/.*)?', 'hasher', 'GET, POST'),
       ('/.*', 'default')
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

Will be handled by the python custom module ``zun_env/zun_env.py``

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


Will be handled by the pythom custom module ``zun_hasher/zun_hahser.py``, this
is because a specified route::

       ('/(md5|sha1|sha256|sha512)(/.*)?', 'hasher', 'GET, POST')





Routes dictionary structure
---------------------------

In the above example, the  ``routes`` dictionary contains:

+---------+---------------------------------+--------------+--------------+
| vroot   | regular expression              | API Resource | HTTP methods |
+=========+=================================+==============+==============+
| default | /(md5|sha1|sha256|sha512)(/.*)? | hasher       | 'GET, POST'  |
+---------+---------------------------------+--------------+--------------+
| default | /.*                             | default      |              |
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
       ('/(md5|sha1|sha256|sha512)(/.*)?', 'hasher', 'GET, POST'),
       ('/.*', 'default')
   ]
   routes['beta'] = [
       ('/upload/?.*', 'upload', 'PUT, POST'),
       ('/.*', 'default')
   ]

Directory structure
-------------------

The API directory structure for the examples presented here is:

.. code-block:: rest
   :emphasize-lines: 6,10,13,16,21,27
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
           |  |    |--__init__.py
           |  |    `--zun_hasher.py
           |  `--v1
           |     |--__init__.py
           |     |--zun_default
           |     | |--__init__.py
           |     | `--zun_default.py
           |     `--zun_hasher
           |       |--__init__.py
           |       `--zun_hasher.py
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
