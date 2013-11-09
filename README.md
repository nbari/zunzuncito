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

The main application contains a **ZunZun** instance the one must be served by an WSGI compliant server, all request later are handle by custom python modules.

All the custom python modules, follow the same structure, they basically consist off a class called **APIResource** which contains a method called **dispatch** that will require two arguments: a WSGI environment "environ" as first argument and a function "start_response" that will start the response, [see PEP 333](http://www.python.org/dev/peps/pep-0333/)

ZunZun is the name of the main class for the zunzuncito module.

Example:

Contents of file app.py:

    import zunzuncito

    root = 'my_api'
    versions = ['v0', 'v1', 'v2']     
    routes = [
        ('/my', 'ip_tools', 'GET'),
        ('/status', 'http_status', 'GET'),
        ('/upload/', 'test_post', 'PUT, POST')
    ]
    app = zunzuncito.ZunZun(root, versions, routes)


To run it with gunicorn:

    gunicorn -b :8080 -w4 app:app

To run it with uWSGI:

    uwsgi --http :8080 --wsgi-file app.py --callable app --master
    
### Install

`python setup.py install`



 


 
