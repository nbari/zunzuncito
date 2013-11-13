"""twisted multiple process

python tx-app.py
"""

import os
import sys
from os import environ
from sys import argv, executable
from socket import AF_INET

from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from twisted.internet import reactor

sys.path.insert(0, os.path.abspath('..'))

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


def main(fd=None):
    resource = WSGIResource(reactor, reactor.getThreadPool(), app)

    if fd is None:
        # Create a new listening port and several other processes to help out.
        port = reactor.listenTCP(8080, Site(resource))

        for i in range(3):
            reactor.spawnProcess(
                None, executable, [executable, __file__, str(port.fileno())],
                childFDs={0: 0, 1: 1, 2: 2, port.fileno(): port.fileno()},
                env=environ
            )
    else:
        # Another process created the port, just start listening on it.
        port = reactor.adoptStreamPort(fd, AF_INET, Site(resource))

    reactor.run()


if __name__ == '__main__':
    print argv
    if len(argv) == 1:
        main()
    else:
        main(int(argv[1]))
