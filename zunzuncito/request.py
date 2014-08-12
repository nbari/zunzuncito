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

    @property
    def host_url(self):
        """
        The URL through the host (no path)
        """
        e = self.environ
        scheme = e.get('wsgi.url_scheme')
        url = scheme + '://'
        host = e.get('HTTP_HOST')
        if host is not None:
            if ':' in host:
                host, port = host.split(':', 1)
            else:
                port = None
        else:
            host = e.get('SERVER_NAME')
            port = e.get('SERVER_PORT')
        if scheme == 'https':
            if port == '443':
                port = None
        elif scheme == 'http':
            if port == '80':
                port = None
        url += host
        if port:
            url += ':%s' % port
        return url

    def is_secure(self):
        return 'wsgi.url_scheme' in self.environ \
            and self.environ['wsgi.url_scheme'] == 'https'
