"""ZunZuncito - zunzun.io

micro-framework for creating REST API's
"""

import imp
import logging
import re
import time

from itertools import ifilter
from uuid import uuid4
from zunzuncito import http_status_codes
from zunzuncito import tools


class ZunZun(object):

    def __init__(self, root, versions=None,
                 routes=None, prefix='zun_', debug=False):
        """
        set defauls
        """
        self.headers = tools.CaseInsensitiveDict()
        self.path = []
        self.prefix = prefix
        self.request_id = None
        self.resource = None
        self.root = root
        self.routes = []
        self.versions = ['v0']
        self.version = self.versions[0]

        if versions:
            """versions:
            first in list is treated as the default
            """
            if isinstance(versions, list):
                versions = [x.lower().strip()
                            for x in map(str, versions) if x.strip()]
                if versions:
                    self.versions = versions
                else:
                    raise Exception('Versions missing')
            else:
                raise Exception(
                    "Versions must be a list, example: ['v0', 'v1', 'v2']")

        """
        set the logger
        """
        self.log = logging.getLogger()
        logHandler = logging.StreamHandler()
        logformat = tools.LogFormatter('%(asctime) %(levelname) %(message)')
        logHandler.setFormatter(logformat)
        self.log.addHandler(logHandler)
        self.log.setLevel('DEBUG' if debug else 'ERROR')

        self.log = logging.getLogger()
        self.log.debug({k: str(v)
                       for k, v in self.__dict__.items()
                       if v and k not in 'log'})

        """
        register / compile the routes regex
        """
        if routes:
            self.register_routes(routes)

    def __call__(self, environ, start_response):
        """Handle a WSGI application request.

        See pep 3333

        :param environ:
            A WSGI environment
        :param start_response:
            A callable accepting a status code, a list of headers and an
            optional exception context to start the response.
        :returns:
            An iterable with the response to return to the client.
        """
        self.start_time = time.time()

        """
        set the REQUEST_ID
        """
        if 'REQUEST_ID' in environ:
            self.request_id = environ['REQUEST_ID']
        elif 'HTTP_REQUEST_ID' in environ:
            self.request_id = environ['HTTP_REQUEST_ID']
        else:
            self.request_id = str(uuid4())

        self.log = logging.LoggerAdapter(logging.getLogger(), {
            'rid': self.request_id,
            'indent': 4})

        """
        get the HTTP method
        """
        self.method = environ['REQUEST_METHOD']

        """
        get the request URI
        """
        self.URI = '/'

        if 'REQUEST_URI' in environ:
            self.URI = environ['REQUEST_URI']
        elif 'PATH_INFO' in environ:
            self.URI = environ['PATH_INFO']

        """
        Default headers in case an exception occurs
        """
        self.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.headers['Request-ID'] = self.request_id
        body = []

        try:
            resource = self.router()
            return resource.dispatch(environ, start_response)
        except tools.HTTPError as e:
            status = e.status

            if e.headers:
                self.headers = e.headers

            if e.display:
                body.append(e.to_json())

            self.log.error(dict((x, y) for x, y in (
                ('API', self.version),
                ('URI', self.URI),
                ('HTTPError', status),
                ('body', e.to_dict())
            )))

        except Exception as e:
            status = 500
            self.log.error(dict((x, y) for x, y in (
                ('API', self.version),
                ('URI', self.URI),
                ('Exception', e),
                ('environ', environ)
            )))

        start_response(
            getattr(http_status_codes, 'HTTP_%d' %
                    status), list(self.headers.items()))
        return body

    def router(self):
        """
        check if the URI is versioned (/v1/resource/...)
        defaults to the first version in versions list (default to v0).
        """
        self.version = self.versions[0]
        for version in self.versions:
            if self.URI.lower().startswith('/%s' % version):
                self.version = version
                """
                if URI is versioned, remove the version '/v0' from URI
                the + 1 if for the starting '/' in the URI
                """
                self.URI = self.URI[len(version) + 1:]
                break

        self.log.debug(dict((x, y) for x, y in (
            ('API', self.version),
            ('URI', self.URI),
            ('versions', self.versions)
        )))

        """
        find a python module (py_mod) to handle the request
        """
        py_mod = False

        """
        try to match any supplied routes (regex match)

        t[0] = regex
        t[1] = py_mod
        t[2] = HTTP methods
        """
        filterf = lambda t: any(i in (self.method.upper(), 'ALL')
                                for i in t[2])
        for regex, module, method in ifilter(filterf, self.routes):
            match = regex.match(self.URI)
            if match:
                py_mod = module
                self.log.debug(dict((x, y) for x, y in (
                    ('API', self.version),
                    ('regex_match', (regex.pattern, self.URI))
                )))
                break

        """
        get the API resource and path from URI api_resource/path
        """
        components = [x.strip()
                      for x in self.URI.split('?')[0].split('/')
                      if x.strip()]

        self.resource = ''.join(components[:1])
        self.path = components[1:]

        if not py_mod:
            py_mod = 'default' if not components else self.resource

        """
        by default the zun_ prefix is appended
        """
        module_name = '%s%s' % (self.prefix.lower(), py_mod.lower())
        module_path = '%s.%s.%s.%s' % (
            self.root,
            self.version,
            module_name,
            module_name)

        try:
            self.log.debug(dict((x, y) for x, y in (
                ('API', self.version),
                ('URI', self.URI),
                ('dispatching', (module_name, module_path))
            )))
            return __import__(module_path, fromlist=['']).APIResource(self)
        except ImportError as e:
            raise tools.HTTPException(
                501,
                title="[ %s ] not found" % module_name,
                description=e)
        except Exception as e:
            raise tools.HTTPException(
                500,
                title="[ %s ] throw exception" % module_name,
                description=e)

    def register_routes(self, routes):
        """compile regex pattern for routes

        :param routes:
            tuple(regex, handler, methods).
        """
        if routes:
            for route in routes:
                if isinstance(route, tuple):
                    regex, module = route[:2]
                    methods = ['ALL']

                    if len(route) > 2:
                        methods = [x.strip().upper()
                                   for x in route[2].split(',') if x]

                    if regex.startswith('^'):
                        self.routes.append(
                            (re.compile(regex), module, methods))
                    else:
                        self.routes.append(
                            (re.compile('^%s$' % regex), module, methods))

                    self.log.debug(dict((x, y) for x, y in (
                        ("registering regex for route", regex),
                        ("handler", module), ("methods", methods)
                    )))
