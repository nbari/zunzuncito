### Design Goals
* Keep it simple and small, avoid extra complexity at all cost [KISS](http://en.wikipedia.org/wiki/KISS_principle).
* Creation of routes on the fly or by defining regular expressions.
* Support API versions out of the box without altering routes.
* Via decorator or in a defined route, accept only certain HTTP methods.
* Follow the single responsibility principle.
* Be compatible with any WSGI server, example: [uWSGI](http://uwsgi-docs.readthedocs.org/en/latest/), [Gunicorn](http://gunicorn.org/), [Twisted](http://twistedmatrix.com/), etc.
* Structured Logging using JSON.
* No template rendering.

> Documentation : [docs.zunzun.io](http://docs.zunzun.io)

### What & Why ZunZuncito
ZunZuncito is a [python](http://python.org/) module that allows to create and maintain [REST](http://en.wikipedia.org/wiki/REST) API's with out hassle.

The simplicity for sketching and debugging helps to develop very fast, versioning is inherit by default, which allow to serve and maintain existing applications, while working in new releases without need to create separate instances, all the applications are WSGI [PEP 333](http://www.python.org/dev/peps/pep-0333/) compliant, allowing to migrate existing code to more robust frameworks, without need to modify existing code.

The idea of creating ZunZuncito, was the need of a very small and light tool (batteries included), that could help to create and deploy REST API's quickly, without forcing the developers to learn or follow a complex flow, but in contrast, from the very beginning, guide them to properly structure their API, giving special attention to "versioned URI's", having with this a solid base that allow to work in different versions within a single ZunZun instance without interrupting service of any existing API [resources](http://en.wikipedia.org/wiki/Web_resource).


### How it works

The main application contains a **ZunZun** instance the one must be served by an WSGI compliant server, all request later are handle by custom python modules; ZunZun is the name of the main class for the zunzuncito module.

All the custom python modules, follow the same structure, they basically consist off a class called **APIResource** which contains a method called **dispatch** that will require two arguments: a WSGI environment "environ" as first argument and a function "start_response" that will start the response, [see PEP 333](http://www.python.org/dev/peps/pep-0333/)

ZunZun core turns around three arguments:

    root: The diretory name containing all your API modules see this like the "document_root"
    versions: list of supported versions ['v0', 'v1', 'v2']
    routes: list of tupples containing regex patterns, handlers and allowed http methods

> In the docs you can find a more detailed overview of the ZunZun arguments and the class it self.

When a new request arrive, the ZunZun router parses the REQUEST_URI in order to accomplish this pattern:

    /version/api_resource/arguments

The router first analyse the URI and determines if it is versioned or not by finding a match with the current specified versions, in case none found, failback to the default wich is always the first item on the versions list in case one provieded, or 'v0', afther this proccess the REQUEST_URI becomes a list of resources something like:

    ['version, 'api_resource', 'arguments']

Supose that the incoming request is:

    'http://api.zunzun.io/v1/gevent/ip'

ZunZun will convert convert it to:

    ['v1', 'gevent', 'ip']

The second step on the router is to found a match within the routes list and the local modules, but before going further lets see the directory structure for the root (document_root) the first and required arguemnt for the ZunZun class.

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

As you can see basically is a directory containing sub-directories the ones at the end are all python modules and can be called in a clean way like:

    import my_api.v1.zun_default

    where zun_default if from the api_resource 'default' that ends beein a custom python module

    * notice the prefix zun_

This helps the router to dispatch all the request to an existin module, so continue with the flow, for the incoming request: http://api.zunzun.io/v1/gevent/ip we will try to find a module that matches the API resource 'gevent':


    'http://api.zunzun.io/v1/gevent/ip' ==> ['v1', 'gevent', 'ip']
    version = v1
    api_resource = gevent
    arguments = ip

In case a list of routes is passed as an argument to the ZunZun instance, the router will try to match the api_resource with the items of the rutes list, if no matches found it will try to found the module in the root directory.

The routes format is very simple, it can be something like:

    # format is: regex pattern, handler (python module), allowed HTTP methods (defaults to ALL)
    [
     ('/.*', default),
     ('/test', default, 'POST, PUT, PATCH'),
     ('(?:[0-9]{1,3}\.){3}[0-9]{1,3}', 'ip', 'GET')
    ]

Lets supose this routes where passed to the ZunZun instance, thereforthe router would try to found a match between the api_resource **gevent** in our example with the regex patterns in the list, basically something like:

        gevent in: ['/.*', '/test', '(?:[0-9]{1,3}\.){3}[0-9]{1,3}']

if no match found then the router would try to load the module from the root directory using something like:

    import my_api.v1.zun_gevent

In the case of not founding a module, an HTTP status [501 Not Implemented](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html) code is returned to the client otherwiste the python module is imported by the router and and the request is handler entirely by the imported module


### The zun_ prefix

You may ask, why the need of the "zun_" prefix and why not just create a simple structure having the same name that the api_resource.

Well, this is more due the way python import modules, and basically is to avoid collitions by having same modules with same hame,  you can change the prefix by passing it as an argument to the ZunZun instance or also disabiling it by sending an empty prefix.

In the previous example, the REQUEST_URI contanins an **APIResource** with the word **gevent** the imported module name is in 'zun_gevent/zun_gevent.py' that gives the flexibility to use the [gevent](http://www.gevent.org/) library within your module with out creating any conflic, your zun_gevent.py could look something like:

        import gevent
        import gevent.socket
        ...

that way you could have any work with gevent or any other API resource having identical name of your current python modules with out any conflic.


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


To run it with gunicorn:

    gunicorn -b :8080 -w4 app:app

To run it with uWSGI:

    uwsgi --http :8080 --wsgi-file app.py --callable app --master


### Install

    git clone https://github.com/nbari/zunzuncito.git

    python setup.py install
