"""
http://mindref.blogspot.pt/2012/09/python-fastest-web-framework.html
https://bitbucket.org/akorn/helloworld/src/f51d4ffb592d/01-welcome/?at=default
"""

import os
import sys

from cStringIO import StringIO as BytesIO
ntob = lambda n, encoding: n

try:
    import cProfile as profile
except ImportError:
    import profile

from pstats import Stats
from timeit import timeit
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

environ = {
    'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;'
                   'q=0.9,*/*;q=0.8',
    'HTTP_ACCEPT_CHARSET': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'HTTP_ACCEPT_ENCODING': 'gzip,deflate,sdch',
    'HTTP_ACCEPT_LANGUAGE': 'uk,en-US;q=0.8,en;q=0.6',
    'HTTP_CACHE_CONTROL': 'max-age=0',
    'HTTP_CONNECTION': 'keep-alive',
    'HTTP_HOST': 'vm0.dev.local:8080',
    'HTTP_USER_AGENT': 'Mozilla/5.0 (X11; Linux i686)',
    'PATH_INFO': '/welcome',
    'QUERY_STRING': '',
    'REMOTE_ADDR': '127.0.0.1',
    'REQUEST_METHOD': 'GET',
    'REQUEST_URI': '/welcome',
    'SCRIPT_NAME': '',
    'SERVER_NAME': 'localhost',
    'SERVER_PORT': '8080',
    'SERVER_PROTOCOL': 'HTTP/1.1',
    'uwsgi.node': 'localhost',
    'uwsgi.version': '1.2.6',
    'wsgi.errors': None,
    'wsgi.file_wrapper': None,
    'wsgi.input': BytesIO(ntob('', 'utf-8')),
    'wsgi.multiprocess': False,
    'wsgi.multithread': False,
    'wsgi.run_once': False,
    'wsgi.url_scheme': 'http',
    'wsgi.version': (1, 0),
}

def start_response(status, headers, exc_info=None):
    return None

frameworks = ['zunzuncito']

sys.path[0] = '.'
path = os.getcwd()

for framework in frameworks:
    os.chdir(os.path.join(path, framework))
    main = __import__('app', None, None, ['main']).main

    f = lambda: list(main(environ.copy(), start_response))
    st = profile.runctx('timeit(f, number=n)', globals(), {'n': 20})

    #profile.run('main(environ.copy(), start_response)')
#    profile.run('f()')

    graphviz = GraphvizOutput()
    graphviz.output_file = 'basic.png'

    with PyCallGraph(output=graphviz):
        main(environ.copy(), start_response)
