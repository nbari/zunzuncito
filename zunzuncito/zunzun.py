"""ZunZuncito - zunzun.io
micro-framework for creating REST API's
"""

import logging
import re
import sys

from uuid import uuid4
from zunzuncito import request
from zunzuncito import response
from zunzuncito import tools


class ZunZun(object):

    def __init__(self, root, versions=None, hosts=None,
                 routes=None, prefix='zun_', rid=None, debug=False):
        self._headers = tools.CaseInsensitiveDict()
        self.host = '*'
        self.hosts = {'*': 'default'}
        if isinstance(hosts, dict):
            self.hosts = hosts
        self.prefix = prefix
        self.resources = {}
        self.rid = rid
        self.root = root
        self.routes = {}
        self.versions = ['v0']
        self.version = self.versions[0]
        self.vroot = 'default'

        if versions:
            if isinstance(versions, list):
                versions = tuple(x.lower().strip()
                                 for x in map(str, versions) if x.strip())
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
        """

        if self.rid and self.rid in environ:
            request_id = environ[self.rid]
        else:
            request_id = str(uuid4())

        req = request.Request(
            self.log,
            request_id,
            environ)

        res = response.Response(
            self.log,
            request_id,
            self._headers.copy(),
            start_response
        )

        body = []

        try:
            body = self.router(req).dispatch(req, res)
        except tools.HTTPError as e:
            res.status = e.status

            if e.headers:
                res.headers.update(e.headers)

            if e.display:
                body.append(e.to_json())

            if e.log:
                self.log.warning(tools.log_json({
                    'API': req.version,
                    'HTTPError': e.status,
                    'URI': req.URI,
                    'body': e.to_dict(),
                    'method': req.method,
                    'rid': req.request_id
                }, True))

        except Exception as e:
            res.status = 500
            self.log.error(tools.log_json({
                'API': req.version,
                'Exception': e,
                'URI': req.URI,
                'method': req.method,
                'rid': req.request_id
            }, True))

        res.send()
        return body or []

    def router(self, req):
        """
        check if the URI is versioned (/v1/resource/...)
        defaults to the first version in versions list (default to v0).
        """
        req.version = self.versions[0]
        for version in self.versions:
            if req.URI.lower().startswith('/%s' % version):
                req.version = version
                """
                if URI is versioned, remove the version '/v0' from URI
                the + 1 if for the starting '/' in the URI
                """
                req.URI = req.URI[len(req.version) + 1:]
                break

        req.log.debug(tools.log_json({
            'API': req.version,
            'URI': req.URI,
            'rid': req.request_id,
            'versions': self.versions
        }, True))

        """
        find a python module (py_mod) to handle the request per host
        """
        py_mod = False

        if req.host in self.hosts.keys():
            req.vroot = self.hosts[req.host]
        else:
            for host in self.hosts.keys():
                if re.match(r'^\*\.', host):
                    domain = r'^(?:[^./@]+\.)*%s$' % (
                        host.replace('*.', '').replace('.', r'\.'))
                    if re.match(domain, host):
                        req.vroot = self.hosts[host]
                        break

        """
        try to match any supplied routes (regex match)
        only if the current host has defined routes

        t[0] = r - regex
        t[1] = p - py_mod
        t[2] = h - HTTP methods
        """
        if self.routes.get(req.vroot, False):
            filterf = lambda t: any(i in (req.method.upper(), 'ALL')
                                    for i in t[2])
            for r, p, h in filter(filterf, self.routes[req.vroot]):
                match = r.match(req.URI)
                if match:
                    py_mod = p
                    req.log.debug(tools.log_json({
                        'HOST': (req.host, req.vroot),
                        'API': req.version,
                        'regex_match': (r.pattern, req.URI),
                        'rid': req.request_id,
                        'methods': h
                    }, True))
                    break

        """
        get the API resource and path from URI api_resource/path
        """
        components = [x.strip()
                      for x in req.URI.split('?')[0].split('/')
                      if x.strip()]

        req.resource = ''.join(components[:1])
        req.path = components[1:]

        if not py_mod:
            """
            URI 2 mod: /add/user/ -> zun_add/zun_user/zun_user.py
            """
            if len(req.path) >= 1 and req.URI.endswith('/'):
                if re.match(r'^[\w-]+$', ''.join(components)):
                    py_mod = components
            else:
                py_mod = 'default' if not components else req.resource

        return self.lazy_load(py_mod, req)

    def lazy_load(self, py_mod, req, stop=False):
        """
        by default the zun_ prefix is appended
        """
        if isinstance(py_mod, list):
            path = '.'.join([self.prefix + i.lower() for i in py_mod])
            name = '%s%s' % (self.prefix, py_mod[-1].lower())
        else:
            path = name = '%s%s' % (self.prefix, py_mod.lower())

        req.py_mod = '%s.%s.%s.%s.%s' % (
            self.root,
            req.vroot,
            req.version,
            path,
            name)

        if req.py_mod in self.resources:
            req.log.debug(tools.log_json({
                'API': req.version,
                'HOST': (req.host, req.vroot),
                'URI': req.URI,
                'dispatching': (name, req.py_mod),
                'rid': req.request_id
            }, True))
            return self.resources[req.py_mod]

        req.log.debug(tools.log_json({
            'API': req.version,
            'HOST': (req.host, req.vroot),
            'URI': req.URI,
            'loading': (name, req.py_mod),
            'rid': req.request_id
        }, True))

        try:
            __import__(req.py_mod, fromlist=[''])
        except ImportError as e:
            if not stop:
                return self.lazy_load('_catchall', req, stop=True)
            raise tools.HTTPException(
                501,
                title="[ %s ] not found" % req.py_mod,
                description=e)

        module = sys.modules[req.py_mod]
        resource = module.__dict__['APIResource']
        self.resources[req.py_mod] = resource()
        return self.resources[req.py_mod]

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
                }, True))
