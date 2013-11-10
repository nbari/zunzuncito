### Design Goals
* Keep it simple and small, avoiding extra complexity at all cost. [KISS](http://en.wikipedia.org/wiki/KISS_principle)
* Create routes on the fly or by defining regular expressions.
* Support API versions out of the box without altering routes.
* Via decorator or in a defined route, accepts only certain [HTTP methods](http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html).
* Follow the single responsibility [principle](http://en.wikipedia.org/wiki/Single_responsibility_principle).
* Be compatible with any WSGI server. Example: [uWSGI](http://uwsgi-docs.readthedocs.org/en/latest/), [Gunicorn](http://gunicorn.org/), [Twisted](http://twistedmatrix.com/), etc.
* Structured Logging using [JSON](http://en.wikipedia.org/wiki/JSON).
* No template rendering.
* Tracing Request-ID "rid" per request.
* Compatibility with Google App Engine. [demo](http://api.zunzun.io)

> Documentation : [docs.zunzun.io](http://docs.zunzun.io)

### What & Why ZunZuncito
ZunZuncito is a [python](http://python.org/) package that allows to create and maintain [REST](http://en.wikipedia.org/wiki/REST) API's without hassle.

The simplicity for sketching and debugging helps to develop very fast; versioning is inherit by default, which allows to serve and maintain existing applications, while working in new releases with no need to create separate instances. All the applications are WSGI [PEP 333](http://www.python.org/dev/peps/pep-0333/) compliant, allowing to migrate existing code to more robust frameworks, without need to modify the existing code.

The idea of creating ZunZuncito, was the need of a very small and light tool (batteries included), that could help to create and deploy REST API's quickly, without forcing the developers to learn or follow a complex flow but, in contrast, from the very beginning, guide them to properly structure their API, giving special attention to "versioned URI's", having with this a solid base that allows to work in different versions within a single ZunZun instance without interrupting service of any existing API [resources](http://en.wikipedia.org/wiki/Web_resource).


### How it works

The main application contains a **ZunZun** instance that must be served by a [WSGI compliant server](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface). All requests are later handled by custom python modules; ZunZun is the name of the main class for the zunzuncito module.

All the custom python modules follow the same structure. They basically consist of a class called **APIResource** which contains a method called **dispatch** that will require two arguments: a WSGI environment "environ" as first argument and a function "start_response" that will start the response, [see PEP 333](http://www.python.org/dev/peps/pep-0333/)

ZunZun core turns around three arguments:

```
root: directory containing all your API modules - see this like the "document_root"
versions: list of supported versions ['v0', 'v1', 'v2']
routes: list of tuples containing regex patterns, handlers and allowed http methods
```

> In the [docs](http://docs.zunzun.io) you can find a more detailed overview of the ZunZun arguments and the class itself.

When a new request arrive, the ZunZun router parses the [REQUEST_URI](http://en.wikipedia.org/wiki/URI_scheme) in order to accomplish this pattern:

    /version/api_resource/path

The router first analyses the URI and determines if it is versioned or not by finding a match with the current specified versions, in case no one is found, fallback to the default which is always the first item on the versions list in case one provided, or 'v0'.

After this process, the REQUEST_URI becomes a list of resources - something like:

    ['version, 'api_resource', 'path']

Suppose that the incoming request is:

    'http://api.zunzun.io/v1/gevent/ip'

ZunZun will convert it to:

    ['v1', 'gevent', 'ip']

The second step on the router is to find a match within the routes list and the local modules, but before going further lets see the directory structure for the root (document_root), the first and required argument for the ZunZun class.

<pre>
my_api
|--__init__.py
|--v0
|  |--__init__.py
|  |--zun_default
|  |  |--__init__.py
|  |  `--zun_default.py
|  |--zun_gevent
|  |  |--__init__.py
|  |  `--zun_gevent.py
|  `--zun_my
|    |--__init__.py
|    `--zun_my.py
|--v1
|  |--__init__.py
|  |--zun_default
|  |  |--__init__.py
|  |  `--zun_default.py
|  |--zun_gevent
|  |  |--__init__.py
|  |  `--zun_gevent.py
|  `--zun_my
|    |--__init__.py
|    `--zun_my.py
`--v2
   |--__init__.py
   |--zun_default
   |  |--__init__.py
   |  `--zun_default.py
   |--zun_gevent
   |  |--__init__.py
   |  `--zun_gevent.py
   `--zun_my
     |--__init__.py
     `--zun_my.py
</pre>

As you can see basically it is a directory containing sub-directories which at the end are all python custom modules and can be called in a clean way like:

    import my_api.v1.zun_default

> notice the prefix **zun_**

This helps the router to dispatch all the request to an existing module, so continue with the flow, for the incoming request: http://api.zunzun.io/v1/gevent/ip we will try to find a module that matches the API resource 'gevent':

    'http://api.zunzun.io/v1/gevent/ip' ==> ['v1', 'gevent', 'ip']
    version = v1
    api_resource = gevent
    path = ip

In case a list of routes is passed as an argument to the ZunZun instance, the router will try to match the api_resource with the items of the routes list. If no matches are found it will try to find the module in the root directory.

The routes format is very simple, it can be something like:

```python
"""
format is:
regex pattern, handler (python module), allowed HTTP methods (defaults to ALL)
"""
[
 ('/.*', default),
 ('/test', default, 'POST, PUT, PATCH'),
 ('(?:[0-9]{1,3}\.){3}[0-9]{1,3}', 'ip', 'GET')
]
```

Lets suppose these routes were passed to the ZunZun instance, therefore the router would try to find a match between the api_resource **gevent** in our example with the regex patterns in the list, basically something like:

    gevent in: ['/.*', '/test', '(?:[0-9]{1,3}\.){3}[0-9]{1,3}']

if no match is found then the router would try to load the module from the root directory using something like:

```python
import my_api.v1.zun_gevent.zun_gevent
```

In case it doesn't find a module, an HTTP status [501 Not Implemented](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html) code is returned to the client. Otherwise the python module is imported by the router and the request is handled entirely by the imported module.


### The zun_ prefix

You may ask, why the need of the "zun_" prefix and why not just create a simple structure having the same name that the api_resource.

Well, this is more due the way python imports modules. It intends to avoid collisions by having same modules with the same name. You can change the prefix by passing it as an argument to the ZunZun instance or also disabling it by sending an empty prefix.

In the previous example, the REQUEST_URI contains an **APIResource** with the word **gevent**. The imported module name is in 'zun_gevent/zun_gevent.py' that gives the flexibility to use the [gevent](http://www.gevent.org/) library within your module without creating any conflict. Your zun_gevent.py would look like:

```python
import gevent
import gevent.socket
...
```

That way you can have any work with gevent or any other API resource having an identical name of your current python modules without any conflict.


### A basic example

Contents of file app.py:

```python
import zunzuncito

root = 'my_api'
versions = ['v0', 'v1', 'v2']
routes = [
    ('/my', 'ip_tools', 'GET'),
    ('/status', 'http_status', 'GET'),
    ('/upload/', 'test_post', 'PUT, POST')
]
app = zunzuncito.ZunZun(root, versions, routes)
```

Contents of file zun_default.py located in "my_api/zun_default/zun_default.py"

```python
"""
zun_default.py API resource
"""
import json
import logging
from zunzuncito import http_status_codes
from zunzuncito.tools import MethodException, HTTPException, allow_methods


class APIResource(object):

    def __init__(self, api):
        self.api = api
        self.status = 200
        self.headers = api.headers.copy()
        self.log = logging.getLogger()
        self.log.setLevel('INFO')
        self.log = logging.LoggerAdapter(
            logging.getLogger(), {
                'rid': api.request_id,
                'indent': 4
            })
        self.log.info(dict((x, y) for x, y in (
            ('API', api.version),
            ('URI', api.URI),
            ('method', api.method)
        )))

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
```

To run it with gunicorn:

    gunicorn -b :8080 -w4 app:app

To run it with uWSGI:

    uwsgi --http :8080 --wsgi-file app.py --callable app --master


### Install

    git clone https://github.com/nbari/zunzuncito.git

    python setup.py install

### Demo

Current demo running on Google App Engine.

[http://api.zunzun.io](http://api.zunzun.io)

available API resources:

* /my
* /status

To get your current IP and location:

    http://api.zunzun.io/my

To get only the IP:

    http://api.zunzun.io/my/ip


For example, to get the meaning of status code 201

    http://api.zunzun.io/status/201

### GAE

Tu have a ZunZun instance up and running in Google App Engine these are the configurations:

Contents of the app.yaml file:

```yaml
application: <your-GAE-application-id>
version: 1
runtime: python27
api_version: 1
threadsafe: no

handlers:
- url: /favicon\.ico
-   static_files: favicon.ico
-     upload: favicon\.ico
-
-     - url: .*
-       script: main.py

```

Contents of the main.py file:

```python

from google.appengine.ext.webapp.util import run_wsgi_app
import zunzuncito

root = 'my_api'
versions = ['v0', 'v1']
routes = [
    ('/my/?.*', 'ip_tools', 'GET'),
    ('/status/?.*', 'http_status', 'GET')
]

app = zunzuncito.ZunZun(root, versions, routes)

run_wsgi_app(app)
```

Directory structure:

<pre>
<your-GAE-application-id>
|--app.yaml
|--main.py
|--favicon.ico
|--zunzuncito
|  |--__init__.py
|  |--http_status_codes.py
|  |--tools.py
|  `--zunzun.py`
`--my_api
  |--v0
  | |--__init__.py
  | |--zun_ip_tools
  | | |--__init__.py
  | | `--zun_ip_tools.py
  | |--zun_http_status
  | | |--__init__.py
  | | `zun_http_status.py
  `--v1
    |--__init__.py
    |--zun_ip_tools
    | |--__init__.py
    | `--zun_ip_tools.py
    `--zun_http_status
       |--__init__.py
       `--zun_http_status.py
</pre>

Basically you just copy the zunzuncito module into your GAE application directory, define your root, versions and routes, create a ZunZun object and focus more on your API resources (custom python modules)
