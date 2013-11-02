"""
ZunZuncito

micro-framework for creating REST API's
"""

import http_status_codes
import imp
import json
import logging
import os
import re
import urlparse
from itertools import ifilter
from tools import HTTPError, MethodException, HTTPException, LogFormatter
from uuid import uuid4


class ZunZun(object):

    def __init__(self, document_root=None, versions=None, routes=None, suffix='zun', debug=False):
        if document_root:
            self.document_root = os.path.abspath(document_root)
            if not os.access(self.document_root, os.R_OK):
                raise Exception('Document root not readable')
        else:
            raise Exception('Document root missing')

        """versions:
        first in list is treated as the default
        """
        if versions:
            if isinstance(versions, list):
                versions = [x.lower().strip() for x in versions if x and not x.isspace()]
                if versions:
                    self.versions = versions
                else:
                    raise Exception('Versions missing')
            else:
                raise Exception("Versions must be a list, example: ['v0', 'v1', 'v2']")
        else:
            self.versions = ['v0']

        """
        set defauls
        """
        self.request_id = None
        self.resources = []
        self.routes = []
        self.suffix = suffix

        """
        set the logger
        """
        self.log = logging.getLogger()
        logHandler = logging.StreamHandler()
        logformat = LogFormatter('%(asctime) %(filename) %(funcName) %(levelname) %(module) %(name) %(pathname) %(message)')
        logHandler.setFormatter(logformat)
        self.log.addHandler(logHandler)
        self.log.setLevel('DEBUG' if debug else 'ERROR')

        self.log = logging.getLogger()
        self.log.debug({k: str(v) for k, v in self.__dict__.items() if v and k not in 'log'})

        """
        register / compile the routes regex
        """
        if routes:
            self.register_routes(routes)

    def __call__(self, env, start_response):
        """
        try to be compliant with pep 3333 so that any WSGI can serve the app
        """
        self.env = env

        """
        get the REQUEST_ID
        """
        if 'REQUEST_ID' in env:
            self.request_id = env['REQUEST_ID']
        elif 'HTTP_REQUEST_ID' in env:
            self.request_id = env['HTTP_REQUEST_ID']
        else:
            self.request_id = str(uuid4())

        self.log = logging.LoggerAdapter(logging.getLogger(),
                {'rid': self.request_id, 'indent': 4})

        """
        get the HTTP method
        """
        self.method = env['REQUEST_METHOD']

        """
        get the request URI
        """
        if 'REQUEST_URI' in env:
            self.URI = env['REQUEST_URI']
        elif 'PATH_INFO' in env:
            self.URI = env['PATH_INFO']
        else:
            self.URI = '/'

        """
        The portion of the request URL that follows the "?"
        """
        if 'QUERY_STRING' in env:
            self.params = urlparse.parse_qs(env['QUERY_STRING'])

        """
        if debug, log the full environ
        """
        self.log.debug({k: str(env[k]) for k in env if k.isupper()},
                extra={'rid': self.request_id})

        """
        Default values
        """
        status = '200 OK'
        headers = {}
        headers['Content-Type'] = 'application/json; charset=UTF-8'
        body = ''

        try:
            resource = self.router()
            body = resource.dispatch()

            if hasattr(body, 'status'):
                status = getattr(http_status_codes, 'HTTP_%d' % body.status)

            if hasattr(body, 'headers'):
                headers = body.headers

        except HTTPError, e:
            status = getattr(http_status_codes, 'HTTP_%d' % e.status)

            if e.headers:
                headers = e.headers

            if e.title:
                body = e.to_json()

            self.log.debug(dict((x,y) for x, y in (
                ('API', self.version),
                ('URI', self.URI),
                ('HTTPError',status ),
                ('Exception', json.loads(e.to_json()))
                )))

        except Exception, e:
            self.log.error(dict((x,y) for x, y in (
                ('API', self.version),
                ('URI', self.URI),
                ('Exception', e),
                ('environ', {k: str(env[k]) for k in env.keys()})
                )))
            status = getattr(http_status_codes, 'HTTP_%d' % 500)

        headers['Request-ID'] = self.request_id
        start_response(status, list(headers.items()))
        return body

    def router(self):
        """
        check if the URI is versioned (/v1/resource/...) otherwise set it to the
        first version in versions list (default to v0).
        """
        self.version = self.versions[0]
        for version in self.versions:
            if self.URI.lower().startswith('/%s' % version):
                self.version = version
                """
                if URI is versioned, remove the version '/v0' from URI so that regex
                can work, the + 1 if for the starting '/' in the URI
                """
                self.URI = self.URI[len(version) + 1:]
                break

        self.log.debug(dict((x,y) for x, y in (
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
        t[1] = module
        t[2] = data
        """
        filterf = lambda t: any(i in (self.method.upper(), 'ALL') for i in t[2])
        for regex, module, method in ifilter(filterf, self.routes):
            match = regex.match(self.URI)
            if match:
                py_mod = module
                self.log.debug(dict((x,y) for x, y in (
                    ('API', version),
                    ('regex', self.URI),
                    )))
                break

        """
        if no match, try find API resource /py_mod/command/args 'a la SlashQuery'
        """
        if not py_mod:
            self.resources = [x.strip() for x in self.URI.split('?')[0].split('/') if x and not x.isspace()]

            if not self.resources:
                py_mod = 'default'
            else:
                py_mod = self.resources[0]

        """
        by default the _zun suffix is appended, this is to avoid posible
        conflicts, example if you want to have a module call 'gevent' the
        directory structure should be gevent_zun/gevent_zun.py, the URI:
        http://yourapi.tld/gevent/
        you can change the suffix when starting the class
        see PEP: 395
        """
        py_mod = py_mod.lower()
        module_path = os.path.join(self.document_root, '%s/%s_%s/%s_%s.py' % (self.version, py_mod, self.suffix, py_mod, self.suffix))

        if not os.access(module_path, os.R_OK):
            self.log.error(dict((x,y) for x, y in (
                ('API', version),
                ('URI', self.URI),
                ('py_mod', py_mod),
                ('msg', 'py_mod is not readable'),
                )))
            raise HTTPException(500, title="[ %s ] module not readable" % py_mod)
        else:
            mod_name, file_ext = os.path.splitext(os.path.split(module_path)[-1])

            py_mod = imp.load_source(mod_name, module_path)

            try:
                self.log.debug(dict((x,y) for x, y in (
                    ('API', version),
                    ('URI', self.URI),
                    ('dispatching', (mod_name, module_path))
                    )))
                return py_mod.APIResource(self)
            except:
                raise HTTPException(500, title="[ %s ] missing APIResource class" % mod_name)

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
                        methods = [x.strip().upper() for x in route[2].split(',') if x]

                    if regex.startswith('^'):
                        self.routes.append((re.compile(regex), module, methods))
                    else:
                        self.routes.append((re.compile('^%s$' % regex), module, methods))

                    self.log.debug(dict((x,y) for x, y in (("registering regex for route", regex), ("handler", module), ("methods", methods))))
