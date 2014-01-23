"""ZunZuncito - zunzun.io

micro-framework for creating REST API's
"""

import logging
import re
import time

from itertools import ifilter
from uuid import uuid4
from zunzuncito import http_status_codes
from zunzuncito import tools


class ZunZun(object):

    def __init__(self, root, versions=None, hosts=None,
                 routes=None, prefix='zun_', rid=None, debug=False):
        self._headers = tools.CaseInsensitiveDict()
        self.headers = None
        self.host = '*'
        self.hosts = {'*': 'default'}
        self.path = []
        self.prefix = prefix
        self.request_id = None
        self.resource = None
        self.rid = rid
        self.root = root
        self.routes = {}
        self.status = None
        self.versions = ['v0']
        self.version = self.versions[0]
        self.vroot = 'default'

        if versions:
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

        self.log = logging.getLogger()

        if not self.log.handlers:
            self.log.addHandler(logging.StreamHandler())

        self.log.setLevel('DEBUG' if debug else 'INFO')
        self.log.debug(tools.log_json(locals()))

        """
        register / compile the routes regex
        """
        if isinstance(routes, dict):
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
        get the HOST
        """
        if 'HTTP_HOST' in environ:
            self.host = environ['HTTP_HOST'].split(':')[0]

        """
        set the REQUEST_ID
        """
        if self.rid and self.rid in environ:
            self.request_id = environ[self.rid]
        else:
            self.request_id = str(uuid4())

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
        self.headers = self._headers.copy()
        self.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.headers['Request-ID'] = self.request_id
        body = []

        try:
            self.status = 200
            body = self.router().dispatch(environ)
        except tools.HTTPError as e:
            self.status = e.status

            if e.headers:
                self.headers = e.headers

            if e.display:
                body.append(e.to_json())

            self.log.error(tools.log_json({
                'API': self.version,
                'URI': self.URI,
                'HTTPError': self.status,
                'body': e.to_dict()
            }, True)
            )

        except Exception as e:
            self.status = 500
            self.log.error(tools.log_json({
                'API': self.version,
                'URI': self.URI,
                'Exception': e
            }, True)
            )

        if self.status in http_status_codes.codes:
            self.status = http_status_codes.codes[self.status]
        else:
            self.status = http_status_codes.generic_reasons[self.status // 100]

        start_response(self.status, list(self.headers.items()))
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

        self.log.debug(tools.log_json({
            'API': self.version,
            'URI': self.URI,
            'versions': self.versions
        }, True)
        )

        """
        find a python module (py_mod) to handle the request per host
        """
        py_mod = False

        if self.host in self.hosts.keys():
            self.vroot = self.hosts[self.host]
        else:
            for host in self.hosts.keys():
                if re.match('^\*\.', host):
                    domain = '^(?:[^./@]+\.)*%s$' % (
                        host.replace('*.', '').replace('.', '\.'))
                    if re.match(domain, host):
                        self.vroot = self.hosts[host]
                        break

        """
        try to match any supplied routes (regex match)
        only if the current host has defined routes

        t[0] = r - regex
        t[1] = p - py_mod
        t[2] = h - HTTP methods
        """
        if self.routes.get(self.vroot, False):
            filterf = lambda t: any(i in (self.method.upper(), 'ALL')
                                    for i in t[2])
            for r, p, h in ifilter(filterf, self.routes[self.vroot]):
                match = r.match(self.URI)
                if match:
                    py_mod = p
                    self.log.debug(tools.log_json({
                        'HOST': (self.host, self.vroot),
                        'API': self.version,
                        'regex_match': (r.pattern, self.URI),
                        'methods': h
                    }, True)
                    )
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
        module_name = '%s%s' % (self.prefix, py_mod.lower())
        module_path = '%s.%s.%s.%s.%s' % (
            self.root,
            self.vroot,
            self.version,
            module_name,
            module_name)

        try:
            self.log.debug(tools.log_json({
                'HOST': (self.host, self.vroot),
                'API': self.version,
                'URI': self.URI,
                'dispatching': (module_name, module_path)
            }, True)
            )
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
        """compile regex pattern for routes per vroot
        :param routes:
            {
                'vroot': tuple(regex, py_mod, methods).
            }
        """
        for vroot, routes in routes.iteritems():
            gen = (route for route in routes if isinstance(route, tuple))
            vroot = vroot.replace('.', '_')
            self.routes[vroot] = []
            for route in gen:
                regex, module = route[:2]
                methods = ['ALL']

                if len(route) > 2:
                    methods = [x.strip().upper()
                               for x in route[2].split(',') if x]

                if regex.startswith('^'):
                    self.routes[vroot].append(
                        (re.compile(regex), module, methods))
                else:
                    self.routes[vroot].append(
                        (re.compile('^%s$' % regex), module, methods))

                self.log.debug(tools.log_json({
                    'vroot': vroot,
                    "regex": regex,
                    "py_mod": module,
                    "methods": methods
                }, True)
                )
