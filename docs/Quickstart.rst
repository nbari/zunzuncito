Quick Start
===========

URI parts:

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


This is the directory structure:

.. sidebar:: API directory structure

   :app.py: application python file.
   :my_api: The **root** directory of the API.
   :default: The **vroot** directory.
   :v0: Directory for default API resources or for version **0** when specified.
   :v1: Directory for API resources version **1**
   :get: API resource
   :client: Path

.. code-block:: rest
   :emphasize-lines: 3,4,6,8,13,16
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
              |  |--zun_get
              |  |  |--__init__.py
              |  |  |--zun_get.py
              |  |  `--zun_client
              |  |     |--__init__.py
              |  |     `--zun_client.py
              |  `--zun_hasher
              |     |--__init__.py
              |     `--zun_hasher.py
              `--v1
                 |--__init__.py
                 |--zun_default
                 |  |--__init__.py
                 |  `--zun_default.py
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

   # For appending the Request-ID header on GAE
   # app = zunzuncito.ZunZun(root, versions, hosts, routes, rid='REQUEST_LOG_ID')


* line 3 defines the "document root" for your API
* line 7 gives multitenant support, in the example all "*" is going to be
  handled by the 'default' **vroot**
* line 11 contains a regex matching all the requests, it is at the bottom
  because in the routes, order matters.


The contents of the **my_api** contain python modules (API Resources) for
example the content of module `zun_default/zun_default.py <https://github.com/nbari/zunzuncito/blob/master/my_api/default/v0/zun_default/zun_default.py>`_ is:

.. code-block:: python
   :linenos:

   from zunzuncito import tools


   class APIResource(object):

      @tools.allow_methods('get, head')
      def dispatch(self, request, response):

          request.log.debug(tools.log_json({
              'API': request.version,
              'URI': request.URI,
              'method': request.method,
              'vroot': request.vroot
          }, True))

          data = {}
          data['about'] = ("Hi %s, I am zunzuncito a micro-framework for creating"
                           " REST API's, you can read more about me in: "
                           "www.zunzun.io") % request.environ.get('REMOTE_ADDR', 0)

          data['Request-ID'] = request.request_id
          data['URI'] = request.URI
          data['Method'] = request.method

          return tools.log_json(data, 4)


.. seealso::

   `Basic template <http://docs.zunzun.io/en/latest/resource/dispatch_method.html#basic-template>`_


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

   :route-run: adds a custom tracking ID, see `uwsgi InternalRouting <http://uwsgi-docs.readthedocs.org/en/latest/InternalRouting.html>`_


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


For this case, to append to all your responses the **Request-ID** header run
the app like this::

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

Contents of the **app.yaml** file:

.. sidebar:: main.app

   :script: **main** is the main.py file **app** is the instance of zunzun


.. code-block:: rest
   :linenos:
   :emphasize-lines: 13

   application: <your-GAE-application-id>
   version: 1
   runtime: python27
   api_version: 1
   threadsafe: yes

   handlers:
   - url: /favicon\.ico
     static_files: favicon.ico
     upload: favicon\.ico

   - url: /.*
     script: main.app


.. note::
   When using GAE the global unique identifier per request is: `REQUEST_LOG_ID <https://developers.google.com/appengine/docs/python/logs/requestlogclass#RequestLog_request_id>`_

For this case, to append to all your responses the **Request-ID** header run
the app like this::

   app = zunzuncito.ZunZun(root, versions, hosts, routes, rid='REQUEST_LOG_ID')
