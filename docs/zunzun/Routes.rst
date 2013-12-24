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

Will be handled by the custom python module ``zun_env/zun_env.py``



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

.. code-block:: rest
   :emphasize-lines: 6,10,13,24,28
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
           |  |  `--zun_hasher
           |  |    |--__init__.py
           |  |    `--zun_hasher.py
           |  `--v1
           |    |--__init__.py
           |    |--zun_default
           |    | |--__init__.py
           |    | `--zun_default.py
           |    `--zun_hasher
           |      |--__init__.py
           |      `--zun_hasher.py
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
