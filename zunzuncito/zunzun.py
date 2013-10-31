"""
Main class
"""

import http_status_codes
import imp
import json
import os
import re
import urlparse
from exceptions import HTTPError, MethodException, HTTPException
from itertools import ifilter


class ZunZun(object):

    def __init__(self, document_root=None, routes=None):
        self.routes = []
        self.resources = []

        if document_root:
            self.document_root = os.path.abspath(document_root)
            if not os.access(self.document_root, os.R_OK):
                raise Exception('Document root not readable')
        else:
            raise Exception('Document root missing')

        if routes:
            self.register_routes(routes)


    def __call__(self, env, start_response):
        """
        see pep 3333
        """
        self.env = env

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
        Default values
        """
        status = '200 OK'
        headers = [('Content-Type', 'application/json; charset=utf-8')]
        body = ''

        try:
            resource = self.router()
            body = resource.dispatch()

            if hasattr(body, 'status'):
                status = getattr(http_status_codes, 'HTTP_%d' % body.status)

            if hasattr(body, 'headers'):
                headers = list(body.headers.items())

        except HTTPError, e:
            status = getattr(http_status_codes, 'HTTP_%d' % e.status)

            if e.headers:
                headers = list(e.headers.items())

            if e.title:
                body = e.to_json()

        except Exception, e:
            print e
            status = getattr(http_status_codes, 'HTTP_%d' % 500)
           # body = json.dumps({k: str(env[k]) for k in env.keys()}, sort_keys=True, indent=4)

        start_response(status, headers)
        return body


    def router(self):
        """
        first try to match any supplied routes
        second find resource module/comand/args "a la SlashQuery"
        """

        py_mod = False

        """
        t[0] = regex
        t[1] = module
        t[2] = data
        """
        filterf = lambda t: any(i in (self.method.upper(), 'ALL') for i in t[2])
        for regex, module, method in ifilter(filterf, self.routes):
            match = regex.match(self.URI)
            if match:
                py_mod = module
                continue

        if not py_mod:
            self.resources = [x.strip() for x in self.URI.split('/') if x]

            if not self.resources:
                py_mod = 'default'
            else:
                py_mod = self.resources[0].lower()

        module_path = os.path.join(self.document_root, '%s/%s.py' % (py_mod, py_mod))

        if not os.access(module_path, os.R_OK):
            raise HTTPException(500, title="[ %s ] module not readable" % py_mod)
        else:
            mod_name, file_ext = os.path.splitext(os.path.split(module_path)[-1])

            if file_ext == '.py':
                py_mod = imp.load_source(mod_name, module_path)
            elif file_ext == '.pyc':
                py_mod = imp.load_compiled(mod_name, module_path)

            try:
                return py_mod.APIResource(self)
            except:
                raise HTTPException(500, title="[ %s ] missing APIResource class" % py_mod)


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

                    self.routes.append((re.compile(regex), module, methods))
