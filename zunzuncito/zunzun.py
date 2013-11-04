"""
ZunZuncito

micro-framework for creating REST API's
"""

import imp
import json
import logging
import os
import re

from itertools import ifilter
from uuid import uuid4
from zunzuncito import http_status_codes
from zunzuncito.tools import HTTPError, MethodException, HTTPException, LogFormatter


class ZunZun(object):

    def __init__(self, document_root=None, versions=None,
                 routes=None, suffix='zun', debug=False):
        if document_root:
            self.document_root = os.path.abspath(document_root)
            if not os.access(self.document_root, os.R_OK):
                raise Exception('Document root not readable')
        else:
            raise Exception('Document root missing')

        if versions:
            """versions:
            first in list is treated as the default
            """
            if isinstance(versions, list):
                versions = [x.lower().strip()
                            for x in versions if x and not x.isspace()]
                if versions:
                    self.versions = versions
                else:
                    raise Exception('Versions missing')
            else:
                raise Exception(
                    "Versions must be a list, example: ['v0', 'v1', 'v2']")
        else:
            self.versions = ['v0']

        """
        set defauls
        """
        self.headers = {}
        self.request_id = None
        self.resources = []
        self.routes = []
        self.suffix = suffix
        self.version = self.versions[0]

        """
        set the logger
        """
        self.log = logging.getLogger()
        logHandler = logging.StreamHandler()
        logformat = LogFormatter('%(asctime) %(levelname) %(message)')
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

        """
        get the REQUEST_ID
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
        if 'REQUEST_URI' in environ:
            self.URI = environ['REQUEST_URI']
        elif 'PATH_INFO' in environ:
            self.URI = environ['PATH_INFO']
        else:
            self.URI = '/'

        """
        Default headers in case an exception occurs
        """
        self.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.headers['Request-ID'] = self.request_id
        body = ''

        try:
            resource = self.router()
            return resource.dispatch(environ, start_response)
        except HTTPError as e:
            status = e.status

            if e.headers:
                self.headers = e.headers

            if e.display:
                body = e.to_json()

            self.log.error(dict((x, y) for x, y in (
                ('API', self.version),
                ('URI', self.URI),
                ('HTTPError', status),
                ('body', json.loads(e.to_json()))
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
        t[1] = module
        t[2] = data
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
        if no match, try find API resource /py_mod/command/args
        """
        if not py_mod:
            self.resources = [x.strip()
                              for x in self.URI.split('?')[0].split('/')
                              if x and not x.isspace()]

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
        module_path = os.path.join(self.document_root, '%s/%s_%s/%s_%s.py' % (
            self.version,
            py_mod,
            self.suffix,
            py_mod,
            self.suffix)
        )

        if not os.access(module_path, os.R_OK):
            self.log.error(dict((x, y) for x, y in (
                ('API', self.version),
                ('URI', self.URI),
                ('py_mod', py_mod),
                ('msg', 'py_mod is not readable'),
            )))
            raise HTTPException(
                500,
                title="[ %s ] module not readable" %
                py_mod)
        else:
            mod_name, file_ext = os.path.splitext(
                os.path.split(module_path)[-1])

            py_mod = imp.load_source(mod_name, module_path)

            self.log.debug(dict((x, y) for x, y in (
                ('API', self.version),
                ('URI', self.URI),
                ('dispatching', (mod_name, module_path))
            )))

            try:
                return py_mod.APIResource(self)
            except Exception as e:
                raise HTTPException(500,
                                    title="[ %s ] throw exception" % mod_name,
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
