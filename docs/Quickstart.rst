Quick Start
===========

This is the directory structure:

.. sidebar:: API directory structure

   :app.py: application python file.
   :my_api: The **root** directory of the API.
   :default: The **vroot** directory.
   :v0: Directory for default API resources or for version *0* when specified.
   :v1: Directory for API resources version *1*


.. code-block:: rest
   :emphasize-lines: 3,4,6,8,16
   :linenos:

   /home/
     `--zunzun/
        |--app.py
        `--my_api
          |--__init__.py
          `--default
            |--__init__.py
            |--v0
            |  |--__init__.py
            |  |--zun_default
            |  |  |--__init__.py
            |  |  `--zun_default.py
            |  `--zun_hasher
            |    |--__init__.py
            |    `--zun_hasher.py
            `--v1
               |--__init__.py
               |--zun_default
               | |--__init__.py
               | `--zun_default.py
               `--zun_hasher
                 |--__init__.py
                 `--zun_hasher.py

Inside directory /home/zunzun there is a file called **app.py** and a directory **my_api**.

For a very basic API, contents of file **app.py** can be:

.. code-block:: python
   :emphasize-lines: 3,7,11
   :linenos:

   import zunzuncito

   root = 'my_api'

   versions = ['v0', 'v1']

   hosts = {'*': 'default'}

   routes = {'default':[
       ('/(md5|sha1|sha256|sha512)(/.*)?', 'hasher', 'GET, POST'),
       ('/.*', 'default')
   ]}

   app = zunzuncito.ZunZun(root, versions, hosts, routes)


* line 3 defines the "document root" for your API
* line 7 gives multitenant support, in the example all "*" is going to be
  handled by the 'default' **vroot**
* line 11 contains a regex matching all the requests, it is at the bottom
  because in the routes, order matters.


The contents of the **my_api** contain python modules (API Resources) for
example the content of module zun_default/zun_default.py is:

.. code-block:: python
   :linenos:

   import json
   import logging
   from zunzuncito import http_status_codes
   from zunzuncito.tools import MethodException, HTTPException, allow_methods,
   log_json


   class APIResource(object):

   def __init__(self, api):
       self.api = api
       self.status = 200
       self.headers = api.headers.copy()
       self.log = logging.getLogger()
       self.log.info(log_json({
            'vroot': api.vroot,
            'API': api.version,
            'URI': api.URI,
            'method': api.method
        }, True)
        )

   @allow_methods('get')
   def dispatch(self, environ, start_response):
       headers = self.api.headers
       start_response(
           getattr(http_status_codes, 'HTTP_%d' %
                   self.status), list(headers.items()))
       data = {}
       data['about'] = ("Hi %s, I am zunzuncito a micro-framework for creating"
                        " REST API's, you can read more about me in: "
                        "www.zunzun.io") % environ.get('REMOTE_ADDR', 0)
       data['request-id'] = self.api.request_id
       data['URI'] = self.api.URI
       data['method'] = self.api.method

       return json.dumps(data, sort_keys=True, indent=4)



How to run it
-------------

Zunzuncito is compatible with any WSGI server, next are some examples of how to
run it with `uWSGI <http://uwsgi-docs.readthedocs.org/en/latest/>`_, and
`Gunicorn <http://gunicorn.org/>`_, `Twisted <http://twistedmatrix.com/>`_.

uWSGI
.....

Listening on port 8080::

    uwsgi --http :8080 --wsgi-file app.py --callable app --master

Listening on port 80 with 2 processes and stats on http://127.0.0.1:8181::

    uwsgi --http :80 --wsgi-file app.py --callable app --master --processes 2 --threads 2 --stats 127.0.0.1:8181 --harakiri 30


Using a .ini file

.. sidebar:: TRACK_ID

   :route-run: adds a custom tracking ID


.. code-block:: rest
   :emphasize-lines: 3,4
   :linenos:

   [uwsgi]
   http = :8080
   route-run = addvar:TRACK_ID=${uwsgi[uuid]}
   route-run = log:TRACK_ID = ${TRACK_ID}
   master = true
   processes = 2
   threads = 1
   stats = 127.0.0.1:8181
   harakiri = 30
   wsgi-file = app.py
   callable = app


To trace all the requests you could and append to the headers the 'REQUEST_ID'
use::

    app = zunzuncito.ZunZun(root, versions, hosts, routes, rid='TRACK_ID')



Gunicorn
........

Listening on port 8080::

    gunicorn -b :8080  app:app

Listening on port 8080 with 2 processes::

    gunicorn -b :8080 -w2 app:app


GAE
---

Tu have a ZunZun instance up and running in Google App Engine you can use the
following configuration.

Contents of the **app.yaml** file::

    application: <your-GAE-application-id>
    version: 1
    runtime: python27
    api_version: 1
    threadsafe: yes

    handlers:
    - url: /favicon\.ico
      static_files: favicon.ico
      upload: favicon\.ico

    - url: .*
      script: main.app


When using GAE the global unique identifier for a request is:
**REQUEST_LOG_ID**  therefore if you want to append the request id to your response you need to run
the app like this::

   app = zunzuncito.ZunZun(root, versions, hosts, routes, rid='REQUEST_LOG_ID')
