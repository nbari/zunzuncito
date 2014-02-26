"""
handles the request
"""


class Request(object):

    def __init__(self, logger, request_id, environ):
        self.log = logger
        self.request_id = request_id
        self.environ = environ
        self.URI = '/'
        self.host = None
        self.method = environ['REQUEST_METHOD']
        self.path = []
        self.py_mod = None
        self.resource = None
        self.version = None
        self.vroot = 'default'

        """
        set the HOST
        """
        if 'HTTP_HOST' in environ:
            self.host = environ['HTTP_HOST'].split(':')[0]

        """
        set the request URI
        """
        if 'REQUEST_URI' in environ:
            self.URI = environ['REQUEST_URI']
        elif 'PATH_INFO' in environ:
            self.URI = environ['PATH_INFO']
