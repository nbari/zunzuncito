"""twisted

python tx-app.py
"""

from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from twisted.internet import reactor

import zunzuncito

"""Root
Name of the directory containing the API
"""
root = 'my_api'

"""Versions
Supported versions
"""
versions = ['v0', 'v1', 'v2']

"""Route format:
    :URI: a regex matching the URI by default
    :handler: the python module that will handle the request
    :methods: list of allowed methods (comma separated)
        if none all are accepted
"""
routes = [
    # ('/.*', 'default'),
    ('/teste', 'test_get', 'GET'),
    ('/teste', 'test_post', 'POST'),
    ('/teste', 'test_put', 'PUT'),
    ('/my', 'ip_tools', 'GET'),
    ('/status/?.*', 'http_status', 'GET')
]

app = zunzuncito.ZunZun(root, versions, routes, debug=False)

resource = WSGIResource(reactor, reactor.getThreadPool(), app)
reactor.listenTCP(8080, Site(resource))
reactor.run()
